//! Deterministic, test-owned helpers for merged Oteryn technical contracts.
//!
//! This crate composes [`oteryn_foundation::ManualClock`] and
//! [`oteryn_diagnostics`] values for tests. It does not provide another clock,
//! scheduler, executor, runtime service, global fixture registry or sink.
//!
//! Runtime strings cannot become reviewed event messages:
//!
//! ```compile_fail
//! use oteryn_diagnostics::{
//!     DiagnosticCategory, DiagnosticCode, Severity, TechnicalContext,
//! };
//! use oteryn_foundation::{Moment, ProcessGeneration};
//! use oteryn_test_support::DiagnosticEventFixture;
//!
//! let owned = String::from("runtime text");
//! let context = TechnicalContext::new(Moment::ZERO, ProcessGeneration::ZERO);
//! let _fixture = DiagnosticEventFixture::new(
//!     Severity::Info,
//!     DiagnosticCategory::Internal,
//!     DiagnosticCode::new(1),
//!     &owned,
//!     context,
//! );
//! ```
//!
//! Runtime strings cannot become structured field keys either:
//!
//! ```compile_fail
//! use oteryn_diagnostics::{
//!     DiagnosticCategory, DiagnosticCode, DiagnosticValue, Severity, TechnicalContext,
//! };
//! use oteryn_foundation::{Moment, ProcessGeneration};
//! use oteryn_test_support::DiagnosticEventFixture;
//!
//! let context = TechnicalContext::new(Moment::ZERO, ProcessGeneration::ZERO);
//! let mut fixture = DiagnosticEventFixture::new(
//!     Severity::Info,
//!     DiagnosticCategory::Internal,
//!     DiagnosticCode::new(1),
//!     "synthetic event",
//!     context,
//! )?;
//! let owned_key = String::from("runtime_key");
//! fixture.try_add_field(&owned_key, DiagnosticValue::Unsigned(1))?;
//! # Ok::<(), oteryn_test_support::TestSupportError>(())
//! ```

use oteryn_diagnostics::{
    CorrelationId, DiagnosticBuildError, DiagnosticCategory, DiagnosticCode, DiagnosticEvent,
    DiagnosticField, DiagnosticValue, FieldKey, SafeText, Severity, StaticTextError,
    TechnicalContext,
};
use oteryn_foundation::{
    ManualClock, Moment, MonotonicClock, ProcessGeneration, SessionGeneration, TaskGeneration,
    TimeError,
};
use std::fmt::{self, Display, Formatter};
use std::time::Duration;

/// Deterministic test-owned timeline backed directly by the shared manual clock.
#[derive(Debug, Clone)]
pub struct TestTimeline {
    clock: ManualClock,
    process_generation: ProcessGeneration,
}

impl TestTimeline {
    /// Construct a timeline at an explicit moment and process generation.
    #[must_use]
    pub fn new(start: Moment, process_generation: ProcessGeneration) -> Self {
        Self {
            clock: ManualClock::new(start),
            process_generation,
        }
    }

    /// Return a clone of the underlying shared manual clock.
    #[must_use]
    pub fn clock(&self) -> ManualClock {
        self.clock.clone()
    }

    /// Return the current deterministic moment.
    #[must_use]
    pub fn now(&self) -> Moment {
        self.clock.now()
    }

    /// Return the explicit process generation used by this timeline.
    #[must_use]
    pub const fn process_generation(&self) -> ProcessGeneration {
        self.process_generation
    }

    /// Advance the shared timeline by an explicit duration.
    ///
    /// # Errors
    ///
    /// Propagates [`TimeError::Overflow`] without mutating the current moment.
    pub fn advance(&self, duration: Duration) -> Result<Moment, TimeError> {
        self.clock.advance(duration)
    }

    /// Move the shared timeline to an explicit non-decreasing moment.
    ///
    /// # Errors
    ///
    /// Propagates [`TimeError::BackwardMovement`] without mutating the current moment.
    pub fn try_set(&self, requested: Moment) -> Result<(), TimeError> {
        self.clock.try_set(requested)
    }

    /// Build technical context at the timeline's exact current moment.
    #[must_use]
    pub fn context(
        &self,
        session_generation: Option<SessionGeneration>,
        task_generation: Option<TaskGeneration>,
        correlation_id: Option<CorrelationId>,
    ) -> TechnicalContext {
        let mut context = TechnicalContext::new(self.now(), self.process_generation);
        if let Some(generation) = session_generation {
            context = context.with_session(generation);
        }
        if let Some(generation) = task_generation {
            context = context.with_task(generation);
        }
        if let Some(correlation) = correlation_id {
            context = context.with_correlation(correlation);
        }
        context
    }
}

