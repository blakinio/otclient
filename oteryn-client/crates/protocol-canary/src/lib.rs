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
use std::fmt::{self, Debug, Formatter};

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
            Self::CredentialExpiredOrConsumed => Some(EntryFailure::for_kind(
                EntryFailureKind::CredentialRejected,
            )),
            Self::CharacterRejected => Some(EntryFailure::selected_entry_unavailable(
                DirectorySubject::Character,
            )),
            Self::ProtocolMismatch | Self::RealAdmissionUnavailable => Some(
                EntryFailure::for_kind(EntryFailureKind::ProtocolMismatch),
            ),
            Self::ClientOrAssetMismatch => Some(EntryFailure::for_kind(
                EntryFailureKind::AssetClientCompatibilityMismatch,
            )),
            Self::ConnectionLost => Some(EntryFailure::for_kind(
                EntryFailureKind::TransportFailure,
            )),
            Self::Cancelled => Some(EntryFailure::for_kind(
                EntryFailureKind::SafeCancellation,
            )),
            Self::InvalidState => Some(EntryFailure::for_kind(
                EntryFailureKind::InvariantViolation,
            )),
        }
    }
}

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
    Synthetic(SyntheticScript),
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

        match self.mode {
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
            let outcome = record_outcome(
                lifecycle,
                attempt_id,
                CanaryAdmissionOutcome::Cancelled,
            );
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

        let outcome = self.exchange(request, credential, cancellation);
        let final_outcome = match outcome {
            CanaryAdmissionOutcome::SessionEntered(_) => {
                match lifecycle.session_entered(attempt_id, clock.now()) {
                    Ok(entered) => CanaryAdmissionOutcome::SessionEntered(entered),
                    Err(failure) => outcome_from_entry_failure(failure),
                }
            }
            failure => record_outcome(lifecycle, attempt_id, failure),
        };
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
        match self.mode {
            AdmissionMode::EvidenceBlocked => false,
            #[cfg(test)]
            AdmissionMode::Synthetic(_) => true,
        }
    }

    fn exchange(
        &mut self,
        request: GameEntryRequest,
        credential: AdmissionCredential,
        cancellation: &CancellationToken,
    ) -> CanaryAdmissionOutcome {
        match &mut self.mode {
            AdmissionMode::EvidenceBlocked => CanaryAdmissionOutcome::RealAdmissionUnavailable,
            #[cfg(test)]
            AdmissionMode::Synthetic(script) => {
                script.exchange(&request, &credential, cancellation)
            }
        }
    }

    #[cfg(test)]
    fn with_synthetic(transport_config: TransportConfig, script: SyntheticScript) -> Self {
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
        EntryFailureKind::CredentialExpired | EntryFailureKind::CredentialAlreadyConsumed => {
            CanaryAdmissionOutcome::CredentialExpiredOrConsumed
        }
        EntryFailureKind::CredentialRejected => {
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

#[cfg(test)]
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum SyntheticDecision {
    Entered,
    AdmissionDenied,
    CredentialExpiredOrConsumed,
    CharacterRejected,
    ProtocolMismatch,
    ClientOrAssetMismatch,
    ConnectionLost,
}

#[cfg(test)]
struct SyntheticScript {
    expected_character: String,
    expected_credential: Vec<u8>,
    decision: SyntheticDecision,
    network_attempts: std::sync::Arc<std::sync::atomic::AtomicUsize>,
}

#[cfg(test)]
impl SyntheticScript {
    fn exchange(
        &mut self,
        request: &GameEntryRequest,
        credential: &AdmissionCredential,
        cancellation: &CancellationToken,
    ) -> CanaryAdmissionOutcome {
        use std::sync::atomic::Ordering;

        self.network_attempts.fetch_add(1, Ordering::SeqCst);
        if cancellation.is_cancelled() {
            return CanaryAdmissionOutcome::Cancelled;
        }
        if request.selected_entry().character().name() != self.expected_character {
            return CanaryAdmissionOutcome::CharacterRejected;
        }
        if credential.expose_secret() != self.expected_credential {
            return CanaryAdmissionOutcome::CredentialExpiredOrConsumed;
        }
        match self.decision {
            SyntheticDecision::Entered => placeholder_success_outcome(),
            SyntheticDecision::AdmissionDenied => CanaryAdmissionOutcome::AdmissionDenied,
            SyntheticDecision::CredentialExpiredOrConsumed => {
                CanaryAdmissionOutcome::CredentialExpiredOrConsumed
            }
            SyntheticDecision::CharacterRejected => CanaryAdmissionOutcome::CharacterRejected,
            SyntheticDecision::ProtocolMismatch => CanaryAdmissionOutcome::ProtocolMismatch,
            SyntheticDecision::ClientOrAssetMismatch => {
                CanaryAdmissionOutcome::ClientOrAssetMismatch
            }
            SyntheticDecision::ConnectionLost => CanaryAdmissionOutcome::ConnectionLost,
        }
    }
}

#[cfg(test)]
fn placeholder_success_outcome() -> CanaryAdmissionOutcome {
    // The shared SessionEntered constructor is intentionally lifecycle-private.
    // This sentinel is replaced by EntryLifecycle::session_entered immediately
    // after the synthetic exchange returns.
    CanaryAdmissionOutcome::AdmissionDenied
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_account_session::AccountSessionId;
    use oteryn_foundation::{CancellationSource, Deadline, ManualClock, Moment};
    use oteryn_game_session::{EntryPhase, GameEntryCredential};
    use oteryn_protocol_core::{
        BoundedReader, BoundedWriter, ProtocolError, ProtocolErrorKind, TrailingDataPolicy,
    };
    use oteryn_world_directory::{
        AccountDirectorySnapshot, Availability, CharacterId, CharacterSummary, Compatibility,
        DirectoryRevision, WorldId, WorldRoute, WorldSummary,
    };
    use std::error::Error;
    use std::sync::Arc;
    use std::sync::atomic::{AtomicUsize, Ordering};
    use std::time::Duration;

    const SYNTHETIC_CHALLENGE: u8 = 1;
    const SYNTHETIC_ACCEPTED: u8 = 2;
    const SYNTHETIC_PENDING: u8 = 3;
    const SYNTHETIC_ENTERED: u8 = 4;
    const SYNTHETIC_DENIED: u8 = 5;

    fn transport_config() -> Result<TransportConfig, Box<dyn Error>> {
        Ok(TransportConfig::new(
            Duration::from_secs(1),
            Duration::from_secs(1),
            Duration::from_secs(1),
            1024,
            1024,
        )?)
    }

    fn lifecycle_with_credential(
        character_name: &str,
        lifetime: Duration,
    ) -> Result<(EntryLifecycle, GameEntryAttemptId, ManualClock), Box<dyn Error>> {
        let clock = ManualClock::new(Moment::ZERO);
        let attempt_id = GameEntryAttemptId::new(1)?;
        let account_session_id = AccountSessionId::new(2)?;
        let world_id = WorldId::new(3)?;
        let character_id = CharacterId::new(4)?;
        let world = WorldSummary::new(
            world_id,
            "synthetic".to_owned(),
            "Synthetic".to_owned(),
            "test".to_owned(),
            WorldRoute::new("127.0.0.1".to_owned(), 7172)?,
            Availability::Available,
            Compatibility::Compatible,
        )?;
        let character = CharacterSummary::new(
            character_id,
            world_id,
            character_name.to_owned(),
            1,
            "None".to_owned(),
            Availability::Available,
            Compatibility::Compatible,
        )?;
        let snapshot = AccountDirectorySnapshot::new(
            account_session_id,
            DirectoryRevision::new(1)?,
            vec![world],
            vec![character],
            Vec::new(),
        )?;
        let selection = snapshot.select(snapshot.revision(), character_id, world_id, None)?;
        let request = GameEntryRequest::new(
            attempt_id,
            selection,
            EntryProfile::CanaryCurrent,
            clock.now(),
        );

        let mut lifecycle = EntryLifecycle::new();
        lifecycle.begin_authentication(attempt_id)?;
        lifecycle.account_ready(attempt_id, account_session_id)?;
        lifecycle.directory_ready(attempt_id, snapshot)?;
        lifecycle.request_entry(request)?;
        lifecycle.credential_ready(
            attempt_id,
            GameEntryCredential::new(
                b"original-synthetic-credential".to_vec(),
                Deadline::after(&clock, lifetime)?,
            )?,
            &clock,
        )?;
        Ok((lifecycle, attempt_id, clock))
    }

    fn script(
        expected_character: &str,
        decision: SyntheticDecision,
        attempts: Arc<AtomicUsize>,
    ) -> SyntheticScript {
        SyntheticScript {
            expected_character: expected_character.to_owned(),
            expected_credential: b"original-synthetic-credential".to_vec(),
            decision,
            network_attempts: attempts,
        }
    }

    #[test]
    fn exact_profile_metadata_and_unknown_profile_are_closed() {
        assert_eq!(CURRENT_PROFILE.revision(), CANARY_CURRENT_REVISION);
        assert_eq!(CURRENT_PROFILE.release(), "3.6.1");
        assert_eq!(CURRENT_PROFILE.client_version(), 1525);
        assert_eq!(CURRENT_PROFILE.max_network_message_bytes(), 65_500);
        assert_eq!(CURRENT_PROFILE.max_input_message_bytes(), 4_096);
        assert_eq!(CURRENT_PROFILE.max_character_name_bytes(), 30);
        assert_eq!(select_profile("current"), Ok(CURRENT_PROFILE));
        assert_eq!(
            select_profile("unknown"),
            Err(CanaryAdmissionOutcome::ProtocolMismatch)
        );
    }

    #[test]
    fn real_admission_is_blocked_before_network_or_credential_use() -> Result<(), Box<dyn Error>> {
        let (lifecycle, _attempt_id, _clock) =
            lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
        let request = lifecycle
            .request()
            .ok_or("missing synthetic request")?;
        let source = CancellationSource::new();
        let mut adapter = CanaryEntryAdapter::new(transport_config()?);
        assert_eq!(
            adapter.connect(request, &source.token()),
            Err(CanaryAdmissionOutcome::RealAdmissionUnavailable)
        );
        assert_eq!(adapter.state(), CanaryConnectionState::Idle);
        assert_eq!(lifecycle.phase(), EntryPhase::CredentialReady);
        Ok(())
    }

    #[test]
    fn successful_synthetic_admission_returns_shared_session_entered() -> Result<(), Box<dyn Error>> {
        let (mut lifecycle, attempt_id, clock) =
            lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
        let attempts = Arc::new(AtomicUsize::new(0));
        let mut adapter = CanaryEntryAdapter::with_synthetic(
            transport_config()?,
            script(
                "Synthetic Character",
                SyntheticDecision::Entered,
                Arc::clone(&attempts),
            ),
        );
        let source = CancellationSource::new();
        let request = lifecycle
            .request()
            .ok_or("missing synthetic request")?
            .clone();
        adapter.connect(&request, &source.token())?;
        let outcome = adapter.enter_session(&mut lifecycle, attempt_id, &clock, &source.token());
        let CanaryAdmissionOutcome::SessionEntered(entered) = outcome else {
            return Err("synthetic admission did not enter session".into());
        };
        assert_eq!(entered.character_id(), CharacterId::new(4)?);
        assert_eq!(attempts.load(Ordering::SeqCst), 1);
        assert_eq!(adapter.state(), CanaryConnectionState::Closed);
        assert_eq!(lifecycle.phase(), EntryPhase::SessionEntered);
        Ok(())
    }

    #[test]
    fn wrong_character_and_server_denials_are_typed() -> Result<(), Box<dyn Error>> {
        for (decision, expected) in [
            (
                SyntheticDecision::CharacterRejected,
                CanaryAdmissionOutcome::CharacterRejected,
            ),
            (
                SyntheticDecision::AdmissionDenied,
                CanaryAdmissionOutcome::AdmissionDenied,
            ),
            (
                SyntheticDecision::CredentialExpiredOrConsumed,
                CanaryAdmissionOutcome::CredentialExpiredOrConsumed,
            ),
            (
                SyntheticDecision::ProtocolMismatch,
                CanaryAdmissionOutcome::ProtocolMismatch,
            ),
            (
                SyntheticDecision::ClientOrAssetMismatch,
                CanaryAdmissionOutcome::ClientOrAssetMismatch,
            ),
            (
                SyntheticDecision::ConnectionLost,
                CanaryAdmissionOutcome::ConnectionLost,
            ),
        ] {
            let (mut lifecycle, attempt_id, clock) =
                lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
            let attempts = Arc::new(AtomicUsize::new(0));
            let mut adapter = CanaryEntryAdapter::with_synthetic(
                transport_config()?,
                script("Synthetic Character", decision, Arc::clone(&attempts)),
            );
            let source = CancellationSource::new();
            let request = lifecycle
                .request()
                .ok_or("missing synthetic request")?
                .clone();
            adapter.connect(&request, &source.token())?;
            assert_eq!(
                adapter.enter_session(&mut lifecycle, attempt_id, &clock, &source.token()),
                expected
            );
            assert_eq!(attempts.load(Ordering::SeqCst), 1);
            assert_eq!(lifecycle.phase(), EntryPhase::Failed);
        }
        Ok(())
    }

    #[test]
    fn wrong_expected_character_is_rejected_without_secret_text() -> Result<(), Box<dyn Error>> {
        let (mut lifecycle, attempt_id, clock) =
            lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
        let attempts = Arc::new(AtomicUsize::new(0));
        let mut adapter = CanaryEntryAdapter::with_synthetic(
            transport_config()?,
            script(
                "Different Character",
                SyntheticDecision::Entered,
                Arc::clone(&attempts),
            ),
        );
        let source = CancellationSource::new();
        let request = lifecycle
            .request()
            .ok_or("missing synthetic request")?
            .clone();
        adapter.connect(&request, &source.token())?;
        assert_eq!(
            adapter.enter_session(&mut lifecycle, attempt_id, &clock, &source.token()),
            CanaryAdmissionOutcome::CharacterRejected
        );
        assert!(!format!("{:?}", adapter).contains("original-synthetic-credential"));
        Ok(())
    }

    #[test]
    fn expired_and_consumed_credentials_fail_before_network_attempt() -> Result<(), Box<dyn Error>> {
        let (mut expired, expired_attempt, expired_clock) =
            lifecycle_with_credential("Synthetic Character", Duration::from_secs(1))?;
        expired_clock.advance(Duration::from_secs(1))?;
        let expired_attempts = Arc::new(AtomicUsize::new(0));
        let mut expired_adapter = CanaryEntryAdapter::with_synthetic(
            transport_config()?,
            script(
                "Synthetic Character",
                SyntheticDecision::Entered,
                Arc::clone(&expired_attempts),
            ),
        );
        let source = CancellationSource::new();
        let request = expired
            .request()
            .ok_or("missing expired request")?
            .clone();
        expired_adapter.connect(&request, &source.token())?;
        assert_eq!(
            expired_adapter.enter_session(
                &mut expired,
                expired_attempt,
                &expired_clock,
                &source.token(),
            ),
            CanaryAdmissionOutcome::CredentialExpiredOrConsumed
        );
        assert_eq!(expired_attempts.load(Ordering::SeqCst), 0);

        let (mut consumed, consumed_attempt, consumed_clock) =
            lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
        let moved = consumed.begin_connecting(consumed_attempt, &consumed_clock)?;
        drop(moved);
        let consumed_attempts = Arc::new(AtomicUsize::new(0));
        let mut consumed_adapter = CanaryEntryAdapter::with_synthetic(
            transport_config()?,
            script(
                "Synthetic Character",
                SyntheticDecision::Entered,
                Arc::clone(&consumed_attempts),
            ),
        );
        let request = consumed
            .request()
            .ok_or("missing consumed request")?
            .clone();
        consumed_adapter.connect(&request, &source.token())?;
        assert_eq!(
            consumed_adapter.enter_session(
                &mut consumed,
                consumed_attempt,
                &consumed_clock,
                &source.token(),
            ),
            CanaryAdmissionOutcome::CredentialExpiredOrConsumed
        );
        assert_eq!(consumed_attempts.load(Ordering::SeqCst), 0);
        Ok(())
    }

    #[test]
    fn cancellation_is_terminal_and_precedes_handoff() -> Result<(), Box<dyn Error>> {
        let (mut lifecycle, attempt_id, clock) =
            lifecycle_with_credential("Synthetic Character", Duration::from_secs(5))?;
        let attempts = Arc::new(AtomicUsize::new(0));
        let mut adapter = CanaryEntryAdapter::with_synthetic(
            transport_config()?,
            script(
                "Synthetic Character",
                SyntheticDecision::Entered,
                Arc::clone(&attempts),
            ),
        );
        let source = CancellationSource::new();
        let request = lifecycle
            .request()
            .ok_or("missing synthetic request")?
            .clone();
        adapter.connect(&request, &source.token())?;
        assert!(source.cancel());
        assert_eq!(
            adapter.enter_session(&mut lifecycle, attempt_id, &clock, &source.token()),
            CanaryAdmissionOutcome::Cancelled
        );
        assert_eq!(attempts.load(Ordering::SeqCst), 0);
        assert_eq!(adapter.state(), CanaryConnectionState::Closed);
        Ok(())
    }

    #[test]
    fn synthetic_transcript_accepts_only_ordered_bounded_entry() -> Result<(), ProtocolError> {
        let transcript = synthetic_success_transcript()?;
        assert_eq!(
            parse_synthetic_transcript(&transcript, 64),
            Ok(SyntheticDecision::Entered)
        );

        let mut reordered = BoundedWriter::new(64)?;
        write_synthetic_frame(&mut reordered, SYNTHETIC_ACCEPTED, None)?;
        write_synthetic_frame(&mut reordered, SYNTHETIC_CHALLENGE, None)?;
        assert_eq!(
            parse_synthetic_transcript(&reordered.into_inner(), 64),
            Err(ProtocolError::new(ProtocolErrorKind::UnknownValue))
        );
        Ok(())
    }

    #[test]
    fn synthetic_transcript_rejects_malformed_truncated_oversized_and_invalid_text(
    ) -> Result<(), ProtocolError> {
        assert_eq!(
            parse_synthetic_transcript(&[5, 0, SYNTHETIC_CHALLENGE], 64),
            Err(ProtocolError::new(ProtocolErrorKind::Truncated))
        );
        assert_eq!(
            parse_synthetic_transcript(&[65, 0], 64),
            Err(ProtocolError::new(ProtocolErrorKind::Oversized))
        );
        let invalid_text = [4_u8, 0, SYNTHETIC_DENIED, 1, 0, 0xFF];
        assert_eq!(
            parse_synthetic_transcript(&invalid_text, 64),
            Err(ProtocolError::new(ProtocolErrorKind::InvalidUtf8))
        );
        Ok(())
    }

    #[test]
    fn arbitrary_bounded_synthetic_transcripts_never_panic_and_are_deterministic() {
        for length in 0..=256 {
            let bytes = vec![length as u8; length];
            let first = parse_synthetic_transcript(&bytes, 256);
            let second = parse_synthetic_transcript(&bytes, 256);
            assert_eq!(first, second);
        }
    }

    fn synthetic_success_transcript() -> Result<Vec<u8>, ProtocolError> {
        let mut writer = BoundedWriter::new(64)?;
        write_synthetic_frame(&mut writer, SYNTHETIC_CHALLENGE, None)?;
        write_synthetic_frame(&mut writer, SYNTHETIC_ACCEPTED, None)?;
        write_synthetic_frame(&mut writer, SYNTHETIC_PENDING, None)?;
        write_synthetic_frame(&mut writer, SYNTHETIC_ENTERED, None)?;
        Ok(writer.into_inner())
    }

    fn write_synthetic_frame(
        transcript: &mut BoundedWriter,
        tag: u8,
        detail: Option<&str>,
    ) -> Result<(), ProtocolError> {
        let mut payload = BoundedWriter::new(32)?;
        payload.write_u8(tag)?;
        if let Some(detail) = detail {
            payload.write_u16_string(detail, 16)?;
        }
        let payload = payload.into_inner();
        transcript.write_u16_le(
            u16::try_from(payload.len())
                .map_err(|_| ProtocolError::new(ProtocolErrorKind::InvalidLength))?,
        )?;
        transcript.write_bytes(&payload)
    }

    fn parse_synthetic_transcript(
        bytes: &[u8],
        max_frame_bytes: usize,
    ) -> Result<SyntheticDecision, ProtocolError> {
        let mut transcript = BoundedReader::new(bytes, 256)?;
        let expected = [
            SYNTHETIC_CHALLENGE,
            SYNTHETIC_ACCEPTED,
            SYNTHETIC_PENDING,
            SYNTHETIC_ENTERED,
        ];
        let mut index = 0;

        while !transcript.is_empty() {
            let frame_length = usize::from(transcript.read_u16_le()?);
            if frame_length == 0 {
                return Err(ProtocolError::new(ProtocolErrorKind::InvalidLength));
            }
            if frame_length > max_frame_bytes {
                return Err(ProtocolError::new(ProtocolErrorKind::Oversized));
            }
            let frame_bytes = transcript.read_exact(frame_length)?;
            let mut frame = BoundedReader::new(frame_bytes, max_frame_bytes)?;
            let tag = frame.read_u8()?;
            if tag == SYNTHETIC_DENIED {
                let _detail = frame.read_u16_string(16)?;
                frame.finish(TrailingDataPolicy::Reject)?;
                return Ok(SyntheticDecision::AdmissionDenied);
            }
            if index >= expected.len() || tag != expected[index] {
                return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue));
            }
            frame.finish(TrailingDataPolicy::Reject)?;
            index += 1;
        }

        transcript.finish(TrailingDataPolicy::Reject)?;
        if index == expected.len() {
            Ok(SyntheticDecision::Entered)
        } else {
            Err(ProtocolError::new(ProtocolErrorKind::Truncated))
        }
    }
}
