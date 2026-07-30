//! Bounded authoritative world, character and gameplay-channel directory contracts.
//!
//! The W7 Gateway adapter converts validated protocol data into these types.
//! Display names are never used as routing keys, every collection is bounded,
//! and [`AccountDirectorySnapshot`] stores records in deterministic identifier
//! order. The crate performs no HTTP, persistence or network access.

use oteryn_account_session::AccountSessionId;
use std::collections::BTreeMap;
use std::error::Error;
use std::fmt::{self, Display, Formatter};
use std::num::{NonZeroU16, NonZeroU64};

/// Maximum authoritative worlds accepted in one account directory.
pub const MAX_WORLDS: usize = 64;
/// Maximum authoritative characters accepted in one account directory.
pub const MAX_CHARACTERS: usize = 128;
/// Maximum gameplay channels accepted across one account directory.
pub const MAX_GAMEPLAY_CHANNELS: usize = 256;
/// Maximum gameplay channels accepted for one world.
pub const MAX_CHANNELS_PER_WORLD: usize = 32;
/// Maximum UTF-8 byte length of a world slug.
pub const MAX_WORLD_SLUG_BYTES: usize = 64;
/// Maximum UTF-8 byte length of a display name.
pub const MAX_DISPLAY_NAME_BYTES: usize = 64;
/// Maximum UTF-8 byte length of a region label.
pub const MAX_REGION_BYTES: usize = 64;
/// Maximum UTF-8 byte length of an authoritative route host.
pub const MAX_HOST_BYTES: usize = 253;
/// Maximum UTF-8 byte length of a vocation label.
pub const MAX_VOCATION_BYTES: usize = 64;
/// Maximum UTF-8 byte length of a gameplay-channel label.
pub const MAX_CHANNEL_LABEL_BYTES: usize = 64;

/// Positive signed-64-compatible authoritative character identifier.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct CharacterId(i64);

impl CharacterId {
    /// Construct an authoritative character identifier.
    ///
    /// # Errors
    ///
    /// Returns an identifier error when `value` is not positive.
    pub const fn new(value: i64) -> Result<Self, IdentifierError> {
        if value > 0 {
            Ok(Self(value))
        } else {
            Err(IdentifierError::new(IdentifierKind::Character))
        }
    }

    /// Return the exact signed 64-bit Gateway value.
    #[must_use]
    pub const fn get(self) -> i64 {
        self.0
    }
}

impl TryFrom<i64> for CharacterId {
    type Error = IdentifierError;

    fn try_from(value: i64) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl Display for CharacterId {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "character:{}", self.get())
    }
}

/// Positive signed-64-compatible authoritative world identifier.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct WorldId(i64);

impl WorldId {
    /// Construct an authoritative world identifier.
    ///
    /// # Errors
    ///
    /// Returns an identifier error when `value` is not positive.
    pub const fn new(value: i64) -> Result<Self, IdentifierError> {
        if value > 0 {
            Ok(Self(value))
        } else {
            Err(IdentifierError::new(IdentifierKind::World))
        }
    }

    /// Return the exact signed 64-bit Gateway value.
    #[must_use]
    pub const fn get(self) -> i64 {
        self.0
    }
}

impl TryFrom<i64> for WorldId {
    type Error = IdentifierError;

    fn try_from(value: i64) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl Display for WorldId {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "world:{}", self.get())
    }
}

/// Reserved positive signed-64-compatible gameplay-channel identifier.
///
/// Gateway protocol v1 does not populate this identifier. It remains an opaque,
/// unserialized optional selection component for later exact producer contracts.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct GameplayChannelId(i64);

impl GameplayChannelId {
    /// Construct an opaque gameplay-channel identifier.
    ///
    /// # Errors
    ///
    /// Returns an identifier error when `value` is not positive.
    pub const fn new(value: i64) -> Result<Self, IdentifierError> {
        if value > 0 {
            Ok(Self(value))
        } else {
            Err(IdentifierError::new(IdentifierKind::GameplayChannel))
        }
    }

    /// Return the positive opaque numeric value.
    #[must_use]
    pub const fn get(self) -> i64 {
        self.0
    }
}

impl TryFrom<i64> for GameplayChannelId {
    type Error = IdentifierError;

    fn try_from(value: i64) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl Display for GameplayChannelId {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "gameplay-channel:{}", self.get())
    }
}

/// Client-local generation of one validated authoritative directory response.
///
/// Gateway protocol v1 has no server directory revision. This value is allocated
/// locally and is always interpreted together with [`AccountSessionId`].
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct DirectoryRevision(NonZeroU64);

