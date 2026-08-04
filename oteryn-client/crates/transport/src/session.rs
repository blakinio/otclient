use crate::config::MAX_FRAME_HEADER_BYTES;
use crate::framing::validate_complete_frame_len;
use crate::{
    ConnectionState, FrameBoundary, InboundFrame, OutboundPriority, TransportConfig,
    TransportError, TransportErrorKind,
};
use oteryn_foundation::{CancellationToken, SessionGeneration};
use std::future::Future;
use std::io;
use std::net::SocketAddr;
use std::sync::Arc;
use std::sync::atomic::{AtomicU64, AtomicUsize, Ordering};
use std::time::Duration;
use tokio::io::{AsyncRead, AsyncReadExt, AsyncWrite, AsyncWriteExt};
use tokio::net::TcpStream;
use tokio::sync::{mpsc, watch};
use tokio::task::{JoinHandle, JoinSet};
use tokio::time::{sleep, timeout};

const CANCELLATION_OBSERVATION_INTERVAL: Duration = Duration::from_millis(1);

/// Latest terminal-safe state of one transport session.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SessionStatus {
    state: ConnectionState,
    terminal_error: Option<TransportErrorKind>,
}

impl SessionStatus {
    const fn connected() -> Self {
        Self {
            state: ConnectionState::Connected,
            terminal_error: None,
        }
    }

    const fn closing() -> Self {
        Self {
            state: ConnectionState::Closing,
            terminal_error: None,
        }
    }

    const fn closed(terminal_error: Option<TransportErrorKind>) -> Self {
        Self {
            state: ConnectionState::Closed,
            terminal_error,
        }
    }

    /// Return the deterministic lifecycle state.
    #[must_use]
    pub const fn state(self) -> ConnectionState {
        self.state
    }

    /// Return the stable terminal failure, when shutdown was not clean.
    #[must_use]
    pub const fn terminal_error(self) -> Option<TransportErrorKind> {
        self.terminal_error
    }
}

/// Bounded non-secret transport counters.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransportMetricsSnapshot {
    /// Complete inbound frames delivered to the application queue.
    pub inbound_frames: u64,
    /// Complete outbound frames written to the socket.
    pub outbound_frames: u64,
    /// Complete inbound bytes delivered to the application queue.
    pub inbound_bytes: u64,
    /// Complete outbound bytes written to the socket.
    pub outbound_bytes: u64,
    /// Outbound frames rejected because a bounded queue was full.
    pub outbound_queue_full: u64,
    /// Highest observed inbound queue occupancy.
    pub inbound_queue_high_water: usize,
    /// Highest observed gameplay queue occupancy.
    pub gameplay_queue_high_water: usize,
    /// Highest observed background queue occupancy.
    pub background_queue_high_water: usize,
}

#[derive(Debug, Default)]
struct TransportMetrics {
    inbound_frames: AtomicU64,
    outbound_frames: AtomicU64,
    inbound_bytes: AtomicU64,
    outbound_bytes: AtomicU64,
    outbound_queue_full: AtomicU64,
    inbound_depth: AtomicUsize,
    gameplay_depth: AtomicUsize,
    background_depth: AtomicUsize,
    inbound_high_water: AtomicUsize,
    gameplay_high_water: AtomicUsize,
    background_high_water: AtomicUsize,
}

impl TransportMetrics {
    fn snapshot(&self) -> TransportMetricsSnapshot {
        TransportMetricsSnapshot {
            inbound_frames: self.inbound_frames.load(Ordering::Acquire),
            outbound_frames: self.outbound_frames.load(Ordering::Acquire),
            inbound_bytes: self.inbound_bytes.load(Ordering::Acquire),
            outbound_bytes: self.outbound_bytes.load(Ordering::Acquire),
            outbound_queue_full: self.outbound_queue_full.load(Ordering::Acquire),
            inbound_queue_high_water: self.inbound_high_water.load(Ordering::Acquire),
            gameplay_queue_high_water: self.gameplay_high_water.load(Ordering::Acquire),
            background_queue_high_water: self.background_high_water.load(Ordering::Acquire),
        }
    }
}

