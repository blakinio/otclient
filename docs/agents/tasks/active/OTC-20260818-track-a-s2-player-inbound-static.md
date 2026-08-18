---
task_id: OTC-20260818-track-a-s2-player-inbound-static
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
execution_mode: github_only
branch: research/OTC-20260818-track-a-s2-player-inbound-static
base_branch: main
base_main: a9e7ab21ed0962482e4381aadd50be92714785a6
related_pr: 512
created: 2026-08-18T10:06:00+02:00
updated: 2026-08-18T10:12:00+02:00
risk: medium
implementation_authorized: true
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
owned_paths:
  - .github/workflows/track-a-s2-player-inbound-static.yml
  - docs/agents/tasks/active/OTC-20260818-track-a-s2-player-inbound-static.md
  - docs/agents/evidence/OTC-20260818-track-a-s2-player-inbound-static/**
  - docs/agents/reports/OTCLIENT-20260818-track-a-s2-player-inbound-static.md
modules_touched:
  - official-client-static-re
reuses:
  - docs/agents/evidence/OTC-20260818-track-a-s1-unfiltered-static-census/**
  - tools/tibia_runtime_bridge/resolver.py
  - tools/tibia_runtime_bridge/profiles/tibia-15.32.df7b29.json
  - exact QMeta reconstruction pattern from merged PR #505
depends_on:
  - OTC-20260818-track-a-s1-unfiltered-static-census
blocks: []
non_overlap:
  - PR #475 physical runtime/worldmap/native-login surfaces are not observed or mutated.
  - PR #302 direct-player-position Draft is not modified; this task may produce static evidence useful to that consumer later.
  - Track B PR #284 is outside scope.
policy_version: 2
context_pressure: medium
decomposition_decision: single
validation_level: focused
repair_cycles_for_current_gate: 1
---

# Objective

Resolve the exact static inbound player-message dispatch surface far enough to prove or bound:

```text
GameserverMessagePlayerDataCurrent / PlayerState / PlayerInventory / PlayerSkills
  -> exact received* method metadata
  -> tibia::game::TPlayerProtocolMessageHandler QMeta method/dispatch target where provable
  -> static downstream owner/call edges toward TPlayerData where provable
```

No runtime is needed or permitted for this task.

# Exact client fence

```yaml
version: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
platform: official_native_linux_only
```

# Starting canonical facts

Promoted by #511:

```text
GameserverMessagePlayerDataBasic    <-> receivedPlayerDataBasicMessage    lexical alignment only
GameserverMessagePlayerDataCurrent  <-> receivedPlayerDataCurrentMessage  lexical alignment only
GameserverMessagePlayerInventory    <-> receivedPlayerInventoryMessage    lexical alignment only
GameserverMessagePlayerSkills       <-> receivedPlayerSkillsMessage       lexical alignment only
GameserverMessagePlayerState        <-> receivedPlayerStateMessage        lexical alignment only
TPlayerProtocolMessageHandler primary vptr = 0x308a008
TPlayerData primary vptr = 0x308ca70
```

Message -> method dispatch and handler -> `TPlayerData` mutation remain `UNKNOWN` until directly proven.

# Questions

1. Recover `TPlayerProtocolMessageHandler` exact Qt metaobject metadata and method table on the exact client.
2. Determine whether target `receivedPlayer*Message` methods are signals/slots/invokables and recover exact QMeta indices/signatures/types.
3. Recover exact dispatch targets from `qt_static_metacall`/equivalent metadata where directly supported.
4. Inspect bounded target code/direct calls/member accesses for downstream owner/data edges.
5. Promote handler -> `TPlayerData` only with direct type/ownership/dataflow evidence; otherwise retain `UNKNOWN`.
6. Do not infer runtime player position or live state from static layout.

# Acceptance

- [x] exact client fence revalidated by first hosted run before its producer-code failure;
- [ ] `TPlayerProtocolMessageHandler` metaobject identity revalidated;
- [ ] exact QMeta target methods/signatures/indices persisted where recoverable;
- [ ] exact static dispatch targets persisted where recoverable;
- [ ] bounded target disassembly/call edges persisted;
- [ ] `TPlayerData` downstream relation classified `FACT | INFERENCE | UNKNOWN` per direct evidence;
- [x] no runtime/login/Synology/X11/process-memory/credential access;
- [x] no raw proprietary client committed/uploaded;
- [ ] temporary producer removed before promotion;
- [ ] exact-head CI/governance and review hygiene before terminal disposition.

# Failure / repair history

## R1 — Capstone skipdata operand access

First exact-head producer run:

```text
run: 32114891658
job: 95642067206
exact packed SHA: PASS
exact unpacked SHA: PASS
client executed: false
runtime access: none
result: producer failure before QMeta result
```

First causal error:

```text
capstone.CsError: Information irrelevant for 'data' instruction in SKIPDATA mode (CS_ERR_SKIPDATA)
```

The producer used one Capstone instance with `skipdata=True` for both whole-section scanning and bounded function decoding, then read `.operands` from skipdata pseudo-instructions.

Repair on head `4c05b244f0c4d6fafaef4364ab6ee4f971e7673f`:

```text
bounded executable functions -> normal Capstone decoder
whole executable sections     -> separate skipdata decoder
skipdata operand reads        -> fail-safe empty operand list on CsError
```

The repair does not change research semantics or broaden scope. No result from the failed run is promoted beyond exact-client fence validation.

# Checkpoint

```yaml
checkpoint_version: 2
status: investigating
pr: 512
last_completed_step: repaired the first deterministic producer failure without touching runtime or broadening scope
blockers: []
next_action: inspect the exact-head post-repair S2 producer; if green, review its sanitized QMeta/dispatch evidence before persisting any FACT, otherwise use only the second bounded repair cycle on the next concrete root cause.
```
