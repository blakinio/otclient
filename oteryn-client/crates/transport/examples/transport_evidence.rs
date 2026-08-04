#[cfg(not(feature = "blocking-baseline"))]
fn main() {
    println!("transport_evidence requires --features blocking-baseline");
}

#[cfg(feature = "blocking-baseline")]
mod enabled {
    use oteryn_foundation::{CancellationSource, SessionGeneration};
    use oteryn_transport::{
        BlockingTcpTransport, BlockingTransportConfig, FrameBoundary, InboundFrame,
        OutboundPriority, TransportConfig, TransportError, TransportErrorKind, TransportSession,
    };
    use std::error::Error;
    use std::io::{Read, Write};
    use std::net::{TcpListener as BlockingListener, TcpStream as BlockingStream};
    use std::sync::Arc;
    use std::thread;
    use std::time::{Duration, Instant};
    use tokio::io::{AsyncReadExt, AsyncWriteExt};
    use tokio::net::TcpListener;
    use tokio::runtime::Builder;
    use tokio::time::{sleep, timeout};

    const FRAME_BYTES: usize = 64;
    const LATENCY_SAMPLES: usize = 200;
    const BURST_FRAMES: usize = 1_000;
    const TOTAL_FRAMES: usize = LATENCY_SAMPLES + BURST_FRAMES;

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
    struct Evidence {
        p50_us: u128,
        p95_us: u128,
        p99_us: u128,
        burst_frames_per_second: f64,
        shutdown_us: u128,
        queue_high_water: Option<usize>,
        queue_full: Option<u64>,
        slow_consumer_cancel_us: Option<u128>,
    }

    pub fn run() -> Result<(), Box<dyn Error>> {
        let blocking = blocking_evidence()?;
        let tokio = tokio_evidence()?;
        print_evidence("blocking", &blocking);
        print_evidence("tokio", &tokio);
        println!("scope=deterministic_loopback_queue_and_scheduler_evidence");
        println!("physical_rtt_claim=false");
        Ok(())
    }

    fn blocking_evidence() -> Result<Evidence, Box<dyn Error>> {
        let listener = BlockingListener::bind("127.0.0.1:0")?;
        let endpoint = listener.local_addr()?;
        let server = thread::spawn(move || -> Result<(), std::io::Error> {
            let (mut stream, _peer) = listener.accept()?;
            echo_blocking(&mut stream, TOTAL_FRAMES)?;
            let mut shutdown_probe = [0_u8; 1];
            let _bytes = stream.read(&mut shutdown_probe)?;
            Ok(())
        });
        let cancellation = CancellationSource::new();
        let config = BlockingTransportConfig::new(
            Duration::from_secs(2),
            Duration::from_secs(2),
            Duration::from_secs(2),
            FRAME_BYTES,
            FRAME_BYTES,
        )?;
        let mut transport = BlockingTcpTransport::new(config);
        transport.connect(endpoint, &cancellation.token())?;
        let frame = frame();
        let mut samples = Vec::with_capacity(LATENCY_SAMPLES);
        for _ in 0..LATENCY_SAMPLES {
            let started = Instant::now();
            transport.write_all_bounded(&frame, &cancellation.token())?;
            let response = transport.read_exact_bounded(FRAME_BYTES, &cancellation.token())?;
            if response != frame {
                return Err("blocking loopback response mismatch".into());
            }
            samples.push(started.elapsed());
        }

        let burst_started = Instant::now();
        for _ in 0..BURST_FRAMES {
            transport.write_all_bounded(&frame, &cancellation.token())?;
            let response = transport.read_exact_bounded(FRAME_BYTES, &cancellation.token())?;
            if response != frame {
                return Err("blocking burst response mismatch".into());
            }
        }
        let burst_elapsed = burst_started.elapsed();
        let shutdown_started = Instant::now();
        transport.close();
        let shutdown_us = shutdown_started.elapsed().as_micros();
        server
            .join()
            .map_err(|_| "blocking evidence server panicked")??;
        let percentiles = percentiles(&mut samples);
        Ok(Evidence {
            p50_us: percentiles.0,
            p95_us: percentiles.1,
            p99_us: percentiles.2,
            burst_frames_per_second: frames_per_second(BURST_FRAMES, burst_elapsed),
            shutdown_us,
            queue_high_water: None,
            queue_full: None,
            slow_consumer_cancel_us: None,
        })
    }