impl DirectoryRevision {
    /// Construct a client-local directory generation.
    ///
    /// # Errors
    ///
    /// Returns an identifier error when `value` is zero.
    pub fn new(value: u64) -> Result<Self, IdentifierError> {
        NonZeroU64::new(value)
            .map(Self)
            .ok_or(IdentifierError::new(IdentifierKind::DirectoryRevision))
    }

    /// Return the non-zero client-local generation value.
    #[must_use]
    pub const fn get(self) -> u64 {
        self.0.get()
    }
}

impl TryFrom<u64> for DirectoryRevision {
    type Error = IdentifierError;

    fn try_from(value: u64) -> Result<Self, Self::Error> {
        Self::new(value)
    }
}

impl Display for DirectoryRevision {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        write!(formatter, "directory-revision:{}", self.get())
    }
}

/// Identifier category used by stable validation diagnostics.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IdentifierKind {
    /// Character identifier.
    Character,
    /// World identifier.
    World,
    /// Gameplay-channel identifier.
    GameplayChannel,
    /// Client-local directory revision.
    DirectoryRevision,
}

/// Stable validation failure for one directory identifier.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct IdentifierError {
    kind: IdentifierKind,
}

impl IdentifierError {
    const fn new(kind: IdentifierKind) -> Self {
        Self { kind }
    }

    /// Return the rejected identifier category.
    #[must_use]
    pub const fn kind(self) -> IdentifierKind {
        self.kind
    }
}

impl Display for IdentifierError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self.kind {
            IdentifierKind::Character => "character ID must be a positive signed 64-bit value",
            IdentifierKind::World => "world ID must be a positive signed 64-bit value",
            IdentifierKind::GameplayChannel => {
                "gameplay channel ID must be a positive signed 64-bit value"
            }
            IdentifierKind::DirectoryRevision => "directory revision must be non-zero",
        };
        formatter.write_str(message)
    }
}

impl Error for IdentifierError {}

/// Closed availability states used for selection control flow.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Availability {
    /// The entry may currently be selected.
    Available,
    /// Capacity is currently exhausted.
    Full,
    /// The entry is under maintenance.
    Maintenance,
    /// The entry is offline.
    Offline,
    /// The authenticated account is not allowed to select the entry.
    Restricted,
}

impl Availability {
    /// Return whether selection may proceed.
    #[must_use]
    pub const fn is_available(self) -> bool {
        matches!(self, Self::Available)
    }
}

/// Closed client compatibility states used for selection control flow.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Compatibility {
    /// The entry matches the current client contract.
    Compatible,
    /// The configured protocol contract does not match.
    ProtocolMismatch,
    /// A newer or repaired client is required.
    ClientUpdateRequired,
    /// Required client assets are incompatible or unavailable.
    AssetUpdateRequired,
    /// The entry is outside the bounded supported contract.
    Unsupported,
}

impl Compatibility {
    /// Return whether entry may proceed without repair or a contract change.
    #[must_use]
    pub const fn is_compatible(self) -> bool {
        matches!(self, Self::Compatible)
    }
}

/// Directory record category associated with a typed validation failure.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DirectorySubject {
    /// A world record.
    World,
    /// A character record.
    Character,
    /// A gameplay-channel record.
    GameplayChannel,
}

/// Bounded text field associated with a typed validation failure.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum TextField {
    /// World slug.
    WorldSlug,
    /// World display name.
    WorldName,
    /// Region label.
    Region,
    /// Authoritative host.
    Host,
    /// Character display name.
    CharacterName,
    /// Vocation label.
    Vocation,
    /// Gameplay-channel label.
    ChannelLabel,
}

/// Validated authoritative TCP route for one world.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorldRoute {
    host: String,
    port: NonZeroU16,
}

impl WorldRoute {
    /// Construct a bounded authoritative route.
    ///
    /// # Errors
    ///
    /// Returns a directory error for an invalid host or zero port.
    pub fn new(host: String, port: u16) -> Result<Self, DirectoryError> {
        validate_host(&host)?;
        let port = NonZeroU16::new(port).ok_or(DirectoryError::InvalidPort)?;
        Ok(Self { host, port })
    }

    /// Return the validated authoritative host.
    #[must_use]
    pub fn host(&self) -> &str {
        &self.host
    }

    /// Return the non-zero authoritative TCP port.
    #[must_use]
    pub const fn port(&self) -> u16 {
        self.port.get()
    }
}

/// Immutable authoritative world summary.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct WorldSummary {
    id: WorldId,
    slug: String,
    name: String,
    region: String,
    route: WorldRoute,
    availability: Availability,
    compatibility: Compatibility,
}

