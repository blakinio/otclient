//! Bounded synchronous TCP transport for application-owned workers.
//!
//! The implementation remains isolated in `transport_base`; this public layer
//! enforces the shared 30-second I/O ceiling before constructing any socket owner.

mod transport_base;

use oteryn_foundation::CancellationToken;
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};
use std::net::SocketAddr;
use std::time::Duration;

pub use transport_base::{ConnectionState, TransportError, TransportErrorKind};

/// Largest frame accepted by the transport contract.
pub const MAX_SUPPORTED_FRAME_BYTES: usize = transport_base::MAX_SUPPORTED_FRAME_BYTES;
/// Largest connect, read or write timeout accepted by the transport contract.
pub const MAX_IO_TIMEOUT: Duration = Duration::from_secs(30);

/// Stable transport configuration failure.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransportConfigError {
    /// At least one timeout was zero.
    ZeroTimeout,
    /// At least one timeout exceeded [`MAX_IO_TIMEOUT`].
    TimeoutTooLarge,
    /// At least one frame-size bound was zero or unsupported.
    InvalidFrameLimit,
}

impl Display for TransportConfigError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::ZeroTimeout => formatter.write_str("transport timeout must be non-zero"),
            Self::TimeoutTooLarge => {
                formatter.write_str("transport timeout exceeds the 30-second limit")
            }
            Self::InvalidFrameLimit => formatter.write_str("transport frame limit is invalid"),
        }
    }
}

impl Error for TransportConfigError {}

impl From<transport_base::TransportConfigError> for TransportConfigError {
    fn from(error: transport_base::TransportConfigError) -> Self {
        match error {
            transport_base::TransportConfigError::ZeroTimeout => Self::ZeroTimeout,
            transport_base::TransportConfigError::InvalidFrameLimit => Self::InvalidFrameLimit,
        }
    }
}

/// Explicit limits and deadlines for one TCP connection.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransportConfig(transport_base::TransportConfig);

impl TransportConfig {
    /// Construct one validated bounded configuration.
    ///
    /// # Errors
    ///
    /// Rejects zero or over-30-second timeouts and zero/unsupported frame limits.
    pub fn new(
        connect_timeout: Duration,
        read_timeout: Duration,
        write_timeout: Duration,
        max_inbound_frame_bytes: usize,
        max_outbound_frame_bytes: usize,
    ) -> Result<Self, TransportConfigError> {
        if connect_timeout > MAX_IO_TIMEOUT
            || read_timeout > MAX_IO_TIMEOUT
            || write_timeout > MAX_IO_TIMEOUT
        {
            return Err(TransportConfigError::TimeoutTooLarge);
        }
        transport_base::TransportConfig::new(
            connect_timeout,
            read_timeout,
            write_timeout,
            max_inbound_frame_bytes,
            max_outbound_frame_bytes,
        )
        .map(Self)
        .map_err(Into::into)
    }

    /// Return the connection-establishment timeout.
    #[must_use]
    pub const fn connect_timeout(self) -> Duration {
        self.0.connect_timeout()
    }

    /// Return the timeout applied to every blocking read operation.
    #[must_use]
    pub const fn read_timeout(self) -> Duration {
        self.0.read_timeout()
    }

    /// Return the timeout applied to every blocking write operation.
    #[must_use]
    pub const fn write_timeout(self) -> Duration {
        self.0.write_timeout()
    }

    /// Return the maximum accepted inbound frame size.
    #[must_use]
    pub const fn max_inbound_frame_bytes(self) -> usize {
        self.0.max_inbound_frame_bytes()
    }

    /// Return the maximum accepted outbound frame size.
    #[must_use]
    pub const fn max_outbound_frame_bytes(self) -> usize {
        self.0.max_outbound_frame_bytes()
    }
}

/// Owner of one bounded, explicitly closed TCP connection.
pub struct TcpTransport(transport_base::TcpTransport);

impl TcpTransport {
    /// Construct a disconnected owner.
    #[must_use]
    pub const fn new(config: TransportConfig) -> Self {
        Self(transport_base::TcpTransport::new(config.0))
    }

    /// Return the deterministic connection state.
    #[must_use]
    pub const fn state(&self) -> ConnectionState {
        self.0.state()
    }

    /// Establish one bounded TCP connection.
    pub fn connect(
        &mut self,
        endpoint: SocketAddr,
        cancellation: &CancellationToken,
    ) -> Result<(), TransportError> {
        self.0.connect(endpoint, cancellation)
    }

    /// Read exactly one bounded frame body.
    pub fn read_exact_bounded(
        &mut self,
        length: usize,
        cancellation: &CancellationToken,
    ) -> Result<Vec<u8>, TransportError> {
        self.0.read_exact_bounded(length, cancellation)
    }

    /// Write exactly one bounded frame body.
    pub fn write_all_bounded(
        &mut self,
        bytes: &[u8],
        cancellation: &CancellationToken,
    ) -> Result<(), TransportError> {
        self.0.write_all_bounded(bytes, cancellation)
    }

    /// Close the stream and make the owner terminal.
    pub fn close(&mut self) {
        self.0.close();
    }
}

impl Debug for TcpTransport {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        Debug::fmt(&self.0, formatter)
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn public_configuration_enforces_the_io_ceiling() {
        let over = Duration::from_secs(31);
        assert_eq!(
            TransportConfig::new(over, Duration::from_secs(1), Duration::from_secs(1), 1, 1),
            Err(TransportConfigError::TimeoutTooLarge)
        );
        assert_eq!(
            TransportConfig::new(Duration::from_secs(1), over, Duration::from_secs(1), 1, 1),
            Err(TransportConfigError::TimeoutTooLarge)
        );
        assert_eq!(
            TransportConfig::new(Duration::from_secs(1), Duration::from_secs(1), over, 1, 1),
            Err(TransportConfigError::TimeoutTooLarge)
        );
        assert!(TransportConfig::new(MAX_IO_TIMEOUT, MAX_IO_TIMEOUT, MAX_IO_TIMEOUT, 1, 1).is_ok());
    }
}
