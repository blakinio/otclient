//! Deterministic application composition for the W7 technical-login milestone.
//!
//! This crate consumes the merged ENTRY and Identity contracts. It does not
//! define substitute account, directory, credential, transport or Canary
//! protocol types. The final Canary adapter is injected as one owned worker
//! operation after the exact producer interface is merged.

use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{CancellationSource, CancellationToken, MonotonicClock};
use oteryn_game_session::{
    AdmissionCredential, EntryFailure, EntryFailureKind, EntryLifecycle, EntryPhase, EntryProfile,
    GameEntryAttemptId, GameEntryCredential, GameEntryRequest, RecoveryAction, SessionEntered,
};
use oteryn_world_directory::{
    AccountDirectorySnapshot, CharacterId, GameplayChannelId, WorldId,
};
use std::collections::VecDeque;
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};
use std::sync::Arc;
use std::thread::{self, JoinHandle};

/// Maximum retained public lifecycle transitions.
pub const MAX_RUNTIME_HISTORY: usize = 32;

/// Exact non-secret development selection for one technical entry.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct TechnicalSelection {
    character_id: CharacterId,
    world_id: WorldId,
    gameplay_channel_id: Option<GameplayChannelId>,
}

impl TechnicalSelection {
    /// Construct an explicit typed selection without inventing directory data.
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
    /// System-browser, callback and Platform/Gateway bootstrap.
    Identity,
    /// Canary transport/admission attempt.
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

/// Stable application-runtime failure.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RuntimeError {
    /// The merged entry lifecycle rejected an operation.
    Entry(EntryFailure),
    /// A named owned worker could not be started.
    WorkerSpawn(WorkerKind),
    /// A named owned worker panicked or could not be joined.
    WorkerJoin(WorkerKind),
    /// A second authentication worker was requested.
    AuthenticationAlreadyActive,
    /// A second connection worker was requested.
    ConnectionAlreadyActive,
    /// No active entry attempt exists.
    NoActiveAttempt,
    /// The non-zero attempt counter was exhausted.
    AttemptIdExhausted,
    /// Runtime shutdown has started and new work is rejected.
    ShuttingDown,
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
            | Self::ShuttingDown => None,
        }
    }
}

/// Non-secret application view of the composed entry lifecycle.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RuntimeSnapshot {
    phase: EntryPhase,
    active_attempt: Option<GameEntryAttemptId>,
    failure: Option<EntryFailure>,
    entered: Option<SessionEntered>,
    shutting_down: bool,
}

impl RuntimeSnapshot {
    /// Return the exact producer-owned entry phase.
    #[must_use]
    pub const fn phase(self) -> EntryPhase {
        self.phase
    }

    /// Return the current non-secret attempt generation.
    #[must_use]
    pub const fn active_attempt(self) -> Option<GameEntryAttemptId> {
        self.active_attempt
    }

    /// Return the current typed failure.
    #[must_use]
    pub const fn failure(self) -> Option<EntryFailure> {
        self.failure
    }

    /// Return the current non-secret admission result.
    #[must_use]
    pub const fn entered(self) -> Option<SessionEntered> {
        self.entered
    }

    /// Return whether deterministic shutdown has begun.
    #[must_use]
    pub const fn shutting_down(self) -> bool {
        self.shutting_down
    }
}

type IdentityWorkerResult = Result<
    (
        AccountSessionId,
        AccountDirectorySnapshot,
        GameEntryCredential,
    ),
    EntryFailure,
>;

enum WorkerEvent {
    Identity {
        attempt_id: GameEntryAttemptId,
        result: IdentityWorkerResult,
    },
    Connection {
        attempt_id: GameEntryAttemptId,
        result: Result<(), EntryFailure>,
    },
}

