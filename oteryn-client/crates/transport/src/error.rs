use std::error::Error;
use std::fmt::{self, Display, Formatter};

/// Deterministic lifecycle of one non-reconnecting TCP session.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ConnectionState {
    /// No socket is connected.
    Disconnected,
    /// A bounded connection attempt is active.
    Connecting,
    /// Reader and writer ownership is active.
    Connected,
    /// Cancellation was requested and child tasks are joining.
    Closing,
    /// The session is terminal and cannot reconnect.
    Closed,
}

/// Stable secret-free transport failure categories.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransportErrorKind {
    /// Caller-owned cancellation ended the operation.
    Cancelled,
    /// A configured operation deadline elapsed.
    Timeout,
    /// No complete inbound frame arrived before the idle deadline.
    IdleTimeout,
    /// A requested frame length was zero or structurally invalid.
    InvalidFrameLength,
    /// A frame exceeded the configured directional limit.
    FrameTooLarge,
    /// A bounded queue rejected additional work.
    QueueFull,
    /// Work targeted a different session generation.
    StaleSession,
    /// The lifecycle did not permit the requested operation.
    InvalidState,
    /// TCP connection establishment failed.
    ConnectFailed,
    /// Reading from the connected stream failed.
    ReadFailed,
    /// Writing to the connected stream failed.
    WriteFailed,
    /// The peer closed or reset the connection.
    ConnectionLost,
    /// Framing failed in a way that may desynchronize the stream.
    ProtocolTerminal,
    /// A bounded allocation could not be reserved.
    ResourceExhausted,
    /// An application-owned Tokio task failed to join.
    TaskFailed,
    /// The application-owned Tokio runtime could not be created.
    RuntimeUnavailable,
}

/// Stable transport error that never includes endpoints, bytes or credentials.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransportError {
    kind: TransportErrorKind,
}

impl TransportError {
    /// Construct one closed error category.
    #[must_use]
    pub const fn new(kind: TransportErrorKind) -> Self {
        Self { kind }
    }

    /// Return the stable category.
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
            TransportErrorKind::IdleTimeout => "transport idle deadline elapsed",
            TransportErrorKind::InvalidFrameLength => "transport frame length is invalid",
            TransportErrorKind::FrameTooLarge => "transport frame exceeds its configured limit",
            TransportErrorKind::QueueFull => "transport queue is full",
            TransportErrorKind::StaleSession => "transport work belongs to a stale session",
            TransportErrorKind::InvalidState => "transport state does not allow this operation",
            TransportErrorKind::ConnectFailed => "transport connection failed",
            TransportErrorKind::ReadFailed => "transport read failed",
            TransportErrorKind::WriteFailed => "transport write failed",
            TransportErrorKind::ConnectionLost => "transport connection was lost",
            TransportErrorKind::ProtocolTerminal => "transport framing failed terminally",
            TransportErrorKind::ResourceExhausted => "transport allocation could not be reserved",
            TransportErrorKind::TaskFailed => "transport task did not finish cleanly",
            TransportErrorKind::RuntimeUnavailable => {
                "application Tokio runtime could not be created"
            }
        };
        formatter.write_str(message)
    }
}

impl Error for TransportError {}
