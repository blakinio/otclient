//! Small standard-library primitives shared by lower Oteryn client layers.
//!
//! This crate intentionally contains no game, protocol, platform-service or
//! application-runtime policy. It provides typed technical generations,
//! monotonic time and explicit cancellation ownership only.
//!
//! Technical generations are deliberately non-interchangeable:
//!
//! ```compile_fail
//! use oteryn_foundation::{ProcessGeneration, SessionGeneration};
//!
//! fn accepts_process(_: ProcessGeneration) {}
//!
//! accepts_process(SessionGeneration::new(1));
//! ```

mod cancellation;
mod generation;
mod time;

pub use cancellation::{CancellationSource, CancellationToken};
pub use generation::{
    GenerationError, GenerationKind, ProcessGeneration, SessionGeneration, TaskGeneration,
};
pub use time::{Deadline, ManualClock, Moment, MonotonicClock, SystemClock, TimeError};
