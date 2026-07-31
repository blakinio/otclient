//! Bounded synchronous TCP transport for application-owned workers.
//!
//! The transport has no resolver, background daemon, reconnect loop or raw
//! socket escape hatch. Callers provide one already-resolved address, explicit
//! limits, explicit timeouts and an application-owned cancellation token.

use oteryn_foundation::CancellationToken;
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};
use std::io::{self, Read, Write};
use std::net::{Shutdown, SocketAddr, TcpStream};
use std::time::Duration;

/// Largest frame accepted by the first transport contract.
pub const MAX_SUPPORTED_FRAME_BYTES: usize = u16::MAX as usize;

/// Stable transport configuration failure.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransportConfigError {
    /// At least one timeout was zero.
    ZeroTimeout,
    /// At least one frame-size bound was zero or unsupported.
    InvalidFrameLimit,
}

impl Display for TransportConfigError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::ZeroTimeout => formatter.write_str("transport timeout must be non-zero"),
            Self::InvalidFrameLimit => formatter.write_str("transport frame limit is invalid"),
        }
    }
}

impl Error for TransportConfigError {}

/// Explicit limits and deadlines for one TCP connection.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransportConfig {
    connect_timeout: Duration,
    read_timeout: Duration,
    write_timeout: Duration,
    max_inbound_frame_bytes: usize,
    max_outbound_frame_bytes: usize,
}

impl TransportConfig {
    /// Construct one validated bounded configuration.
    ///
    /// # Errors
    ///
    /// Rejects zero timeouts and zero/unsupported frame limits.
    pub fn new(
        connect_timeout: Duration,
        read_timeout: Duration,
        write_timeout: Duration,
        max_inbound_frame_bytes: usize,
        max_outbound_frame_bytes: usize,
    ) -> Result<Self, TransportConfigError> {
        if connect_timeout.is_zero() || read_timeout.is_zero() || write_timeout.is_zero() {
            return Err(TransportConfigError::ZeroTimeout);
        }
        if !valid_frame_limit(max_inbound_frame_bytes)
            || !valid_frame_limit(max_outbound_frame_bytes)
        {
            return Err(TransportConfigError::InvalidFrameLimit);
        }
        Ok(Self {
            connect_timeout,
            read_timeout,
            write_timeout,
            max_inbound_frame_bytes,
            max_outbound_frame_bytes,
        })
    }

    /// Return the connection-establishment timeout.
    #[must_use]
    pub const fn connect_timeout(self) -> Duration {
        self.connect_timeout
    }

    /// Return the timeout applied to every blocking read operation.
    #[must_use]
    pub const fn read_timeout(self) -> Duration {
        self.read_timeout
    }

    /// Return the timeout applied to every blocking write operation.
    #[must_use]
    pub const fn write_timeout(self) -> Duration {
        self.write_timeout
    }

    /// Return the maximum accepted inbound frame size.
    #[must_use]
    pub const fn max_inbound_frame_bytes(self) -> usize {
        self.max_inbound_frame_bytes
    }

    /// Return the maximum accepted outbound frame size.
    #[must_use]
    pub const fn max_outbound_frame_bytes(self) -> usize {
        self.max_outbound_frame_bytes
    }
}

fn valid_frame_limit(value: usize) -> bool {
    value > 0 && value <= MAX_SUPPORTED_FRAME_BYTES
}

/// Deterministic state of one non-reconnecting connection owner.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConnectionState {
    /// No connection attempt has started.
    Disconnected,
    /// One connection attempt is in progress.
    Connecting,
    /// One TCP stream is connected.
    Connected,
    /// The owner is terminally closed and cannot reconnect.
    Closed,
}

/// Closed stable transport error categories.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransportErrorKind {
    /// The application cancelled at a safe observation boundary.
    Cancelled,
    /// A configured connection, read or write timeout elapsed.
    Timeout,
    /// A frame length was zero.
    InvalidFrameLength,
    /// A frame exceeded its configured direction-specific limit.
    FrameTooLarge,
    /// The operation is invalid for the deterministic connection state.
    InvalidState,
    /// TCP connection establishment failed.
    ConnectFailed,
    /// A bounded read failed without exposing backend text.
    ReadFailed,
    /// A bounded write failed without exposing backend text.
    WriteFailed,
    /// The peer closed or reset the connection.
    ConnectionLost,
    /// A bounded buffer allocation could not be satisfied.
    ResourceExhausted,
}

/// Stable non-secret transport error.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransportError {
    kind: TransportErrorKind,
}

impl TransportError {
    /// Construct one stable category.
    #[must_use]
    pub const fn new(kind: TransportErrorKind) -> Self {
        Self { kind }
    }

