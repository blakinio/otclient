//! Deterministic application composition for the W7 technical-login milestone.
//!
//! This crate consumes merged producer types and owns orchestration only.

mod model;
mod runtime;
mod worker;

pub use model::{RuntimeError, RuntimeSnapshot, TechnicalSelection, WorkerKind};
pub use runtime::{MAX_RUNTIME_HISTORY, TechnicalLoginRuntime};

#[cfg(test)]
mod tests;
