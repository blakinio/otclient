//! Deterministic protocol-neutral gameplay simulation and immutable render snapshots.
//!
//! This crate is the sole mutable writer for accepted [`GameEventEnvelope`]
//! values. It intentionally contains no Canary layouts, sockets, renderer,
//! assets, UI, platform or application-composition policy.

use oteryn_game_domain::{
    ContainerCapacity, ContainerHandle, ContainerSlot, DomainError, EntityHandle, EntityKind,
    GameEvent, GameEventEnvelope, ItemCount, ItemHandle, ItemTypeId, NameText, ObjectLocation,
    ResourceValue, SessionEndReason, SessionToken, StackIndex, TilePosition,
};
use std::collections::{BTreeMap, BTreeSet};
use std::fmt::{self, Display, Formatter};

/// Bounded capacities enforced after every atomic event application.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct SimulationLimits {
    max_tiles: usize,
    max_stack_entries_per_tile: usize,
    max_entities: usize,
    max_items: usize,
    max_containers: usize,
    max_container_slots: usize,
}

impl SimulationLimits {
    /// Conservative capacities for the P2 minimum-visible-world producer.
    pub const M2_DEFAULT: Self = Self {
        max_tiles: 4_096,
        max_stack_entries_per_tile: 64,
        max_entities: 4_096,
        max_items: 16_384,
        max_containers: 256,
        max_container_slots: 256,
    };

    /// Construct non-zero simulation limits within absolute crate ceilings.
    ///
    /// # Errors
    ///
    /// Returns [`SimulationError::ZeroLimit`] for the first zero limit and
    /// [`SimulationError::LimitTooLarge`] when a value exceeds its hard ceiling.
    pub fn try_new(
        max_tiles: usize,
        max_stack_entries_per_tile: usize,
        max_entities: usize,
        max_items: usize,
        max_containers: usize,
        max_container_slots: usize,
    ) -> Result<Self, SimulationError> {
        let values = [
            (LimitKind::Tiles, max_tiles),
            (LimitKind::StackEntriesPerTile, max_stack_entries_per_tile),
            (LimitKind::Entities, max_entities),
            (LimitKind::Items, max_items),
            (LimitKind::Containers, max_containers),
            (LimitKind::ContainerSlots, max_container_slots),
        ];
        for (kind, value) in values {
            if value == 0 {
                return Err(SimulationError::ZeroLimit(kind));
            }
            let hard_max = kind.hard_max();
            if value > hard_max {
                return Err(SimulationError::LimitTooLarge {
                    kind,
                    hard_max,
                    actual: value,
                });
            }
        }
        Ok(Self {
            max_tiles,
            max_stack_entries_per_tile,
            max_entities,
            max_items,
            max_containers,
            max_container_slots,
        })
    }

    /// Return the maximum number of occupied world tiles.
    #[must_use]
    pub const fn max_tiles(self) -> usize {
        self.max_tiles
    }

    /// Return the maximum number of visible stack entries on one tile.
    #[must_use]
    pub const fn max_stack_entries_per_tile(self) -> usize {
        self.max_stack_entries_per_tile
    }

    /// Return the maximum number of tracked entities.
    #[must_use]
    pub const fn max_entities(self) -> usize {
        self.max_entities
    }

    /// Return the maximum number of tracked item instances.
    #[must_use]
    pub const fn max_items(self) -> usize {
        self.max_items
    }

    /// Return the maximum number of open containers.
    #[must_use]
    pub const fn max_containers(self) -> usize {
        self.max_containers
    }

    /// Return the maximum accepted capacity and tracked slot count per container.
    #[must_use]
    pub const fn max_container_slots(self) -> usize {
        self.max_container_slots
    }
}

impl Default for SimulationLimits {
    fn default() -> Self {
        Self::M2_DEFAULT
    }
}

/// Stable simulation limit categories used by public errors.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum LimitKind {
    /// Occupied world tiles.
    Tiles,
    /// Visible entries on one tile.
    StackEntriesPerTile,
    /// Tracked entities.
    Entities,
    /// Tracked item instances.
    Items,
    /// Open containers.
    Containers,
    /// Slots in one open container.
    ContainerSlots,
}

impl LimitKind {
    const fn hard_max(self) -> usize {
        match self {
            Self::Tiles | Self::Entities => 16_384,
            Self::StackEntriesPerTile => 256,
            Self::Items => 65_536,
            Self::Containers | Self::ContainerSlots => 1_024,
        }
    }
}

impl Display for LimitKind {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let name = match self {
            Self::Tiles => "tiles",
            Self::StackEntriesPerTile => "stack entries per tile",
            Self::Entities => "entities",
            Self::Items => "items",
            Self::Containers => "containers",
            Self::ContainerSlots => "container slots",
        };
        formatter.write_str(name)
    }
}

/// Closed simulation lifecycle.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum SimulationPhase {
    /// No bootstrap event has been accepted.
    AwaitingBootstrap,
    /// Bootstrap began but the local player is not established.
    Bootstrapping,
    /// The local player and active world are established.
    Active,
    /// The gameplay session ended and session-owned state was cleared.
    Ended,
}

