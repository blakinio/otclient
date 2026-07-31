use oteryn_account_session::AccountSessionId;
use oteryn_app_runtime::{RuntimeError, TechnicalLoginRuntime, TechnicalSelection};
use oteryn_foundation::{MonotonicClock, SystemClock};
use oteryn_game_session::{EntryFailure, EntryFailureKind, EntryPhase, SessionEntered};
use oteryn_identity::{
    FixedAccountSession, IdentityClient, IdentityConfig, OsEntropy, SystemBrowser,
    TcpLoopbackBinder,
};
use oteryn_platform::{PlatformClient, PlatformEndpoints, UreqTransport};
use oteryn_protocol_canary::{CanaryAdmissionOutcome, CanaryEntryAdapter};
use oteryn_transport::TransportConfig;
use oteryn_world_directory::{
    CharacterId, DirectoryRevision, DirectorySubject, WorldId, WorldRoute,
};
use std::env;
use std::error::Error;
use std::fmt::{self, Display, Formatter};
use std::sync::Arc;
use std::time::Duration;

const OPT_IN: &str = "OTERYN_TECHNICAL_LOGIN";
const AUTHORIZATION_BASE: &str = "OTERYN_TECH_AUTHORIZATION_BASE";
const GATEWAY_BASE: &str = "OTERYN_TECH_GATEWAY_BASE";
const PUBLIC_CLIENT_ID: &str = "OTERYN_TECH_PUBLIC_CLIENT_ID";
const WORLD_ID: &str = "OTERYN_TECH_WORLD_ID";
const WORLD_HOST: &str = "OTERYN_TECH_WORLD_HOST";
const WORLD_PORT: &str = "OTERYN_TECH_WORLD_PORT";
const CHARACTER_ID: &str = "OTERYN_TECH_CHARACTER_ID";
const CALLBACK_TIMEOUT: &str = "OTERYN_TECH_CALLBACK_TIMEOUT_SECS";
const HTTP_TIMEOUT: &str = "OTERYN_TECH_HTTP_TIMEOUT_SECS";
const CONNECT_TIMEOUT: &str = "OTERYN_TECH_CONNECT_TIMEOUT_SECS";
const READ_TIMEOUT: &str = "OTERYN_TECH_READ_TIMEOUT_SECS";
const WRITE_TIMEOUT: &str = "OTERYN_TECH_WRITE_TIMEOUT_SECS";

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum TechnicalWorkerStage {
    Identity,
    Admission,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) struct TechnicalWorkerSignal {
    pub(crate) attempt_id: oteryn_game_session::GameEntryAttemptId,
    pub(crate) stage: TechnicalWorkerStage,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum ConfigField {
    OptIn,
    AuthorizationBase,
    GatewayBase,
    PublicClientId,
    WorldId,
    WorldHost,
    WorldPort,
    CharacterId,
    CallbackTimeout,
    HttpTimeout,
    ConnectTimeout,
    ReadTimeout,
    WriteTimeout,
}

impl Display for ConfigField {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str(match self {
            Self::OptIn => OPT_IN,
            Self::AuthorizationBase => AUTHORIZATION_BASE,
            Self::GatewayBase => GATEWAY_BASE,
            Self::PublicClientId => PUBLIC_CLIENT_ID,
            Self::WorldId => WORLD_ID,
            Self::WorldHost => WORLD_HOST,
            Self::WorldPort => WORLD_PORT,
            Self::CharacterId => CHARACTER_ID,
            Self::CallbackTimeout => CALLBACK_TIMEOUT,
            Self::HttpTimeout => HTTP_TIMEOUT,
            Self::ConnectTimeout => CONNECT_TIMEOUT,
            Self::ReadTimeout => READ_TIMEOUT,
            Self::WriteTimeout => WRITE_TIMEOUT,
        })
    }
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub(crate) enum TechnicalLoginError {
    MissingConfiguration(ConfigField),
    InvalidConfiguration(ConfigField),
    Runtime(RuntimeError),
}

impl From<RuntimeError> for TechnicalLoginError {
    fn from(error: RuntimeError) -> Self {
        Self::Runtime(error)
    }
}

impl Display for TechnicalLoginError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::MissingConfiguration(field) => {
                write!(formatter, "technical login requires explicit {field}")
            }
            Self::InvalidConfiguration(field) => {
                write!(
                    formatter,
                    "technical login configuration {field} is invalid"
                )
            }
            Self::Runtime(error) => Display::fmt(error, formatter),
        }
    }
}

