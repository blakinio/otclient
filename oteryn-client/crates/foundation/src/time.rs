use std::fmt::{self, Display, Formatter};
use std::sync::{Arc, RwLock};
use std::time::{Duration, Instant};

/// Monotonic time elapsed from a clock-specific origin.
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Moment(Duration);

impl Moment {
    /// The clock origin.
    pub const ZERO: Self = Self(Duration::ZERO);

    /// Construct a moment from elapsed monotonic time.
    #[must_use]
    pub const fn from_elapsed(elapsed: Duration) -> Self {
        Self(elapsed)
    }

    /// Return elapsed monotonic time from the clock origin.
    #[must_use]
    pub const fn elapsed(self) -> Duration {
        self.0
    }

    /// Add a duration without overflowing.
    ///
    /// # Errors
    ///
    /// Returns [`TimeError::Overflow`] when the resulting moment cannot be represented.
    pub fn checked_add(self, duration: Duration) -> Result<Self, TimeError> {
        self.0
            .checked_add(duration)
            .map(Self)
            .ok_or(TimeError::Overflow {
                base: self,
                duration,
            })
    }

    /// Measure a monotonic interval.
    ///
    /// # Errors
    ///
    /// Returns [`TimeError::NonMonotonicInterval`] when `self` is before `start`.
    pub fn checked_duration_since(self, start: Self) -> Result<Duration, TimeError> {
        self.0
            .checked_sub(start.0)
            .ok_or(TimeError::NonMonotonicInterval { start, end: self })
    }
}

impl Display for Moment {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write_duration(formatter, self.0)
    }
}

/// An absolute monotonic deadline.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Deadline(Moment);

impl Deadline {
    /// Construct a deadline at an explicit monotonic moment.
    #[must_use]
    pub const fn at(moment: Moment) -> Self {
        Self(moment)
    }

    /// Construct a deadline after a duration measured by `clock`.
    ///
    /// # Errors
    ///
    /// Returns [`TimeError::Overflow`] when the deadline cannot be represented.
    pub fn after<C>(clock: &C, duration: Duration) -> Result<Self, TimeError>
    where
        C: MonotonicClock + ?Sized,
    {
        clock.now().checked_add(duration).map(Self)
    }

    /// Return the deadline's absolute monotonic moment.
    #[must_use]
    pub const fn moment(self) -> Moment {
        self.0
    }

    /// Return whether the deadline has elapsed according to `clock`.
    #[must_use]
    pub fn has_elapsed<C>(self, clock: &C) -> bool
    where
        C: MonotonicClock + ?Sized,
    {
        clock.now() >= self.0
    }

    /// Return remaining monotonic time, saturating at zero after expiry.
    #[must_use]
    pub fn remaining<C>(self, clock: &C) -> Duration
    where
        C: MonotonicClock + ?Sized,
    {
        self.0.elapsed().saturating_sub(clock.now().elapsed())
    }
}

/// Narrow interface for clocks used in timeout and lifecycle ordering.
pub trait MonotonicClock: Send + Sync {
    /// Return elapsed monotonic time from this clock's origin.
    fn now(&self) -> Moment;
}

/// Production monotonic clock backed only by [`Instant`].
#[derive(Debug, Clone)]
pub struct SystemClock {
    origin: Instant,
}

impl SystemClock {
    /// Create a clock whose origin is the current monotonic instant.
    #[must_use]
    pub fn new() -> Self {
        Self {
            origin: Instant::now(),
        }
    }
}

impl Default for SystemClock {
    fn default() -> Self {
        Self::new()
    }
}

impl MonotonicClock for SystemClock {
    fn now(&self) -> Moment {
        Moment::from_elapsed(self.origin.elapsed())
    }
}

/// Deterministic thread-safe clock advanced explicitly by tests or owners.
///
/// Clones share one current moment. The API never moves time backwards:
/// [`Self::try_set`] rejects a requested moment before the current one.
#[derive(Debug, Clone)]
pub struct ManualClock {
    current: Arc<RwLock<Moment>>,
}

impl ManualClock {
    /// Create a manual clock at an explicit monotonic moment.
    #[must_use]
    pub fn new(start: Moment) -> Self {
        Self {
            current: Arc::new(RwLock::new(start)),
        }
    }

    /// Advance the shared clock by an explicit duration.
    ///
    /// # Errors
    ///
    /// Returns [`TimeError::Overflow`] when the resulting moment cannot be represented.
    pub fn advance(&self, duration: Duration) -> Result<Moment, TimeError> {
        let mut current = match self.current.write() {
            Ok(guard) => guard,
            Err(poisoned) => poisoned.into_inner(),
        };
        let next = current.checked_add(duration)?;
        *current = next;
        Ok(next)
    }