    fn tokio_evidence() -> Result<Evidence, Box<dyn Error>> {
        Builder::new_multi_thread()
            .worker_threads(2)
            .enable_io()
            .enable_time()
            .build()?
            .block_on(async {
                let listener = TcpListener::bind("127.0.0.1:0").await?;
                let endpoint = listener.local_addr()?;
                let server = tokio::spawn(async move {
                    let (mut stream, _peer) = listener.accept().await?;
                    echo_tokio(&mut stream, TOTAL_FRAMES).await?;
                    let mut shutdown_probe = [0_u8; 1];
                    let _bytes = stream.read(&mut shutdown_probe).await?;
                    Ok::<(), std::io::Error>(())
                });
                let cancellation = CancellationSource::new();
                let config = TransportConfig::new(
                    Duration::from_secs(2),
                    Duration::from_secs(2),
                    Duration::from_secs(2),
                    FRAME_BYTES,
                    FRAME_BYTES,
                )?
                .with_idle_timeout(Duration::from_secs(5))?
                .with_queue_capacities(1_024, 1_024, 64)?;
                let generation = SessionGeneration::new(1);
                let mut transport = TransportSession::connect(
                    endpoint,
                    generation,
                    config,
                    Arc::new(U16TotalLength),
                    &cancellation.token(),
                )
                .await?;
                let frame = frame();
                let mut samples = Vec::with_capacity(LATENCY_SAMPLES);
                for _ in 0..LATENCY_SAMPLES {
                    let started = Instant::now();
                    transport.try_send(
                        generation,
                        OutboundPriority::Gameplay,
                        frame.clone(),
                    )?;
                    let response = receive_one(&mut transport).await?;
                    if response.bytes() != frame {
                        return Err("Tokio loopback response mismatch".into());
                    }
                    samples.push(started.elapsed());
                }

                let burst_started = Instant::now();
                for _ in 0..BURST_FRAMES {
                    transport.try_send(
                        generation,
                        OutboundPriority::Gameplay,
                        frame.clone(),
                    )?;
                }
                for _ in 0..BURST_FRAMES {
                    let response = receive_one(&mut transport).await?;
                    if response.bytes() != frame {
                        return Err("Tokio burst response mismatch".into());
                    }
                }
                let burst_elapsed = burst_started.elapsed();
                let metrics = transport.metrics();
                let shutdown_started = Instant::now();
                transport.close();
                let _summary = transport.join().await?;
                let shutdown_us = shutdown_started.elapsed().as_micros();
                server.await??;

                let (slow_high_water, slow_queue_full, slow_cancel_us) =
                    slow_consumer_evidence().await?;
                let percentiles = percentiles(&mut samples);
                Ok::<Evidence, Box<dyn Error>>(Evidence {
                    p50_us: percentiles.0,
                    p95_us: percentiles.1,
                    p99_us: percentiles.2,
                    burst_frames_per_second: frames_per_second(BURST_FRAMES, burst_elapsed),
                    shutdown_us,
                    queue_high_water: Some(
                        metrics
                            .gameplay_queue_high_water
                            .max(metrics.inbound_queue_high_water)
                            .max(slow_high_water),
                    ),
                    queue_full: Some(metrics.outbound_queue_full + slow_queue_full),
                    slow_consumer_cancel_us: Some(slow_cancel_us),
                })
            })
    }

    async fn slow_consumer_evidence() -> Result<(usize, u64, u128), Box<dyn Error>> {
        let listener = TcpListener::bind("127.0.0.1:0").await?;
        let endpoint = listener.local_addr()?;
        let server = tokio::spawn(async move {
            let (mut stream, _peer) = listener.accept().await?;
            let frame = frame();
            for _ in 0..64 {
                stream.write_all(&frame).await?;
            }
            stream.flush().await?;
            let mut shutdown_probe = [0_u8; 1];
            let _bytes = stream.read(&mut shutdown_probe).await?;
            Ok::<(), std::io::Error>(())
        });
        let cancellation = CancellationSource::new();
        let config = TransportConfig::new(
            Duration::from_secs(2),
            Duration::from_secs(2),
            Duration::from_secs(2),
            FRAME_BYTES,
            FRAME_BYTES,
        )?
        .with_idle_timeout(Duration::from_secs(5))?
        .with_queue_capacities(8, 8, 8)?;
        let transport = TransportSession::connect(
            endpoint,
            SessionGeneration::new(2),
            config,
            Arc::new(U16TotalLength),
            &cancellation.token(),
        )
        .await?;
        sleep(Duration::from_millis(25)).await;
        let metrics = transport.metrics();
        let cancel_started = Instant::now();
        let _changed = cancellation.cancel();
        let terminal = timeout(Duration::from_secs(1), transport.wait()).await??;
        drop(terminal);
        let cancel_us = cancel_started.elapsed().as_micros();
        server.await??;
        Ok((
            metrics.inbound_queue_high_water,
            metrics.outbound_queue_full,
            cancel_us,
        ))
    }

