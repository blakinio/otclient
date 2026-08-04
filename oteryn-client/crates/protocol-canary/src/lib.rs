//! Exact-evidence-gated Canary Current admission boundary for W7.
//!
//! The public adapter consumes the merged W7 entry lifecycle and never exposes
//! an admission credential or raw socket to application code. Exact source facts
//! are published as non-secret metadata. Real wire admission remains fail-closed
//! until provenance-safe transcript evidence is sufficient to implement and
//! validate RSA, XTEA, sequence, padding and compression end to end.

use oteryn_foundation::{CancellationToken, MonotonicClock};
use oteryn_game_session::{
    AdmissionCredential, EntryFailure, EntryFailureKind, EntryLifecycle, EntryProfile,
    GameEntryAttemptId, GameEntryRequest, SessionEntered,
};
use oteryn_transport::{TcpTransport, TransportConfig};
use oteryn_world_directory::DirectorySubject;
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};

#[cfg(test)]
mod synthetic;
#[cfg(test)]
mod tests;

mod command;
mod inbound;
mod known_player;
mod map;
mod reconciliation;
mod tile;

pub use command::{
    CanaryCommandError, EncodedCanaryCommand, OPCODE_LOGOUT, OPCODE_STEP_EAST, OPCODE_STEP_NORTH,
    OPCODE_STEP_NORTH_EAST, OPCODE_STEP_NORTH_WEST, OPCODE_STEP_SOUTH, OPCODE_STEP_SOUTH_EAST,
    OPCODE_STEP_SOUTH_WEST, OPCODE_STEP_WEST, OPCODE_STOP_MOVEMENT,
    encode_current_development_command,
};
pub use inbound::{
    CanaryInboundBootstrapState, CanaryInboundError, OPCODE_ALLOW_BUG_REPORT, OPCODE_ENTER_WORLD,
    OPCODE_LOCAL_PLAYER_INITIALIZATION, OPCODE_PENDING_STATE_ENTERED, OPCODE_TIBIA_TIME,
    decode_current_allow_bug_report, decode_current_enter_world,
    decode_current_local_player_initialization, decode_current_pending_state_entered,
    decode_current_tibia_time,
};
pub use known_player::decode_current_known_remote_player_appearance;
pub use map::{OPCODE_MAP_DESCRIPTION, decode_current_local_player_only_map};
pub use reconciliation::{
    CanaryEntityReconciliationResolver, CanaryReconciliationError, OPCODE_MOVE_CREATURE,
    OPCODE_REMOVE_TILE_THING, ResolvedCanaryEntityMovement, decode_current_remote_entity_movement,
    decode_current_remote_entity_removal,
};
pub use tile::{OPCODE_TILE_UPDATE, decode_current_empty_tile_update};

/// Exact generated-source revision selected as the Current development baseline.
pub const CANARY_CURRENT_REVISION: &str = "bc0068ab80bbf003e128fce0589b4cc89d2682d3";
/// Runtime descriptor revision used before the P2 generated-index alignment.
pub const CANARY_PREVIOUS_RUNTIME_REVISION: &str = "95b276db311cf6e9acd58b847f1fb0ca6697b137";
/// Historical source cut accepted before the generated P1 index existed.
pub const CANARY_ACCEPTED_SOURCE_CUT: &str = "4b2d6f432d92628c42bde1d95daed6ae0d0eb88f";
/// Generated source-index schema consumed as read-only development evidence.
pub const CANARY_SOURCE_INDEX_SCHEMA: &str = "oteryn-canary-source-index-v1";
/// Repository named by the generated source-index producer metadata.
pub const CANARY_SOURCE_INDEX_REPOSITORY: &str = "blakinio/canary";
/// Producer profile expression recorded by the generated source index.
pub const CANARY_SOURCE_INDEX_PROFILE: &str = "ProtocolProfileId::Current";
/// Total exact dispatch/source entries in the generated index.
pub const CANARY_SOURCE_INDEX_ENTRY_COUNT: usize = 347;
/// Client-to-server entries in the generated index.
pub const CANARY_SOURCE_INDEX_CLIENT_TO_SERVER_COUNT: usize = 159;
/// Server-to-client entries in the generated index.
pub const CANARY_SOURCE_INDEX_SERVER_TO_CLIENT_COUNT: usize = 188;
/// Exact enabled feature declarations at the selected source revision.
pub const CANARY_CURRENT_ENABLED_FEATURES: [&str; 16] = [
    "CurrentPayload",
    "CustomMonkPackets",
    "GameEventPayload",
    "GraphicalEffectSourceByte",
    "ImbuementWindow",
    "LoginSpeedFormula",
    "MarketPackets",
    "MemorialPackets",
    "ModernLoginSideSystems",
    "OfficialSkillWheelPayload",
    "OfficialSoulSealsPackets",
    "OfficialTaskboardPackets",
    "OfficialVocationSpecificPlayerData",
    "OfficialWeaponProficiencyPayload",
    "PlayerDataLevelPercentU16",
    "ResourceBalancePackets",
];
/// Exact Canary release identifier at the selected revision.
pub const CANARY_RELEASE: &str = "3.6.1";
/// Exact Current client/protocol version at the selected revision.
pub const CANARY_CURRENT_CLIENT_VERSION: u16 = 1525;
/// Exact profile identifier in Canary's profile registry.
pub const CANARY_CURRENT_PROFILE_IDENTIFIER: &str = "current";
/// Canary's bounded network-message buffer size.
pub const CANARY_NETWORK_MESSAGE_MAX_BYTES: usize = 65_500;
/// Canary's bounded client input-message size.
pub const CANARY_INPUT_MESSAGE_MAX_BYTES: usize = 4_096;
/// Canary's explicit player-name byte limit.
pub const CANARY_CHARACTER_NAME_MAX_BYTES: usize = 30;