impl WorldSummary {
    /// Construct a validated world summary.
    ///
    /// # Errors
    ///
    /// Returns a bounded text or route validation error.
    pub fn new(
        id: WorldId,
        slug: String,
        name: String,
        region: String,
        route: WorldRoute,
        availability: Availability,
        compatibility: Compatibility,
    ) -> Result<Self, DirectoryError> {
        validate_text(&slug, TextField::WorldSlug, MAX_WORLD_SLUG_BYTES)?;
        validate_text(&name, TextField::WorldName, MAX_DISPLAY_NAME_BYTES)?;
        validate_text(&region, TextField::Region, MAX_REGION_BYTES)?;
        Ok(Self {
            id,
            slug,
            name,
            region,
            route,
            availability,
            compatibility,
        })
    }

    /// Return the authoritative identifier.
    #[must_use]
    pub const fn id(&self) -> WorldId {
        self.id
    }

    /// Return the bounded stable slug supplied by the directory.
    #[must_use]
    pub fn slug(&self) -> &str {
        &self.slug
    }

    /// Return the bounded display name.
    #[must_use]
    pub fn name(&self) -> &str {
        &self.name
    }

    /// Return the bounded region label.
    #[must_use]
    pub fn region(&self) -> &str {
        &self.region
    }

    /// Return the authoritative validated route.
    #[must_use]
    pub const fn route(&self) -> &WorldRoute {
        &self.route
    }

    /// Return the closed availability state.
    #[must_use]
    pub const fn availability(&self) -> Availability {
        self.availability
    }

    /// Return the closed compatibility state.
    #[must_use]
    pub const fn compatibility(&self) -> Compatibility {
        self.compatibility
    }
}

/// Immutable authoritative character summary.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct CharacterSummary {
    id: CharacterId,
    world_id: WorldId,
    name: String,
    level: u32,
    vocation: String,
    availability: Availability,
    compatibility: Compatibility,
}

impl CharacterSummary {
    /// Construct a validated character summary.
    ///
    /// # Errors
    ///
    /// Returns a directory error for empty/oversized text or a zero level.
    pub fn new(
        id: CharacterId,
        world_id: WorldId,
        name: String,
        level: u32,
        vocation: String,
        availability: Availability,
        compatibility: Compatibility,
    ) -> Result<Self, DirectoryError> {
        validate_text(&name, TextField::CharacterName, MAX_DISPLAY_NAME_BYTES)?;
        validate_text(&vocation, TextField::Vocation, MAX_VOCATION_BYTES)?;
        if level == 0 {
            return Err(DirectoryError::InvalidCharacterLevel);
        }
        Ok(Self {
            id,
            world_id,
            name,
            level,
            vocation,
            availability,
            compatibility,
        })
    }

    /// Return the authoritative identifier.
    #[must_use]
    pub const fn id(&self) -> CharacterId {
        self.id
    }

    /// Return the authoritative owning world identifier.
    #[must_use]
    pub const fn world_id(&self) -> WorldId {
        self.world_id
    }

    /// Return the bounded display name.
    #[must_use]
    pub fn name(&self) -> &str {
        &self.name
    }

    /// Return the positive character level.
    #[must_use]
    pub const fn level(&self) -> u32 {
        self.level
    }

    /// Return the bounded vocation label.
    #[must_use]
    pub fn vocation(&self) -> &str {
        &self.vocation
    }

    /// Return the closed availability state.
    #[must_use]
    pub const fn availability(&self) -> Availability {
        self.availability
    }

    /// Return the closed compatibility state.
    #[must_use]
    pub const fn compatibility(&self) -> Compatibility {
        self.compatibility
    }
}

/// Immutable authoritative gameplay-channel summary.
///
/// W7 Gateway protocol v1 does not populate this record; the bounded optional
/// model exists so later exact producer contracts need not redefine identity.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct GameplayChannelSummary {
    id: GameplayChannelId,
    world_id: WorldId,
    label: String,
    availability: Availability,
    compatibility: Compatibility,
}

impl GameplayChannelSummary {
    /// Construct a validated gameplay-channel summary.
    ///
    /// # Errors
    ///
    /// Returns a bounded text validation error.
    pub fn new(
        id: GameplayChannelId,
        world_id: WorldId,
        label: String,
        availability: Availability,
        compatibility: Compatibility,
    ) -> Result<Self, DirectoryError> {
        validate_text(&label, TextField::ChannelLabel, MAX_CHANNEL_LABEL_BYTES)?;
        Ok(Self {
            id,
            world_id,
            label,
            availability,
            compatibility,
        })
    }