/// Stable event categories used by lifecycle errors.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SimulationEventKind {
    /// Bootstrap began.
    BootstrapStarted,
    /// Bootstrap completed.
    BootstrapCompleted,
    /// One tile was cleared.
    TileCleared,
    /// One entity appeared.
    EntityAppeared,
    /// One entity moved.
    EntityMoved,
    /// One entity was removed.
    EntityRemoved,
    /// One item changed.
    ItemChanged,
    /// One item was removed.
    ItemRemoved,
    /// Player resources changed.
    PlayerResources,
    /// One container opened.
    ContainerOpened,
    /// One container slot changed.
    ContainerSlotChanged,
    /// One container slot cleared.
    ContainerSlotCleared,
    /// One container closed.
    ContainerClosed,
    /// The session ended.
    SessionEnded,
}

impl SimulationEventKind {
    const fn from_event(event: &GameEvent) -> Self {
        match event {
            GameEvent::BootstrapStarted => Self::BootstrapStarted,
            GameEvent::BootstrapCompleted { .. } => Self::BootstrapCompleted,
            GameEvent::TileCleared { .. } => Self::TileCleared,
            GameEvent::EntityAppeared { .. } => Self::EntityAppeared,
            GameEvent::EntityMoved { .. } => Self::EntityMoved,
            GameEvent::EntityRemoved { .. } => Self::EntityRemoved,
            GameEvent::ItemChanged { .. } => Self::ItemChanged,
            GameEvent::ItemRemoved { .. } => Self::ItemRemoved,
            GameEvent::PlayerResources { .. } => Self::PlayerResources,
            GameEvent::ContainerOpened { .. } => Self::ContainerOpened,
            GameEvent::ContainerSlotChanged { .. } => Self::ContainerSlotChanged,
            GameEvent::ContainerSlotCleared { .. } => Self::ContainerSlotCleared,
            GameEvent::ContainerClosed { .. } => Self::ContainerClosed,
            GameEvent::SessionEnded { .. } => Self::SessionEnded,
        }
    }
}

impl Display for SimulationEventKind {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let name = match self {
            Self::BootstrapStarted => "bootstrap started",
            Self::BootstrapCompleted => "bootstrap completed",
            Self::TileCleared => "tile cleared",
            Self::EntityAppeared => "entity appeared",
            Self::EntityMoved => "entity moved",
            Self::EntityRemoved => "entity removed",
            Self::ItemChanged => "item changed",
            Self::ItemRemoved => "item removed",
            Self::PlayerResources => "player resources",
            Self::ContainerOpened => "container opened",
            Self::ContainerSlotChanged => "container slot changed",
            Self::ContainerSlotCleared => "container slot cleared",
            Self::ContainerClosed => "container closed",
            Self::SessionEnded => "session ended",
        };
        formatter.write_str(name)
    }
}

/// Monotonic simulation revision carried by immutable snapshots.
#[derive(Debug, Default, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct SimulationRevision(u64);

impl SimulationRevision {
    /// Initial revision before the first accepted event.
    pub const ZERO: Self = Self(0);

    /// Return the numeric revision.
    #[must_use]
    pub const fn get(self) -> u64 {
        self.0
    }

    fn checked_next(self) -> Result<Self, SimulationError> {
        self.0
            .checked_add(1)
            .map(Self)
            .ok_or(SimulationError::RevisionExhausted)
    }
}

/// Stable simulation failures.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum SimulationError {
    /// One configured capacity was zero.
    ZeroLimit(LimitKind),
    /// One configured capacity exceeded the absolute crate ceiling.
    LimitTooLarge {
        /// Capacity category.
        kind: LimitKind,
        /// Absolute crate ceiling.
        hard_max: usize,
        /// Requested value.
        actual: usize,
    },
    /// A merged game-domain contract rejected the envelope.
    Domain(DomainError),
    /// An event is invalid in the current lifecycle phase.
    InvalidPhase {
        /// Event category.
        event: SimulationEventKind,
        /// Current phase.
        phase: SimulationPhase,
    },
    /// The simulation revision cannot advance without wrapping.
    RevisionExhausted,
    /// One bounded collection exceeded its configured limit.
    CapacityExceeded {
        /// Capacity category.
        kind: LimitKind,
        /// Configured limit.
        limit: usize,
        /// Attempted count.
        attempted: usize,
    },
    /// An event referenced an unknown entity.
    UnknownEntity(EntityHandle),
    /// An entity was not at the event's declared prior position.
    EntityPositionMismatch {
        /// Entity being moved or removed.
        entity: EntityHandle,
        /// Position stored by simulation.
        actual: TilePosition,
        /// Position declared by the event.
        declared: TilePosition,
    },
    /// An event referenced an unknown item.
    UnknownItem(ItemHandle),
    /// An item was not at the event's declared location.
    ItemLocationMismatch {
        /// Item being removed.
        item: ItemHandle,
        /// Location stored by simulation.
        actual: ObjectLocation,
        /// Location declared by the event.
        declared: ObjectLocation,
    },
    /// An event referenced a container that is not open.
    UnknownContainer(ContainerHandle),
    /// A slot is outside the open container capacity or configured bound.
    ContainerSlotOutOfRange {
        /// Open container.
        container: ContainerHandle,
        /// Rejected slot.
        slot: ContainerSlot,
        /// Container capacity.
        capacity: ContainerCapacity,
    },
    /// Two visible objects attempted to occupy one tile stack index.
    OccupiedTileStack {
        /// Tile containing the collision.
        position: TilePosition,
        /// Duplicate stack index.
        stack: StackIndex,
    },
    /// Two item instances attempted to occupy one non-tile location.
    OccupiedItemLocation(ObjectLocation),
    /// Active state has no established local player handle.
    MissingLocalPlayer,
    /// Active state references a local player entity that is no longer tracked.
    LocalPlayerMissing(EntityHandle),
    /// A local player handle was declared with a non-player entity kind.
    LocalPlayerKindMismatch(EntityHandle),
}

