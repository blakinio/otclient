use crate::{
    ContainerCapacity, ContainerHandle, ContainerSlot, DomainError, EntityHandle, EnvelopeVersion,
    ItemCount, ItemHandle, ItemTypeId, NameText, ObjectLocation, ResourceValue, SessionToken,
    StackIndex, TilePosition,
};
use oteryn_foundation::SessionGeneration;

/// Minimum semantic entity classes shared by gameplay consumers.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum EntityKind {
    /// The local or remote player entity.
    Player,
    /// A creature controlled by gameplay state.
    Creature,
    /// A non-player character.
    NonPlayerCharacter,
}

/// Stable semantic reasons for ending a gameplay session.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum SessionEndReason {
    /// The local user requested a clean end.
    Requested,
    /// The underlying connection was lost.
    ConnectionLost,
    /// The server closed the session.
    ServerClosed,
    /// Validated protocol processing could not continue.
    ProtocolFailure,
}

/// Closed minimum event vocabulary emitted by validated gameplay producers.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub enum GameEvent {
    /// Session bootstrap began; mutable simulation is not implied.
    BootstrapStarted,
    /// Bootstrap supplied the local player and initial position.
    BootstrapCompleted {
        /// Session-scoped local player entity.
        player: EntityHandle,
        /// Initial player position.
        position: TilePosition,
    },
    /// Consumers should clear the current contents of one tile.
    TileCleared {
        /// Tile whose semantic contents were reset.
        position: TilePosition,
    },
    /// One entity became visible at a tile stack position.
    EntityAppeared {
        /// Session-scoped entity handle.
        entity: EntityHandle,
        /// Semantic entity class.
        kind: EntityKind,
        /// Optional bounded display name.
        name: Option<NameText>,
        /// Tile position.
        position: TilePosition,
        /// Ordering position on the tile.
        stack: StackIndex,
    },
    /// One entity moved between canonical tile positions.
    EntityMoved {
        /// Session-scoped entity handle.
        entity: EntityHandle,
        /// Previous tile position.
        from: TilePosition,
        /// New tile position.
        to: TilePosition,
        /// New ordering position on the destination tile.
        stack: StackIndex,
    },
    /// One entity is no longer present at the stated tile.
    EntityRemoved {
        /// Session-scoped entity handle.
        entity: EntityHandle,
        /// Last known tile position.
        position: TilePosition,
    },
    /// One item instance was added or replaced at a canonical location.
    ItemChanged {
        /// Session-scoped item instance.
        item: ItemHandle,
        /// Canonical item definition identifier.
        item_type: ItemTypeId,
        /// Non-zero item quantity.
        count: ItemCount,
        /// Canonical location containing the item.
        location: ObjectLocation,
    },
    /// One item instance was removed from a canonical location.
    ItemRemoved {
        /// Session-scoped item instance.
        item: ItemHandle,
        /// Canonical location that previously contained the item.
        location: ObjectLocation,
    },
    /// Local player health and mana changed.
    PlayerResources {
        /// Validated health range.
        health: ResourceValue,
        /// Validated mana range.
        mana: ResourceValue,
    },
    /// A session-scoped container became available.
    ContainerOpened {
        /// Open container handle.
        container: ContainerHandle,
        /// Bounded, debug-redacted container title.
        title: NameText,
        /// Non-zero container capacity.
        capacity: ContainerCapacity,
    },
    /// One slot in an open container changed.
    ContainerSlotChanged {
        /// Open container handle.
        container: ContainerHandle,
        /// Slot that changed.
        slot: ContainerSlot,
        /// Session-scoped item now occupying the slot.
        item: ItemHandle,
        /// Canonical item definition identifier.
        item_type: ItemTypeId,
        /// Non-zero item quantity.
        count: ItemCount,
    },
    /// One slot in an open container became empty.
    ContainerSlotCleared {
        /// Open container handle.
        container: ContainerHandle,
        /// Slot that became empty.
        slot: ContainerSlot,
    },
    /// A session-scoped container was closed.
    ContainerClosed {
        /// Closed container handle.
        container: ContainerHandle,
    },
    /// Session lifecycle ended for a stable semantic reason.
    SessionEnded {
        /// Semantic end reason.
        reason: SessionEndReason,
    },
}

impl GameEvent {
    fn ensure_session(&self, session: SessionToken) -> Result<(), DomainError> {
        match self {
            Self::BootstrapCompleted { player, .. } => player.ensure_session(session),
            Self::EntityAppeared { entity, .. }
            | Self::EntityMoved { entity, .. }
            | Self::EntityRemoved { entity, .. } => entity.ensure_session(session),
            Self::ItemChanged { item, location, .. }
            | Self::ItemRemoved { item, location } => {
                item.ensure_session(session)?;
                location.ensure_session(session)
            }
            Self::ContainerOpened { container, .. }
            | Self::ContainerSlotCleared { container, .. }
            | Self::ContainerClosed { container } => container.ensure_session(session),
            Self::ContainerSlotChanged {
                container, item, ..
            } => {
                container.ensure_session(session)?;
                item.ensure_session(session)
            }
            Self::BootstrapStarted
            | Self::TileCleared { .. }
            | Self::PlayerResources { .. }
            | Self::SessionEnded { .. } => Ok(()),
        }
    }
}

/// Versioned, session-fenced semantic gameplay event.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct GameEventEnvelope {
    version: EnvelopeVersion,
    session: SessionToken,
    event: GameEvent,
}

impl GameEventEnvelope {
    /// Construct a version-one event envelope.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::SessionMismatch`] when a nested handle belongs to
    /// a different session generation.
    pub fn v1(session: SessionToken, event: GameEvent) -> Result<Self, DomainError> {
        Self::try_new(EnvelopeVersion::V1.get(), session, event)
    }

    /// Construct a validated event envelope from a numeric contract version.
    ///
    /// # Errors
    ///
    /// Returns a stable version or session validation error.
    pub fn try_new(
        version: u16,
        session: SessionToken,
        event: GameEvent,
    ) -> Result<Self, DomainError> {
        let version = EnvelopeVersion::try_new(version)?;
        event.ensure_session(session)?;
        Ok(Self {
            version,
            session,
            event,
        })
    }

    /// Return the accepted contract version.
    #[must_use]
    pub const fn version(&self) -> EnvelopeVersion {
        self.version
    }

    /// Return the session token fencing this event.
    #[must_use]
    pub const fn session(&self) -> SessionToken {
        self.session
    }

    /// Borrow the closed semantic event payload.
    #[must_use]
    pub const fn event(&self) -> &GameEvent {
        &self.event
    }

    /// Verify that this envelope still belongs to the caller's current session.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::StaleSession`] or
    /// [`DomainError::SessionMismatch`] on generation mismatch.
    pub fn ensure_current(&self, current: SessionGeneration) -> Result<(), DomainError> {
        self.session.ensure_current(current)?;
        self.event.ensure_session(self.session)
    }
}
