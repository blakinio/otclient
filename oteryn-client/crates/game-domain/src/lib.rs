//! Protocol-neutral public gameplay contracts for the Oteryn Rust client.
//!
//! This crate owns canonical session-scoped identifiers, bounded gameplay
//! values and the closed version-one [`GameEvent`] and [`GameCommand`]
//! envelopes. It intentionally contains no Canary layouts, socket ownership,
//! mutable simulation, renderer, UI, platform or application composition.
//!
//! Identifier types are deliberately non-interchangeable:
//!
//! ```compile_fail
//! use oteryn_game_domain::{EntityHandle, ItemHandle};
//!
//! fn accepts_entity(_: EntityHandle) {}
//!
//! fn reject_item(item: ItemHandle) {
//!     accepts_entity(item);
//! }
//! ```

mod command;
mod envelope;
mod error;
mod event;
mod ids;
mod location;
mod session;
mod text;
mod values;

pub use command::{GameCommand, GameCommandEnvelope};
pub use envelope::EnvelopeVersion;
pub use error::{DomainError, IdentifierKind};
pub use event::{EntityKind, GameEvent, GameEventEnvelope, SessionEndReason};
pub use ids::{
    ContainerHandle, ContainerId, CreatureHandle, CreatureId, EntityHandle, EntityId, ItemHandle,
    ItemId, ItemTypeId, SessionHandle,
};
pub use location::{ObjectLocation, ObjectTarget};
pub use session::SessionToken;
pub use text::{BoundedText, NameText};
pub use values::{
    ContainerCapacity, ContainerSlot, Direction, Floor, InventorySlot, ItemCount, ResourceValue,
    StackIndex, TilePosition,
};

#[cfg(test)]
mod tests {
    use super::*;
    use oteryn_foundation::SessionGeneration;
    use std::collections::BTreeSet;

    fn token(value: u64) -> SessionToken {
        SessionToken::new(SessionGeneration::new(value))
    }

    fn position() -> TilePosition {
        TilePosition::new(100, 200, Floor::new(7))
    }

    #[test]
    fn identifiers_are_non_zero_ordered_and_hash_stable() -> Result<(), DomainError> {
        assert_eq!(
            EntityId::try_new(0),
            Err(DomainError::ZeroIdentifier(IdentifierKind::Entity))
        );

        let first = EntityId::try_new(1)?;
        let second = EntityId::try_new(2)?;
        let mut values = BTreeSet::new();
        assert!(values.insert(second));
        assert!(values.insert(first));
        assert_eq!(values.into_iter().collect::<Vec<_>>(), vec![first, second]);
        Ok(())
    }

    #[test]
    fn handles_reject_wrong_envelope_generation() -> Result<(), DomainError> {
        let envelope_session = token(4);
        let foreign_session = token(5);
        let player = EntityHandle::new(foreign_session, EntityId::try_new(10)?);
        let event = GameEvent::BootstrapCompleted {
            player,
            position: position(),
        };

        assert_eq!(
            GameEventEnvelope::v1(envelope_session, event),
            Err(DomainError::SessionMismatch {
                envelope: SessionGeneration::new(4),
                value: SessionGeneration::new(5),
            })
        );
        Ok(())
    }

    #[test]
    fn stale_envelopes_fail_deterministically() -> Result<(), DomainError> {
        let session = token(9);
        let command = GameCommandEnvelope::v1(
            session,
            GameCommand::Step {
                direction: Direction::North,
            },
        )?;

        assert_eq!(
            command.ensure_current(SessionGeneration::new(10)),
            Err(DomainError::StaleSession {
                expected: SessionGeneration::new(10),
                actual: SessionGeneration::new(9),
            })
        );
        Ok(())
    }

    #[test]
    fn nested_command_locations_are_session_checked() -> Result<(), DomainError> {
        let envelope_session = token(20);
        let foreign_session = token(21);
        let item = ItemHandle::new(envelope_session, ItemId::try_new(100)?);
        let foreign_container = ContainerHandle::new(foreign_session, ContainerId::try_new(3)?);
        let command = GameCommand::MoveItem {
            item,
            from: ObjectLocation::Tile {
                position: position(),
                stack: StackIndex::new(2),
            },
            to: ObjectLocation::Container {
                container: foreign_container,
                slot: ContainerSlot::new(1),
            },
            count: ItemCount::try_new(1)?,
        };

        assert_eq!(
            GameCommandEnvelope::v1(envelope_session, command),
            Err(DomainError::SessionMismatch {
                envelope: SessionGeneration::new(20),
                value: SessionGeneration::new(21),
            })
        );
        Ok(())
    }

    #[test]
    fn bounded_text_rejects_oversize_and_redacts_debug() -> Result<(), DomainError> {
        let text = BoundedText::<8>::try_new("secret")?;
        assert_eq!(text.as_str(), "secret");
        assert_eq!(text.len(), 6);
        assert!(!text.is_empty());

        let debug = format!("{text:?}");
        assert!(!debug.contains("secret"));
        assert!(debug.contains("redacted"));
        assert_eq!(
            BoundedText::<4>::try_new("12345"),
            Err(DomainError::TextTooLong { max: 4, actual: 5 })
        );
        assert_eq!(
            BoundedText::<0>::try_new(""),
            Err(DomainError::ZeroTextLimit)
        );
        Ok(())
    }

    #[test]
    fn versions_counts_capacities_and_resources_are_checked() -> Result<(), DomainError> {
        assert_eq!(
            EnvelopeVersion::try_new(2),
            Err(DomainError::UnsupportedEnvelopeVersion(2))
        );
        assert_eq!(ItemCount::try_new(0), Err(DomainError::ZeroItemCount));
        assert_eq!(
            ContainerCapacity::try_new(0),
            Err(DomainError::ZeroContainerCapacity)
        );
        assert_eq!(
            ResourceValue::try_new(11, 10),
            Err(DomainError::InvalidResourceRange {
                current: 11,
                max: 10,
            })
        );
        assert_eq!(ResourceValue::try_new(5, 10)?.current(), 5);
        Ok(())
    }

    #[test]
    fn event_debug_does_not_disclose_bounded_external_text() -> Result<(), DomainError> {
        let session = token(30);
        let entity = EntityHandle::new(session, EntityId::try_new(7)?);
        let event = GameEventEnvelope::v1(
            session,
            GameEvent::EntityAppeared {
                entity,
                kind: EntityKind::NonPlayerCharacter,
                name: Some(NameText::try_new("hidden-name")?),
                position: position(),
                stack: StackIndex::new(1),
            },
        )?;

        let debug = format!("{event:?}");
        assert!(!debug.contains("hidden-name"));
        assert!(debug.contains("redacted"));
        event.ensure_current(SessionGeneration::new(30))?;
        Ok(())
    }
}
