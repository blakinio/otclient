use crate::inbound::{CanaryInboundBootstrapState, decode_current_pending_state_entered};
use crate::known_player::decode_current_known_remote_player_appearance;
use crate::map::decode_current_local_player_only_map;
use crate::non_player::decode_current_unknown_remote_non_player_appearance;
use crate::tile::decode_current_unknown_remote_player_appearance;
use oteryn_foundation::SessionGeneration;
use oteryn_game_domain::{
    EntityHandle, EntityId, EntityKind, Floor, GameEvent, NameText, SessionToken, StackIndex,
    TilePosition,
};
use oteryn_protocol_core::{ProtocolError, ProtocolErrorKind};
use std::error::Error;
use std::num::ParseIntError;

const LOCAL_PLAYER_INITIALIZATION_FIXTURE: &str = include_str!(
    "../../../tests/integration/canary-world-protocol/fixtures/local-player-initialization.hex"
);
const ALLOW_BUG_REPORT_FIXTURE: &str =
    include_str!("../../../tests/integration/canary-world-protocol/fixtures/allow-bug-report.hex");
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

const INVISIBLE_UNKNOWN_PLAYER: &str = "
6A 35 12 79 56 07 01
61 00 00 00 00 00 05 04 03 02 00
06 00 52 65 6D 6F 74 65
64 02 00 00 00 00 00 00
07 D7 DC 00 00 00 00 00 00 01 00 FF 00 01
";
const INVISIBLE_KNOWN_PLAYER: &str = "
6A 35 12 79 56 07 01
62 00 05 04 03 02
64 02 00 00 00 00 00 00
07 D7 DC 00 00 00 00 00 01 00 FF 00 01
";
const INVISIBLE_MONSTER: &str = "
6A 35 12 79 56 07 01
61 00 00 00 00 00 05 04 03 02 01
03 00 52 61 74
64 02 00 00 00 00 00 00
07 D7 DC 00 00 00 00 00 01 00 FF 00 01
";
const INVISIBLE_NPC: &str = "
6A 36 12 79 56 07 02
61 00 00 00 00 00 06 04 03 02 02
05 00 47 75 69 64 65
64 02 00 00 00 00 00 00
07 D7 DC 00 00 00 00 00 02 00 FF 00 01
";
const INVISIBLE_PLAYER_SUMMON: &str = "
6A 37 12 79 56 07 03
61 00 00 00 00 00 07 04 03 02 01
04 00 57 6F 6C 66
64 02 00 00 00 00 00 00
07 D7 DC 00 00 00 00 00 03 04 03 02 01 00 FF 00 01
";

fn parse_hex(input: &str) -> Result<Vec<u8>, ParseIntError> {
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
        &parse_hex(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?,
        current,
    )?;
    state.decode_allow_bug_report(&parse_hex(ALLOW_BUG_REPORT_FIXTURE)?, current)?;
    state.decode_tibia_time(&parse_hex(TIBIA_TIME_FIXTURE)?, current)?;
    decode_current_pending_state_entered(
        &parse_hex(PENDING_STATE_ENTERED_FIXTURE)?,
        &mut state,
        current,
    )?;
    state.decode_enter_world(&parse_hex(ENTER_WORLD_FIXTURE)?, current)?;
    decode_current_local_player_only_map(
        &parse_hex(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?,
        &mut state,
        current,
    )?;
    Ok((state, current))
}

fn assert_appearance(
    event: &GameEvent,
    state: &CanaryInboundBootstrapState,
    id: u32,
    kind: EntityKind,
    name: Option<&str>,
    position: TilePosition,
    stack: StackIndex,
) -> Result<(), Box<dyn Error>> {
    let expected_name = name.map(NameText::try_new).transpose()?;
    assert_eq!(
        event,
        &GameEvent::EntityAppeared {
            entity: EntityHandle::new(state.session(), EntityId::try_new(id)?),
            kind,
            name: expected_name,
            position,
            stack,
        }
    );
    Ok(())
}

#[test]
fn invisible_default_outfit_is_accepted_for_every_supported_family() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(120)?;

    let unknown_player = decode_current_unknown_remote_player_appearance(
        &parse_hex(INVISIBLE_UNKNOWN_PLAYER)?,
        &state,
        current,
    )?;
    assert_appearance(
        unknown_player.event(),
        &state,
        0x0203_0405,
        EntityKind::Player,
        Some("Remote"),
        TilePosition::new(0x1235, 0x5679, Floor::new(7)),
        StackIndex::new(1),
    )?;

    let known_player = decode_current_known_remote_player_appearance(
        &parse_hex(INVISIBLE_KNOWN_PLAYER)?,
        &state,
        current,
    )?;
    assert_appearance(
        known_player.event(),
        &state,
        0x0203_0405,
        EntityKind::Player,
        None,
        TilePosition::new(0x1235, 0x5679, Floor::new(7)),
        StackIndex::new(1),
    )?;

    for (fixture, id, kind, name, position, stack) in [
        (
            INVISIBLE_MONSTER,
            0x0203_0405,
            EntityKind::Creature,
            "Rat",
            TilePosition::new(0x1235, 0x5679, Floor::new(7)),
            StackIndex::new(1),
        ),
        (
            INVISIBLE_NPC,
            0x0203_0406,
            EntityKind::NonPlayerCharacter,
            "Guide",
            TilePosition::new(0x1236, 0x5679, Floor::new(7)),
            StackIndex::new(2),
        ),
        (
            INVISIBLE_PLAYER_SUMMON,
            0x0203_0407,
            EntityKind::Creature,
            "Wolf",
            TilePosition::new(0x1237, 0x5679, Floor::new(7)),
            StackIndex::new(3),
        ),
    ] {
        let envelope = decode_current_unknown_remote_non_player_appearance(
            &parse_hex(fixture)?,
            &state,
            current,
        )?;
        assert_appearance(
            envelope.event(),
            &state,
            id,
            kind,
            Some(name),
            position,
            stack,
        )?;
    }
    Ok(())
}

#[test]
fn every_invisible_family_truncated_prefix_is_rejected() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(121)?;
    let unknown = parse_hex(INVISIBLE_UNKNOWN_PLAYER)?;
    for length in 0..unknown.len() {
        assert_eq!(
            decode_current_unknown_remote_player_appearance(&unknown[..length], &state, current),
            Err(crate::inbound::CanaryInboundError::Protocol(
                ProtocolError::new(ProtocolErrorKind::Truncated),
            ))
        );
    }

    let known = parse_hex(INVISIBLE_KNOWN_PLAYER)?;
    for length in 0..known.len() {
        assert_eq!(
            decode_current_known_remote_player_appearance(&known[..length], &state, current),
            Err(crate::inbound::CanaryInboundError::Protocol(
                ProtocolError::new(ProtocolErrorKind::Truncated),
            ))
        );
    }

    for fixture in [INVISIBLE_MONSTER, INVISIBLE_NPC, INVISIBLE_PLAYER_SUMMON] {
        let input = parse_hex(fixture)?;
        for length in 0..input.len() {
            assert_eq!(
                decode_current_unknown_remote_non_player_appearance(
                    &input[..length],
                    &state,
                    current,
                ),
                Err(crate::inbound::CanaryInboundError::Protocol(
                    ProtocolError::new(ProtocolErrorKind::Truncated),
                ))
            );
        }
    }
    Ok(())
}