#[derive(Debug)]
struct OutboundFrame {
    bytes: Vec<u8>,
}

/// Joined terminal result of one session supervisor.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SessionSummary {
    generation: SessionGeneration,
    metrics: TransportMetricsSnapshot,
}

impl SessionSummary {
    /// Return the fenced session generation.
    #[must_use]
    pub const fn generation(self) -> SessionGeneration {
        self.generation
    }

    /// Return the final bounded counters.
    #[must_use]
    pub const fn metrics(self) -> TransportMetricsSnapshot {
        self.metrics
    }
}

/// Application-facing handle to one bounded full-duplex Tokio TCP session.
///
/// The handle owns no runtime. It must be created and awaited from the
/// application-owned Tokio runtime. Dropping it cancels and aborts the complete
/// supervisor tree; normal lifecycle code should call [`Self::close`] and
/// [`Self::join`] for deterministic joined shutdown.
pub struct TransportSession {
    generation: SessionGeneration,
    config: TransportConfig,
    gameplay_tx: mpsc::Sender<OutboundFrame>,
    background_tx: mpsc::Sender<OutboundFrame>,
    inbound_rx: mpsc::Receiver<InboundFrame>,
    cancel_tx: watch::Sender<bool>,
    status_tx: watch::Sender<SessionStatus>,
    status_rx: watch::Receiver<SessionStatus>,
    supervisor: Option<JoinHandle<Result<SessionSummary, TransportError>>>,
    metrics: Arc<TransportMetrics>,
    close_requested: bool,
}

impl TransportSession {
    /// Connect and start exactly one bounded reader, writer and supervisor tree.
    ///
    /// # Errors
    ///
    /// Returns a stable error for cancellation, timeout, invalid framing bounds,
    /// TCP setup failure or resource exhaustion.
    pub async fn connect(
        endpoint: SocketAddr,
        generation: SessionGeneration,
        config: TransportConfig,
        boundary: Arc<dyn FrameBoundary>,
        cancellation: &CancellationToken,
    ) -> Result<Self, TransportError> {
        let header_len = boundary.header_len();
        if header_len == 0 || header_len > MAX_FRAME_HEADER_BYTES {
            return Err(TransportError::new(TransportErrorKind::InvalidFrameLength));
        }

        let stream = connect_with_deadline(
            TcpStream::connect(endpoint),
            config.connect_timeout(),
            cancellation,
        )
        .await?;
        stream
            .set_nodelay(true)
            .map_err(|error| classify_connect_error(&error))?;

        let (gameplay_tx, gameplay_rx) = mpsc::channel(config.gameplay_queue_capacity());
        let (background_tx, background_rx) = mpsc::channel(config.background_queue_capacity());
        let (inbound_tx, inbound_rx) = mpsc::channel(config.inbound_queue_capacity());
        let (cancel_tx, cancel_rx) = watch::channel(false);
        let (status_tx, status_rx) = watch::channel(SessionStatus::connected());
        let metrics = Arc::new(TransportMetrics::default());
        let supervisor_metrics = Arc::clone(&metrics);
        let supervisor_cancel = cancel_tx.clone();
        let supervisor_status = status_tx.clone();
        let external_cancellation = cancellation.clone();
        let supervisor = tokio::spawn(run_session(
            stream,
            generation,
            config,
            boundary,
            gameplay_rx,
            background_rx,
            inbound_tx,
            cancel_rx,
            supervisor_cancel,
            supervisor_status,
            external_cancellation,
            supervisor_metrics,
        ));

        Ok(Self {
            generation,
            config,
            gameplay_tx,
            background_tx,
            inbound_rx,
            cancel_tx,
            status_tx,
            status_rx,
            supervisor: Some(supervisor),
            metrics,
            close_requested: false,
        })
    }

    /// Return the fenced session generation.
    #[must_use]
    pub const fn generation(&self) -> SessionGeneration {
        self.generation
    }

    /// Return the latest lifecycle and terminal state.
    #[must_use]
    pub fn status(&self) -> SessionStatus {
        *self.status_rx.borrow()
    }

