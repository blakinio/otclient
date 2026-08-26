---
task_id: OTC-20260827-current-game-login-field-provenance
status: in_progress
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: research
branch: research/OTC-20260827-current-game-login-field-provenance
related_pr: 722
base_branch: main
base_main: b74992cf7a628268fe451551897672bceed55e1e
created: 2026-08-27T18:00:00+02:00
risk: high
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
promotion_authority: coordinator_only
implementation_authorized: false
owned_paths:
  - .github/workflows/tibia-official-client-re-login-field-provenance.yml
  - tools/tibia_re_login_field_provenance/
  - docs/agents/tasks/active/OTC-20260827-current-game-login-field-provenance.md
modules_touched: []
---

# Current native game-login field provenance

## Objective

Recover current-build **value provenance** for the already-promoted `GameclientMessageLogin` / `LoginRSAEncryptedBlock` schema without guessing user-facing semantic field names.

Trusted-main prerequisites are terminal:

- current game-login wire-writer promotion: trusted main via PR #706;
- current typed game-login schema promotion: trusted main via PR #719;
- source schema PR #711: closed unmerged as consumed/superseded;
- schema lifecycle closeout: trusted main via PR #721.

Track B PR #284 remains read-only during this research task.

## Exact accepted client fence

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

The workflow must fail closed if the public current package moves away from this fence. A new client build requires a new schema/writer provenance chain instead of mixing evidence across builds.

## Research boundary

Allowed:

- disposable GitHub-hosted runner;
- public launcher package metadata and exact public Linux client file;
- transient static ELF/disassembly inspection;
- RTTI/vtable/FDE/code-reference recovery;
- sanitized static literals and instruction contexts;
- artifact containing addresses, instructions and classifications only.

Forbidden:

- executing the Official Tibia client;
- login, credentials, session values or character selection;
- process-memory inspection or mutation;
- packet/session capture;
- gameplay or input;
- uploading or retaining the proprietary client binary;
- mutating Track B #284;
- naming password/session/AuthInfo fields from intuition.

## Root-cause hypothesis under test

The prior Track B failure is caused by the legacy raw game-login body being structurally incompatible with the current official typed protobuf payload. The outer transport is already proven structurally aligned. Before implementation, the exact provenance of values feeding current protobuf fields must be recovered far enough to map Track B's available login inputs without inventing semantics.

## Required evidence

1. Re-derive `TAuthenticationAndEncryptionInfo` and `TLoginProtocolMessageHandler` exact RTTI/vtables from the exact fenced client.
2. Re-derive handler slot `+0x60` producer and snapshot the complete FDE.
3. Snapshot AuthInfo slots used by the producer (`+0x10`, `+0x18`, `+0x30`, `+0x40`, `+0x50`, `+0x60`, `+0x90`).
4. Recover static identity references/direct calls to those slot implementations with bounded instruction context.
5. Recover constructor/vtable-reference contexts and only static binary literals relevant to those same FDEs.
6. Persist secret-free machine-readable evidence; keep unsupported human semantic names `UNKNOWN`.

## Stop conditions

- public exact client fence mismatch => BLOCKED, no evidence mixing;
- ambiguous RTTI/vtable identity => BLOCKED;
- provenance insufficient to map required Track B inputs => keep the affected mapping `UNKNOWN`, do not implement or E2E;
- no secret-bearing runtime attempt is legal in this source task.