impl Debug for WorkerEvent {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Identity { attempt_id, result } => {
                let result = match result {
                    Ok(_) => "Ok([REDACTED IDENTITY OUTPUT])",
                    Err(_) => "Err([TYPED FAILURE])",
                };
                formatter
                    .debug_struct("IdentityWorkerEvent")
                    .field("attempt_id", attempt_id)
                    .field("result", &result)
                    .finish()
            }
            Self::Connection { attempt_id, result } => formatter
                .debug_struct("ConnectionWorkerEvent")
                .field("attempt_id", attempt_id)
                .field("result", result)
                .finish(),
        }
    }
}

struct OwnedWorker {
    kind: WorkerKind,
    attempt_id: GameEntryAttemptId,
    cancellation: CancellationSource,
    handle: JoinHandle<WorkerEvent>,
}

impl OwnedWorker {
    fn cancel(&self) {
        let _changed = self.cancellation.cancel();
    }

    fn is_finished(&self) -> bool {
        self.handle.is_finished()
    }

    fn join(self) -> Result<WorkerEvent, RuntimeError> {
        self.handle
            .join()
            .map_err(|_panic_payload| RuntimeError::WorkerJoin(self.kind))
    }
}

/// Deterministic owner of one authentication worker and one connection worker.
///
/// Worker closures are the application boundary used by the private fake
/// harness. Final application composition captures the exact merged Identity
/// and Canary producer services in these closures; the runtime never exposes a
/// replacement transport or protocol contract.
pub struct TechnicalLoginRuntime {
    clock: Arc<dyn MonotonicClock>,
    lifecycle: EntryLifecycle,
    next_attempt: u64,
    active_attempt: Option<GameEntryAttemptId>,
    selection: Option<TechnicalSelection>,
    identity_worker: Option<OwnedWorker>,
    connection_worker: Option<OwnedWorker>,
    history: VecDeque<EntryPhase>,
    shutting_down: bool,
}

impl TechnicalLoginRuntime {
    /// Construct a logged-out runtime with an injected monotonic clock.
    #[must_use]
    pub fn new(clock: Arc<dyn MonotonicClock>) -> Self {
        let lifecycle = EntryLifecycle::new();
        let mut history = VecDeque::with_capacity(MAX_RUNTIME_HISTORY);
        history.push_back(lifecycle.phase());
        Self {
            clock,
            lifecycle,
            next_attempt: 1,
            active_attempt: None,
            selection: None,
            identity_worker: None,
            connection_worker: None,
            history,
            shutting_down: false,
        }
    }

    /// Return one redacted non-secret snapshot.
    #[must_use]
    pub fn snapshot(&self) -> RuntimeSnapshot {
        RuntimeSnapshot {
            phase: self.lifecycle.phase(),
            active_attempt: self.active_attempt,
            failure: self.lifecycle.failure(),
            entered: self.lifecycle.entered_result(),
            shutting_down: self.shutting_down,
        }
    }

