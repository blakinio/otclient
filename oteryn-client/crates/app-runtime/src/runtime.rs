use crate::worker::{OwnedWorker, WorkerEvent};
use crate::{RuntimeError, RuntimeSnapshot, TechnicalSelection, WorkerKind};
use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{CancellationSource, CancellationToken, MonotonicClock};
use oteryn_game_session::{
    EntryFailure, EntryFailureKind, EntryLifecycle, EntryPhase, EntryProfile, GameEntryAttemptId,
    GameEntryCredential, GameEntryRequest, SessionEntered,
};
use oteryn_world_directory::AccountDirectorySnapshot;
use std::collections::VecDeque;
use std::fmt::{self, Debug, Formatter};
use std::sync::Arc;
use std::thread;

/// Maximum retained non-secret lifecycle transitions.
pub const MAX_RUNTIME_HISTORY: usize = 32;

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
    shutting_down: bool,
}

impl TechnicalLoginRuntime {
    /// Construct a logged-out runtime.
    #[must_use]
    pub fn new(clock: Arc<dyn MonotonicClock>) -> Self {
        let mut history = VecDeque::with_capacity(MAX_RUNTIME_HISTORY);
        history.push_back(EntryPhase::LoggedOut);
        Self {
            clock,
            lifecycle: Some(EntryLifecycle::new()),
            phase: EntryPhase::LoggedOut,
            failure: None,
            entered: None,
            next_attempt: 1,
            active_attempt: None,
            selection: None,
            identity_worker: None,
            connection_worker: None,
            history,
            shutting_down: false,
        }
    }

    /// Return one redacted snapshot.
    #[must_use]
    pub const fn snapshot(&self) -> RuntimeSnapshot {
        RuntimeSnapshot {
            phase: self.phase,
            active_attempt: self.active_attempt,
            failure: self.failure,
            entered: self.entered,
            shutting_down: self.shutting_down,
        }
    }

