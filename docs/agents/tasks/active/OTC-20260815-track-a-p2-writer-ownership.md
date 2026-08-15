---
task_id: OTC-20260815-track-a-p2-writer-ownership
status: validating
agent: ChatGPT
session_id: chatgpt-p2-researcher-20260815-1344
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: runtime-research
phase: p2-writer-ownership
branch: research/OTC-20260815-track-a-p2-writer-ownership
base_branch: main
base_main: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
worktree: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-writer-ownership
worktree_mode: isolated_branch_checkout_equivalent
risk: medium
related_pr: 301
updated: 2026-08-15T13:56:00+02:00
owned_paths:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-writer-ownership.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-writer-ownership/**
  - .github/workflows/tibia-official-client-re-p2-writer-ownership.yml
  - .github/scripts/tibia-official-client-re-p2-writer-ownership.py
depends_on:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45 / merged PR #299
  - coordinator PR #300 for promotion authority
blocks: []
policy_version: 2
prompting_standard_version: 2.1
prompt_contract_version: 1.0.0
execution_mode: github-only
run_scope: single_task
continuation_policy: continue_until_real_stop
task_completion_policy: draft_pr_only
user_communication: terminal_only
claim_check: passed against main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45, isolated Draft PR #301 and coordinator task #300 released to ready before researcher mutation
semantic_result: PROVEN_WRITER_RETAINED_UPSTREAM_BY_TPROTOCOLCLIENTMESSAGEPROCESSOR
proposed_disposition: ACCEPT_WITH_EDITS
successful_run: 31883231486
successful_job: 95008610322
source_artifact_id: 9229609330
source_artifact_sha256: bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c
sanitized_result_artifact_id: 9246558034
sanitized_result_artifact_sha256: d6a08baa10ff6fd7edf7e6e6a21dcaaa0244e2b69a9adc26417bab00a831759a
---

# Objective

Resolve the next concrete P2 ownership edge for the exact official native Linux Tibia client without reviving superseded sink models: determine how the canonical `TProtocolWriter` is retained relative to the accepted `TProtocolClientMessageProcessor -> TGameserverNetworkPacketRawDataProcessor -> TGameserverDualConnection` chain.

# Exact client fence

```yaml
version_mapping: 15.32.df7b29
size: 51965216
sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
platform: official_native_linux_only
```

# Result summary

Successful exact-head workflow run `31883231486` / job `95008610322`:

```text
P2_WRITER_OWNERSHIP_RESULT=PROVEN_WRITER_RETAINED_UPSTREAM_BY_TPROTOCOLCLIENTMESSAGEPROCESSOR
P2_DIRECT_DUALCONNECTION_WRITER_MEMBER=NOT_PROVEN
P2_FRAMING_ORDER=UNKNOWN
P2_TRANSFORM_BOUNDARY=UNKNOWN
P2_FINAL_BINARY_EGRESS=UNKNOWN
P2_CAUSAL_LOCAL_HARNESS=UNKNOWN
```

Detailed evidence:

- `docs/agents/evidence/OTC-20260815-track-a-p2-writer-ownership/20260815-writer-retention-provenance.md`
- `docs/agents/evidence/OTC-20260815-track-a-p2-writer-ownership/result.json`
- reproducer `.github/scripts/tibia-official-client-re-p2-writer-ownership.py`
- workflow `.github/workflows/tibia-official-client-re-p2-writer-ownership.yml`

# FACT — exact source and canonical identities are fenced

The successful workflow:

1. checks out exact Draft head `e603691ac4458efb4132e485f36538fef6a277dd` for the executed discriminator;
2. downloads historical reviewed exact-build artifact `9229609330` from run `31828102313`;
3. verifies ZIP SHA-256 `bc5604ffbcf7e75a6b00dad227aefaa0036ea4792efb61ce85de488b6877782c`;
4. requires the artifact exact-client SHA and selected setup FDE `0x196fee0..0x1972517`;
5. consumes current canonical #299 report from the same checkout for the accepted type/field identities.

Canonical identities used by the gate:

```text
TProtocolWriter RTTI 0x3080728 / vptr 0x2f69dd0
TIODeviceWriter RTTI 0x3080718 / vptr 0x2f69d48
TProtocolWriter : TIODeviceWriter
outer +0xa00/+0xa08 -> TProtocolClientMessageProcessor
outer +0xa10/+0xa18 -> TGameserverNetworkPacketRawDataProcessor
outer +0xc18/+0xc20 -> TGameserverDualConnection
```

# FACT — concrete writer retention

Inside the exact setup FDE, the discriminator proves the following bounded structural relation:

```text
TProtocolClientMessageProcessor
 -> retained intermediate object (exact class UNKNOWN)
 -> retained shared TProtocolWriter
```

Specifically:

- `TGameserverDualConnection` is constructed/retained separately at outer `+0xc18/+0xc20`;
- a concrete object receives canonical `TProtocolWriter` vptr `0x2f69dd0` in the same setup FDE;
- an intermediate retained object stores the writer object/control pair;
- a wrapper retaining that intermediate pair is stored at outer `+0xa00/+0xa08`;
- canonical #299 independently identifies outer `+0xa00/+0xa08` as `TProtocolClientMessageProcessor`.

This resolves the research hypothesis as **indirect writer retention on the upstream `TProtocolClientMessageProcessor` branch**, rather than proving a direct writer member on `TGameserverDualConnection`.

# INFERENCE

Canonical #299 independently proves the processing graph:

```text
TProtocolClientMessageProcessor
 -> TGameserverNetworkPacketRawDataProcessor
 -> TGameserverDualConnection
```

Combining that graph with the writer-retention fact supports:

```text
writer_location_relative_to_dualconnection = UPSTREAM_ON_TPROTOCOLCLIENTMESSAGEPROCESSOR_BRANCH
```

The word `UPSTREAM` is therefore graph-relative inference, not a claim of direct `DualConnection -> writer` membership.

# NOT_PROVEN / UNKNOWN

- direct `TGameserverDualConnection -> TProtocolWriter` member/reference: `NOT_PROVEN`;
- exact class identity of intermediate vptr `0x2f69e30`: `UNKNOWN`;
- exact gameplay framing/serialization order: `UNKNOWN`;
- compression/encryption/sequence transformation boundary: `UNKNOWN`;
- final binary QIODevice/socket egress: `UNKNOWN`;
- causal controlled/local harness: `UNKNOWN`;
- historical `0x3084c70 -> +0xd0 -> 0xb40630` writer-family relationship to canonical `TProtocolWriter`: `UNKNOWN`.

# Negative controls

The successful discriminator fails closed unless all are preserved:

- `0xb46bd0` remains **DISPROVEN as binary gameplay sink evidence** despite writing through a real `TGameserverTCPConnection::QTcpSocket*`;
- old `owner+0x88 -> ... -> 0xb5b880` remains **DISPROVEN/SUPERSEDED**;
- historical source artifact reports `WRITER_DIRECT_CALL_COUNT=0`, preventing generic QIODevice/direct-call coincidence from satisfying the ownership gate.

# Repair history

Run `31883167971` / job `95008465831` failed after source artifact download/digest verification because the parser expected Markdown backticks around canonical address values that are actually inside a fenced code block. Commit `e603691ac4458efb4132e485f36538fef6a277dd` corrected only the textual matcher; no address, client fence, provenance edge or semantic gate was relaxed. Run `31883231486` then passed every exact structural and negative-control marker and uploaded sanitized artifact `9246558034`.

# Acceptance gate

- [x] exact client identity hard-fenced;
- [x] current-main #299 facts used;
- [x] concrete constructor/retention evidence ties the canonical writer to the accepted owner graph;
- [x] exact canonical RTTI/vtable identities required by the gate;
- [x] negative controls reject superseded/generic writer coincidences;
- [x] execution success reported separately from semantic result;
- [x] framing/encryption/final egress remain UNKNOWN rather than overclaimed;
- [x] no credentials/proprietary binary bytes/secret-bearing payloads/account state committed or uploaded by this task;
- [ ] exact final-head repository CI terminal after the durable evidence/task checkpoint.

# Proposed researcher disposition

`ACCEPT_WITH_EDITS` for the bounded retention fact and graph-relative inference.

P2 remains incomplete. The next independent research hypothesis should target the transformation/framing order and final binary egress from the now-narrowed writer branch, with a causal local/custom harness still required before full P2 closure.

# Next action

Wait only for exact final-head repository CI for this durable handoff generation. If terminal green, set this task to `ready`/review handoff and release branch ownership to coordinator PR #300. Do not mutate #300 from this researcher session.
