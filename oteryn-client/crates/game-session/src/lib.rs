//! Deterministic one-shot game-entry contract and lifecycle for W7.
//!
//! This crate binds one validated directory selection to one short-lived opaque
//! credential and exposes only typed lifecycle transitions. It contains no HTTP,
//! sockets, Canary packet definitions, browser integration or global state.

use oteryn_account_session::AccountSessionId;
use oteryn_foundation::{Deadline, Moment, MonotonicClock};
use oteryn_world_directory::{
    AccountDirectorySnapshot, CharacterId, Compatibility, DirectoryError, DirectoryRevision,
    DirectorySubject, GameplayChannelId, SelectedEntry, WorldId,
};
use std::error::Error;
use std::fmt::{self, Debug, Display, Formatter};
use std::num::NonZeroU64;

/// Maximum opaque credential size accepted by the shared entry contract.
pub const MAX_GAME_ENTRY_CREDENTIAL_BYTES: usize = 4_096;

/// Client-local identity for one complete account-to-game entry attempt.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct GameEntryAttemptId(NonZeroU64);

impl GameEntryAttemptId {
    /// Construct an entry-attempt identity.
    ///
    /// # Errors
    ///
    /// Returns [`GameEntryAttemptIdError::Zero`] when `value` is zero.
    pub fn new(value: u64) -> Result<Self, GameEntryAttemptIdError> {
        NonZeroU64::new(value)
            .map(Self)
            .ok_or(GameEntryAttemptIdError::Zero)
    }

    /// Return the non-zero client-local value.
    #[must_use]
    pub const fn get(self) -> u64 {
        self.0.get()
    }
}

impl TryFrom<u64> for GameEntryAttemptId {
    type Error = GameEntryAttemptIdError;

    fn try_from(value: u64) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl Display for GameEntryAttemptId {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "game-entry-attempt:{}", self.get())
    }
}

/// Stable validation failure for [`GameEntryAttemptId`].
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum GameEntryAttemptIdError {
    /// Zero cannot identify an active entry attempt.
    Zero,
}

impl Display for GameEntryAttemptIdError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("game entry attempt ID must be non-zero")
    }
}

impl Error for GameEntryAttemptIdError {}

/// Closed entry profile supported by the first technical-login contract.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EntryProfile {
    /// Project-owned Canary Current profile for the exact pinned adapter.
    CanaryCurrent,
}

/// One validated request binding an attempt to an exact directory selection.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GameEntryRequest {
    attempt_id: GameEntryAttemptId,
    selected_entry: SelectedEntry,
    profile: EntryProfile,
    requested_at: Moment,
}

impl GameEntryRequest {
    /// Construct a request from an exact validated directory selection.
    #[must_use]
    pub const fn new(
        attempt_id: GameEntryAttemptId,
        selected_entry: SelectedEntry,
        profile: EntryProfile,
        requested_at: Moment,
    ) -> Self {
        Self {
            attempt_id,
            selected_entry,
            profile,
            requested_at,
        }
    }

    /// Return the originating attempt identity.
    #[must_use]
    pub const fn attempt_id(&self) -> GameEntryAttemptId {
        self.attempt_id
    }

    /// Return the exact validated selection.
    #[must_use]
    pub const fn selected_entry(&self) -> &SelectedEntry {
        &self.selected_entry
    }

    /// Return the closed entry profile.
    #[must_use]
    pub const fn profile(&self) -> EntryProfile {
        self.profile
    }

    /// Return the deterministic monotonic request moment.
    #[must_use]
    pub const fn requested_at(&self) -> Moment {
        self.requested_at
    }
}

/// Opaque short-lived one-shot game-entry credential.
///
/// The type intentionally implements neither [`Clone`] nor serialization. Debug
/// and display output are always redacted. The only byte access is the explicit
/// admission-boundary method on [`AdmissionCredential`].
///
/// ```compile_fail
/// use oteryn_foundation::{Deadline, Moment};
/// use oteryn_game_session::GameEntryCredential;
///
/// fn main() -> Result<(), Box<dyn std::error::Error>> {
///     let credential = GameEntryCredential::new(
///         b"synthetic-secret".to_vec(),
///         Deadline::at(Moment::ZERO),
///     )?;
///     let _copy = credential.clone();
///     Ok(())
/// }
/// ```
pub struct GameEntryCredential {
    secret: SecretBytes,
    expires_at: Deadline,
}

impl GameEntryCredential {
    /// Own one non-empty bounded opaque credential and its monotonic expiry.
    ///
    /// # Errors
    ///
    /// Returns a validation error for empty or oversized secret material.
    pub fn new(secret: Vec<u8>, expires_at: Deadline) -> Result<Self, CredentialValidationError> {
        Ok(Self {
            secret: SecretBytes::new(secret)?,
            expires_at,
        })
    }

    /// Return the deterministic monotonic expiry.
    #[must_use]
    pub const fn expires_at(&self) -> Deadline {
        self.expires_at
    }

    /// Return whether the credential has reached its expiry.
    #[must_use]
    pub fn is_expired<C>(&self, clock: &C) -> bool
    where
        C: MonotonicClock + ?Sized,
    {
        self.is_expired_at(clock.now())
    }

    fn is_expired_at(&self, now: Moment) -> bool {
        now >= self.expires_at.moment()
    }

    fn into_admission(self) -> AdmissionCredential {
        AdmissionCredential {
            secret: self.secret,
            expires_at: self.expires_at,
        }
    }
}