    /// Return the closed failure category.
    #[must_use]
    pub const fn kind(self) -> TransportErrorKind {
        self.kind
    }
}

impl Display for TransportError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self.kind {
            TransportErrorKind::Cancelled => "transport operation was cancelled",
            TransportErrorKind::Timeout => "transport operation timed out",
            TransportErrorKind::InvalidFrameLength => "transport frame length is invalid",
            TransportErrorKind::FrameTooLarge => "transport frame exceeds its size limit",
            TransportErrorKind::InvalidState => "transport connection state rejects the operation",
            TransportErrorKind::ConnectFailed => "transport connection failed",
            TransportErrorKind::ReadFailed => "transport read failed",
            TransportErrorKind::WriteFailed => "transport write failed",
            TransportErrorKind::ConnectionLost => "transport connection was lost",
            TransportErrorKind::ResourceExhausted => "transport buffer allocation failed",
        };
        formatter.write_str(message)
    }
}

impl Error for TransportError {}

/// Owner of one bounded, explicitly closed TCP connection.
pub struct TcpTransport {
    stream: Option<TcpStream>,
    state: ConnectionState,
    config: TransportConfig,
}

impl TcpTransport {
    /// Construct a disconnected owner.
    #[must_use]
    pub const fn new(config: TransportConfig) -> Self {
        Self {
            stream: None,
            state: ConnectionState::Disconnected,
            config,
        }
    }

    /// Return the deterministic connection state.
    #[must_use]
    pub const fn state(&self) -> ConnectionState {
        self.state
    }

    /// Establish one TCP connection to an already-resolved address.
    ///
    /// # Errors
    ///
    /// Returns a stable cancellation, timeout, connection or state error. A
    /// failed attempt closes this owner; it never retries or reconnects.
    pub fn connect(
        &mut self,
        endpoint: SocketAddr,
        cancellation: &CancellationToken,
    ) -> Result<(), TransportError> {
        if self.state != ConnectionState::Disconnected {
            return Err(TransportError::new(TransportErrorKind::InvalidState));
        }
        if cancellation.is_cancelled() {
            self.state = ConnectionState::Closed;
            return Err(TransportError::new(TransportErrorKind::Cancelled));
        }

        self.state = ConnectionState::Connecting;
        let stream = match TcpStream::connect_timeout(&endpoint, self.config.connect_timeout()) {
            Ok(stream) => stream,
            Err(error) => {
                self.state = ConnectionState::Closed;
                return Err(map_connect_error(&error));
            }
        };

        if cancellation.is_cancelled() {
            let _ = stream.shutdown(Shutdown::Both);
            self.state = ConnectionState::Closed;
            return Err(TransportError::new(TransportErrorKind::Cancelled));
        }

        if stream
            .set_read_timeout(Some(self.config.read_timeout()))
            .is_err()
            || stream
                .set_write_timeout(Some(self.config.write_timeout()))
                .is_err()
            || stream.set_nodelay(true).is_err()
        {
            let _ = stream.shutdown(Shutdown::Both);
            self.state = ConnectionState::Closed;
            return Err(TransportError::new(TransportErrorKind::ConnectFailed));
        }

        self.stream = Some(stream);
        self.state = ConnectionState::Connected;
        Ok(())
    }

    /// Read exactly one caller-declared bounded frame body.
    ///
    /// # Errors
    ///
    /// Rejects zero/oversized lengths before allocation and handles partial
    /// reads, timeout, cancellation and abrupt closure deterministically.
    pub fn read_exact_bounded(
        &mut self,
        length: usize,
        cancellation: &CancellationToken,
    ) -> Result<Vec<u8>, TransportError> {
        if self.state != ConnectionState::Connected {
            return Err(TransportError::new(TransportErrorKind::InvalidState));
        }
        validate_frame_length(length, self.config.max_inbound_frame_bytes())?;

        let mut output = Vec::new();
        output
            .try_reserve_exact(length)
            .map_err(|_| TransportError::new(TransportErrorKind::ResourceExhausted))?;
        output.resize(length, 0);

        let result = match self.stream.as_mut() {
            Some(stream) => read_exact_loop(stream, &mut output, cancellation),
            None => Err(TransportError::new(TransportErrorKind::InvalidState)),
        };
        self.apply_terminal_result(result)?;
        Ok(output)
    }

    /// Write exactly one caller-declared bounded frame body.
    ///
    /// # Errors
    ///
    /// Rejects zero/oversized frames before I/O and handles partial writes,
    /// timeout, cancellation and abrupt closure deterministically.
    pub fn write_all_bounded(
        &mut self,
        bytes: &[u8],
        cancellation: &CancellationToken,
    ) -> Result<(), TransportError> {
        if self.state != ConnectionState::Connected {
            return Err(TransportError::new(TransportErrorKind::InvalidState));
        }
        validate_frame_length(bytes.len(), self.config.max_outbound_frame_bytes())?;

        let result = match self.stream.as_mut() {
            Some(stream) => write_all_loop(stream, bytes, cancellation),
            None => Err(TransportError::new(TransportErrorKind::InvalidState)),
        };
        self.apply_terminal_result(result)
    }

