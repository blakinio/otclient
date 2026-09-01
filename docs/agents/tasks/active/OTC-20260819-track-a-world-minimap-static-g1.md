---
task_id: OTC-20260819-track-a-world-minimap-static-g1
status: validating
agent: ChatGPT
session_id: chatgpt-pr593-audit-remediation-20260901
session_role: audit_remediator
project_lane: otclient
lane: P0-STATE
track_id: official-client-re
task_kind: discovery
phase: independent_audit_remediation
execution_mode: github_only
branch: research/OTC-20260819-track-a-world-minimap-static-g1
base_branch: main
base_main: 54a20bbd8721e92d069974af14d6ebd2f4f5a55d
latest_observed_main: 54a20bbd8721e92d069974af14d6ebd2f4f5a55d
related_pr: 593
created: 2026-08-19T13:45:00+02:00
updated: 2026-09-01T18:45:07+02:00
risk: low
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
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
implementation_authorized: true
e2e_required: false
e2e_result: NOT_APPLICABLE
e2e_reason: documentation-only GitHub-hosted static evidence; no executable, UI, runtime, network, or product behavior changed
current_blocker: FRESH_INDEPENDENT_AUDIT_AFTER_REMEDIATION
next_action: run a fresh independent audit on the remediated exact head; if zero material findings, complete exact-head CI and close out under current-main protection
policy_version: 2
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one historical static-evidence package with bounded audit remediation and no runtime authority
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-world-minimap-static-g1.md
  - docs/agents/reports/OTCLIENT-20260819-track-a-world-minimap-static-g1.md
  - docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g1/**
modules_touched:
  - official-client-re-documentation
reuses:
  - docs/agents/reports/OTCLIENT-20260819-track-a-world-minimap-static-g0.md
  - docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g0/**
  - docs/agents/reports/OTCLIENT-20260816-worldmap-extent-static-re.md
  - docs/agents/contracts/MAP_OBSERVATION_V1.md
depends_on:
  - merged promotion PR #551 / merge 6071b237d70a11ab10e5050cc23730162b0e7e0b
blocks: []
related_prs:
  - 475
  - 551
  - 552
  - 583
  - 593
feature_scope:
  type: documentation
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
---

# Track A world/minimap static G1

## Objective

Reconcile the historical G1 static package after independent audit: preserve useful 2026-08-19 hypotheses, withdraw unsupported current-build promotion authority, refresh against protected main, and close the documentation package without borrowing PR #475 runtime authority.

## Authority and isolation

```yaml
runtime_access: none
mutation_authorized: false
client_byte_mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
```

No Synology/KasmVNC/client-process observation, login, gameplay, input, debugger injection, process-memory access or client-byte mutation was performed.

Historical 2026-08-19 producer fence (superseded; not current trusted authority):

```text
client_version=15.32
client_size=52109920
client_sha256=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
```

Current trusted Track A fence on remediated main:

```text
client_version=15.32.75d4a0
client_size=52105824
client_sha256=d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
```

The historical producer fence above is not promoted to this current build.

## Historical producer evidence and replay result

### Producer v1

```text
head      eff3ddf9c2054c1398975d1a2939a5cd01259b63
run/job   32249741341 / 96057873107
result    SUCCESS (historical)
artifact  9363988901
artifact_status EXPIRED / HTTP 410 on 2026-09-01
zip sha   68e1864b990742814d11501fbf6757fcf5da4677d3718bf093227173ba4d5745
```

The strict Qt method-ID discriminator is retained. Its later convenience `first_direct_call` scan could cross adjacent method cases and is explicitly rejected.

### Producer v2 repair

```text
head      91004362eaa5562cf268fff455c161b6f55dc7c2
run/job   32250742374 / 96060897630
result    SUCCESS (historical)
artifact  9364339983
artifact_status EXPIRED / HTTP 410 on 2026-09-01
zip sha   ba5cdae01c702c618a9944de6b4630605ed3eae85b0bed3f0ba66ec69d3ba81f
Track A governance 32250742373 = SUCCESS
CI                 32250742591 = SUCCESS
```

v2 contains direct bounded disassembly/xref evidence only and removes the flawed call-attribution heuristic.

Both historical producer artifacts contained compact text only and reported `RAW_CLIENT_RETAINED=false`, but both are now expired. Exact job reruns `99940034906` and `99940062914` failed closed before analysis because the September 1 public package no longer matched the historical packed fence; v1 observed packed SHA `439db64ead9b62aa0870094fa0ce30e8e0ccaf35844de1a515692770a7019036`. Cleanup preserved `RAW_CLIENT_RETAINED=false`.

## Acceptance inventory

- [x] historical 2026-08-19 producer fence and successful run/job provenance preserved;
- [x] both expired artifact IDs and digests preserved, with GitHub HTTP 410 status recorded;
- [x] exact historical producer reruns attempted and their fail-closed package-fence mismatch recorded;
- [x] no raw packed/unpacked client retained or uploaded during the original runs or remediation reruns;
- [x] historical F11/F12/F13 address/offset/formula details explicitly downgraded to non-promotable hypotheses;
- [x] current trusted Track A fence recorded separately from the historical producer fence;
- [x] F11/F12/F13 conservatively remain `PARTIAL` with no new G1 canonical semantic promotion;
- [x] F08/F10 remain unchanged and blocked;
- [x] final PR scope remains only the three declared docs/evidence/task paths;
- [x] structured E2E result is `NOT_APPLICABLE` with a concrete documentation-only reason;
- [x] first independent audit findings `WM-G1-AUD-001..003` are durably recorded and remediated in content;
- [ ] fresh independent audit on the remediated exact head before completion/merge.

## Evidence result

### F11 — `PARTIAL -> PARTIAL` (historical hypotheses only; no G1 promotion)

```text
internal state pointer: controller +0x48
current layer:          int32(state +0x60)
valid controller range: 0..15 inclusive
visible width:          int32(state +0x84)
visible height:         int32(state +0x88)
```

The expired 2026-08-19 producer transcription reported that floor-up decrements, floor-down increments, and setter/action paths clamp to `0..15`, recompute the view and notify layer change. Visible-area refresh consumes actual `QQuickItem` width/height from the controller's quick-item owner.

Remaining: complete source-level internal view-state model, tile/cache boundary selection/eviction semantics, and any final required live/stability boundary.

### F12 — `PARTIAL -> PARTIAL` (historical hypotheses only; no G1 promotion)

The expired 2026-08-19 producer transcription reported that `TMinimapMarkerStorage` has three Qt signals followed by `onDelayedCallback` and `setMarkersFromMinimapMarkerFile`. The save signal carries shared `MinimapMarkerFileContent` ownership. `onDelayedCallback` gates its save-side virtual path on byte `storage+0x40`. Exact protobuf type names, `minimapmarkers.bin`, serializer/deserializer failures and marker action families are retained.

Historical bounded `FileDescriptorProto` scan transcription: `MINIMAP_DESCRIPTOR_CANDIDATES=0`; exact protobuf field numbers/types remain UNKNOWN.

### F13 — `PARTIAL -> PARTIAL` (historical hypotheses only; no G1 promotion)

The expired 2026-08-19 producer transcription reported direct method-case disassembly binding the primary conversions to the historical helper addresses. In projection mode `0`:

```text
forward: X=x+32*L, Y=y+32*L
inverse: x=X-32*L, y=Y-32*L, layer=L
oracle:  (3,5,7) -> (227,229) -> (3,5,7)
```

`setAdditionalColumnsAndRows` stores four signed 32-bit parameters at viewport `+0xa0..+0xaf` and schedules recomputation. `translateBySubfieldOffset` adds its two-integer offset component-wise to the viewport pair at `+0x88`.

Remaining: complete non-zero projection/shearing/scale/rounding semantics and any required governed live click/pick round trip.

## Durable outputs

- `docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g1/20260819-layout-schema-transform.md`
- `docs/agents/reports/OTCLIENT-20260819-track-a-world-minimap-static-g1.md`

## Main drift / source PR state

This remediation restacks the final three-path package directly on protected `main@54a20bbd8721e92d069974af14d6ebd2f4f5a55d`. Original pre-remediation head `dc2eb26d4b90ed0464da311d638fa35074a1ebd2` is retained in local backup ref `backup/pr593-pre-remediation-dc2eb26d` and in this task history.

The remediated diff must remain exactly the three declared documentation/evidence/task paths. A fresh `origin/main` readback is required again immediately before promotion because unrelated coordinator work may advance main while this remediation validates.

## Validation and audit remediation

Historical exact-head checks before remediation:

```text
source-docs head 304400b318ee654245b6a927327ea6768c4808ed
Track A governance 32251606403 = SUCCESS
CI                 32251606609 = SUCCESS
blocker head dc2eb26d4b90ed0464da311d638fa35074a1ebd2
Track A governance 32251857622 = SUCCESS
CI                 32251857874 = SUCCESS
```

Fresh independent audit on the blocker head:

```text
auditor       gpt-5.6-luna / medium
session       01a05dcd-59a6-7523-94c4-5c6e7d585f11
result        AUDIT_FAIL
findings      WM-G1-AUD-001 high; WM-G1-AUD-002 high; WM-G1-AUD-003 medium
```

Remediation evidence:

```text
artifact 9363988901 = EXPIRED / HTTP 410
artifact 9364339983 = EXPIRED / HTTP 410
rerun job 99940034906 = FAIL_CLOSED at historical packed fence
rerun job 99940062914 = FAIL_CLOSED at historical packed fence
fresh public packed SHA observed = 439db64ead9b62aa0870094fa0ce30e8e0ccaf35844de1a515692770a7019036
raw client retained = false
```

A second independent audit and fresh exact-head CI/governance are required after the remediation commit.

## Independent-audit blocker

The first fresh independent audit is complete and its three material findings are now content-remediated. This task remains non-terminal until a **second fresh validator session** audits the remediated exact head.

```text
BLOCKER=FRESH_INDEPENDENT_AUDIT_AFTER_REMEDIATION
```

Do not mark Ready or merge on the first failed audit. The second auditor must verify the authority downgrade, current-main freshness, explicit E2E disposition, exact three-path scope and absence of unsupported current-build promotion claims.

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 5
  session_id: chatgpt-pr593-audit-remediation-20260901
  session_started_at: 2026-09-01T18:45:07+02:00
  checkpointed_at: 2026-09-01T18:45:07+02:00
  last_progress_at: 2026-09-01T18:45:07+02:00
  phase: independent_audit_remediation
  exact_head: ae07a3da386d3d9d021cee04d072065405b3008e
  pull_request: 593
  active_operation: none
  external_run_ids: [32249741341, 32250742374, 32251606403, 32251606609]
  rerun_job_ids: [99940034906, 99940062914]
  check_generation: post-audit-remediation
  checks_used: 0
  status: validating
  safe_to_resume: true
  resume_condition: remediated exact head remains three-path only and a fresh independent auditor is available
  next_action: run a fresh independent audit on the remediated exact head; if zero material findings, run exact-head CI/governance, refresh protected main, then close out under repository policy
```

## Invocation counters

```yaml
invocation_started_at: 2026-08-19T13:45:00+02:00
last_progress_at: 2026-09-01T18:45:07+02:00
ci_checks_for_current_head: 0
ci_check_generation: blocker-checkpoint
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 2
context_reconstruction_attempts: 0
stall_warnings: 0
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-01T18:51:48+02:00
head: ae07a3da386d3d9d021cee04d072065405b3008e
branch: research/OTC-20260819-track-a-world-minimap-static-g1
pr: 593
status: validating
context_routes:
  - official-client-re
  - world-minimap-static-g1
  - independent-audit-remediation
owned_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-world-minimap-static-g1.md
  - docs/agents/reports/OTCLIENT-20260819-track-a-world-minimap-static-g1.md
  - docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g1/**
proven:
  - Independent Luna/medium audit returned AUDIT_FAIL with WM-G1-AUD-001 through WM-G1-AUD-003.
  - Producer artifacts 9363988901 and 9364339983 are expired and GitHub returns HTTP 410 for download.
  - Exact historical producer reruns 99940034906 and 99940062914 failed closed at the historical package fence before analysis; v1 observed packed SHA 439db64ead9b62aa0870094fa0ce30e8e0ccaf35844de1a515692770a7019036.
  - Both remediation reruns removed temporary client bytes and reported RAW_CLIENT_RETAINED=false.
  - Current trusted Track A repository fence is 15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a; historical G1 addresses and formulas are not promoted to it.
derived:
  - Safe closeout is an authority downgrade that preserves historical hypotheses, not a current-build semantic promotion.
unknown:
  - Current public unpacked client identity corresponding to packed SHA 439db64ead9b62aa0870094fa0ce30e8e0ccaf35844de1a515692770a7019036; intentionally not derived after historical fence mismatch.
  - Fresh exact-build F11/F12/F13 offsets and formulas for 15.32.75d4a0 or any later public package.
conflicts: []
first_failure:
  marker: WM-G1-AUD-002
  evidence: Expired primary artifacts prevented independent exact-source falsification of the original G1 promotion claims.
rejected_hypotheses:
  - Rerunning the historical workflows would regenerate the old exact-build evidence; the public current package moved and both workflows failed closed at their pinned fence.
changed_paths:
  - docs/agents/tasks/active/OTC-20260819-track-a-world-minimap-static-g1.md
  - docs/agents/reports/OTCLIENT-20260819-track-a-world-minimap-static-g1.md
  - docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g1/20260819-layout-schema-transform.md
validation:
  - command: git diff --check
    result: PASS
    evidence: Remediation diff is whitespace-clean before commit.
  - command: python tools/agents/checkpoint.py docs/agents/tasks/active/OTC-20260819-track-a-world-minimap-static-g1.md --require-checkpoint
    result: PASS
    evidence: Fresh checkpoint validation passed after the mandatory Context checkpoint was added.
blockers:
  - FRESH_INDEPENDENT_AUDIT_AFTER_REMEDIATION
next_action: run a fresh independent audit on the remediated exact head; if zero material findings, run exact-head CI/governance, refresh protected main, then close out under repository policy
```
