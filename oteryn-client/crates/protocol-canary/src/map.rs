use crate::inbound::{CanaryInboundBootstrapState, CanaryInboundError};
use crate::{CANARY_CHARACTER_NAME_MAX_BYTES, CANARY_NETWORK_MESSAGE_MAX_BYTES};
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{Floor, GameEvent, GameEventEnvelope, TilePosition};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};

/// Canary Current server opcode for the initial map description.
pub const OPCODE_MAP_DESCRIPTION: u8 = 0x64;

const MAP_WIDTH: usize = 18;
const MAP_HEIGHT: usize = 14;
const MAP_TILES_PER_FLOOR: usize = MAP_WIDTH * MAP_HEIGHT;
const MAP_MAX_LAYERS: u8 = 16;
const MAP_SURFACE_LAYER: u8 = 7;
const MAP_LAYER_VIEW_LIMIT: u8 = 2;
const LOCAL_PLAYER_X_OFFSET: usize = 8;
const LOCAL_PLAYER_Y_OFFSET: usize = 6;
const LOCAL_PLAYER_TILE_ORDINAL: usize = LOCAL_PLAYER_X_OFFSET * MAP_HEIGHT + LOCAL_PLAYER_Y_OFFSET;
const UNKNOWN_CREATURE_MARKER: u16 = 0x61;
const CREATURE_TYPE_PLAYER: u8 = 0;
const MAX_CREATURE_ICONS: u8 = 3;
const CREATURE_MARK_UNMARKED: u8 = 0xFF;
const CREATURE_INSPECTION_NONE: u8 = 0;

