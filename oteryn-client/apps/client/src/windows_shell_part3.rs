impl ApplicationHandler<ShellUserEvent> for ShellApplication {
    fn resumed(&mut self, event_loop: &ActiveEventLoop) {
        if self.exit_requested {
            return;
        }
        if let Some(window) = self.window.clone() {
            let size = window.inner_size();
            let result = self
                .renderer
                .as_mut()
                .map(|renderer| renderer.resume(PROCESS_GENERATION, size.width, size.height));
            if result.is_none_or(|result| self.handle_renderer_result(event_loop, result)) {
                window.request_redraw();
                self.start_technical_login(event_loop);
            }
            return;
        }

        if self.state.phase() != ShellPhase::Starting {
            return;
        }

        let attributes = Window::default_attributes()
            .with_title("Oteryn")
            .with_resizable(true)
            .with_inner_size(LogicalSize::new(960.0, 540.0));
        let window = match event_loop.create_window(attributes) {
            Ok(window) => Arc::new(window),
            Err(_error) => {
                self.fail_and_exit(event_loop, RuntimeError::WindowCreation);
                return;
            }
        };
        window.set_ime_allowed(true);
        let size = window.inner_size();
        self.state.resize(size.width, size.height);
        let renderer = match WindowsRenderer::new(
            Arc::clone(&window),
            PROCESS_GENERATION,
            size.width,
            size.height,
        ) {
            Ok(renderer) => renderer,
            Err(error) => {
                self.fail_and_exit(event_loop, RuntimeError::Renderer(error));
                return;
            }
        };
        if let Err(error) = self.state.mark_running(self.clock.now()) {
            self.fail_and_exit(event_loop, RuntimeError::Shell(error));
            return;
        }
        self.renderer = Some(renderer);
        self.window = Some(Arc::clone(&window));
        self.start_technical_login(event_loop);
        window.request_redraw();
    }

    fn user_event(&mut self, event_loop: &ActiveEventLoop, event: ShellUserEvent) {
        match event {
            ShellUserEvent::Wake { generation } => {
                if self.exit_requested {
                    let _pending = self.progress_exit(event_loop);
                    return;
                }
                let result = self
                    .state
                    .apply_commands(&[ShellCommand::Wake { generation }], self.clock.now());
                self.handle_state_result(event_loop, result);
            }
            ShellUserEvent::TechnicalLogin { generation, signal } => {
                self.handle_technical_signal(event_loop, generation, signal);
            }
        }
    }

    fn window_event(
        &mut self,
        event_loop: &ActiveEventLoop,
        window_id: WindowId,
        event: WindowEvent,
    ) {
        let belongs_to_shell = self
            .window
            .as_ref()
            .is_some_and(|window| window.id() == window_id);
        if belongs_to_shell {
            self.handle_window_event(event_loop, event);
        }
    }

    fn about_to_wait(&mut self, event_loop: &ActiveEventLoop) {
        if self.exit_requested {
            if self.progress_exit(event_loop) {
                event_loop.set_control_flow(ControlFlow::WaitUntil(
                    Instant::now() + ACTIVE_POLL_INTERVAL,
                ));
            }
            return;
        }
        if self.poll_technical_login(event_loop) {
            event_loop.set_control_flow(ControlFlow::WaitUntil(
                Instant::now() + ACTIVE_POLL_INTERVAL,
            ));
        } else {
            event_loop.set_control_flow(ControlFlow::Wait);
        }
    }

    fn suspended(&mut self, event_loop: &ActiveEventLoop) {
        if self.exit_requested {
            return;
        }
        self.state.set_focused(false);
        let result = self
            .renderer
            .as_mut()
            .map(|renderer| renderer.suspend(PROCESS_GENERATION));
        if let Some(result) = result {
            self.handle_renderer_result(event_loop, result);
        }
    }

    fn exiting(&mut self, _event_loop: &ActiveEventLoop) {
        self.release_renderer_and_window();
        if !matches!(self.state.phase(), ShellPhase::Closing | ShellPhase::Exited) {
            let close_result = self
                .state
                .request_close(PROCESS_GENERATION, self.clock.now());
            if let Err(error) = close_result {
                self.remember_failure(RuntimeError::Shell(error));
            }
        }
        if self.state.phase() == ShellPhase::Closing {
            let exit_result = self.state.mark_exited(self.clock.now());
            if let Err(error) = exit_result {
                self.remember_failure(RuntimeError::Shell(error));
            }
        }
    }
}
