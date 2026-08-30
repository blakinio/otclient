---
task_id: OTC-20260828-current-login-field6-runtime
status: implementing
agent: ChatGPT
session_id: chatgpt-20260830-field6-v4-package-cdn-repair
session_role: implementer
policy_version: 2
project_lane: otclient
lane: RUNTIME_RESEARCH
track_id: official-client-re
task_kind: reverse_engineering_runtime
phase: validate
branch: fix/OTC-20260830-field6-package-cdn-throttle
base_branch: main
base_main: 18ff83053f5c5d85c9bce6debab0f7fef6b79ecd
created: 2026-08-28T19:00:00+02:00
updated: 2026-08-30T11:55:00+02:00
risk: high
execution_class: github_hosted
execution_mode: github_actions_static
execution_reason: repository-only TDD repair of the pre-action current-package acquisition regression observed in terminal V4; no live client, credentials, or physical mutation are allowed in this phase
persistent_session_role: none
physical_e2e_required: false
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
credentials_allowed: false
login_allowed: false
relogin_allowed: false
restart_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
physical_action_budget: 1
physical_action_count: 0
implementation_authorized: true
live_runtime_authorization_source: PR_758_COMMENT_5457904227_HISTORICAL_V4_ADMISSION
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: false
  e2e_required: false