    async fn receive_one(
        transport: &mut TransportSession,
    ) -> Result<InboundFrame, Box<dyn Error>> {
        timeout(Duration::from_secs(2), async {
            loop {
                if let Some(frame) = transport.try_recv()? {
                    return Ok::<InboundFrame, TransportError>(frame);
                }
                tokio::task::yield_now().await;
            }
        })
        .await?
        .map_err(Into::into)
    }

    fn echo_blocking(
        stream: &mut BlockingStream,
        frames: usize,
    ) -> Result<(), std::io::Error> {
        let mut frame = [0_u8; FRAME_BYTES];
        for _ in 0..frames {
            stream.read_exact(&mut frame)?;
            stream.write_all(&frame)?;
        }
        stream.flush()
    }

    async fn echo_tokio(
        stream: &mut tokio::net::TcpStream,
        frames: usize,
    ) -> Result<(), std::io::Error> {
        let mut frame = [0_u8; FRAME_BYTES];
        for _ in 0..frames {
            stream.read_exact(&mut frame).await?;
            stream.write_all(&frame).await?;
        }
        stream.flush().await
    }

    fn frame() -> Vec<u8> {
        let mut frame = vec![0_u8; FRAME_BYTES];
        let length = u16::try_from(FRAME_BYTES).unwrap_or(u16::MAX);
        frame[..2].copy_from_slice(&length.to_le_bytes());
        for (index, byte) in frame[2..].iter_mut().enumerate() {
            *byte = u8::try_from(index % 251).unwrap_or(0);
        }
        frame
    }

    fn percentiles(samples: &mut [Duration]) -> (u128, u128, u128) {
        samples.sort_unstable();
        (
            percentile(samples, 50),
            percentile(samples, 95),
            percentile(samples, 99),
        )
    }

    fn percentile(samples: &[Duration], percentile: usize) -> u128 {
        let last = samples.len().saturating_sub(1);
        let index = last.saturating_mul(percentile) / 100;
        samples
            .get(index)
            .copied()
            .unwrap_or(Duration::ZERO)
            .as_micros()
    }

    fn frames_per_second(frames: usize, elapsed: Duration) -> f64 {
        let seconds = elapsed.as_secs_f64();
        if seconds == 0.0 {
            0.0
        } else {
            frames as f64 / seconds
        }
    }

    fn print_evidence(name: &str, evidence: &Evidence) {
        println!("{name}.queue_latency_us.p50={}", evidence.p50_us);
        println!("{name}.queue_latency_us.p95={}", evidence.p95_us);
        println!("{name}.queue_latency_us.p99={}", evidence.p99_us);
        println!(
            "{name}.burst_frames_per_second={:.2}",
            evidence.burst_frames_per_second
        );
        println!("{name}.shutdown_us={}", evidence.shutdown_us);
        match evidence.queue_high_water {
            Some(value) => println!("{name}.queue_high_water={value}"),
            None => println!("{name}.queue_high_water=not_applicable"),
        }
        match evidence.queue_full {
            Some(value) => println!("{name}.queue_full={value}"),
            None => println!("{name}.queue_full=not_applicable"),
        }
        match evidence.slow_consumer_cancel_us {
            Some(value) => println!("{name}.slow_consumer_cancel_us={value}"),
            None => println!("{name}.slow_consumer_cancel_us=not_applicable"),
        }
    }
}

#[cfg(feature = "blocking-baseline")]
fn main() -> Result<(), Box<dyn std::error::Error>> {
    enabled::run()
}