    /// Return a non-secret metrics snapshot.
    #[must_use]
    pub fn metrics(&self) -> TransportMetricsSnapshot {
        self.metrics.snapshot()
    }

    /// Enqueue one already-framed outbound message without blocking.
    ///
    /// Gameplay messages preserve FIFO order in one dedicated queue and are
    /// always selected before background work by the writer. Queue saturation is
    /// explicit; no frame is silently dropped or coalesced.
    ///
    /// # Errors
    ///
    /// Rejects stale generations, invalid/oversized frames, closed sessions and
    /// full bounded queues.
    pub fn try_send(
        &self,
        generation: SessionGeneration,
        priority: OutboundPriority,
        bytes: Vec<u8>,
    ) -> Result<(), TransportError> {
        if generation != self.generation {
            return Err(TransportError::new(TransportErrorKind::StaleSession));
        }
        if self.close_requested || self.status().state() != ConnectionState::Connected {
            return Err(TransportError::new(TransportErrorKind::InvalidState));
        }
        if bytes.is_empty() {
            return Err(TransportError::new(TransportErrorKind::InvalidFrameLength));
        }
        if bytes.len() > self.config.max_outbound_frame_bytes() {
            return Err(TransportError::new(TransportErrorKind::FrameTooLarge));
        }

        let frame = OutboundFrame { bytes };
        match priority {
            OutboundPriority::Gameplay => enqueue(
                &self.gameplay_tx,
                frame,
                &self.metrics.gameplay_depth,
                &self.metrics.gameplay_high_water,
                &self.metrics.outbound_queue_full,
            ),
            OutboundPriority::Background => enqueue(
                &self.background_tx,
                frame,
                &self.metrics.background_depth,
                &self.metrics.background_high_water,
                &self.metrics.outbound_queue_full,
            ),
        }
    }

    /// Receive one complete inbound frame without blocking.
    ///
    /// # Errors
    ///
    /// Returns a terminal session error after the queue is drained.
    pub fn try_recv(&mut self) -> Result<Option<InboundFrame>, TransportError> {
        match self.inbound_rx.try_recv() {
            Ok(frame) => {
                self.metrics.inbound_depth.fetch_sub(1, Ordering::AcqRel);
                Ok(Some(frame))
            }
            Err(mpsc::error::TryRecvError::Empty) => {
                if let Some(kind) = self.status().terminal_error() {
                    Err(TransportError::new(kind))
                } else {
                    Ok(None)
                }
            }
            Err(mpsc::error::TryRecvError::Disconnected) => {
                if let Some(kind) = self.status().terminal_error() {
                    Err(TransportError::new(kind))
                } else {
                    Ok(None)
                }
            }
        }
    }

    /// Request cancellation through the dedicated bounded control state.
    pub fn close(&mut self) {
        if self.close_requested {
            return;
        }
        self.close_requested = true;
        if self.status().state() == ConnectionState::Connected {
            let _ = self.status_tx.send(SessionStatus::closing());
            let _ = self.cancel_tx.send(true);
        }
    }

    /// Return whether the complete supervisor tree has finished.
    #[must_use]
    pub fn is_finished(&self) -> bool {
        self.supervisor
            .as_ref()
            .is_none_or(tokio::task::JoinHandle::is_finished)
    }

    /// Wait for a peer, deadline, external cancellation or protocol failure.
    ///
    /// This method does not request shutdown. Use [`Self::join`] for a
    /// caller-initiated deterministic close.
    ///
    /// # Errors
    ///
    /// Returns the terminal transport failure or a task-join failure.
    pub async fn wait(mut self) -> Result<SessionSummary, TransportError> {
        let Some(supervisor) = self.supervisor.take() else {
            return Err(TransportError::new(TransportErrorKind::InvalidState));
        };
        supervisor
            .await
            .map_err(|_join_error| TransportError::new(TransportErrorKind::TaskFailed))?
    }

    /// Cancel and join the complete reader/writer/supervisor tree.
    ///
    /// # Errors
    ///
    /// Returns a terminal transport failure or a task-join failure.
    pub async fn join(mut self) -> Result<SessionSummary, TransportError> {
        self.close();
        self.wait().await
    }
}

