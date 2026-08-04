from __future__ import annotations

import os
import re
from pathlib import Path

BRANCH = "feat/OTC2-20260804-canary-known-player-appearance"
BASE = "694314af9162b4e435d4b269dbec6ebe7b0a83e4"
UPDATED = "2026-08-04T10:52:00+02:00"
SESSION_ID = "OTC2-20260804T1043+0200-known-player"
PR_NUMBER = os.environ.get("PR_NUMBER", "pending")


def replace_once(path: Path, old: str, new: str) -> None:
    content = path.read_text(encoding="utf-8")
    if new in content:
        return
    if old not in content:
        raise RuntimeError(f"missing replacement anchor in {path}: {old!r}")
    path.write_text(content.replace(old, new, 1), encoding="utf-8", newline="\n")


lib = Path("oteryn-client/crates/protocol-canary/src/lib.rs")
replace_once(lib, "mod inbound;\nmod map;", "mod inbound;\nmod known_player;\nmod map;")
replace_once(
    lib,
    "pub use map::{OPCODE_MAP_DESCRIPTION, decode_current_local_player_only_map};\n",
    "pub use known_player::decode_current_known_remote_player_appearance;\n"
    "pub use map::{OPCODE_MAP_DESCRIPTION, decode_current_local_player_only_map};\n",
)

tests = Path("oteryn-client/crates/protocol-canary/src/known_player/tests.rs")
replace_once(tests, "invalid_type[30] = 1;", "invalid_type[31] = 1;")

task_path = Path(
    "docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md"
)
task = task_path.read_text(encoding="utf-8")
frontmatter = {
    "status: blocked": "status: implementing",
    "phase: item-catalogue-and-local-map-strip-blocker": "phase: known-player-appearance-implementation",
    "branch: main": f"branch: {BRANCH}",
    "updated: 2026-08-04T08:53:00+02:00": f"updated: {UPDATED}",
    'required_base_commit: "14e2718b7ff046b0620d5c838429cef81aa6d340"': f'required_base_commit: "{BASE}"',
    "last_progress_at: 2026-08-04T08:53:00+02:00": f"last_progress_at: {UPDATED}",
    "ci_check_generation: entity-reconciliation-closeout-restack-exact-head": "ci_check_generation: known-player-appearance-focused",
    "terminal_ci_checks_for_current_generation: 5": "terminal_ci_checks_for_current_generation: 0",
    "repair_cycles_for_current_gate: 1": "repair_cycles_for_current_gate: 0",
}
for old, new in frontmatter.items():
    if old in task:
        task = task.replace(old, new, 1)

related = re.search(r"^related_prs: \[(.*?)\]$", task, flags=re.MULTILINE)
if related and PR_NUMBER != "pending":
    values = [value.strip() for value in related.group(1).split(",") if value.strip()]
    if PR_NUMBER not in values:
        values.append(PR_NUMBER)
        task = task[: related.start()] + f"related_prs: [{', '.join(values)}]" + task[related.end() :]

task = task.replace(
    "  - complete known-creature cache, non-player, hidden-health and extension branches",
    "  - nonzero known-cache eviction, non-player, hidden-health and extension branches",
    1,
)
old_matrix = "| creature/entity appearance | `PARTIAL` | One complete post-bootstrap `0x6A` unknown ordinary remote-player branch with zero cache eviction emits `EntityAppeared`. Known/cache-eviction, hidden, summon, monster, NPC, invisible and OTCR branches remain unsupported. |"
new_matrix = "| creature/entity appearance | `PARTIAL` | Complete post-bootstrap `0x6A` ordinary-player branches are implemented for unknown identity with zero cache eviction and known identity marker `0x62`. Nonzero eviction, hidden, summon, monster, NPC, invisible and OTCR branches remain unsupported. |"
if old_matrix in task:
    task = task.replace(old_matrix, new_matrix, 1)

old_remaining = "The known-creature cache transition, nonzero eviction, non-player types, hidden-health, summon, invisible outfit and OTCR extension branches are not normalized as complete accepted families. They remain `UNKNOWN` and unimplemented."
new_remaining = "The complete known ordinary-player appearance branch is staged in this phase. Nonzero cache eviction, non-player types, hidden-health, summon, invisible outfit and OTCR extension branches are not normalized as complete accepted families. They remain `UNKNOWN` and unimplemented."
if old_remaining in task:
    task = task.replace(old_remaining, new_remaining, 1)

