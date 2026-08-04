use crate::CANARY_NETWORK_MESSAGE_MAX_BYTES;
use crate::inbound::{CanaryInboundBootstrapState, CanaryInboundError};
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{
    DomainError, EntityHandle, Floor, GameEvent, GameEventEnvelope, StackIndex, TilePosition,
};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};
use std::fmt::{Display, Formatter};

/// Canary Current server opcode for removing one thing from a tile stack.
pub const OPCODE_REMOVE_TILE_THING: u8 = 0x6C;
/// Canary Current server opcode for one non-teleport creature movement.
pub const OPCODE_MOVE_CREATURE: u8 = 0x6D;

const MAP_MAX_LAYERS: u8 = 16;
const MAX_TILE_STACK_INDEX: u8 = 9;

/// Read-only caller-owned identity resolution used after complete wire parsing.
///
/// The adapter invokes this contract only after opcode, positions, stack bounds,
/// message length and trailing-data validation have succeeded. Implementations
/// must observe authoritative caller state without mutating simulation. They
/// return `None` whenever identity or destination ordering is unknown or
/// ambiguous.
pub trait CanaryEntityReconciliationResolver {
    /// Resolve one non-local entity being removed from a canonical tile stack.
    fn resolve_removed_entity(
        &self,
        position: TilePosition,
        stack: StackIndex,
    ) -> Option<EntityHandle>;

    /// Resolve one non-local entity movement and its destination stack ordering.
    fn resolve_moved_entity(
        &self,
        from: TilePosition,
        from_stack: StackIndex,
        to: TilePosition,
    ) -> Option<ResolvedCanaryEntityMovement>;
}

/// Caller-owned semantic result for one completely parsed remote movement.
#[derive(Debug, Clone, Copy, PartialEq, Eq, Hash)]
pub struct ResolvedCanaryEntityMovement {
    entity: EntityHandle,
    destination_stack: StackIndex,
}

impl ResolvedCanaryEntityMovement {
    /// Construct one read-only resolver result.
    #[must_use]
    pub const fn new(entity: EntityHandle, destination_stack: StackIndex) -> Self {
        Self {
            entity,
            destination_stack,
        }
    }

    /// Return the session-fenced entity selected by caller-owned state.
    #[must_use]
    pub const fn entity(self) -> EntityHandle {
        self.entity
    }

    /// Return caller-owned destination ordering for the moved entity.
    #[must_use]
    pub const fn destination_stack(self) -> StackIndex {
        self.destination_stack
    }
}

/// Stable failure returned by Current entity reconciliation decoding.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum CanaryReconciliationError {
    /// Existing bounded inbound validation failed.
    Inbound(CanaryInboundError),
    /// Caller-owned state could not resolve one unambiguous entity identity.
    IdentityUnavailable,
    /// The message resolved to the local player, whose map-strip branch is unsupported.
    LocalPlayerUnsupported,
    /// Caller-owned destination ordering exceeded the Current visible-stack bound.
    InvalidDestinationStack,
}

impl Display for CanaryReconciliationError {
    fn fmt(&self, formatter: &mut Formatter<'_>) -> std::fmt::Result {
        match self {
            Self::Inbound(error) => Display::fmt(error, formatter),
            Self::IdentityUnavailable => {
                formatter.write_str("caller-owned world state could not resolve the Canary entity")
            }
            Self::LocalPlayerUnsupported => formatter
                .write_str("local-player Canary movement or removal requires map reconciliation"),
            Self::InvalidDestinationStack => formatter
                .write_str("caller-owned destination stack exceeds the Current visible bound"),
        }
    }
}

impl std::error::Error for CanaryReconciliationError {}

impl From<CanaryInboundError> for CanaryReconciliationError {
    fn from(error: CanaryInboundError) -> Self {
        Self::Inbound(error)
    }
}

impl From<ProtocolError> for CanaryReconciliationError {
    fn from(error: ProtocolError) -> Self {
        Self::Inbound(CanaryInboundError::Protocol(error))
    }
}

impl From<DomainError> for CanaryReconciliationError {
    fn from(error: DomainError) -> Self {
        Self::Inbound(CanaryInboundError::Domain(error))
    }
}