impl Debug for GameEntryCredential {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("GameEntryCredential([REDACTED])")
    }
}

impl Display for GameEntryCredential {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("[REDACTED GAME ENTRY CREDENTIAL]")
    }
}

/// Credential moved exactly once into the transport/admission boundary.
///
/// This type is also non-cloneable and redacted. Consumers must call
/// [`Self::expose_secret`] only while constructing the exact authenticated world
/// login and must not persist or format the returned bytes.
pub struct AdmissionCredential {
    secret: SecretBytes,
    expires_at: Deadline,
}

impl AdmissionCredential {
    /// Expose opaque bytes only to the exact admission encoder.
    #[must_use]
    pub fn expose_secret(&self) -> &[u8] {
        self.secret.as_slice()
    }

    /// Return the deterministic monotonic expiry for a final pre-write check.
    #[must_use]
    pub const fn expires_at(&self) -> Deadline {
        self.expires_at
    }

    /// Return whether the moved credential has reached its expiry.
    #[must_use]
    pub fn is_expired<C>(&self, clock: &C) -> bool
    where
        C: MonotonicClock + ?Sized,
    {
        clock.now() >= self.expires_at.moment()
    }
}

impl Debug for AdmissionCredential {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("AdmissionCredential([REDACTED])")
    }
}

impl Display for AdmissionCredential {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter.write_str("[REDACTED ADMISSION CREDENTIAL]")
    }
}

struct SecretBytes(Box<[u8]>);

impl SecretBytes {
    fn new(secret: Vec<u8>) -> Result<Self, CredentialValidationError> {
        if secret.is_empty() {
            return Err(CredentialValidationError::Empty);
        }
        if secret.len() > MAX_GAME_ENTRY_CREDENTIAL_BYTES {
            return Err(CredentialValidationError::TooLarge);
        }
        Ok(Self(secret.into_boxed_slice()))
    }

    fn as_slice(&self) -> &[u8] {
        &self.0
    }

    fn clear(&mut self) {
        self.0.fill(0);
    }
}

impl Drop for SecretBytes {
    fn drop(&mut self) {
        self.clear();
    }
}

/// Stable construction failure for opaque credential material.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CredentialValidationError {
    /// Credential bytes were empty.
    Empty,
    /// Credential bytes exceeded [`MAX_GAME_ENTRY_CREDENTIAL_BYTES`].
    TooLarge,
}

impl Display for CredentialValidationError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Empty => formatter.write_str("game entry credential must not be empty"),
            Self::TooLarge => formatter.write_str("game entry credential exceeds the size limit"),
        }
    }
}

impl Error for CredentialValidationError {}

/// Public deterministic entry lifecycle phases.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EntryPhase {
    /// No authenticated account context exists.
    LoggedOut,
    /// One authentication generation is active.
    Authenticating,
    /// An authenticated account context is ready.
    AccountReady,
    /// One validated authoritative directory generation is ready.
    DirectoryReady,
    /// Entry was explicitly requested for one validated selection.
    EntryRequested,
    /// One fresh credential is owned by the lifecycle.
    CredentialReady,
    /// The credential was moved into the admission boundary.
    Connecting,
    /// Ordered admission completed through the technical entry marker.
    SessionEntered,
    /// One typed recoverable or terminal failure was recorded.
    Failed,
    /// Session resources and secrets are being closed.
    Closing,
}

/// Closed recovery actions exposed to application composition.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RecoveryAction {
    /// Start a new authentication transaction.
    AuthenticateAgain,
    /// Fetch and validate a fresh directory generation.
    RefreshDirectory,
    /// Select a different character.
    ChooseAnotherCharacter,
    /// Select a different world.
    ChooseAnotherWorld,
    /// Select a different gameplay channel.
    ChooseAnotherChannel,
    /// Obtain a newly issued one-shot credential.
    RequestFreshCredential,
    /// Return to the current validated selection surface.
    ReturnToSelection,
    /// Update or repair the client/profile/assets.
    UpdateOrRepair,
    /// Stop the current flow safely.
    Abort,
}

/// Required closed W7 entry failure categories.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum EntryFailureKind {
    /// A completion belongs to an obsolete authentication/entry generation.
    StaleAuthenticationTransaction,
    /// The same browser callback or account-ready completion was delivered twice.
    DuplicateCallback,
    /// The authenticated account context expired or mismatched.
    AccountSessionExpired,
    /// Selection/request used an obsolete directory generation.
    DirectoryRevisionStale,
    /// The selected world, character or channel is absent/unavailable.
    SelectedEntryUnavailable,
    /// The credential reached its deterministic deadline.
    CredentialExpired,
    /// The credential was already moved into admission.
    CredentialAlreadyConsumed,
    /// The exact issuer rejected or burned the credential.
    CredentialRejected,
    /// The configured protocol profile is incompatible.
    ProtocolMismatch,
    /// Client or asset compatibility requires update/repair.
    AssetClientCompatibilityMismatch,
    /// A bounded transport operation failed.
    TransportFailure,
    /// The server denied admission for a non-credential reason.
    ServerAdmissionDenied,
    /// The active flow was cancelled at a safe boundary.
    SafeCancellation,
    /// A lifecycle or contract invariant was violated.
    InvariantViolation,
}

/// Typed stable entry failure with one bounded recommended action.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct EntryFailure {
    kind: EntryFailureKind,
    recommended_action: RecoveryAction,
}