/// Exact non-secret SHA-256 evidence for one indexed producer source file.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CanarySourceFile {
    path: &'static str,
    sha256: &'static str,
}

impl CanarySourceFile {
    /// Create one immutable source-file evidence record.
    #[must_use]
    pub const fn new(path: &'static str, sha256: &'static str) -> Self {
        Self { path, sha256 }
    }

    /// Return the repository-relative producer source path.
    #[must_use]
    pub const fn path(self) -> &'static str {
        self.path
    }

    /// Return the lowercase SHA-256 digest of the exact source bytes.
    #[must_use]
    pub const fn sha256(self) -> &'static str {
        self.sha256
    }
}

/// Exact producer source path/hash evidence recorded by the generated index.
pub const CANARY_CURRENT_SOURCE_FILES: [CanarySourceFile; 7] = [
    CanarySourceFile::new(
        "src/core.hpp",
        "6e665eb99b62049c78b84d142eea070913b74699c2c40448d1473e3bcd211ce6",
    ),
    CanarySourceFile::new(
        "src/server/network/protocol/protocol_port_utils.hpp",
        "3a39e0693cdea574f6decc5a061c715b3b1573e82791696cd681b46243e70505",
    ),
    CanarySourceFile::new(
        "src/server/network/protocol/protocol_profile.cpp",
        "69d2d4193e721b83805031108825a5f3bf30ae4e5e46c27729ea5493ea6d33df",
    ),
    CanarySourceFile::new(
        "src/server/network/protocol/protocol_profile.hpp",
        "7cbb7ac6d16b6f7eb74201d00fc60ccd6d098e862814164efa45596392ff4a58",
    ),
    CanarySourceFile::new(
        "src/server/network/protocol/protocol_session_hint.hpp",
        "3b84362af14d7909b37c6b8adf61d941987cb59729090c295841866488a2d2db",
    ),
    CanarySourceFile::new(
        "src/server/network/protocol/protocolgame.cpp",
        "af7484cd0c4e1e4e5812ea3b6f1813031687331696001fb74de0be9bd21d5efc",
    ),
    CanarySourceFile::new(
        "src/server/network/protocol/protocolgame.hpp",
        "33a97f6c54baa6138555164995c0125141407bd7d7a4e71dd7c0561c0f246beb",
    ),
];

/// Exact non-secret Current-profile source descriptor.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CurrentProfileDescriptor {
    revision: &'static str,
    release: &'static str,
    identifier: &'static str,
    client_version: u16,
    source_index_schema: &'static str,
    source_repository: &'static str,
    source_profile: &'static str,
    source_entry_count: usize,
    client_to_server_entry_count: usize,
    server_to_client_entry_count: usize,
    enabled_features: &'static [&'static str],
    source_files: &'static [CanarySourceFile],
    max_network_message_bytes: usize,
    max_input_message_bytes: usize,
    max_character_name_bytes: usize,
}

