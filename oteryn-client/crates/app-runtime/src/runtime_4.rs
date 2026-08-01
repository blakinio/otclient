impl TechnicalLoginRuntime {
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
}