impl From<DomainError> for SimulationError {
    fn from(error: DomainError) -> Self {
        Self::Domain(error)
    }
}

impl Display for SimulationError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::ZeroLimit(kind) => write!(formatter, "{kind} limit must be non-zero"),
            Self::LimitTooLarge {
                kind,
                hard_max,
                actual,
            } => write!(
                formatter,
                "{kind} limit {actual} exceeds absolute ceiling {hard_max}"
            ),
            Self::Domain(error) => Display::fmt(error, formatter),
            Self::InvalidPhase { event, phase } => {
                write!(formatter, "{event} is invalid during {phase:?}")
            }
            Self::RevisionExhausted => formatter.write_str("simulation revision is exhausted"),
            Self::CapacityExceeded {
                kind,
                limit,
                attempted,
            } => write!(
                formatter,
                "{kind} capacity {attempted} exceeds configured limit {limit}"
            ),
            Self::UnknownEntity(_) => formatter.write_str("event references an unknown entity"),
            Self::EntityPositionMismatch { .. } => {
                formatter.write_str("entity position does not match event declaration")
            }
            Self::UnknownItem(_) => formatter.write_str("event references an unknown item"),
            Self::ItemLocationMismatch { .. } => {
                formatter.write_str("item location does not match event declaration")
            }
            Self::UnknownContainer(_) => {
                formatter.write_str("event references an unknown container")
            }
            Self::ContainerSlotOutOfRange { .. } => {
                formatter.write_str("container slot is outside the accepted capacity")
            }
            Self::OccupiedTileStack { .. } => {
                formatter.write_str("tile stack index is already occupied")
            }
            Self::OccupiedItemLocation(_) => {
                formatter.write_str("item location is already occupied")
            }
            Self::MissingLocalPlayer => {
                formatter.write_str("active simulation has no local player handle")
            }
            Self::LocalPlayerMissing(_) => {
                formatter.write_str("active simulation lost the local player entity")
            }
            Self::LocalPlayerKindMismatch(_) => {
                formatter.write_str("local player entity must use player kind")
            }
        }
    }
}

impl std::error::Error for SimulationError {}

#[derive(Debug, Clone, PartialEq, Eq)]
struct EntityState {
    kind: EntityKind,
    name: Option<NameText>,
    position: TilePosition,
    stack: StackIndex,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct ItemState {
    item_type: ItemTypeId,
    count: ItemCount,
    location: ObjectLocation,
}

#[derive(Debug, Clone, Copy, PartialEq, Eq)]
struct ContainerState {
    capacity: ContainerCapacity,
}

#[derive(Debug, Clone, PartialEq, Eq)]
struct WorldState {
    phase: SimulationPhase,
    local_player: Option<EntityHandle>,
    resources: Option<PlayerResourceSnapshot>,
    end_reason: Option<SessionEndReason>,
    entities: BTreeMap<EntityHandle, EntityState>,
    items: BTreeMap<ItemHandle, ItemState>,
    containers: BTreeMap<ContainerHandle, ContainerState>,
}

impl Default for WorldState {
    fn default() -> Self {
        Self {
            phase: SimulationPhase::AwaitingBootstrap,
            local_player: None,
            resources: None,
            end_reason: None,
            entities: BTreeMap::new(),
            items: BTreeMap::new(),
            containers: BTreeMap::new(),
        }
    }
}

/// One immutable player-resource pair carried by snapshots.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct PlayerResourceSnapshot {
    health: ResourceValue,
    mana: ResourceValue,
}

impl PlayerResourceSnapshot {
    /// Return the accepted health range.
    #[must_use]
    pub const fn health(self) -> ResourceValue {
        self.health
    }

    /// Return the accepted mana range.
    #[must_use]
    pub const fn mana(self) -> ResourceValue {
        self.mana
    }
}

/// Renderer-facing immutable object entry.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum RenderObject {
    /// One visible world entity.
    Entity {
        /// Session-scoped entity handle.
        entity: EntityHandle,
        /// Semantic entity class.
        kind: EntityKind,
        /// Optional bounded display name.
        name: Option<NameText>,
    },
    /// One visible world item.
    Item {
        /// Session-scoped item handle.
        item: ItemHandle,
        /// Canonical item definition.
        item_type: ItemTypeId,
        /// Non-zero item count.
        count: ItemCount,
    },
}

/// One immutable object at a tile stack position.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct RenderStackEntry {
    stack: StackIndex,
    object: RenderObject,
}

impl RenderStackEntry {
    /// Return the tile stack index.
    #[must_use]
    pub const fn stack(&self) -> StackIndex {
        self.stack
    }

    /// Borrow the semantic render object.
    #[must_use]
    pub const fn object(&self) -> &RenderObject {
        &self.object
    }
}

/// One immutable ordered tile snapshot.
#[derive(Debug, Clone, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct RenderTile {
    position: TilePosition,
    entries: Vec<RenderStackEntry>,
}

impl RenderTile {
    /// Return the canonical tile position.
    #[must_use]
    pub const fn position(&self) -> TilePosition {
        self.position
    }

    /// Borrow ordered visible stack entries.
    #[must_use]
    pub fn entries(&self) -> &[RenderStackEntry] {
        &self.entries
    }
}