impl CurrentProfileDescriptor {
    /// Return the exact read-only source revision.
    #[must_use]
    pub const fn revision(self) -> &'static str {
        self.revision
    }

    /// Return the exact Canary release.
    #[must_use]
    pub const fn release(self) -> &'static str {
        self.release
    }

    /// Return the exact profile identifier.
    #[must_use]
    pub const fn identifier(self) -> &'static str {
        self.identifier
    }

    /// Return the exact client/protocol version.
    #[must_use]
    pub const fn client_version(self) -> u16 {
        self.client_version
    }

    /// Return the generated source-index schema.
    #[must_use]
    pub const fn source_index_schema(self) -> &'static str {
        self.source_index_schema
    }

    /// Return the repository named by the source-index producer metadata.
    #[must_use]
    pub const fn source_repository(self) -> &'static str {
        self.source_repository
    }

    /// Return the producer profile expression recorded by the source index.
    #[must_use]
    pub const fn source_profile(self) -> &'static str {
        self.source_profile
    }

    /// Return the total generated dispatch/source entry count.
    #[must_use]
    pub const fn source_entry_count(self) -> usize {
        self.source_entry_count
    }

    /// Return the generated client-to-server entry count.
    #[must_use]
    pub const fn client_to_server_entry_count(self) -> usize {
        self.client_to_server_entry_count
    }

    /// Return the generated server-to-client entry count.
    #[must_use]
    pub const fn server_to_client_entry_count(self) -> usize {
        self.server_to_client_entry_count
    }

    /// Return the exact enabled feature declarations.
    #[must_use]
    pub const fn enabled_features(self) -> &'static [&'static str] {
        self.enabled_features
    }

    /// Return exact producer source path/SHA-256 evidence.
    #[must_use]
    pub const fn source_files(self) -> &'static [CanarySourceFile] {
        self.source_files
    }

    /// Return the server's bounded network-message size.
    #[must_use]
    pub const fn max_network_message_bytes(self) -> usize {
        self.max_network_message_bytes
    }

    /// Return the server's bounded client input-message size.
    #[must_use]
    pub const fn max_input_message_bytes(self) -> usize {
        self.max_input_message_bytes
    }

    /// Return the exact character-name byte limit.
    #[must_use]
    pub const fn max_character_name_bytes(self) -> usize {
        self.max_character_name_bytes
    }
}

/// Selected exact Current profile descriptor.
pub const CURRENT_PROFILE: CurrentProfileDescriptor = CurrentProfileDescriptor {
    revision: CANARY_CURRENT_REVISION,
    release: CANARY_RELEASE,
    identifier: CANARY_CURRENT_PROFILE_IDENTIFIER,
    client_version: CANARY_CURRENT_CLIENT_VERSION,
    source_index_schema: CANARY_SOURCE_INDEX_SCHEMA,
    source_repository: CANARY_SOURCE_INDEX_REPOSITORY,
    source_profile: CANARY_SOURCE_INDEX_PROFILE,
    source_entry_count: CANARY_SOURCE_INDEX_ENTRY_COUNT,
    client_to_server_entry_count: CANARY_SOURCE_INDEX_CLIENT_TO_SERVER_COUNT,
    server_to_client_entry_count: CANARY_SOURCE_INDEX_SERVER_TO_CLIENT_COUNT,
    enabled_features: &CANARY_CURRENT_ENABLED_FEATURES,
    source_files: &CANARY_CURRENT_SOURCE_FILES,
    max_network_message_bytes: CANARY_NETWORK_MESSAGE_MAX_BYTES,
    max_input_message_bytes: CANARY_INPUT_MESSAGE_MAX_BYTES,
    max_character_name_bytes: CANARY_CHARACTER_NAME_MAX_BYTES,
};

/// Select the one profile supported by the W7 adapter.
///
/// # Errors
///
/// Returns [`CanaryAdmissionOutcome::ProtocolMismatch`] for every unknown profile.
pub fn select_profile(
    identifier: &str,
) -> Result<CurrentProfileDescriptor, CanaryAdmissionOutcome> {
    if identifier == CANARY_CURRENT_PROFILE_IDENTIFIER {
        Ok(CURRENT_PROFILE)
    } else {
        Err(CanaryAdmissionOutcome::ProtocolMismatch)
    }
}

