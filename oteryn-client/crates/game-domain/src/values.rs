use crate::DomainError;
use std::num::NonZeroU16;

/// Protocol-neutral floor coordinate bounded by its `u8` representation.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct Floor(u8);

impl Floor {
    /// Construct a floor coordinate.
    #[must_use]
    pub const fn new(value: u8) -> Self {
        Self(value)
    }

    /// Return the floor coordinate.
    #[must_use]
    pub const fn get(self) -> u8 {
        self.0
    }
}

/// Position of one tile in the canonical game world coordinate space.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct TilePosition {
    x: u16,
    y: u16,
    floor: Floor,
}

impl TilePosition {
    /// Construct a bounded tile position.
    #[must_use]
    pub const fn new(x: u16, y: u16, floor: Floor) -> Self {
        Self { x, y, floor }
    }

    /// Return the horizontal X coordinate.
    #[must_use]
    pub const fn x(self) -> u16 {
        self.x
    }

    /// Return the horizontal Y coordinate.
    #[must_use]
    pub const fn y(self) -> u16 {
        self.y
    }

    /// Return the floor coordinate.
    #[must_use]
    pub const fn floor(self) -> Floor {
        self.floor
    }
}

/// Ordering position of an object on a tile.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct StackIndex(u8);

impl StackIndex {
    /// Construct a stack index bounded by its `u8` representation.
    #[must_use]
    pub const fn new(value: u8) -> Self {
        Self(value)
    }

    /// Return the stack index.
    #[must_use]
    pub const fn get(self) -> u8 {
        self.0
    }
}

/// Slot index inside one open container.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct ContainerSlot(u16);

impl ContainerSlot {
    /// Construct a container slot index.
    #[must_use]
    pub const fn new(value: u16) -> Self {
        Self(value)
    }

    /// Return the slot index.
    #[must_use]
    pub const fn get(self) -> u16 {
        self.0
    }
}

/// Product-neutral inventory slot identifier.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct InventorySlot(u8);

impl InventorySlot {
    /// Construct an inventory slot identifier.
    #[must_use]
    pub const fn new(value: u8) -> Self {
        Self(value)
    }

    /// Return the slot identifier.
    #[must_use]
    pub const fn get(self) -> u8 {
        self.0
    }
}

/// Closed movement direction vocabulary shared by input and gameplay consumers.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub enum Direction {
    /// Move north.
    North,
    /// Move north-east.
    NorthEast,
    /// Move east.
    East,
    /// Move south-east.
    SouthEast,
    /// Move south.
    South,
    /// Move south-west.
    SouthWest,
    /// Move west.
    West,
    /// Move north-west.
    NorthWest,
}

/// Non-zero quantity used by item movement commands and item state events.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct ItemCount(NonZeroU16);

impl ItemCount {
    /// Construct a non-zero item count.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::ZeroItemCount`] when `value` is zero.
    pub fn try_new(value: u16) -> Result<Self, DomainError> {
        NonZeroU16::new(value)
            .map(Self)
            .ok_or(DomainError::ZeroItemCount)
    }

    /// Return the non-zero count.
    #[must_use]
    pub const fn get(self) -> u16 {
        self.0.get()
    }
}

/// Non-zero capacity of one open container.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct ContainerCapacity(NonZeroU16);

impl ContainerCapacity {
    /// Construct a non-zero container capacity.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::ZeroContainerCapacity`] when `value` is zero.
    pub fn try_new(value: u16) -> Result<Self, DomainError> {
        NonZeroU16::new(value)
            .map(Self)
            .ok_or(DomainError::ZeroContainerCapacity)
    }

    /// Return the non-zero capacity.
    #[must_use]
    pub const fn get(self) -> u16 {
        self.0.get()
    }
}

/// Current and maximum value for a bounded player resource.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ResourceValue {
    current: u32,
    max: u32,
}

impl ResourceValue {
    /// Construct a validated resource range.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::InvalidResourceRange`] when `max` is zero or
    /// `current` exceeds `max`.
    pub fn try_new(current: u32, max: u32) -> Result<Self, DomainError> {
        if max == 0 || current > max {
            Err(DomainError::InvalidResourceRange { current, max })
        } else {
            Ok(Self { current, max })
        }
    }

    /// Return the current value.
    #[must_use]
    pub const fn current(self) -> u32 {
        self.current
    }

    /// Return the declared maximum value.
    #[must_use]
    pub const fn max(self) -> u32 {
        self.max
    }
}
