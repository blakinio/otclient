---
task_id: OTC-20260728-canary-current-evidence
coordination_id: ""
status: completed
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R06
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-CP
parallel_lane_state: archived
coordinator_task: none
branch: docs/OTC-20260728-canary-current-evidence
base_branch: main
created: 2026-07-28T23:25:00+02:00
updated: 2026-07-28T23:40:00+02:00
last_verified_commit: "1c47cc734e1e4526082421477e8086c430598490"
required_base_commit: "9b5c86dff694aa65f4b264683f9c5ce3bf000035"
risk: low
related_issue: ""
related_pr: "#63"
depends_on:
  - merged foundation audit PR #47
  - merged current parallel-wave plan PR #59
integration_after:
  - "9b5c86dff694aa65f4b264683f9c5ce3bf000035"
blocks: []
owned_paths:
  - oteryn-client/docs/research/canary-current/**
  - docs/agents/tasks/archive/OTC-20260728-canary-current-evidence.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - current Canary protocol-profile source evidence
  - accepted Oteryn client architecture and foundation audit
crates_touched: []
features_touched: []
contracts_touched:
  - evidence only; no accepted contract modification
modules_touched: []
reuses:
  - foundation audit Canary compatibility report
  - accepted protocol-boundary and session architecture
  - current Canary profile registry, transport/login and multi-channel source
  - current Platform Game Session to Canary contract
public_interfaces:
  - documentation evidence only
cross_repo_tasks: []
performance_evidence:
  - no runtime or performance claim
security_evidence:
  - no credentials, private captures, packet bytes or proprietary content
  - fixture plan requires synthetic provenance and secret/private-data exclusion
---

# Goal

Revalidate the exact current Canary `ProtocolProfileId::Current` evidence needed for a future minimum-playable Rust adapter and produce a provenance-first fixture acquisition plan without adding protocol code, packet constants or external-repository changes.

# Result

Merged PR #63 delivered four isolated evidence documents under `oteryn-client/docs/research/canary-current/`:

- `README.md` with exact repository cuts, evidence labels and implementation boundary;
- `CURRENT_PROFILE_MATRIX.md` with Current 15.25 transport/login/profile/build evidence and MPS family ownership;
- `FIXTURE_ACQUISITION_MANIFEST.md` with provenance metadata and positive/boundary/truncated/malformed/wrong-gate/out-of-order requirements;
- `CHANNEL_AND_SESSION_GAPS.md` separating response-local world indexing, Canary process/channel IDs, Platform world IDs and future product `WorldChannelId`.

# Material findings

- Canary Current compatibility is an exact revision/profile/transport/login/feature/build tuple, not only protocol number 1525.
- Modern multi-channel login serializes a response-local zero-based world-table index; it is not automatically a stable product channel ID.
- Platform world, Canary channel row/process, response-local world index and product channel identifiers require an explicit mapping and stability contract.
- Gateway native-auth v1 remains limited to one configured Platform world and one exact process-local Canary issuer.
- The first WS-R06 package should isolate Current transport/login parsing against provenance-verified synthetic fixtures before channel-aware routing work.

# Evidence cuts

- otclient base: `9b5c86dff694aa65f4b264683f9c5ce3bf000035`
- Canary current: `87149c6b527f43025860c20cca0a440091ee8730`
- Oteryn Platform current: `285eb5f89b8f83752fa4d5798bb242136b7b9ae6`

External repositories remained read-only.

# Validation

| Evidence | Result |
|---|---|
| complete five-file/full-patch review on `1c47cc734e1e4526082421477e8086c430598490` | PASS |
| Rust Client run `30401061507` | PASS: Windows workspace and Supply Chain |
| repository CI run `30401062033` | PASS: scope, syntax/workflow, Lua, informational analysis and `CI / Required` |
| ready-for-review CI run `30401213650` | PASS: all emitted required jobs; legacy Windows build skipped correctly |
| comments, submitted reviews and unresolved threads | none |
| current base before merge | PASS: main remained `9b5c86dff694aa65f4b264683f9c5ce3bf000035` |

# Merge

- PR: #63
- exact validated head: `1c47cc734e1e4526082421477e8086c430598490`
- squash merge: `68567dbb118a3b3f2e420b62f5360979f461a725`
- merged: 2026-07-28

# Boundaries preserved

- no packet constants or byte fixtures;
- no Rust product code, Cargo, lockfile, CI or architecture changes;
- no accepted cross-repository contract modification;
- no external-repository writes;
- no credentials, private captures, proprietary assets or personal data;
- no Rust parser, runtime, server or compatibility claim.

# Next action

A future WS-R06 implementation task must perform a fresh producer preflight, create shared coordination IDs, select one exact Canary revision/build, acquire the synthetic fixture corpus described by this package and fail closed for unsupported profiles/pairs.

# Completion

- Final status: completed
- PR: #63
- Merge commit: `68567dbb118a3b3f2e420b62f5360979f461a725`
- Archived at: `docs/agents/tasks/archive/OTC-20260728-canary-current-evidence.md`
