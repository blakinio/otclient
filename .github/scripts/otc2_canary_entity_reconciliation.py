from __future__ import annotations

import os
import re
from pathlib import Path

BRANCH = "feat/OTC2-20260803-canary-entity-reconciliation"
BASE = "2a7a179633bb345dc4013563967a89f4fc47d233"
UPDATED = "2026-08-04T08:10:00+02:00"
PR_NUMBER = os.environ.get("PR_NUMBER", "pending")


def replace_once(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    if new in content:
        return
    if old not in content:
        raise RuntimeError(f"missing replacement anchor in {path}: {old!r}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8", newline="\n")


lib = Path("oteryn-client/crates/protocol-canary/src/lib.rs")
replace_once(lib, "mod map;\nmod tile;", "mod map;\nmod reconciliation;\nmod tile;")
replace_once(
    lib,
    "pub use map::{OPCODE_MAP_DESCRIPTION, decode_current_local_player_only_map};\n",
    "pub use map::{OPCODE_MAP_DESCRIPTION, decode_current_local_player_only_map};\n"
    "pub use reconciliation::{\n"
    "    CanaryEntityReconciliationResolver, CanaryReconciliationError,\n"
    "    OPCODE_MOVE_CREATURE, OPCODE_REMOVE_TILE_THING, ResolvedCanaryEntityMovement,\n"
    "    decode_current_remote_entity_movement, decode_current_remote_entity_removal,\n"
    "};\n",
)

task_path = Path(
    "docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md"
)
task = task_path.read_text(encoding="utf-8")
frontmatter_replacements = {
    "status: blocked": "status: implementing",
    "phase: item-catalogue-and-stack-identity-blocker": "phase: entity-reconciliation-implementation",
    "branch: main": f"branch: {BRANCH}",
    "updated: 2026-08-04T00:12:00+02:00": f"updated: {UPDATED}",
    'required_base_commit: "6b3efb75131f0ee1b9ce1779aa3ef7eaa1a536a2"': f'required_base_commit: "{BASE}"',
    "last_progress_at: 2026-08-04T00:10:31+02:00": f"last_progress_at: {UPDATED}",
    "ci_checks_for_current_head: 4": "ci_checks_for_current_head: 0",
    "ci_check_generation: unknown-player-appearance-terminal": "ci_check_generation: entity-reconciliation-focused",
    "terminal_ci_checks_for_current_generation: 4": "terminal_ci_checks_for_current_generation: 0",
    "repair_cycles_for_current_gate: 4": "repair_cycles_for_current_gate: 0",
}
for old, new in frontmatter_replacements.items():
    if old in task:
        task = task.replace(old, new, 1)

related_match = re.search(r"^related_prs: \[(.*?)\]$", task, flags=re.MULTILINE)
if related_match and PR_NUMBER != "pending":
    values = [value.strip() for value in related_match.group(1).split(",") if value.strip()]
    if PR_NUMBER not in values:
        values.append(PR_NUMBER)
        task = (
            task[: related_match.start()]
            + f"related_prs: [{', '.join(values)}]"
            + task[related_match.end() :]
        )

movement_old = "| movement and reconciliation | `BLOCKED` | Local movement appends general map strips. Remote movement exposes positions and stack indices but no accepted protocol-neutral handle resolver exists. |"
movement_new = "| movement and reconciliation | `PARTIAL` | The complete remote non-teleport `0x6D` layout is implemented behind a read-only caller-owned resolver that supplies the session-fenced entity and destination stack. Local-player movement and appended map strips remain blocked. |"
removal_old = "| removal | `BLOCKED` | Position plus stack index cannot be converted to an authoritative `EntityHandle` or item handle without caller-owned world state. |"
removal_new = "| removal | `PARTIAL` | The complete remote-entity `0x6C` layout is implemented behind a read-only caller-owned resolver. Item removal and local-player teleport/map-reset branches remain unsupported. |"
if movement_old in task:
    task = task.replace(movement_old, movement_new, 1)
if removal_old in task:
    task = task.replace(removal_old, removal_new, 1)

section_marker = "# Caller-owned entity reconciliation continuation"
if section_marker not in task:
    insertion = f"""# Caller-owned entity reconciliation continuation

The pinned producer proves two complete field layouts that can be normalized without owning world state when the caller supplies a read-only authoritative observation resolver:

```yaml
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
branch: {BRANCH}
pr: {PR_NUMBER}
remote_entity_movement:
  opcode: 0x6D
  layout: [old_position_u16_u16_u8, old_stack_u8, new_position_u16_u16_u8]
  source_branch: non_local_non_teleport_creature_visible_at_old_and_new_position
  resolver_output: [session_fenced_entity_handle, destination_stack]
  event: GameEvent::EntityMoved
remote_entity_removal:
  opcode: 0x6C
  layout: [position_u16_u16_u8, stack_u8]
  accepted_object: caller_resolved_non_local_entity
  event: GameEvent::EntityRemoved
resolver_contract:
  ownership: caller
  access: read_only
  malformed_input_invocation: forbidden
  simulation_mutation: false
  unresolved_or_ambiguous: fail_closed
shared_path_lease: []
validation: pending
```

Local-player movement is excluded because its producer branch appends map strips. Generic item removal is excluded because this phase does not own or infer item identity. General map and tile decoding remain blocked by authoritative item metadata.

"""
    task = task.replace("# Exact blocker normalization\n", insertion + "# Exact blocker normalization\n", 1)

checkpoint_pattern = re.compile(
    r"# Durable checkpoint\n\n```yaml\n.*?\n```\n?", re.DOTALL
)
checkpoint = f"""# Durable checkpoint

```yaml
checkpoint_version: 26
updated_at: {UPDATED}
observed_main: {BASE}
status: implementing
phase: entity-reconciliation-implementation
active_branch: {BRANCH}
pr: {PR_NUMBER}
base: {BASE}
changed_paths:
  - oteryn-client/crates/protocol-canary/src/lib.rs
  - oteryn-client/crates/protocol-canary/src/reconciliation.rs
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-entity-movement.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-entity-movement-trailing.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-entity-removal.hex
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-entity-removal-invalid-stack.hex
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
implementation:
  remote_entity_movement_0x6D: staged
  remote_entity_removal_0x6C: staged
  caller_owned_resolver: staged
validation: pending
fresh_audit: pending
shared_path_lease: []
ownership:
  protocol_canary: retained
  shared_paths: released
remaining_blocker: General AddItem decoding still requires authoritative item-type and runtime branch metadata; local movement requires complete map-strip decoding.
next_action: Run focused and exact-head validation for the read-only entity reconciliation slice, remediate findings, then merge and return the parent task to the remaining item-catalogue blocker.
```
"""
if checkpoint_pattern.search(task):
    task = checkpoint_pattern.sub(checkpoint, task, count=1)
else:
    task = task.rstrip() + "\n\n" + checkpoint

task_path.write_text(task, encoding="utf-8", newline="\n")

evidence_path = Path(
    "oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md"
)
evidence = evidence_path.read_text(encoding="utf-8")
evidence_marker = "## Read-only entity reconciliation slice"
if evidence_marker not in evidence:
    evidence += f"""

## Read-only entity reconciliation slice

Status: implementation validation pending on `{BRANCH}` / PR `#{PR_NUMBER}`.

Pinned producer revision `bc0068ab80bbf003e128fce0589b4cc89d2682d3` proves:

- remote non-teleport creature movement uses `0x6D + old Position + old stack u8 + new Position` when the creature is not the local player and both positions are visible;
- `RemoveTileThing` emits `0x6C + Position + stack u8` only for stack positions below ten;
- local-player movement appends map-strip payloads and is not part of this slice;
- `0x6C` remains generic at the producer, so this slice admits only a non-local entity resolved by caller-owned authoritative state.

The adapter introduces a read-only resolver contract using only protocol-neutral `TilePosition`, `StackIndex` and session-fenced `EntityHandle` values. Resolution happens after full bounded parsing and trailing-data rejection. Unknown, ambiguous, local-player, stale-session and invalid destination-stack outcomes fail closed. No resolver method may mutate simulation, and no Canary appearance, cache, item or map-strip field crosses the adapter boundary.

Original synthetic fixtures cover positive movement/removal, every truncated prefix, trailing movement data and an invalid removal stack. They contain no credentials, private captures, deployed configuration, proprietary assets or copied producer implementation bodies.
"""
    evidence_path.write_text(evidence, encoding="utf-8", newline="\n")