/// Immutable renderer-facing snapshot of one simulation revision.
#[derive(Debug, Clone, PartialEq, Eq, Hash)]
pub struct RenderSnapshot {
    session: SessionToken,
    revision: SimulationRevision,
    phase: SimulationPhase,
    local_player: Option<EntityHandle>,
    resources: Option<PlayerResourceSnapshot>,
    end_reason: Option<SessionEndReason>,
    tiles: Vec<RenderTile>,
}

impl RenderSnapshot {
    /// Return the gameplay session token.
    #[must_use]
    pub const fn session(&self) -> SessionToken {
        self.session
    }

    /// Return the committed simulation revision.
    #[must_use]
    pub const fn revision(&self) -> SimulationRevision {
        self.revision
    }

    /// Return the committed lifecycle phase.
    #[must_use]
    pub const fn phase(&self) -> SimulationPhase {
        self.phase
    }

    /// Return the local player handle after bootstrap.
    #[must_use]
    pub const fn local_player(&self) -> Option<EntityHandle> {
        self.local_player
    }

    /// Return the latest player resources.
    #[must_use]
    pub const fn resources(&self) -> Option<PlayerResourceSnapshot> {
        self.resources
    }

    /// Return the terminal session reason.
    #[must_use]
    pub const fn end_reason(&self) -> Option<SessionEndReason> {
        self.end_reason
    }

    /// Borrow tiles in canonical position order.
    #[must_use]
    pub fn tiles(&self) -> &[RenderTile] {
        &self.tiles
    }
}

/// One session-scoped single-writer simulation.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct Simulation {
    session: SessionToken,
    limits: SimulationLimits,
    revision: SimulationRevision,
    state: WorldState,
}

impl Simulation {
    /// Construct an empty simulation for one gameplay session.
    #[must_use]
    pub fn new(session: SessionToken, limits: SimulationLimits) -> Self {
        Self {
            session,
            limits,
            revision: SimulationRevision::ZERO,
            state: WorldState::default(),
        }
    }

    /// Return the owned gameplay session token.
    #[must_use]
    pub const fn session(&self) -> SessionToken {
        self.session
    }

    /// Return the configured capacities.
    #[must_use]
    pub const fn limits(&self) -> SimulationLimits {
        self.limits
    }

    /// Return the current lifecycle phase.
    #[must_use]
    pub const fn phase(&self) -> SimulationPhase {
        self.state.phase
    }

    /// Return the current committed revision.
    #[must_use]
    pub const fn revision(&self) -> SimulationRevision {
        self.revision
    }

    /// Return the number of tracked entities.
    #[must_use]
    pub fn entity_count(&self) -> usize {
        self.state.entities.len()
    }

    /// Return the number of tracked item instances.
    #[must_use]
    pub fn item_count(&self) -> usize {
        self.state.items.len()
    }

    /// Return the number of open containers.
    #[must_use]
    pub fn container_count(&self) -> usize {
        self.state.containers.len()
    }

    /// Atomically apply one validated semantic event.
    ///
    /// On failure, state and revision remain unchanged.
    ///
    /// # Errors
    ///
    /// Returns stable domain, lifecycle, consistency or capacity errors.
    pub fn apply(
        &mut self,
        envelope: &GameEventEnvelope,
    ) -> Result<SimulationRevision, SimulationError> {
        envelope.ensure_current(self.session.generation())?;
        let next_revision = self.revision.checked_next()?;
        let mut candidate = self.state.clone();
        candidate.apply_event(envelope.event())?;
        candidate.validate(self.limits)?;
        self.state = candidate;
        self.revision = next_revision;
        Ok(next_revision)
    }

    /// Publish an immutable renderer-facing snapshot.
    ///
    /// # Errors
    ///
    /// Returns a consistency error if visible locations contain a duplicate
    /// stack index. Such a condition is also rejected during event application.
    pub fn snapshot(&self) -> Result<RenderSnapshot, SimulationError> {
        self.state.snapshot(self.session, self.revision)
    }
}

impl WorldState {
    fn ensure_phase(
        &self,
        event: SimulationEventKind,
        accepted: &[SimulationPhase],
    ) -> Result<(), SimulationError> {
        if accepted.contains(&self.phase) {
            Ok(())
        } else {
            Err(SimulationError::InvalidPhase {
                event,
                phase: self.phase,
            })
        }
    }

