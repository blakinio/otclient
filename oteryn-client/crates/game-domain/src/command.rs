use crate::{
    CreatureHandle, Direction, DomainError, EnvelopeVersion, ItemCount, ItemHandle, ObjectLocation,
    ObjectTarget, SessionToken,
};
use oteryn_foundation::SessionGeneration;

/// Closed minimum command vocabulary accepted by gameplay producers.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub enum GameCommand {
    /// Request one semantic movement step.
    Step {
        /// Requested movement direction.
        direction: Direction,
    },
    /// Stop an active movement sequence without ending the session.
    StopMovement,
    /// Inspect one canonical semantic target.
    LookAt {
        /// Target to inspect.
        target: ObjectTarget,
    },
    /// Use or interact with one canonical semantic target.
    Use {
        /// Target to use.
        target: ObjectTarget,
    },
    /// Move a non-zero quantity of one item between canonical locations.
    MoveItem {
        /// Session-scoped item instance.
        item: ItemHandle,
        /// Source location.
        from: ObjectLocation,
        /// Destination location.
        to: ObjectLocation,
        /// Non-zero quantity to move.
        count: ItemCount,
    },
    /// Select one session-scoped creature as the attack target.
    SetAttackTarget {
        /// Creature to target.
        target: CreatureHandle,
    },
    /// Clear the active attack target.
    ClearAttackTarget,
    /// Request a clean gameplay-session logout.
    Logout,
}

impl GameCommand {
    fn ensure_session(&self, session: SessionToken) -> Result<(), DomainError> {
        match self {
            Self::LookAt { target } | Self::Use { target } => target.ensure_session(session),
            Self::MoveItem { item, from, to, .. } => {
                item.ensure_session(session)?;
                from.ensure_session(session)?;
                to.ensure_session(session)
            }
            Self::SetAttackTarget { target } => target.ensure_session(session),
            Self::Step { .. } | Self::StopMovement | Self::ClearAttackTarget | Self::Logout => {
                Ok(())
            }
        }
    }
}

/// Versioned, session-fenced semantic gameplay command.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct GameCommandEnvelope {
    version: EnvelopeVersion,
    session: SessionToken,
    command: GameCommand,
}

impl GameCommandEnvelope {
    /// Construct a version-one command envelope.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::SessionMismatch`] when a nested handle belongs to
    /// a different session generation.
    pub fn v1(session: SessionToken, command: GameCommand) -> Result<Self, DomainError> {
        Self::try_new(EnvelopeVersion::V1.get(), session, command)
    }

    /// Construct a validated command envelope from a numeric contract version.
    ///
    /// # Errors
    ///
    /// Returns a stable version or session validation error.
    pub fn try_new(
        version: u16,
        session: SessionToken,
        command: GameCommand,
    ) -> Result<Self, DomainError> {
        let version = EnvelopeVersion::try_new(version)?;
        command.ensure_session(session)?;
        Ok(Self {
            version,
            session,
            command,
        })
    }

    /// Return the accepted contract version.
    #[must_use]
    pub const fn version(self) -> EnvelopeVersion {
        self.version
    }

    /// Return the session token fencing this command.
    #[must_use]
    pub const fn session(self) -> SessionToken {
        self.session
    }

    /// Return the closed semantic command payload.
    #[must_use]
    pub const fn command(self) -> GameCommand {
        self.command
    }

    /// Verify that this envelope still belongs to the caller's current session.
    ///
    /// # Errors
    ///
    /// Returns [`DomainError::StaleSession`] or
    /// [`DomainError::SessionMismatch`] on generation mismatch.
    pub fn ensure_current(self, current: SessionGeneration) -> Result<(), DomainError> {
        self.session.ensure_current(current)?;
        self.command.ensure_session(self.session)
    }
}
