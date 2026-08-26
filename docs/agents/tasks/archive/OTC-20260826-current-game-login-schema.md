---
task_id: OTC-20260826-current-game-login-schema
status: completed
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
branch: research/OTC-20260826-current-game-login-schema
related_pr: 711
base_branch: main
created: 2026-08-26T21:34:00+02:00
completed: 2026-08-27T00:55:00+02:00
risk: high
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
promotion_authority: coordinator_only
owned_paths: []
modules_touched: []
implementation_authorized: false
---

# Archived source research — current game-login schema

Terminal source disposition: **ACCEPT_WITH_EDITS / CLOSED UNMERGED AS SUPERSEDED**.

```text
source PR             #711
source live head       39e1f7343d8c3932356a78db1eae00147e810d7d
source evidence head   d24b6e61d1086094112020db6e7d959c24bdb34a
producer run           33017207072 = SUCCESS
producer job           98338388458 = SUCCESS
artifact               9625060590
artifact digest         sha256:be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
result.json sha256      1940d58a7fcb2615da7f9d47179e6dbdf41397f89b8b522af52da75b076154dc
promotion PR           #719
promotion ready head    fbbd62771a7819e9304733b4737bcf8cff9dc4c4
promotion merge         a2d71495da22d21ec2c648d71e9996aa11b37776
```

The source workflow/analyzer was intentionally not merged. Coordinator PR #719 independently re-downloaded and re-hashed the exact source artifact and promoted only accepted sanitized current-build facts to trusted `main`.

Accepted canonical result now lives under:

- `docs/agents/evidence/OTC-20260827-current-game-login-schema-promotion/20260827-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260827-current-game-login-schema-promotion/result.json`

Current exact public Linux client fence at promotion:

```text
version          15.32.75d4a0
packed sha256    075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f
unpacked sha256  d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a
unpacked size    52105824
```

Promoted current facts prove the generated protobuf wire shape of `GameclientMessageLogin`, nested field 7 `LoginRSAEncryptedBlock`, the nested message wire shape, current `TLoginProtocolMessageHandler +0x60 -> 0xe25620` producer, and retained `TAuthenticationAndEncryptionInfo` source type. Track B's generic outer transport remains structurally aligned while its legacy raw login body is not the current native typed payload.

Explicitly withheld:

```yaml
user_facing_authinfo_field_names: UNKNOWN
password_session_to_specific_rsa_field_mapping: UNKNOWN
causal_explanation_of_track_b_structured_0x14: UNKNOWN
```

No official-client execution, login, credentials, session values, process memory, packet capture, proprietary binary upload or Track B mutation occurred in this source task.

```yaml
closeout:
  source_pr_terminal: CLOSED_UNMERGED_SUPERSEDED
  coordinator_decision: ACCEPT_WITH_EDITS
  promoted_to_trusted_main: true
  promotion_pr: 719
  promotion_merge: a2d71495da22d21ec2c648d71e9996aa11b37776
  audit_result: PASS_BOUNDED
  material_findings_open: 0
  e2e:
    result: NOT_APPLICABLE
    reason: static exact-file protocol reconstruction only
  ownership_released: true
  blocker: none
  next_action: none
```
