---
task_id: OTC-20260817-track-a-p2-f50090-framing
status: investigating
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: investigate
branch: docs/OTC-20260817-track-a-p2-f50090-framing
base_branch: main
base_main: c1adcf491580e28d40f215356a9e559af2ccadc4
risk: medium
owned_paths:
  - docs/agents/tasks/active/OTC-20260817-track-a-p2-f50090-framing.md
  - docs/agents/evidence/OTC-20260817-track-a-p2-f50090-framing/**
modules_touched: []
reuses:
  - PR #492 canonical Qt/QTcpSocket-bound egress promotion
  - PR #449 exact-client bounded processor artifact run 32005141186
  - PR #310 accepted downstream artifact run 31904696996
  - PR #488 exact-client f50090 bounded hosted decode run 32037533068
depends_on:
  - main@c1adcf491580e28d40f215356a9e559af2ccadc4
  - PR #492 merged canonical outbound reachability
blocks: []
policy_version: 2
prompting_standard_version: 2.1
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
task_completion_policy: checkpoint_only
user_communication: low_noise
decomposition_decision: single
validation_level: focused
execution_class: github_hosted
source_staging_class: existing_exact_client_artifact_reuse
runtime_access: none
persistent_session_role: none
physical_e2e_required: false
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
owner_funded_ai_api_authorized: false
promotion_authority: coordinator_only
feature_scope:
  type: protocol
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: internal_only
exact_client:
  version: 15.32.df7b29
  size: 51965216
  sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
  platform: official_native_linux_only
---

# Track A P2 — outbound framing at `0xf50090`

## Objective

Use only already-retained exact-client bounded evidence to prove or falsify the smallest post-`#492` transport-semantic frontier:

```text
Does the proven QTcpSocket-bound `0xf50090 -> 0x4dd250` path serialize a concrete frame header around the same outbound payload?
```

Do not broaden into a generic Qt write census, Linux syscall tracing, runtime/login, world-map work or unsupported protocol semantics.

## Accepted canonical input

Current `main@c1adcf491580e28d40f215356a9e559af2ccadc4` promotes:

```text
same outbound message
 -> TGameserverDualConnection +0x78 branch
 -> virtual +0x30 @ 0xb56c93
 -> TConnectionMultiplexer::write @ 0xf50040
 -> second virtual +0x30 @ 0xf50090
 -> TGameserverTCPConnection::write @ 0xb40a10
 -> concrete TGameserverTCPConnection-owned QTcpSocket
 -> QDataStream
 -> QDataStream::writeRawData @ 0x4dd250
```

Canonical terminal state before this task:

```text
DUALCONNECTION_TO_BINARY_EGRESS=PROVEN
FINAL_BINARY_EGRESS=PROVEN_AT_QT_QTCPSOCKET_BOUNDARY
FINAL_SOCKET_OWNER=TGameserverTCPConnection
FRAMING=UNKNOWN
SEQUENCE=UNKNOWN
COMPRESSION=UNKNOWN
ENCRYPTION=UNKNOWN
LINUX_SOCKET_SYSCALL=UNKNOWN
```

## Hypothesis

`H1`: exact bounded bytes already retained for `0xf50090` prove a deterministic scalar header is serialized to the same QDataStream before the raw outbound payload, sufficient to classify framing as `PROVEN` at the Qt/QTcpSocket boundary.

A scalar's width/order may be proven without assigning a semantic name to the field. Sequence, compression and encryption remain separate hypotheses.

## Evidence inventory

Primary exact-client evidence to independently re-evaluate:

- run `32037533068`, hosted job `95410901806`, main window `0xf50040..0xf50480`, SHA-256 `1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea`;
- run `31904696996`, artifact `9252025461`, SHA-256 `2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991`;
- run `32005141186`, source artifact `9279753620`, SHA-256 `6c970c23aa95856698eb71024937ed847502fb1f040701ce04c632da32c38d32`, hosted artifact `9279759553`, SHA-256 `8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528`;
- current-main canonical QTcpSocket-bound promotion under `docs/agents/evidence/OTC-20260817-track-a-p2-qtcpsocket-boundary-promotion/`.

No new source staging is authorized by this task unless existing evidence proves insufficient and a separately persisted minimal producer contract is first justified.

## Negative controls

Do not use as framing/egress proof:

- `0xb40630/0xb4066b` as the DualConnection egress branch;
- `0xb46bd0` QString/local8bit/newline path;
- `0xc33259` QMatrix4x4/non-network path;
- superseded `0xb5b880`;
- generic Qt `QIODevice::write` census;
- class names without dataflow;
- vtable adjacency;
- mere possession of a `QTcpSocket*`.

## Acceptance

- [ ] independently bind every claimed scalar/raw write to exact instructions from an exact-client bounded artifact;
- [ ] preserve same-message/payload provenance into the already-proven QTcpSocket-bound QDataStream;
- [ ] state exact serialized stage order without inventing field semantics or byte order;
- [ ] classify `FRAMING` as `PROVEN` only if the pre-payload header is instruction/dataflow-proven;
- [ ] keep `SEQUENCE`, `COMPRESSION`, `ENCRYPTION` and Linux syscall boundary `UNKNOWN` unless separately direct evidence resolves them;
- [ ] record RawDataProcessor padding behavior only to the strength directly shown by bytes; do not label its helper/encryption semantics without proof;
- [ ] no live runtime, world-map, login, owner-funded AI, raw executable upload or proprietary full-binary commit;
- [ ] publish only Draft researcher evidence and route it to coordinator review; researcher does not self-promote canonical state.

## Current next action

Independently decode the retained `0xf50090` write sequence and cross-check it against the current-main QTcpSocket-bound provenance. If the header is proven, persist a bounded Draft evidence package and stop this researcher frontier at the semantic boundary; leave the 32-bit field provenance as the next smallest falsifiable hypothesis.