impl Drop for TransportSession {
    fn drop(&mut self) {
        self.close();
        if let Some(supervisor) = self.supervisor.take() {
            supervisor.abort();
        }
    }
}

/// Compatibility name retained for the current fail-closed Canary owner.
pub type TcpTransport = TransportSession;

fn enqueue(
    sender: &mpsc::Sender<OutboundFrame>,
    frame: OutboundFrame,
    depth: &AtomicUsize,
    high_water: &AtomicUsize,
    queue_full: &AtomicU64,
) -> Result<(), TransportError> {
    let current_depth = depth.fetch_add(1, Ordering::AcqRel).saturating_add(1);
    match sender.try_send(frame) {
        Ok(()) => {
            high_water.fetch_max(current_depth, Ordering::AcqRel);
            Ok(())
        }
        Err(mpsc::error::TrySendError::Full(_frame)) => {
            depth.fetch_sub(1, Ordering::AcqRel);
            queue_full.fetch_add(1, Ordering::AcqRel);
            Err(TransportError::new(TransportErrorKind::QueueFull))
        }
        Err(mpsc::error::TrySendError::Closed(_frame)) => {
            depth.fetch_sub(1, Ordering::AcqRel);
            Err(TransportError::new(TransportErrorKind::InvalidState))
        }
    }
}

#[allow(clippy::too_many_arguments)]
async fn run_session(
    stream: TcpStream,
    generation: SessionGeneration,
    config: TransportConfig,
    boundary: Arc<dyn FrameBoundary>,
    gameplay_rx: mpsc::Receiver<OutboundFrame>,
    background_rx: mpsc::Receiver<OutboundFrame>,
    inbound_tx: mpsc::Sender<InboundFrame>,
    cancel_rx: watch::Receiver<bool>,
    cancel_tx: watch::Sender<bool>,
    status_tx: watch::Sender<SessionStatus>,
    external_cancellation: CancellationToken,
    metrics: Arc<TransportMetrics>,
) -> Result<SessionSummary, TransportError> {
    let (reader, writer) = stream.into_split();
    let mut tasks = JoinSet::new();
    tasks.spawn(reader_loop(
        reader,
        generation,
        config,
        boundary,
        inbound_tx,
        cancel_rx.clone(),
        Arc::clone(&metrics),
    ));
    tasks.spawn(writer_loop(
        writer,
        config,
        gameplay_rx,
        background_rx,
        cancel_rx.clone(),
        Arc::clone(&metrics),
    ));
    tasks.spawn(cancellation_loop(external_cancellation, cancel_rx));

    let first_result = match tasks.join_next().await {
        Some(result) => classify_join_result(result),
        None => Err(TransportError::new(TransportErrorKind::TaskFailed)),
    };
    let clean_shutdown_requested = *cancel_tx.borrow();
    let _ = cancel_tx.send(true);

    let mut terminal = first_result;
    while let Some(result) = tasks.join_next().await {
        let child_result = classify_join_result(result);
        if terminal.is_ok() {
            terminal = child_result;
        }
    }

    if clean_shutdown_requested
        && matches!(
            terminal,
            Ok(())
                | Err(TransportError {
                    kind: TransportErrorKind::Cancelled
                })
        )
    {
        terminal = Ok(());
    }

    let terminal_error = terminal.as_ref().err().map(|error| error.kind());
    let _ = status_tx.send(SessionStatus::closed(terminal_error));
    let summary = SessionSummary {
        generation,
        metrics: metrics.snapshot(),
    };
    terminal.map(|()| summary)
}

fn classify_join_result(
    result: Result<Result<(), TransportError>, tokio::task::JoinError>,
) -> Result<(), TransportError> {
    result.map_err(|_join_error| TransportError::new(TransportErrorKind::TaskFailed))?
}

