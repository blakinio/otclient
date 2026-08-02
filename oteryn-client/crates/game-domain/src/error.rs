use oteryn_foundation::SessionGeneration;
use std::fmt::{self, Display, Formatter};

/// Identifies a gameplay identifier rejected at a public boundary.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum IdentifierKind {
    /// Canonical world entity identifier.
    Entity,
    /// Canonical creature identifier.
    Creature,
    /// Canonical item instance identifier.
    Item,
    /// Canonical item type identifier.
    ItemType,
    /// Canonical container identifier.
    Container,
}

impl Display for IdentifierKind {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        let name = match self {
            Self::Entity => "entity",
            Self::Creature => "creature",
            Self::Item => "item",
            Self::ItemType => "item type",
            Self::Container => "container",
        };
        formatter.write_str(name)
    }
}

/// Stable validation failures produced by protocol-neutral gameplay contracts.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum DomainError {
    /// An identifier that must be non-zero was zero.
    ZeroIdentifier(IdentifierKind),
    /// A bounded text type was configured with an unusable zero-byte limit.
    ZeroTextLimit,
    /// External text exceeded its public byte limit.
    TextTooLong {
        /// Maximum accepted UTF-8 byte length.
        max: usize,
        /// Actual UTF-8 byte length.
        actual: usize,
    },
    /// An envelope version is not supported by this crate revision.
    UnsupportedEnvelopeVersion(u16),
    /// A session-scoped value belongs to a previous or future session.
    StaleSession {
        /// Session generation expected by the caller.
        expected: SessionGeneration,
        /// Session generation carried by the value.
        actual: SessionGeneration,
    },
    /// A nested handle does not belong to its containing envelope session.
    SessionMismatch {
        /// Generation declared by the envelope.
        envelope: SessionGeneration,
        /// Generation carried by the nested value.
        value: SessionGeneration,
    },
    /// An item movement count must be non-zero.
    ZeroItemCount,
    /// A container capacity must be non-zero.
    ZeroContainerCapacity,
    /// A resource range was invalid.
    InvalidResourceRange {
        /// Current resource value.
        current: u32,
        /// Declared maximum resource value.
        max: u32,
    },
}

impl Display for DomainError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> fmt::Result {
        match self {
            Self::ZeroIdentifier(kind) => write!(formatter, "{kind} identifier must be non-zero"),
            Self::ZeroTextLimit => formatter.write_str("bounded text limit must be non-zero"),
            Self::TextTooLong { max, actual } => {
                write!(formatter, "bounded text length {actual} exceeds limit {max}")
            }
            Self::UnsupportedEnvelopeVersion(version) => {
                write!(formatter, "unsupported gameplay envelope version {version}")
            }
            Self::StaleSession { expected, actual } => write!(
                formatter,
                "session generation mismatch: expected {expected}, got {actual}"
            ),
            Self::SessionMismatch { envelope, value } => write!(
                formatter,
                "nested value session generation {value} does not match envelope generation {envelope}"
            ),
            Self::ZeroItemCount => formatter.write_str("item count must be non-zero"),
            Self::ZeroContainerCapacity => {
                formatter.write_str("container capacity must be non-zero")
            }
            Self::InvalidResourceRange { current, max } => write!(
                formatter,
                "resource value {current} is invalid for declared maximum {max}"
            ),
        }
    }
}

impl std::error::Error for DomainError {}