    /// Iterate the bounded producer-owned phase history.
    pub fn history(&self) -> impl ExactSizeIterator<Item = EntryPhase> + '_ {
        self.history.iter().copied()
    }

    /// Start exactly one owned authentication worker.
    ///
    /// The operation must perform the merged Identity flow and return only
    /// producer-owned account, directory and credential values.
    pub fn start_authentication<F>(
        &mut self,
        selection: TechnicalSelection,
        operation: F,
    ) -> Result<GameEntryAttemptId, RuntimeError>
    where
        F: FnOnce(GameEntryAttemptId, CancellationToken) -> IdentityWorkerResult
            + Send
            + 'static,
    {
        if self.shutting_down {
            return Err(RuntimeError::ShuttingDown);
        }
        if self.identity_worker.is_some() {
            return Err(RuntimeError::AuthenticationAlreadyActive);
        }
        if self.connection_worker.is_some() {
            return Err(RuntimeError::ConnectionAlreadyActive);
        }

        let attempt_id = self.allocate_attempt_id()?;
        self.lifecycle.begin_authentication(attempt_id)?;
        self.active_attempt = Some(attempt_id);
        self.selection = Some(selection);
        self.record_phase();

        let cancellation = CancellationSource::new();
        let token = cancellation.token();
        let thread_name = format!("oteryn-identity-{}", attempt_id.get());
        let handle = thread::Builder::new()
            .name(thread_name)
            .spawn(move || WorkerEvent::Identity {
                attempt_id,
                result: operation(attempt_id, token),
            });

        match handle {
            Ok(handle) => {
                self.identity_worker = Some(OwnedWorker {
                    kind: WorkerKind::Identity,
                    attempt_id,
                    cancellation,
                    handle,
                });
                Ok(attempt_id)
            }
            Err(_error) => {
                self.fail_attempt(
                    attempt_id,
                    EntryFailure::for_kind(EntryFailureKind::TransportFailure),
                )?;
                Err(RuntimeError::WorkerSpawn(WorkerKind::Identity))
            }
        }
    }

    /// Start exactly one owned Canary admission worker.
    ///
    /// The moved credential is available only inside the operation. Returning
    /// `Ok(())` asserts that the exact adapter observed its ordered technical
    /// admission marker; the runtime then creates producer-owned
    /// [`SessionEntered`] through [`EntryLifecycle`].
    pub fn start_connection<F>(&mut self, operation: F) -> Result<(), RuntimeError>
    where
        F: FnOnce(GameEntryAttemptId, CancellationToken, AdmissionCredential)
                -> Result<(), EntryFailure>
            + Send
            + 'static,
    {
        if self.shutting_down {
            return Err(RuntimeError::ShuttingDown);
        }
        if self.connection_worker.is_some() {
            return Err(RuntimeError::ConnectionAlreadyActive);
        }
        if self.identity_worker.is_some() {
            return Err(RuntimeError::AuthenticationAlreadyActive);
        }
        let attempt_id = self.active_attempt.ok_or(RuntimeError::NoActiveAttempt)?;
        let credential = self
            .lifecycle
            .begin_connecting(attempt_id, self.clock.as_ref())?;
        self.record_phase();

        let cancellation = CancellationSource::new();
        let token = cancellation.token();
        let thread_name = format!("oteryn-connection-{}", attempt_id.get());
        let handle = thread::Builder::new()
            .name(thread_name)
            .spawn(move || WorkerEvent::Connection {
                attempt_id,
                result: operation(attempt_id, token, credential),
            });

        match handle {
            Ok(handle) => {
                self.connection_worker = Some(OwnedWorker {
                    kind: WorkerKind::Connection,
                    attempt_id,
                    cancellation,
                    handle,
                });
                Ok(())
            }
            Err(_error) => {
                self.fail_attempt(
                    attempt_id,
                    EntryFailure::for_kind(EntryFailureKind::TransportFailure),
                )?;
                Err(RuntimeError::WorkerSpawn(WorkerKind::Connection))
            }
        }
    }

    /// Apply every currently completed worker result.
    ///
    /// Returns `true` when at least one joined worker produced a transition.
    pub fn poll(&mut self) -> Result<bool, RuntimeError> {
        let mut progressed = false;

        if self
            .identity_worker
            .as_ref()
            .is_some_and(OwnedWorker::is_finished)
            && let Some(worker) = self.identity_worker.take()
        {
            let event = self.join_event(worker)?;
            self.apply_event(event)?;
            progressed = true;
        }

        if self
            .connection_worker
            .as_ref()
            .is_some_and(OwnedWorker::is_finished)
            && let Some(worker) = self.connection_worker.take()
        {
            let event = self.join_event(worker)?;
            self.apply_event(event)?;
            progressed = true;
        }

        Ok(progressed)
    }

    /// Cancel active work, join every owned worker and record typed cancellation.
    pub fn cancel_active(&mut self) -> Result<(), RuntimeError> {
        let attempt_id = self.active_attempt.ok_or(RuntimeError::NoActiveAttempt)?;
        self.cancel_workers();
        self.join_and_discard_workers()?;

        if !matches!(
            self.lifecycle.phase(),
            EntryPhase::Failed | EntryPhase::Closing | EntryPhase::LoggedOut
        ) {
            self.lifecycle.cancel(attempt_id)?;
            self.record_phase();
        }
        self.selection = None;
        Ok(())
    }

    /// Disconnect/clear all session-scoped state and return to `LoggedOut`.
    pub fn disconnect_to_logged_out(&mut self) -> Result<(), RuntimeError> {
        self.cancel_workers();
        self.join_and_discard_workers()?;
        self.lifecycle.close();
        self.record_phase();
        self.lifecycle.finish_closing()?;
        self.record_phase();
        self.active_attempt = None;
        self.selection = None;
        Ok(())
    }

    /// Deterministically stop new work, cancel/join workers and clear lifecycle state.
    pub fn shutdown(&mut self) -> Result<(), RuntimeError> {
        if self.shutting_down {
            return Ok(());
        }
        self.shutting_down = true;
        self.disconnect_to_logged_out()
    }

    fn allocate_attempt_id(&mut self) -> Result<GameEntryAttemptId, RuntimeError> {
        let value = self.next_attempt;
        let attempt_id =
            GameEntryAttemptId::new(value).map_err(|_error| RuntimeError::AttemptIdExhausted)?;
        self.next_attempt = value
            .checked_add(1)
            .ok_or(RuntimeError::AttemptIdExhausted)?;
        Ok(attempt_id)
    }

    fn join_event(&mut self, worker: OwnedWorker) -> Result<WorkerEvent, RuntimeError> {
        let attempt_id = worker.attempt_id;
        let kind = worker.kind;
        match worker.join() {
            Ok(event) => Ok(event),
            Err(error) => {
                if self.active_attempt == Some(attempt_id) {
                    let failure = EntryFailure::for_kind(EntryFailureKind::InvariantViolation);
                    let _recorded = self.fail_attempt(attempt_id, failure);
                }
                Err(match error {
                    RuntimeError::WorkerJoin(_) => RuntimeError::WorkerJoin(kind),
                    other => other,
                })
            }
        }
    }

    fn apply_event(&mut self, event: WorkerEvent) -> Result<(), RuntimeError> {
        match event {
            WorkerEvent::Identity { attempt_id, result } => {
                self.require_active_attempt(attempt_id)?;
                match result {
                    Ok((account_session_id, directory, credential)) => self
                        .apply_identity_success(
                            attempt_id,
                            account_session_id,
                            directory,
                            credential,
                        ),
                    Err(failure) => self.fail_attempt(attempt_id, failure),
                }
            }
            WorkerEvent::Connection { attempt_id, result } => {
                self.require_active_attempt(attempt_id)?;
                match result {
                    Ok(()) => {
                        self.lifecycle
                            .session_entered(attempt_id, self.clock.now())?;
                        self.record_phase();
                        Ok(())
                    }
                    Err(failure) => self.fail_attempt(attempt_id, failure),
                }
            }
        }
    }

    fn apply_identity_success(
        &mut self,
        attempt_id: GameEntryAttemptId,
        account_session_id: AccountSessionId,
        directory: AccountDirectorySnapshot,
        credential: GameEntryCredential,
    ) -> Result<(), RuntimeError> {
        self.lifecycle
            .account_ready(attempt_id, account_session_id)?;
        self.record_phase();

        let selection = self.selection.ok_or(RuntimeError::NoActiveAttempt)?;
        let selected_entry = match directory.select(
            directory.revision(),
            selection.character_id(),
            selection.world_id(),
            selection.gameplay_channel_id(),
        ) {
            Ok(selected_entry) => selected_entry,
            Err(error) => {
                let failure = EntryFailure::from(error);
                self.fail_attempt(attempt_id, failure)?;
                return Ok(());
            }
        };

        self.lifecycle.directory_ready(attempt_id, directory)?;
        self.record_phase();
        let request = GameEntryRequest::new(
            attempt_id,
            selected_entry,
            EntryProfile::CanaryCurrent,
            self.clock.now(),
        );
        self.lifecycle.request_entry(request)?;
        self.record_phase();

        if let Err(failure) =
            self.lifecycle
                .credential_ready(attempt_id, credential, self.clock.as_ref())
        {
            self.fail_attempt(attempt_id, failure)?;
            return Ok(());
        }
        self.record_phase();
        Ok(())
    }

    fn require_active_attempt(
        &self,
        attempt_id: GameEntryAttemptId,
    ) -> Result<(), RuntimeError> {
        if self.active_attempt == Some(attempt_id) {
            Ok(())
        } else {
            Err(RuntimeError::Entry(EntryFailure::for_kind(
                EntryFailureKind::StaleAuthenticationTransaction,
            )))
        }
    }

    fn fail_attempt(
        &mut self,
        attempt_id: GameEntryAttemptId,
        failure: EntryFailure,
    ) -> Result<(), RuntimeError> {
        self.lifecycle.record_failure(attempt_id, failure)?;
        self.record_phase();
        self.selection = None;
        Ok(())
    }

    fn cancel_workers(&self) {
        if let Some(worker) = self.identity_worker.as_ref() {
            worker.cancel();
        }
        if let Some(worker) = self.connection_worker.as_ref() {
            worker.cancel();
        }
    }

    fn join_and_discard_workers(&mut self) -> Result<(), RuntimeError> {
        let mut first_error = None;

        if let Some(worker) = self.identity_worker.take()
            && worker.join().is_err()
        {
            first_error = Some(RuntimeError::WorkerJoin(WorkerKind::Identity));
        }
        if let Some(worker) = self.connection_worker.take()
            && worker.join().is_err()
            && first_error.is_none()
        {
            first_error = Some(RuntimeError::WorkerJoin(WorkerKind::Connection));
        }

        if let Some(error) = first_error {
            Err(error)
        } else {
            Ok(())
        }
    }

    fn record_phase(&mut self) {
        let phase = self.lifecycle.phase();
        if self.history.back().copied() == Some(phase) {
            return;
        }
        if self.history.len() == MAX_RUNTIME_HISTORY {
            self.history.pop_front();
        }
        self.history.push_back(phase);
    }
}

