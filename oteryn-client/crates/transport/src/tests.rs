use super::*;
use crate::session::{test_read_exact, test_write_all};
use oteryn_foundation::{CancellationSource, SessionGeneration};
use std::error::Error;
use std::io;
use std::sync::Arc;
use std::time::Duration;
use tokio::io::{AsyncReadExt, AsyncWriteExt};
use tokio::net::TcpListener;
use tokio::runtime::{Builder, Runtime};
use tokio::time::{sleep, timeout};

#[derive(Debug)]
struct U16TotalLength;

impl FrameBoundary for U16TotalLength {
    fn header_len(&self) -> usize {
        2
    }

    fn complete_frame_len(&self, header: &[u8]) -> Result<usize, TransportError> {
        if header.len() != 2 {
            return Err(TransportError::new(
                TransportErrorKind::InvalidFrameLength,
            ));
        }
        Ok(usize::from(u16::from_le_bytes([header[0], header[1]])))
    }
}

#[derive(Debug)]
struct TerminalBoundary;

impl FrameBoundary for TerminalBoundary {
    fn header_len(&self) -> usize {
        2
    }

    fn complete_frame_len(&self, _header: &[u8]) -> Result<usize, TransportError> {
        Err(TransportError::new(
            TransportErrorKind::InvalidFrameLength,
        ))
    }
}

fn runtime() -> Result<Runtime, io::Error> {
    Builder::new_multi_thread()
        .worker_threads(2)
        .enable_io()
        .enable_time()
        .build()
}

fn config() -> Result<TransportConfig, TransportConfigError> {
    TransportConfig::new(
        Duration::from_secs(2),
        Duration::from_secs(1),
        Duration::from_secs(1),
        128,
        128,
    )?
    .with_idle_timeout(Duration::from_secs(2))?
    .with_queue_capacities(4, 4, 2)
}

#[test]
fn configuration_retains_limits_and_explicit_queue_bounds() -> Result<(), Box<dyn Error>> {
    let over = Duration::from_secs(31);
    assert_eq!(
        TransportConfig::new(
            over,
            Duration::from_secs(1),
            Duration::from_secs(1),
            1,
            1,
        ),
        Err(TransportConfigError::TimeoutTooLarge)
    );
    assert_eq!(
        config()?.with_queue_capacities(0, 1, 1),
        Err(TransportConfigError::InvalidQueueCapacity)
    );
    assert_eq!(
        config()?.with_idle_timeout(Duration::ZERO),
        Err(TransportConfigError::ZeroTimeout)
    );
    Ok(())
}

#[test]
fn full_duplex_loopback_preserves_frames_and_joins() -> Result<(), Box<dyn Error>> {
    runtime()?.block_on(async {
        let listener = TcpListener::bind("127.0.0.1:0").await?;
        let endpoint = listener.local_addr()?;
        let server = tokio::spawn(async move {
            let (mut socket, _peer) = listener.accept().await?;
            let mut request = [0_u8; 5];
            socket.read_exact(&mut request).await?;
            if request != [5, 0, 1, 2, 3] {
                return Err(io::Error::other("unexpected outbound frame"));
            }
            socket.write_all(&[5, 0, 9, 8, 7]).await?;
            socket.flush().await?;
            let mut shutdown_probe = [0_u8; 1];
            let _bytes = socket.read(&mut shutdown_probe).await?;
            Ok::<(), io::Error>(())
        });

        let cancellation = CancellationSource::new();
        let generation = SessionGeneration::new(7);
        let mut session = TransportSession::connect(
            endpoint,
            generation,
            config()?,
            Arc::new(U16TotalLength),
            &cancellation.token(),
        )
        .await?;
        session.try_send(
            generation,
            OutboundPriority::Gameplay,
            vec![5, 0, 1, 2, 3],
        )?;

        let frame = timeout(Duration::from_secs(2), async {
            loop {
                if let Some(frame) = session.try_recv()? {
                    return Ok::<InboundFrame, TransportError>(frame);
                }
                tokio::task::yield_now().await;
            }
        })
        .await??;
        assert_eq!(frame.generation(), generation);
        assert_eq!(frame.bytes(), &[5, 0, 9, 8, 7]);
        let metrics = session.metrics();
        assert_eq!(metrics.inbound_frames, 1);
        assert_eq!(metrics.outbound_frames, 1);
        assert!(metrics.gameplay_queue_high_water >= 1);

        session.close();
        assert_eq!(session.status().state(), ConnectionState::Closing);
        let summary = session.join().await?;
        server.await??;
        assert_eq!(summary.generation(), generation);
        assert_eq!(summary.metrics().inbound_frames, 1);
        Ok::<(), Box<dyn Error>>(())
    })
}

