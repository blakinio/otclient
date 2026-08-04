//! Protocol-neutral bounded full-duplex transport on an application-owned Tokio runtime.
//!
//! This crate owns TCP byte transport, directional queue bounds, deadlines,
//! cancellation, generation fencing and deterministic joined shutdown. It owns
//! no global runtime, Gateway or gameplay policy, credentials, opcodes or domain
//! state. Selected protocol adapters provide only the exact framing boundary.

mod config;
mod error;
mod framing;
mod session;

#[cfg(any(test, feature = "blocking-baseline"))]
#[path = "transport_base.rs"]
pub mod blocking_baseline;

pub use config::{
    DEFAULT_BACKGROUND_QUEUE_CAPACITY, DEFAULT_GAMEPLAY_QUEUE_CAPACITY,
    DEFAULT_INBOUND_QUEUE_CAPACITY, MAX_FRAME_HEADER_BYTES, MAX_IO_TIMEOUT, MAX_QUEUE_CAPACITY,
    MAX_SUPPORTED_FRAME_BYTES, TransportConfig, TransportConfigError,
};
pub use error::{ConnectionState, TransportError, TransportErrorKind};
pub use framing::{FrameBoundary, InboundFrame, OutboundPriority};
pub use session::{
    SessionStatus, SessionSummary, TcpTransport, TransportMetricsSnapshot, TransportSession,
};

#[cfg(any(test, feature = "blocking-baseline"))]
pub use blocking_baseline::{
    TcpTransport as BlockingTcpTransport, TransportConfig as BlockingTransportConfig,
    TransportConfigError as BlockingTransportConfigError,
};

#[cfg(test)]
mod tests;
