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
            .field("tokio_runtime_active", &self.tokio_runtime.is_some())
            .field("history_len", &self.history.len())
            .finish()
    }
}

impl Drop for TechnicalLoginRuntime {
    fn drop(&mut self) {
        self.cancel_workers();
        if let Some(worker) = self.connection_worker.take()
            && let Some(runtime) = self.tokio_runtime.as_ref()
        {
            worker.abort_and_join(runtime);
        }
        let _joined = self.join_and_recover_workers();
        if let Some(lifecycle) = self.lifecycle.as_mut() {
            lifecycle.close();
            let _closed = lifecycle.finish_closing();
        }
        self.shutdown_tokio_runtime();
    }
}
