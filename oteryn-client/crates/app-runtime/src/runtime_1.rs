use crate::worker::{OwnedWorker, WorkerEvent};
use crate::{RuntimeError, RuntimeSnapshot, ShutdownProgress, TechnicalSelection, WorkerKind};
use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{CancellationSource, CancellationToken, Moment, MonotonicClock};
use oteryn_game_session::{
    EntryFailure, EntryFailureKind, EntryLifecycle, EntryPhase, EntryProfile, GameEntryAttemptId,
    GameEntryCredential, GameEntryRequest, SessionEntered,
};
use oteryn_world_directory::AccountDirectorySnapshot;
use std::collections::VecDeque;
use std::fmt::{self, Debug, Formatter};
use std::sync::Arc;
use std::thread;
use std::time::Duration;

/// Maximum retained non-secret lifecycle transitions.
pub const MAX_RUNTIME_HISTORY: usize = 32;
/// Bound after which shutdown reports an overdue worker while retaining ownership.
pub const SHUTDOWN_OVERDUE_AFTER: Duration = Duration::from_secs(31);

/// Deterministic owner of one authentication and one connection worker.
pub struct TechnicalLoginRuntime {
    clock: Arc<dyn MonotonicClock>,
    lifecycle: Option<EntryLifecycle>,
    phase: EntryPhase,
    failure: Option<EntryFailure>,
    entered: Option<SessionEntered>,
    next_attempt: u64,
    active_attempt: Option<GameEntryAttemptId>,
    selection: Option<TechnicalSelection>,
    identity_worker: Option<OwnedWorker>,
    connection_worker: Option<OwnedWorker>,
    history: VecDeque<EntryPhase>,
    shutdown_started: Option<Moment>,
}
