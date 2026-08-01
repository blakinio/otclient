use super::technical_login::{
    TechnicalLoginController, TechnicalLoginError, TechnicalWorkerSignal,
};
use oteryn_app_runtime::{RuntimeError as TechnicalRuntimeError, ShutdownProgress};
use oteryn_client::{ShellCommand, ShellError, ShellPhase, ShellState};
use oteryn_foundation::{MonotonicClock, ProcessGeneration, SystemClock};
use oteryn_renderer::{RendererError, WindowsRenderer};
use std::fmt::{self, Display, Formatter};
use std::process::ExitCode;
use std::sync::Arc;
use std::thread::{self, JoinHandle};
use std::time::{Duration, Instant};
use winit::application::ApplicationHandler;
use winit::dpi::LogicalSize;
use winit::event::{Ime, WindowEvent};
use winit::event_loop::{ActiveEventLoop, ControlFlow, EventLoop, EventLoopProxy};
use winit::window::{Window, WindowId};

const PROCESS_GENERATION: ProcessGeneration = ProcessGeneration::new(1);
const ACTIVE_POLL_INTERVAL: Duration = Duration::from_millis(16);

#[derive(Debug, Clone, Copy)]
enum ShellUserEvent {
    Wake {
        generation: ProcessGeneration,
    },
    TechnicalLogin {
        generation: ProcessGeneration,
        signal: TechnicalWorkerSignal,
    },
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
    TechnicalLogin(TechnicalLoginError),
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
            Self::TechnicalLogin(error) => Display::fmt(error, formatter),
        }
    }
}

impl std::error::Error for RuntimeError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::Shell(error) => Some(error),
            Self::Renderer(error) => Some(error),
            Self::TechnicalLogin(error) => Some(error),
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

impl From<TechnicalLoginError> for RuntimeError {
    fn from(error: TechnicalLoginError) -> Self {
        Self::TechnicalLogin(error)
    }
}

struct ShellApplication {
    clock: SystemClock,
    state: ShellState,
    renderer: Option<WindowsRenderer<Arc<Window>>>,
    window: Option<Arc<Window>>,
    technical_login: Option<TechnicalLoginController>,
    technical_login_started: bool,
    proxy: EventLoopProxy<ShellUserEvent>,
    failure: Option<RuntimeError>,
    exit_requested: bool,
    shutdown_overdue_reported: bool,
}