/// Closed failure while composing a deterministic diagnostic fixture.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TestSupportError {
    /// Reviewed static message or field-key validation failed.
    StaticText(StaticTextError),
    /// The bounded diagnostics event rejected a field.
    DiagnosticBuild(DiagnosticBuildError),
}

impl Display for TestSupportError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::StaticText(error) => Display::fmt(error, formatter),
            Self::DiagnosticBuild(error) => Display::fmt(error, formatter),
        }
    }
}

impl std::error::Error for TestSupportError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::StaticText(error) => Some(error),
            Self::DiagnosticBuild(error) => Some(error),
        }
    }
}

impl From<StaticTextError> for TestSupportError {
    fn from(error: StaticTextError) -> Self {
        Self::StaticText(error)
    }
}

impl From<DiagnosticBuildError> for TestSupportError {
    fn from(error: DiagnosticBuildError) -> Self {
        Self::DiagnosticBuild(error)
    }
}

/// Deterministic builder for one classified, bounded diagnostic event.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct DiagnosticEventFixture {
    event: DiagnosticEvent,
}

impl DiagnosticEventFixture {
    /// Construct a fixture from reviewed static message text and explicit context.
    ///
    /// # Errors
    ///
    /// Returns a closed error when the reviewed static message is invalid.
    pub fn new(
        severity: Severity,
        category: DiagnosticCategory,
        code: DiagnosticCode,
        message: &'static str,
        context: TechnicalContext,
    ) -> Result<Self, TestSupportError> {
        let message = SafeText::trusted_static(message)?;
        Ok(Self {
            event: DiagnosticEvent::new(severity, category, code, message, context),
        })
    }

    /// Add one reviewed static key and already-classified value.
    ///
    /// # Errors
    ///
    /// Returns a closed static-text or bounded-event construction error. Rejected
    /// fields do not change the fixture.
    pub fn try_add_field(
        &mut self,
        key: &'static str,
        value: DiagnosticValue,
    ) -> Result<(), TestSupportError> {
        let key = FieldKey::trusted_static(key)?;
        self.event
            .try_add_field(DiagnosticField::new(key, value))?;
        Ok(())
    }

    /// Return the event assembled so far without consuming the fixture.
    #[must_use]
    pub const fn event(&self) -> &DiagnosticEvent {
        &self.event
    }