/// Decode one complete Current remote non-teleport creature movement.
///
/// The accepted logical message is exactly opcode `0x6D`, old `Position`, old
/// stack index below ten and new `Position`. The source-reachable local-player
/// branch appends map strips and is deliberately rejected after resolution.
/// Success emits only [`GameEvent::EntityMoved`] using a session-fenced entity
/// and destination stack supplied by read-only caller-owned world state.
///
/// # Errors
///
/// Rejects stale/pre-bootstrap/terminal state, malformed or same positions,
/// invalid floor/stack bounds, truncation, oversize, trailing data, unresolved
/// identity, local-player resolution, invalid destination ordering and session
/// mismatch. The resolver is never invoked for malformed input.
pub fn decode_current_remote_entity_movement<R: CanaryEntityReconciliationResolver>(
    input: &[u8],
    state: &CanaryInboundBootstrapState,
    current: SessionGeneration,
    resolver: &R,
) -> Result<GameEventEnvelope, CanaryReconciliationError> {
    let local_player = ensure_reconciliation_ready(state, current)?;

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    expect_opcode(&mut reader, OPCODE_MOVE_CREATURE)?;
    let from = read_position(&mut reader)?;
    let from_stack = read_stack(&mut reader)?;
    let to = read_position(&mut reader)?;
    if from == to {
        return Err(unknown_value().into());
    }
    reader.finish(TrailingDataPolicy::Reject)?;

    let resolved = resolver
        .resolve_moved_entity(from, from_stack, to)
        .ok_or(CanaryReconciliationError::IdentityUnavailable)?;
    if resolved.entity() == local_player {
        return Err(CanaryReconciliationError::LocalPlayerUnsupported);
    }
    if resolved.destination_stack().get() > MAX_TILE_STACK_INDEX {
        return Err(CanaryReconciliationError::InvalidDestinationStack);
    }

    let envelope = GameEventEnvelope::v1(
        state.session(),
        GameEvent::EntityMoved {
            entity: resolved.entity(),
            from,
            to,
            stack: resolved.destination_stack(),
        },
    )?;
    envelope.ensure_current(current)?;
    Ok(envelope)
}

/// Decode one complete Current remote-entity removal from a tile stack.
///
/// The accepted logical message is exactly opcode `0x6C`, one `Position` and a
/// stack index below ten. `RemoveTileThing` is generic in the producer; this
/// bounded decoder admits only an entity that caller-owned authoritative state
/// resolves unambiguously. Items and the local-player teleport/map-reset branch
/// remain unsupported. Success emits only [`GameEvent::EntityRemoved`].
///
/// # Errors
///
/// Rejects stale/pre-bootstrap/terminal state, malformed floor/stack bounds,
/// truncation, oversize, trailing data, unresolved identity, local-player
/// resolution and session mismatch. The resolver is never invoked for malformed
/// input.
pub fn decode_current_remote_entity_removal<R: CanaryEntityReconciliationResolver>(
    input: &[u8],
    state: &CanaryInboundBootstrapState,
    current: SessionGeneration,
    resolver: &R,
) -> Result<GameEventEnvelope, CanaryReconciliationError> {
    let local_player = ensure_reconciliation_ready(state, current)?;

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    expect_opcode(&mut reader, OPCODE_REMOVE_TILE_THING)?;
    let position = read_position(&mut reader)?;
    let stack = read_stack(&mut reader)?;
    reader.finish(TrailingDataPolicy::Reject)?;

    let entity = resolver
        .resolve_removed_entity(position, stack)
        .ok_or(CanaryReconciliationError::IdentityUnavailable)?;
    if entity == local_player {
        return Err(CanaryReconciliationError::LocalPlayerUnsupported);
    }

    let envelope = GameEventEnvelope::v1(
        state.session(),
        GameEvent::EntityRemoved { entity, position },
    )?;
    envelope.ensure_current(current)?;
    Ok(envelope)
}

