use crate::inbound::{CanaryInboundBootstrapState, CanaryInboundError};
use crate::{CANARY_CHARACTER_NAME_MAX_BYTES, CANARY_NETWORK_MESSAGE_MAX_BYTES};
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{
    EntityHandle, EntityId, EntityKind, Floor, GameEvent, GameEventEnvelope, NameText, StackIndex,
    TilePosition,
};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};

/// Canary Current server opcode for one complete tile replacement.
pub const OPCODE_TILE_UPDATE: u8 = 0x69;
/// Canary Current server opcode for adding one thing to a tile stack.
pub const OPCODE_ADD_TILE_THING: u8 = 0x6A;

const EMPTY_TILE_MARKER: u8 = 0x01;
const TILE_DESCRIPTION_TERMINATOR: u8 = 0xFF;
const UNKNOWN_CREATURE_MARKER: u16 = 0x61;
const CREATURE_TYPE_PLAYER: u8 = 0;
const MAX_CREATURE_ICONS: u8 = 3;
const MAX_TILE_STACK_INDEX: u8 = 9;
const MAP_MAX_LAYERS: u8 = 16;
const CREATURE_MARK_UNMARKED: u8 = 0xFF;
const CREATURE_INSPECTION_NONE: u8 = 0;

impl CanaryInboundBootstrapState {
    /// Decode one complete Current unknown ordinary remote-player appearance.
    ///
    /// This method accepts only the source-reachable `sendAddCreature` branch
    /// encoded as opcode `0x6A`, position, stack index below ten, unknown marker
    /// `0x61`, zero known-cache eviction id and the complete Current ordinary
    /// player payload. Known creatures, cache eviction, hidden health, summons,
    /// monsters, NPCs, invisible outfits and OTCR extensions remain rejected.
    ///
    /// # Errors
    ///
    /// Returns the same fail-closed errors as
    /// [`decode_current_unknown_remote_player_appearance`].
    pub fn decode_unknown_remote_player_appearance(
        &self,
        input: &[u8],
        current: SessionGeneration,
    ) -> Result<GameEventEnvelope, CanaryInboundError> {
        decode_current_unknown_remote_player_appearance(input, self, current)
    }
}

/// Decode the complete Current absent-tile branch of `sendUpdateTile`.
///
/// The accepted logical message is exactly opcode `0x69`, a little-endian
/// `u16/u16/u8` position, absent-tile marker `0x01` and terminator `0xFF`.
/// Success emits only [`GameEvent::TileCleared`]. The nested non-empty tile
/// branch remains unsupported because it delegates to item and creature writers.
///
/// # Errors
///
/// Rejects stale or pre-bootstrap state, terminal sessions, truncation,
/// oversize, wrong opcode/markers and every trailing byte.
pub fn decode_current_empty_tile_update(
    input: &[u8],
    state: &CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    state.session().ensure_current(current)?;
    if !state.bootstrap_completed() || state.session_ended() {
        return Err(CanaryInboundError::InvalidOrder);
    }

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    if reader.read_u8()? != OPCODE_TILE_UPDATE {
        return Err(unknown_value().into());
    }

    let x = reader.read_u16_le()?;
    let y = reader.read_u16_le()?;
    let floor = Floor::new(reader.read_u8()?);
    if reader.read_u8()? != EMPTY_TILE_MARKER || reader.read_u8()? != TILE_DESCRIPTION_TERMINATOR {
        return Err(unknown_value().into());
    }
    reader.finish(TrailingDataPolicy::Reject)?;

    let envelope = GameEventEnvelope::v1(
        state.session(),
        GameEvent::TileCleared {
            position: TilePosition::new(x, y, floor),
        },
    )?;
    envelope.ensure_current(current)?;
    Ok(envelope)
}