/// Decode one complete, source-reachable Current initial-map branch.
///
/// This deliberately narrow branch accepts an `18 x 14` map description whose
/// only existing tile is the local-player tile, with no ground or items and one
/// ordinary unknown-player creature matching the identity established by
/// opcode `0x17`. The complete Current unknown-player payload and every
/// surrounding map skip marker are consumed. Success emits only
/// [`GameEvent::BootstrapCompleted`].
///
/// General non-empty tiles remain unsupported because `AddItem` length depends
/// on the authoritative item catalogue and other creature branches require
/// additional identity/cache semantics.
///
/// # Errors
///
/// Rejects stale or impossible order, duplicate bootstrap, invalid floor/map
/// geometry, malformed skip runs, item/extra-tile markers, a non-local creature,
/// unsupported creature branches, invalid fixed fields, truncation, oversize
/// and every trailing byte. State advances only after semantic envelope
/// validation succeeds.
pub fn decode_current_local_player_only_map(
    input: &[u8],
    state: &mut CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    state.session().ensure_current(current)?;
    if !state.enter_world_received() || state.session_ended() || state.bootstrap_completed() {
        return Err(CanaryInboundError::InvalidOrder);
    }
    let player = state
        .local_player()
        .ok_or(CanaryInboundError::InvalidOrder)?;

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    expect_u8(&mut reader, OPCODE_MAP_DESCRIPTION)?;
    let x = reader.read_u16_le()?;
    let y = reader.read_u16_le()?;
    let z = reader.read_u8()?;
    let (preceding_tiles, following_tiles) = local_player_map_geometry(z)?;

    consume_missing_tiles(&mut reader, preceding_tiles, -1)?;
    if reader.read_u16_le()? != UNKNOWN_CREATURE_MARKER || reader.read_u32_le()? != 0 {
        return Err(unknown_value().into());
    }
    if reader.read_u32_le()? != player.id().get() {
        return Err(unknown_value().into());
    }
    expect_u8(&mut reader, CREATURE_TYPE_PLAYER)?;

    let name = reader.read_u16_string(CANARY_CHARACTER_NAME_MAX_BYTES)?;
    if name.is_empty() {
        return Err(unknown_value().into());
    }

    let health_percent = reader.read_u8()?;
    if !(1..=100).contains(&health_percent) {
        return Err(unknown_value().into());
    }
    if reader.read_u8()? > 7 {
        return Err(unknown_value().into());
    }

    let look_type = reader.read_u16_le()?;
    if look_type == 0 {
        return Err(unknown_value().into());
    }
    let _outfit_colors_and_addons = reader.read_exact(5)?;

    let look_mount = reader.read_u16_le()?;
    if look_mount != 0 {
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

    consume_missing_tiles(&mut reader, following_tiles, 0)?;
    reader.finish(TrailingDataPolicy::Reject)?;

    let position = TilePosition::new(x, y, Floor::new(z));
    let envelope = GameEventEnvelope::v1(
        state.session(),
        GameEvent::BootstrapCompleted { player, position },
    )?;
    envelope.ensure_current(current)?;
    state.mark_bootstrap_completed();
    Ok(envelope)
}

fn local_player_map_geometry(z: u8) -> Result<(usize, usize), ProtocolError> {
    if z >= MAP_MAX_LAYERS {
        return Err(unknown_value());
    }

    let (floor_count, local_floor_index) = if z <= MAP_SURFACE_LAYER {
        (
            usize::from(MAP_SURFACE_LAYER + 1),
            usize::from(MAP_SURFACE_LAYER - z),
        )
    } else {
        let first = z.saturating_sub(MAP_LAYER_VIEW_LIMIT);
        let last = z
            .saturating_add(MAP_LAYER_VIEW_LIMIT)
            .min(MAP_MAX_LAYERS - 1);
        (usize::from(last - first + 1), usize::from(z - first))
    };

    let total_tiles = floor_count
        .checked_mul(MAP_TILES_PER_FLOOR)
        .ok_or_else(arithmetic_overflow)?;
    let preceding_tiles = local_floor_index
        .checked_mul(MAP_TILES_PER_FLOOR)
        .and_then(|value| value.checked_add(LOCAL_PLAYER_TILE_ORDINAL))
        .ok_or_else(arithmetic_overflow)?;
    let following_tiles = total_tiles
        .checked_sub(
            preceding_tiles
                .checked_add(1)
                .ok_or_else(arithmetic_overflow)?,
        )
        .ok_or_else(arithmetic_overflow)?;
    Ok((preceding_tiles, following_tiles))
}

fn consume_missing_tiles(
    reader: &mut BoundedReader<'_>,
    missing_tiles: usize,
    initial_skip: i16,
) -> Result<(), ProtocolError> {
    let mut skip = initial_skip;
    for _ in 0..missing_tiles {
        if skip == 0xFE {
            expect_u8(reader, 0xFF)?;
            expect_u8(reader, 0xFF)?;
            skip = -1;
        } else {
            skip += 1;
        }
    }

    if skip >= 0 {
        let encoded_skip =
            u8::try_from(skip).map_err(|_| ProtocolError::new(ProtocolErrorKind::InvalidLength))?;
        expect_u8(reader, encoded_skip)?;
        expect_u8(reader, 0xFF)?;
    }
    Ok(())
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

const fn arithmetic_overflow() -> ProtocolError {
    ProtocolError::new(ProtocolErrorKind::ArithmeticOverflow)
}

#[cfg(test)]
mod tests {
    use super::*;
    use crate::inbound::decode_current_pending_state_entered;
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
        Ok((state, current))
    }

    #[test]
    fn exact_local_player_only_map_completes_bootstrap() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = ready_state(60)?;
        let player = state.local_player().ok_or("missing local player")?;
        let input = parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?;
        let envelope = decode_current_local_player_only_map(&input, &mut state, current)?;

        assert_eq!(envelope.session(), state.session());
        assert_eq!(
            envelope.event(),
            &GameEvent::BootstrapCompleted {
                player,
                position: TilePosition::new(0x1234, 0x5678, Floor::new(7)),
            }
        );
        assert!(state.bootstrap_completed());
        Ok(())
    }

    #[test]
    fn every_truncated_prefix_fails_atomically() -> Result<(), Box<dyn Error>> {
        let input = parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?;
        for length in 0..input.len() {
            let (mut state, current) = ready_state(61)?;
            assert_eq!(
                decode_current_local_player_only_map(&input[..length], &mut state, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(
                    ProtocolErrorKind::Truncated,
                )))
            );
            assert!(!state.bootstrap_completed());
        }
        Ok(())
    }

    #[test]
    fn closed_map_and_creature_fields_fail_closed() -> Result<(), Box<dyn Error>> {
        let original = parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?;
        let mutations = [
            (0, 0x63),
            (5, 0x10),
            (6, 0x74),
            (8, 0x62),
            (10, 0x01),
            (14, 0x05),
            (18, 0x01),
            (30, 0x00),
            (31, 0x08),
            (32, 0x00),
            (45, 0x04),
            (49, 0x01),
            (52, 0xFE),
            (53, 0x01),
            (54, 0x02),
            (55, 0xFE),
        ];

        for (index, value) in mutations {
            let mut input = original.clone();
            input[index] = value;
            let (mut state, current) = ready_state(62)?;
            assert_eq!(
                decode_current_local_player_only_map(&input, &mut state, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(
                    ProtocolErrorKind::UnknownValue,
                )))
            );
            assert!(!state.bootstrap_completed());
        }
        Ok(())
    }

    #[test]
    fn invalid_utf8_and_trailing_data_fail_closed() -> Result<(), Box<dyn Error>> {
        let original = parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?;

        let mut invalid_utf8 = original.clone();
        invalid_utf8[21] = 0xFF;
        let (mut utf8_state, utf8_current) = ready_state(63)?;
        assert_eq!(
            decode_current_local_player_only_map(&invalid_utf8, &mut utf8_state, utf8_current,),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::InvalidUtf8,
            )))
        );
        assert!(!utf8_state.bootstrap_completed());

        let mut trailing = original;
        trailing.push(0);
        let (mut trailing_state, trailing_current) = ready_state(64)?;
        assert_eq!(
            decode_current_local_player_only_map(&trailing, &mut trailing_state, trailing_current,),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::TrailingData,
            )))
        );
        assert!(!trailing_state.bootstrap_completed());
        Ok(())
    }

    #[test]
    fn oversized_and_invalid_order_inputs_are_rejected() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = ready_state(65)?;
        let oversized = vec![0; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];
        assert_eq!(
            decode_current_local_player_only_map(&oversized, &mut state, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized,
            )))
        );

        let input = parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?;
        let before_enter = SessionGeneration::new(66);
        let mut before_state = CanaryInboundBootstrapState::new(SessionToken::new(before_enter));
        assert_eq!(
            decode_current_local_player_only_map(&input, &mut before_state, before_enter),
            Err(CanaryInboundError::InvalidOrder)
        );

        let (mut stale_state, actual) = ready_state(67)?;
        assert_eq!(
            decode_current_local_player_only_map(
                &input,
                &mut stale_state,
                SessionGeneration::new(actual.get() + 1),
            ),
            Err(CanaryInboundError::Domain(DomainError::StaleSession {
                expected: SessionGeneration::new(actual.get() + 1),
                actual,
            }))
        );

        let (mut terminal_state, terminal_current) = ready_state(68)?;
        terminal_state.decode_session_end_information(&[0x18, 0x00], terminal_current)?;
        assert_eq!(
            decode_current_local_player_only_map(&input, &mut terminal_state, terminal_current,),
            Err(CanaryInboundError::InvalidOrder)
        );
        Ok(())
    }

    #[test]
    fn duplicate_map_bootstrap_is_rejected() -> Result<(), Box<dyn Error>> {
        let input = parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?;
        let (mut state, current) = ready_state(69)?;
        decode_current_local_player_only_map(&input, &mut state, current)?;
        assert_eq!(
            decode_current_local_player_only_map(&input, &mut state, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        Ok(())
    }
}
