use oteryn_asset_types::AssetError;
use std::error::Error;
use std::fmt::{self, Display, Formatter};

/// Stable, path-free failures produced by the immutable asset runtime.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum RuntimeError {
    /// A pack generation must be non-zero.
    InvalidGeneration,
    /// Runtime limits exceed the synthetic-v1 schema bounds or are unusable.
    InvalidLimits,
    /// Checked size arithmetic could not be represented.
    ArithmeticOverflow,
    /// The already-opened object could not be read completely.
    ObjectUnavailable,
    /// The object exceeds the configured pack-byte limit.
    ObjectTooLarge,
    /// The decoded record count exceeds the configured runtime limit.
    TooManyRecords,
    /// One decoded payload exceeds the configured runtime limit.
    PayloadTooLarge,
    /// A logical handle belongs to a different pack generation.
    StaleHandle,
    /// A logical handle does not identify a record in the current pack.
    UnknownAsset,
    /// The synthetic-v1 schema rejected the object.
    Asset(AssetError),
}

impl Display for RuntimeError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let message = match self {
            Self::InvalidGeneration => "asset pack generation must be non-zero",
            Self::InvalidLimits => "asset runtime limits are invalid",
            Self::ArithmeticOverflow => "asset runtime size arithmetic overflowed",
            Self::ObjectUnavailable => "asset pack object is unavailable",
            Self::ObjectTooLarge => "asset pack object exceeds the runtime limit",
            Self::TooManyRecords => "asset pack record count exceeds the runtime limit",
            Self::PayloadTooLarge => "asset payload exceeds the runtime limit",
            Self::StaleHandle => "asset handle belongs to a stale pack generation",
            Self::UnknownAsset => "asset handle is not present in the current pack",
            Self::Asset(error) => return Display::fmt(error, formatter),
        };
        formatter.write_str(message)
    }
}

impl Error for RuntimeError {
    fn source(&self) -> Option<&(dyn Error + 'static)> {
        match self {
            Self::Asset(error) => Some(error),
            _ => None,
        }
    }
}

impl From<AssetError> for RuntimeError {
    fn from(value: AssetError) -> Self {
        Self::Asset(value)
    }
}