fn ensure_reconciliation_ready(
    state: &CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<EntityHandle, CanaryReconciliationError> {
    state
        .session()
        .ensure_current(current)
        .map_err(CanaryInboundError::from)?;
    if !state.bootstrap_completed() || state.session_ended() {
        return Err(CanaryInboundError::InvalidOrder.into());
    }
    state
        .local_player()
        .ok_or_else(|| CanaryInboundError::InvalidOrder.into())
}

fn read_position(
    reader: &mut BoundedReader<'_>,
) -> Result<TilePosition, CanaryReconciliationError> {
    let x = reader.read_u16_le()?;
    let y = reader.read_u16_le()?;
    let z = reader.read_u8()?;
    if z >= MAP_MAX_LAYERS {
        return Err(unknown_value().into());
    }
    Ok(TilePosition::new(x, y, Floor::new(z)))
}

fn read_stack(reader: &mut BoundedReader<'_>) -> Result<StackIndex, CanaryReconciliationError> {
    let stack = reader.read_u8()?;
    if stack > MAX_TILE_STACK_INDEX {
        return Err(unknown_value().into());
    }
    Ok(StackIndex::new(stack))
}

fn expect_opcode(
    reader: &mut BoundedReader<'_>,
    expected: u8,
) -> Result<(), CanaryReconciliationError> {
    if reader.read_u8()? == expected {
        Ok(())
    } else {
        Err(unknown_value().into())
    }
}

const fn unknown_value() -> ProtocolError {
    ProtocolError::new(ProtocolErrorKind::UnknownValue)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::inbound::decode_current_pending_state_entered;
    use crate::map::decode_current_local_player_only_map;
    use oteryn_game_domain::{EntityId, SessionToken};
    use std::error::Error;
    use std::num::ParseIntError;

    const LOCAL_PLAYER_INITIALIZATION_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/local-player-initialization.hex"
    );
    const ALLOW_BUG_REPORT_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/allow-bug-report.hex"
    );
    const TIBIA_TIME_FIXTURE: &str =
        include_str!("../../../tests/integration/canary-world-protocol/fixtures/tibia-time.hex");
    const PENDING_STATE_ENTERED_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/pending-state-entered.hex"
    );
    const ENTER_WORLD_FIXTURE: &str =
        include_str!("../../../tests/integration/canary-world-protocol/fixtures/enter-world.hex");
    const LOCAL_PLAYER_ONLY_MAP_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/local-player-only-map.hex"
    );
    const REMOTE_ENTITY_MOVEMENT_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/remote-entity-movement.hex"
    );
    const REMOTE_ENTITY_MOVEMENT_TRAILING_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/remote-entity-movement-trailing.hex"
    );
    const REMOTE_ENTITY_REMOVAL_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/remote-entity-removal.hex"
    );
    const REMOTE_ENTITY_REMOVAL_INVALID_STACK_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/remote-entity-removal-invalid-stack.hex"
    );

    #[derive(Debug, Clone, Copy)]
    struct SyntheticResolver {
        entity: EntityHandle,
        from: TilePosition,
        from_stack: StackIndex,
        to: TilePosition,
        destination_stack: StackIndex,
    }

    impl CanaryEntityReconciliationResolver for SyntheticResolver {
        fn resolve_removed_entity(
            &self,
            position: TilePosition,
            stack: StackIndex,
        ) -> Option<EntityHandle> {
            (position == self.from && stack == self.from_stack).then_some(self.entity)
        }

        fn resolve_moved_entity(
            &self,
            from: TilePosition,
            from_stack: StackIndex,
            to: TilePosition,
        ) -> Option<ResolvedCanaryEntityMovement> {
            (from == self.from && from_stack == self.from_stack && to == self.to).then_some(
                ResolvedCanaryEntityMovement::new(self.entity, self.destination_stack),
            )
        }
    }

    fn parse_hex_fixture(input: &str) -> Result<Vec<u8>, ParseIntError> {
        input
            .split_whitespace()
            .map(|token| u8::from_str_radix(token, 16))
            .collect()
    }

    fn ready_state(
        generation: u64,
    ) -> Result<(CanaryInboundBootstrapState, SessionGeneration), Box<dyn Error>> {
        let current = SessionGeneration::new(generation);
        let mut state = CanaryInboundBootstrapState::new(SessionToken::new(current));
        state.decode_local_player_initialization(
            &parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?,
            current,
        )?;
        state.decode_allow_bug_report(&parse_hex_fixture(ALLOW_BUG_REPORT_FIXTURE)?, current)?;
        state.decode_tibia_time(&parse_hex_fixture(TIBIA_TIME_FIXTURE)?, current)?;
        decode_current_pending_state_entered(
            &parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?,
            &mut state,
            current,
        )?;
        state.decode_enter_world(&parse_hex_fixture(ENTER_WORLD_FIXTURE)?, current)?;
        decode_current_local_player_only_map(
            &parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?,
            &mut state,
            current,
        )?;
        Ok((state, current))
    }

    fn resolver(state: &CanaryInboundBootstrapState) -> Result<SyntheticResolver, DomainError> {
        Ok(SyntheticResolver {
            entity: EntityHandle::new(state.session(), EntityId::try_new(0x0203_0405)?),
            from: TilePosition::new(0x1235, 0x5679, Floor::new(7)),
            from_stack: StackIndex::new(1),
            to: TilePosition::new(0x1236, 0x5679, Floor::new(7)),
            destination_stack: StackIndex::new(2),
        })
    }

    #[test]
    fn exact_remote_movement_emits_entity_moved() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(80)?;
        let resolver = resolver(&state)?;
        let envelope = decode_current_remote_entity_movement(
            &parse_hex_fixture(REMOTE_ENTITY_MOVEMENT_FIXTURE)?,
            &state,
            current,
            &resolver,
        )?;
        assert_eq!(
            envelope.event(),
            &GameEvent::EntityMoved {
                entity: resolver.entity,
                from: resolver.from,
                to: resolver.to,
                stack: resolver.destination_stack,
            }
        );
        Ok(())
    }

    #[test]
    fn exact_remote_removal_emits_entity_removed() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(81)?;
        let resolver = resolver(&state)?;
        let envelope = decode_current_remote_entity_removal(
            &parse_hex_fixture(REMOTE_ENTITY_REMOVAL_FIXTURE)?,
            &state,
            current,
            &resolver,
        )?;
        assert_eq!(
            envelope.event(),
            &GameEvent::EntityRemoved {
                entity: resolver.entity,
                position: resolver.from,
            }
        );
        Ok(())
    }

    #[test]
    fn every_truncated_prefix_fails_before_resolution() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(82)?;
        let resolver = resolver(&state)?;
        let movement = parse_hex_fixture(REMOTE_ENTITY_MOVEMENT_FIXTURE)?;
        for length in 0..movement.len() {
            assert_eq!(
                decode_current_remote_entity_movement(
                    &movement[..length],
                    &state,
                    current,
                    &resolver,
                ),
                Err(CanaryReconciliationError::Inbound(
                    CanaryInboundError::Protocol(ProtocolError::new(ProtocolErrorKind::Truncated)),
                ))
            );
        }

        let removal = parse_hex_fixture(REMOTE_ENTITY_REMOVAL_FIXTURE)?;
        for length in 0..removal.len() {
            assert_eq!(
                decode_current_remote_entity_removal(
                    &removal[..length],
                    &state,
                    current,
                    &resolver,
                ),
                Err(CanaryReconciliationError::Inbound(
                    CanaryInboundError::Protocol(ProtocolError::new(ProtocolErrorKind::Truncated)),
                ))
            );
        }
        Ok(())
    }

    #[test]
    fn closed_fields_and_trailing_data_fail_closed() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(83)?;
        let resolver = resolver(&state)?;
        let trailing = parse_hex_fixture(REMOTE_ENTITY_MOVEMENT_TRAILING_FIXTURE)?;
        assert_eq!(
            decode_current_remote_entity_movement(&trailing, &state, current, &resolver),
            Err(CanaryReconciliationError::Inbound(
                CanaryInboundError::Protocol(ProtocolError::new(ProtocolErrorKind::TrailingData)),
            ))
        );

        let invalid_stack = parse_hex_fixture(REMOTE_ENTITY_REMOVAL_INVALID_STACK_FIXTURE)?;
        assert_eq!(
            decode_current_remote_entity_removal(&invalid_stack, &state, current, &resolver,),
            Err(CanaryReconciliationError::Inbound(
                CanaryInboundError::Protocol(ProtocolError::new(ProtocolErrorKind::UnknownValue)),
            ))
        );

        let same_position = [
            0x6D, 0x35, 0x12, 0x79, 0x56, 0x07, 0x01, 0x35, 0x12, 0x79, 0x56, 0x07,
        ];
        assert_eq!(
            decode_current_remote_entity_movement(&same_position, &state, current, &resolver,),
            Err(CanaryReconciliationError::Inbound(
                CanaryInboundError::Protocol(ProtocolError::new(ProtocolErrorKind::UnknownValue)),
            ))
        );
        Ok(())
    }

    #[test]
    fn caller_owned_resolution_fails_closed() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(84)?;
        let base = resolver(&state)?;
        let movement = parse_hex_fixture(REMOTE_ENTITY_MOVEMENT_FIXTURE)?;
        let removal = parse_hex_fixture(REMOTE_ENTITY_REMOVAL_FIXTURE)?;

        let unresolved = SyntheticResolver {
            from: TilePosition::new(1, 2, Floor::new(3)),
            ..base
        };
        assert_eq!(
            decode_current_remote_entity_movement(&movement, &state, current, &unresolved,),
            Err(CanaryReconciliationError::IdentityUnavailable)
        );
        assert_eq!(
            decode_current_remote_entity_removal(&removal, &state, current, &unresolved,),
            Err(CanaryReconciliationError::IdentityUnavailable)
        );

        let local = SyntheticResolver {
            entity: state.local_player().ok_or("missing local player")?,
            ..base
        };
        assert_eq!(
            decode_current_remote_entity_movement(&movement, &state, current, &local),
            Err(CanaryReconciliationError::LocalPlayerUnsupported)
        );
        assert_eq!(
            decode_current_remote_entity_removal(&removal, &state, current, &local),
            Err(CanaryReconciliationError::LocalPlayerUnsupported)
        );

        let invalid_destination = SyntheticResolver {
            destination_stack: StackIndex::new(10),
            ..base
        };
        assert_eq!(
            decode_current_remote_entity_movement(&movement, &state, current, &invalid_destination,),
            Err(CanaryReconciliationError::InvalidDestinationStack)
        );

        let foreign_session = SessionToken::new(SessionGeneration::new(current.get() + 1));
        let foreign = SyntheticResolver {
            entity: EntityHandle::new(foreign_session, EntityId::try_new(0x0203_0405)?),
            ..base
        };
        assert!(matches!(
            decode_current_remote_entity_movement(&movement, &state, current, &foreign),
            Err(CanaryReconciliationError::Inbound(
                CanaryInboundError::Domain(DomainError::SessionMismatch { .. })
            ))
        ));
        Ok(())
    }

    #[test]
    fn stale_and_prebootstrap_state_are_rejected() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(85)?;
        let resolver = resolver(&state)?;
        let movement = parse_hex_fixture(REMOTE_ENTITY_MOVEMENT_FIXTURE)?;
        assert!(matches!(
            decode_current_remote_entity_movement(
                &movement,
                &state,
                SessionGeneration::new(current.get() + 1),
                &resolver,
            ),
            Err(CanaryReconciliationError::Inbound(
                CanaryInboundError::Domain(DomainError::StaleSession { .. })
            ))
        ));

        let initial_generation = SessionGeneration::new(86);
        let initial = CanaryInboundBootstrapState::new(SessionToken::new(initial_generation));
        let unresolved = SyntheticResolver {
            entity: EntityHandle::new(initial.session(), EntityId::try_new(0x0203_0405)?),
            ..resolver
        };
        assert_eq!(
            decode_current_remote_entity_movement(
                &movement,
                &initial,
                initial_generation,
                &unresolved,
            ),
            Err(CanaryReconciliationError::Inbound(
                CanaryInboundError::InvalidOrder,
            ))
        );
        Ok(())
    }
}
