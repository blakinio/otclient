use crate::CANARY_NETWORK_MESSAGE_MAX_BYTES;
use crate::inbound::{CanaryInboundBootstrapState, CanaryInboundError};
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{Floor, GameEvent, GameEventEnvelope, TilePosition};
use oteryn_protocol_core::{BoundedReader, ProtocolError, ProtocolErrorKind, TrailingDataPolicy};

/// Canary Current server opcode for one complete tile replacement.
pub const OPCODE_TILE_UPDATE: u8 = 0x69;

const EMPTY_TILE_MARKER: u8 = 0x01;
const TILE_DESCRIPTION_TERMINATOR: u8 = 0xFF;

/// Decode the complete Current absent-tile branch of `sendUpdateTile`.
///
/// The accepted logical message is exactly opcode `0x69`, a little-endian
/// `u16/u16/u8` position, absent-tile marker `0x01` and terminator `0xFF`.
/// Success emits only [`GameEvent::TileCleared`]. The nested non-empty tile
/// branch remains unsupported because it delegates to item and creature writers.
///
/// # Errors
///
/// Rejects stale or pre-enter-world state, terminal sessions, truncation,
/// oversize, wrong opcode/markers and every trailing byte.
pub fn decode_current_empty_tile_update(
    input: &[u8],
    state: &CanaryInboundBootstrapState,
    current: SessionGeneration,
) -> Result<GameEventEnvelope, CanaryInboundError> {
    state.session().ensure_current(current)?;
    if !state.enter_world_received() || state.session_ended() {
        return Err(CanaryInboundError::InvalidOrder);
    }

    let mut reader = BoundedReader::new(input, CANARY_NETWORK_MESSAGE_MAX_BYTES)?;
    if reader.read_u8()? != OPCODE_TILE_UPDATE {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
    }

    let x = reader.read_u16_le()?;
    let y = reader.read_u16_le()?;
    let floor = Floor::new(reader.read_u8()?);
    if reader.read_u8()? != EMPTY_TILE_MARKER || reader.read_u8()? != TILE_DESCRIPTION_TERMINATOR {
        return Err(ProtocolError::new(ProtocolErrorKind::UnknownValue).into());
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
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        state.decode_local_player_initialization(&local, current)?;
        let permission = parse_hex_fixture(ALLOW_BUG_REPORT_FIXTURE)?;
        state.decode_allow_bug_report(&permission, current)?;
        let time = parse_hex_fixture(TIBIA_TIME_FIXTURE)?;
        state.decode_tibia_time(&time, current)?;
        let pending = parse_hex_fixture(PENDING_STATE_ENTERED_FIXTURE)?;
        decode_current_pending_state_entered(&pending, &mut state, current)?;
        let enter = parse_hex_fixture(ENTER_WORLD_FIXTURE)?;
        state.decode_enter_world(&enter, current)?;
        Ok((state, current))
    }

    #[test]
    fn exact_absent_tile_fixture_emits_tile_cleared() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(40)?;
        let input = parse_hex_fixture(TILE_CLEAR_FIXTURE)?;
        let envelope = decode_current_empty_tile_update(&input, &state, current)?;

        assert_eq!(envelope.session(), state.session());
        assert_eq!(
            envelope.event(),
            &GameEvent::TileCleared {
                position: TilePosition::new(0x1234, 0x5678, Floor::new(7)),
            }
        );
        Ok(())
    }

    #[test]
    fn every_truncated_prefix_is_rejected() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(41)?;
        let input = parse_hex_fixture(TILE_CLEAR_FIXTURE)?;
        for length in 0..input.len() {
            assert_eq!(
                decode_current_empty_tile_update(&input[..length], &state, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(
                    ProtocolErrorKind::Truncated,
                )))
            );
        }
        Ok(())
    }

    #[test]
    fn closed_fields_and_trailing_data_fail_closed() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(42)?;
        let wrong_opcode = [0x68, 0x34, 0x12, 0x78, 0x56, 0x07, 0x01, 0xFF];
        let wrong_marker = parse_hex_fixture(TILE_CLEAR_WRONG_MARKER_FIXTURE)?;
        let wrong_terminator = parse_hex_fixture(TILE_CLEAR_WRONG_TERMINATOR_FIXTURE)?;
        let trailing = parse_hex_fixture(TILE_CLEAR_TRAILING_FIXTURE)?;

        for input in [&wrong_opcode[..], &wrong_marker, &wrong_terminator] {
            assert_eq!(
                decode_current_empty_tile_update(input, &state, current),
                Err(CanaryInboundError::Protocol(ProtocolError::new(
                    ProtocolErrorKind::UnknownValue,
                )))
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
    fn oversized_input_is_rejected_before_dispatch() -> Result<(), Box<dyn Error>> {
        let (state, current) = ready_state(43)?;
        let input = vec![0; CANARY_NETWORK_MESSAGE_MAX_BYTES + 1];
        assert_eq!(
            decode_current_empty_tile_update(&input, &state, current),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Oversized,
            )))
        );
        Ok(())
    }

    #[test]
    fn tile_clear_requires_enter_world_and_current_session() -> Result<(), Box<dyn Error>> {
        let current = SessionGeneration::new(44);
        let state = CanaryInboundBootstrapState::new(SessionToken::new(current));
        let input = parse_hex_fixture(TILE_CLEAR_FIXTURE)?;
        assert_eq!(
            decode_current_empty_tile_update(&input, &state, current),
            Err(CanaryInboundError::InvalidOrder)
        );

        let (ready, actual) = ready_state(45)?;
        assert_eq!(
            decode_current_empty_tile_update(
                &input,
                &ready,
                SessionGeneration::new(actual.get() + 1),
            ),
            Err(CanaryInboundError::Domain(DomainError::StaleSession {
                expected: SessionGeneration::new(actual.get() + 1),
                actual,
            }))
        );
        Ok(())
    }

    #[test]
    fn terminal_session_rejects_later_tile_updates() -> Result<(), Box<dyn Error>> {
        let (mut state, current) = ready_state(46)?;
        state.decode_session_end_information(&[0x18, 0x00], current)?;
        let input = parse_hex_fixture(TILE_CLEAR_FIXTURE)?;
        assert_eq!(
            decode_current_empty_tile_update(&input, &state, current),
            Err(CanaryInboundError::InvalidOrder)
        );
        Ok(())
    }
}
