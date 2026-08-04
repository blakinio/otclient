use super::*;
use crate::inbound::decode_current_pending_state_entered;
use crate::map::decode_current_local_player_only_map;
use oteryn_game_domain::{DomainError, SessionToken};
use std::error::Error;
use std::num::ParseIntError;

const LOCAL_PLAYER_INITIALIZATION_FIXTURE: &str = include_str!(
    "../../../../tests/integration/canary-world-protocol/fixtures/local-player-initialization.hex"
);
const ALLOW_BUG_REPORT_FIXTURE: &str = include_str!(
    "../../../../tests/integration/canary-world-protocol/fixtures/allow-bug-report.hex"
);
const TIBIA_TIME_FIXTURE: &str =
    include_str!("../../../../tests/integration/canary-world-protocol/fixtures/tibia-time.hex");
const PENDING_STATE_ENTERED_FIXTURE: &str = include_str!(
    "../../../../tests/integration/canary-world-protocol/fixtures/pending-state-entered.hex"
);
const ENTER_WORLD_FIXTURE: &str =
    include_str!("../../../../tests/integration/canary-world-protocol/fixtures/enter-world.hex");
const LOCAL_PLAYER_ONLY_MAP_FIXTURE: &str = include_str!(
    "../../../../tests/integration/canary-world-protocol/fixtures/local-player-only-map.hex"
);
const UNKNOWN_MONSTER_APPEARANCE_FIXTURE: &str = include_str!(
    "../../../../tests/integration/canary-world-protocol/fixtures/unknown-monster-appearance.hex"
);
const UNKNOWN_NPC_APPEARANCE_FIXTURE: &str = include_str!(
    "../../../../tests/integration/canary-world-protocol/fixtures/unknown-npc-appearance.hex"
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
    decode_current_local_player_only_map(
        &parse_hex_fixture(LOCAL_PLAYER_ONLY_MAP_FIXTURE)?,
        &mut state,
        current,
    )?;
    Ok((state, current))
}

#[test]
fn exact_unknown_monster_emits_creature_appearance() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(100)?;
    let envelope = decode_current_unknown_remote_non_player_appearance(
        &parse_hex_fixture(UNKNOWN_MONSTER_APPEARANCE_FIXTURE)?,
        &state,
        current,
    )?;
    assert_eq!(
        envelope.event(),
        &GameEvent::EntityAppeared {
            entity: EntityHandle::new(state.session(), EntityId::try_new(0x0203_0405)?),
            kind: EntityKind::Creature,
            name: Some(NameText::try_new("Rat")?),
            position: TilePosition::new(0x1235, 0x5679, Floor::new(7)),
            stack: StackIndex::new(1),
        }
    );
    Ok(())
}

#[test]
fn exact_unknown_npc_emits_npc_appearance() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(101)?;
    let envelope = decode_current_unknown_remote_non_player_appearance(
        &parse_hex_fixture(UNKNOWN_NPC_APPEARANCE_FIXTURE)?,
        &state,
        current,
    )?;
    assert_eq!(
        envelope.event(),
        &GameEvent::EntityAppeared {
            entity: EntityHandle::new(state.session(), EntityId::try_new(0x0203_0406)?),
            kind: EntityKind::NonPlayerCharacter,
            name: Some(NameText::try_new("Guide")?),
            position: TilePosition::new(0x1236, 0x5679, Floor::new(7)),
            stack: StackIndex::new(2),
        }
    );
    Ok(())
}

#[test]
fn every_truncated_prefix_is_rejected() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(102)?;
    for fixture in [
        UNKNOWN_MONSTER_APPEARANCE_FIXTURE,
        UNKNOWN_NPC_APPEARANCE_FIXTURE,
    ] {
        let appearance = parse_hex_fixture(fixture)?;
        for length in 0..appearance.len() {
            assert_eq!(
                decode_current_unknown_remote_non_player_appearance(
                    &appearance[..length],
                    &state,
                    current,
                ),
                Err(CanaryInboundError::Protocol(ProtocolError::new(
                    ProtocolErrorKind::Truncated,
                )))
            );
        }
    }
    Ok(())
}

#[test]
fn header_payload_and_trailing_branches_fail_closed() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(103)?;
    let fixture = parse_hex_fixture(UNKNOWN_MONSTER_APPEARANCE_FIXTURE)?;

    let mut known_marker = fixture.clone();
    known_marker[7] = 0x62;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&known_marker, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut eviction = fixture.clone();
    eviction[9] = 1;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&eviction, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut player_header = fixture.clone();
    player_header[17] = 0;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&player_header, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut hidden_health = fixture.clone();
    hidden_health[23] = 0;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&hidden_health, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut invalid_direction = fixture.clone();
    invalid_direction[24] = 8;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&invalid_direction, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut invisible_outfit = fixture.clone();
    invisible_outfit[25] = 0;
    invisible_outfit[26] = 0;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&invisible_outfit, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut summon_rewrite = fixture.clone();
    summon_rewrite[42] = 3;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&summon_rewrite, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut trailing = fixture;
    trailing.push(0);
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&trailing, &state, current),
        Err(CanaryInboundError::Protocol(ProtocolError::new(
            ProtocolErrorKind::TrailingData,
        )))
    );
    Ok(())
}

#[test]
fn identity_name_state_and_bounds_fail_closed() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(104)?;
    let fixture = parse_hex_fixture(UNKNOWN_MONSTER_APPEARANCE_FIXTURE)?;

    let mut local = fixture.clone();
    local[13..17].copy_from_slice(&0x0102_0304_u32.to_le_bytes());
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&local, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut zero = fixture.clone();
    zero[13..17].copy_from_slice(&0_u32.to_le_bytes());
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&zero, &state, current),
        Err(CanaryInboundError::Domain(DomainError::ZeroIdentifier(
            oteryn_game_domain::IdentifierKind::Entity,
        )))
    );

    let mut empty_name = fixture.clone();
    empty_name[18] = 0;
    empty_name[19] = 0;
    empty_name.drain(20..23);
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&empty_name, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut invalid_floor = fixture.clone();
    invalid_floor[5] = 16;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&invalid_floor, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut invalid_stack = fixture.clone();
    invalid_stack[6] = 10;
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&invalid_stack, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    assert!(matches!(
        decode_current_unknown_remote_non_player_appearance(
            &fixture,
            &state,
            SessionGeneration::new(current.get() + 1),
        ),
        Err(CanaryInboundError::Domain(DomainError::StaleSession { .. }))
    ));

    let initial_generation = SessionGeneration::new(105);
    let initial = CanaryInboundBootstrapState::new(SessionToken::new(initial_generation));
    assert_eq!(
        decode_current_unknown_remote_non_player_appearance(&fixture, &initial, initial_generation,),
        Err(CanaryInboundError::InvalidOrder)
    );
    Ok(())
}