/// Deterministic state of the W7 Canary connection/admission owner.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CanaryConnectionState {
    /// No connection attempt has started.
    Idle,
    /// A bounded admission connection is active.
    Connected,
    /// The owner is terminal and cannot reconnect.
    Closed,
}

/// Stable application-facing Canary admission classifications.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CanaryAdmissionOutcome {
    /// Ordered technical admission completed and produced the shared result.
    SessionEntered(SessionEntered),
    /// The server denied admission for a non-credential reason.
    AdmissionDenied,
    /// The one-shot credential expired, was consumed or was rejected as such.
    CredentialExpiredOrConsumed,
    /// The selected character was rejected or did not match the credential.
    CharacterRejected,
    /// The configured profile or protocol did not match.
    ProtocolMismatch,
    /// The client version or asset identity requires repair/update.
    ClientOrAssetMismatch,
    /// The connection timed out, closed or otherwise became unusable.
    ConnectionLost,
    /// The active attempt was cancelled at a safe boundary.
    Cancelled,
    /// The requested operation violated deterministic adapter state.
    InvalidState,
    /// The exact real-wire implementation is intentionally blocked by evidence.
    RealAdmissionUnavailable,
}

impl CanaryAdmissionOutcome {
    /// Return the corresponding shared W7 failure when this is not success.
    #[must_use]
    pub const fn entry_failure(self) -> Option<EntryFailure> {
        match self {
            Self::SessionEntered(_) => None,
            Self::AdmissionDenied => Some(EntryFailure::for_kind(
                EntryFailureKind::ServerAdmissionDenied,
            )),
            Self::CredentialExpiredOrConsumed => {
                Some(EntryFailure::for_kind(EntryFailureKind::CredentialRejected))
            }
            Self::CharacterRejected => Some(EntryFailure::selected_entry_unavailable(
                DirectorySubject::Character,
            )),
            Self::ProtocolMismatch | Self::RealAdmissionUnavailable => {
                Some(EntryFailure::for_kind(EntryFailureKind::ProtocolMismatch))
            }
            Self::ClientOrAssetMismatch => Some(EntryFailure::for_kind(
                EntryFailureKind::AssetClientCompatibilityMismatch,
            )),
            Self::ConnectionLost => {
                Some(EntryFailure::for_kind(EntryFailureKind::TransportFailure))
            }
            Self::Cancelled => Some(EntryFailure::for_kind(EntryFailureKind::SafeCancellation)),
            Self::InvalidState => {
                Some(EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
            }
        }
    }
}

impl Display for CanaryAdmissionOutcome {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::SessionEntered(_) => "Canary session entered",
            Self::AdmissionDenied => "Canary admission denied",
            Self::CredentialExpiredOrConsumed => {
                "Canary credential expired, was consumed or was rejected"
            }
            Self::CharacterRejected => "Canary character was rejected",
            Self::ProtocolMismatch => "Canary protocol profile mismatch",
            Self::ClientOrAssetMismatch => "Canary client or asset mismatch",
            Self::ConnectionLost => "Canary admission connection was lost",
            Self::Cancelled => "Canary admission was cancelled",
            Self::InvalidState => "Canary admission state is invalid",
            Self::RealAdmissionUnavailable => {
                "Canary real admission is blocked by incomplete evidence"
            }
        };
        formatter.write_str(message)
    }
}

impl Error for CanaryAdmissionOutcome {}

/// Application-facing owner of one non-reconnecting Canary entry attempt.
pub struct CanaryEntryAdapter {
    state: CanaryConnectionState,
    transport_config: TransportConfig,
    transport: Option<TcpTransport>,
    mode: AdmissionMode,
}

enum AdmissionMode {
    EvidenceBlocked,
    #[cfg(test)]
    Synthetic(synthetic::SyntheticScript),
}

enum AdmissionExchange {
    #[cfg(test)]
    Entered,
    Outcome(CanaryAdmissionOutcome),
}

impl CanaryEntryAdapter {
    /// Construct the fail-closed exact Current adapter.
    ///
    /// Until the evidence document records provenance-safe exact transcript
    /// material, [`Self::connect`] returns
    /// [`CanaryAdmissionOutcome::RealAdmissionUnavailable`] before network I/O.
    #[must_use]
    pub const fn new(transport_config: TransportConfig) -> Self {
        Self {
            state: CanaryConnectionState::Idle,
            transport_config,
            transport: None,
            mode: AdmissionMode::EvidenceBlocked,
        }
    }