    /// Return the opaque channel identifier.
    #[must_use]
    pub const fn id(&self) -> GameplayChannelId {
        self.id
    }

    /// Return the authoritative owning world identifier.
    #[must_use]
    pub const fn world_id(&self) -> WorldId {
        self.world_id
    }

    /// Return the bounded display label.
    #[must_use]
    pub fn label(&self) -> &str {
        &self.label
    }

    /// Return the closed availability state.
    #[must_use]
    pub const fn availability(&self) -> Availability {
        self.availability
    }

    /// Return the closed compatibility state.
    #[must_use]
    pub const fn compatibility(&self) -> Compatibility {
        self.compatibility
    }
}

/// Canonically ordered validated account directory for one local session generation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct AccountDirectorySnapshot {
    account_session_id: AccountSessionId,
    revision: DirectoryRevision,
    worlds: Vec<WorldSummary>,
    characters: Vec<CharacterSummary>,
    gameplay_channels: Vec<GameplayChannelSummary>,
}

impl AccountDirectorySnapshot {
    /// Validate, deterministically sort and own one authoritative directory response.
    ///
    /// # Errors
    ///
    /// Returns a closed directory error for exceeded bounds, duplicate identifiers,
    /// unknown world references or per-world channel overflow.
    pub fn new(
        account_session_id: AccountSessionId,
        revision: DirectoryRevision,
        mut worlds: Vec<WorldSummary>,
        mut characters: Vec<CharacterSummary>,
        mut gameplay_channels: Vec<GameplayChannelSummary>,
    ) -> Result<Self, DirectoryError> {
        if worlds.len() > MAX_WORLDS {
            return Err(DirectoryError::TooManyWorlds);
        }
        if characters.len() > MAX_CHARACTERS {
            return Err(DirectoryError::TooManyCharacters);
        }
        if gameplay_channels.len() > MAX_GAMEPLAY_CHANNELS {
            return Err(DirectoryError::TooManyGameplayChannels);
        }

        worlds.sort_by_key(WorldSummary::id);
        characters.sort_by_key(CharacterSummary::id);
        gameplay_channels.sort_by_key(GameplayChannelSummary::id);

        reject_duplicate_worlds(&worlds)?;
        reject_duplicate_characters(&characters)?;
        reject_duplicate_channels(&gameplay_channels)?;

        for character in &characters {
            if find_world(&worlds, character.world_id()).is_none() {
                return Err(DirectoryError::UnknownWorldReference {
                    subject: DirectorySubject::Character,
                    world_id: character.world_id(),
                });
            }
        }

        let mut channels_per_world = BTreeMap::<WorldId, usize>::new();
        for channel in &gameplay_channels {
            if find_world(&worlds, channel.world_id()).is_none() {
                return Err(DirectoryError::UnknownWorldReference {
                    subject: DirectorySubject::GameplayChannel,
                    world_id: channel.world_id(),
                });
            }
            let count = channels_per_world.entry(channel.world_id()).or_default();
            *count = count
                .checked_add(1)
                .ok_or(DirectoryError::ArithmeticOverflow)?;
            if *count > MAX_CHANNELS_PER_WORLD {
                return Err(DirectoryError::TooManyChannelsForWorld(channel.world_id()));
            }
        }

        Ok(Self {
            account_session_id,
            revision,
            worlds,
            characters,
            gameplay_channels,
        })
    }

    /// Return the local account-session identity owning this response.
    #[must_use]
    pub const fn account_session_id(&self) -> AccountSessionId {
        self.account_session_id
    }

    /// Return the client-local validated response generation.
    #[must_use]
    pub const fn revision(&self) -> DirectoryRevision {
        self.revision
    }

    /// Return worlds in deterministic identifier order.
    #[must_use]
    pub fn worlds(&self) -> &[WorldSummary] {
        &self.worlds
    }

    /// Return characters in deterministic identifier order.
    #[must_use]
    pub fn characters(&self) -> &[CharacterSummary] {
        &self.characters
    }

    /// Return gameplay channels in deterministic identifier order.
    #[must_use]
    pub fn gameplay_channels(&self) -> &[GameplayChannelSummary] {
        &self.gameplay_channels
    }

