from pathlib import Path
import re

MAP_RS = '''use crate::inbound::{CanaryInboundBootstrapState, CanaryInboundError};
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
const LOCAL_PLAYER_TILE_ORDINAL: usize =
    LOCAL_PLAYER_X_OFFSET * MAP_HEIGHT + LOCAL_PLAYER_Y_OFFSET;
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
        (
            usize::from(last - first + 1),
            usize::from(z - first),
        )
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
            decode_current_local_player_only_map(
                &invalid_utf8,
                &mut utf8_state,
                utf8_current,
            ),
            Err(CanaryInboundError::Protocol(ProtocolError::new(
                ProtocolErrorKind::InvalidUtf8,
            )))
        );
        assert!(!utf8_state.bootstrap_completed());

        let mut trailing = original;
        trailing.push(0);
        let (mut trailing_state, trailing_current) = ready_state(64)?;
        assert_eq!(
            decode_current_local_player_only_map(
                &trailing,
                &mut trailing_state,
                trailing_current,
            ),
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
        let mut before_state =
            CanaryInboundBootstrapState::new(SessionToken::new(before_enter));
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
            decode_current_local_player_only_map(
                &input,
                &mut terminal_state,
                terminal_current,
            ),
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
'''
FIXTURE = '''64 34 12 78 56 07 75 FF
61 00 00 00 00 00 04 03 02 01 00
09 00 53 79 6E 74 68 65 74 69 63
64 02 80 00 01 02 03 04 00 00 00
07 D7 DC 00 00 00 00 00 00 01 00 FF 00 01
FF FF FF FF FF FF FF FF FF FF FF FF FF FF 69 FF
'''

root = Path(".")
inbound_path = root / "oteryn-client/crates/protocol-canary/src/inbound.rs"
lib_path = root / "oteryn-client/crates/protocol-canary/src/lib.rs"
task_path = root / "docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md"
evidence_path = root / "oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md"
fixture_dir = root / "oteryn-client/tests/integration/canary-world-protocol/fixtures"

inbound = inbound_path.read_text(encoding="utf-8")
replacements = [
    (
        "    enter_world_received: bool,\n    session_ended: bool,\n",
        "    enter_world_received: bool,\n    bootstrap_completed: bool,\n    session_ended: bool,\n",
        "bootstrap state field",
    ),
    (
        "            enter_world_received: false,\n            session_ended: false,\n",
        "            enter_world_received: false,\n            bootstrap_completed: false,\n            session_ended: false,\n",
        "bootstrap state constructor",
    ),
    (
        "    pub const fn enter_world_received(self) -> bool {\n        self.enter_world_received\n    }\n\n",
        "    pub const fn enter_world_received(self) -> bool {\n        self.enter_world_received\n    }\n\n    /// Return whether a complete initial map established the local position.\n    #[must_use]\n    pub const fn bootstrap_completed(self) -> bool {\n        self.bootstrap_completed\n    }\n\n    pub(crate) const fn mark_bootstrap_completed(&mut self) {\n        self.bootstrap_completed = true;\n    }\n\n",
        "bootstrap state accessors",
    ),
]
for old, new, label in replacements:
    count = inbound.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    inbound = inbound.replace(old, new, 1)
inbound_path.write_text(inbound, encoding="utf-8", newline="\n")

lib = lib_path.read_text(encoding="utf-8")
for old, new, label in [
    ("mod inbound;\nmod tile;\n", "mod inbound;\nmod map;\nmod tile;\n", "map module"),
    (
        "pub use tile::{OPCODE_TILE_UPDATE, decode_current_empty_tile_update};\n",
        "pub use map::{OPCODE_MAP_DESCRIPTION, decode_current_local_player_only_map};\npub use tile::{OPCODE_TILE_UPDATE, decode_current_empty_tile_update};\n",
        "map export",
    ),
]:
    count = lib.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, found {count}")
    lib = lib.replace(old, new, 1)
lib_path.write_text(lib, encoding="utf-8", newline="\n")

(root / "oteryn-client/crates/protocol-canary/src/map.rs").write_text(
    MAP_RS, encoding="utf-8", newline="\n"
)
(fixture_dir / "local-player-only-map.hex").write_text(
    FIXTURE, encoding="utf-8", newline="\n"
)

readme_path = fixture_dir / "README.md"
readme = readme_path.read_text(encoding="utf-8")
append = """

Local-player-only map fixture proves one complete source-reachable Current
bootstrap branch: opcode `0x64`, authoritative local position, exact surface
floor traversal and skip markers, one item-free tile containing only the
ordinary unknown local player, and the complete fixed-width Current player
creature payload. The synthetic name, appearance, clock, coordinates and
status values are invented. No item catalogue bytes or private capture are
included.
"""
if "Local-player-only map fixture proves" not in readme:
    readme += append
readme_path.write_text(readme, encoding="utf-8", newline="\n")