    /// Return the exact selected profile descriptor.
    #[must_use]
    pub const fn profile(&self) -> CurrentProfileDescriptor {
        CURRENT_PROFILE
    }

    /// Return the deterministic connection state.
    #[must_use]
    pub const fn state(&self) -> CanaryConnectionState {
        self.state
    }

    /// Return the bounded transport configuration owned by this adapter.
    #[must_use]
    pub const fn transport_config(&self) -> TransportConfig {
        self.transport_config
    }

    /// Start the one permitted admission connection.
    ///
    /// # Errors
    ///
    /// Rejects invalid profile/character/state/cancellation and fails closed
    /// before network I/O while exact real-wire evidence remains incomplete.
    pub fn connect(
        &mut self,
        request: &GameEntryRequest,
        cancellation: &CancellationToken,
    ) -> Result<(), CanaryAdmissionOutcome> {
        if self.state != CanaryConnectionState::Idle {
            return Err(CanaryAdmissionOutcome::InvalidState);
        }
        validate_request(request)?;
        if cancellation.is_cancelled() {
            self.state = CanaryConnectionState::Closed;
            return Err(CanaryAdmissionOutcome::Cancelled);
        }

        match &self.mode {
            AdmissionMode::EvidenceBlocked => Err(CanaryAdmissionOutcome::RealAdmissionUnavailable),
            #[cfg(test)]
            AdmissionMode::Synthetic(_) => {
                self.state = CanaryConnectionState::Connected;
                Ok(())
            }
        }
    }

    /// Consume the lifecycle-owned credential once and classify admission.
    ///
    /// The public production mode returns `RealAdmissionUnavailable` before
    /// credential handoff. Synthetic test mode exercises the exact ownership,
    /// cleanup and outcome mapping without claiming Canary wire compatibility.
    pub fn enter_session<C>(
        &mut self,
        lifecycle: &mut EntryLifecycle,
        attempt_id: GameEntryAttemptId,
        clock: &C,
        cancellation: &CancellationToken,
    ) -> CanaryAdmissionOutcome
    where
        C: MonotonicClock + ?Sized,
    {
        if self.state != CanaryConnectionState::Connected {
            return CanaryAdmissionOutcome::InvalidState;
        }
        if !self.has_admission_implementation() {
            return CanaryAdmissionOutcome::RealAdmissionUnavailable;
        }
        if cancellation.is_cancelled() {
            let outcome = record_outcome(lifecycle, attempt_id, CanaryAdmissionOutcome::Cancelled);
            self.close();
            return outcome;
        }

        let request = match lifecycle.request() {
            Some(request) => request.clone(),
            None => {
                self.close();
                return CanaryAdmissionOutcome::InvalidState;
            }
        };
        if let Err(outcome) = validate_request(&request) {
            self.close();
            return outcome;
        }

        let credential = match lifecycle.begin_connecting(attempt_id, clock) {
            Ok(credential) => credential,
            Err(failure) => {
                self.close();
                return outcome_from_entry_failure(failure);
            }
        };

        let final_outcome = match self.exchange(&request, &credential, cancellation) {
            #[cfg(test)]
            AdmissionExchange::Entered => {
                match lifecycle.session_entered(attempt_id, clock.now()) {
                    Ok(entered) => CanaryAdmissionOutcome::SessionEntered(entered),
                    Err(failure) => outcome_from_entry_failure(failure),
                }
            }
            AdmissionExchange::Outcome(outcome) => record_outcome(lifecycle, attempt_id, outcome),
        };
        drop(credential);
        self.close();
        final_outcome
    }

    /// Cancel the active lifecycle and close the adapter.
    pub fn cancel(
        &mut self,
        lifecycle: &mut EntryLifecycle,
        attempt_id: GameEntryAttemptId,
    ) -> CanaryAdmissionOutcome {
        let outcome = match lifecycle.cancel(attempt_id) {
            Ok(()) => CanaryAdmissionOutcome::Cancelled,
            Err(failure) => outcome_from_entry_failure(failure),
        };
        self.close();
        outcome
    }

    /// Close the connection and make this adapter terminal.
    pub fn close(&mut self) {
        if let Some(mut transport) = self.transport.take() {
            transport.close();
        }
        self.state = CanaryConnectionState::Closed;
    }