async fn cancellation_loop(
    external_cancellation: CancellationToken,
    mut cancel_rx: watch::Receiver<bool>,
) -> Result<(), TransportError> {
    tokio::select! {
        biased;
        changed = cancel_rx.changed() => {
            if changed.is_err() || *cancel_rx.borrow() {
                Ok(())
            } else {
                Err(TransportError::new(TransportErrorKind::InvalidState))
            }
        }
        () = observe_cancellation(&external_cancellation) => {
            Err(TransportError::new(TransportErrorKind::Cancelled))
        }
    }
}

async fn reader_loop<R>(
    mut reader: R,
    generation: SessionGeneration,
    config: TransportConfig,
    boundary: Arc<dyn FrameBoundary>,
    inbound_tx: mpsc::Sender<InboundFrame>,
    mut cancel_rx: watch::Receiver<bool>,
    metrics: Arc<TransportMetrics>,
) -> Result<(), TransportError>
where
    R: AsyncRead + Unpin,
{
    loop {
        let frame = tokio::select! {
            biased;
            changed = cancel_rx.changed() => {
                if changed.is_err() || *cancel_rx.borrow() {
                    return Err(TransportError::new(TransportErrorKind::Cancelled));
                }
                continue;
            }
            result = timeout(
                config.idle_timeout(),
                read_frame(&mut reader, config, boundary.as_ref()),
            ) => {
                match result {
                    Ok(frame) => frame?,
                    Err(_elapsed) => {
                        return Err(TransportError::new(TransportErrorKind::IdleTimeout));
                    }
                }
            }
        };
        let frame_len = frame.len();
        let permit = tokio::select! {
            biased;
            changed = cancel_rx.changed() => {
                if changed.is_err() || *cancel_rx.borrow() {
                    return Err(TransportError::new(TransportErrorKind::Cancelled));
                }
                continue;
            }
            permit = inbound_tx.reserve() => {
                permit.map_err(|_closed| TransportError::new(TransportErrorKind::InvalidState))?
            }
        };
        let current_depth = metrics
            .inbound_depth
            .fetch_add(1, Ordering::AcqRel)
            .saturating_add(1);
        metrics
            .inbound_high_water
            .fetch_max(current_depth, Ordering::AcqRel);
        permit.send(InboundFrame::new(generation, frame));
        metrics.inbound_frames.fetch_add(1, Ordering::AcqRel);
        metrics.inbound_bytes.fetch_add(
            u64::try_from(frame_len).unwrap_or(u64::MAX),
            Ordering::AcqRel,
        );
    }
}

async fn writer_loop<W>(
    mut writer: W,
    config: TransportConfig,
    mut gameplay_rx: mpsc::Receiver<OutboundFrame>,
    mut background_rx: mpsc::Receiver<OutboundFrame>,
    mut cancel_rx: watch::Receiver<bool>,
    metrics: Arc<TransportMetrics>,
) -> Result<(), TransportError>
where
    W: AsyncWrite + Unpin,
{
    loop {
        let frame = receive_next_frame(
            &mut gameplay_rx,
            &mut background_rx,
            &mut cancel_rx,
            metrics.as_ref(),
        )
        .await?;
        let frame_len = frame.bytes.len();
        let result = tokio::select! {
            biased;
            changed = cancel_rx.changed() => {
                if changed.is_err() || *cancel_rx.borrow() {
                    let _ = timeout(config.write_timeout(), writer.shutdown()).await;
                    return Err(TransportError::new(TransportErrorKind::Cancelled));
                }
                continue;
            }
            result = write_all_deadline(&mut writer, &frame.bytes, config.write_timeout()) => result,
        };
        result?;
        metrics.outbound_frames.fetch_add(1, Ordering::AcqRel);
        metrics.outbound_bytes.fetch_add(
            u64::try_from(frame_len).unwrap_or(u64::MAX),
            Ordering::AcqRel,
        );
    }
}

