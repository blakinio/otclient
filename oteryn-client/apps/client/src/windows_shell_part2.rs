impl ShellApplication {
    fn new(proxy: EventLoopProxy<ShellUserEvent>) -> Result<Self, RuntimeError> {
        let clock = SystemClock::new();
        let state = ShellState::new(PROCESS_GENERATION, clock.now())?;
        let technical_login = TechnicalLoginController::from_environment()?;
        Ok(Self {
            clock,
            state,
            renderer: None,
            window: None,
            technical_login,
            technical_login_started: false,
            proxy,
            failure: None,
            exit_requested: false,
            shutdown_overdue_reported: false,
        })
    }

    fn remember_failure(&mut self, failure: RuntimeError) {
        if self.failure.is_none() {
            self.failure = Some(failure);
        }
    }

    fn fail_and_exit(&mut self, event_loop: &ActiveEventLoop, failure: RuntimeError) {
        self.remember_failure(failure);
        self.request_exit(event_loop);
    }

    fn poll_technical_shutdown(&mut self) -> Result<ShutdownProgress, TechnicalLoginError> {
        match self.technical_login.as_mut() {
            Some(controller) if controller.is_shutting_down() => controller.poll_shutdown(),
            Some(controller) => controller.begin_shutdown(),
            None => Ok(ShutdownProgress::Complete),
        }
    }

    fn release_renderer_and_window(&mut self) {
        let renderer_close = self
            .renderer
            .as_mut()
            .map(|renderer| renderer.close(PROCESS_GENERATION));
        if let Some(Err(error)) = renderer_close {
            self.remember_failure(RuntimeError::Renderer(error));
        }
        self.renderer = None;
        self.window = None;
    }

    fn finish_exit(&mut self, event_loop: &ActiveEventLoop) {
        self.release_renderer_and_window();
        if !matches!(self.state.phase(), ShellPhase::Closing | ShellPhase::Exited)
            && let Err(error) = self
                .state
                .request_close(PROCESS_GENERATION, self.clock.now())
        {
            self.remember_failure(RuntimeError::Shell(error));
        }
        event_loop.exit();
    }

    fn progress_exit(&mut self, event_loop: &ActiveEventLoop) -> bool {
        match self.poll_technical_shutdown() {
            Ok(ShutdownProgress::Complete) => {
                self.finish_exit(event_loop);
                false
            }
            Ok(ShutdownProgress::Pending(_kind)) => true,
            Ok(ShutdownProgress::Overdue(kind)) => {
                if !self.shutdown_overdue_reported {
                    self.shutdown_overdue_reported = true;
                    self.remember_failure(RuntimeError::TechnicalLogin(
                        TechnicalLoginError::Runtime(TechnicalRuntimeError::ShutdownOverdue(
                            kind,
                        )),
                    ));
                }
                true
            }
            Err(error) => {
                let has_active_worker = self
                    .technical_login
                    .as_ref()
                    .is_some_and(TechnicalLoginController::retains_worker);
                self.remember_failure(RuntimeError::TechnicalLogin(error));
                if has_active_worker {
                    true
                } else {
                    self.finish_exit(event_loop);
                    false
                }
            }
        }
    }

    fn request_exit(&mut self, event_loop: &ActiveEventLoop) {
        if !self.exit_requested {
            self.exit_requested = true;
            if !matches!(self.state.phase(), ShellPhase::Closing | ShellPhase::Exited)
                && let Err(error) = self
                    .state
                    .request_close(PROCESS_GENERATION, self.clock.now())
            {
                self.remember_failure(RuntimeError::Shell(error));
            }
        }
        if self.progress_exit(event_loop) {
            event_loop.set_control_flow(ControlFlow::WaitUntil(
                Instant::now() + ACTIVE_POLL_INTERVAL,
            ));
        }
    }

    fn handle_state_result(
        &mut self,
        event_loop: &ActiveEventLoop,
        result: Result<(), ShellError>,
    ) {
        if let Err(error) = result {
            self.fail_and_exit(event_loop, RuntimeError::Shell(error));
        }
    }

    fn handle_renderer_result(
        &mut self,
        event_loop: &ActiveEventLoop,
        result: Result<(), RendererError>,
    ) -> bool {
        if let Err(error) = result {
            self.fail_and_exit(event_loop, RuntimeError::Renderer(error));
            false
        } else {
            true
        }
    }

    fn handle_resize(&mut self, event_loop: &ActiveEventLoop, width: u32, height: u32) {
        self.state.resize(width, height);
        let renderer_result = self
            .renderer
            .as_mut()
            .map(|renderer| renderer.resize(PROCESS_GENERATION, width, height));
        if let Some(result) = renderer_result
            && !self.handle_renderer_result(event_loop, result)
        {
            return;
        }
        if width != 0
            && height != 0
            && let Some(window) = self.window.as_ref()
        {
            window.request_redraw();
        }
    }

    fn handle_redraw(&mut self, event_loop: &ActiveEventLoop) {
        let render_result = self
            .renderer
            .as_mut()
            .map(|renderer| renderer.render(PROCESS_GENERATION));
        if let Some(result) = render_result {
            self.handle_renderer_result(event_loop, result);
        }
    }

    fn handle_window_event(&mut self, event_loop: &ActiveEventLoop, event: WindowEvent) {
        if self.exit_requested {
            if matches!(&event, WindowEvent::CloseRequested | WindowEvent::Destroyed) {
                self.request_exit(event_loop);
            }
            return;
        }
        match event {
            WindowEvent::CloseRequested | WindowEvent::Destroyed => {
                self.request_exit(event_loop);
            }
            WindowEvent::Resized(size) => {
                self.handle_resize(event_loop, size.width, size.height);
            }
            WindowEvent::Focused(focused) => self.state.set_focused(focused),
            WindowEvent::ModifiersChanged(modifiers) => {
                self.state
                    .set_modifiers_active(!modifiers.state().is_empty());
            }
            WindowEvent::Ime(event) => match event {
                Ime::Enabled | Ime::Commit(_) | Ime::Preedit(_, _) => {
                    self.state.set_ime_active(true);
                }
                Ime::Disabled => self.state.set_ime_active(false),
            },
            WindowEvent::ScaleFactorChanged { scale_factor, .. } => {
                let result = scale_factor_milli(scale_factor)
                    .ok_or(ShellError::InvalidScaleFactor)
                    .and_then(|factor| self.state.set_scale_factor_milli(factor));
                self.handle_state_result(event_loop, result);
            }
            WindowEvent::RedrawRequested => self.handle_redraw(event_loop),
            WindowEvent::KeyboardInput { .. }
            | WindowEvent::MouseInput { .. }
            | WindowEvent::MouseWheel { .. }
            | WindowEvent::CursorMoved { .. }
            | WindowEvent::CursorEntered { .. }
            | WindowEvent::CursorLeft { .. } => {}
            _ => {}
        }
    }

    fn start_technical_login(&mut self, event_loop: &ActiveEventLoop) {
        if self.exit_requested || self.technical_login_started || self.technical_login.is_none() {
            return;
        }
        let proxy = self.proxy.clone();
        let result = self.technical_login.as_mut().map(|controller| {
            controller.start(move |signal| {
                let _send_result = proxy.send_event(ShellUserEvent::TechnicalLogin {
                    generation: PROCESS_GENERATION,
                    signal,
                });
            })
        });
        match result {
            Some(Ok(())) => {
                self.technical_login_started = true;
                self.update_technical_title();
            }
            Some(Err(error)) => {
                self.fail_and_exit(event_loop, RuntimeError::TechnicalLogin(error));
            }
            None => {}
        }
    }

    fn handle_technical_signal(
        &mut self,
        event_loop: &ActiveEventLoop,
        generation: ProcessGeneration,
        signal: TechnicalWorkerSignal,
    ) {
        if generation != PROCESS_GENERATION {
            return;
        }
        let result = self
            .technical_login
            .as_mut()
            .map(|controller| controller.handle_signal(signal));
        if let Some(Err(error)) = result {
            self.fail_and_exit(event_loop, RuntimeError::TechnicalLogin(error));
            return;
        }
        if self.exit_requested {
            let _pending = self.progress_exit(event_loop);
        } else {
            self.update_technical_title();
        }
    }

    fn poll_technical_login(&mut self, event_loop: &ActiveEventLoop) -> bool {
        let result = self
            .technical_login
            .as_mut()
            .map(TechnicalLoginController::poll);
        if let Some(Err(error)) = result {
            self.fail_and_exit(event_loop, RuntimeError::TechnicalLogin(error));
            return false;
        }
        self.update_technical_title();
        self.technical_login
            .as_ref()
            .is_some_and(TechnicalLoginController::retains_worker)
    }

    fn update_technical_title(&self) {
        let title = self
            .technical_login
            .as_ref()
            .map(TechnicalLoginController::window_title);
        if let (Some(title), Some(window)) = (title, self.window.as_ref()) {
            window.set_title(title);
        }
    }
}