#[test]
fn stale_generation_and_oversized_outbound_are_rejected_before_io() -> Result<(), Box<dyn Error>> {
    runtime()?.block_on(async {
        let listener = TcpListener::bind("127.0.0.1:0").await?;
        let endpoint = listener.local_addr()?;
        let server = tokio::spawn(async move {
            let (_socket, _peer) = listener.accept().await?;
            sleep(Duration::from_millis(100)).await;
            Ok::<(), io::Error>(())
        });
        let cancellation = CancellationSource::new();
        let generation = SessionGeneration::new(3);
        let mut session = TransportSession::connect(
            endpoint,
            generation,
            config()?,
            Arc::new(U16TotalLength),
            &cancellation.token(),
        )
        .await?;

        assert_eq!(
            session.try_send(
                SessionGeneration::new(4),
                OutboundPriority::Gameplay,
                vec![2, 0],
            ),
            Err(TransportError::new(TransportErrorKind::StaleSession))
        );
        assert_eq!(
            session.try_send(
                generation,
                OutboundPriority::Gameplay,
                vec![0_u8; 129],
            ),
            Err(TransportError::new(TransportErrorKind::FrameTooLarge))
        );

        session.close();
        let _summary = session.join().await?;
        server.await??;
        Ok::<(), Box<dyn Error>>(())
    })
}

#[test]
fn malformed_and_protocol_terminal_lengths_close_before_body_allocation()
-> Result<(), Box<dyn Error>> {
    runtime()?.block_on(async {
        let listener = TcpListener::bind("127.0.0.1:0").await?;
        let endpoint = listener.local_addr()?;
        let server = tokio::spawn(async move {
            let (mut socket, _peer) = listener.accept().await?;
            socket.write_all(&[255, 0]).await?;
            socket.flush().await?;
            Ok::<(), io::Error>(())
        });
        let cancellation = CancellationSource::new();
        let session = TransportSession::connect(
            endpoint,
            SessionGeneration::new(1),
            config()?,
            Arc::new(U16TotalLength),
            &cancellation.token(),
        )
        .await?;
        assert_eq!(
            session.wait().await,
            Err(TransportError::new(TransportErrorKind::FrameTooLarge))
        );
        server.await??;

        let listener = TcpListener::bind("127.0.0.1:0").await?;
        let endpoint = listener.local_addr()?;
        let server = tokio::spawn(async move {
            let (mut socket, _peer) = listener.accept().await?;
            socket.write_all(&[2, 0]).await?;
            socket.flush().await?;
            Ok::<(), io::Error>(())
        });
        let session = TransportSession::connect(
            endpoint,
            SessionGeneration::new(2),
            config()?,
            Arc::new(TerminalBoundary),
            &cancellation.token(),
        )
        .await?;
        assert_eq!(
            session.wait().await,
            Err(TransportError::new(TransportErrorKind::ProtocolTerminal))
        );
        server.await??;
        Ok::<(), Box<dyn Error>>(())
    })
}

#[test]
fn idle_deadline_and_preconnect_cancellation_are_typed() -> Result<(), Box<dyn Error>> {
    runtime()?.block_on(async {
        let listener = TcpListener::bind("127.0.0.1:0").await?;
        let endpoint = listener.local_addr()?;
        let server = tokio::spawn(async move {
            let (_socket, _peer) = listener.accept().await?;
            sleep(Duration::from_millis(100)).await;
            Ok::<(), io::Error>(())
        });
        let idle_config = TransportConfig::new(
            Duration::from_secs(1),
            Duration::from_secs(1),
            Duration::from_secs(1),
            64,
            64,
        )?
        .with_idle_timeout(Duration::from_millis(20))?;
        let cancellation = CancellationSource::new();
        let session = TransportSession::connect(
            endpoint,
            SessionGeneration::new(1),
            idle_config,
            Arc::new(U16TotalLength),
            &cancellation.token(),
        )
        .await?;
        assert_eq!(
            session.wait().await,
            Err(TransportError::new(TransportErrorKind::IdleTimeout))
        );
        server.await??;

        let cancelled = CancellationSource::new();
        let _changed = cancelled.cancel();
        let result = TransportSession::connect(
            endpoint,
            SessionGeneration::new(2),
            config()?,
            Arc::new(U16TotalLength),
            &cancelled.token(),
        )
        .await;
        assert_eq!(
            result.err(),
            Some(TransportError::new(TransportErrorKind::Cancelled))
        );
        Ok::<(), Box<dyn Error>>(())
    })
}

#[test]
fn external_cancellation_interrupts_connected_read_and_joins() -> Result<(), Box<dyn Error>> {
    runtime()?.block_on(async {
        let listener = TcpListener::bind("127.0.0.1:0").await?;
        let endpoint = listener.local_addr()?;
        let server = tokio::spawn(async move {
            let (_socket, _peer) = listener.accept().await?;
            sleep(Duration::from_millis(100)).await;
            Ok::<(), io::Error>(())
        });
        let cancellation = CancellationSource::new();
        let session = TransportSession::connect(
            endpoint,
            SessionGeneration::new(8),
            config()?,
            Arc::new(U16TotalLength),
            &cancellation.token(),
        )
        .await?;
        let _changed = cancellation.cancel();
        assert_eq!(
            timeout(Duration::from_secs(1), session.wait()).await?,
            Err(TransportError::new(TransportErrorKind::Cancelled))
        );
        server.await??;
        Ok::<(), Box<dyn Error>>(())
    })
}

