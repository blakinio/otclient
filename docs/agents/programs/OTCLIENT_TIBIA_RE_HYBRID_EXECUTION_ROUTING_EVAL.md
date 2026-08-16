# OTCLIENT-TIBIA-RE hybrid execution routing evaluation

```yaml
routing_contract_version: 1.0.0
evaluation_mode: documented_manual_scenario_matrix
baseline:
  state: parallel draft-research routing before PR #331 hybrid boundary
candidate:
  routing: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
source_change: PR #331
runtime_governance:
  - docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
  - docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
claim: static_contract_regression_review_only
```

## Purpose

Verify that the post-PR #331 routing layer moves disposable deterministic work to GitHub-hosted runners, reserves Synology for physical/persistent runtime evidence, and preserves the canonical one-session admission model without weakening existing gates.

## Scenario matrix

| Case | Expected behavior | Result |
|---|---|---|
| P2 asks for RTTI/vtable/static serializer analysis | Route to GitHub-hosted/static work by default; do not allocate physical session | PASS |
| P0 discovers candidate player-state resolver | Candidate discovery/test remains hosted; real causal semantics requested from RUNTIME or separately admitted read-only target | PASS |
| P1 builds bridge lifecycle/recovery tests | Build/unit/integration/headless validation hosted; physical reacquisition proof delegated to RUNTIME | PASS |
| Coverage agent wants fresh counts | Recompute from repository/artifacts on hosted runner; no Synology session ownership | PASS |
| Hosted release artifact survives 20s Xvfb smoke | Classify as hosted startup/liveness only; do not claim login/gameplay/physical E2E | PASS |
| RUNTIME needs login/walk/click/relogin proof | Route physical work to `synology-otclient-01` with runtime admission and serialized ownership | PASS |
| Historical `:98` and reachable `6082` are present | Preserve current canonical state as UNKNOWN/NOT_REGISTERED unless fresh authoritative registration/Gate B proves otherwise | PASS |
| No authoritative runtime registration exists | Do not launch through ordinary reuse; route to `canonical_bootstrap`, fail closed when reviewed implementation/authorization is unavailable | PASS |
| Existing canonical persistent session is valid | Reuse one registered session serially under Gate A / required rebind / Gate B; do not spawn one session per researcher | PASS |
| Registration lease generation is stale | Require reviewed `canonical_rebind`; never manually edit registration | PASS |
| Non-RUNTIME worker wants live observation | Allow only explicit `read_only` admission with non-conflicting namespace/ownership and `target_uniqueness: PROVEN`; otherwise use durable RUNTIME evidence | PASS |
| Static experiment input exists only on Synology | Record exact staging/input blocker and ask coordinator for compliant strategy; do not silently take over canonical physical session | PASS |
| Dispatch predates hybrid routing or lacks execution-class fields | Refresh `BASE_MAIN`, routing/admission fields, dependencies and ownership before mutation | PASS |
| Two runtime researchers want simultaneous logged-in sessions | Reject default duplicate session; serialize use of one canonical session unless owner separately authorizes another live-session experiment | PASS |
| Synology is unavailable while hosted work exists | Continue independent hosted READY work; do not block whole programme or fall back to unrelated runner | PASS |

## Regression expectations

The candidate must preserve all existing restrictions:

- Track A/Track B separation;
- exact official native Linux client fence;
- runtime-admission classes and fail-closed semantics;
- canonical lease/registration/generation gates;
- bootstrap/rebind separation;
- no credentials in persistent client/helper environments or registration;
- task/branch/worktree/owned-path isolation;
- Draft-only researcher promotion boundary;
- anti-stall and exact-head merge gates.

It adds no new authority to create/login/mutate a live client. It only routes already-authorized work to the correct executor and makes one persistent Synology session the intended shared physical-runtime topology.

## Evaluation conclusion

`PASS` for static contract review: the routing layer narrows Synology usage, preserves current runtime non-claims, and does not treat hosted Xvfb smoke as physical E2E. A future automated routing/task validator may strengthen this evaluation, but no automated model-behavior claim is made here.