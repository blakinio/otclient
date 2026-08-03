from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    return text.replace(old, new, 1)


def write(path: str, content: str) -> None:
    Path(path).write_text(content, encoding="utf-8", newline="\n")


lib_path = Path("oteryn-client/crates/protocol-canary/src/lib.rs")
lib = lib_path.read_text(encoding="utf-8")
lib = replace_once(lib, "mod inbound;\n", "mod inbound;\nmod tile;\n", "tile module")
lib = replace_once(
    lib,
    "pub use inbound::{\n"
    "    CanaryInboundBootstrapState, CanaryInboundError, OPCODE_ENTER_WORLD,\n"
    "    OPCODE_LOCAL_PLAYER_INITIALIZATION, OPCODE_PENDING_STATE_ENTERED, decode_current_enter_world,\n"
    "    decode_current_local_player_initialization, decode_current_pending_state_entered,\n"
    "};\n",
    "pub use inbound::{\n"
    "    CanaryInboundBootstrapState, CanaryInboundError, OPCODE_ENTER_WORLD,\n"
    "    OPCODE_LOCAL_PLAYER_INITIALIZATION, OPCODE_PENDING_STATE_ENTERED, decode_current_enter_world,\n"
    "    decode_current_local_player_initialization, decode_current_pending_state_entered,\n"
    "};\n"
    "pub use tile::{OPCODE_TILE_UPDATE, decode_current_empty_tile_update};\n",
    "tile re-export",
)
lib_path.write_text(lib, encoding="utf-8", newline="\n")

write(
    "oteryn-client/crates/protocol-canary/src/tile.rs",
    r'''use crate::CANARY_NETWORK_MESSAGE_MAX_BYTES;
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
    if reader.read_u8()? != EMPTY_TILE_MARKER
        || reader.read_u8()? != TILE_DESCRIPTION_TERMINATOR
    {
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
        let mut state =
            CanaryInboundBootstrapState::new(SessionToken::new(current));
        let local = parse_hex_fixture(LOCAL_PLAYER_INITIALIZATION_FIXTURE)?;
        state.decode_local_player_initialization(&local, current)?;
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
''',
)

fixtures = {
    "tile-clear.hex": "69 34 12 78 56 07 01 FF\n",
    "tile-clear-wrong-marker.hex": "69 34 12 78 56 07 00 FF\n",
    "tile-clear-wrong-terminator.hex": "69 34 12 78 56 07 01 FE\n",
    "tile-clear-trailing.hex": "69 34 12 78 56 07 01 FF 00\n",
}
for name, content in fixtures.items():
    write(
        f"oteryn-client/tests/integration/canary-world-protocol/fixtures/{name}",
        content,
    )

readme_path = Path(
    "oteryn-client/tests/integration/canary-world-protocol/fixtures/README.md"
)
readme = readme_path.read_text(encoding="utf-8")
readme += """

Tile-clear fixtures prove only the complete Current absent-tile branch of
`sendUpdateTile`: opcode `0x69`, position encoded as `u16le/u16le/u8`, marker
`0x01` and terminator `0xFF`. Wrong marker, wrong terminator and trailing data
are negative cases. Coordinates are synthetic and no map contents are copied.
"""
readme_path.write_text(readme, encoding="utf-8", newline="\n")

evidence_path = Path(
    "oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md"
)
evidence = evidence_path.read_text(encoding="utf-8")
evidence = replace_once(
    evidence,
    "Status: local-player identity, pending-state, enter-world order and known session-end slices are merged; the parent producer remains blocked on complete map/world layouts and general identity resolution.  ",
    "Status: local-player identity/order and known session-end slices are merged; the complete absent-tile update branch is under exact-head validation while the parent remains blocked on non-empty map/world layouts and general identity resolution.  ",
    "evidence status",
)
evidence = replace_once(
    evidence,
    "## Inbound readiness matrix\n",
    """## Proven absent-tile update branch

The exact Current `ProtocolGame::sendUpdateTile` producer writes opcode `0x69`
and `NetworkMessage::addPosition`, which is exactly `x:u16le`, `y:u16le`,
`z:u8`. When the producer tile pointer is absent it writes fixed marker `0x01`
and terminator `0xFF`; no `GetTileDescription`, item writer or creature writer
is invoked.

```yaml
logical_message:
  opcode_u8: 0x69
  x_u16_le: canonical_tile_x
  y_u16_le: canonical_tile_y
  z_u8: canonical_floor
  absent_tile_marker_u8: 0x01
  terminator_u8: 0xFF
prerequisite: current_session_after_enter_world
output: GameEventEnvelope::v1(GameEvent::TileCleared)
state_mutation: none
nested_writer_dependency: none
```

The decoder rejects every truncated prefix, wrong opcode, wrong marker,
wrong terminator, oversize, trailing data, stale/pre-enter-world state and a
terminal session. Synthetic fixtures contain coordinates only.

## Inbound readiness matrix
""",
    "evidence tile section",
)
evidence = replace_once(
    evidence,
    "| tile and stack updates | `PARTIAL` | Outer opcodes/positions are visible, but nested tile descriptions and stack-only identity ownership remain incomplete. |",
    "| tile and stack updates | `PARTIAL` | The complete absent-tile `0x69 + position + 0x01 + 0xFF` branch is implemented as `TileCleared`. Non-empty tile descriptions and stack-only identity ownership remain incomplete. |",
    "evidence matrix",
)
evidence = replace_once(
    evidence,
    "No partial map, tile, entity, movement or removal decoder is implemented. No parser mutates simulation state.\n",
    "No partial map, entity, movement or removal decoder is implemented. The tile decoder accepts only the complete absent-tile branch and no parser mutates simulation state.\n",
    "evidence claim",
)
evidence = replace_once(
    evidence,
    "## Terminal bootstrap identity validation\n",
    """## Active empty-tile validation

```yaml
branch: feat/OTC2-20260803-canary-tile-clear
base: 6eb1d3c4421ca32170fe4ca703001e953a2eb58a
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
source_methods: [ProtocolGame::sendUpdateTile, NetworkMessage::addPosition]
new_decoder: decode_current_empty_tile_update
negative_matrix: [truncated, wrong_opcode, wrong_marker, wrong_terminator, oversized, trailing, stale, pre_enter_world, terminal]
validation: focused_workflow_running
```

## Terminal bootstrap identity validation
""",
    "evidence validation phase",
)
evidence_path.write_text(evidence, encoding="utf-8", newline="\n")