impl Debug for TechnicalLoginRuntime {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("TechnicalLoginRuntime")
            .field("snapshot", &self.snapshot())
            .field("identity_worker_active", &self.identity_worker.is_some())
            .field("connection_worker_active", &self.connection_worker.is_some())
            .field("history_len", &self.history.len())
            .finish()
    }
}

impl Drop for TechnicalLoginRuntime {
    fn drop(&mut self) {
        self.cancel_workers();
        let _joined = self.join_and_discard_workers();
        self.lifecycle.close();
        let _closed = self.lifecycle.finish_closing();
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_foundation::{Deadline, ManualClock, Moment};
    use oteryn_world_directory::{
        Availability, CharacterSummary, Compatibility, DirectoryRevision, WorldRoute, WorldSummary,
    };
    use std::sync::Mutex;
    use std::time::Duration;

    fn selection() -> Result<TechnicalSelection, Box<dyn Error>> {
        Ok(TechnicalSelection::new(
            CharacterId::new(22)?,
            WorldId::new(11)?,
            None,
        ))
    }

    fn snapshot(
        account_session_id: AccountSessionId,
        revision: u64,
    ) -> Result<AccountDirectorySnapshot, Box<dyn Error>> {
        let world_id = WorldId::new(11)?;
        let world = WorldSummary::new(
            world_id,
            "canary".to_owned(),
            "Canary".to_owned(),
            "eu".to_owned(),
            WorldRoute::new("canary.example.test".to_owned(), 7172)?,
            Availability::Available,
            Compatibility::Compatible,
        )?;
        let character = CharacterSummary::new(
            CharacterId::new(22)?,
            world_id,
            "Technical Character".to_owned(),
            42,
            "Knight".to_owned(),
            Availability::Available,
            Compatibility::Compatible,
        )?;
        Ok(AccountDirectorySnapshot::new(
            account_session_id,
            DirectoryRevision::new(revision)?,
            vec![world],
            vec![character],
            Vec::new(),
        )?)
    }

    fn identity_result(
        clock: &ManualClock,
        secret: &[u8],
    ) -> Result<
        (
            AccountSessionId,
            AccountDirectorySnapshot,
            GameEntryCredential,
        ),
        Box<dyn Error>,
    > {
        let session_id = AccountSessionId::new(33)?;
        Ok((
            session_id,
            snapshot(session_id, 1)?,
            GameEntryCredential::new(
                secret.to_vec(),
                Deadline::after(clock, Duration::from_secs(30))?,
            )?,
        ))
    }

    fn poll_until_progress(runtime: &mut TechnicalLoginRuntime) -> Result<(), Box<dyn Error>> {
        for _ in 0..10_000 {
            if runtime.poll()? {
                return Ok(());
            }
            thread::yield_now();
        }
        Err("worker did not complete within bounded polling".into())
    }

    #[test]
    fn complete_fake_flow_reaches_session_entered_in_order() -> Result<(), Box<dyn Error>> {
        let manual = ManualClock::new(Moment::ZERO);
        let clock: Arc<dyn MonotonicClock> = Arc::new(manual.clone());
        let mut runtime = TechnicalLoginRuntime::new(clock);
        let identity_clock = manual.clone();

        assert_eq!(runtime.snapshot().phase(), EntryPhase::LoggedOut);
        let attempt_id = runtime.start_authentication(selection()?, move |_attempt, _token| {
            identity_result(&identity_clock, b"fresh-credential")
                .map_err(|_error| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
        })?;
        assert_eq!(runtime.snapshot().phase(), EntryPhase::Authenticating);
        poll_until_progress(&mut runtime)?;
        assert_eq!(runtime.snapshot().phase(), EntryPhase::CredentialReady);

        runtime.start_connection(move |received, token, credential| {
            if received != attempt_id || token.is_cancelled() {
                return Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation));
            }
            if credential.expose_secret() != b"fresh-credential" {
                return Err(EntryFailure::for_kind(EntryFailureKind::CredentialRejected));
            }
            Ok(())
        })?;
        assert_eq!(runtime.snapshot().phase(), EntryPhase::Connecting);
        poll_until_progress(&mut runtime)?;
        assert_eq!(runtime.snapshot().phase(), EntryPhase::SessionEntered);

        assert_eq!(
            runtime.history().collect::<Vec<_>>(),
            vec![
                EntryPhase::LoggedOut,
                EntryPhase::Authenticating,
                EntryPhase::AccountReady,
                EntryPhase::DirectoryReady,
                EntryPhase::EntryRequested,
                EntryPhase::CredentialReady,
                EntryPhase::Connecting,
                EntryPhase::SessionEntered,
            ]
        );
        Ok(())
    }