    fn has_admission_implementation(&self) -> bool {
        match &self.mode {
            AdmissionMode::EvidenceBlocked => false,
            #[cfg(test)]
            AdmissionMode::Synthetic(_) => true,
        }
    }

    #[cfg(not(test))]
    fn exchange(
        &mut self,
        _request: &GameEntryRequest,
        _credential: &AdmissionCredential,
        _cancellation: &CancellationToken,
    ) -> AdmissionExchange {
        match &mut self.mode {
            AdmissionMode::EvidenceBlocked => {
                AdmissionExchange::Outcome(CanaryAdmissionOutcome::RealAdmissionUnavailable)
            }
        }
    }

    #[cfg(test)]
    fn exchange(
        &mut self,
        request: &GameEntryRequest,
        credential: &AdmissionCredential,
        cancellation: &CancellationToken,
    ) -> AdmissionExchange {
        match &mut self.mode {
            AdmissionMode::EvidenceBlocked => {
                AdmissionExchange::Outcome(CanaryAdmissionOutcome::RealAdmissionUnavailable)
            }
            AdmissionMode::Synthetic(script) => script.exchange(request, credential, cancellation),
        }
    }

    #[cfg(test)]
    fn with_synthetic(
        transport_config: TransportConfig,
        script: synthetic::SyntheticScript,
    ) -> Self {
        Self {
            state: CanaryConnectionState::Idle,
            transport_config,
            transport: None,
            mode: AdmissionMode::Synthetic(script),
        }
    }
}

impl Debug for CanaryEntryAdapter {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("CanaryEntryAdapter")
            .field("state", &self.state)
            .field("profile", &CURRENT_PROFILE)
            .finish()
    }
}

impl Drop for CanaryEntryAdapter {
    fn drop(&mut self) {
        self.close();
    }
}

fn validate_request(request: &GameEntryRequest) -> Result<(), CanaryAdmissionOutcome> {
    if request.profile() != EntryProfile::CanaryCurrent
        || request.selected_entry().gameplay_channel().is_some()
    {
        return Err(CanaryAdmissionOutcome::ProtocolMismatch);
    }
    let character_name = request.selected_entry().character().name();
    if character_name.is_empty() || character_name.len() > CANARY_CHARACTER_NAME_MAX_BYTES {
        return Err(CanaryAdmissionOutcome::CharacterRejected);
    }
    Ok(())
}

fn record_outcome(
    lifecycle: &mut EntryLifecycle,
    attempt_id: GameEntryAttemptId,
    outcome: CanaryAdmissionOutcome,
) -> CanaryAdmissionOutcome {
    let failure = match outcome.entry_failure() {
        Some(failure) => failure,
        None => return CanaryAdmissionOutcome::InvalidState,
    };
    if lifecycle.record_failure(attempt_id, failure).is_err() {
        CanaryAdmissionOutcome::InvalidState
    } else {
        outcome
    }
}

fn outcome_from_entry_failure(failure: EntryFailure) -> CanaryAdmissionOutcome {
    match failure.kind() {
        EntryFailureKind::CredentialExpired
        | EntryFailureKind::CredentialAlreadyConsumed
        | EntryFailureKind::CredentialRejected => {
            CanaryAdmissionOutcome::CredentialExpiredOrConsumed
        }
        EntryFailureKind::SelectedEntryUnavailable => CanaryAdmissionOutcome::CharacterRejected,
        EntryFailureKind::ProtocolMismatch => CanaryAdmissionOutcome::ProtocolMismatch,
        EntryFailureKind::AssetClientCompatibilityMismatch => {
            CanaryAdmissionOutcome::ClientOrAssetMismatch
        }
        EntryFailureKind::TransportFailure => CanaryAdmissionOutcome::ConnectionLost,
        EntryFailureKind::SafeCancellation => CanaryAdmissionOutcome::Cancelled,
        EntryFailureKind::ServerAdmissionDenied => CanaryAdmissionOutcome::AdmissionDenied,
        EntryFailureKind::StaleAuthenticationTransaction
        | EntryFailureKind::DuplicateCallback
        | EntryFailureKind::AccountSessionExpired
        | EntryFailureKind::DirectoryRevisionStale
        | EntryFailureKind::InvariantViolation => CanaryAdmissionOutcome::InvalidState,
    }
}