section_marker = "# Known ordinary remote-player appearance continuation"
if section_marker not in task:
    section = f"""# Known ordinary remote-player appearance continuation

The pinned Current producer proves a second complete ordinary-player `sendAddCreature` family that does not require item metadata or mutable cache ownership:

```yaml
source_revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
branch: {BRANCH}
pr: {PR_NUMBER}
opcode: 0x6A
position: [x_u16_le, y_u16_le, z_u8]
stack_bound: 0_through_9
known_marker_u16_le: 0x62
entity_id: nonzero_and_distinct_from_local_player
known_header_omits: [cache_eviction_id, entity_type, name]
common_payload:
  health: 1_through_100
  direction: 0_through_7
  visible_outfit: required
  guild_emblem: omitted_for_known_branch
  final_entity_type: ordinary_player
output: GameEventEnvelope::v1(GameEvent::EntityAppeared)
output_name: null
cache_mutation: false
shared_path_lease: []
validation: pending
```

The adapter accepts the wire-carried session-fenced entity identity but does not create, mutate or infer the producer's known-creature cache. Hidden health, invisible outfits, summons, monsters, NPCs, nonzero eviction and OTCR extensions remain rejected.

"""
    task = task.replace("# Exact blocker normalization\n", section + "# Exact blocker normalization\n", 1)

checkpoint_pattern = re.compile(r"# Durable checkpoint\n\n```yaml\n.*?\n```\n?", re.DOTALL)
checkpoint = f"""# Durable checkpoint

```yaml
checkpoint_version: 30
updated_at: {UPDATED}
observed_main: {BASE}
status: implementing
phase: known-player-appearance-implementation
active_branch: {BRANCH}
pr: {PR_NUMBER}
base: {BASE}
changed_paths:
  - oteryn-client/crates/protocol-canary/src/lib.rs
  - oteryn-client/crates/protocol-canary/src/known_player.rs
  - oteryn-client/crates/protocol-canary/src/known_player/tests.rs
  - oteryn-client/tests/integration/canary-world-protocol/fixtures/known-remote-player-appearance.hex
  - oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md
  - docs/agents/tasks/active/OTC2-20260803-playability-p2-canary-world-protocol.md
implementation:
  known_remote_player_appearance_0x6A_0x62: staged
  cache_mutation: false
validation: pending
fresh_audit: pending
shared_path_lease: []
ownership:
  protocol_canary: retained
  shared_paths: released
remaining_blocker: General AddItem/non-empty map decoding still requires authoritative Current item metadata; local-player movement requires complete map strips; nonzero cache eviction and non-player creature branches remain incomplete.
next_action: Run focused and exact-head validation for the known ordinary-player appearance branch, remediate findings, merge, then return the parent task to the remaining item and creature-family blockers.
```
"""
if not checkpoint_pattern.search(task):
    raise RuntimeError("durable checkpoint not found")
task = checkpoint_pattern.sub(checkpoint, task, count=1)

recovery_pattern = re.compile(r"## Recovery checkpoint\n\n```yaml\n.*?\n```\n?", re.DOTALL)
recovery = f"""## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 2
  session_id: {SESSION_ID}
  session_started_at: 2026-08-04T10:43:00+02:00
  checkpointed_at: {UPDATED}
  last_progress_at: {UPDATED}
  phase: known-player-appearance-implementation
  exact_head: pending_patch_commit
  pull_request: {PR_NUMBER}
  active_operation: known-player decoder implementation and exact-head validation
  external_run_ids: []
  operation_started_at: {UPDATED}
  wait_deadline_at: 2026-08-04T11:37:00+02:00
  check_generation: known-player-appearance-focused
  checks_used: 0
  status: active
  safe_to_resume: true
  resume_condition: Continue the exact PR head through focused validation, audit, required CI and protected merge.
  next_action: Validate and merge the complete known ordinary remote-player appearance branch without expanding into item or non-player families.
```
"""
if recovery_pattern.search(task):
    task = recovery_pattern.sub(recovery, task, count=1)
else:
    task = task.rstrip() + "\n\n" + recovery

task_path.write_text(task, encoding="utf-8", newline="\n")

evidence_path = Path(
    "oteryn-client/docs/evidence/playability/p2/canary-current-runtime-baseline.md"
)
evidence = evidence_path.read_text(encoding="utf-8")
evidence_marker = "## Known ordinary remote-player appearance"
if evidence_marker not in evidence:
    evidence += f"""

## Known ordinary remote-player appearance

Status: implementation validation pending on `{BRANCH}` / PR `#{PR_NUMBER}`.

Pinned producer revision `bc0068ab80bbf003e128fce0589b4cc89d2682d3` proves that the known `AddCreature` branch writes marker `0x62` and the creature id, then the common appearance payload. Unlike the unknown branch, it writes no cache-eviction id, entity type or name in the header and omits guild emblem from the common payload.

The staged decoder accepts only a visible ordinary remote player with health `1..=100`, direction `0..=7`, nonzero outfit, at most three icons, final player type, unmarked state, no inspection and a closed walkthrough flag. It emits `EntityAppeared` with the wire-carried session-fenced entity and `name: None`. It never mutates or infers the producer cache.

The synthetic fixture and negative mutations cover every truncated prefix, wrong marker, hidden health, invalid direction, wrong final type, local/zero identity, stale/pre-bootstrap state and trailing data. No credential, private capture, proprietary asset or deployed configuration is included.
"""
    evidence_path.write_text(evidence, encoding="utf-8", newline="\n")