    /// Produce one validated explicit selection from this exact generation.
    ///
    /// # Errors
    ///
    /// Rejects a stale revision, unknown identifiers, mismatched world relations,
    /// or any selected record that is unavailable or incompatible.
    pub fn select(
        &self,
        expected_revision: DirectoryRevision,
        character_id: CharacterId,
        world_id: WorldId,
        gameplay_channel_id: Option<GameplayChannelId>,
    ) -> Result<SelectedEntry, DirectoryError> {
        if expected_revision != self.revision {
            return Err(DirectoryError::StaleRevision {
                expected: expected_revision,
                actual: self.revision,
            });
        }

        let world = find_world(&self.worlds, world_id)
            .ok_or(DirectoryError::WorldNotFound(world_id))?;
        ensure_selectable(
            DirectorySubject::World,
            world.availability(),
            world.compatibility(),
        )?;

        let character = find_character(&self.characters, character_id)
            .ok_or(DirectoryError::CharacterNotFound(character_id))?;
        if character.world_id() != world_id {
            return Err(DirectoryError::CharacterWorldMismatch {
                character_id,
                selected_world_id: world_id,
                actual_world_id: character.world_id(),
            });
        }
        ensure_selectable(
            DirectorySubject::Character,
            character.availability(),
            character.compatibility(),
        )?;

        let gameplay_channel = gameplay_channel_id
            .map(|id| {
                let channel = find_channel(&self.gameplay_channels, id)
                    .ok_or(DirectoryError::GameplayChannelNotFound(id))?;
                if channel.world_id() != world_id {
                    return Err(DirectoryError::ChannelWorldMismatch {
                        channel_id: id,
                        selected_world_id: world_id,
                        actual_world_id: channel.world_id(),
                    });
                }
                ensure_selectable(
                    DirectorySubject::GameplayChannel,
                    channel.availability(),
                    channel.compatibility(),
                )?;
                Ok(channel.clone())
            })
            .transpose()?;

        Ok(SelectedEntry {
            account_session_id: self.account_session_id,
            directory_revision: self.revision,
            world: world.clone(),
            character: character.clone(),
            gameplay_channel,
        })
    }

    /// Verify that a selection still belongs to this exact immutable snapshot.
    ///
    /// # Errors
    ///
    /// Rejects account/revision mismatch or any changed selected record.
    pub fn validate_selection(&self, selection: &SelectedEntry) -> Result<(), DirectoryError> {
        if selection.account_session_id != self.account_session_id {
            return Err(DirectoryError::AccountSessionMismatch);
        }
        let current = self.select(
            selection.directory_revision,
            selection.character.id(),
            selection.world.id(),
            selection.gameplay_channel.as_ref().map(GameplayChannelSummary::id),
        )?;
        if current != *selection {
            return Err(DirectoryError::SelectionNoLongerMatches);
        }
        Ok(())
    }
}

/// Explicit validated character/world/optional-channel selection.
///
/// Instances can only be produced by [`AccountDirectorySnapshot::select`]. They
/// retain the authoritative route and display metadata from that exact snapshot.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct SelectedEntry {
    account_session_id: AccountSessionId,
    directory_revision: DirectoryRevision,
    world: WorldSummary,
    character: CharacterSummary,
    gameplay_channel: Option<GameplayChannelSummary>,
}

impl SelectedEntry {
    /// Return the owning account-session generation.
    #[must_use]
    pub const fn account_session_id(&self) -> AccountSessionId {
        self.account_session_id
    }

    /// Return the exact directory generation used for selection.
    #[must_use]
    pub const fn directory_revision(&self) -> DirectoryRevision {
        self.directory_revision
    }

    /// Return the selected authoritative world.
    #[must_use]
    pub const fn world(&self) -> &WorldSummary {
        &self.world
    }

    /// Return the selected authoritative character.
    #[must_use]
    pub const fn character(&self) -> &CharacterSummary {
        &self.character
    }

    /// Return the optional selected gameplay channel.
    #[must_use]
    pub const fn gameplay_channel(&self) -> Option<&GameplayChannelSummary> {
        self.gameplay_channel.as_ref()
    }
}