impl EntryFailure {
    /// Construct the deterministic default action for one failure category.
    #[must_use]
    pub const fn for_kind(kind: EntryFailureKind) -> Self {
        let recommended_action = match kind {
            EntryFailureKind::StaleAuthenticationTransaction
            | EntryFailureKind::DuplicateCallback
            | EntryFailureKind::AccountSessionExpired => RecoveryAction::AuthenticateAgain,
            EntryFailureKind::DirectoryRevisionStale => RecoveryAction::RefreshDirectory,
            EntryFailureKind::SelectedEntryUnavailable => RecoveryAction::ReturnToSelection,
            EntryFailureKind::CredentialExpired
            | EntryFailureKind::CredentialAlreadyConsumed
            | EntryFailureKind::CredentialRejected
            | EntryFailureKind::TransportFailure => RecoveryAction::RequestFreshCredential,
            EntryFailureKind::ProtocolMismatch
            | EntryFailureKind::AssetClientCompatibilityMismatch => RecoveryAction::UpdateOrRepair,
            EntryFailureKind::ServerAdmissionDenied => RecoveryAction::ReturnToSelection,
            EntryFailureKind::SafeCancellation | EntryFailureKind::InvariantViolation => {
                RecoveryAction::Abort
            }
        };
        Self {
            kind,
            recommended_action,
        }
    }

    /// Construct selection failure with a subject-specific recovery action.
    #[must_use]
    pub const fn selected_entry_unavailable(subject: DirectorySubject) -> Self {
        let recommended_action = match subject {
            DirectorySubject::World => RecoveryAction::ChooseAnotherWorld,
            DirectorySubject::Character => RecoveryAction::ChooseAnotherCharacter,
            DirectorySubject::GameplayChannel => RecoveryAction::ChooseAnotherChannel,
        };
        Self {
            kind: EntryFailureKind::SelectedEntryUnavailable,
            recommended_action,
        }
    }

    /// Return the stable failure category.
    #[must_use]
    pub const fn kind(self) -> EntryFailureKind {
        self.kind
    }

    /// Return the deterministic application recovery action.
    #[must_use]
    pub const fn recommended_action(self) -> RecoveryAction {
        self.recommended_action
    }
}

impl From<DirectoryError> for EntryFailure {
    fn from(error: DirectoryError) -> Self {
        match error {
            DirectoryError::StaleRevision { .. } | DirectoryError::SelectionNoLongerMatches => {
                Self::for_kind(EntryFailureKind::DirectoryRevisionStale)
            }
            DirectoryError::WorldNotFound(_) => {
                Self::selected_entry_unavailable(DirectorySubject::World)
            }
            DirectoryError::CharacterNotFound(_)
            | DirectoryError::CharacterWorldMismatch { .. } => {
                Self::selected_entry_unavailable(DirectorySubject::Character)
            }
            DirectoryError::GameplayChannelNotFound(_)
            | DirectoryError::ChannelWorldMismatch { .. } => {
                Self::selected_entry_unavailable(DirectorySubject::GameplayChannel)
            }
            DirectoryError::Unavailable { subject, .. } => {
                Self::selected_entry_unavailable(subject)
            }
            DirectoryError::Incompatible {
                subject,
                compatibility,
            } => match compatibility {
                Compatibility::ProtocolMismatch => {
                    Self::for_kind(EntryFailureKind::ProtocolMismatch)
                }
                Compatibility::ClientUpdateRequired | Compatibility::AssetUpdateRequired => {
                    Self::for_kind(EntryFailureKind::AssetClientCompatibilityMismatch)
                }
                Compatibility::Unsupported => Self::selected_entry_unavailable(subject),
                Compatibility::Compatible => Self::for_kind(EntryFailureKind::InvariantViolation),
            },
            DirectoryError::AccountSessionMismatch => {
                Self::for_kind(EntryFailureKind::AccountSessionExpired)
            }
            DirectoryError::Identifier(_)
            | DirectoryError::EmptyText(_)
            | DirectoryError::TextTooLong { .. }
            | DirectoryError::ControlCharacter(_)
            | DirectoryError::SurroundingWhitespace(_)
            | DirectoryError::InvalidHost
            | DirectoryError::InvalidPort
            | DirectoryError::InvalidCharacterLevel
            | DirectoryError::TooManyWorlds
            | DirectoryError::TooManyCharacters
            | DirectoryError::TooManyGameplayChannels
            | DirectoryError::TooManyChannelsForWorld(_)
            | DirectoryError::DuplicateWorldId(_)
            | DirectoryError::DuplicateCharacterId(_)
            | DirectoryError::DuplicateGameplayChannelId(_)
            | DirectoryError::UnknownWorldReference { .. }
            | DirectoryError::ArithmeticOverflow => {
                Self::for_kind(EntryFailureKind::InvariantViolation)
            }
        }
    }
}

