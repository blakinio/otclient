//! Deterministic application-shell state for the Oteryn Windows client spike.
//!
//! The state machine is independent of an interactive desktop. The binary
//! adapter owns the concrete `winit` event loop and translates reviewed event
//! classes into these closed operations.

use oteryn_diagnostics::{
    DiagnosticBuildError, DiagnosticCategory, DiagnosticCode, DiagnosticEvent, DiagnosticField,
    DiagnosticValue, FieldKey, SafeText, Severity, StaticTextError, TechnicalContext,
};
use oteryn_foundation::{Moment, ProcessGeneration};
use std::collections::VecDeque;
use std::fmt::{self, Display, Formatter};

/// Maximum number of commands accepted in one transactional batch.
pub const MAX_COMMAND_BATCH: usize = 16;
/// Maximum number of recent lifecycle diagnostics retained by the shell.
pub const MAX_SHELL_DIAGNOSTICS: usize = 32;

const CODE_CREATED: u32 = 1_001;
const CODE_RUNNING: u32 = 1_002;
const CODE_CLOSE_REQUESTED: u32 = 1_003;
const CODE_EXITED: u32 = 1_004;
const CODE_WAKE_RECEIVED: u32 = 1_005;

/// Stable application-shell lifecycle phase.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ShellPhase {
    /// State exists but no active window has completed startup.
    Starting,
    /// The application owns an active shell window.
    Running,
    /// Shutdown has been requested and new work is rejected.
    Closing,
    /// Event-loop shutdown has completed.
    Exited,
}

impl ShellPhase {
    const fn as_static_str(self) -> &'static str {
        match self {
            Self::Starting => "starting",
            Self::Running => "running",
            Self::Closing => "closing",
            Self::Exited => "exited",
        }
    }
}

impl Display for ShellPhase {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(self.as_static_str())
    }
}

/// Closed operation names used by transition failures.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ShellAction {
    /// Mark the shell window as running.
    MarkRunning,
    /// Complete event-loop shutdown.
    MarkExited,
}

impl Display for ShellAction {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::MarkRunning => "mark-running",
            Self::MarkExited => "mark-exited",
        })
    }
}

/// Deterministic window-related state retained without native handles.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct WindowSnapshot {
    width: u32,
    height: u32,
    scale_factor_milli: u32,
    focused: bool,
    minimized: bool,
    ime_active: bool,
    modifiers_active: bool,
}

impl Default for WindowSnapshot {
    fn default() -> Self {
        Self {
            width: 0,
            height: 0,
            scale_factor_milli: 1_000,
            focused: false,
            minimized: true,
            ime_active: false,
            modifiers_active: false,
        }
    }
}

impl WindowSnapshot {
    /// Return the last physical width.
    #[must_use]
    pub const fn width(self) -> u32 {
        self.width
    }

    /// Return the last physical height.
    #[must_use]
    pub const fn height(self) -> u32 {
        self.height
    }

    /// Return the scale factor represented in thousandths.
    #[must_use]
    pub const fn scale_factor_milli(self) -> u32 {
        self.scale_factor_milli
    }

    /// Return whether the shell currently has focus.
    #[must_use]
    pub const fn focused(self) -> bool {
        self.focused
    }

    /// Return whether the last size represents a minimized/zero-size window.
    #[must_use]
    pub const fn minimized(self) -> bool {
        self.minimized
    }

    /// Return whether an IME composition is considered active.
    #[must_use]
    pub const fn ime_active(self) -> bool {
        self.ime_active
    }

    /// Return whether non-empty keyboard modifiers are active.
    #[must_use]
    pub const fn modifiers_active(self) -> bool {
        self.modifiers_active
    }
}

/// Bounded command accepted by the deterministic shell.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ShellCommand {
    /// One synthetic event-loop wake from the current process generation.
    Wake {
        /// Generation that produced the event.
        generation: ProcessGeneration,
    },
    /// Request idempotent shutdown for the current process generation.
    RequestClose {
        /// Generation that produced the event.
        generation: ProcessGeneration,
    },
}

impl ShellCommand {
    const fn generation(self) -> ProcessGeneration {
        match self {
            Self::Wake { generation } | Self::RequestClose { generation } => generation,
        }
    }
}