    fn apply_event(&mut self, event: &GameEvent) -> Result<(), SimulationError> {
        let kind = SimulationEventKind::from_event(event);
        match event {
            GameEvent::BootstrapStarted => {
                self.ensure_phase(kind, &[SimulationPhase::AwaitingBootstrap])?;
                self.phase = SimulationPhase::Bootstrapping;
                self.end_reason = None;
            }
            GameEvent::BootstrapCompleted { player, position } => {
                self.ensure_phase(kind, &[SimulationPhase::Bootstrapping])?;
                if let Some(entity) = self.entities.get(player)
                    && entity.kind != EntityKind::Player
                {
                    return Err(SimulationError::LocalPlayerKindMismatch(*player));
                }
                self.entities
                    .entry(*player)
                    .and_modify(|entity| entity.position = *position)
                    .or_insert_with(|| EntityState {
                        kind: EntityKind::Player,
                        name: None,
                        position: *position,
                        stack: StackIndex::new(0),
                    });
                self.local_player = Some(*player);
                self.phase = SimulationPhase::Active;
            }
            GameEvent::TileCleared { position } => {
                self.ensure_world_event(kind)?;
                self.entities
                    .retain(|_, entity| entity.position != *position);
                self.items.retain(|_, item| {
                    !matches!(
                        item.location,
                        ObjectLocation::Tile {
                            position: item_position,
                            ..
                        } if item_position == *position
                    )
                });
            }
            GameEvent::EntityAppeared {
                entity,
                kind: entity_kind,
                name,
                position,
                stack,
            } => {
                self.ensure_world_event(kind)?;
                if self.local_player == Some(*entity) && *entity_kind != EntityKind::Player {
                    return Err(SimulationError::LocalPlayerKindMismatch(*entity));
                }
                self.entities.insert(
                    *entity,
                    EntityState {
                        kind: *entity_kind,
                        name: name.clone(),
                        position: *position,
                        stack: *stack,
                    },
                );
            }
            GameEvent::EntityMoved {
                entity,
                from,
                to,
                stack,
            } => {
                self.ensure_world_event(kind)?;
                let stored = self
                    .entities
                    .get_mut(entity)
                    .ok_or(SimulationError::UnknownEntity(*entity))?;
                if stored.position != *from {
                    return Err(SimulationError::EntityPositionMismatch {
                        entity: *entity,
                        actual: stored.position,
                        declared: *from,
                    });
                }
                stored.position = *to;
                stored.stack = *stack;
            }
            GameEvent::EntityRemoved { entity, position } => {
                self.ensure_world_event(kind)?;
                let stored = self
                    .entities
                    .get(entity)
                    .ok_or(SimulationError::UnknownEntity(*entity))?;
                if stored.position != *position {
                    return Err(SimulationError::EntityPositionMismatch {
                        entity: *entity,
                        actual: stored.position,
                        declared: *position,
                    });
                }
                self.entities.remove(entity);
            }
            GameEvent::ItemChanged {
                item,
                item_type,
                count,
                location,
            } => {
                self.ensure_world_event(kind)?;
                self.validate_item_location(*location)?;
                self.replace_item(
                    *item,
                    ItemState {
                        item_type: *item_type,
                        count: *count,
                        location: *location,
                    },
                );
            }
            GameEvent::ItemRemoved { item, location } => {
                self.ensure_world_event(kind)?;
                let stored = self
                    .items
                    .get(item)
                    .ok_or(SimulationError::UnknownItem(*item))?;
                if stored.location != *location {
                    return Err(SimulationError::ItemLocationMismatch {
                        item: *item,
                        actual: stored.location,
                        declared: *location,
                    });
                }
                self.items.remove(item);
            }
            GameEvent::PlayerResources { health, mana } => {
                self.ensure_world_event(kind)?;
                self.resources = Some(PlayerResourceSnapshot {
                    health: *health,
                    mana: *mana,
                });
            }
            GameEvent::ContainerOpened {
                container,
                title: _,
                capacity,
            } => {
                self.ensure_world_event(kind)?;
                self.containers.insert(
                    *container,
                    ContainerState {
                        capacity: *capacity,
                    },
                );
            }
            GameEvent::ContainerSlotChanged {
                container,
                slot,
                item,
                item_type,
                count,
            } => {
                self.ensure_world_event(kind)?;
                let location = ObjectLocation::Container {
                    container: *container,
                    slot: *slot,
                };
                self.validate_item_location(location)?;
                self.replace_item(
                    *item,
                    ItemState {
                        item_type: *item_type,
                        count: *count,
                        location,
                    },
                );
            }
            GameEvent::ContainerSlotCleared { container, slot } => {
                self.ensure_world_event(kind)?;
                let location = ObjectLocation::Container {
                    container: *container,
                    slot: *slot,
                };
                self.validate_item_location(location)?;
                self.items.retain(|_, item| item.location != location);
            }
            GameEvent::ContainerClosed { container } => {
                self.ensure_world_event(kind)?;
                if self.containers.remove(container).is_none() {
                    return Err(SimulationError::UnknownContainer(*container));
                }
                self.items.retain(|_, item| {
                    !matches!(
                        item.location,
                        ObjectLocation::Container {
                            container: item_container,
                            ..
                        } if item_container == *container
                    )
                });
            }
            GameEvent::SessionEnded { reason } => {
                self.ensure_phase(
                    kind,
                    &[
                        SimulationPhase::AwaitingBootstrap,
                        SimulationPhase::Bootstrapping,
                        SimulationPhase::Active,
                    ],
                )?;
                self.phase = SimulationPhase::Ended;
                self.local_player = None;
                self.resources = None;
                self.entities.clear();
                self.items.clear();
                self.containers.clear();
                self.end_reason = Some(*reason);
            }
        }
        Ok(())
    }

    fn ensure_world_event(&self, event: SimulationEventKind) -> Result<(), SimulationError> {
        self.ensure_phase(
            event,
            &[SimulationPhase::Bootstrapping, SimulationPhase::Active],
        )
    }

    fn replace_item(&mut self, item: ItemHandle, state: ItemState) {
        let location = state.location;
        self.items
            .retain(|existing, stored| *existing == item || stored.location != location);
        self.items.insert(item, state);
    }