impl Display for EntryFailure {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self.kind {
            EntryFailureKind::StaleAuthenticationTransaction => {
                "stale authentication transaction"
            }
            EntryFailureKind::DuplicateCallback => "duplicate authentication callback",
            EntryFailureKind::AccountSessionExpired => "account session expired",
            EntryFailureKind::DirectoryRevisionStale => "directory revision is stale",
            EntryFailureKind::SelectedEntryUnavailable => "selected entry is unavailable",
            EntryFailureKind::CredentialExpired => "game entry credential expired",
            EntryFailureKind::CredentialAlreadyConsumed => {
                "game entry credential was already consumed"
            }
            EntryFailureKind::CredentialRejected => "game entry credential was rejected",
            EntryFailureKind::ProtocolMismatch => "game entry protocol mismatch",
            EntryFailureKind::AssetClientCompatibilityMismatch => {
                "asset or client compatibility mismatch"
            }
            EntryFailureKind::TransportFailure => "game entry transport failure",
            EntryFailureKind::ServerAdmissionDenied => "server admission denied",
            EntryFailureKind::SafeCancellation => "game entry cancelled safely",
            EntryFailureKind::InvariantViolation => "game entry invariant violation",
        };
        formatter.write_str(message)
    }
}

impl Error for EntryFailure {}

/// Non-secret typed proof that ordered technical admission completed.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SessionEntered {
    attempt_id: GameEntryAttemptId,
    account_session_id: AccountSessionId,
    directory_revision: DirectoryRevision,
    character_id: CharacterId,
    world_id: WorldId,
    gameplay_channel_id: Option<GameplayChannelId>,
    profile: EntryProfile,
    entered_at: Moment,
}

impl SessionEntered {
    fn from_request(request: &GameEntryRequest, entered_at: Moment) -> Self {
        Self {
            attempt_id: request.attempt_id(),
            account_session_id: request.selected_entry().account_session_id(),
            directory_revision: request.selected_entry().directory_revision(),
            character_id: request.selected_entry().character().id(),
            world_id: request.selected_entry().world().id(),
            gameplay_channel_id: request
                .selected_entry()
                .gameplay_channel()
                .map(oteryn_world_directory::GameplayChannelSummary::id),
            profile: request.profile(),
            entered_at,
        }
    }

    /// Return the originating entry attempt.
    #[must_use]
    pub const fn attempt_id(self) -> GameEntryAttemptId {
        self.attempt_id
    }

    /// Return the account-session generation.
    #[must_use]
    pub const fn account_session_id(self) -> AccountSessionId {
        self.account_session_id
    }

    /// Return the selected directory generation.
    #[must_use]
    pub const fn directory_revision(self) -> DirectoryRevision {
        self.directory_revision
    }

    /// Return the admitted character identifier.
    #[must_use]
    pub const fn character_id(self) -> CharacterId {
        self.character_id
    }

    /// Return the admitted world identifier.
    #[must_use]
    pub const fn world_id(self) -> WorldId {
        self.world_id
    }

    /// Return the optional admitted gameplay-channel identifier.
    #[must_use]
    pub const fn gameplay_channel_id(self) -> Option<GameplayChannelId> {
        self.gameplay_channel_id
    }

    /// Return the exact entry profile.
    #[must_use]
    pub const fn profile(self) -> EntryProfile {
        self.profile
    }

    /// Return the deterministic monotonic admission moment.
    #[must_use]
    pub const fn entered_at(self) -> Moment {
        self.entered_at
    }
}

/// Deterministic owner of one W7 entry transaction.
///
/// Rejected transitions return [`EntryFailure`] without mutating the current
/// state. Credential ownership is dropped and overwritten on failure, close and
/// every other terminal replacement path.
pub struct EntryLifecycle {
    state: LifecycleState,
}

enum LifecycleState {
    LoggedOut,
    Authenticating {
        attempt_id: GameEntryAttemptId,
    },
    AccountReady {
        attempt_id: GameEntryAttemptId,
        account_session_id: AccountSessionId,
    },
    DirectoryReady {
        attempt_id: GameEntryAttemptId,
        snapshot: Box<AccountDirectorySnapshot>,
    },
    EntryRequested {
        request: Box<GameEntryRequest>,
    },
    CredentialReady {
        request: Box<GameEntryRequest>,
        credential: Option<GameEntryCredential>,
    },
    Connecting {
        request: Box<GameEntryRequest>,
    },
    SessionEntered {
        result: SessionEntered,
    },
    Failed {
        attempt_id: Option<GameEntryAttemptId>,
        failure: EntryFailure,
    },
    Closing,
}

impl EntryLifecycle {
    /// Construct the initial logged-out lifecycle.
    #[must_use]
    pub const fn new() -> Self {
        Self {
            state: LifecycleState::LoggedOut,
        }
    }

    /// Return the current public phase without exposing credential material.
    #[must_use]
    pub const fn phase(&self) -> EntryPhase {
        match self.state {
            LifecycleState::LoggedOut => EntryPhase::LoggedOut,
            LifecycleState::Authenticating { .. } => EntryPhase::Authenticating,
            LifecycleState::AccountReady { .. } => EntryPhase::AccountReady,
            LifecycleState::DirectoryReady { .. } => EntryPhase::DirectoryReady,
            LifecycleState::EntryRequested { .. } => EntryPhase::EntryRequested,
            LifecycleState::CredentialReady { .. } => EntryPhase::CredentialReady,
            LifecycleState::Connecting { .. } => EntryPhase::Connecting,
            LifecycleState::SessionEntered { .. } => EntryPhase::SessionEntered,
            LifecycleState::Failed { .. } => EntryPhase::Failed,
            LifecycleState::Closing => EntryPhase::Closing,
        }
    }

    /// Start one fresh authentication/entry generation.
    ///
    /// # Errors
    ///
    /// Rejects attempts to restart a non-terminal active flow.
    pub fn begin_authentication(
        &mut self,
        attempt_id: GameEntryAttemptId,
    ) -> Result<(), EntryFailure> {
        if !matches!(
            self.state,
            LifecycleState::LoggedOut | LifecycleState::Failed { .. }
        ) {
            return Err(invariant_failure());
        }
        self.state = LifecycleState::Authenticating { attempt_id };
        Ok(())
    }