#[test]
fn inbound_saturation_does_not_starve_control_cancellation() -> Result<(), Box<dyn Error>> {
    runtime()?.block_on(async {
        let listener = TcpListener::bind("127.0.0.1:0").await?;
        let endpoint = listener.local_addr()?;
        let server = tokio::spawn(async move {
            let (mut socket, _peer) = listener.accept().await?;
            socket.write_all(&[2, 0, 2, 0]).await?;
            socket.flush().await?;
            sleep(Duration::from_millis(100)).await;
            Ok::<(), io::Error>(())
        });
        let saturated = config()?.with_queue_capacities(1, 1, 1)?;
        let cancellation = CancellationSource::new();
        let session = TransportSession::connect(
            endpoint,
            SessionGeneration::new(9),
            saturated,
            Arc::new(U16TotalLength),
            &cancellation.token(),
        )
        .await?;
        sleep(Duration::from_millis(10)).await;
        let _changed = cancellation.cancel();
        assert_eq!(
            timeout(Duration::from_secs(1), session.wait()).await?,
            Err(TransportError::new(TransportErrorKind::Cancelled))
        );
        server.await??;
        Ok::<(), Box<dyn Error>>(())
    })
}

#[test]
fn partial_io_timeout_and_eof_are_typed_without_truncation() -> Result<(), Box<dyn Error>> {
    runtime()?.block_on(async {
        let (mut client, mut server) = tokio::io::duplex(2);
        let writer = tokio::spawn(async move {
            server.write_all(&[1, 2]).await?;
            tokio::task::yield_now().await;
            server.write_all(&[3, 4, 5]).await?;
            Ok::<(), io::Error>(())
        });
        let mut received = [0_u8; 5];
        test_read_exact(&mut client, &mut received, Duration::from_secs(1)).await?;
        assert_eq!(received, [1, 2, 3, 4, 5]);
        writer.await??;

        let (mut client, mut server) = tokio::io::duplex(2);
        let reader = tokio::spawn(async move {
            let mut received = [0_u8; 5];
            server.read_exact(&mut received).await?;
            Ok::<[u8; 5], io::Error>(received)
        });
        test_write_all(
            &mut client,
            &[9, 8, 7, 6, 5],
            Duration::from_secs(1),
        )
        .await?;
        assert_eq!(reader.await??, [9, 8, 7, 6, 5]);

        let (mut client, _server) = tokio::io::duplex(1);
        let mut byte = [0_u8; 1];
        assert_eq!(
            test_read_exact(&mut client, &mut byte, Duration::from_millis(10)).await,
            Err(TransportError::new(TransportErrorKind::Timeout))
        );

        let (mut client, _server) = tokio::io::duplex(1);
        assert_eq!(
            test_write_all(&mut client, &[1, 2, 3], Duration::from_millis(10)).await,
            Err(TransportError::new(TransportErrorKind::Timeout))
        );

        let (mut client, server) = tokio::io::duplex(1);
        drop(server);
        assert_eq!(
            test_read_exact(&mut client, &mut byte, Duration::from_secs(1)).await,
            Err(TransportError::new(TransportErrorKind::ConnectionLost))
        );
        Ok::<(), Box<dyn Error>>(())
    })
}

#[test]
fn shutdown_with_queued_work_and_repeated_cycles_leave_no_session_task()
-> Result<(), Box<dyn Error>> {
    runtime()?.block_on(async {
        for generation_value in 1_u64..=16 {
            let listener = TcpListener::bind("127.0.0.1:0").await?;
            let endpoint = listener.local_addr()?;
            let server = tokio::spawn(async move {
                let (mut socket, _peer) = listener.accept().await?;
                let mut buffer = [0_u8; 16];
                loop {
                    if socket.read(&mut buffer).await? == 0 {
                        break;
                    }
                }
                Ok::<(), io::Error>(())
            });
            let cancellation = CancellationSource::new();
            let generation = SessionGeneration::new(generation_value);
            let mut session = TransportSession::connect(
                endpoint,
                generation,
                config()?,
                Arc::new(U16TotalLength),
                &cancellation.token(),
            )
            .await?;
            session.try_send(
                generation,
                OutboundPriority::Background,
                vec![2, 0],
            )?;
            session.close();
            let summary = timeout(Duration::from_secs(1), session.join()).await??;
            assert_eq!(summary.generation(), generation);
            server.await??;
        }
        Ok::<(), Box<dyn Error>>(())
    })
}
