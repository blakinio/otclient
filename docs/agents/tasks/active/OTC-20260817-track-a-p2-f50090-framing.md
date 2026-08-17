---
task_id: OTC-20260817-track-a-p2-f50090-framing
status: ready
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: review
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
  - run 32037533068 / hosted job 95410901806
  - run 31904696996 / artifact 9252025461
  - run 32005141186 / artifacts 9279753620 and 9279759553
  - exact helper artifact 9251725866
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

Prove or falsify framing on the already-canonical same-message path ending at the Qt/QTcpSocket-bound `QDataStream::writeRawData @ 0x4dd250`, using only retained exact-client bounded evidence.

## Result

`H1` is **PROVEN** at researcher level.

Exact `0xf50090` bytes establish this ordered serialization before the raw payload:

```text
scalar A: low16(ceil(payload_length/8))
 -> scalar B: DWORD(message+0), semantics UNKNOWN
 -> raw payload pointer/length
 -> QDataStream::writeRawData @ 0x4dd250
```

Current-main PR #492 independently binds this same QDataStream/raw write to the concrete `TGameserverTCPConnection`-owned QTcpSocket. Therefore the pre-payload fields are a concrete outbound framing layer rather than a local-only QBuffer representation.

Exact `0xb47130` bytes additionally prove an earlier same-message envelope transform: prepend one byte, append helper-produced bytes until total QByteArray length is divisible by 8, store appended-byte count in the first byte, then assign the transformed QByteArray back. The helper and optional later indirect transform are not semantically classified.

Researcher terminal classification:

```text
DUALCONNECTION_TO_BINARY_EGRESS=PROVEN
FINAL_BINARY_EGRESS=QDataStream::writeRawData@0x4dd250_AT_QT_QTCPSOCKET_BOUNDARY
FINAL_SOCKET_OWNER=TGameserverTCPConnection
FRAMING=PROVEN
SEQUENCE=UNKNOWN
COMPRESSION=UNKNOWN
ENCRYPTION=UNKNOWN
LINUX_SOCKET_SYSCALL=UNKNOWN
```

This is **not canonical until coordinator promotion**.

## Evidence

- `docs/agents/evidence/OTC-20260817-track-a-p2-f50090-framing/result.json`
- `docs/agents/evidence/OTC-20260817-track-a-p2-f50090-framing/20260817-f50090-egress-framing.md`
- run `32037533068`, hosted job `95410901806`, exact window `0xf50040..0xf50480`, SHA-256 `1d14d72f683455daa3ab065bd48c3588f8755798ce63e70b838569353c3e2cea`
- artifact `9252025461`, SHA-256 `2a866247558b079944d81c9ad33bd4c5361c8144a7f367b273ab3bc19a080991`
- artifact `9279759553`, SHA-256 `8228d6c281cf99f45f5c880b76e7a2817130156fde4cc892a402eccf4af10528`
- artifact `9251725866`, SHA-256 `f669df2ace3db0e269f60287d82c51b69eff11eaf7c7f5b932e049492632bd1e`

## Acceptance

- [x] scalar/raw write claims bound to exact-client instructions;
- [x] same-message/payload provenance retained into canonical QTcpSocket-bound QDataStream;
- [x] exact proven stage order recorded without naming unknown field semantics;
- [x] `FRAMING=PROVEN` only from concrete pre-payload write order;
- [x] `SEQUENCE`, `COMPRESSION`, `ENCRYPTION` and Linux syscall remain `UNKNOWN`;
- [x] RawDataProcessor padding behavior limited to direct byte/dataflow proof;
- [x] no runtime/login/world-map/new source staging/owner-funded AI/full executable upload;
- [x] output remains Draft researcher evidence with coordinator-only promotion authority.

## Rejected / controlled candidates

- `0xb40630/0xb4066b`: disproven as this DualConnection egress branch; the call at `0xb4066b` exists but belongs to a distinct function/path.
- `0xb46bd0`: QString/local8bit/newline negative control; not used.
- `0xc33259`: QMatrix4x4/non-network negative control; not used.
- `0xb5b880`: superseded historical sink; not used.

## Next action

Coordinator independently review/falsify this Draft and, if accepted, promote `FRAMING=PROVEN`. After promotion, the next smallest independent frontier is exact producer/update provenance of `DWORD(message+0)` at `f50107`, to prove or disprove sequence semantics without inferring from width or position.