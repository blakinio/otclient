impl TechnicalLoginRuntime {
    /// Join and apply every currently completed worker.
    pub fn poll(&mut self) -> Result<bool, RuntimeError> {
        if self.shutdown_started.is_some() {
            return Ok(false);
        }
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
            .is_some_and(OwnedTokioWorker::is_finished)
            && let Some(worker) = self.connection_worker.take()
        {
            let event = worker.join(
                self.tokio_runtime
                    .as_ref()
                    .ok_or(RuntimeError::RuntimeUnavailable)?,
            )?;
            self.apply_event(event)?;
            progressed = true;
        }
        Ok(progressed)
    }

    /// Cancel active operations without joining an unfinished worker.
    pub fn cancel_active(&mut self) -> Result<(), RuntimeError> {
        let attempt_id = self.active_attempt.ok_or(RuntimeError::NoActiveAttempt)?;
        self.cancel_workers();
        if let Some(kind) = self.unfinished_worker_kind() {
            return Err(RuntimeError::ShutdownPending(kind));
        }
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

    /// Close every session-scoped value without joining an unfinished worker.
    pub fn disconnect_to_logged_out(&mut self) -> Result<(), RuntimeError> {
        self.cancel_workers();
        if let Some(kind) = self.unfinished_worker_kind() {
            return Err(RuntimeError::ShutdownPending(kind));
        }
        self.join_and_recover_workers()?;
        self.finish_closing()
    }

    /// Begin deterministic shutdown and poll once without blocking.
    pub fn begin_shutdown(&mut self) -> Result<ShutdownProgress, RuntimeError> {
        if self.shutdown_started.is_none() {
            self.shutdown_started = Some(self.clock.now());
            self.cancel_workers();
            if let Some(lifecycle) = self.lifecycle.as_mut() {
                lifecycle.close();
            }
            self.record_phase(EntryPhase::Closing);
        }
        self.poll_shutdown()
    }

    /// Poll deterministic shutdown without joining an unfinished worker.
    pub fn poll_shutdown(&mut self) -> Result<ShutdownProgress, RuntimeError> {
        let started = self
            .shutdown_started
            .ok_or(RuntimeError::ShutdownNotStarted)?;
        self.cancel_workers();
        self.join_finished_workers_for_shutdown()?;
        if let Some(kind) = self.unfinished_worker_kind() {
            let elapsed = self.clock.now().elapsed().saturating_sub(started.elapsed());
            if elapsed >= SHUTDOWN_OVERDUE_AFTER {
                return Ok(ShutdownProgress::Overdue(kind));
            }
            return Ok(ShutdownProgress::Pending(kind));
        }
        self.finish_closing()?;
        self.shutdown_tokio_runtime();
        Ok(ShutdownProgress::Complete)
    }

    /// Compatibility wrapper that never joins an unfinished worker.
    pub fn shutdown(&mut self) -> Result<(), RuntimeError> {
        match self.begin_shutdown()? {
            ShutdownProgress::Complete => Ok(()),
            ShutdownProgress::Pending(kind) => Err(RuntimeError::ShutdownPending(kind)),
            ShutdownProgress::Overdue(kind) => Err(RuntimeError::ShutdownOverdue(kind)),
        }
    }

    fn require_startable(&self) -> Result<(), RuntimeError> {
        if self.shutdown_started.is_some() {
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
}