impl Error for TechnicalLoginError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Runtime(error) => Some(error),
            Self::MissingConfiguration(_) | Self::InvalidConfiguration(_) => None,
        }
    }
}

#[derive(Debug, Clone)]
struct TechnicalLoginConfig {
    authorization_base: String,
    gateway_base: String,
    public_client_id: String,
    world_id: WorldId,
    world_host: String,
    world_port: u16,
    character_id: CharacterId,
    callback_timeout: Duration,
    http_timeout: Duration,
    transport: TransportConfig,
}

impl TechnicalLoginConfig {
    fn from_environment() -> Result<Option<Self>, TechnicalLoginError> {
        match env::var(OPT_IN) {
            Err(env::VarError::NotPresent) => return Ok(None),
            Err(env::VarError::NotUnicode(_)) => {
                return Err(TechnicalLoginError::InvalidConfiguration(
                    ConfigField::OptIn,
                ));
            }
            Ok(value) if value == "1" => {}
            Ok(_) => {
                return Err(TechnicalLoginError::InvalidConfiguration(
                    ConfigField::OptIn,
                ));
            }
        }

        let authorization_base =
            required_string(AUTHORIZATION_BASE, ConfigField::AuthorizationBase)?;
        let gateway_base = required_string(GATEWAY_BASE, ConfigField::GatewayBase)?;
        let public_client_id = required_string(PUBLIC_CLIENT_ID, ConfigField::PublicClientId)?;
        let world_id = WorldId::new(required_i64(WORLD_ID, ConfigField::WorldId)?)
            .map_err(|_| TechnicalLoginError::InvalidConfiguration(ConfigField::WorldId))?;
        let world_host = required_string(WORLD_HOST, ConfigField::WorldHost)?;
        let world_port = required_u16(WORLD_PORT, ConfigField::WorldPort)?;
        WorldRoute::new(world_host.clone(), world_port)
            .map_err(|_| TechnicalLoginError::InvalidConfiguration(ConfigField::WorldHost))?;
        let character_id = CharacterId::new(required_i64(CHARACTER_ID, ConfigField::CharacterId)?)
            .map_err(|_| TechnicalLoginError::InvalidConfiguration(ConfigField::CharacterId))?;
        let callback_timeout = required_duration(CALLBACK_TIMEOUT, ConfigField::CallbackTimeout)?;
        let http_timeout = required_duration(HTTP_TIMEOUT, ConfigField::HttpTimeout)?;
        let connect_timeout = required_duration(CONNECT_TIMEOUT, ConfigField::ConnectTimeout)?;
        let read_timeout = required_duration(READ_TIMEOUT, ConfigField::ReadTimeout)?;
        let write_timeout = required_duration(WRITE_TIMEOUT, ConfigField::WriteTimeout)?;
        let transport =
            TransportConfig::new(connect_timeout, read_timeout, write_timeout, 4_096, 4_096)
                .map_err(|_| {
                    TechnicalLoginError::InvalidConfiguration(ConfigField::ConnectTimeout)
                })?;

        PlatformEndpoints::new(&authorization_base, &gateway_base).map_err(|_| {
            TechnicalLoginError::InvalidConfiguration(ConfigField::AuthorizationBase)
        })?;
        IdentityConfig::new(
            &authorization_base,
            public_client_id.clone(),
            "/callback".to_owned(),
            callback_timeout,
        )
        .map_err(|_| TechnicalLoginError::InvalidConfiguration(ConfigField::AuthorizationBase))?;
        UreqTransport::new(http_timeout)
            .map_err(|_| TechnicalLoginError::InvalidConfiguration(ConfigField::HttpTimeout))?;

        Ok(Some(Self {
            authorization_base,
            gateway_base,
            public_client_id,
            world_id,
            world_host,
            world_port,
            character_id,
            callback_timeout,
            http_timeout,
            transport,
        }))
    }
}