/// Closed, secret-free application-shell failure.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ShellError {
    /// An operation is not valid in the current phase.
    InvalidTransition {
        /// Current phase.
        phase: ShellPhase,
        /// Rejected operation.
        action: ShellAction,
    },
    /// A command was produced by an obsolete process generation.
    StaleGeneration {
        /// Current process generation.
        expected: ProcessGeneration,
        /// Rejected generation.
        received: ProcessGeneration,
    },
    /// A command batch exceeded the fixed transactional bound.
    CommandBatchTooLarge {
        /// Maximum accepted number of commands.
        max_commands: usize,
    },
    /// A zero scale factor was rejected.
    InvalidScaleFactor,
    /// Reviewed static diagnostic text was invalid.
    DiagnosticText(StaticTextError),
    /// A bounded diagnostic event rejected a field.
    DiagnosticBuild(DiagnosticBuildError),
}

impl Display for ShellError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::InvalidTransition { phase, action } => {
                write!(formatter, "shell cannot {action} while {phase}")
            }
            Self::StaleGeneration { expected, received } => write!(
                formatter,
                "shell rejected stale process generation {received}; current generation is {expected}"
            ),
            Self::CommandBatchTooLarge { max_commands } => {
                write!(
                    formatter,
                    "shell command batch exceeds {max_commands} commands"
                )
            }
            Self::InvalidScaleFactor => formatter.write_str("shell scale factor must be non-zero"),
            Self::DiagnosticText(error) => Display::fmt(error, formatter),
            Self::DiagnosticBuild(error) => Display::fmt(error, formatter),
        }
    }
}

impl std::error::Error for ShellError {
    fn source(&self) -> Option<&(dyn std::error::Error + 'static)> {
        match self {
            Self::DiagnosticText(error) => Some(error),
            Self::DiagnosticBuild(error) => Some(error),
            Self::InvalidTransition { .. }
            | Self::StaleGeneration { .. }
            | Self::CommandBatchTooLarge { .. }
            | Self::InvalidScaleFactor => None,
        }
    }
}

impl From<StaticTextError> for ShellError {
    fn from(error: StaticTextError) -> Self {
        Self::DiagnosticText(error)
    }
}

impl From<DiagnosticBuildError> for ShellError {
    fn from(error: DiagnosticBuildError) -> Self {
        Self::DiagnosticBuild(error)
    }
}

/// Deterministic application-shell state independent of native window handles.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct ShellState {
    process_generation: ProcessGeneration,
    phase: ShellPhase,
    window: WindowSnapshot,
    wake_count: u64,
    diagnostics: VecDeque<DiagnosticEvent>,
}

impl ShellState {
    /// Construct a new shell and record its first bounded lifecycle diagnostic.
    ///
    /// # Errors
    ///
    /// Returns a closed diagnostic construction error if reviewed constants no
    /// longer satisfy the diagnostics contract.
    pub fn new(
        process_generation: ProcessGeneration,
        occurred_at: Moment,
    ) -> Result<Self, ShellError> {
        let mut state = Self {
            process_generation,
            phase: ShellPhase::Starting,
            window: WindowSnapshot::default(),
            wake_count: 0,
            diagnostics: VecDeque::with_capacity(MAX_SHELL_DIAGNOSTICS),
        };
        state.record_lifecycle(CODE_CREATED, "shell created", occurred_at)?;
        Ok(state)
    }

    /// Return the owning process generation.
    #[must_use]
    pub const fn process_generation(&self) -> ProcessGeneration {
        self.process_generation
    }

    /// Return the current lifecycle phase.
    #[must_use]
    pub const fn phase(&self) -> ShellPhase {
        self.phase
    }

    /// Return the deterministic window snapshot.
    #[must_use]
    pub const fn window(&self) -> WindowSnapshot {
        self.window
    }

    /// Return the number of accepted synthetic wakes.
    #[must_use]
    pub const fn wake_count(&self) -> u64 {
        self.wake_count
    }

    /// Return the bounded number of retained diagnostics.
    #[must_use]
    pub fn diagnostic_count(&self) -> usize {
        self.diagnostics.len()
    }

