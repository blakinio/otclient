include!("technical_login_base.rs");

use oteryn_app_runtime::ShutdownProgress;

impl TechnicalLoginController {
    pub(crate) fn begin_shutdown(&mut self) -> Result<ShutdownProgress, TechnicalLoginError> {
        Ok(self.runtime.begin_shutdown()?)
    }

    pub(crate) fn poll_shutdown(&mut self) -> Result<ShutdownProgress, TechnicalLoginError> {
        Ok(self.runtime.poll_shutdown()?)
    }

    pub(crate) fn retains_worker(&self) -> bool {
        self.runtime.has_active_worker()
    }

    pub(crate) fn is_shutting_down(&self) -> bool {
        self.runtime.snapshot().shutting_down()
    }
}
