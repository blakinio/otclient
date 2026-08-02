use crate::{DomainError, IdentifierKind, SessionToken};
use oteryn_foundation::SessionGeneration;
use std::num::NonZeroU32;

macro_rules! identifier_type {
    ($name:ident, $kind:expr, $description:literal) => {
        #[doc = $description]
        #[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
        pub struct $name(NonZeroU32);

        impl $name {
            /// Construct an identifier from an externally supplied numeric value.
            ///
            /// # Errors
            ///
            /// Returns [`DomainError::ZeroIdentifier`] when `value` is zero.
            pub fn try_new(value: u32) -> Result<Self, DomainError> {
                NonZeroU32::new(value)
                    .map(Self)
                    .ok_or(DomainError::ZeroIdentifier($kind))
            }

            /// Return the canonical non-zero numeric value.
            #[must_use]
            pub const fn get(self) -> u32 {
                self.0.get()
            }
        }
    };
}

identifier_type!(
    EntityId,
    IdentifierKind::Entity,
    "Canonical protocol-neutral identifier for one world entity instance."
);
identifier_type!(
    CreatureId,
    IdentifierKind::Creature,
    "Canonical protocol-neutral identifier for one creature instance."
);
identifier_type!(
    ItemId,
    IdentifierKind::Item,
    "Canonical protocol-neutral identifier for one item instance."
);
identifier_type!(
    ItemTypeId,
    IdentifierKind::ItemType,
    "Canonical protocol-neutral identifier for one item definition."
);
identifier_type!(
    ContainerId,
    IdentifierKind::Container,
    "Canonical protocol-neutral identifier for one open container instance."
);

/// One typed identifier fenced to a specific gameplay session generation.
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord, Hash)]
pub struct SessionHandle<T> {
    session: SessionGeneration,
    id: T,
}

impl<T> SessionHandle<T> {
    /// Bind a canonical identifier to one gameplay session.
    #[must_use]
    pub const fn new(session: SessionToken, id: T) -> Self {
        Self {
            session: session.generation(),
            id,
        }
    }

    /// Return the session generation carried by this handle.
    #[must_use]
    pub const fn session(self) -> SessionGeneration
    where
        T: Copy,
    {
        self.session
    }

    /// Verify that this handle belongs to `session`.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::SessionMismatch`] when generations differ.
    pub fn ensure_session(&self, session: SessionToken) -> Result<(), DomainError> {
        let envelope = session.generation();
        if self.session == envelope {
            Ok(())
        } else {
            Err(DomainError::SessionMismatch {
                envelope,
                value: self.session,
            })
        }
    }
}

impl<T: Copy> SessionHandle<T> {
    /// Return the typed identifier carried by this handle.
    #[must_use]
    pub const fn id(self) -> T {
        self.id
    }
}

/// Session-scoped canonical world entity handle.
pub type EntityHandle = SessionHandle<EntityId>;
/// Session-scoped canonical creature handle.
pub type CreatureHandle = SessionHandle<CreatureId>;
/// Session-scoped canonical item instance handle.
pub type ItemHandle = SessionHandle<ItemId>;
/// Session-scoped canonical open-container handle.
pub type ContainerHandle = SessionHandle<ContainerId>;