/// Decode one complete source-reachable Current remote-player add branch.
///
/// The producer layout is `0x6A`, `Position`, `stack_u8`, followed by the full
/// non-legacy `AddCreature` unknown ordinary-player payload. The accepted cache
/// eviction id is exactly zero, so this parser does not invent or own the
/// producer's known-creature cache. Success emits one protocol-neutral
/// [`GameEvent::EntityAppeared`]. No appearance, health, icon or vocation wire
/// value crosses the adapter boundary.
///
/// # Errors
///
/// Rejects stale/pre-bootstrap/terminal state, local-player reuse, zero identity,
/// cache eviction, known/hidden/non-player branches, invalid floor/stack bounds,
/// malformed strings, invalid fixed fields, truncation, oversize and trailing data.
pub fn decode_current_unknown_remote_player_appearance(
    input: &[u8],
    state: &CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    state.session().ensure_current(current)?;
    if !state.bootstrap_completed() || state.session_ended() {
        return Err(CanaryInboundError::InvalidOrder);
    }
    let local_player = state
        .local_player()
        .ok_or(CanaryInboundError::InvalidOrder)?;

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    expect_u8(&mut reader, OPCODE_ADD_TILE_THING)?;
    let x = reader.read_u16_le()?;
    let y = reader.read_u16_le()?;
    let z = reader.read_u8()?;
    if z >= MAP_MAX_LAYERS {
        return Err(unknown_value().into());
    }
    let stack = reader.read_u8()?;
    if stack > MAX_TILE_STACK_INDEX {
        return Err(unknown_value().into());
    }

    if reader.read_u16_le()? != UNKNOWN_CREATURE_MARKER || reader.read_u32_le()? != 0 {
        return Err(unknown_value().into());
    }
    let entity_id = reader.read_u32_le()?;
    if entity_id == local_player.id().get() {
        return Err(unknown_value().into());
    }
    expect_u8(&mut reader, CREATURE_TYPE_PLAYER)?;

    let name = reader.read_u16_string(CANARY_CHARACTER_NAME_MAX_BYTES)?;
    if name.is_empty() {
        return Err(unknown_value().into());
    }

    if !(1..=100).contains(&reader.read_u8()?) || reader.read_u8()? > 7 {
        return Err(unknown_value().into());
    }

    if reader.read_u16_le()? == 0 {
        return Err(unknown_value().into());
    }
    let _outfit_colors_and_addons = reader.read_exact(5)?;

    if reader.read_u16_le()? != 0 {
        let _mount_colors = reader.read_exact(4)?;
    }

    let _light_level = reader.read_u8()?;
    let _light_color = reader.read_u8()?;
    let _step_speed = reader.read_u16_le()?;

    let icon_count = reader.read_u8()?;
    if icon_count > MAX_CREATURE_ICONS {
        return Err(unknown_value().into());
    }
    for _ in 0..icon_count {
        let _serialized_icon = reader.read_u8()?;
        let _icon_category = reader.read_u8()?;
        let _icon_count = reader.read_u16_le()?;
    }

    let _skull = reader.read_u8()?;
    let _party_shield = reader.read_u8()?;
    let _guild_emblem = reader.read_u8()?;
    expect_u8(&mut reader, CREATURE_TYPE_PLAYER)?;
    let _vocation = reader.read_u8()?;
    let _speech_bubble = reader.read_u8()?;
    expect_u8(&mut reader, CREATURE_MARK_UNMARKED)?;
    expect_u8(&mut reader, CREATURE_INSPECTION_NONE)?;
    if !matches!(reader.read_u8()?, 0 | 1) {
        return Err(unknown_value().into());
    }
    reader.finish(TrailingDataPolicy::Reject)?;

    let entity = EntityHandle::new(state.session(), EntityId::try_new(entity_id)?);
    let envelope = GameEventEnvelope::v1(
        state.session(),
        GameEvent::EntityAppeared {
            entity,
            kind: EntityKind::Player,
            name: Some(NameText::try_new(name)?),
            position: TilePosition::new(x, y, Floor::new(z)),
            stack: StackIndex::new(stack),
        },
    )?;
    envelope.ensure_current(current)?;
    Ok(envelope)
}