fn required_string(name: &str, field: ConfigField) -> Result<String, TechnicalLoginError> {
    match env::var(name) {
        Ok(value) if !value.is_empty() => Ok(value),
        Ok(_) => Err(TechnicalLoginError::InvalidConfiguration(field)),
        Err(env::VarError::NotPresent) => Err(TechnicalLoginError::MissingConfiguration(field)),
        Err(env::VarError::NotUnicode(_)) => Err(TechnicalLoginError::InvalidConfiguration(field)),
    }
}

fn required_i64(name: &str, field: ConfigField) -> Result<i64, TechnicalLoginError> {
    required_string(name, field)?
        .parse::<i64>()
        .map_err(|_| TechnicalLoginError::InvalidConfiguration(field))
}

fn required_u16(name: &str, field: ConfigField) -> Result<u16, TechnicalLoginError> {
    required_string(name, field)?
        .parse::<u16>()
        .map_err(|_| TechnicalLoginError::InvalidConfiguration(field))
}

fn required_duration(name: &str, field: ConfigField) -> Result<Duration, TechnicalLoginError> {
    let seconds = required_string(name, field)?
        .parse::<u64>()
        .map_err(|_| TechnicalLoginError::InvalidConfiguration(field))?;
    if seconds == 0 {
        return Err(TechnicalLoginError::InvalidConfiguration(field));
    }
    Ok(Duration::from_secs(seconds))
}

pub(crate) struct TechnicalLoginController {
    config: TechnicalLoginConfig,
    clock: SystemClock,
    runtime: TechnicalLoginRuntime,
    notifier: Option<Arc<dyn Fn(TechnicalWorkerSignal) + Send + Sync>>,
}

impl TechnicalLoginController {
    pub(crate) fn from_environment() -> Result<Option<Self>, TechnicalLoginError> {
        let Some(config) = TechnicalLoginConfig::from_environment()? else {
            return Ok(None);
        };
        let clock = SystemClock::new();
        let runtime_clock: Arc<dyn MonotonicClock> = Arc::new(clock.clone());
        Ok(Some(Self {
            config,
            clock,
            runtime: TechnicalLoginRuntime::new(runtime_clock),
            notifier: None,
        }))
    }

    pub(crate) fn start<F>(&mut self, notify: F) -> Result<(), TechnicalLoginError>
    where
        F: Fn(TechnicalWorkerSignal) + Send + Sync + 'static,
    {
        let notifier: Arc<dyn Fn(TechnicalWorkerSignal) + Send + Sync> = Arc::new(notify);
        self.notifier = Some(Arc::clone(&notifier));
        let config = self.config.clone();
        let identity_clock = self.clock.clone();
        let selection = TechnicalSelection::new(config.character_id, config.world_id, None);
        self.runtime
            .start_authentication(selection, move |attempt_id, cancellation| {
                let result = run_identity(&config, identity_clock, cancellation);
                notifier(TechnicalWorkerSignal {
                    attempt_id,
                    stage: TechnicalWorkerStage::Identity,
                });
                result
            })?;
        Ok(())
    }

    pub(crate) fn handle_signal(
        &mut self,
        signal: TechnicalWorkerSignal,
    ) -> Result<(), TechnicalLoginError> {
        if self.runtime.snapshot().active_attempt() != Some(signal.attempt_id) {
            return Ok(());
        }
        let _progressed = self.runtime.poll()?;
        if signal.stage == TechnicalWorkerStage::Identity
            && self.runtime.snapshot().phase() == EntryPhase::CredentialReady
        {
            self.start_admission()?;
        }
        Ok(())
    }

    pub(crate) fn poll(&mut self) -> Result<(), TechnicalLoginError> {
        let _progressed = self.runtime.poll()?;
        if self.runtime.snapshot().phase() == EntryPhase::CredentialReady {
            self.start_admission()?;
        }
        Ok(())
    }

    pub(crate) fn has_active_worker(&self) -> bool {
        matches!(
            self.runtime.snapshot().phase(),
            EntryPhase::Authenticating | EntryPhase::Connecting
        )
    }