    /// Move the shared clock to an explicit moment without allowing backwards time.
    ///
    /// Equal moments are accepted and leave the clock unchanged.
    ///
    /// # Errors
    ///
    /// Returns [`TimeError::BackwardMovement`] when `requested` is before the current moment.
    pub fn try_set(&self, requested: Moment) -> Result<(), TimeError> {
        let mut current = match self.current.write() {
            Ok(guard) => guard,
            Err(poisoned) => poisoned.into_inner(),
        };
        if requested < *current {
            return Err(TimeError::BackwardMovement {
                current: *current,
                requested,
            });
        }
        *current = requested;
        Ok(())
    }
}

impl MonotonicClock for ManualClock {
    fn now(&self) -> Moment {
        let current = match self.current.read() {
            Ok(guard) => guard,
            Err(poisoned) => poisoned.into_inner(),
        };
        *current
    }
}

/// Failure produced by checked monotonic-time operations.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TimeError {
    /// Adding a duration exceeded the representable [`Duration`] range.
    Overflow {
        /// Moment at which addition started.
        base: Moment,
        /// Duration that could not be added.
        duration: Duration,
    },
    /// A manual clock was asked to move before its current moment.
    BackwardMovement {
        /// Current clock moment.
        current: Moment,
        /// Rejected requested moment.
        requested: Moment,
    },
    /// An interval ended before it started.
    NonMonotonicInterval {
        /// Intended interval start.
        start: Moment,
        /// Rejected interval end.
        end: Moment,
    },
}

impl Display for TimeError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Overflow { base, duration } => {
                write!(formatter, "monotonic time overflow at {base} while adding ")?;
                write_duration(formatter, *duration)
            }
            Self::BackwardMovement { current, requested } => write!(
                formatter,
                "manual clock cannot move backwards from {current} to {requested}"
            ),
            Self::NonMonotonicInterval { start, end } => write!(
                formatter,
                "monotonic interval end {end} is before start {start}"
            ),
        }
    }
}

impl std::error::Error for TimeError {}

fn write_duration(formatter: &mut Formatter<'_>, duration: Duration) -> fmt::Result {
    write!(
        formatter,
        "{}.{:09}s",
        duration.as_secs(),
        duration.subsec_nanos()
    )
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn system_clock_never_reports_before_its_origin() {
        let clock = SystemClock::new();
        let first = clock.now();
        let second = clock.now();

        assert!(first >= Moment::ZERO);
        assert!(second >= first);
    }

    #[test]
    fn manual_clock_advances_deterministically_and_shares_state() -> Result<(), TimeError> {
        let clock = ManualClock::new(Moment::from_elapsed(Duration::from_secs(2)));
        let observer = clock.clone();

        assert_eq!(clock.advance(Duration::from_millis(250))?.elapsed(), Duration::from_millis(2250));
        assert_eq!(observer.now(), clock.now());
        Ok(())
    }

    #[test]
    fn manual_clock_rejects_backwards_movement() {
        let current = Moment::from_elapsed(Duration::from_secs(5));
        let requested = Moment::from_elapsed(Duration::from_secs(4));
        let clock = ManualClock::new(current);

        assert_eq!(
            clock.try_set(requested),
            Err(TimeError::BackwardMovement { current, requested })
        );
        assert_eq!(clock.now(), current);
    }

    #[test]
    fn deadlines_use_explicit_monotonic_duration() -> Result<(), TimeError> {
        let clock = ManualClock::new(Moment::ZERO);
        let deadline = Deadline::after(&clock, Duration::from_secs(3))?;

        assert_eq!(deadline.remaining(&clock), Duration::from_secs(3));
        assert!(!deadline.has_elapsed(&clock));
        clock.advance(Duration::from_secs(2))?;
        assert_eq!(deadline.remaining(&clock), Duration::from_secs(1));
        clock.advance(Duration::from_secs(1))?;
        assert!(deadline.has_elapsed(&clock));
        assert_eq!(deadline.remaining(&clock), Duration::ZERO);
        Ok(())
    }

    #[test]
    fn invalid_interval_is_explicit() {
        let start = Moment::from_elapsed(Duration::from_secs(2));
        let end = Moment::from_elapsed(Duration::from_secs(1));

        assert_eq!(
            end.checked_duration_since(start),
            Err(TimeError::NonMonotonicInterval { start, end })
        );
    }

    #[test]
    fn time_errors_have_deterministic_safe_output() {
        let error = TimeError::BackwardMovement {
            current: Moment::from_elapsed(Duration::from_secs(2)),
            requested: Moment::from_elapsed(Duration::from_secs(1)),
        };

        assert_eq!(
            error.to_string(),
            "manual clock cannot move backwards from 2.000000000s to 1.000000000s"
        );
        assert_eq!(
            format!("{error:?}"),
            "BackwardMovement { current: Moment(2s), requested: Moment(1s) }"
        );
    }
}
