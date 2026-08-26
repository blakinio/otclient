---
task_id: OTC-20260827-current-game-login-schema-promotion
status: completed
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: archived
related_pr: 719
base_branch: main
base_main: e621a1407d124a71dc9437912e1676aa8929cc11
created: 2026-08-27T00:36:00+02:00
completed: 2026-08-27T00:55:00+02:00
risk: high
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
owned_paths: []
modules_touched: []
implementation_authorized: false
---

# Archived coordinator promotion — current game-login schema

Terminal result: **DONE / ACCEPT_WITH_EDITS**.

Coordinator promotion PR #719 was built directly from trusted `main@e621a1407d124a71dc9437912e1676aa8929cc11`, contained exactly three docs/evidence files, independently re-downloaded and re-hashed source artifact `9625060590`, preserved unsupported password/session/AuthInfo semantics as `UNKNOWN`, and squash-merged to trusted main as:

```text
promotion merge     a2d71495da22d21ec2c648d71e9996aa11b37776
ready head          fbbd62771a7819e9304733b4737bcf8cff9dc4c4
required CI run     33020803060 = SUCCESS
CI / Required job   98350466328 = SUCCESS
review threads      0
submitted reviews   0
changed files       3 docs/evidence paths
```

Independent audit input:

```text
source PR            #711
source live head      39e1f7343d8c3932356a78db1eae00147e810d7d
source evidence head  d24b6e61d1086094112020db6e7d959c24bdb34a
producer run          33017207072 = SUCCESS
producer job          98338388458 = SUCCESS
source artifact       9625060590
artifact digest       sha256:be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
result.json sha256    1940d58a7fcb2615da7f9d47179e6dbdf41397f89b8b522af52da75b076154dc
```

Canonical accepted result now lives under:

- `docs/agents/evidence/OTC-20260827-current-game-login-schema-promotion/20260827-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260827-current-game-login-schema-promotion/result.json`

Accepted current facts include the exact client fence, generated-message ABI needed to interpret the captured serializers, exact `GameclientMessageLogin` and nested `LoginRSAEncryptedBlock` wire shapes, current `TLoginProtocolMessageHandler +0x60 -> 0xe25620` producer, retained `TAuthenticationAndEncryptionInfo` source type, and rejection of Track B #284's legacy raw login body as matching the current typed native payload.

Explicitly not promoted:

```yaml
password_session_semantic_field_names: UNKNOWN
password_session_to_rsa_field_mapping: UNKNOWN
retained_authinfo_user_facing_field_names: UNKNOWN
causal_explanation_of_track_b_structured_0x14: UNKNOWN
```

Source PR #711 was closed unmerged as consumed/superseded after promotion. Its workflow/analyzer was not merged. The active promotion task record is removed by this lifecycle closeout so current Track A task governance can evaluate only live ownership records.

```yaml
closeout:
  implementation_complete: true
  audit:
    result: PASS_BOUNDED
    decision: ACCEPT_WITH_EDITS
    material_findings_open: 0
  e2e:
    result: NOT_APPLICABLE
    reason: docs-only promotion of static exact-file protocol evidence
  final_required_ci:
    head: fbbd62771a7819e9304733b4737bcf8cff9dc4c4
    run: 33020803060
    job: 98350466328
    result: PASS
  pull_requests:
    source_711: CLOSED_UNMERGED_SUPERSEDED
    promotion_719: MERGED
    unresolved_review_threads: 0
  task_status: completed
  task_archived: true
  ownership_released: true
  blocker: none
  next_action: Track B #284 may consume only trusted-main promoted facts.
```