/// Stable bounded validation failures for directory construction and selection.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DirectoryError {
    /// One typed identifier was invalid.
    Identifier(IdentifierError),
    /// Required text was empty.
    EmptyText(TextField),
    /// Text exceeded its UTF-8 byte limit.
    TextTooLong { field: TextField, maximum: usize },
    /// Text contained a control character.
    ControlCharacter(TextField),
    /// Text had leading or trailing whitespace.
    SurroundingWhitespace(TextField),
    /// An authoritative host contained an unsupported character or encoding.
    InvalidHost,
    /// A route used TCP port zero.
    InvalidPort,
    /// A character level was zero.
    InvalidCharacterLevel,
    /// World count exceeded [`MAX_WORLDS`].
    TooManyWorlds,
    /// Character count exceeded [`MAX_CHARACTERS`].
    TooManyCharacters,
    /// Gameplay-channel count exceeded [`MAX_GAMEPLAY_CHANNELS`].
    TooManyGameplayChannels,
    /// One world exceeded [`MAX_CHANNELS_PER_WORLD`].
    TooManyChannelsForWorld(WorldId),
    /// Two world records used the same identifier.
    DuplicateWorldId(WorldId),
    /// Two character records used the same identifier.
    DuplicateCharacterId(CharacterId),
    /// Two gameplay-channel records used the same identifier.
    DuplicateGameplayChannelId(GameplayChannelId),
    /// A character/channel referenced an absent world.
    UnknownWorldReference {
        subject: DirectorySubject,
        world_id: WorldId,
    },
    /// Checked arithmetic could not represent a bounded count.
    ArithmeticOverflow,
    /// A selection used a different directory generation.
    StaleRevision {
        expected: DirectoryRevision,
        actual: DirectoryRevision,
    },
    /// A selection belonged to another account-session generation.
    AccountSessionMismatch,
    /// The selected world identifier was absent.
    WorldNotFound(WorldId),
    /// The selected character identifier was absent.
    CharacterNotFound(CharacterId),
    /// The selected gameplay-channel identifier was absent.
    GameplayChannelNotFound(GameplayChannelId),
    /// The character did not belong to the selected world.
    CharacterWorldMismatch {
        character_id: CharacterId,
        selected_world_id: WorldId,
        actual_world_id: WorldId,
    },
    /// The gameplay channel did not belong to the selected world.
    ChannelWorldMismatch {
        channel_id: GameplayChannelId,
        selected_world_id: WorldId,
        actual_world_id: WorldId,
    },
    /// The selected entry is not currently available.
    Unavailable {
        subject: DirectorySubject,
        availability: Availability,
    },
    /// The selected entry is not compatible with this client contract.
    Incompatible {
        subject: DirectorySubject,
        compatibility: Compatibility,
    },
    /// A previously validated selection no longer exactly matches its snapshot.
    SelectionNoLongerMatches,
}

impl From<IdentifierError> for DirectoryError {
    fn from(value: IdentifierError) -> Self {
        Self::Identifier(value)
    }
}

impl Display for DirectoryError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::Identifier(error) => Display::fmt(error, formatter),
            Self::EmptyText(field) => write!(formatter, "required directory text is empty: {field:?}"),
            Self::TextTooLong { field, maximum } => write!(
                formatter,
                "directory text exceeds {maximum} UTF-8 bytes: {field:?}"
            ),
            Self::ControlCharacter(field) => {
                write!(formatter, "directory text contains a control character: {field:?}")
            }
            Self::SurroundingWhitespace(field) => write!(
                formatter,
                "directory text contains surrounding whitespace: {field:?}"
            ),
            Self::InvalidHost => formatter.write_str("authoritative world host is invalid"),
            Self::InvalidPort => formatter.write_str("authoritative world port must be non-zero"),
            Self::InvalidCharacterLevel => formatter.write_str("character level must be non-zero"),
            Self::TooManyWorlds => formatter.write_str("world count exceeds the directory limit"),
            Self::TooManyCharacters => {
                formatter.write_str("character count exceeds the directory limit")
            }
            Self::TooManyGameplayChannels => {
                formatter.write_str("gameplay-channel count exceeds the directory limit")
            }
            Self::TooManyChannelsForWorld(world_id) => {
                write!(formatter, "gameplay-channel count exceeds the per-world limit for {world_id}")
            }
            Self::DuplicateWorldId(id) => write!(formatter, "duplicate world identifier: {id}"),
            Self::DuplicateCharacterId(id) => {
                write!(formatter, "duplicate character identifier: {id}")
            }
            Self::DuplicateGameplayChannelId(id) => {
                write!(formatter, "duplicate gameplay-channel identifier: {id}")
            }
            Self::UnknownWorldReference { subject, world_id } => write!(
                formatter,
                "{subject:?} references an unknown authoritative world: {world_id}"
            ),
            Self::ArithmeticOverflow => formatter.write_str("directory count arithmetic overflow"),
            Self::StaleRevision { expected, actual } => write!(
                formatter,
                "directory revision is stale: expected {expected}, current {actual}"
            ),
            Self::AccountSessionMismatch => {
                formatter.write_str("directory selection belongs to another account session")
            }
            Self::WorldNotFound(id) => write!(formatter, "selected world is absent: {id}"),
            Self::CharacterNotFound(id) => write!(formatter, "selected character is absent: {id}"),
            Self::GameplayChannelNotFound(id) => {
                write!(formatter, "selected gameplay channel is absent: {id}")
            }
            Self::CharacterWorldMismatch {
                character_id,
                selected_world_id,
                actual_world_id,
            } => write!(
                formatter,
                "{character_id} belongs to {actual_world_id}, not {selected_world_id}"
            ),
            Self::ChannelWorldMismatch {
                channel_id,
                selected_world_id,
                actual_world_id,
            } => write!(
                formatter,
                "{channel_id} belongs to {actual_world_id}, not {selected_world_id}"
            ),
            Self::Unavailable {
                subject,
                availability,
            } => write!(
                formatter,
                "selected {subject:?} is unavailable: {availability:?}"
            ),
            Self::Incompatible {
                subject,
                compatibility,
            } => write!(
                formatter,
                "selected {subject:?} is incompatible: {compatibility:?}"
            ),
            Self::SelectionNoLongerMatches => {
                formatter.write_str("selected entry no longer matches its directory snapshot")
            }
        }
    }
}