async fn receive_next_frame(
    gameplay_rx: &mut mpsc::Receiver<OutboundFrame>,
    background_rx: &mut mpsc::Receiver<OutboundFrame>,
    cancel_rx: &mut watch::Receiver<bool>,
    metrics: &TransportMetrics,
) -> Result<OutboundFrame, TransportError> {
    tokio::select! {
        biased;
        changed = cancel_rx.changed() => {
            if changed.is_err() || *cancel_rx.borrow() {
                Err(TransportError::new(TransportErrorKind::Cancelled))
            } else {
                Err(TransportError::new(TransportErrorKind::InvalidState))
            }
        }
        frame = gameplay_rx.recv() => {
            match frame {
                Some(frame) => {
                    metrics.gameplay_depth.fetch_sub(1, Ordering::AcqRel);
                    Ok(frame)
                }
                None => Err(TransportError::new(TransportErrorKind::InvalidState)),
            }
        }
        frame = background_rx.recv() => {
            match frame {
                Some(frame) => {
                    metrics.background_depth.fetch_sub(1, Ordering::AcqRel);
                    Ok(frame)
                }
                None => Err(TransportError::new(TransportErrorKind::InvalidState)),
            }
        }
    }
}

async fn read_frame<R>(
    reader: &mut R,
    config: TransportConfig,
    boundary: &dyn FrameBoundary,
) -> Result<Vec<u8>, TransportError>
where
    R: AsyncRead + Unpin,
{
    let header_len = boundary.header_len();
    if header_len == 0 || header_len > MAX_FRAME_HEADER_BYTES {
        return Err(TransportError::new(TransportErrorKind::InvalidFrameLength));
    }
    let mut header = vec![0_u8; header_len];
    read_exact_deadline(reader, &mut header, config.read_timeout()).await?;
    let complete_len = boundary
        .complete_frame_len(&header)
        .map_err(|_error| TransportError::new(TransportErrorKind::ProtocolTerminal))?;
    validate_complete_frame_len(header_len, complete_len, config.max_inbound_frame_bytes())?;

    let mut frame = Vec::new();
    frame
        .try_reserve_exact(complete_len)
        .map_err(|_allocation_error| TransportError::new(TransportErrorKind::ResourceExhausted))?;
    frame.resize(complete_len, 0);
    frame[..header_len].copy_from_slice(&header);
    if complete_len > header_len {
        read_exact_deadline(reader, &mut frame[header_len..], config.read_timeout()).await?;
    }
    Ok(frame)
}

async fn read_exact_deadline<R>(
    reader: &mut R,
    buffer: &mut [u8],
    deadline: Duration,
) -> Result<(), TransportError>
where
    R: AsyncRead + Unpin,
{
    let operation = async {
        let mut offset = 0;
        while offset < buffer.len() {
            let read = match reader.read(&mut buffer[offset..]).await {
                Ok(0) => {
                    return Err(TransportError::new(TransportErrorKind::ConnectionLost));
                }
                Ok(read) => read,
                Err(error) => return Err(classify_read_error(&error)),
            };
            offset = offset
                .checked_add(read)
                .ok_or_else(|| TransportError::new(TransportErrorKind::ResourceExhausted))?;
        }
        Ok(())
    };
    timeout(deadline, operation)
        .await
        .map_err(|_elapsed| TransportError::new(TransportErrorKind::Timeout))?
}

async fn write_all_deadline<W>(
    writer: &mut W,
    buffer: &[u8],
    deadline: Duration,
) -> Result<(), TransportError>
where
    W: AsyncWrite + Unpin,
{
    let operation = async {
        let mut offset = 0;
        while offset < buffer.len() {
            let written = match writer.write(&buffer[offset..]).await {
                Ok(0) => {
                    return Err(TransportError::new(TransportErrorKind::ConnectionLost));
                }
                Ok(written) => written,
                Err(error) => return Err(classify_write_error(&error)),
            };
            offset = offset
                .checked_add(written)
                .ok_or_else(|| TransportError::new(TransportErrorKind::ResourceExhausted))?;
        }
        Ok(())
    };
    timeout(deadline, operation)
        .await
        .map_err(|_elapsed| TransportError::new(TransportErrorKind::Timeout))?
}

