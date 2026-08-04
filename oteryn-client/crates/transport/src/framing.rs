use crate::{TransportError, TransportErrorKind};
use oteryn_foundation::SessionGeneration;

/// Protocol-owned description of one bounded stream frame boundary.
///
/// The transport reads exactly [`Self::header_len`] bytes, asks the selected
/// adapter boundary for the complete frame length, validates it against the
/// configured transport limit and only then allocates the remaining body.
pub trait FrameBoundary: Send + Sync + 'static {
    /// Return the exact framing header length required before allocation.
    fn header_len(&self) -> usize;

    /// Decode the complete frame length, including the header itself.
    ///
    /// Implementations must return a stable terminal error for malformed,
    /// contradictory or unsupported header fields.
    fn complete_frame_len(&self, header: &[u8]) -> Result<usize, TransportError>;
}

/// One complete validated inbound transport frame.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct InboundFrame {
    generation: SessionGeneration,
    bytes: Vec<u8>,
}

impl InboundFrame {
    pub(crate) const fn new(generation: SessionGeneration, bytes: Vec<u8>) -> Self {
        Self { generation, bytes }
    }

    /// Return the owning session generation.
    #[must_use]
    pub const fn generation(&self) -> SessionGeneration {
        self.generation
    }

    /// Borrow the complete frame, including its framing header.
    #[must_use]
    pub fn bytes(&self) -> &[u8] {
        &self.bytes
    }

    /// Consume the event and return the complete bounded frame.
    #[must_use]
    pub fn into_bytes(self) -> Vec<u8> {
        self.bytes
    }
}

/// Outbound scheduling class.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum OutboundPriority {
    /// Ordered player actions and other latency-sensitive gameplay messages.
    Gameplay,
    /// Non-critical keepalive, telemetry or background requests.
    Background,
}

pub(crate) fn validate_complete_frame_len(
    header_len: usize,
    complete_len: usize,
    max_frame_bytes: usize,
) -> Result<(), TransportError> {
    if header_len == 0 || complete_len < header_len {
        return Err(TransportError::new(
            TransportErrorKind::InvalidFrameLength,
        ));
    }
    if complete_len > max_frame_bytes {
        return Err(TransportError::new(TransportErrorKind::FrameTooLarge));
    }
    Ok(())
}