    /// Accept one authenticated account context for the active generation.
    ///
    /// # Errors
    ///
    /// Rejects stale attempts, duplicate callbacks and invalid phase ordering.
    pub fn account_ready(
        &mut self,
        attempt_id: GameEntryAttemptId,
        account_session_id: AccountSessionId,
    ) -> Result<(), EntryFailure> {
        match &self.state {
            LifecycleState::Authenticating {
                attempt_id: active,
            } if *active == attempt_id => {}
            LifecycleState::Authenticating { .. } => return Err(stale_failure()),
            LifecycleState::AccountReady {
                attempt_id: active,
                ..
            } if *active == attempt_id => {
                return Err(EntryFailure::for_kind(EntryFailureKind::DuplicateCallback));
            }
            _ if self.has_different_attempt(attempt_id) => return Err(stale_failure()),
            _ => return Err(invariant_failure()),
        }
        self.state = LifecycleState::AccountReady {
            attempt_id,
            account_session_id,
        };
        Ok(())
    }

    /// Install one validated directory generation or a strictly newer refresh.
    ///
    /// # Errors
    ///
    /// Rejects stale attempts, account mismatch, non-increasing revisions and
    /// invalid phase ordering without replacing the current snapshot.
    pub fn directory_ready(
        &mut self,
        attempt_id: GameEntryAttemptId,
        snapshot: AccountDirectorySnapshot,
    ) -> Result<(), EntryFailure> {
        match &self.state {
            LifecycleState::AccountReady {
                attempt_id: active,
                account_session_id,
            } if *active == attempt_id => {
                if *account_session_id != snapshot.account_session_id() {
                    return Err(EntryFailure::for_kind(
                        EntryFailureKind::AccountSessionExpired,
                    ));
                }
            }
            LifecycleState::DirectoryReady {
                attempt_id: active,
                snapshot: current,
            } if *active == attempt_id => {
                if current.account_session_id() != snapshot.account_session_id() {
                    return Err(EntryFailure::for_kind(
                        EntryFailureKind::AccountSessionExpired,
                    ));
                }
                if snapshot.revision() <= current.revision() {
                    return Err(EntryFailure::for_kind(
                        EntryFailureKind::DirectoryRevisionStale,
                    ));
                }
            }
            _ if self.has_different_attempt(attempt_id) => return Err(stale_failure()),
            _ => return Err(invariant_failure()),
        }
        self.state = LifecycleState::DirectoryReady {
            attempt_id,
            snapshot: Box::new(snapshot),
        };
        Ok(())
    }

    /// Bind one request to the currently installed directory snapshot.
    ///
    /// # Errors
    ///
    /// Rejects stale attempts/selections and invalid phase ordering without
    /// mutating the installed directory.
    pub fn request_entry(&mut self, request: GameEntryRequest) -> Result<(), EntryFailure> {
        match &self.state {
            LifecycleState::DirectoryReady {
                attempt_id,
                snapshot,
            } if *attempt_id == request.attempt_id() => {
                snapshot.validate_selection(request.selected_entry())?;
            }
            _ if self.has_different_attempt(request.attempt_id()) => return Err(stale_failure()),
            _ => return Err(invariant_failure()),
        }
        self.state = LifecycleState::EntryRequested {
            request: Box::new(request),
        };
        Ok(())
    }

    /// Move one fresh credential into lifecycle ownership.
    ///
    /// # Errors
    ///
    /// Rejects an already expired credential, stale attempt or invalid phase.
    pub fn credential_ready<C>(
        &mut self,
        attempt_id: GameEntryAttemptId,
        credential: GameEntryCredential,
        clock: &C,
    ) -> Result<(), EntryFailure>
    where
        C: MonotonicClock + ?Sized,
    {
        if credential.is_expired(clock) {
            return Err(EntryFailure::for_kind(EntryFailureKind::CredentialExpired));
        }
        let request = match &self.state {
            LifecycleState::EntryRequested { request }
                if request.attempt_id() == attempt_id => request.as_ref().clone(),
            _ if self.has_different_attempt(attempt_id) => return Err(stale_failure()),
            _ => return Err(invariant_failure()),
        };
        self.state = LifecycleState::CredentialReady {
            request: Box::new(request),
            credential: Some(credential),
        };
        Ok(())
    }

    /// Move the credential exactly once into the admission boundary.
    ///
    /// # Errors
    ///
    /// Rejects stale, expired, already consumed or incorrectly ordered handoff.
    /// Rejections do not mutate credential ownership or phase.
    pub fn begin_connecting<C>(
        &mut self,
        attempt_id: GameEntryAttemptId,
        clock: &C,
    ) -> Result<AdmissionCredential, EntryFailure>
    where
        C: MonotonicClock + ?Sized,
    {
        if self.has_different_attempt(attempt_id) {
            return Err(stale_failure());
        }
        let now = clock.now();
        let (request, admission) = match &mut self.state {
            LifecycleState::CredentialReady {
                request,
                credential,
            } => {
                let current = credential.as_ref().ok_or_else(consumed_failure)?;
                if current.is_expired_at(now) {
                    return Err(EntryFailure::for_kind(EntryFailureKind::CredentialExpired));
                }
                let owned = credential.take().ok_or_else(consumed_failure)?;
                (request.clone(), owned.into_admission())
            }
            LifecycleState::Connecting { .. } => return Err(consumed_failure()),
            _ => return Err(invariant_failure()),
        };
        self.state = LifecycleState::Connecting { request };
        Ok(admission)
    }