async fn connect_with_deadline<F, T>(
    connect: F,
    deadline: Duration,
    cancellation: &CancellationToken,
) -> Result<T, TransportError>
where
    F: Future<Output = io::Result<T>>,
{
    if cancellation.is_cancelled() {
        return Err(TransportError::new(TransportErrorKind::Cancelled));
    }
    tokio::pin!(connect);
    tokio::select! {
        biased;
        () = observe_cancellation(cancellation) => {
            Err(TransportError::new(TransportErrorKind::Cancelled))
        }
        result = timeout(deadline, &mut connect) => {
            match result {
                Ok(Ok(value)) => Ok(value),
                Ok(Err(error)) => Err(classify_connect_error(&error)),
                Err(_elapsed) => Err(TransportError::new(TransportErrorKind::Timeout)),
            }
        }
    }
}

async fn observe_cancellation(cancellation: &CancellationToken) {
    while !cancellation.is_cancelled() {
        sleep(CANCELLATION_OBSERVATION_INTERVAL).await;
    }
}

fn classify_connect_error(error: &io::Error) -> TransportError {
    match error.kind() {
        io::ErrorKind::TimedOut => TransportError::new(TransportErrorKind::Timeout),
        _ => TransportError::new(TransportErrorKind::ConnectFailed),
    }
}

fn classify_read_error(error: &io::Error) -> TransportError {
    match error.kind() {
        io::ErrorKind::TimedOut => TransportError::new(TransportErrorKind::Timeout),
        io::ErrorKind::UnexpectedEof
        | io::ErrorKind::ConnectionAborted
        | io::ErrorKind::ConnectionReset
        | io::ErrorKind::BrokenPipe => TransportError::new(TransportErrorKind::ConnectionLost),
        _ => TransportError::new(TransportErrorKind::ReadFailed),
    }
}

fn classify_write_error(error: &io::Error) -> TransportError {
    match error.kind() {
        io::ErrorKind::TimedOut => TransportError::new(TransportErrorKind::Timeout),
        io::ErrorKind::UnexpectedEof
        | io::ErrorKind::ConnectionAborted
        | io::ErrorKind::ConnectionReset
        | io::ErrorKind::BrokenPipe => TransportError::new(TransportErrorKind::ConnectionLost),
        _ => TransportError::new(TransportErrorKind::WriteFailed),
    }
}

#[cfg(test)]
pub(crate) async fn test_read_exact<R>(
    reader: &mut R,
    buffer: &mut [u8],
    deadline: Duration,
) -> Result<(), TransportError>
where
    R: AsyncRead + Unpin,
{
    read_exact_deadline(reader, buffer, deadline).await
}

#[cfg(test)]
pub(crate) async fn test_write_all<W>(
    writer: &mut W,
    buffer: &[u8],
    deadline: Duration,
) -> Result<(), TransportError>
where
    W: AsyncWrite + Unpin,
{
    write_all_deadline(writer, buffer, deadline).await
}

#[cfg(test)]
mod internal_tests {
    use super::*;
    use oteryn_foundation::CancellationSource;
    use std::error::Error;
    use std::future::pending;

    #[tokio::test(flavor = "current_thread")]
    async fn connect_deadline_and_cancellation_are_deterministic() {
        let timeout_source = CancellationSource::new();
        let timed_out = connect_with_deadline(
            pending::<io::Result<()>>(),
            Duration::from_millis(5),
            &timeout_source.token(),
        )
        .await;
        assert_eq!(
            timed_out,
            Err(TransportError::new(TransportErrorKind::Timeout))
        );

        let cancelled_source = CancellationSource::new();
        let token = cancelled_source.token();
        let cancel = tokio::spawn(async move {
            tokio::task::yield_now().await;
            let _changed = cancelled_source.cancel();
        });
        let cancelled =
            connect_with_deadline(pending::<io::Result<()>>(), Duration::from_secs(1), &token)
                .await;
        assert_eq!(
            cancelled,
            Err(TransportError::new(TransportErrorKind::Cancelled))
        );
        assert!(cancel.await.is_ok());
    }

