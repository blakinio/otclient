from pathlib import Path
import re

TILE = Path("oteryn-client/crates/protocol-canary/src/tile.rs")
FIXTURE = Path("oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-player-appearance.hex")
TASK = Path("docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md")
EVIDENCE = Path("oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md")


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        raise RuntimeError(f"missing expected text: {old!r}")
    return text.replace(old, new, 1)


tile = TILE.read_text(encoding="utf-8")
for marker in [
    "decode_unknown_remote_player_appearance",
    "decode_current_unknown_remote_player_appearance",
    "GameEvent::EntityAppeared",
]:
    if marker not in tile:
        raise RuntimeError(f"missing implementation marker: {marker}")

# Remove two accidental no-op mutations so every negative case changes a byte.
tile = tile.replace("            (19, 0x00),\n", "", 1)
tile = tile.replace("            (29, 0x00),\n", "", 1)
TILE.write_text(tile, encoding="utf-8", newline="\n")

fixture = FIXTURE.read_text(encoding="utf-8")
if not fixture.startswith("6A ") or "61 00" not in fixture:
    raise RuntimeError("unexpected remote-player fixture")

task = TASK.read_text(encoding="utf-8")
task = replace_once(task, "phase: local-player-only-map-bootstrap", "phase: unknown-player-appearance")
task = replace_once(
    task,
    "branch: feat/OTC2-20260803-canary-local-player-map",
    "branch: feat/OTC2-20260803-canary-unknown-player-appearance",
)
task = re.sub(r"^updated: .+$", "updated: 2026-08-03T23:30:00+02:00", task, count=1, flags=re.MULTILINE)
task = re.sub(
    r'^required_base_commit: ".+"$',
    'required_base_commit: "ed355c66c305a4f7a42962bcc692194145626371"',
    task,
    count=1,
    flags=re.MULTILINE,
)
task = re.sub(
    r"^related_prs: \[(.*?)\]$",
    lambda match: "related_prs: [" + match.group(1).rstrip() + ", 241, 242, 243, 244]",
    task,
    count=1,
    flags=re.MULTILINE,
)
task = re.sub(r"^last_progress_at: .+$", "last_progress_at: 2026-08-03T23:30:00+02:00", task, count=1, flags=re.MULTILINE)
task = re.sub(r"^ci_check_generation: .+$", "ci_check_generation: unknown-player-appearance-focused", task, count=1, flags=re.MULTILINE)

task = replace_once(
    task,
    "  bootstrap_completed_emitted: false",
    "  bootstrap_completed_emitted: true\n"
    "unknown_remote_player_appearance_0x6A:\n"
    "  prerequisite: completed_current_bootstrap\n"
    "  accepted_branch: unknown_ordinary_player_with_zero_cache_eviction\n"
    "  bounds: [floor_0_through_15, stack_0_through_9, name_max_30, icons_max_3]\n"
    "  output: GameEvent::EntityAppeared\n"
    "  retained_wire_fields: [entity_id, name, position, stack]",
)
task = replace_once(
    task,
    "| session bootstrap | `PARTIAL` | Exact order through local identity, bug-report permission, Tibia time, pending-state and enter-world is implemented. A complete map description remains required before `BootstrapCompleted`. |",
    "| session bootstrap | `PARTIAL` | Exact order through local identity, bug-report permission, Tibia time, pending-state and enter-world plus one complete item-free local-player map emits `BootstrapCompleted`; general map admission remains incomplete. |",
)
task = replace_once(
    task,
    "| map description | `UNKNOWN` | Outer viewport/floor/skip structure is proven, but the reachable initial map necessarily contains the local creature and therefore depends on complete nested item/creature writers. |",
    "| map description | `PARTIAL` | One complete item-free local-player-only `0x64` branch is implemented. General non-empty tiles remain blocked by authoritative item metadata and broader creature/cache branches. |",
)
task = replace_once(
    task,
    "| creature/entity appearance | `UNKNOWN` | Known/unknown creature branches, cache eviction, appearance fields, feature gates and collection bounds are not yet normalized as one complete family. |",
    "| creature/entity appearance | `PARTIAL` | One complete post-bootstrap `0x6A` unknown ordinary remote-player branch with zero cache eviction emits `EntityAppeared`. Known/cache-eviction, hidden, summon, monster, NPC, invisible and OTCR branches remain unsupported. |",
)

