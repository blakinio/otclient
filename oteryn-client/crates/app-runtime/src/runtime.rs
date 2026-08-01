use crate::model::{
    RuntimeError, RuntimeSnapshot, ShutdownProgress, TechnicalSelection, WorkerKind,
};
use crate::worker::{IdentityOutput, OwnedWorker, WorkerEvent};
use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{CancellationSource, CancellationToken, Moment, MonotonicClock};
use oteryn_game_session::{
    EntryFailure, EntryFailureKind, EntryLifecycle, EntryPhase, GameEntryAttemptId,
    GameEntryRequest, SessionEntered,
};
use oteryn_world_directory::AccountDirectorySnapshot;
use std::collections::VecDeque;
use std::fmt::{self, Debug, Formatter};
use std::num::NonZeroU64;
use std::sync::Arc;
use std::thread;
use std::time::Duration;

/// Maximum retained public phase-history entries.
pub const MAX_RUNTIME_HISTORY: usize = 32;
/// Bound after which shutdown reports an overdue worker while retaining ownership.
pub const SHUTDOWN_OVERDUE_AFTER: Duration = Duration::from_secs(31);

/// Deterministic application-owned W7 technical-login runtime.
pub struct TechnicalLoginRuntime {
    clock: Arc<dyn MonotonicClock>,
    lifecycle: Option<EntryLifecycle>,
    selection: Option<TechnicalSelection>,
    worker: Option<OwnedWorker>,
    next_attempt: u64,
    shutdown_started: Option<Moment>,
    history: VecDeque<EntryPhase>,
}

impl TechnicalLoginRuntime {
    /// Construct one runtime from an explicit monotonic clock.
    #[must_use]
    pub fn new(clock: Arc<dyn MonotonicClock>) -> Self {
        let mut history = VecDeque::with_capacity(MAX_RUNTIME_HISTORY);
        history.push_back(EntryPhase::LoggedOut);
        Self {
            clock,
            lifecycle: Some(EntryLifecycle::new()),
            selection: None,
            worker: None,
            next_attempt: 1,
            shutdown_started: None,
            history,
        }
    }

    /// Return the bounded secret-free runtime snapshot.
    #[must_use]
    pub fn snapshot(&self) -> RuntimeSnapshot {
        let lifecycle = self.lifecycle.as_ref();
        RuntimeSnapshot {
            phase: lifecycle.map_or(EntryPhase::LoggedOut, EntryLifecycle::phase),
            active_attempt: lifecycle.and_then(EntryLifecycle::active_attempt),
            failure: lifecycle.and_then(EntryLifecycle::failure),
            entered: lifecycle.and_then(EntryLifecycle::entered),
            shutting_down: self.shutdown_started.is_some(),
        }
    }

    /// Return the bounded oldest-to-newest phase history.
    #[must_use]
    pub fn phase_history(&self) -> Vec<EntryPhase> {
        self.history.iter().copied().collect()
    }

    /// Return whether an owned worker still exists.
    #[must_use]
    pub fn has_active_worker(&self) -> bool {
        self.worker.is_some()
    }

    /// Start one owned Identity worker.
    pub fn start_authentication<F>(
        &mut self,
        selection: TechnicalSelection,
        operation: F,
    ) -> Result<GameEntryAttemptId, RuntimeError>
    where
        F: FnOnce(GameEntryAttemptId, CancellationToken) -> Result<IdentityOutput, EntryFailure>
            + Send
            + 'static,
    {
        if self.shutdown_started.is_some() {
            return Err(RuntimeError::ShuttingDown);
        }
        if self.worker.is_some() {
            return Err(RuntimeError::AuthenticationAlreadyActive);
        }
        self.ensure_logged_out()?;
        let attempt_id = self.allocate_attempt()?;
        let cancellation = CancellationSource::new();
        let token = cancellation.token();
        let handle = thread::Builder::new()
            .name("oteryn-identity".to_owned())
            .spawn(move || WorkerEvent::Identity {
                attempt_id,
                result: operation(attempt_id, token),
            })
            .map_err(|_| RuntimeError::WorkerSpawn(WorkerKind::Identity))?;
        self.selection = Some(selection);
        self.lifecycle_mut()?.begin_authentication(attempt_id)?;
        self.record_phase();
        self.worker = Some(OwnedWorker {
            kind: WorkerKind::Identity,
            cancellation,
            handle,
        });
        Ok(attempt_id)
    }

