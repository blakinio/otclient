impl TechnicalLoginRuntime {
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

    fn unfinished_worker_kind(&self) -> Option<WorkerKind> {
        self.identity_worker
            .as_ref()
            .filter(|worker| !worker.is_finished())
            .map(|worker| worker.kind)
            .or_else(|| {
                self.connection_worker
                    .as_ref()
                    .filter(|worker| !worker.is_finished())
                    .map(|worker| worker.kind)
            })
    }

    fn join_finished_workers_for_shutdown(&mut self) -> Result<(), RuntimeError> {
        if self
            .identity_worker
            .as_ref()
            .is_some_and(OwnedWorker::is_finished)
            && let Some(worker) = self.identity_worker.take()
            && let Err(error) = worker.join()
        {
            self.lifecycle = Some(EntryLifecycle::new());
            return Err(error);
        }
        if self
            .connection_worker
            .as_ref()
            .is_some_and(OwnedWorker::is_finished)
            && let Some(worker) = self.connection_worker.take()
        {
            let kind = worker.kind;
            match worker.join() {
                Ok(WorkerEvent::Connection { lifecycle, .. }) => {
                    self.lifecycle = Some(lifecycle);
                }
                Ok(WorkerEvent::Identity { .. }) => {
                    self.lifecycle = Some(EntryLifecycle::new());
                    return Err(RuntimeError::WorkerJoin(kind));
                }
                Err(error) => {
                    self.lifecycle = Some(EntryLifecycle::new());
                    return Err(error);
                }
            }
        }
        Ok(())
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

    fn finish_closing(&mut self) -> Result<(), RuntimeError> {
        let lifecycle = self.lifecycle.get_or_insert_with(EntryLifecycle::new);
        lifecycle.close();
        self.record_phase(EntryPhase::Closing);
        self.lifecycle_mut()?.finish_closing()?;
        self.record_phase(EntryPhase::LoggedOut);
        self.active_attempt = None;
        self.selection = None;
        self.failure = None;
        self.entered = None;
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
