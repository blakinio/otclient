use crate::{
    ContainerHandle, ContainerSlot, CreatureHandle, DomainError, EntityHandle, InventorySlot,
    ItemHandle, SessionToken, StackIndex, TilePosition,
};

/// Canonical protocol-neutral location of an item or interactable object.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum ObjectLocation {
    /// Object at one tile stack position.
    Tile {
        /// World tile position.
        position: TilePosition,
        /// Ordering position on the tile.
        stack: StackIndex,
    },
    /// Object inside an open session-scoped container.
    Container {
        /// Open container handle.
        container: ContainerHandle,
        /// Slot inside the container.
        slot: ContainerSlot,
    },
    /// Object in one product-neutral inventory slot.
    Inventory {
        /// Inventory slot identifier.
        slot: InventorySlot,
    },
}

impl ObjectLocation {
    pub(crate) fn ensure_session(&self, session: SessionToken) -> Result<(), DomainError> {
        match self {
            Self::Container { container, .. } => container.ensure_session(session),
            Self::Tile { .. } | Self::Inventory { .. } => Ok(()),
        }
    }
}

/// Canonical target accepted by look, use and targeting commands.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum ObjectTarget {
    /// Target one world entity.
    Entity(EntityHandle),
    /// Target one creature.
    Creature(CreatureHandle),
    /// Target one item instance.
    Item(ItemHandle),
    /// Target an object by location.
    Location(ObjectLocation),
}

impl ObjectTarget {
    pub(crate) fn ensure_session(&self, session: SessionToken) -> Result<(), DomainError> {
        match self {
            Self::Entity(handle) => handle.ensure_session(session),
            Self::Creature(handle) => handle.ensure_session(session),
            Self::Item(handle) => handle.ensure_session(session),
            Self::Location(location) => location.ensure_session(session),
        }
    }
}
