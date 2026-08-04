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
            tokio_runtime: None,
            history,
            shutdown_started: None,
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
            shutting_down: self.shutdown_started.is_some(),
        }
    }

    /// Iterate bounded phases in deterministic order.
    pub fn history(&self) -> impl ExactSizeIterator<Item = EntryPhase> + '_ {
        self.history.iter().copied()
    }

    /// Return whether either application-owned worker is retained.
    #[must_use]
    pub const fn has_active_worker(&self) -> bool {
        self.identity_worker.is_some() || self.connection_worker.is_some()
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

    /// Move the complete producer-owned lifecycle into one Tokio admission task.
    ///
    /// The application owns the runtime. The future may create transport
    /// sessions and child tasks, while the event loop only polls completion.
    /// Application code never receives `AdmissionCredential`.
    pub fn start_connection<F, Fut>(&mut self, operation: F) -> Result<(), RuntimeError>
    where
        F: FnOnce(
                EntryLifecycle,
                GameEntryAttemptId,
                CancellationToken,
                Arc<dyn MonotonicClock>,
            ) -> Fut
            + Send
            + 'static,
        Fut: Future<Output = (EntryLifecycle, Result<SessionEntered, EntryFailure>)>
            + Send
            + 'static,
    {
        if self.shutdown_started.is_some() {
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

        self.ensure_tokio_runtime()?;
        let attempt_id = self.active_attempt.ok_or(RuntimeError::NoActiveAttempt)?;
        let lifecycle = self.lifecycle.take().ok_or(RuntimeError::NoActiveAttempt)?;
        let cancellation = CancellationSource::new();
        let token = cancellation.token();
        let clock = Arc::clone(&self.clock);
        let (event_tx, event_rx) = sync_channel(1);
        let handle = {
            let runtime = self
                .tokio_runtime
                .as_ref()
                .ok_or(RuntimeError::RuntimeUnavailable)?;
            runtime.spawn(async move {
                let (lifecycle, result) = operation(lifecycle, attempt_id, token, clock).await;
                drop(event_tx.send(WorkerEvent::Connection {
                    attempt_id,
                    lifecycle,
                    result,
                }));
            })
        };
        self.connection_worker = Some(OwnedTokioWorker {
            kind: WorkerKind::Connection,
            cancellation,
            handle,
            event_rx,
        });
        self.record_phase(EntryPhase::Connecting);
        Ok(())
    }

    fn ensure_tokio_runtime(&mut self) -> Result<(), RuntimeError> {
        if self.tokio_runtime.is_some() {
            return Ok(());
        }
        let runtime = TokioRuntimeBuilder::new_multi_thread()
            .worker_threads(TOKIO_RUNTIME_WORKER_THREADS)
            .thread_name("oteryn-network")
            .enable_io()
            .enable_time()
            .build()
            .map_err(|_error| RuntimeError::RuntimeUnavailable)?;
        self.tokio_runtime = Some(runtime);
        Ok(())
    }
}