    #[tokio::test(flavor = "current_thread")]
    async fn gameplay_priority_is_fifo_and_precedes_background() {
        let (gameplay_tx, mut gameplay_rx) = mpsc::channel(4);
        let (background_tx, mut background_rx) = mpsc::channel(4);
        let (_cancel_tx, mut cancel_rx) = watch::channel(false);
        let metrics = TransportMetrics::default();

        assert!(
            enqueue(
                &background_tx,
                OutboundFrame { bytes: vec![9] },
                &metrics.background_depth,
                &metrics.background_high_water,
                &metrics.outbound_queue_full,
            )
            .is_ok()
        );
        assert!(
            enqueue(
                &gameplay_tx,
                OutboundFrame { bytes: vec![1] },
                &metrics.gameplay_depth,
                &metrics.gameplay_high_water,
                &metrics.outbound_queue_full,
            )
            .is_ok()
        );
        assert!(
            enqueue(
                &gameplay_tx,
                OutboundFrame { bytes: vec![2] },
                &metrics.gameplay_depth,
                &metrics.gameplay_high_water,
                &metrics.outbound_queue_full,
            )
            .is_ok()
        );

        let first = receive_next_frame(
            &mut gameplay_rx,
            &mut background_rx,
            &mut cancel_rx,
            &metrics,
        )
        .await;
        let second = receive_next_frame(
            &mut gameplay_rx,
            &mut background_rx,
            &mut cancel_rx,
            &metrics,
        )
        .await;
        let third = receive_next_frame(
            &mut gameplay_rx,
            &mut background_rx,
            &mut cancel_rx,
            &metrics,
        )
        .await;

        assert_eq!(first.map(|frame| frame.bytes), Ok(vec![1]));
        assert_eq!(second.map(|frame| frame.bytes), Ok(vec![2]));
        assert_eq!(third.map(|frame| frame.bytes), Ok(vec![9]));
    }

    #[tokio::test(flavor = "current_thread")]
    async fn cancellation_interrupts_a_backpressured_write() -> Result<(), Box<dyn Error>> {
        let (client, _server) = tokio::io::duplex(1);
        let config = TransportConfig::new(
            Duration::from_secs(1),
            Duration::from_secs(1),
            Duration::from_secs(1),
            128,
            128,
        )?;
        let (gameplay_tx, gameplay_rx) = mpsc::channel(1);
        let (_background_tx, background_rx) = mpsc::channel(1);
        let (cancel_tx, cancel_rx) = watch::channel(false);
        let metrics = Arc::new(TransportMetrics::default());
        let writer = tokio::spawn(writer_loop(
            client,
            config,
            gameplay_rx,
            background_rx,
            cancel_rx,
            metrics,
        ));
        gameplay_tx
            .send(OutboundFrame {
                bytes: vec![7_u8; 128],
            })
            .await?;
        sleep(Duration::from_millis(5)).await;
        let _changed = cancel_tx.send(true);
        let joined = timeout(Duration::from_millis(100), writer).await?;
        let result = joined?;
        assert_eq!(
            result,
            Err(TransportError::new(TransportErrorKind::Cancelled))
        );
        Ok(())
    }

    #[test]
    fn connection_reset_is_terminally_classified() {
        let reset = io::Error::from(io::ErrorKind::ConnectionReset);
        assert_eq!(
            classify_read_error(&reset),
            TransportError::new(TransportErrorKind::ConnectionLost)
        );
        assert_eq!(
            classify_write_error(&reset),
            TransportError::new(TransportErrorKind::ConnectionLost)
        );
    }

    #[test]
    fn outbound_saturation_is_explicit_and_counted() {
        let (tx, _rx) = mpsc::channel(1);
        let metrics = TransportMetrics::default();
        let first = enqueue(
            &tx,
            OutboundFrame { bytes: vec![1] },
            &metrics.gameplay_depth,
            &metrics.gameplay_high_water,
            &metrics.outbound_queue_full,
        );
        let second = enqueue(
            &tx,
            OutboundFrame { bytes: vec![2] },
            &metrics.gameplay_depth,
            &metrics.gameplay_high_water,
            &metrics.outbound_queue_full,
        );
        assert!(first.is_ok());
        assert_eq!(
            second,
            Err(TransportError::new(TransportErrorKind::QueueFull))
        );
        assert_eq!(metrics.snapshot().outbound_queue_full, 1);
        assert_eq!(metrics.snapshot().gameplay_queue_high_water, 1);
    }
}