    /// Close the stream and make the owner terminal.
    pub fn close(&mut self) {
        if let Some(stream) = self.stream.take() {
            let _ = stream.shutdown(Shutdown::Both);
        }
        self.state = ConnectionState::Closed;
    }

    fn apply_terminal_result(
        &mut self,
        result: Result<(), TransportError>,
    ) -> Result<(), TransportError> {
        if let Err(error) = result {
            if error.kind() == TransportErrorKind::ConnectionLost {
                self.close();
            }
            return Err(error);
        }
        Ok(())
    }
}

impl Debug for TcpTransport {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("TcpTransport")
            .field("state", &self.state)
            .field("config", &self.config)
            .finish()
    }
}

impl Drop for TcpTransport {
    fn drop(&mut self) {
        self.close();
    }
}

fn validate_frame_length(length: usize, maximum: usize) -> Result<(), TransportError> {
    if length == 0 {
        return Err(TransportError::new(
            TransportErrorKind::InvalidFrameLength,
        ));
    }
    if length > maximum {
        return Err(TransportError::new(TransportErrorKind::FrameTooLarge));
    }
    Ok(())
}

fn read_exact_loop(
    stream: &mut TcpStream,
    output: &mut [u8],
    cancellation: &CancellationToken,
) -> Result<(), TransportError> {
    let mut offset = 0;
    while offset < output.len() {
        if cancellation.is_cancelled() {
            return Err(TransportError::new(TransportErrorKind::Cancelled));
        }
        match stream.read(&mut output[offset..]) {
            Ok(0) => return Err(TransportError::new(TransportErrorKind::ConnectionLost)),
            Ok(read) => offset += read,
            Err(error) if error.kind() == io::ErrorKind::Interrupted => {}
            Err(error) => return Err(map_read_error(&error)),
        }
    }
    Ok(())
}

fn write_all_loop(
    stream: &mut TcpStream,
    bytes: &[u8],
    cancellation: &CancellationToken,
) -> Result<(), TransportError> {
    let mut offset = 0;
    while offset < bytes.len() {
        if cancellation.is_cancelled() {
            return Err(TransportError::new(TransportErrorKind::Cancelled));
        }
        match stream.write(&bytes[offset..]) {
            Ok(0) => return Err(TransportError::new(TransportErrorKind::ConnectionLost)),
            Ok(written) => offset += written,
            Err(error) if error.kind() == io::ErrorKind::Interrupted => {}
            Err(error) => return Err(map_write_error(&error)),
        }
    }
    Ok(())
}

fn map_connect_error(error: &io::Error) -> TransportError {
    if is_timeout(error.kind()) {
        TransportError::new(TransportErrorKind::Timeout)
    } else {
        TransportError::new(TransportErrorKind::ConnectFailed)
    }
}

fn map_read_error(error: &io::Error) -> TransportError {
    if is_timeout(error.kind()) {
        TransportError::new(TransportErrorKind::Timeout)
    } else if is_connection_lost(error.kind()) {
        TransportError::new(TransportErrorKind::ConnectionLost)
    } else {
        TransportError::new(TransportErrorKind::ReadFailed)
    }
}

fn map_write_error(error: &io::Error) -> TransportError {
    if is_timeout(error.kind()) {
        TransportError::new(TransportErrorKind::Timeout)
    } else if is_connection_lost(error.kind()) {
        TransportError::new(TransportErrorKind::ConnectionLost)
    } else {
        TransportError::new(TransportErrorKind::WriteFailed)
    }
}

fn is_timeout(kind: io::ErrorKind) -> bool {
    matches!(kind, io::ErrorKind::TimedOut | io::ErrorKind::WouldBlock)
}

