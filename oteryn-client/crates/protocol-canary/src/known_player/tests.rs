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
const KNOWN_REMOTE_PLAYER_APPEARANCE_FIXTURE: &str = include_str!(
    "../../../../tests/integration/canary-world-protocol/fixtures/known-remote-player-appearance.hex"
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
fn exact_known_remote_player_emits_appearance_without_name() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(90)?;
    let envelope = decode_current_known_remote_player_appearance(
        &parse_hex_fixture(KNOWN_REMOTE_PLAYER_APPEARANCE_FIXTURE)?,
        &state,
        current,
    )?;
    let entity = EntityHandle::new(state.session(), EntityId::try_new(0x0203_0405)?);
    assert_eq!(
        envelope.event(),
        &GameEvent::EntityAppeared {
            entity,
            kind: EntityKind::Player,
            name: None,
            position: TilePosition::new(0x1235, 0x5679, Floor::new(7)),
            stack: StackIndex::new(1),
        }
    );
    Ok(())
}

#[test]
fn every_truncated_prefix_is_rejected() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(91)?;
    let appearance = parse_hex_fixture(KNOWN_REMOTE_PLAYER_APPEARANCE_FIXTURE)?;
    for length in 0..appearance.len() {
        assert_eq!(
            decode_current_known_remote_player_appearance(&appearance[..length], &state, current,),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::Truncated,
            )))
        );
    }
    Ok(())
}

#[test]
fn closed_fields_and_trailing_data_fail_closed() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(92)?;
    let fixture = parse_hex_fixture(KNOWN_REMOTE_PLAYER_APPEARANCE_FIXTURE)?;

    let mut wrong_marker = fixture.clone();
    wrong_marker[7] = 0x61;
    assert_eq!(
        decode_current_known_remote_player_appearance(&wrong_marker, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut hidden_health = fixture.clone();
    hidden_health[13] = 0;
    assert_eq!(
        decode_current_known_remote_player_appearance(&hidden_health, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut invalid_direction = fixture.clone();
    invalid_direction[14] = 8;
    assert_eq!(
        decode_current_known_remote_player_appearance(&invalid_direction, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut invalid_type = fixture.clone();
    invalid_type[31] = 1;
    assert_eq!(
        decode_current_known_remote_player_appearance(&invalid_type, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut trailing = fixture;
    trailing.push(0);
    assert_eq!(
        decode_current_known_remote_player_appearance(&trailing, &state, current),
        Err(CanaryInboundError::Protocol(ProtocolError::new(
            ProtocolErrorKind::TrailingData,
        )))
    );
    Ok(())
}

#[test]
fn local_zero_stale_and_prebootstrap_identity_fail_closed() -> Result<(), Box<dyn Error>> {
    let (state, current) = ready_state(93)?;
    let fixture = parse_hex_fixture(KNOWN_REMOTE_PLAYER_APPEARANCE_FIXTURE)?;

    let mut local = fixture.clone();
    local[9..13].copy_from_slice(&0x0102_0304_u32.to_le_bytes());
    assert_eq!(
        decode_current_known_remote_player_appearance(&local, &state, current),
        Err(CanaryInboundError::Protocol(unknown_value()))
    );

    let mut zero = fixture.clone();
    zero[9..13].copy_from_slice(&0_u32.to_le_bytes());
    assert_eq!(
        decode_current_known_remote_player_appearance(&zero, &state, current),
        Err(CanaryInboundError::Domain(DomainError::ZeroIdentifier(
            oteryn_game_domain::IdentifierKind::Entity,
        )))
    );

    assert!(matches!(
        decode_current_known_remote_player_appearance(
            &fixture,
            &state,
            SessionGeneration::new(current.get() + 1),
        ),
        Err(CanaryInboundError::Domain(DomainError::StaleSession { .. }))
    ));

    let initial_generation = SessionGeneration::new(94);
    let initial = CanaryInboundBootstrapState::new(SessionToken::new(initial_generation));
    assert_eq!(
        decode_current_known_remote_player_appearance(&fixture, &initial, initial_generation,),
        Err(CanaryInboundError::InvalidOrder)
    );
    Ok(())
}