    /// Consume the fixture and return the deterministic event.
    #[must_use]
    pub fn build(self) -> DiagnosticEvent {
        self.event
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_diagnostics::{MAX_EVENT_FIELDS, SensitiveKind};
    use std::error::Error;
    use std::sync::{Arc, Barrier};
    use std::thread;

    const FIELD_KEYS: [&str; MAX_EVENT_FIELDS] = [
        "field_00", "field_01", "field_02", "field_03", "field_04", "field_05", "field_06",
        "field_07", "field_08", "field_09", "field_10", "field_11", "field_12", "field_13",
        "field_14", "field_15",
    ];

    fn basic_context() -> TechnicalContext {
        TechnicalContext::new(Moment::ZERO, ProcessGeneration::new(1))
    }

    fn basic_fixture() -> Result<DiagnosticEventFixture, TestSupportError> {
        DiagnosticEventFixture::new(
            Severity::Info,
            DiagnosticCategory::Internal,
            DiagnosticCode::new(7),
            "synthetic event",
            basic_context(),
        )
    }

    #[test]
    fn timeline_starts_and_advances_deterministically() -> Result<(), TimeError> {
        let start = Moment::from_elapsed(Duration::from_secs(2));
        let timeline = TestTimeline::new(start, ProcessGeneration::new(3));

        assert_eq!(timeline.now(), start);
        assert_eq!(timeline.process_generation(), ProcessGeneration::new(3));
        assert_eq!(
            timeline.advance(Duration::from_millis(250))?,
            Moment::from_elapsed(Duration::from_millis(2250))
        );
        assert_eq!(
            timeline.now(),
            Moment::from_elapsed(Duration::from_millis(2250))
        );
        Ok(())
    }

    #[test]
    fn cloned_timeline_and_clock_observe_one_state_across_threads() -> Result<(), Box<dyn Error>> {
        let timeline = TestTimeline::new(Moment::ZERO, ProcessGeneration::ZERO);
        let observer = timeline.clone();
        let direct_clock = timeline.clock();
        let ready = Arc::new(Barrier::new(2));
        let released = Arc::new(Barrier::new(2));
        let worker_ready = Arc::clone(&ready);
        let worker_released = Arc::clone(&released);
        let handle = thread::spawn(move || {
            worker_ready.wait();
            worker_released.wait();
            (observer.now(), direct_clock.now())
        });

        ready.wait();
        timeline.advance(Duration::from_secs(4))?;
        released.wait();
        let observed = handle
            .join()
            .map_err(|_| std::io::Error::other("test observer thread panicked"))?;

        assert_eq!(observed, (timeline.now(), timeline.now()));
        Ok(())
    }

    #[test]
    fn backwards_and_overflow_failures_leave_time_unchanged() {
        let current = Moment::from_elapsed(Duration::from_secs(5));
        let timeline = TestTimeline::new(current, ProcessGeneration::ZERO);
        let requested = Moment::from_elapsed(Duration::from_secs(4));

        assert_eq!(
            timeline.try_set(requested),
            Err(TimeError::BackwardMovement { current, requested })
        );
        assert_eq!(timeline.now(), current);

        let maximum = Moment::from_elapsed(Duration::MAX);
        let overflow = TestTimeline::new(maximum, ProcessGeneration::ZERO);
        assert_eq!(
            overflow.advance(Duration::from_nanos(1)),
            Err(TimeError::Overflow {
                base: maximum,
                duration: Duration::from_nanos(1),
            })
        );
        assert_eq!(overflow.now(), maximum);
    }

    #[test]
    fn context_uses_exact_current_time_and_explicit_identifiers() -> Result<(), TimeError> {
        let timeline = TestTimeline::new(Moment::ZERO, ProcessGeneration::new(2));
        timeline.advance(Duration::from_secs(3))?;
        let context = timeline.context(
            Some(SessionGeneration::new(5)),
            Some(TaskGeneration::new(8)),
            Some(CorrelationId::new(13)),
        );

        assert_eq!(context.occurred_at(), timeline.now());
        assert_eq!(context.process_generation(), ProcessGeneration::new(2));
        assert_eq!(context.session_generation(), Some(SessionGeneration::new(5)));
        assert_eq!(context.task_generation(), Some(TaskGeneration::new(8)));
        assert_eq!(context.correlation_id(), Some(CorrelationId::new(13)));
        Ok(())
    }

    #[test]
    fn fixture_preserves_field_insertion_order() -> Result<(), TestSupportError> {
        let mut fixture = basic_fixture()?;
        fixture.try_add_field("first_field", DiagnosticValue::Unsigned(1))?;
        fixture.try_add_field("second_field", DiagnosticValue::Boolean(true))?;
        let event = fixture.build();

        assert_eq!(event.fields()[0].key().as_str(), "first_field");
        assert_eq!(event.fields()[1].key().as_str(), "second_field");
        Ok(())
    }

    #[test]
    fn duplicate_and_field_bound_failures_do_not_mutate_fixture() -> Result<(), TestSupportError> {
        let mut duplicate = basic_fixture()?;
        duplicate.try_add_field("same_field", DiagnosticValue::Unsigned(1))?;
        assert_eq!(
            duplicate.try_add_field("same_field", DiagnosticValue::Unsigned(2)),
            Err(TestSupportError::DiagnosticBuild(
                DiagnosticBuildError::DuplicateField
            ))
        );
        assert_eq!(duplicate.event().field_count(), 1);

        let mut bounded = basic_fixture()?;
        for (index, key) in FIELD_KEYS.into_iter().enumerate() {
            bounded.try_add_field(key, DiagnosticValue::Unsigned(index as u64))?;
        }
        assert_eq!(
            bounded.try_add_field("overflow_field", DiagnosticValue::Unsigned(17)),
            Err(TestSupportError::DiagnosticBuild(
                DiagnosticBuildError::TooManyFields {
                    max_fields: MAX_EVENT_FIELDS,
                }
            ))
        );
        assert_eq!(bounded.event().field_count(), MAX_EVENT_FIELDS);
        Ok(())
    }

    #[test]
    fn redacted_runtime_text_is_absent_from_display_debug_and_clones(
    ) -> Result<(), TestSupportError> {
        let marker = "synthetic-secret-shaped-marker";
        let mut fixture = basic_fixture()?;
        fixture.try_add_field(
            "sensitive_value",
            DiagnosticValue::redacted(SensitiveKind::Confidential, marker),
        )?;
        let event = fixture.build();
        let cloned = event.clone();
        let display = event.to_string();
        let debug = format!("{cloned:?}");

        assert!(!display.contains(marker));
        assert!(!debug.contains(marker));
        assert!(display.contains("<redacted:confidential>"));
        assert!(debug.contains("<redacted:confidential>"));
        Ok(())
    }

    #[test]
    fn errors_are_closed_and_secret_free() {
        let static_error = TestSupportError::StaticText(StaticTextError::InvalidCharacters);
        let build_error = TestSupportError::DiagnosticBuild(DiagnosticBuildError::DuplicateField);

        assert_eq!(
            static_error.to_string(),
            "diagnostic static text contains invalid characters"
        );
        assert_eq!(
            build_error.to_string(),
            "diagnostic event contains a duplicate field key"
        );
    }
}