impl Error for DirectoryError {}

fn validate_text(value: &str, field: TextField, maximum: usize) -> Result<(), DirectoryError> {
    if value.is_empty() {
        return Err(DirectoryError::EmptyText(field));
    }
    if value.len() > maximum {
        return Err(DirectoryError::TextTooLong { field, maximum });
    }
    if value.chars().any(char::is_control) {
        return Err(DirectoryError::ControlCharacter(field));
    }
    if value.trim() != value {
        return Err(DirectoryError::SurroundingWhitespace(field));
    }
    Ok(())
}

fn validate_host(host: &str) -> Result<(), DirectoryError> {
    validate_text(host, TextField::Host, MAX_HOST_BYTES)?;
    if !host.is_ascii()
        || host
            .bytes()
            .any(|byte| !(byte.is_ascii_alphanumeric() || matches!(byte, b'.' | b'-' | b':')))
    {
        return Err(DirectoryError::InvalidHost);
    }
    Ok(())
}

fn reject_duplicate_worlds(worlds: &[WorldSummary]) -> Result<(), DirectoryError> {
    for pair in worlds.windows(2) {
        if pair[0].id() == pair[1].id() {
            return Err(DirectoryError::DuplicateWorldId(pair[0].id()));
        }
    }
    Ok(())
}

fn reject_duplicate_characters(characters: &[CharacterSummary]) -> Result<(), DirectoryError> {
    for pair in characters.windows(2) {
        if pair[0].id() == pair[1].id() {
            return Err(DirectoryError::DuplicateCharacterId(pair[0].id()));
        }
    }
    Ok(())
}

fn reject_duplicate_channels(channels: &[GameplayChannelSummary]) -> Result<(), DirectoryError> {
    for pair in channels.windows(2) {
        if pair[0].id() == pair[1].id() {
            return Err(DirectoryError::DuplicateGameplayChannelId(pair[0].id()));
        }
    }
    Ok(())
}

fn find_world(worlds: &[WorldSummary], id: WorldId) -> Option<&WorldSummary> {
    worlds
        .binary_search_by_key(&id, WorldSummary::id)
        .ok()
        .map(|index| &worlds[index])
}

fn find_character(
    characters: &[CharacterSummary],
    id: CharacterId,
) -> Option<&CharacterSummary> {
    characters
        .binary_search_by_key(&id, CharacterSummary::id)
        .ok()
        .map(|index| &characters[index])
}

fn find_channel(
    channels: &[GameplayChannelSummary],
    id: GameplayChannelId,
) -> Option<&GameplayChannelSummary> {
    channels
        .binary_search_by_key(&id, GameplayChannelSummary::id)
        .ok()
        .map(|index| &channels[index])
}