    /// Iterate bounded phases in deterministic order.
    pub fn history(&self) -> impl ExactSizeIterator<Item = EntryPhase> + '_ {
        self.history.iter().copied()
    }

    /// Start one Identity operation on an owned thread.
    ///
    /// Final composition maps merged `IdentityBootstrap` into the returned
    /// producer-owned tuple.
    pub fn start_authentication<F>(
        &mut self,
        selection: TechnicalSelection,
        operation: F,
    ) -> Result<GameEntryAttemptId, RuntimeError>
    where
        F: FnOnce(
                GameEntryAttemptId,
                CancellationToken,
            ) -> Result<
                (
                    AccountSessionId,
                    AccountDirectorySnapshot,
                    GameEntryCredential,
                ),
                EntryFailure,
            > + Send
            + 'static,
    {
        self.require_startable()?;
        let attempt_id = self.allocate_attempt_id()?;
        self.lifecycle_mut()?.begin_authentication(attempt_id)?;
        self.active_attempt = Some(attempt_id);
        self.selection = Some(selection);
        self.failure = None;
        self.entered = None;
        self.sync_phase();

        let cancellation = CancellationSource::new();
        let token = cancellation.token();
        let handle = thread::Builder::new()
            .name(format!("oteryn-identity-{}", attempt_id.get()))
            .spawn(move || WorkerEvent::Identity {
                attempt_id,
                result: operation(attempt_id, token),
            });

        match handle {
            Ok(handle) => {
                self.identity_worker = Some(OwnedWorker {
                    kind: WorkerKind::Identity,
                    cancellation,
                    handle,
                });
                Ok(attempt_id)
            }
            Err(_error) => {
                self.set_failure(EntryFailure::for_kind(EntryFailureKind::TransportFailure));
                Err(RuntimeError::WorkerSpawn(WorkerKind::Identity))
            }
        }
    }

    /// Move the complete producer-owned lifecycle into one admission worker.
    ///
    /// This matches the Canary producer boundary: application code never
    /// receives `AdmissionCredential`. The closure returns the lifecycle it
    /// consumed together with its typed result.
    pub fn start_connection<F>(&mut self, operation: F) -> Result<(), RuntimeError>
    where
        F: FnOnce(
                EntryLifecycle,
                GameEntryAttemptId,
                CancellationToken,
                Arc<dyn MonotonicClock>,
            ) -> (EntryLifecycle, Result<SessionEntered, EntryFailure>)
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
        if self.phase != EntryPhase::CredentialReady {
            return Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation).into());
        }

        let attempt_id = self.active_attempt.ok_or(RuntimeError::NoActiveAttempt)?;
        let lifecycle = self.lifecycle.take().ok_or(RuntimeError::NoActiveAttempt)?;
        let cancellation = CancellationSource::new();
        let token = cancellation.token();
        let clock = Arc::clone(&self.clock);
        let handle = thread::Builder::new()
            .name(format!("oteryn-connection-{}", attempt_id.get()))
            .spawn(move || {
                let (lifecycle, result) = operation(lifecycle, attempt_id, token, clock);
                WorkerEvent::Connection {
                    attempt_id,
                    lifecycle,
                    result,
                }
            });

        match handle {
            Ok(handle) => {
                self.connection_worker = Some(OwnedWorker {
                    kind: WorkerKind::Connection,
                    cancellation,
                    handle,
                });
                self.record_phase(EntryPhase::Connecting);
                Ok(())
            }
            Err(_error) => {
                self.lifecycle = Some(EntryLifecycle::new());
                self.set_failure(EntryFailure::for_kind(EntryFailureKind::TransportFailure));
                Err(RuntimeError::WorkerSpawn(WorkerKind::Connection))
            }
        }
    }

    /// Join and apply every currently completed worker.
    pub fn poll(&mut self) -> Result<bool, RuntimeError> {
        let mut progressed = false;
        if self
            .identity_worker
            .as_ref()
            .is_some_and(OwnedWorker::is_finished)
            && let Some(worker) = self.identity_worker.take()
        {
            self.apply_event(worker.join()?)?;
            progressed = true;
        }
        if self
            .connection_worker
            .as_ref()
            .is_some_and(OwnedWorker::is_finished)
            && let Some(worker) = self.connection_worker.take()
        {
            self.apply_event(worker.join()?)?;
            progressed = true;
        }
        Ok(progressed)
    }

    /// Cancel active operations, join them and record typed cancellation.
    pub fn cancel_active(&mut self) -> Result<(), RuntimeError> {
        let attempt_id = self.active_attempt.ok_or(RuntimeError::NoActiveAttempt)?;
        self.cancel_workers();
        self.join_and_recover_workers()?;
        if let Some(lifecycle) = self.lifecycle.as_mut()
            && !matches!(
                lifecycle.phase(),
                EntryPhase::Failed | EntryPhase::Closing | EntryPhase::LoggedOut
            )
        {
            lifecycle.cancel(attempt_id)?;
        }
        self.failure = Some(EntryFailure::for_kind(EntryFailureKind::SafeCancellation));
        self.entered = None;
        self.selection = None;
        self.record_phase(EntryPhase::Failed);
        Ok(())
    }

    /// Close every session-scoped value and return to `LoggedOut`.
    pub fn disconnect_to_logged_out(&mut self) -> Result<(), RuntimeError> {
        self.cancel_workers();
        self.join_and_recover_workers()?;
        self.lifecycle
            .get_or_insert_with(EntryLifecycle::new)
            .close();
        self.record_phase(EntryPhase::Closing);
        self.lifecycle_mut()?.finish_closing()?;
        self.record_phase(EntryPhase::LoggedOut);
        self.active_attempt = None;
        self.selection = None;
        self.failure = None;
        self.entered = None;
        Ok(())
    }

    /// Reject new work, cancel/join workers and clear all session state.
    pub fn shutdown(&mut self) -> Result<(), RuntimeError> {
        if self.shutting_down {
            return Ok(());
        }
        self.shutting_down = true;
        self.disconnect_to_logged_out()
    }

    fn require_startable(&self) -> Result<(), RuntimeError> {
        if self.shutting_down {
            return Err(RuntimeError::ShuttingDown);
        }
        if self.identity_worker.is_some() {
            return Err(RuntimeError::AuthenticationAlreadyActive);
        }
        if self.connection_worker.is_some() {
            return Err(RuntimeError::ConnectionAlreadyActive);
        }
        if !matches!(self.phase, EntryPhase::LoggedOut | EntryPhase::Failed) {
            return Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation).into());
        }
        Ok(())
    }

    fn allocate_attempt_id(&mut self) -> Result<GameEntryAttemptId, RuntimeError> {
        let attempt_id = GameEntryAttemptId::new(self.next_attempt)
            .map_err(|_error| RuntimeError::AttemptIdExhausted)?;
        self.next_attempt = self
            .next_attempt
            .checked_add(1)
            .ok_or(RuntimeError::AttemptIdExhausted)?;
        Ok(attempt_id)
    }

    fn apply_event(&mut self, event: WorkerEvent) -> Result<(), RuntimeError> {
        match event {
            WorkerEvent::Identity { attempt_id, result } => {
                self.require_active(attempt_id)?;
                match result {
                    Ok((account_session_id, directory, credential)) => self.apply_identity_success(
                        attempt_id,
                        account_session_id,
                        directory,
                        credential,
                    ),
                    Err(failure) => {
                        self.lifecycle_mut()?.record_failure(attempt_id, failure)?;
                        self.set_failure(failure);
                        Ok(())
                    }
                }
            }
            WorkerEvent::Connection {
                attempt_id,
                lifecycle,
                result,
            } => {
                self.require_active(attempt_id)?;
                self.lifecycle = Some(lifecycle);
                match result {
                    Ok(entered) => self.apply_entered(entered),
                    Err(failure) => self.apply_connection_failure(attempt_id, failure),
                }
            }
        }
    }

    fn apply_entered(&mut self, entered: SessionEntered) -> Result<(), RuntimeError> {
        if self
            .lifecycle
            .as_ref()
            .and_then(EntryLifecycle::entered_result)
            != Some(entered)
        {
            let failure = EntryFailure::for_kind(EntryFailureKind::InvariantViolation);
            self.set_failure(failure);
            return Err(failure.into());
        }
        self.failure = None;
        self.entered = Some(entered);
        self.record_phase(EntryPhase::SessionEntered);
        Ok(())
    }

    fn apply_connection_failure(
        &mut self,
        attempt_id: GameEntryAttemptId,
        failure: EntryFailure,
    ) -> Result<(), RuntimeError> {
        if self
            .lifecycle
            .as_ref()
            .and_then(EntryLifecycle::failure)
            .is_none()
        {
            self.lifecycle_mut()?.record_failure(attempt_id, failure)?;
        }
        self.set_failure(failure);
        Ok(())
    }

    fn apply_identity_success(
        &mut self,
        attempt_id: GameEntryAttemptId,
        account_session_id: AccountSessionId,
        directory: AccountDirectorySnapshot,
        credential: GameEntryCredential,
    ) -> Result<(), RuntimeError> {
        self.lifecycle_mut()?
            .account_ready(attempt_id, account_session_id)?;
        self.sync_phase();
        let selection = self.selection.ok_or(RuntimeError::NoActiveAttempt)?;
        let selected_entry = match directory.select(
            directory.revision(),
            selection.character_id(),
            selection.world_id(),
            selection.gameplay_channel_id(),
        ) {
            Ok(value) => value,
            Err(error) => {
                let failure = EntryFailure::from(error);
                self.lifecycle_mut()?.record_failure(attempt_id, failure)?;
                self.set_failure(failure);
                return Ok(());
            }
        };
        self.lifecycle_mut()?
            .directory_ready(attempt_id, directory)?;
        self.sync_phase();
        let requested_at = self.clock.now();
        self.lifecycle_mut()?.request_entry(GameEntryRequest::new(
            attempt_id,
            selected_entry,
            EntryProfile::CanaryCurrent,
            requested_at,
        ))?;
        self.sync_phase();
        let clock = Arc::clone(&self.clock);
        if let Err(failure) =
            self.lifecycle_mut()?
                .credential_ready(attempt_id, credential, clock.as_ref())
        {
            self.lifecycle_mut()?.record_failure(attempt_id, failure)?;
            self.set_failure(failure);
            return Ok(());
        }
        self.sync_phase();
        Ok(())
    }

    fn require_active(&self, attempt_id: GameEntryAttemptId) -> Result<(), RuntimeError> {
        if self.active_attempt == Some(attempt_id) {
            Ok(())
        } else {
            Err(EntryFailure::for_kind(EntryFailureKind::StaleAuthenticationTransaction).into())
        }
    }

    fn lifecycle_mut(&mut self) -> Result<&mut EntryLifecycle, RuntimeError> {
        self.lifecycle.as_mut().ok_or(RuntimeError::NoActiveAttempt)
    }

    fn sync_phase(&mut self) {
        let phase = self.lifecycle.as_ref().map(EntryLifecycle::phase);
        if let Some(phase) = phase {
            self.record_phase(phase);
        }
    }

    fn set_failure(&mut self, failure: EntryFailure) {
        self.failure = Some(failure);
        self.entered = None;
        self.selection = None;
        self.record_phase(EntryPhase::Failed);
    }

    fn cancel_workers(&self) {
        if let Some(worker) = self.identity_worker.as_ref() {
            worker.cancel();
        }
        if let Some(worker) = self.connection_worker.as_ref() {
            worker.cancel();
        }
    }

    fn join_and_recover_workers(&mut self) -> Result<(), RuntimeError> {
        if let Some(worker) = self.identity_worker.take() {
            let kind = worker.kind;
            if worker.join().is_err() {
                self.lifecycle = Some(EntryLifecycle::new());
                return Err(RuntimeError::WorkerJoin(kind));
            }
        }
        if let Some(worker) = self.connection_worker.take() {
            let kind = worker.kind;
            match worker.join() {
                Ok(WorkerEvent::Connection { lifecycle, .. }) => {
                    self.lifecycle = Some(lifecycle);
                }
                Ok(WorkerEvent::Identity { .. }) | Err(_) => {
                    self.lifecycle = Some(EntryLifecycle::new());
                    return Err(RuntimeError::WorkerJoin(kind));
                }
            }
        }
        Ok(())
    }

    fn record_phase(&mut self, phase: EntryPhase) {
        self.phase = phase;
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
            .field(
                "connection_worker_active",
                &self.connection_worker.is_some(),
            )
            .field("history_len", &self.history.len())
            .finish()
    }
}

impl Drop for TechnicalLoginRuntime {
    fn drop(&mut self) {
        self.cancel_workers();
        let _joined = self.join_and_recover_workers();
        if let Some(lifecycle) = self.lifecycle.as_mut() {
            lifecycle.close();
            let _closed = lifecycle.finish_closing();
        }
    }
}
