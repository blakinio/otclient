use std::sync::Arc;
use std::sync::atomic::{AtomicBool, Ordering};

#[derive(Debug)]
struct CancellationState {
    cancelled: AtomicBool,
}

/// Unique owner of explicit cancellation authority.
///
/// Cancellation is idempotent. Dropping a source does **not** cancel its
/// tokens: owners must call [`Self::cancel`] explicitly when cancellation is
/// part of their lifecycle. The shared state is released after the source and
/// every token are dropped.
#[derive(Debug)]
pub struct CancellationSource {
    state: Arc<CancellationState>,
}

impl CancellationSource {
    /// Create an uncancelled source.
    #[must_use]
    pub fn new() -> Self {
        Self {
            state: Arc::new(CancellationState {
                cancelled: AtomicBool::new(false),
            }),
        }
    }

    /// Create an observer token for this source.
    #[must_use]
    pub fn token(&self) -> CancellationToken {
        CancellationToken {
            state: Arc::clone(&self.state),
        }
    }

    /// Explicitly cancel this source.
    ///
    /// Returns `true` only for the call that changes the shared state from
    /// uncancelled to cancelled. Every later call returns `false`.
    #[must_use]
    pub fn cancel(&self) -> bool {
        !self.state.cancelled.swap(true, Ordering::AcqRel)
    }

    /// Return whether this source has been cancelled.
    #[must_use]
    pub fn is_cancelled(&self) -> bool {
        self.state.cancelled.load(Ordering::Acquire)
    }
}

impl Default for CancellationSource {
    fn default() -> Self {
        Self::new()
    }
}

/// Cloneable observer of one explicit cancellation source.
///
/// A token has no cancellation authority. Dropping any token has no effect on
/// the source or other tokens. Dropping the final token releases only its
/// shared observation state and never starts or stops background work.
#[derive(Debug, Clone)]
pub struct CancellationToken {
    state: Arc<CancellationState>,
}

impl CancellationToken {
    /// Return whether the owning source explicitly cancelled the operation.
    #[must_use]
    pub fn is_cancelled(&self) -> bool {
        self.state.cancelled.load(Ordering::Acquire)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::sync::Barrier;
    use std::thread;

    #[test]
    fn cancellation_is_idempotent_and_visible_to_all_clones() {
        let source = CancellationSource::new();
        let first = source.token();
        let second = first.clone();

        assert!(!first.is_cancelled());
        assert!(source.cancel());
        assert!(!source.cancel());
        assert!(source.is_cancelled());
        assert!(first.is_cancelled());
        assert!(second.is_cancelled());
    }

    #[test]
    fn dropping_an_observer_does_not_cancel_independent_work() {
        let source = CancellationSource::new();
        let dropped = source.token();
        let remaining = source.token();

        drop(dropped);

        assert!(!source.is_cancelled());
        assert!(!remaining.is_cancelled());
        assert!(source.cancel());
        assert!(remaining.is_cancelled());
    }

    #[test]
    fn dropping_the_source_does_not_implicitly_cancel() {
        let token = {
            let source = CancellationSource::new();
            source.token()
        };

        assert!(!token.is_cancelled());
    }

    #[test]
    fn repeated_create_cancel_and_drop_releases_shared_state() {
        for _ in 0..512 {
            let weak = {
                let source = CancellationSource::new();
                let first = source.token();
                let second = first.clone();
                let weak = Arc::downgrade(&source.state);

                assert!(source.cancel());
                drop(first);
                drop(second);
                drop(source);
                weak
            };

            assert!(weak.upgrade().is_none());
        }
    }

    #[test]
    fn cancellation_race_is_thread_safe() -> Result<(), &'static str> {
        const RACERS: usize = 8;

        let source = CancellationSource::new();
        let token = source.token();
        let start = Barrier::new(RACERS + 1);

        let (winners, all_observed) = thread::scope(|scope| {
            let mut handles = Vec::with_capacity(RACERS);

            for _ in 0..RACERS {
                let observer = token.clone();
                let owner = &source;
                let start_line = &start;
                handles.push(scope.spawn(move || {
                    start_line.wait();
                    (owner.cancel(), observer.is_cancelled())
                }));
            }

            start.wait();

            let mut winners = 0;
            let mut all_observed = true;
            for handle in handles {
                let (won, observed) = handle.join().map_err(|_| "cancellation racer panicked")?;
                winners += usize::from(won);
                all_observed &= observed;
            }

            Ok::<_, &'static str>((winners, all_observed))
        })?;

        assert_eq!(winners, 1);
        assert!(all_observed);
        Ok(())
    }
}
