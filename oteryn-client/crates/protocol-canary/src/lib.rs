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

/// Exact read-only Canary revision selected by this evidence cut.
pub const CANARY_CURRENT_REVISION: &str = "95b276db311cf6e9acd58b847f1fb0ca6697b137";
/// Revision at which the accepted W7 protocol source cut was established.
pub const CANARY_ACCEPTED_SOURCE_CUT: &str = "4b2d6f432d92628c42bde1d95daed6ae0d0eb88f";
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

/// Exact non-secret Current-profile source descriptor.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CurrentProfileDescriptor {
    revision: &'static str,
    release: &'static str,
    identifier: &'static str,
    client_version: u16,
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