    fn validate_item_location(&self, location: ObjectLocation) -> Result<(), SimulationError> {
        if let ObjectLocation::Container { container, slot } = location {
            let stored = self
                .containers
                .get(&container)
                .ok_or(SimulationError::UnknownContainer(container))?;
            if slot.get() >= stored.capacity.get() {
                return Err(SimulationError::ContainerSlotOutOfRange {
                    container,
                    slot,
                    capacity: stored.capacity,
                });
            }
        }
        Ok(())
    }

    fn validate(&self, limits: SimulationLimits) -> Result<(), SimulationError> {
        if self.phase == SimulationPhase::Active {
            let player = self
                .local_player
                .ok_or(SimulationError::MissingLocalPlayer)?;
            let entity = self
                .entities
                .get(&player)
                .ok_or(SimulationError::LocalPlayerMissing(player))?;
            if entity.kind != EntityKind::Player {
                return Err(SimulationError::LocalPlayerKindMismatch(player));
            }
        }

        enforce_capacity(
            LimitKind::Entities,
            limits.max_entities,
            self.entities.len(),
        )?;
        enforce_capacity(LimitKind::Items, limits.max_items, self.items.len())?;
        enforce_capacity(
            LimitKind::Containers,
            limits.max_containers,
            self.containers.len(),
        )?;

        for (container, state) in &self.containers {
            let capacity = usize::from(state.capacity.get());
            enforce_capacity(
                LimitKind::ContainerSlots,
                limits.max_container_slots,
                capacity,
            )?;
            let slot_count = self
                .items
                .values()
                .filter(|item| {
                    matches!(
                        item.location,
                        ObjectLocation::Container {
                            container: item_container,
                            ..
                        } if item_container == *container
                    )
                })
                .count();
            enforce_capacity(
                LimitKind::ContainerSlots,
                limits.max_container_slots,
                slot_count,
            )?;
        }

        for item in self.items.values() {
            if let ObjectLocation::Container { container, slot } = item.location {
                let state = self
                    .containers
                    .get(&container)
                    .ok_or(SimulationError::UnknownContainer(container))?;
                if slot.get() >= state.capacity.get() {
                    return Err(SimulationError::ContainerSlotOutOfRange {
                        container,
                        slot,
                        capacity: state.capacity,
                    });
                }
            }
        }

        let visible = self.visible_entries()?;
        enforce_capacity(LimitKind::Tiles, limits.max_tiles, visible.len())?;
        for entries in visible.values() {
            enforce_capacity(
                LimitKind::StackEntriesPerTile,
                limits.max_stack_entries_per_tile,
                entries.len(),
            )?;
        }

        let mut locations = BTreeSet::new();
        for item in self.items.values() {
            if !matches!(item.location, ObjectLocation::Tile { .. })
                && !locations.insert(item.location)
            {
                return Err(SimulationError::OccupiedItemLocation(item.location));
            }
        }
        Ok(())
    }

    fn visible_entries(
        &self,
    ) -> Result<BTreeMap<TilePosition, Vec<RenderStackEntry>>, SimulationError> {
        let mut tiles: BTreeMap<TilePosition, Vec<RenderStackEntry>> = BTreeMap::new();
        for (entity, state) in &self.entities {
            tiles
                .entry(state.position)
                .or_default()
                .push(RenderStackEntry {
                    stack: state.stack,
                    object: RenderObject::Entity {
                        entity: *entity,
                        kind: state.kind,
                        name: state.name.clone(),
                    },
                });
        }
        for (item, state) in &self.items {
            if let ObjectLocation::Tile { position, stack } = state.location {
                tiles.entry(position).or_default().push(RenderStackEntry {
                    stack,
                    object: RenderObject::Item {
                        item: *item,
                        item_type: state.item_type,
                        count: state.count,
                    },
                });
            }
        }
        for (position, entries) in &mut tiles {
            entries.sort();
            let mut stacks = BTreeSet::new();
            for entry in entries.iter() {
                if !stacks.insert(entry.stack) {
                    return Err(SimulationError::OccupiedTileStack {
                        position: *position,
                        stack: entry.stack,
                    });
                }
            }
        }
        Ok(tiles)
    }

    fn snapshot(
        &self,
        session: SessionToken,
        revision: SimulationRevision,
    ) -> Result<RenderSnapshot, SimulationError> {
        let tiles = self
            .visible_entries()?
            .into_iter()
            .map(|(position, entries)| RenderTile { position, entries })
            .collect();
        Ok(RenderSnapshot {
            session,
            revision,
            phase: self.phase,
            local_player: self.local_player,
            resources: self.resources,
            end_reason: self.end_reason,
            tiles,
        })
    }
}