context_pressure: medium
context_growth: stable
context_score: 8
estimate_confidence: medium
decomposition_decision: phased
decomposition_reason: keep one field6 task; repair current-package preflight repository-only, then rotate to a separately admitted successor physical generation after trusted-main merge
validation_level: focused
last_completed_step: closed unmerged Draft PR #809 as superseded after a connector-side mark-ready GraphQL failure and opened non-draft replacement PR #811 from the same repair branch/head; this pointer update creates the final exact-head CI generation required before merge
session_rotation_count: 3
heavy_validation_runs: 1
stale_takeover_count: 0
human_interruptions: 0
invocation_started_at: 2026-08-30T11:05:00+02:00
last_progress_at: 2026-08-30T11:55:00+02:00
ci_checks_for_current_head: 0
ci_check_generation: package_cdn_throttle_pr811_final
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
context_reconstruction_attempts: 1
stall_warnings: 0
owned_paths:
  - .github/scripts/test_track_a_current_client_package_parallel.py
  - .github/scripts/test_track_a_current_login_field6_runtime.py
  - .github/scripts/test_track_a_current_login_field6_security_contract.py
  - .github/scripts/audit_track_a_current_login_field6_admission.py
  - .github/scripts/track_a_current_client_package_materialize.py
  - .github/scripts/track_a_current_client_package_acquire.sh
  - .github/scripts/track_a_current_login_field6_runtime.sh
  - .github/scripts/track_a_current_login_field6_runtime_secret_wrapper.sh
  - .github/workflows/track-a-current-client-package-materializer.yml
  - .github/workflows/track-a-current-login-field6-runtime.yml
  - docs/agents/tasks/active/OTC-20260828-current-login-field6-runtime.md
  - docs/agents/reports/OTC-20260829-field6-v4-admission-v2.md
  - docs/agents/evidence/OTC-20260828-current-login-field6-runtime/**
  - docs/superpowers/plans/2026-08-28-field6-materializer-repair.md
  - docs/superpowers/plans/2026-08-28-field6-v4-observation.md
modules_touched:
  - track-a-ephemeral-runtime-research
depends_on:
  - merged PR #752 exact-current field6 scalar-owner promotion
  - merged PR #754 exact-current client fence
  - merged PR #758 runtime observation implementation
  - merged PR #775 bounded exact-current package materialization repair
  - merged PR #783 V4 generation and historical-rerun guard
  - merged PR #795 self-hosted secret-runner boundary
  - merged PR #798 reusable self-hosted boundary audit
  - merged PR #802 terminal Synology host-probe evidence
  - merged PR #804 independent ephemeral physical runtime contract/routing
  - merged PR #806 independent V4 consumer
  - merged PR #807 independent host wait gate
  - PR #758 owner V4 admission comment 5457904227
  - PR #758 consumed V4 trigger comment 5467500633
  - V4 run 33300352335 / job 99227195253
  - closed superseded Draft PR #809
  - replacement PR #811
blocks:
  - OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE
---

# Objective

Recover the exact current public scalar carried in `edx` when the official native Linux Tibia client enters the statically proven `GameclientMessageLogin` producer at `PIE + 0xe25620`, then promote that scalar as the only admissible Track B field6 input.

The current phase is a repository-only repair of package acquisition. It is deliberately `runtime_access: none`; no repair commit or PR may receive Tibia credentials, execute downloaded Tibia content, submit login, perform GUI/process mutation, select a character, enter the world, capture network payloads, or consume the remaining one-action physical budget.

# Exact client fence

The accepted current official native Linux client fence remains:

```yaml
version: 15.32.75d4a0
size: 52105824
sha256: d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
packed_bin_client_sha256: 075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
producer_entry: 0xe25620
FIELD6_VALUE: UNKNOWN
```

No scalar may be guessed or promoted without a later separately admitted physical observation.

# Terminal V4 reconciliation

The V4 owner admission on PR #758 is comment `5457904227`. The distinct live trigger was PR #758 comment `5467500633` with the exact body:

```text
AUTHORIZE_CURRENT_LOGIN_FIELD6_RUNTIME_V4 once=true
```

That comment created workflow run `33300352335`, attempt 1, job `99227195253` on runner `molehill-otclient-v4-01`. The fresh independent provenance gate and trusted-main admission passed. The task-owned WARP gate then passed, but exact-current package materialization failed with:

```text
FETCH_FAILED:curl_22
```

GitHub shows the following later steps as skipped:

- Consume exact owner authorization once;
- inject `TIBIA_TEST_EMAIL` / `TIBIA_TEST_PASSWORD` into the protected wrapper;
- start the official client;
- submit login;
- validate or upload field6 evidence.

Cleanup completed with `TRACK_A_FIELD6_PACKAGE_CLEANUP=PASS`. Therefore the terminal V4 result is authoritative as:

```yaml
physical_action_count: 0
login_submit_count: 0
FIELD6_VALUE: UNKNOWN
owner_authorization_consumed: false
credentials_injected: false
official_client_started: false
```

The V4 trigger is consumed as a generation identifier and must not be posted again or replayed. `GITHUB_RUN_ATTEMPT != 1` remains forbidden.

# Package-acquisition diagnosis

## FACT — V3 serial behavior

V3 run `33202129157` / job `98953921602` reached `TRACK_A_FIELD6_PACKAGE_WARP=PASS`, then continued serial exact-package materialization for about 17 minutes 30 seconds until the 18-minute workflow deadline cancelled the job. Its log contains no `curl_22` package HTTP failure. Authorization, credentials, client execution, and login were not reached.

## FACT — V4 parallel behavior

Merged repair #775 changed the live wrapper to `FILE_WORKERS='8'` while preserving a hard maximum of 16. V4 run `33300352335` reached the same WARP PASS boundary and then failed with `curl_22` roughly seconds into package materialization, before authorization consumption.

## FACT — current disposable public probe

On the task-owned diagnostic copy of `OTClientV4Clean`, a public, secret-free probe re-established WARP and fetched the current manifest. It proved:

```text
MANIFEST_VERSION=15.32.75d4a0
MANIFEST_FILE_COUNT=1634
CLIENT_REMOTE=bin/client.lzma
CLIENT_PACKEDSIZE=10215969
CLIENT_PACKEDHASH=075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
CLIENT_UNPACKEDSIZE=52105824
CLIENT_UNPACKEDHASH=d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
```

Through WARP the manifest returned successfully, but range probes for all 1634 payload rows returned HTTP `403`. A direct non-WARP probe returned HTTP `403` for the manifest, `bin/qt.conf.lzma`, and `bin/client.lzma`.

The exact current 403 response headers/cookies remain UNKNOWN because `Molehill-PC` disconnected from Remote Desktop during the bounded header-read probe. This missing detail does not authorize guessing a CDN requirement.

## INFERENCE — causal hypothesis

Confidence: medium-high. The 8-way payload concurrency introduced by #775 likely triggered or materially worsened the current `static.tibia.com`/edge access-throttling behavior. The strongest repository evidence is the controlled contrast: V3 serial transfer continued for 17m30s without `curl_22`, whereas V4 with 8 workers failed almost immediately after the same WARP PASS. This remains an inference until a current response-header or equivalent authoritative CDN diagnostic proves the exact policy.

# Repair design and TDD boundary

The smallest fail-closed repair is to restore the production acquisition path to one file worker while retaining the existing bounded materializer implementation and all packed/unpacked integrity checks, and to solve the already-proven serial wall-clock problem by increasing only the bounded live-observation job deadline to 45 minutes.

Required invariants:

- production wrapper pins `FILE_WORKERS='1'`;
- materializer default is serial unless an explicit fixture/tool caller requests bounded concurrency;
- `MAX_FILE_WORKERS=16`, validation, deterministic result ordering, exact packed/unpacked hashes and exact client fence remain intact;
- WARP/SOCKS task ownership remains intact;
- downloaded content is never executed during package preflight;
- partial/cancelled state cleanup remains fail-closed;
- live observation job timeout is exactly 45 minutes, a bounded heavy-operation ceiling justified by V3 already exceeding the old 18-minute package deadline;
- the materializer contract workflow must cover the live workflow path so a future timeout/pinning regression emits the contract check.

Repository repair E2E is `NOT_APPLICABLE`: this phase is intentionally static/hosted and must not execute the official client or consume live login authority. A later successor physical generation is a separate E2E/admission phase and remains required before field6 can be promoted.

# Repair implementation and validation

## FACT — TDD RED

Closed Draft PR #809 was initially opened from `fix/OTC-20260830-field6-package-cdn-throttle`. RED head `584ed49386354579b0e63d54f03a0e19d5f3fd88` produced materializer contract run `33304674507`, job `99238982400`, which failed exactly with:

```text
FIELD6_MATERIALIZER_CDN_THROTTLE_RED: DEFAULT_FILE_WORKERS must be 1
```

The same RED generation also exposed a distinct transition defect: the security contract accepted only the historical live V4 task shape, and the V4-specific admission audit rejected package-repair paths even when the task was explicitly `runtime_access: none`.

## FACT — minimal GREEN

GREEN implementation head `3f3b42b3a3a66f322d8610d68a10ebaf8f25291d` changes only the intended behavior:

- `.github/scripts/track_a_current_client_package_materialize.py`: `DEFAULT_FILE_WORKERS` is `1` while `MAX_FILE_WORKERS` remains `16`;
- `.github/scripts/track_a_current_client_package_acquire.sh`: production `FILE_WORKERS='1'`;
- `.github/workflows/track-a-current-login-field6-runtime.yml`: bounded live timeout `45`; static-safe repair state runs security/runtime validation but skips only the historical V4-diff admission audit, while any non-static state still invokes that full audit;
- `.github/workflows/track-a-current-client-package-materializer.yml`: live field6 workflow is included in contract path coverage;
- `.github/scripts/test_track_a_current_login_field6_security_contract.py`: accepts exactly either static-safe or live-authorized task state while continuing to validate the executable live workflow's independent-runner, rerun, secret-ordering, stdin-secret and provenance controls;
- `.github/scripts/test_track_a_current_client_package_parallel.py`: preserves explicit bounded-concurrency fixture coverage while requiring serial production/default behavior and the 45-minute live ceiling.

All exact client packed/unpacked size and SHA fences, deterministic materialization ordering, WARP/SOCKS ownership, downloaded-content non-execution and cleanup behavior remain covered by the hosted contract.

## FACT — checkpoint verification

Implementation head `3f3b42b3a3a66f322d8610d68a10ebaf8f25291d` passed package materializer, field6 runtime/static audit, Track A governance, self-hosted boundary and CI syntax/workflow validation; the physical observation job was SKIPPED.

The durable checkpoint head `cc4f021a7113e5988986af4cd4d4d4b90417d8a5` then received its own exact-head verification. In run `33305040161`, `CI / Required` job `99240025660` completed SUCCESS; package/runtime/admission/governance/self-hosted-boundary checks also completed SUCCESS, and the physical `One-shot isolated field6 observation` check `99239959490` was SKIPPED. Review threads and reviews on #809 were empty and `main` remained `18ff83053f5c5d85c9bce6debab0f7fef6b79ecd`.

## FACT — PR replacement without code change

The connected GitHub `mark ready for review` mutation for #809 failed on a connector-side GraphQL schema error (`Repository.fullDatabaseId`). Readback proved #809 remained `draft=true`. To avoid bypassing the ready gate, #809 was closed unmerged as superseded. Non-draft replacement PR #811 was opened from the same repair branch at the same verified `cc4f021a7113e5988986af4cd4d4d4b90417d8a5` head. No code changed as part of that replacement.

This task-pointer commit is the only change after replacement and therefore must receive its own exact-head CI/readback on PR #811 before merge.

# Independent host state

`Molehill-PC` went offline from Remote Desktop during public HTTP diagnostics. No live action is legal while the host is unavailable.

The existing `OTClientV4Clean` instance has been used for public diagnostics after the terminal V4 failure and is therefore no longer admissible as a fresh secret-bearing successor guest. When the host becomes available, it must be terminated and unregistered, and any successor generation must start from a brand-new guest imported from the pinned Canonical rootfs and re-prove all independent-runtime isolation/provenance gates. Synology remains disqualified for this secret-bearing ephemeral task by trusted host-probe evidence.

# Successor-generation boundary

This repair does not create or authorize V5 (or any other successor label). After repair PR #811 is reviewed, exact-head GREEN, and merged, a separate trusted-main admission update must record the terminal V4 pre-action result, preserve `physical_action_count: 0`, rotate to one distinct successor generation/trigger, and restore `ephemeral_isolated` credential/login authority only after all independent-runtime prerequisites are re-proven. The old V4 trigger/comment must never be reused.

Track B remains blocked until a later sanitized evidence-promotion PR proves and merges one exact `FIELD6_VALUE=<uint32>` from the official current client.

# Next action

Require all exact-head workflows for this PR #811 pointer commit to finish GREEN, confirm no unresolved review threads/reviews and no material `main` drift, then squash-merge PR #811 with an expected-head guard. Once #811 is on trusted `main`, rotate this same task through a separate successor-generation admission update; do not reuse V4 and do not restore live credential/login authority until a brand-new independent guest is available and re-proves all isolation/provenance gates.