    /// Start one owned Canary connection/admission worker from a credential-ready lifecycle.
    pub fn start_connection<F>(
        &mut self,
        operation: F,
    ) -> Result<GameEntryAttemptId, RuntimeError>
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
        if self.shutdown_started.is_some() {
            return Err(RuntimeError::ShuttingDown);
        }
        if self.worker.is_some() {
            return Err(RuntimeError::ConnectionAlreadyActive);
        }
        let attempt_id = self
            .lifecycle
            .as_ref()
            .and_then(EntryLifecycle::active_attempt)
            .ok_or(RuntimeError::NoActiveAttempt)?;
        let mut lifecycle = self.lifecycle.take().ok_or(RuntimeError::NoActiveAttempt)?;
        lifecycle.mark_connecting(attempt_id)?;
        self.record_external_phase(lifecycle.phase());
        let cancellation = CancellationSource::new();
        let token = cancellation.token();
        let clock = Arc::clone(&self.clock);
        let spawn = thread::Builder::new()
            .name("oteryn-canary-entry".to_owned())
            .spawn(move || {
                let (lifecycle, result) = operation(lifecycle, attempt_id, token, clock);
                WorkerEvent::Connection {
                    attempt_id,
                    lifecycle,
                    result,
                }
            });
        match spawn {
            Ok(handle) => {
                self.worker = Some(OwnedWorker {
                    kind: WorkerKind::Connection,
                    cancellation,
                    handle,
                });
                Ok(attempt_id)
            }
            Err(_) => {
                self.lifecycle = Some(EntryLifecycle::new());
                self.selection = None;
                self.record_phase();
                Err(RuntimeError::WorkerSpawn(WorkerKind::Connection))
            }
        }
    }

    /// Poll one worker completion without blocking.
    pub fn poll(&mut self) -> Result<bool, RuntimeError> {
        if self.shutdown_started.is_some() {
            return Ok(false);
        }
        let Some(worker) = self.worker.as_ref() else {
            return Ok(false);
        };
        if !worker.is_finished() {
            return Ok(false);
        }
        let event = self
            .worker
            .take()
            .ok_or(RuntimeError::NoActiveAttempt)?
            .join()?;
        self.apply_event(event)?;
        Ok(true)
    }

    /// Request cancellation without joining an unfinished worker.
    pub fn cancel_active(&mut self) -> Result<(), RuntimeError> {
        let Some(worker) = self.worker.as_ref() else {
            if let Some(lifecycle) = self.lifecycle.as_mut() {
                lifecycle.mark_failure(EntryFailure::for_kind(
                    EntryFailureKind::SafeCancellation,
                ))?;
                self.record_phase();
            }
            return Ok(());
        };
        worker.cancel();
        if worker.is_finished() {
            let event = self
                .worker
                .take()
                .ok_or(RuntimeError::NoActiveAttempt)?
                .join()?;
            self.apply_event(event)?;
        }
        Ok(())
    }

    /// Return to logged-out state without joining an unfinished worker.
    pub fn disconnect_to_logged_out(&mut self) -> Result<(), RuntimeError> {
        if let Some(worker) = self.worker.as_ref() {
            worker.cancel();
            if !worker.is_finished() {
                return Err(RuntimeError::ShutdownPending);
            }
        }
        if let Some(worker) = self.worker.take() {
            let _event = worker.join()?;
        }
        self.reset_to_logged_out()
    }

    /// Begin deterministic nonblocking shutdown and poll once.
    pub fn begin_shutdown(&mut self) -> Result<ShutdownProgress, RuntimeError> {
        if self.shutdown_started.is_none() {
            self.shutdown_started = Some(self.clock.now());
        }
        if let Some(worker) = self.worker.as_ref() {
            worker.cancel();
        }
        if let Some(lifecycle) = self.lifecycle.as_mut() {
            let _result = lifecycle.mark_closing();
            self.record_phase();
        }
        self.poll_shutdown()
    }

    /// Poll shutdown without joining an unfinished worker.
    pub fn poll_shutdown(&mut self) -> Result<ShutdownProgress, RuntimeError> {
        let started = self
            .shutdown_started
            .ok_or(RuntimeError::ShutdownNotStarted)?;
        let Some(worker) = self.worker.as_ref() else {
            self.reset_to_logged_out()?;
            return Ok(ShutdownProgress::Complete);
        };
        worker.cancel();
        let kind = worker.kind;
        let finished = worker.is_finished();
        if finished {
            let worker = self
                .worker
                .take()
                .ok_or(RuntimeError::NoActiveAttempt)?;
            let _event = worker.join()?;
            self.reset_to_logged_out()?;
            return Ok(ShutdownProgress::Complete);
        }
        let elapsed = self
            .clock
            .now()
            .checked_duration_since(started)
            .unwrap_or(Duration::MAX);
        if elapsed >= SHUTDOWN_OVERDUE_AFTER {
            Ok(ShutdownProgress::Overdue(kind))
        } else {
            Ok(ShutdownProgress::Pending(kind))
        }
    }

    /// Compatibility wrapper that never blocks on an unfinished worker.
    pub fn shutdown(&mut self) -> Result<(), RuntimeError> {
        match self.begin_shutdown()? {
            ShutdownProgress::Complete => Ok(()),
            ShutdownProgress::Pending(_) | ShutdownProgress::Overdue(_) => {
                Err(RuntimeError::ShutdownPending)
            }
        }
    }

    fn apply_event(&mut self, event: WorkerEvent) -> Result<(), RuntimeError> {
        match event {
            WorkerEvent::Identity { attempt_id, result } => {
                let active_attempt = self
                    .lifecycle
                    .as_ref()
                    .and_then(EntryLifecycle::active_attempt);
                if active_attempt != Some(attempt_id) {
                    return Ok(());
                }
                match result {
                    Ok((account_session_id, directory, credential)) => {
                        self.apply_identity_success(
                            attempt_id,
                            account_session_id,
                            directory,
                            credential,
                        )?;
                    }
                    Err(failure) => {
                        self.lifecycle_mut()?.mark_failure(failure)?;
                        self.record_phase();
                    }
                }
            }
            WorkerEvent::Connection {
                attempt_id,
                mut lifecycle,
                result,
            } => {
                if lifecycle.active_attempt() != Some(attempt_id) {
                    return Ok(());
                }
                match result {
                    Ok(entered) => lifecycle.mark_session_entered(attempt_id, entered)?,
                    Err(failure) => lifecycle.mark_failure(failure)?,
                }
                self.lifecycle = Some(lifecycle);
                self.record_phase();
            }
        }
        Ok(())
    }

    fn apply_identity_success(
        &mut self,
        attempt_id: GameEntryAttemptId,
        account_session_id: AccountSessionId,
        directory: AccountDirectorySnapshot,
        credential: oteryn_game_session::GameEntryCredential,
    ) -> Result<(), RuntimeError> {
        let selection = self.selection.ok_or(RuntimeError::NoActiveAttempt)?;
        let selected = directory.select_character(
            selection.character_id(),
            selection.world_id(),
            selection.gameplay_channel_id(),
        )?;
        let lifecycle = self.lifecycle_mut()?;
        lifecycle.mark_account_ready(attempt_id, account_session_id)?;
        lifecycle.install_directory(attempt_id, directory)?;
        lifecycle.request_entry(
            attempt_id,
            GameEntryRequest::new(account_session_id, selected),
        )?;
        lifecycle.install_credential(attempt_id, credential)?;
        self.record_phase();
        Ok(())
    }

    fn ensure_logged_out(&mut self) -> Result<(), RuntimeError> {
        if self
            .lifecycle
            .as_ref()
            .is_some_and(|lifecycle| lifecycle.phase() == EntryPhase::LoggedOut)
        {
            return Ok(());
        }
        self.reset_to_logged_out()
    }

    fn reset_to_logged_out(&mut self) -> Result<(), RuntimeError> {
        if let Some(lifecycle) = self.lifecycle.as_mut()
            && lifecycle.phase() != EntryPhase::LoggedOut
        {
            lifecycle.disconnect()?;
        }
        self.lifecycle = Some(EntryLifecycle::new());
        self.selection = None;
        self.record_phase();
        Ok(())
    }

    fn allocate_attempt(&mut self) -> Result<GameEntryAttemptId, RuntimeError> {
        let raw = NonZeroU64::new(self.next_attempt).ok_or(RuntimeError::AttemptIdExhausted)?;
        self.next_attempt = self
            .next_attempt
            .checked_add(1)
            .ok_or(RuntimeError::AttemptIdExhausted)?;
        Ok(GameEntryAttemptId::new(raw))
    }

    fn lifecycle_mut(&mut self) -> Result<&mut EntryLifecycle, RuntimeError> {
        self.lifecycle.as_mut().ok_or(RuntimeError::NoActiveAttempt)
    }

    fn record_phase(&mut self) {
        let phase = self
            .lifecycle
            .as_ref()
            .map_or(EntryPhase::LoggedOut, EntryLifecycle::phase);
        self.record_external_phase(phase);
    }

    fn record_external_phase(&mut self, phase: EntryPhase) {
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
            .field("selection", &self.selection)
            .field("worker", &self.worker.as_ref().map(|worker| worker.kind))
            .field("next_attempt", &self.next_attempt)
            .field("shutdown_started", &self.shutdown_started)
            .field("history", &self.history)
            .finish()
    }
}

impl Drop for TechnicalLoginRuntime {
    fn drop(&mut self) {
        if let Some(worker) = self.worker.take() {
            worker.cancel();
            // The Windows event-loop path retains the controller until
            // `poll_shutdown` reports `Complete`. This join is an ownership
            // invariant fallback for non-event-loop callers and prevents an
            // unfinished JoinHandle from being detached on misuse.
            let _result = worker.join();
        }
    }
}
