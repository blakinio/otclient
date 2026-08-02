use crate::RuntimeError;
use oteryn_asset_types::AssetId;
use std::num::NonZeroU64;

/// Non-zero generation identifying one immutable opened pack instance.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct PackGeneration(NonZeroU64);

impl PackGeneration {
    /// Construct a pack generation.
    ///
    /// # Errors
    ///
    /// Returns [`RuntimeError::InvalidGeneration`] for zero.
    pub fn new(value: u64) -> Result<Self, RuntimeError> {
        NonZeroU64::new(value)
            .map(Self)
            .ok_or(RuntimeError::InvalidGeneration)
    }

    /// Return the numeric generation.
    #[must_use]
    pub const fn get(self) -> u64 {
        self.0.get()
    }
}

/// Generation-fenced logical reference to one asset record.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct AssetHandle {
    generation: PackGeneration,
    id: AssetId,
}

impl AssetHandle {
    /// Construct a logical handle for a generation and asset identifier.
    #[must_use]
    pub const fn new(generation: PackGeneration, id: AssetId) -> Self {
        Self { generation, id }
    }

    /// Return the pack generation carried by the handle.
    #[must_use]
    pub const fn generation(self) -> PackGeneration {
        self.generation
    }

    /// Return the canonical asset identifier.
    #[must_use]
    pub const fn id(self) -> AssetId {
        self.id
    }
}