    /// Iterate retained diagnostics in deterministic oldest-to-newest order.
    pub fn diagnostics(&self) -> impl ExactSizeIterator<Item = &DiagnosticEvent> {
        self.diagnostics.iter()
    }

    /// Move from starting to running. Repeated running notifications are idempotent.
    ///
    /// # Errors
    ///
    /// Returns [`ShellError::InvalidTransition`] after closing has begun.
    pub fn mark_running(&mut self, occurred_at: Moment) -> Result<bool, ShellError> {
        match self.phase {
            ShellPhase::Starting => {
                self.phase = ShellPhase::Running;
                self.record_lifecycle(CODE_RUNNING, "shell running", occurred_at)?;
                Ok(true)
            }
            ShellPhase::Running => Ok(false),
            ShellPhase::Closing | ShellPhase::Exited => Err(ShellError::InvalidTransition {
                phase: self.phase,
                action: ShellAction::MarkRunning,
            }),
        }
    }

    /// Request shutdown for the current generation. The close path is idempotent.
    ///
    /// # Errors
    ///
    /// Returns [`ShellError::StaleGeneration`] for obsolete commands.
    pub fn request_close(
        &mut self,
        generation: ProcessGeneration,
        occurred_at: Moment,
    ) -> Result<bool, ShellError> {
        self.require_generation(generation)?;
        match self.phase {
            ShellPhase::Starting | ShellPhase::Running => {
                self.phase = ShellPhase::Closing;
                self.clear_transient_input();
                self.record_lifecycle(CODE_CLOSE_REQUESTED, "shell close requested", occurred_at)?;
                Ok(true)
            }
            ShellPhase::Closing | ShellPhase::Exited => Ok(false),
        }
    }

    /// Complete shutdown after the close path has started.
    ///
    /// # Errors
    ///
    /// Returns [`ShellError::InvalidTransition`] if close was not requested.
    pub fn mark_exited(&mut self, occurred_at: Moment) -> Result<bool, ShellError> {
        match self.phase {
            ShellPhase::Closing => {
                self.phase = ShellPhase::Exited;
                self.record_lifecycle(CODE_EXITED, "shell exited", occurred_at)?;
                Ok(true)
            }
            ShellPhase::Exited => Ok(false),
            ShellPhase::Starting | ShellPhase::Running => Err(ShellError::InvalidTransition {
                phase: self.phase,
                action: ShellAction::MarkExited,
            }),
        }
    }

    /// Apply a bounded batch transactionally.
    ///
    /// # Errors
    ///
    /// Rejects oversized batches, stale generations or diagnostic construction
    /// failures without mutating the original state.
    pub fn apply_commands(
        &mut self,
        commands: &[ShellCommand],
        occurred_at: Moment,
    ) -> Result<(), ShellError> {
        if commands.len() > MAX_COMMAND_BATCH {
            return Err(ShellError::CommandBatchTooLarge {
                max_commands: MAX_COMMAND_BATCH,
            });
        }

        let mut staged = self.clone();
        for command in commands {
            staged.apply_command(*command, occurred_at)?;
        }
        *self = staged;
        Ok(())
    }

    /// Record a physical resize; either zero dimension represents minimization.
    pub fn resize(&mut self, width: u32, height: u32) {
        self.window.width = width;
        self.window.height = height;
        self.window.minimized = width == 0 || height == 0;
    }

    /// Record focus. Losing focus clears transient modifier and IME state.
    pub fn set_focused(&mut self, focused: bool) {
        self.window.focused = focused;
        if !focused {
            self.clear_transient_input();
        }
    }

    /// Record whether keyboard modifiers are active.
    pub fn set_modifiers_active(&mut self, active: bool) {
        self.window.modifiers_active = active;
    }

    /// Record whether an IME composition is active.
    pub fn set_ime_active(&mut self, active: bool) {
        self.window.ime_active = active;
    }

    /// Record a positive scale factor represented in thousandths.
    ///
    /// # Errors
    ///
    /// Rejects zero without mutating the previous factor.
    pub fn set_scale_factor_milli(&mut self, scale_factor_milli: u32) -> Result<(), ShellError> {
        if scale_factor_milli == 0 {
            return Err(ShellError::InvalidScaleFactor);
        }
        self.window.scale_factor_milli = scale_factor_milli;
        Ok(())
    }