    #[test]
    fn second_active_authentication_and_connection_are_rejected() -> Result<(), Box<dyn Error>> {
        let manual = ManualClock::new(Moment::ZERO);
        let clock: Arc<dyn MonotonicClock> = Arc::new(manual.clone());
        let mut runtime = TechnicalLoginRuntime::new(clock);
        let identity_clock = manual.clone();

        runtime.start_authentication(selection()?, move |_attempt, _token| {
            identity_result(&identity_clock, b"one")
                .map_err(|_error| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
        })?;
        assert_eq!(
            runtime.start_authentication(selection()?, |_attempt, _token| {
                Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
            }),
            Err(RuntimeError::AuthenticationAlreadyActive)
        );
        poll_until_progress(&mut runtime)?;

        runtime.start_connection(|_attempt, _token, _credential| Ok(()))?;
        assert_eq!(
            runtime.start_connection(|_attempt, _token, _credential| Ok(())),
            Err(RuntimeError::ConnectionAlreadyActive)
        );
        runtime.cancel_active()?;
        assert_eq!(runtime.snapshot().phase(), EntryPhase::Failed);
        Ok(())
    }

    #[test]
    fn cancellation_and_shutdown_join_owned_workers() -> Result<(), Box<dyn Error>> {
        let manual = ManualClock::new(Moment::ZERO);
        let clock: Arc<dyn MonotonicClock> = Arc::new(manual);
        let mut runtime = TechnicalLoginRuntime::new(clock);

        runtime.start_authentication(selection()?, |_attempt, token| {
            while !token.is_cancelled() {
                thread::yield_now();
            }
            Err(EntryFailure::for_kind(EntryFailureKind::SafeCancellation))
        })?;
        runtime.cancel_active()?;
        assert_eq!(runtime.snapshot().phase(), EntryPhase::Failed);
        assert_eq!(
            runtime.snapshot().failure().map(EntryFailure::kind),
            Some(EntryFailureKind::SafeCancellation)
        );

        runtime.shutdown()?;
        assert_eq!(runtime.snapshot().phase(), EntryPhase::LoggedOut);
        assert!(runtime.snapshot().shutting_down());
        assert_eq!(
            runtime.start_authentication(selection()?, |_attempt, _token| {
                Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
            }),
            Err(RuntimeError::ShuttingDown)
        );
        Ok(())
    }

    #[test]
    fn selected_character_mismatch_is_typed_and_recoverable() -> Result<(), Box<dyn Error>> {
        let manual = ManualClock::new(Moment::ZERO);
        let clock: Arc<dyn MonotonicClock> = Arc::new(manual.clone());
        let mut runtime = TechnicalLoginRuntime::new(clock);
        let invalid =
            TechnicalSelection::new(CharacterId::new(999)?, WorldId::new(11)?, None);
        let identity_clock = manual.clone();

        runtime.start_authentication(invalid, move |_attempt, _token| {
            identity_result(&identity_clock, b"not-exposed")
                .map_err(|_error| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
        })?;
        poll_until_progress(&mut runtime)?;

        let failure = runtime
            .snapshot()
            .failure()
            .ok_or("missing typed selection failure")?;
        assert_eq!(failure.kind(), EntryFailureKind::SelectedEntryUnavailable);
        assert_eq!(
            failure.recommended_action(),
            RecoveryAction::ChooseAnotherCharacter
        );
        Ok(())
    }

    #[test]
    fn second_attempt_uses_a_fresh_credential() -> Result<(), Box<dyn Error>> {
        let manual = ManualClock::new(Moment::ZERO);
        let clock: Arc<dyn MonotonicClock> = Arc::new(manual.clone());
        let mut runtime = TechnicalLoginRuntime::new(clock);
        let observed = Arc::new(Mutex::new(Vec::<Vec<u8>>::new()));

        for (index, secret) in [b"first-fresh".as_slice(), b"second-fresh".as_slice()]
            .into_iter()
            .enumerate()
        {
            let identity_clock = manual.clone();
            let owned_secret = secret.to_vec();
            runtime.start_authentication(selection()?, move |_attempt, _token| {
                identity_result(&identity_clock, &owned_secret).map_err(|_error| {
                    EntryFailure::for_kind(EntryFailureKind::InvariantViolation)
                })
            })?;
            poll_until_progress(&mut runtime)?;

            let sink = Arc::clone(&observed);
            runtime.start_connection(move |_attempt, _token, credential| {
                let mut values = sink.lock().map_err(|_poisoned| {
                    EntryFailure::for_kind(EntryFailureKind::InvariantViolation)
                })?;
                values.push(credential.expose_secret().to_vec());
                Ok(())
            })?;
            poll_until_progress(&mut runtime)?;
            assert_eq!(runtime.snapshot().phase(), EntryPhase::SessionEntered);

            assert!(matches!(
                runtime.start_connection(|_attempt, _token, _credential| Ok(())),
                Err(RuntimeError::Entry(failure))
                    if failure.kind() == EntryFailureKind::InvariantViolation
            ));
            runtime.disconnect_to_logged_out()?;
            assert_eq!(runtime.snapshot().phase(), EntryPhase::LoggedOut);
            assert_eq!(runtime.snapshot().active_attempt(), None);
            assert_eq!(index + 1, observed.lock().map_err(|_| "poisoned sink")?.len());
        }

        assert_eq!(
            *observed.lock().map_err(|_| "poisoned sink")?,
            vec![b"first-fresh".to_vec(), b"second-fresh".to_vec()]
        );
        Ok(())
    }

    #[test]
    fn typed_worker_failures_do_not_leak_secret_material() -> Result<(), Box<dyn Error>> {
        let manual = ManualClock::new(Moment::ZERO);
        let clock: Arc<dyn MonotonicClock> = Arc::new(manual.clone());
        let mut runtime = TechnicalLoginRuntime::new(clock);
        let identity_clock = manual.clone();
        let marker = "SECRET-MARKER-DO-NOT-LOG";

        runtime.start_authentication(selection()?, move |_attempt, _token| {
            identity_result(&identity_clock, marker.as_bytes())
                .map_err(|_error| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
        })?;
        poll_until_progress(&mut runtime)?;

        let debug = format!("{runtime:?}");
        assert!(!debug.contains(marker));
        assert!(runtime.snapshot().failure().is_none());
        runtime.start_connection(|_attempt, _token, _credential| {
            Err(EntryFailure::for_kind(
                EntryFailureKind::ServerAdmissionDenied,
            ))
        })?;
        poll_until_progress(&mut runtime)?;
        assert_eq!(
            runtime.snapshot().failure().map(EntryFailure::kind),
            Some(EntryFailureKind::ServerAdmissionDenied)
        );
        assert!(!format!("{runtime:?}").contains(marker));
        assert!(!runtime
            .snapshot()
            .failure()
            .map(|failure| failure.to_string().contains(marker))
            .unwrap_or(false));
        Ok(())
    }

    #[test]
    fn fake_failure_matrix_preserves_typed_recovery() -> Result<(), Box<dyn Error>> {
        let cases = [
            EntryFailureKind::StaleAuthenticationTransaction,
            EntryFailureKind::DuplicateCallback,
            EntryFailureKind::AccountSessionExpired,
            EntryFailureKind::DirectoryRevisionStale,
            EntryFailureKind::SelectedEntryUnavailable,
            EntryFailureKind::CredentialExpired,
            EntryFailureKind::CredentialAlreadyConsumed,
            EntryFailureKind::CredentialRejected,
            EntryFailureKind::ProtocolMismatch,
            EntryFailureKind::AssetClientCompatibilityMismatch,
            EntryFailureKind::TransportFailure,
            EntryFailureKind::ServerAdmissionDenied,
            EntryFailureKind::SafeCancellation,
        ];

        for kind in cases {
            let manual = ManualClock::new(Moment::ZERO);
            let clock: Arc<dyn MonotonicClock> = Arc::new(manual);
            let mut runtime = TechnicalLoginRuntime::new(clock);
            runtime.start_authentication(selection()?, move |_attempt, _token| {
                Err(EntryFailure::for_kind(kind))
            })?;
            poll_until_progress(&mut runtime)?;
            let failure = runtime.snapshot().failure().ok_or("missing failure")?;
            assert_eq!(failure.kind(), kind);
            assert!(!failure.to_string().contains("SECRET"));
        }
        Ok(())
    }
}
