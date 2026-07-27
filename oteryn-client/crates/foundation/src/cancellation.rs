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
    fn cancellation_observation_is_thread_safe() -> Result<(), &'static str> {
        const OBSERVERS: usize = 8;
        const SPINS: usize = 1_000_000;

        let source = CancellationSource::new();
        let token = source.token();
        let barrier = Arc::new(Barrier::new(OBSERVERS + 1));
        let mut handles = Vec::with_capacity(OBSERVERS);

        for _ in 0..OBSERVERS {
            let observer = token.clone();
            let start = Arc::clone(&barrier);
            handles.push(thread::spawn(move || {
                start.wait();
                for _ in 0..SPINS {
                    if observer.is_cancelled() {
                        return true;
                    }
                    std::hint::spin_loop();
                }
                observer.is_cancelled()
            }));
        }

        barrier.wait();
        assert!(source.cancel());

        for handle in handles {
            let observed = handle.join().map_err(|_| "cancellation observer panicked")?;
            assert!(observed);
        }
        Ok(())
    }
}