section = """
# Unknown ordinary remote-player appearance

The exact pinned `sendAddCreature` and `AddCreature` source proves one bounded
post-bootstrap entity branch that does not require ownership of the producer's
known-creature cache: opcode `0x6A`, canonical position, stack below ten,
unknown marker `0x61`, zero eviction id, a distinct non-zero player id and the
complete Current ordinary-player payload.

```yaml
accepted_opcode: 0x6A
accepted_marker: 0x61
accepted_cache_eviction: 0
accepted_entity_type: player
accepted_stack: 0_through_9
accepted_floor: 0_through_15
output: GameEvent::EntityAppeared
simulation_mutation: false
unsupported: [known_0x62, nonzero_eviction, hidden, summon, monster, npc, invisible, otcr]
```

The original synthetic fixture contains no capture, secret or proprietary asset
byte. Canary-only status and appearance fields are consumed but do not escape
the adapter.

"""
if "# Unknown ordinary remote-player appearance" not in task:
    task = replace_once(task, "# P2 barrier\n", section + "# P2 barrier\n")

checkpoint = """# Durable checkpoint

```yaml
checkpoint_version: 24
updated_at: 2026-08-03T23:30:00+02:00
observed_main: ed355c66c305a4f7a42962bcc692194145626371
status: validating
phase: unknown-player-appearance
implemented_bootstrap_order: [local_player_0x17, allow_bug_report_0x1A, tibia_time_0xEF, pending_state_0x0A, enter_world_0x0F, local_player_only_map_0x64]
active_branch: feat/OTC2-20260803-canary-unknown-player-appearance
active_layout: unknown_ordinary_remote_player_add_0x6A
validation: focused_workflow_running
shared_path_lease: []
ownership:
  protocol_canary: retained_by_active_parent_task
  shared_paths: released
blocker: General AddItem decoding requires authoritative item-type branch metadata; movement and removal provide position/stack without an accepted protocol-neutral handle resolver; known/cache-eviction and non-player creature branches remain incomplete.
next_action: Validate and merge the unknown ordinary remote-player appearance, then terminally normalize the remaining item-catalogue and position/stack identity blockers without inference.
```
"""
task = re.sub(r"# Durable checkpoint\n\n```yaml\n.*?\n```\s*$", checkpoint, task, count=1, flags=re.DOTALL)
TASK.write_text(task, encoding="utf-8", newline="\n")

evidence = EVIDENCE.read_text(encoding="utf-8")
if "## Unknown ordinary remote-player appearance" not in evidence:
    evidence += """

## Unknown ordinary remote-player appearance

Source classification: `PROVEN` for one narrow Current/non-legacy branch at
`blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`.

The producer emits `0x6A + Position + stack_u8` for a non-local creature below
stack index ten. `AddCreature` then emits unknown marker `0x61`, an optional
known-cache eviction id, entity id, type/name and the complete appearance/status
tail. The implemented branch requires eviction id zero and ordinary player type,
consumes the full payload and emits only `GameEvent::EntityAppeared` with a
session-fenced handle, bounded name, position and stack.

Known marker `0x62`, nonzero eviction, hidden health, summon, monster, NPC,
invisible/zero-looktype and OTCR branches remain `UNKNOWN` and fail closed. The
fixture is original synthetic data without credentials, captures or assets.
"""
EVIDENCE.write_text(evidence, encoding="utf-8", newline="\n")
