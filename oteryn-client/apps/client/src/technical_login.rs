include!("technical_login_base.rs");

use oteryn_app_runtime::ShutdownProgress;

impl TechnicalLoginController {
    pub(crate) fn begin_shutdown(&mut self) -> Result<ShutdownProgress, TechnicalLoginError> {
        Ok(self.runtime.begin_shutdown()?)
    }

    pub(crate) fn poll_shutdown(&mut self) -> Result<ShutdownProgress, TechnicalLoginError> {
        let progress = self.runtime.poll_shutdown()?;
        if progress == ShutdownProgress::Complete {
            self.shutdown()?;
        }
        Ok(progress)
    }

    pub(crate) fn is_shutting_down(&self) -> bool {
        self.runtime.snapshot().shutting_down()
    }
}