fn ensure_selectable(
    subject: DirectorySubject,
    availability: Availability,
    compatibility: Compatibility,
) -> Result<(), DirectoryError> {
    if !availability.is_available() {
        return Err(DirectoryError::Unavailable {
            subject,
            availability,
        });
    }
    if !compatibility.is_compatible() {
        return Err(DirectoryError::Incompatible {
            subject,
            compatibility,
        });
    }
    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;

    fn world(id: i64) -> Result<WorldSummary, Box<dyn Error>> {
        Ok(WorldSummary::new(
            WorldId::new(id)?,
            format!("world-{id}"),
            format!("World {id}"),
            "eu".to_owned(),
            WorldRoute::new(format!("world{id}.example.test"), 7172)?,
            Availability::Available,
            Compatibility::Compatible,
        )?)
    }

    fn character(id: i64, world_id: i64) -> Result<CharacterSummary, Box<dyn Error>> {
        Ok(CharacterSummary::new(
            CharacterId::new(id)?,
            WorldId::new(world_id)?,
            format!("Character {id}"),
            42,
            "Knight".to_owned(),
            Availability::Available,
            Compatibility::Compatible,
        )?)
    }

    fn snapshot() -> Result<AccountDirectorySnapshot, Box<dyn Error>> {
        Ok(AccountDirectorySnapshot::new(
            AccountSessionId::new(7)?,
            DirectoryRevision::new(3)?,
            vec![world(2)?, world(1)?],
            vec![character(20, 2)?, character(10, 1)?],
            Vec::new(),
        )?)
    }

    #[test]
    fn identifiers_reject_zero_and_negative_values() {
        assert!(CharacterId::new(0).is_err());
        assert!(CharacterId::new(-1).is_err());
        assert!(WorldId::new(0).is_err());
        assert!(GameplayChannelId::new(-9).is_err());
        assert!(DirectoryRevision::new(0).is_err());
    }

    #[test]
    fn directory_enforces_string_and_collection_bounds() -> Result<(), Box<dyn Error>> {
        let result = WorldSummary::new(
            WorldId::new(1)?,
            "x".repeat(MAX_WORLD_SLUG_BYTES + 1),
            "World".to_owned(),
            "eu".to_owned(),
            WorldRoute::new("world.example.test".to_owned(), 7172)?,
            Availability::Available,
            Compatibility::Compatible,
        );
        assert_eq!(
            result,
            Err(DirectoryError::TextTooLong {
                field: TextField::WorldSlug,
                maximum: MAX_WORLD_SLUG_BYTES,
            })
        );

        let repeated_world = world(1)?;
        let worlds = vec![repeated_world; MAX_WORLDS + 1];
        let result = AccountDirectorySnapshot::new(
            AccountSessionId::new(1)?,
            DirectoryRevision::new(1)?,
            worlds,
            Vec::new(),
            Vec::new(),
        );
        assert_eq!(result, Err(DirectoryError::TooManyWorlds));
        Ok(())
    }

    #[test]
    fn duplicate_identifiers_are_rejected() -> Result<(), Box<dyn Error>> {
        let duplicate = world(4)?;
        let result = AccountDirectorySnapshot::new(
            AccountSessionId::new(1)?,
            DirectoryRevision::new(1)?,
            vec![duplicate.clone(), duplicate],
            Vec::new(),
            Vec::new(),
        );
        assert_eq!(
            result,
            Err(DirectoryError::DuplicateWorldId(WorldId::new(4)?))
        );
        Ok(())
    }

    #[test]
    fn snapshot_order_is_deterministic() -> Result<(), Box<dyn Error>> {
        let snapshot = snapshot()?;
        let world_ids = snapshot
            .worlds()
            .iter()
            .map(WorldSummary::id)
            .collect::<Vec<_>>();
        let character_ids = snapshot
            .characters()
            .iter()
            .map(CharacterSummary::id)
            .collect::<Vec<_>>();

        assert_eq!(world_ids, vec![WorldId::new(1)?, WorldId::new(2)?]);
        assert_eq!(
            character_ids,
            vec![CharacterId::new(10)?, CharacterId::new(20)?]
        );
        Ok(())
    }

    #[test]
    fn stale_revision_and_invalid_relationship_do_not_select() -> Result<(), Box<dyn Error>> {
        let snapshot = snapshot()?;
        assert_eq!(
            snapshot.select(
                DirectoryRevision::new(2)?,
                CharacterId::new(10)?,
                WorldId::new(1)?,
                None,
            ),
            Err(DirectoryError::StaleRevision {
                expected: DirectoryRevision::new(2)?,
                actual: DirectoryRevision::new(3)?,
            })
        );
        assert_eq!(
            snapshot.select(
                DirectoryRevision::new(3)?,
                CharacterId::new(10)?,
                WorldId::new(2)?,
                None,
            ),
            Err(DirectoryError::CharacterWorldMismatch {
                character_id: CharacterId::new(10)?,
                selected_world_id: WorldId::new(2)?,
                actual_world_id: WorldId::new(1)?,
            })
        );
        Ok(())
    }

    #[test]
    fn valid_selection_retains_typed_authoritative_route() -> Result<(), Box<dyn Error>> {
        let snapshot = snapshot()?;
        let selection = snapshot.select(
            snapshot.revision(),
            CharacterId::new(10)?,
            WorldId::new(1)?,
            None,
        )?;

        assert_eq!(selection.account_session_id(), snapshot.account_session_id());
        assert_eq!(selection.character().id(), CharacterId::new(10)?);
        assert_eq!(selection.world().route().host(), "world1.example.test");
        assert_eq!(selection.world().route().port(), 7172);
        assert!(selection.gameplay_channel().is_none());
        snapshot.validate_selection(&selection)?;
        Ok(())
    }
}