fn is_connection_lost(kind: io::ErrorKind) -> bool {
    matches!(
        kind,
        io::ErrorKind::BrokenPipe
            | io::ErrorKind::ConnectionAborted
            | io::ErrorKind::ConnectionReset
            | io::ErrorKind::NotConnected
            | io::ErrorKind::UnexpectedEof
    )
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_foundation::CancellationSource;
    use std::net::TcpListener;
    use std::thread;

    fn test_config() -> Result<TransportConfig, TransportConfigError> {
        TransportConfig::new(
            Duration::from_secs(1),
            Duration::from_millis(100),
            Duration::from_millis(100),
            1024,
            1024,
        )
    }

    fn connected_pair() -> Result<(TcpTransport, TcpStream), Box<dyn Error>> {
        let listener = TcpListener::bind("127.0.0.1:0")?;
        let endpoint = listener.local_addr()?;
        let accept = thread::spawn(move || listener.accept().map(|(stream, _)| stream));

        let source = CancellationSource::new();
        let mut transport = TcpTransport::new(test_config()?);
        transport.connect(endpoint, &source.token())?;
        let server = accept
            .join()
            .map_err(|_| "TCP accept thread panicked")??;
        Ok((transport, server))
    }

    #[test]
    fn configuration_rejects_unbounded_values() {
        assert_eq!(
            TransportConfig::new(
                Duration::ZERO,
                Duration::from_secs(1),
                Duration::from_secs(1),
                1,
                1,
            ),
            Err(TransportConfigError::ZeroTimeout)
        );
        assert_eq!(
            TransportConfig::new(
                Duration::from_secs(1),
                Duration::from_secs(1),
                Duration::from_secs(1),
                MAX_SUPPORTED_FRAME_BYTES + 1,
                1,
            ),
            Err(TransportConfigError::InvalidFrameLimit)
        );
    }

    #[test]
    fn partial_reads_and_writes_complete_exactly() -> Result<(), Box<dyn Error>> {
        let (mut transport, mut server) = connected_pair()?;
        let source = CancellationSource::new();

        server.write_all(b"ab")?;
        server.write_all(b"cd")?;
        assert_eq!(
            transport.read_exact_bounded(4, &source.token())?,
            b"abcd"
        );

        transport.write_all_bounded(b"synthetic", &source.token())?;
        let mut received = [0_u8; 9];
        server.read_exact(&mut received)?;
        assert_eq!(&received, b"synthetic");
        Ok(())
    }

    #[test]
    fn invalid_and_oversized_frames_are_rejected_before_io() -> Result<(), Box<dyn Error>> {
        let (mut transport, _server) = connected_pair()?;
        let source = CancellationSource::new();
        assert_eq!(
            transport.read_exact_bounded(0, &source.token()),
            Err(TransportError::new(
                TransportErrorKind::InvalidFrameLength
            ))
        );
        assert_eq!(
            transport.write_all_bounded(&vec![0_u8; 1025], &source.token()),
            Err(TransportError::new(TransportErrorKind::FrameTooLarge))
        );
        assert_eq!(transport.state(), ConnectionState::Connected);
        Ok(())
    }

    #[test]
    fn cancellation_prevents_connect_and_io() -> Result<(), Box<dyn Error>> {
        let listener = TcpListener::bind("127.0.0.1:0")?;
        let endpoint = listener.local_addr()?;
        let source = CancellationSource::new();
        assert!(source.cancel());
        let mut transport = TcpTransport::new(test_config()?);
        assert_eq!(
            transport.connect(endpoint, &source.token()),
            Err(TransportError::new(TransportErrorKind::Cancelled))
        );
        assert_eq!(transport.state(), ConnectionState::Closed);

        let (mut connected, _server) = connected_pair()?;
        let connected_source = CancellationSource::new();
        assert!(connected_source.cancel());
        assert_eq!(
            connected.read_exact_bounded(1, &connected_source.token()),
            Err(TransportError::new(TransportErrorKind::Cancelled))
        );
        Ok(())
    }

    #[test]
    fn read_timeout_and_abrupt_close_are_stable() -> Result<(), Box<dyn Error>> {
        let (mut timed, server) = connected_pair()?;
        let source = CancellationSource::new();
        assert_eq!(
            timed.read_exact_bounded(1, &source.token()),
            Err(TransportError::new(TransportErrorKind::Timeout))
        );
        drop(server);

        let (mut closed, peer) = connected_pair()?;
        drop(peer);
        assert_eq!(
            closed.read_exact_bounded(1, &source.token()),
            Err(TransportError::new(TransportErrorKind::ConnectionLost))
        );
        assert_eq!(closed.state(), ConnectionState::Closed);
        Ok(())
    }

    #[test]
    fn errors_never_include_caller_or_backend_text() {
        let marker = "synthetic-secret-marker";
        for kind in [
            TransportErrorKind::Cancelled,
            TransportErrorKind::Timeout,
            TransportErrorKind::InvalidFrameLength,
            TransportErrorKind::FrameTooLarge,
            TransportErrorKind::InvalidState,
            TransportErrorKind::ConnectFailed,
            TransportErrorKind::ReadFailed,
            TransportErrorKind::WriteFailed,
            TransportErrorKind::ConnectionLost,
            TransportErrorKind::ResourceExhausted,
        ] {
            let rendered = TransportError::new(kind).to_string();
            assert!(!rendered.contains(marker));
        }
    }
}