    /// Record ordered technical admission for the active connection attempt.
    ///
    /// # Errors
    ///
    /// Rejects stale attempts and admission before credential handoff.
    pub fn session_entered(
        &mut self,
        attempt_id: GameEntryAttemptId,
        entered_at: Moment,
    ) -> Result<SessionEntered, EntryFailure> {
        if self.has_different_attempt(attempt_id) {
            return Err(stale_failure());
        }
        let result = match &self.state {
            LifecycleState::Connecting { request } => {
                SessionEntered::from_request(request, entered_at)
            }
            _ => return Err(invariant_failure()),
        };
        self.state = LifecycleState::SessionEntered { result };
        Ok(result)
    }

    /// Record one typed failure and release all state/credential ownership.
    ///
    /// # Errors
    ///
    /// Rejects a stale attempt or failure recording without an active attempt.
    pub fn record_failure(
        &mut self,
        attempt_id: GameEntryAttemptId,
        failure: EntryFailure,
    ) -> Result<(), EntryFailure> {
        match self.active_attempt() {
            Some(active) if active == attempt_id => {}
            Some(_) => return Err(stale_failure()),
            None => return Err(invariant_failure()),
        }
        self.state = LifecycleState::Failed {
            attempt_id: Some(attempt_id),
            failure,
        };
        Ok(())
    }

    /// Cancel the active attempt at a safe boundary.
    ///
    /// # Errors
    ///
    /// Rejects cancellation from a stale or absent attempt.
    pub fn cancel(&mut self, attempt_id: GameEntryAttemptId) -> Result<(), EntryFailure> {
        self.record_failure(
            attempt_id,
            EntryFailure::for_kind(EntryFailureKind::SafeCancellation),
        )
    }

    /// Mark the active account context expired and clear session-scoped state.
    ///
    /// # Errors
    ///
    /// Rejects a stale or absent attempt.
    pub fn account_session_expired(
        &mut self,
        attempt_id: GameEntryAttemptId,
    ) -> Result<(), EntryFailure> {
        self.record_failure(
            attempt_id,
            EntryFailure::for_kind(EntryFailureKind::AccountSessionExpired),
        )
    }

    /// Begin deterministic close and drop every owned session-scoped value.
    pub fn close(&mut self) {
        if !matches!(self.state, LifecycleState::Closing) {
            self.state = LifecycleState::Closing;
        }
    }

    /// Finish close and return to the initial logged-out state.
    ///
    /// # Errors
    ///
    /// Rejects completion before [`Self::close`].
    pub fn finish_closing(&mut self) -> Result<(), EntryFailure> {
        if !matches!(self.state, LifecycleState::Closing) {
            return Err(invariant_failure());
        }
        self.state = LifecycleState::LoggedOut;
        Ok(())
    }

    /// Return the currently recorded failure, when in [`EntryPhase::Failed`].
    #[must_use]
    pub const fn failure(&self) -> Option<EntryFailure> {
        match self.state {
            LifecycleState::Failed { failure, .. } => Some(failure),
            _ => None,
        }
    }

    /// Return the technical admission result, when entered.
    #[must_use]
    pub const fn entered_result(&self) -> Option<SessionEntered> {
        match self.state {
            LifecycleState::SessionEntered { result } => Some(result),
            _ => None,
        }
    }

    /// Return the installed directory while selection is active.
    #[must_use]
    pub fn directory(&self) -> Option<&AccountDirectorySnapshot> {
        match &self.state {
            LifecycleState::DirectoryReady { snapshot, .. } => Some(snapshot),
            _ => None,
        }
    }

    /// Return the active non-secret entry request after selection.
    #[must_use]
    pub fn request(&self) -> Option<&GameEntryRequest> {
        match &self.state {
            LifecycleState::EntryRequested { request }
            | LifecycleState::CredentialReady { request, .. }
            | LifecycleState::Connecting { request } => Some(request),
            _ => None,
        }
    }

    const fn active_attempt(&self) -> Option<GameEntryAttemptId> {
        match &self.state {
            LifecycleState::LoggedOut | LifecycleState::Closing => None,
            LifecycleState::Authenticating { attempt_id }
            | LifecycleState::AccountReady { attempt_id, .. }
            | LifecycleState::DirectoryReady { attempt_id, .. } => Some(*attempt_id),
            LifecycleState::EntryRequested { request }
            | LifecycleState::CredentialReady { request, .. }
            | LifecycleState::Connecting { request } => Some(request.attempt_id()),
            LifecycleState::SessionEntered { result } => Some(result.attempt_id()),
            LifecycleState::Failed { attempt_id, .. } => *attempt_id,
        }
    }

    fn has_different_attempt(&self, attempt_id: GameEntryAttemptId) -> bool {
        self.active_attempt().is_some_and(|active| active != attempt_id)
    }
}

impl Default for EntryLifecycle {
    fn default() -> Self {
        Self::new()
    }
}

impl Debug for EntryLifecycle {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        formatter
            .debug_struct("EntryLifecycle")
            .field("phase", &self.phase())
            .finish()
    }
}

const fn stale_failure() -> EntryFailure {
    EntryFailure::for_kind(EntryFailureKind::StaleAuthenticationTransaction)
}