    pub(crate) fn window_title(&self) -> &'static str {
        match self.runtime.snapshot().phase() {
            EntryPhase::LoggedOut => "Oteryn — Technical Login: logged out",
            EntryPhase::Authenticating => "Oteryn — Technical Login: authenticating",
            EntryPhase::AccountReady | EntryPhase::DirectoryReady | EntryPhase::EntryRequested => {
                "Oteryn — Technical Login: preparing entry"
            }
            EntryPhase::CredentialReady => "Oteryn — Technical Login: credential ready",
            EntryPhase::Connecting => "Oteryn — Technical Login: connecting",
            EntryPhase::SessionEntered => "Oteryn — Technical Login: session entered",
            EntryPhase::Failed => "Oteryn — Technical Login: recoverable failure",
            EntryPhase::Closing => "Oteryn — Technical Login: closing",
        }
    }

    pub(crate) fn shutdown(&mut self) -> Result<(), TechnicalLoginError> {
        self.runtime.shutdown()?;
        Ok(())
    }

    fn start_admission(&mut self) -> Result<(), TechnicalLoginError> {
        let notifier = self
            .notifier
            .as_ref()
            .cloned()
            .ok_or(TechnicalLoginError::Runtime(RuntimeError::NoActiveAttempt))?;
        let transport = self.config.transport;
        self.runtime
            .start_connection(move |mut lifecycle, attempt_id, cancellation, clock| {
                let result = (|| -> Result<SessionEntered, EntryFailure> {
                    let request = lifecycle.request().cloned().ok_or_else(|| {
                        EntryFailure::for_kind(EntryFailureKind::InvariantViolation)
                    })?;
                    let mut adapter = CanaryEntryAdapter::new(transport);
                    match adapter.connect(&request, &cancellation) {
                        Ok(()) => match adapter.enter_session(
                            &mut lifecycle,
                            attempt_id,
                            clock.as_ref(),
                            &cancellation,
                        ) {
                            CanaryAdmissionOutcome::SessionEntered(entered) => Ok(entered),
                            outcome => Err(outcome.entry_failure().unwrap_or_else(|| {
                                EntryFailure::for_kind(EntryFailureKind::InvariantViolation)
                            })),
                        },
                        Err(outcome) => Err(outcome.entry_failure().unwrap_or_else(|| {
                            EntryFailure::for_kind(EntryFailureKind::InvariantViolation)
                        })),
                    }
                })();
                notifier(TechnicalWorkerSignal {
                    attempt_id,
                    stage: TechnicalWorkerStage::Admission,
                });
                (lifecycle, result)
            })?;
        Ok(())
    }
}

fn run_identity(
    config: &TechnicalLoginConfig,
    clock: SystemClock,
    cancellation: oteryn_foundation::CancellationToken,
) -> Result<
    (
        AccountSessionId,
        oteryn_world_directory::AccountDirectorySnapshot,
        oteryn_game_session::GameEntryCredential,
    ),
    EntryFailure,
> {
    let account_session = AccountSessionId::new(1)
        .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?;
    let directory_revision = DirectoryRevision::new(1)
        .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?;
    let endpoints = PlatformEndpoints::new(&config.authorization_base, &config.gateway_base)
        .map_err(|_| EntryFailure::for_kind(EntryFailureKind::InvariantViolation))?;
    let transport = UreqTransport::new(config.http_timeout)
        .map_err(|_| EntryFailure::for_kind(EntryFailureKind::TransportFailure))?;
    let client = IdentityClient::new(
        PlatformClient::new(endpoints, transport),
        Box::new(TcpLoopbackBinder),
        Box::new(SystemBrowser),
        Box::new(OsEntropy),
        Box::new(clock),
    );
    let identity_config = IdentityConfig::new(
        &config.authorization_base,
        config.public_client_id.clone(),
        "/callback".to_owned(),
        config.callback_timeout,
    )
    .map_err(|error| error.entry_failure())?;
    let bootstrap = client
        .authenticate(
            &identity_config,
            &FixedAccountSession(account_session),
            account_session,
            directory_revision,
            &cancellation,
        )
        .map_err(|error| error.entry_failure())?;
    let accepted_account = bootstrap.account_session_id();
    let (directory, credential) = bootstrap.into_parts();
    let world = directory
        .worlds()
        .iter()
        .find(|world| world.id() == config.world_id)
        .ok_or_else(|| EntryFailure::selected_entry_unavailable(DirectorySubject::World))?;
    if world.route().host() != config.world_host || world.route().port() != config.world_port {
        return Err(EntryFailure::selected_entry_unavailable(
            DirectorySubject::World,
        ));
    }
    Ok((accepted_account, directory, credential))
}