fn expect_u8(reader: &mut BoundedReader<'_>, expected: u8) -> Result<(), ProtocolError> {
    if reader.read_u8()? == expected {
        Ok(())
    } else {
        Err(unknown_value())
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
    use oteryn_game_domain::{DomainError, SessionToken};
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
    const TILE_CLEAR_FIXTURE: &str =
        include_str!("../../../tests/integration/canary-world-protocol/fixtures/tile-clear.hex");
    const TILE_CLEAR_WRONG_MARKER_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/tile-clear-wrong-marker.hex"
    );
    const TILE_CLEAR_WRONG_TERMINATOR_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/tile-clear-wrong-terminator.hex"
    );
    const TILE_CLEAR_TRAILING_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/tile-clear-trailing.hex"
    );
    const REMOTE_PLAYER_APPEARANCE_FIXTURE: &str = include_str!(
        "../../../tests/integration/canary-world-protocol/fixtures/remote-player-appearance.hex"
    );

    fn parse_hex_fixture(input: &str) -> Result<Vec<u8>, ParseIntError> {
        input
            .split_whitespace()
            .map(|token| u8::from_str_radix(token, 16))
            .collect()
    }

    fn entered_state(
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
        Ok((state, current))
    }

    fn ready_state(
        generation: u64,
    ) -> Result<(CanaryInboundBootstrapState, SessionGeneration), Box<dyn Error>> {
        let (mut state, current) = entered_state(generation)?;
        decode_current_local_player_only_map(
            &parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?,
            &mut state,
            current,
        )?;
        Ok((state, current))
    }

    #[test]
    fn exact_absent_tile_fixture_emits_tile_cleared() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(40)?;
        let envelope = decode_current_empty_tile_update(
            &parse_hex_fixture(TILE_CLEAR_FIXTURE)?,
            &state,
            current,
        )?;
        assert_eq!(
            envelope.event(),
            &GameEvent::TileCleared {
                position: TilePosition::new(0x1234, 0x5678, Floor::new(7)),
            }
        );
        Ok(())
    }

    #[test]
    fn exact_unknown_remote_player_emits_entity_appeared() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(47)?;
        let envelope = state.decode_unknown_remote_player_appearance(
            &parse_hex_fixture(REMOTE_PLAYER_APPEARANCE_FIXTURE)?,
            current,
        )?;
        let entity = EntityHandle::new(state.session(), EntityId::try_new(0x0203_0405)?);
        assert_eq!(
            envelope.event(),
            &GameEvent::EntityAppeared {
                entity,
                kind: EntityKind::Player,
                name: Some(NameText::try_new("Remote")?),
                position: TilePosition::new(0x1235, 0x5679, Floor::new(7)),
                stack: StackIndex::new(1),
            }
        );
        Ok(())
    }

    #[test]
    fn every_truncated_prefix_is_rejected() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(41)?;
        let tile = parse_hex_fixture(TILE_CLEAR_FIXTURE)?;
        for length in 0..tile.len() {
            assert_eq!(
                decode_current_empty_tile_update(&tile[..length], &state, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(
                    ProtocolErrorKind::Truncated,
                )))
            );
        }

        let appearance = parse_hex_fixture(REMOTE_PLAYER_APPEARANCE_FIXTURE)?;
        for length in 0..appearance.len() {
            assert_eq!(
                state.decode_unknown_remote_player_appearance(&appearance[..length], current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(
                    ProtocolErrorKind::Truncated,
                )))
            );
        }
        Ok(())
    }

    #[test]
    fn tile_closed_fields_and_trailing_data_fail_closed() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(42)?;
        let wrong_opcode = [0x68, 0x34, 0x12, 0x78, 0x56, 0x07, 0x01, 0xFF];
        let wrong_marker = parse_hex_fixture(TILE_CLEAR_WRONG_MARKER_FIXTURE)?;
        let wrong_terminator = parse_hex_fixture(TILE_CLEAR_WRONG_TERMINATOR_FIXTURE)?;
        let trailing = parse_hex_fixture(TILE_CLEAR_TRAILING_FIXTURE)?;

        for input in [&wrong_opcode[..], &wrong_marker, &wrong_terminator] {
            assert_eq!(
                decode_current_empty_tile_update(input, &state, current),
                Err(CanaryInboundError::Protocol(unknown_value()))
            );
        }
        assert_eq!(
            decode_current_empty_tile_update(&trailing, &state, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::TrailingData,
            )))
        );
        Ok(())
    }

    #[test]
    fn remote_player_closed_branches_fail_closed() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(48)?;
        let original = parse_hex_fixture(REMOTE_PLAYER_APPEARANCE_FIXTURE)?;
        let mutations = [
            (0, 0x6B),
            (5, 0x10),
            (6, 0x0A),
            (7, 0x62),
            (9, 0x01),
            (17, 0x01),
            (18, 0x00),
            (19, 0x00),
            (26, 0x00),
            (27, 0x08),
            (28, 0x00),
            (29, 0x00),
            (41, 0x04),
            (45, 0x01),
            (48, 0x00),
            (49, 0x01),
            (50, 0x02),
        ];
        for (index, value) in mutations {
            let mut input = original.clone();
            input[index] = value;
            assert_eq!(
                state.decode_unknown_remote_player_appearance(&input, current),
                Err(CanaryInboundError::Protocol(unknown_value()))
            );
        }

        let mut local_identity = original.clone();
        local_identity[13..17].copy_from_slice(&[0x04, 0x03, 0x02, 0x01]);
        assert_eq!(
            state.decode_unknown_remote_player_appearance(&local_identity, current),
            Err(CanaryInboundError::Protocol(unknown_value()))
        );
        Ok(())
    }

    #[test]
    fn remote_player_invalid_utf8_and_trailing_data_fail_closed() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(49)?;
        let original = parse_hex_fixture(REMOTE_PLAYER_APPEARANCE_FIXTURE)?;
        let mut invalid_utf8 = original.clone();
        invalid_utf8[20] = 0xFF;
        assert_eq!(
            state.decode_unknown_remote_player_appearance(&invalid_utf8, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::InvalidUtf8,
            )))
        );

        let mut trailing = original;
        trailing.push(0);
        assert_eq!(
            state.decode_unknown_remote_player_appearance(&trailing, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::TrailingData,
            )))
        );
        Ok(())
    }

    #[test]
    fn oversized_input_is_rejected_before_dispatch() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(43)?;
        let input = vec![0; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];
        assert_eq!(
            decode_current_empty_tile_update(&input, &state, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized,
            )))
        );
        assert_eq!(
            state.decode_unknown_remote_player_appearance(&input, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized,
            )))
        );
        Ok(())
    }

    #[test]
    fn tile_and_entity_updates_require_completed_current_session() -> Result<(), Box<dyn Error>> {
        let current = SessionGeneration::new(44);
        let state = CanaryInboundBootstrapState::new(SessionToken::new(current));
        let tile = parse_hex_fixture(TILE_CLEAR_FIXTURE)?;
        let appearance = parse_hex_fixture(REMOTE_PLAYER_APPEARANCE_FIXTURE)?;
        assert_eq!(
            decode_current_empty_tile_update(&tile, &state, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert_eq!(
            state.decode_unknown_remote_player_appearance(&appearance, current),
            Err(CanaryInboundError::InvalidOrder)
        );

        let (entered, entered_current) = entered_state(45)?;
        assert_eq!(
            decode_current_empty_tile_update(&tile, &entered, entered_current),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert_eq!(
            entered.decode_unknown_remote_player_appearance(&appearance, entered_current),
            Err(CanaryInboundError::InvalidOrder)
        );

        let (ready, actual) = ready_state(46)?;
        let expected = SessionGeneration::new(actual.get() + 1);
        let stale = CanaryInboundError::Domain(DomainError::StaleSession { expected, actual });
        assert_eq!(
            decode_current_empty_tile_update(&tile, &ready, expected),
            Err(stale)
        );
        assert_eq!(
            ready.decode_unknown_remote_player_appearance(&appearance, expected),
            Err(stale)
        );
        Ok(())
    }

    #[test]
    fn terminal_session_rejects_later_tile_and_entity_updates() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = ready_state(50)?;
        state.decode_session_end_information(&[0x18, 0x00], current)?;
        assert_eq!(
            decode_current_empty_tile_update(
                &parse_hex_fixture(TILE_CLEAR_FIXTURE)?,
                &state,
                current,
            ),
            Err(CanaryInboundError::InvalidOrder)
        );
        assert_eq!(
            state.decode_unknown_remote_player_appearance(
                &parse_hex_fixture(REMOTE_PLAYER_APPEARANCE_FIXTURE)?,
                current,
            ),
            Err(CanaryInboundError::InvalidOrder)
        );
        Ok(())
    }
}