    fn apply_command(
        &mut self,
        command: ShellCommand,
        occurred_at: Moment,
    ) -> Result<(), ShellError> {
        self.require_generation(command.generation())?;
        match command {
            ShellCommand::Wake { .. } => {
                if matches!(self.phase, ShellPhase::Starting | ShellPhase::Running) {
                    self.wake_count = self.wake_count.saturating_add(1);
                    self.record_lifecycle(CODE_WAKE_RECEIVED, "shell wake received", occurred_at)?;
                }
                Ok(())
            }
            ShellCommand::RequestClose { generation } => {
                let _changed = self.request_close(generation, occurred_at)?;
                Ok(())
            }
        }
    }

    fn require_generation(&self, received: ProcessGeneration) -> Result<(), ShellError> {
        if received == self.process_generation {
            Ok(())
        } else {
            Err(ShellError::StaleGeneration {
                expected: self.process_generation,
                received,
            })
        }
    }

    fn clear_transient_input(&mut self) {
        self.window.modifiers_active = false;
        self.window.ime_active = false;
    }

    fn record_lifecycle(
        &mut self,
        code: u32,
        message: &'static str,
        occurred_at: Moment,
    ) -> Result<(), ShellError> {
        let context = TechnicalContext::new(occurred_at, self.process_generation);
        let message = SafeText::trusted_static(message)?;
        let phase_text = SafeText::trusted_static(self.phase.as_static_str())?;
        let phase_key = FieldKey::trusted_static("phase")?;
        let wake_key = FieldKey::trusted_static("wake_count")?;
        let mut event = DiagnosticEvent::new(
            Severity::Info,
            DiagnosticCategory::Lifecycle,
            DiagnosticCode::new(code),
            message,
            context,
        );
        event.try_add_field(DiagnosticField::new(
            phase_key,
            DiagnosticValue::SafeText(phase_text),
        ))?;
        event.try_add_field(DiagnosticField::new(
            wake_key,
            DiagnosticValue::Unsigned(self.wake_count),
        ))?;

        if self.diagnostics.len() == MAX_SHELL_DIAGNOSTICS {
            let _discarded = self.diagnostics.pop_front();
        }
        self.diagnostics.push_back(event);
        Ok(())
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_diagnostics::{CorrelationId, DiagnosticValue};
    use oteryn_test_support::{DiagnosticEventFixture, TestTimeline};
    use std::time::Duration;

    fn timeline_and_state() -> Result<(TestTimeline, ShellState), ShellError> {
        let timeline = TestTimeline::new(Moment::ZERO, ProcessGeneration::new(7));
        let state = ShellState::new(timeline.process_generation(), timeline.now())?;
        Ok((timeline, state))
    }

    #[test]
    fn lifecycle_transitions_are_explicit_and_idempotent() -> Result<(), Box<dyn std::error::Error>>
    {
        let (timeline, mut state) = timeline_and_state()?;
        assert_eq!(state.phase(), ShellPhase::Starting);
        assert!(state.mark_running(timeline.now())?);
        assert!(!state.mark_running(timeline.now())?);
        assert!(state.request_close(state.process_generation(), timeline.now())?);
        assert!(!state.request_close(state.process_generation(), timeline.now())?);
        assert!(state.mark_exited(timeline.now())?);
        assert!(!state.mark_exited(timeline.now())?);
        Ok(())
    }

    #[test]
    fn stale_generation_rejection_is_transactional() -> Result<(), Box<dyn std::error::Error>> {
        let (timeline, mut state) = timeline_and_state()?;
        state.mark_running(timeline.now())?;
        let before = state.clone();
        let commands = [
            ShellCommand::Wake {
                generation: state.process_generation(),
            },
            ShellCommand::RequestClose {
                generation: ProcessGeneration::new(6),
            },
        ];

        assert_eq!(
            state.apply_commands(&commands, timeline.now()),
            Err(ShellError::StaleGeneration {
                expected: ProcessGeneration::new(7),
                received: ProcessGeneration::new(6),
            })
        );
        assert_eq!(state, before);
        Ok(())
    }

    #[test]
    fn command_batch_bound_is_enforced_without_mutation() -> Result<(), ShellError> {
        let (timeline, mut state) = timeline_and_state()?;
        let before = state.clone();
        let commands = vec![
            ShellCommand::Wake {
                generation: state.process_generation(),
            };
            MAX_COMMAND_BATCH + 1
        ];

        assert_eq!(
            state.apply_commands(&commands, timeline.now()),
            Err(ShellError::CommandBatchTooLarge {
                max_commands: MAX_COMMAND_BATCH,
            })
        );
        assert_eq!(state, before);
        Ok(())
    }

    #[test]
    fn resize_focus_modifiers_and_ime_are_deterministic() -> Result<(), ShellError> {
        let (_timeline, mut state) = timeline_and_state()?;
        state.resize(0, 720);
        assert!(state.window().minimized());
        state.resize(1280, 720);
        assert!(!state.window().minimized());
        assert_eq!(state.window().width(), 1280);
        assert_eq!(state.window().height(), 720);

        state.set_focused(true);
        state.set_modifiers_active(true);
        state.set_ime_active(true);
        state.set_focused(false);
        assert!(!state.window().focused());
        assert!(!state.window().modifiers_active());
        assert!(!state.window().ime_active());

        assert_eq!(
            state.set_scale_factor_milli(0),
            Err(ShellError::InvalidScaleFactor)
        );
        assert_eq!(state.window().scale_factor_milli(), 1_000);
        state.set_scale_factor_milli(1_500)?;
        assert_eq!(state.window().scale_factor_milli(), 1_500);
        Ok(())
    }

    #[test]
    fn diagnostic_history_is_bounded_and_ordered() -> Result<(), Box<dyn std::error::Error>> {
        let (timeline, mut state) = timeline_and_state()?;
        state.mark_running(timeline.now())?;
        for _ in 0..(MAX_SHELL_DIAGNOSTICS + 8) {
            state.apply_commands(
                &[ShellCommand::Wake {
                    generation: state.process_generation(),
                }],
                timeline.now(),
            )?;
        }

        assert_eq!(state.diagnostic_count(), MAX_SHELL_DIAGNOSTICS);
        assert!(
            state
                .diagnostics()
                .all(|event| event.code() == DiagnosticCode::new(CODE_WAKE_RECEIVED))
        );
        assert_eq!(state.wake_count(), (MAX_SHELL_DIAGNOSTICS + 8) as u64);
        Ok(())
    }

    #[test]
    fn merged_test_support_builds_compatible_diagnostics() -> Result<(), Box<dyn std::error::Error>>
    {
        let timeline = TestTimeline::new(Moment::ZERO, ProcessGeneration::new(9));
        timeline.advance(Duration::from_millis(25))?;
        let context = timeline.context(None, None, Some(CorrelationId::new(11)));
        let mut fixture = DiagnosticEventFixture::new(
            Severity::Info,
            DiagnosticCategory::Lifecycle,
            DiagnosticCode::new(2_001),
            "shell fixture",
            context,
        )?;
        fixture.try_add_field(
            "generation",
            DiagnosticValue::ProcessGeneration(ProcessGeneration::new(9)),
        )?;
        let event = fixture.build();

        assert_eq!(event.context().occurred_at(), timeline.now());
        assert_eq!(event.field_count(), 1);
        Ok(())
    }

    #[test]
    fn repeated_construction_has_no_global_state() -> Result<(), ShellError> {
        let first = ShellState::new(ProcessGeneration::new(1), Moment::ZERO)?;
        let second = ShellState::new(ProcessGeneration::new(2), Moment::ZERO)?;

        assert_eq!(first.wake_count(), 0);
        assert_eq!(second.wake_count(), 0);
        assert_ne!(first.process_generation(), second.process_generation());
        assert_eq!(first.diagnostic_count(), 1);
        assert_eq!(second.diagnostic_count(), 1);
        Ok(())
    }

    #[test]
    fn errors_are_closed_and_contain_no_external_text() {
        let error = ShellError::StaleGeneration {
            expected: ProcessGeneration::new(3),
            received: ProcessGeneration::new(2),
        };
        let display = error.to_string();
        let debug = format!("{error:?}");

        assert_eq!(
            display,
            "shell rejected stale process generation 2; current generation is 3"
        );
        assert!(!debug.contains("token"));
        assert!(!display.contains("secret"));
    }
}
