use oteryn_game_session::{EntryFailure, EntryPhase, GameEntryAttemptId, SessionEntered};
use oteryn_world_directory::{CharacterId, GameplayChannelId, WorldId};
use std::error::Error;
use std::fmt::{self, Display, Formatter};

/// Exact typed development selection for one technical entry.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TechnicalSelection {
    character_id: CharacterId,
    world_id: WorldId,
    gameplay_channel_id: Option<GameplayChannelId>,
}

impl TechnicalSelection {
    /// Construct a selection without inventing directory data.
    #[must_use]
    pub const fn new(
        character_id: CharacterId,
        world_id: WorldId,
        gameplay_channel_id: Option<GameplayChannelId>,
    ) -> Self {
        Self {
            character_id,
            world_id,
            gameplay_channel_id,
        }
    }

    /// Return the selected character.
    #[must_use]
    pub const fn character_id(self) -> CharacterId {
        self.character_id
    }

    /// Return the selected world.
    #[must_use]
    pub const fn world_id(self) -> WorldId {
        self.world_id
    }

    /// Return the optional selected gameplay channel.
    #[must_use]
    pub const fn gameplay_channel_id(self) -> Option<GameplayChannelId> {
        self.gameplay_channel_id
    }
}

/// Closed owned worker categories.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum WorkerKind {
    /// Browser/callback and Platform/Gateway bootstrap.
    Identity,
    /// Canary connection/admission.
    Connection,
}

impl Display for WorkerKind {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::Identity => "identity",
            Self::Connection => "connection",
        })
    }
}

/// Nonblocking progress of one explicit technical-login shutdown.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ShutdownProgress {
    /// Cancellation was requested and the worker remains owned and unfinished.
    Pending(WorkerKind),
    /// The worker remains owned and unfinished beyond the accepted bound.
    Overdue(WorkerKind),
    /// No worker remains and the runtime is terminally logged out.
    Complete,
}

/// Stable secret-free runtime failure.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RuntimeError {
    /// The merged entry lifecycle rejected the operation.
    Entry(EntryFailure),
    /// A named worker could not start.
    WorkerSpawn(WorkerKind),
    /// A named worker panicked or could not be joined.
    WorkerJoin(WorkerKind),
    /// A second authentication worker was requested.
    AuthenticationAlreadyActive,
    /// A second connection worker was requested.
    ConnectionAlreadyActive,
    /// No entry attempt exists.
    NoActiveAttempt,
    /// The non-zero attempt counter was exhausted.
    AttemptIdExhausted,
    /// Shutdown started and rejects new work.
    ShuttingDown,
    /// Shutdown polling was requested before shutdown began.
    ShutdownNotStarted,
    /// An owned worker remains unfinished during a nonblocking operation.
    ShutdownPending,
    /// An owned worker remains unfinished beyond the accepted shutdown bound.
    ShutdownOverdue(WorkerKind),
}

impl From<EntryFailure> for RuntimeError {
    fn from(failure: EntryFailure) -> Self {
        Self::Entry(failure)
    }
}

impl Display for RuntimeError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Entry(failure) => Display::fmt(failure, formatter),
            Self::WorkerSpawn(kind) => write!(formatter, "{kind} worker could not be started"),
            Self::WorkerJoin(kind) => write!(formatter, "{kind} worker did not finish cleanly"),
            Self::AuthenticationAlreadyActive => {
                formatter.write_str("one authentication attempt is already active")
            }
            Self::ConnectionAlreadyActive => {
                formatter.write_str("one connection attempt is already active")
            }
            Self::NoActiveAttempt => formatter.write_str("no technical-login attempt is active"),
            Self::AttemptIdExhausted => formatter.write_str("entry attempt identity was exhausted"),
            Self::ShuttingDown => formatter.write_str("technical-login runtime is shutting down"),
            Self::ShutdownNotStarted => {
                formatter.write_str("technical-login shutdown has not started")
            }
            Self::ShutdownPending => {
                formatter.write_str("technical-login shutdown is still pending")
            }
            Self::ShutdownOverdue(kind) => {
                write!(formatter, "{kind} worker shutdown is overdue")
            }
        }
    }
}

impl Error for RuntimeError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Entry(failure) => Some(failure),
            Self::WorkerSpawn(_)
            | Self::WorkerJoin(_)
            | Self::AuthenticationAlreadyActive
            | Self::ConnectionAlreadyActive
            | Self::NoActiveAttempt
            | Self::AttemptIdExhausted
            | Self::ShuttingDown
            | Self::ShutdownNotStarted
            | Self::ShutdownPending
            | Self::ShutdownOverdue(_) => None,
        }
    }
}

/// Non-secret view consumed by the application shell.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RuntimeSnapshot {
    pub(crate) phase: EntryPhase,
    pub(crate) active_attempt: Option<GameEntryAttemptId>,
    pub(crate) failure: Option<EntryFailure>,
    pub(crate) entered: Option<SessionEntered>,
    pub(crate) shutting_down: bool,
}

impl RuntimeSnapshot {
    /// Return the producer-owned phase classification.
    #[must_use]
    pub const fn phase(self) -> EntryPhase {
        self.phase
    }

    /// Return the current non-secret attempt.
    #[must_use]
    pub const fn active_attempt(self) -> Option<GameEntryAttemptId> {
        self.active_attempt
    }

    /// Return the current typed failure.
    #[must_use]
    pub const fn failure(self) -> Option<EntryFailure> {
        self.failure
    }

    /// Return the current admission result.
    #[must_use]
    pub const fn entered(self) -> Option<SessionEntered> {
        self.entered
    }

    /// Return whether shutdown has begun.
    #[must_use]
    pub const fn shutting_down(self) -> bool {
        self.shutting_down
    }
}