task = task_path.read_text(encoding="utf-8")
updates = [
    (r"^status: blocked$", "status: validating"),
    (r"^phase: .*$", "phase: local-player-only-map-bootstrap"),
    (r"^branch: .*$", "branch: feat/OTC2-20260803-canary-local-player-map"),
    (r"^updated: .*$", "updated: 2026-08-03T20:25:00+02:00"),
    (r'^required_base_commit: ".*"$', 'required_base_commit: "2f0bff09cd9f5a9acf2629d7ba080e98d3f5f1ad"'),
    (r"^last_progress_at: .*$", "last_progress_at: 2026-08-03T20:25:00+02:00"),
    (r"^ci_check_generation: .*$", "ci_check_generation: local-player-map-focused"),
]
for pattern, replacement in updates:
    task, count = re.subn(pattern, replacement, task, count=1, flags=re.MULTILINE)
    if count != 1:
        raise SystemExit(f"task anchor not found: {pattern}")
task = task.replace(
    "related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223, 224, 225, 227, 228, 230, 231, 232, 233, 234, 235, 236, 237]",
    "related_prs: [188, 190, 191, 192, 193, 196, 198, 203, 204, 219, 220, 221, 222, 223, 224, 225, 227, 228, 230, 231, 232, 233, 234, 235, 236, 237, 238, 239, 240]",
    1,
)
active = """
# Active local-player-only map bootstrap

The pinned source permits one complete initial-map branch without item-catalogue
decoding: an existing item-free tile containing only the ordinary local player.
The branch consumes the complete unknown-player payload, exact `18 x 14`
surface traversal and all skip markers.

```yaml
opcode: 0x64
position: [x_u16_le, y_u16_le, z_u8]
accepted_floor: source_valid_0_through_15
accepted_tiles: exactly_one_local_player_tile
accepted_items: none
accepted_creatures: exactly_one_unknown_ordinary_local_player
identity: must_match_session_local_player_from_0x17
output: GameEvent::BootstrapCompleted
simulation_mutation: false
general_map_claim: false
```

Other tiles, every item branch, known creatures, non-player creature types,
health-hidden players, zero-looktype outfits and extra contents remain rejected.

"""
if "# Active local-player-only map bootstrap" not in task:
    task = task.replace("# P2 barrier\n", active + "# P2 barrier\n", 1)
checkpoint = """# Durable checkpoint

```yaml
checkpoint_version: 23
updated_at: 2026-08-03T20:25:00+02:00
observed_main: 2f0bff09cd9f5a9acf2629d7ba080e98d3f5f1ad
status: validating
phase: local-player-only-map-bootstrap
implemented_bootstrap_order: [local_player_0x17, allow_bug_report_0x1A, tibia_time_0xEF, pending_state_0x0A, enter_world_0x0F]
active_branch: feat/OTC2-20260803-canary-local-player-map
active_layout: local_player_only_initial_map_0x64
validation: focused_workflow_running
shared_path_lease: []
ownership:
  protocol_canary: retained_by_active_parent_task
  shared_paths: released
blocker: General non-empty map/item/creature layouts and position/stack identity ownership remain incomplete outside this narrow item-free local-player branch.
next_action: Validate and merge the local-player-only map bootstrap, then resume full AddItem and general AddCreature normalization without inference.
```
"""
task, count = re.subn(
    r"# Durable checkpoint\n\n```yaml\n.*?\n```\n?\Z",
    checkpoint,
    task,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("durable checkpoint anchor not found")
task_path.write_text(task, encoding="utf-8", newline="\n")

evidence = evidence_path.read_text(encoding="utf-8")
status_pattern = r"^Status: .*$"
status_replacement = (
    "Status: local-player identity, login side-preamble, session-end and absent-tile slices "
    "are merged; one source-reachable item-free local-player map bootstrap is under exact validation."
)
evidence, count = re.subn(
    status_pattern, status_replacement, evidence, count=1, flags=re.MULTILINE
)
if count != 1:
    raise SystemExit("evidence status anchor not found")
section = """
## Active item-free local-player map validation

The pinned source permits an existing tile to contain a creature list without
ground or items. `GetTileDescription` then emits the ordinary unknown-player
branch. For an initial surface map at synthetic position `(0x1234, 0x5678, 7)`,
the local tile is ordinal 118 in the first `18 x 14` floor and the complete
message has deterministic leading and trailing skip runs.

```yaml
opcode: 0x64
viewport: 18_by_14
surface_floors: 7_down_to_0
leading_missing_tiles: 118
leading_marker: [0x75, 0xFF]
tile_contents:
  ground: none
  items: none
  creatures: [ordinary_unknown_local_player]
unknown_player:
  marker_u16_le: 0x61
  removed_known_u32_le: 0
  id: must_match_0x17_local_identity
  bounded_name: consumed_not_exposed
  outfit_branch: non_zero_looktype
  icon_count_max: 3
  final_fixed_fields: [mark_0xFF, inspection_0x00]
trailing_missing_tiles: 1897
trailing_markers: [seven_FF_FF_pairs, 0x69_0xFF]
output: GameEvent::BootstrapCompleted
general_map_or_item_support: false
```

The decoder rejects every item, extra tile/creature, known-creature marker,
non-local identity, unsupported player branch, malformed RLE marker, impossible
order, truncation, oversize and trailing data.

"""
if "## Active item-free local-player map validation" not in evidence:
    evidence = evidence.replace("## Fixture provenance\n", section + "## Fixture provenance\n", 1)
evidence_path.write_text(evidence, encoding="utf-8", newline="\n")