const fn consumed_failure() -> EntryFailure {
    EntryFailure::for_kind(EntryFailureKind::CredentialAlreadyConsumed)
}

const fn invariant_failure() -> EntryFailure {
    EntryFailure::for_kind(EntryFailureKind::InvariantViolation)
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_foundation::ManualClock;
    use oteryn_world_directory::{
        Availability, CharacterSummary, Compatibility, WorldRoute, WorldSummary,
    };
    use std::time::Duration;

    fn snapshot(revision: u64) -> Result<AccountDirectorySnapshot, Box<dyn Error>> {
        let world_id = WorldId::new(11)?;
        let world = WorldSummary::new(
            world_id,
            "canary".to_owned(),
            "Canary".to_owned(),
            "eu".to_owned(),
            WorldRoute::new("canary.example.test".to_owned(), 7172)?,
            Availability::Available,
            Compatibility::Compatible,
        )?;
        let character = CharacterSummary::new(
            CharacterId::new(22)?,
            world_id,
            "Technical Character".to_owned(),
            42,
            "Knight".to_owned(),
            Availability::Available,
            Compatibility::Compatible,
        )?;
        Ok(AccountDirectorySnapshot::new(
            AccountSessionId::new(33)?,
            DirectoryRevision::new(revision)?,
            vec![world],
            vec![character],
            Vec::new(),
        )?)
    }

    fn request(attempt_id: GameEntryAttemptId) -> Result<GameEntryRequest, Box<dyn Error>> {
        let snapshot = snapshot(1)?;
        let selection = snapshot.select(
            snapshot.revision(),
            CharacterId::new(22)?,
            WorldId::new(11)?,
            None,
        )?;
        Ok(GameEntryRequest::new(
            attempt_id,
            selection,
            EntryProfile::CanaryCurrent,
            Moment::ZERO,
        ))
    }

    fn advance_to_entry_requested(
        lifecycle: &mut EntryLifecycle,
        attempt_id: GameEntryAttemptId,
    ) -> Result<(), Box<dyn Error>> {
        lifecycle.begin_authentication(attempt_id)?;
        lifecycle.account_ready(attempt_id, AccountSessionId::new(33)?)?;
        lifecycle.directory_ready(attempt_id, snapshot(1)?)?;
        lifecycle.request_entry(request(attempt_id)?)?;
        Ok(())
    }

    #[test]
    fn valid_lifecycle_consumes_once_and_enters_session() -> Result<(), Box<dyn Error>> {
        let clock = ManualClock::new(Moment::ZERO);
        let attempt_id = GameEntryAttemptId::new(1)?;
        let mut lifecycle = EntryLifecycle::new();
        advance_to_entry_requested(&mut lifecycle, attempt_id)?;
        let credential = GameEntryCredential::new(
            b"synthetic-one-shot".to_vec(),
            Deadline::after(&clock, Duration::from_secs(5))?,
        )?;
        lifecycle.credential_ready(attempt_id, credential, &clock)?;
        let admission = lifecycle.begin_connecting(attempt_id, &clock)?;

        assert_eq!(admission.expose_secret(), b"synthetic-one-shot");
        assert_eq!(lifecycle.phase(), EntryPhase::Connecting);
        let entered = lifecycle.session_entered(attempt_id, clock.now())?;
        assert_eq!(entered.character_id(), CharacterId::new(22)?);
        assert_eq!(entered.world_id(), WorldId::new(11)?);
        assert_eq!(lifecycle.entered_result(), Some(entered));
        assert_eq!(lifecycle.phase(), EntryPhase::SessionEntered);
        Ok(())
    }

    #[test]
    fn second_handoff_is_rejected_without_state_change() -> Result<(), Box<dyn Error>> {
        let clock = ManualClock::new(Moment::ZERO);
        let attempt_id = GameEntryAttemptId::new(2)?;
        let mut lifecycle = EntryLifecycle::new();
        advance_to_entry_requested(&mut lifecycle, attempt_id)?;
        lifecycle.credential_ready(
            attempt_id,
            GameEntryCredential::new(
                b"single-use".to_vec(),
                Deadline::after(&clock, Duration::from_secs(5))?,
            )?,
            &clock,
        )?;
        let _admission = lifecycle.begin_connecting(attempt_id, &clock)?;
        let before = lifecycle.phase();

        let error = lifecycle.begin_connecting(attempt_id, &clock);
        assert!(matches!(
            error,
            Err(EntryFailure {
                kind: EntryFailureKind::CredentialAlreadyConsumed,
                ..
            })
        ));
        assert_eq!(lifecycle.phase(), before);
        Ok(())
    }

    #[test]
    fn expiry_uses_manual_clock_and_preserves_rejected_state() -> Result<(), Box<dyn Error>> {
        let clock = ManualClock::new(Moment::ZERO);
        let attempt_id = GameEntryAttemptId::new(3)?;
        let mut lifecycle = EntryLifecycle::new();
        advance_to_entry_requested(&mut lifecycle, attempt_id)?;
        lifecycle.credential_ready(
            attempt_id,
            GameEntryCredential::new(
                b"expires".to_vec(),
                Deadline::after(&clock, Duration::from_secs(1))?,
            )?,
            &clock,
        )?;
        clock.advance(Duration::from_secs(1))?;

        assert_eq!(
            lifecycle.begin_connecting(attempt_id, &clock).map(|_| ()),
            Err(EntryFailure::for_kind(EntryFailureKind::CredentialExpired))
        );
        assert_eq!(lifecycle.phase(), EntryPhase::CredentialReady);
        Ok(())
    }

    #[test]
    fn stale_and_duplicate_completions_do_not_mutate_state() -> Result<(), Box<dyn Error>> {
        let active = GameEntryAttemptId::new(4)?;
        let stale = GameEntryAttemptId::new(5)?;
        let mut lifecycle = EntryLifecycle::new();
        lifecycle.begin_authentication(active)?;

        assert_eq!(
            lifecycle.account_ready(stale, AccountSessionId::new(33)?),
            Err(EntryFailure::for_kind(
                EntryFailureKind::StaleAuthenticationTransaction
            ))
        );
        assert_eq!(lifecycle.phase(), EntryPhase::Authenticating);
        lifecycle.account_ready(active, AccountSessionId::new(33)?)?;
        assert_eq!(
            lifecycle.account_ready(active, AccountSessionId::new(33)?),
            Err(EntryFailure::for_kind(EntryFailureKind::DuplicateCallback))
        );
        assert_eq!(lifecycle.phase(), EntryPhase::AccountReady);
        Ok(())
    }

    #[test]
    fn invalid_transition_does_not_mutate_state() -> Result<(), Box<dyn Error>> {
        let mut lifecycle = EntryLifecycle::new();
        let attempt_id = GameEntryAttemptId::new(6)?;

        assert_eq!(
            lifecycle.account_ready(attempt_id, AccountSessionId::new(33)?),
            Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
        );
        assert_eq!(lifecycle.phase(), EntryPhase::LoggedOut);
        Ok(())
    }

    #[test]
    fn stale_directory_refresh_is_rejected_without_replacement() -> Result<(), Box<dyn Error>> {
        let attempt_id = GameEntryAttemptId::new(7)?;
        let mut lifecycle = EntryLifecycle::new();
        lifecycle.begin_authentication(attempt_id)?;
        lifecycle.account_ready(attempt_id, AccountSessionId::new(33)?)?;
        lifecycle.directory_ready(attempt_id, snapshot(2)?)?;

        assert_eq!(
            lifecycle.directory_ready(attempt_id, snapshot(1)?),
            Err(EntryFailure::for_kind(
                EntryFailureKind::DirectoryRevisionStale
            ))
        );
        assert_eq!(
            lifecycle.directory().map(AccountDirectorySnapshot::revision),
            Some(DirectoryRevision::new(2)?)
        );
        Ok(())
    }

    #[test]
    fn cancellation_is_typed_and_terminal_secret_output_is_redacted(
    ) -> Result<(), Box<dyn Error>> {
        let clock = ManualClock::new(Moment::ZERO);
        let attempt_id = GameEntryAttemptId::new(8)?;
        let mut lifecycle = EntryLifecycle::new();
        advance_to_entry_requested(&mut lifecycle, attempt_id)?;
        let secret = "never-log-this-value";
        let credential = GameEntryCredential::new(
            secret.as_bytes().to_vec(),
            Deadline::after(&clock, Duration::from_secs(5))?,
        )?;
        assert!(!format!("{credential:?}").contains(secret));
        assert!(!credential.to_string().contains(secret));
        lifecycle.credential_ready(attempt_id, credential, &clock)?;
        assert!(!format!("{lifecycle:?}").contains(secret));

        lifecycle.cancel(attempt_id)?;
        assert_eq!(lifecycle.phase(), EntryPhase::Failed);
        assert_eq!(
            lifecycle.failure(),
            Some(EntryFailure::for_kind(EntryFailureKind::SafeCancellation))
        );
        assert_eq!(
            lifecycle.failure().map(EntryFailure::recommended_action),
            Some(RecoveryAction::Abort)
        );
        assert!(!format!("{lifecycle:?}").contains(secret));
        Ok(())
    }

    #[test]
    fn admission_formatting_is_redacted() -> Result<(), Box<dyn Error>> {
        let clock = ManualClock::new(Moment::ZERO);
        let credential = GameEntryCredential::new(
            b"admission-secret".to_vec(),
            Deadline::after(&clock, Duration::from_secs(2))?,
        )?;
        let admission = credential.into_admission();

        assert_eq!(format!("{admission:?}"), "AdmissionCredential([REDACTED])");
        assert_eq!(
            admission.to_string(),
            "[REDACTED ADMISSION CREDENTIAL]"
        );
        assert!(!format!("{admission:?}").contains("admission-secret"));
        Ok(())
    }

    #[test]
    fn secret_storage_overwrite_is_explicit() -> Result<(), CredentialValidationError> {
        let mut secret = SecretBytes::new(b"erase-me".to_vec())?;
        secret.clear();
        assert!(secret.as_slice().iter().all(|byte| *byte == 0));
        Ok(())
    }

    #[test]
    fn close_is_idempotent_and_finish_is_ordered() -> Result<(), Box<dyn Error>> {
        let mut lifecycle = EntryLifecycle::new();
        assert_eq!(
            lifecycle.finish_closing(),
            Err(EntryFailure::for_kind(EntryFailureKind::InvariantViolation))
        );
        lifecycle.close();
        lifecycle.close();
        assert_eq!(lifecycle.phase(), EntryPhase::Closing);
        lifecycle.finish_closing()?;
        assert_eq!(lifecycle.phase(), EntryPhase::LoggedOut);
        Ok(())
    }
}
