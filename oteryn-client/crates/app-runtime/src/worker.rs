use crate::{RuntimeError, WorkerKind};
use oteryn_account_session::AccountSessionId;
use oteryn_foundation::CancellationSource;
use oteryn_game_session::{
    EntryFailure, EntryLifecycle, GameEntryAttemptId, GameEntryCredential, SessionEntered,
};
use oteryn_world_directory::AccountDirectorySnapshot;
use std::fmt::{self, Debug, Formatter};
use std::thread::JoinHandle;

pub(crate) type IdentityOutput = (
    AccountSessionId,
    AccountDirectorySnapshot,
    GameEntryCredential,
);

pub(crate) enum WorkerEvent {
    Identity {
        attempt_id: GameEntryAttemptId,
        result: Result<IdentityOutput, EntryFailure>,
    },
    Connection {
        attempt_id: GameEntryAttemptId,
        lifecycle: EntryLifecycle,
        result: Result<SessionEntered, EntryFailure>,
    },
}

impl Debug for WorkerEvent {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Identity { attempt_id, result } => formatter
                .debug_struct("IdentityWorkerEvent")
                .field("attempt_id", attempt_id)
                .field(
                    "result",
                    &match result {
                        Ok(_) => "Ok([REDACTED IDENTITY OUTPUT])",
                        Err(_) => "Err([TYPED FAILURE])",
                    },
                )
                .finish(),
            Self::Connection {
                attempt_id,
                lifecycle,
                result,
            } => formatter
                .debug_struct("ConnectionWorkerEvent")
                .field("attempt_id", attempt_id)
                .field("lifecycle", lifecycle)
                .field("result", result)
                .finish(),
        }
    }
}

pub(crate) struct OwnedWorker {
    pub(crate) kind: WorkerKind,
    pub(crate) attempt_id: GameEntryAttemptId,
    pub(crate) cancellation: CancellationSource,
    pub(crate) handle: JoinHandle<WorkerEvent>,
}

impl OwnedWorker {
    pub(crate) fn cancel(&self) {
        let _changed = self.cancellation.cancel();
    }

    pub(crate) fn is_finished(&self) -> bool {
        self.handle.is_finished()
    }

    pub(crate) fn join(self) -> Result<WorkerEvent, RuntimeError> {
        self.handle
            .join()
            .map_err(|_panic_payload| RuntimeError::WorkerJoin(self.kind))
    }
}
