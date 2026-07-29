#[cfg(windows)]
mod windows_shell {
    use oteryn_client::{ShellCommand, ShellError, ShellPhase, ShellState};
    use oteryn_foundation::{MonotonicClock, ProcessGeneration, SystemClock};
    use oteryn_renderer::{RendererError, WindowsRenderer};
    use std::fmt::{self, Display, Formatter};
    use std::process::ExitCode;
    use std::sync::Arc;
    use std::thread::{self, JoinHandle};
    use winit::application::ApplicationHandler;
    use winit::dpi::LogicalSize;
    use winit::event::{Ime, WindowEvent};
    use winit::event_loop::{ActiveEventLoop, ControlFlow, EventLoop};
    use winit::window::{Window, WindowId};

    const PROCESS_GENERATION: ProcessGeneration = ProcessGeneration::new(1);

    #[derive(Debug, Clone, Copy)]
    enum ShellUserEvent {
        Wake { generation: ProcessGeneration },
    }

    #[derive(Debug, Clone, Copy, PartialEq, Eq)]
    enum RuntimeError {
        EventLoopCreation,
        WindowCreation,
        EventLoopRun,
        WorkerSpawn,
        WorkerJoin,
        Shell(ShellError),
        Renderer(RendererError),
    }

    impl Display for RuntimeError {
        fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
            match self {
                Self::EventLoopCreation => {
                    formatter.write_str("Windows event loop could not be created")
                }
                Self::WindowCreation => {
                    formatter.write_str("Windows shell window could not be created")
                }
                Self::EventLoopRun => {
                    formatter.write_str("Windows event loop terminated with an error")
                }
                Self::WorkerSpawn => formatter.write_str("shell wake worker could not be started"),
                Self::WorkerJoin => formatter.write_str("shell wake worker did not finish cleanly"),
                Self::Shell(error) => Display::fmt(error, formatter),
                Self::Renderer(error) => Display::fmt(error, formatter),
            }
        }
    }

    impl std::error::Error for RuntimeError {
        fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
            match self {
                Self::Shell(error) => Some(error),
                Self::Renderer(error) => Some(error),
                Self::EventLoopCreation
                | Self::WindowCreation
                | Self::EventLoopRun
                | Self::WorkerSpawn
                | Self::WorkerJoin => None,
            }
        }
    }

    impl From<ShellError> for RuntimeError {
        fn from(error: ShellError) -> Self {
            Self::Shell(error)
        }
    }

    impl From<RendererError> for RuntimeError {
        fn from(error: RendererError) -> Self {
            Self::Renderer(error)
        }
    }

    struct ShellApplication {
        clock: SystemClock,
        state: ShellState,
        renderer: Option<WindowsRenderer<Arc<Window>>>,
        window: Option<Arc<Window>>,
        failure: Option<RuntimeError>,
    }

    impl ShellApplication {
        fn new() -> Result<Self, RuntimeError> {
            let clock = SystemClock::new();
            let state = ShellState::new(PROCESS_GENERATION, clock.now())?;
            Ok(Self {
                clock,
                state,
                renderer: None,
                window: None,
                failure: None,
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

        fn request_exit(&mut self, event_loop: &ActiveEventLoop) {
            self.release_renderer_and_window();
            if let Err(error) = self
                .state
                .request_close(PROCESS_GENERATION, self.clock.now())
            {
                self.remember_failure(RuntimeError::Shell(error));
            }
            event_loop.exit();
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
                | WindowEvent::CursorLeft => {}
                _ => {}
            }
        }
    }

    impl ApplicationHandler<ShellUserEvent> for ShellApplication {
        fn resumed(&mut self, event_loop: &ActiveEventLoop) {
            if let Some(window) = self.window.clone() {
                let size = window.inner_size();
                let result = self
                    .renderer
                    .as_mut()
                    .map(|renderer| renderer.resume(PROCESS_GENERATION, size.width, size.height));
                if result.is_none_or(|result| self.handle_renderer_result(event_loop, result)) {
                    window.request_redraw();
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
            window.request_redraw();
        }

        fn user_event(&mut self, event_loop: &ActiveEventLoop, event: ShellUserEvent) {
            let command = match event {
                ShellUserEvent::Wake { generation } => ShellCommand::Wake { generation },
            };
            let result = self.state.apply_commands(&[command], self.clock.now());
            self.handle_state_result(event_loop, result);
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

        fn suspended(&mut self, event_loop: &ActiveEventLoop) {
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

    fn scale_factor_milli(scale_factor: f64) -> Option<u32> {
        if !scale_factor.is_finite() || scale_factor <= 0.0 {
            return None;
        }
        let scaled = (scale_factor * 1_000.0).round();
        if scaled >= f64::from(u32::MAX) {
            Some(u32::MAX)
        } else if scaled < 1.0 {
            Some(1)
        } else {
            Some(scaled as u32)
        }
    }

    fn spawn_wake_worker(
        proxy: winit::event_loop::EventLoopProxy<ShellUserEvent>,
    ) -> Result<JoinHandle<()>, RuntimeError> {
        thread::Builder::new()
            .name(String::from("oteryn-shell-wake"))
            .spawn(move || {
                let _send_result = proxy.send_event(ShellUserEvent::Wake {
                    generation: PROCESS_GENERATION,
                });
            })
            .map_err(|_error| RuntimeError::WorkerSpawn)
    }

    fn run() -> Result<(), RuntimeError> {
        let event_loop = EventLoop::<ShellUserEvent>::with_user_event()
            .build()
            .map_err(|_error| RuntimeError::EventLoopCreation)?;
        event_loop.set_control_flow(ControlFlow::Wait);
        let wake_worker = spawn_wake_worker(event_loop.create_proxy())?;
        let mut application = ShellApplication::new()?;

        let run_result = event_loop
            .run_app(&mut application)
            .map_err(|_error| RuntimeError::EventLoopRun);
        let join_result = wake_worker
            .join()
            .map_err(|_panic_payload| RuntimeError::WorkerJoin);

        run_result?;
        join_result?;
        if let Some(failure) = application.failure {
            return Err(failure);
        }
        Ok(())
    }

    pub fn main() -> ExitCode {
        match run() {
            Ok(()) => ExitCode::SUCCESS,
            Err(error) => {
                eprintln!("{error}");
                ExitCode::FAILURE
            }
        }
    }
}

#[cfg(windows)]
fn main() -> std::process::ExitCode {
    windows_shell::main()
}

#[cfg(not(windows))]
fn main() {
    eprintln!("the Oteryn renderer surface spike is validated only on Windows");
}
