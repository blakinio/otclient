---
task_id: OTC-20260818-native-cold-auth-qmeta
status: investigating
agent: ChatGPT
session_id: chatgpt-native-cold-auth-qmeta-20260818
session_role: researcher
project_lane: otclient
lane: COVERAGE-AUDIT
track_id: official-client-re
task_kind: discovery
phase: investigate
execution_mode: github_only
execution_reason: exact-SHA deterministic QMeta recovery does not require the serialized physical runtime
branch: research/OTC-20260818-native-cold-auth-qmeta
base_branch: main
base_main: bd167a8a9b4192b3c87c21423e2af37e897f5e79
updated: 2026-08-18T07:20:00+02:00
risk: high
implementation_authorized: true
research_status: DRAFT_NOT_PROMOTED
promotion_authority: coordinator_only
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
canonical_registration: NOT_APPLICABLE
canonical_lease_generation: NOT_APPLICABLE
registration_lease_generation: NOT_APPLICABLE
gate_a: NOT_APPLICABLE
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: NOT_APPLICABLE
mutation_authorized: false
owned_paths:
  - .github/workflows/track-a-native-cold-auth-qmeta.yml
  - docs/agents/tasks/active/OTC-20260818-native-cold-auth-qmeta.md
  - docs/agents/evidence/OTC-20260818-native-cold-auth-qmeta/**
modules_touched: []
reuses:
  - PR #498 exact-SHA auth/session static evidence (DRAFT dependency)
  - PR #475 GameClient QMeta table constants and static-metacall evidence at head 135c808d40934e3f9dfafe8cb0efb83aade92858 (DRAFT dependency)
depends_on:
  - blakinio/otclient#498
  - blakinio/otclient#475@135c808d40934e3f9dfafe8cb0efb83aade92858
blocks: []
client_version: 15.32.df7b29
client_size: 51965216
client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
packed_client_lzma_sha256: 496c5b3517c0996a1bbd0e76a7738d450f79d0bf4fef140a807044776042dc9b
context_pressure: medium
context_growth: stable
context_score: 6
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one bounded exact-SHA QMeta discriminator with independent paths and no runtime ownership
validation_level: focused
invocation_started_at: 2026-08-18T07:20:00+02:00
last_progress_at: 2026-08-18T07:20:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: draft
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 1
stall_warnings: 0
---

# Objective

Recover, on the exact official native Linux client and without executing it, the concrete Qt/QMeta invocation contract for:

```text
TGameClient::onRequestLoginWithCredentials(QString, QString)
```

needed by `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` to replace the legacy GUI/button cold-auth path with original native client logic below the login form.

# Trust boundary

PR #498 and PR #475 are researcher inputs, not canonical facts merely because they are referenced here. Load-bearing values must be independently revalidated against the exact packed/unpacked SHA in this task before being labelled `FACT`.

No official-client process, X11 state, Synology runner, VNC observer, credentials, session, login budget or live account state may be touched by this task.

# Hypotheses

## H1

The exact `TGameClient` QMeta object represented by the predecessor candidates:

```text
stringdata:      0x1c93cf4
metadata:        0x1c93740
static_metacall: 0xd06260
```

contains `onRequestLoginWithCredentials` as an invokable two-argument method and allows an exact method metadata index to be recovered.

## H2

The static-metacall dispatch for that method resolves to one deterministic executable target whose instruction bytes can be fenced on exact SHA for later PIE/runtime rebinding.

# Acceptance

Persist DRAFT evidence with:

```text
EXACT_PACKED_SHA=PASS
EXACT_CLIENT_SHA=PASS
TGAMECLIENT_QMETA_IDENTITY=PASS|FAIL
COLD_AUTH_METHOD_NAME=onRequestLoginWithCredentials
COLD_AUTH_METHOD_META_INDEX=<integer|UNKNOWN>
COLD_AUTH_ARGC=2|UNKNOWN
COLD_AUTH_ARG_TYPES=<QString,QString|UNKNOWN>
COLD_AUTH_METHOD_FLAGS=<value|UNKNOWN>
COLD_AUTH_DISPATCH_TARGET=<va|UNKNOWN>
COLD_AUTH_TARGET_EXECUTABLE=true|false|UNKNOWN
COLD_AUTH_TARGET_INSTRUCTION_FENCE=<hex|UNKNOWN>
CLIENT_EXECUTED=false
RUNTIME_ACCESS=none
```

Fail closed if the exact SHA changed, the QMeta tables do not parse consistently, more than one dispatch candidate remains equally viable, or the method/target cannot be resolved without guessing.

# Negative controls

- Do not search live process memory.
- Do not start the client or use Synology.
- Do not consume credentials or environment secrets.
- Do not infer method index from a historical call site.
- Do not promote Draft PR #498/#475 prose as fact without exact-SHA reproduction.
- Do not invoke or design calls to `onGameSessionConnected` / `onGameSessionLoginSuccessful` as success shortcuts.

# Checkpoint

```yaml
checkpoint_version: 1
status: investigating
last_completed_step: claimed independent GitHub-hosted static lane after live #475 V24 runtime ownership was proven active
blockers: []
next_action: add the exact-SHA hosted QMeta discriminator and open the required Draft PR before running it
```