fn enforce_capacity(
    kind: LimitKind,
    limit: usize,
    attempted: usize,
) -> Result<(), SimulationError> {
    if attempted <= limit {
        Ok(())
    } else {
        Err(SimulationError::CapacityExceeded {
            kind,
            limit,
            attempted,
        })
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_foundation::SessionGeneration;
    use oteryn_game_domain::{ContainerId, EntityId, Floor, ItemId, SessionToken};

    fn token(value: u64) -> SessionToken {
        SessionToken::new(SessionGeneration::new(value))
    }

    fn limits() -> Result<SimulationLimits, SimulationError> {
        SimulationLimits::try_new(16, 8, 16, 32, 4, 16)
    }

    fn position(x: u16, y: u16) -> TilePosition {
        TilePosition::new(x, y, Floor::new(7))
    }

    fn entity(session: SessionToken, value: u32) -> Result<EntityHandle, DomainError> {
        Ok(EntityHandle::new(session, EntityId::try_new(value)?))
    }

    fn item(session: SessionToken, value: u32) -> Result<ItemHandle, DomainError> {
        Ok(ItemHandle::new(session, ItemId::try_new(value)?))
    }

    #[test]
    fn bootstrap_publishes_local_player_snapshot() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(1);
        let player = entity(session, 1)?;
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapCompleted {
                player,
                position: position(100, 200),
            },
        )?)?;

        let snapshot = simulation.snapshot()?;
        assert_eq!(snapshot.phase(), SimulationPhase::Active);
        assert_eq!(snapshot.local_player(), Some(player));
        assert_eq!(snapshot.tiles().len(), 1);
        assert_eq!(snapshot.revision().get(), 2);
        Ok(())
    }

    #[test]
    fn failed_event_is_atomic() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(2);
        let player = entity(session, 1)?;
        let missing = entity(session, 2)?;
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapCompleted {
                player,
                position: position(1, 1),
            },
        )?)?;
        let before = simulation.clone();

        let error = simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::EntityMoved {
                entity: missing,
                from: position(1, 1),
                to: position(2, 1),
                stack: StackIndex::new(0),
            },
        )?);
        assert_eq!(error, Err(SimulationError::UnknownEntity(missing)));
        assert_eq!(simulation, before);
        Ok(())
    }

    #[test]
    fn stale_session_is_rejected_without_mutation() -> Result<(), Box<dyn std::error::Error>> {
        let current = token(3);
        let stale = token(2);
        let mut simulation = Simulation::new(current, limits()?);
        let before = simulation.clone();
        let event = GameEventEnvelope::v1(stale, GameEvent::BootstrapStarted)?;
        assert!(matches!(
            simulation.apply(&event),
            Err(SimulationError::Domain(DomainError::StaleSession { .. }))
        ));
        assert_eq!(simulation, before);
        Ok(())
    }

    #[test]
    fn visible_entries_are_canonically_ordered() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(4);
        let player = entity(session, 1)?;
        let other = entity(session, 2)?;
        let object = item(session, 3)?;
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::EntityAppeared {
                entity: other,
                kind: EntityKind::Creature,
                name: None,
                position: position(5, 5),
                stack: StackIndex::new(2),
            },
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::ItemChanged {
                item: object,
                item_type: ItemTypeId::try_new(100)?,
                count: ItemCount::try_new(1)?,
                location: ObjectLocation::Tile {
                    position: position(5, 5),
                    stack: StackIndex::new(1),
                },
            },
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapCompleted {
                player,
                position: position(5, 6),
            },
        )?)?;

        let snapshot = simulation.snapshot()?;
        assert_eq!(snapshot.tiles().len(), 2);
        assert_eq!(snapshot.tiles()[0].entries()[0].stack().get(), 1);
        assert_eq!(snapshot.tiles()[0].entries()[1].stack().get(), 2);
        Ok(())
    }

    #[test]
    fn tile_stack_collision_is_rejected_atomically() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(5);
        let first = entity(session, 1)?;
        let second = entity(session, 2)?;
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::EntityAppeared {
                entity: first,
                kind: EntityKind::Creature,
                name: None,
                position: position(1, 1),
                stack: StackIndex::new(1),
            },
        )?)?;
        let before = simulation.clone();

        let result = simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::EntityAppeared {
                entity: second,
                kind: EntityKind::Creature,
                name: None,
                position: position(1, 1),
                stack: StackIndex::new(1),
            },
        )?);
        assert!(matches!(
            result,
            Err(SimulationError::OccupiedTileStack { .. })
        ));
        assert_eq!(simulation, before);
        Ok(())
    }

    #[test]
    fn container_lifecycle_is_bounded_and_cleared() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(6);
        let container = ContainerHandle::new(session, ContainerId::try_new(1)?);
        let object = item(session, 2)?;
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::ContainerOpened {
                container,
                title: NameText::try_new("Bag")?,
                capacity: ContainerCapacity::try_new(2)?,
            },
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::ContainerSlotChanged {
                container,
                slot: ContainerSlot::new(0),
                item: object,
                item_type: ItemTypeId::try_new(50)?,
                count: ItemCount::try_new(1)?,
            },
        )?)?;
        assert_eq!(simulation.container_count(), 1);
        assert_eq!(simulation.item_count(), 1);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::ContainerClosed { container },
        )?)?;
        assert_eq!(simulation.container_count(), 0);
        assert_eq!(simulation.item_count(), 0);
        Ok(())
    }

    #[test]
    fn session_end_clears_session_owned_state() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(7);
        let player = entity(session, 1)?;
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapCompleted {
                player,
                position: position(1, 1),
            },
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::SessionEnded {
                reason: SessionEndReason::Requested,
            },
        )?)?;

        let snapshot = simulation.snapshot()?;
        assert_eq!(snapshot.phase(), SimulationPhase::Ended);
        assert_eq!(snapshot.local_player(), None);
        assert_eq!(snapshot.end_reason(), Some(SessionEndReason::Requested));
        assert!(snapshot.tiles().is_empty());
        assert_eq!(simulation.entity_count(), 0);
        Ok(())
    }

    #[test]
    fn identical_streams_produce_equal_snapshots() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(8);
        let player = entity(session, 1)?;
        let events = [
            GameEventEnvelope::v1(session, GameEvent::BootstrapStarted)?,
            GameEventEnvelope::v1(
                session,
                GameEvent::BootstrapCompleted {
                    player,
                    position: position(3, 4),
                },
            )?,
            GameEventEnvelope::v1(
                session,
                GameEvent::PlayerResources {
                    health: ResourceValue::try_new(50, 100)?,
                    mana: ResourceValue::try_new(20, 40)?,
                },
            )?,
        ];

        let mut first = Simulation::new(session, limits()?);
        let mut second = Simulation::new(session, limits()?);
        for event in &events {
            first.apply(event)?;
            second.apply(event)?;
        }
        assert_eq!(first.snapshot()?, second.snapshot()?);
        Ok(())
    }

    #[test]
    fn zero_limits_fail_explicitly() {
        assert_eq!(
            SimulationLimits::try_new(0, 1, 1, 1, 1, 1),
            Err(SimulationError::ZeroLimit(LimitKind::Tiles))
        );
    }

    #[test]
    fn removing_local_player_is_rejected_atomically() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(9);
        let player = entity(session, 1)?;
        let player_position = position(8, 8);
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapCompleted {
                player,
                position: player_position,
            },
        )?)?;
        let before = simulation.clone();

        assert_eq!(
            simulation.apply(&GameEventEnvelope::v1(
                session,
                GameEvent::EntityRemoved {
                    entity: player,
                    position: player_position,
                },
            )?),
            Err(SimulationError::LocalPlayerMissing(player))
        );
        assert_eq!(simulation, before);
        Ok(())
    }

    #[test]
    fn clearing_local_player_tile_is_rejected_atomically() -> Result<(), Box<dyn std::error::Error>>
    {
        let session = token(10);
        let player = entity(session, 1)?;
        let player_position = position(9, 9);
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapCompleted {
                player,
                position: player_position,
            },
        )?)?;
        let before = simulation.clone();

        assert_eq!(
            simulation.apply(&GameEventEnvelope::v1(
                session,
                GameEvent::TileCleared {
                    position: player_position,
                },
            )?),
            Err(SimulationError::LocalPlayerMissing(player))
        );
        assert_eq!(simulation, before);
        Ok(())
    }

    #[test]
    fn changed_item_replaces_previous_item_at_location() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(11);
        let first = item(session, 1)?;
        let second = item(session, 2)?;
        let location = ObjectLocation::Tile {
            position: position(2, 2),
            stack: StackIndex::new(1),
        };
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::ItemChanged {
                item: first,
                item_type: ItemTypeId::try_new(100)?,
                count: ItemCount::try_new(1)?,
                location,
            },
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::ItemChanged {
                item: second,
                item_type: ItemTypeId::try_new(101)?,
                count: ItemCount::try_new(2)?,
                location,
            },
        )?)?;

        assert_eq!(simulation.item_count(), 1);
        let snapshot = simulation.snapshot()?;
        assert!(matches!(
        snapshot.tiles()[0].entries()[0].object(),
        RenderObject::Item { item, .. } if *item == second
              ));
        Ok(())
    }

    #[test]
    fn container_slot_change_replaces_previous_item() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(12);
        let container = ContainerHandle::new(session, ContainerId::try_new(1)?);
        let first = item(session, 1)?;
        let second = item(session, 2)?;
        let slot = ContainerSlot::new(0);
        let mut simulation = Simulation::new(session, limits()?);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::ContainerOpened {
                container,
                title: NameText::try_new("Bag")?,
                capacity: ContainerCapacity::try_new(2)?,
            },
        )?)?;
        for object in [first, second] {
            simulation.apply(&GameEventEnvelope::v1(
                session,
                GameEvent::ContainerSlotChanged {
                    container,
                    slot,
                    item: object,
                    item_type: ItemTypeId::try_new(50)?,
                    count: ItemCount::try_new(1)?,
                },
            )?)?;
        }
        assert_eq!(simulation.item_count(), 1);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::ItemRemoved {
                item: second,
                location: ObjectLocation::Container { container, slot },
            },
        )?)?;
        assert_eq!(simulation.item_count(), 0);
        Ok(())
    }

    #[test]
    fn entity_capacity_failure_is_atomic() -> Result<(), Box<dyn std::error::Error>> {
        let session = token(13);
        let player = entity(session, 1)?;
        let other = entity(session, 2)?;
        let constrained = SimulationLimits::try_new(16, 8, 1, 32, 4, 16)?;
        let mut simulation = Simulation::new(session, constrained);
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapStarted,
        )?)?;
        simulation.apply(&GameEventEnvelope::v1(
            session,
            GameEvent::BootstrapCompleted {
                player,
                position: position(1, 1),
            },
        )?)?;
        let before = simulation.clone();
        assert_eq!(
            simulation.apply(&GameEventEnvelope::v1(
                session,
                GameEvent::EntityAppeared {
                    entity: other,
                    kind: EntityKind::Creature,
                    name: None,
                    position: position(2, 1),
                    stack: StackIndex::new(0),
                },
            )?),
            Err(SimulationError::CapacityExceeded {
                kind: LimitKind::Entities,
                limit: 1,
                attempted: 2,
            })
        );
        assert_eq!(simulation, before);
        Ok(())
    }

    #[test]
    fn absolute_limit_ceiling_fails_explicitly() {
        assert_eq!(
            SimulationLimits::try_new(16_385, 1, 1, 1, 1, 1),
            Err(SimulationError::LimitTooLarge {
                kind: LimitKind::Tiles,
                hard_max: 16_384,
                actual: 16_385,
            })
        );
    }
}
