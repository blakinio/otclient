use std::error::Error;
use std::fmt::{self, Display, Formatter};
use std::time::Duration;

/// Largest complete frame accepted by the transport boundary.
pub const MAX_SUPPORTED_FRAME_BYTES: usize = u16::MAX as usize;
/// Largest framing header accepted before protocol-specific validation.
pub const MAX_FRAME_HEADER_BYTES: usize = 32;
/// Largest queue capacity accepted by one transport session.
pub const MAX_QUEUE_CAPACITY: usize = 4_096;
/// Default inbound frame queue capacity.
pub const DEFAULT_INBOUND_QUEUE_CAPACITY: usize = 64;
/// Default latency-sensitive gameplay queue capacity.
pub const DEFAULT_GAMEPLAY_QUEUE_CAPACITY: usize = 64;
/// Default background queue capacity.
pub const DEFAULT_BACKGROUND_QUEUE_CAPACITY: usize = 16;

/// Stable transport configuration failure.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TransportConfigError {
    /// At least one timeout was zero.
    ZeroTimeout,
    /// At least one frame-size bound was zero or unsupported.
    InvalidFrameLimit,
    /// At least one queue capacity was zero or unsupported.
    InvalidQueueCapacity,
}

impl Display for TransportConfigError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::ZeroTimeout => formatter.write_str("transport timeout must be non-zero"),
            Self::InvalidFrameLimit => formatter.write_str("transport frame limit is invalid"),
            Self::InvalidQueueCapacity => {
                formatter.write_str("transport queue capacity is invalid")
            }
        }
    }
}

impl Error for TransportConfigError {}

/// Explicit limits, deadlines and queue bounds for one TCP session.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TransportConfig {
    connect_timeout: Duration,
    read_timeout: Duration,
    write_timeout: Duration,
    idle_timeout: Duration,
    max_inbound_frame_bytes: usize,
    max_outbound_frame_bytes: usize,
    inbound_queue_capacity: usize,
    gameplay_queue_capacity: usize,
    background_queue_capacity: usize,
}

impl TransportConfig {
    /// Construct a validated configuration with conservative queue defaults.
    ///
    /// The idle deadline initially matches the read deadline. Callers may
    /// replace it with [`Self::with_idle_timeout`].
    ///
    /// # Errors
    ///
    /// Rejects zero timeouts and zero or unsupported frame limits.
    pub fn new(
        connect_timeout: Duration,
        read_timeout: Duration,
        write_timeout: Duration,
        max_inbound_frame_bytes: usize,
        max_outbound_frame_bytes: usize,
    ) -> Result<Self, TransportConfigError> {
        validate_timeout(connect_timeout)?;
        validate_timeout(read_timeout)?;
        validate_timeout(write_timeout)?;
        validate_frame_limit(max_inbound_frame_bytes)?;
        validate_frame_limit(max_outbound_frame_bytes)?;
        Ok(Self {
            connect_timeout,
            read_timeout,
            write_timeout,
            idle_timeout: read_timeout,
            max_inbound_frame_bytes,
            max_outbound_frame_bytes,
            inbound_queue_capacity: DEFAULT_INBOUND_QUEUE_CAPACITY,
            gameplay_queue_capacity: DEFAULT_GAMEPLAY_QUEUE_CAPACITY,
            background_queue_capacity: DEFAULT_BACKGROUND_QUEUE_CAPACITY,
        })
    }

    /// Replace the idle deadline.
    ///
    /// # Errors
    ///
    /// Rejects a zero duration.
    pub fn with_idle_timeout(mut self, idle_timeout: Duration) -> Result<Self, TransportConfigError> {
        validate_timeout(idle_timeout)?;
        self.idle_timeout = idle_timeout;
        Ok(self)
    }

    /// Replace all bounded queue capacities.
    ///
    /// # Errors
    ///
    /// Rejects zero or excessively large capacities.
    pub fn with_queue_capacities(
        mut self,
        inbound_queue_capacity: usize,
        gameplay_queue_capacity: usize,
        background_queue_capacity: usize,
    ) -> Result<Self, TransportConfigError> {
        validate_queue_capacity(inbound_queue_capacity)?;
        validate_queue_capacity(gameplay_queue_capacity)?;
        validate_queue_capacity(background_queue_capacity)?;
        self.inbound_queue_capacity = inbound_queue_capacity;
        self.gameplay_queue_capacity = gameplay_queue_capacity;
        self.background_queue_capacity = background_queue_capacity;
        Ok(self)
    }

    /// Return the connection-establishment deadline.
    #[must_use]
    pub const fn connect_timeout(self) -> Duration {
        self.connect_timeout
    }

    /// Return the deadline applied to each bounded read operation.
    #[must_use]
    pub const fn read_timeout(self) -> Duration {
        self.read_timeout
    }

    /// Return the deadline applied to each bounded write operation.
    #[must_use]
    pub const fn write_timeout(self) -> Duration {
        self.write_timeout
    }

    /// Return the maximum time without a complete inbound frame.
    #[must_use]
    pub const fn idle_timeout(self) -> Duration {
        self.idle_timeout
    }

    /// Return the maximum complete inbound frame size.
    #[must_use]
    pub const fn max_inbound_frame_bytes(self) -> usize {
        self.max_inbound_frame_bytes
    }

    /// Return the maximum complete outbound frame size.
    #[must_use]
    pub const fn max_outbound_frame_bytes(self) -> usize {
        self.max_outbound_frame_bytes
    }

    /// Return the inbound frame queue capacity.
    #[must_use]
    pub const fn inbound_queue_capacity(self) -> usize {
        self.inbound_queue_capacity
    }

    /// Return the latency-sensitive gameplay queue capacity.
    #[must_use]
    pub const fn gameplay_queue_capacity(self) -> usize {
        self.gameplay_queue_capacity
    }

    /// Return the background queue capacity.
    #[must_use]
    pub const fn background_queue_capacity(self) -> usize {
        self.background_queue_capacity
    }
}

fn validate_timeout(timeout: Duration) -> Result<(), TransportConfigError> {
    if timeout.is_zero() {
        Err(TransportConfigError::ZeroTimeout)
    } else {
        Ok(())
    }
}

fn validate_frame_limit(limit: usize) -> Result<(), TransportConfigError> {
    if limit == 0 || limit > MAX_SUPPORTED_FRAME_BYTES {
        Err(TransportConfigError::InvalidFrameLimit)
    } else {
        Ok(())
    }
}

fn validate_queue_capacity(capacity: usize) -> Result<(), TransportConfigError> {
    if capacity == 0 || capacity > MAX_QUEUE_CAPACITY {
        Err(TransportConfigError::InvalidQueueCapacity)
    } else {
        Ok(())
    }
}