task_path = Path(
    "docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md"
)
task = task_path.read_text(encoding="utf-8")
task = replace_once(task, "status: blocked\n", "status: validating\n", "task status")
task = replace_once(
    task,
    "phase: inbound-map-layout-and-general-identity-blocker\n",
    "phase: empty-tile-update-normalization\n",
    "task phase",
)
task = replace_once(
    task,
    "branch: docs/OTC2-20260803-canary-bootstrap-identity-closeout\n",
    "branch: feat/OTC2-20260803-canary-tile-clear\n",
    "task branch",
)
task = replace_once(
    task,
    "updated: 2026-08-03T16:25:00+02:00\n",
    "updated: 2026-08-03T18:10:00+02:00\n",
    "task updated",
)
task = replace_once(
    task,
    'required_base_commit: "d6ac5c89a378d58ef4bdbd7ba0e5a61f686e4e0a"\n',
    'required_base_commit: "6eb1d3c4421ca32170fe4ca703001e953a2eb58a"\n',
    "task base",
)
task = replace_once(
    task,
    "related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221]\n",
    "related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223]\n",
    "task related prs",
)
task = replace_once(
    task,
    "last_progress_at: 2026-08-03T16:25:00+02:00\n",
    "last_progress_at: 2026-08-03T18:10:00+02:00\n",
    "task progress",
)
task = replace_once(
    task,
    "ci_check_generation: bootstrap-identity-closeout\n",
    "ci_check_generation: empty-tile-focused\n",
    "task ci generation",
)
task = replace_once(
    task,
    "| tile and stack updates | `PARTIAL` | Outer opcodes and positions are visible; nested tile bodies and authoritative stack identity remain incomplete. |",
    "| tile and stack updates | `PARTIAL` | The complete absent-tile `0x69` branch is being normalized to `TileCleared`; nested non-empty tile bodies and authoritative stack identity remain incomplete. |",
    "task matrix",
)
task = replace_once(
    task,
    "# P2 barrier\n",
    """# Active empty-tile update phase

The pinned Current source proves one complete tile branch that is independent of
`GetTileDescription`, `AddItem`, `AddCreature` and stack identity:

```yaml
producer: ProtocolGame::sendUpdateTile
opcode: 0x69
position: [x_u16_le, y_u16_le, z_u8]
absent_tile_branch: [0x01, 0xFF]
prerequisite: current_session_after_enter_world
semantic_output: GameEvent::TileCleared
nested_writer_dependency: none
simulation_mutation: false
```

The non-empty branch remains blocked because it invokes nested variable writers.
This phase does not claim map bootstrap completion or relax real admission.

# P2 barrier
""",
    "task phase section",
)
task = replace_once(task, "checkpoint_version: 18\n", "checkpoint_version: 19\n", "checkpoint version")
task = replace_once(
    task,
    "updated_at: 2026-08-03T16:25:00+02:00\n",
    "updated_at: 2026-08-03T18:10:00+02:00\n",
    "checkpoint updated",
)
task = replace_once(
    task,
    "observed_main: d6ac5c89a378d58ef4bdbd7ba0e5a61f686e4e0a\n",
    "observed_main: 6eb1d3c4421ca32170fe4ca703001e953a2eb58a\n",
    "checkpoint main",
)
task = replace_once(task, "status: blocked\n", "status: validating\n", "checkpoint status")
task = replace_once(
    task,
    "phase: inbound-map-layout-and-general-identity-blocker\n",
    "phase: empty-tile-update-normalization\n",
    "checkpoint phase",
)
task = replace_once(
    task,
    "implemented_bootstrap_order: [local_player_0x17, pending_state_0x0A, enter_world_0x0F]\n",
    "implemented_bootstrap_order: [local_player_0x17, pending_state_0x0A, enter_world_0x0F]\nactive_branch: feat/OTC2-20260803-canary-tile-clear\nactive_layout: empty_tile_update_0x69\nvalidation: focused_workflow_running\n",
    "checkpoint active phase",
)
task = replace_once(
    task,
    "next_action: Obtain and accept one complete pinned map-description layout plus its nested writer bounds and authoritative identity-resolution contract, then resume this same task without inferring fields or ownership.\n",
    "next_action: Validate and merge the complete absent-tile update branch, then resume non-empty map/tile writer normalization without inferring fields or ownership.\n",
    "checkpoint next action",
)
task_path.write_text(task, encoding="utf-8", newline="\n")
