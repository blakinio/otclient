---
task_id: OTC-20260827-current-game-login-field-provenance
status: completed
agent: ChatGPT
session_role: researcher
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: discovery
phase: archived
branch: research/OTC-20260827-current-game-login-field-provenance
related_pr: 722
base_branch: main
base_main: b74992cf7a628268fe451551897672bceed55e1e
created: 2026-08-27T18:00:00+02:00
completed: 2026-08-27T08:50:00+02:00
risk: high
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
promotion_authority: coordinator_only
implementation_authorized: false
owned_paths: []
modules_touched: []
---

# Archived source research — current game-login field provenance

Terminal source disposition: **ACCEPT_WITH_EDITS / CLOSED UNMERGED AS SUPERSEDED**.

```text
source PR            #722
source head          36320a5e024f1ffab70592be52404da351b16b27
producer run         33046520991 = SUCCESS
producer job         98431684189 = SUCCESS
artifact             9635892718
artifact sha256       fca8de5f33c1c80f57b80a7575a9f9eabf2664d7355c25275e02c2a479b49e62
result.json sha256    d4926050670959c78d3dc59d1fd3dff32ea328fbde0603c538ab43e3ea2510a7
promotion PR         #724
promotion merge      4c9667d7770613ff24cf10f497c8826eb12dabab
```

The source workflow and analyzers were intentionally not merged. Coordinator PR #724 independently audited and promoted only exact structural source-slot → protobuf-field provenance. Unsupported user-facing names and password/session mapping remain `UNKNOWN`.

The failed optional Qt metadata experiment (`CHARACTER_SELECTION_QMETA_AMBIGUOUS=0`) was not promoted and was not replaced by a heuristic.

No official-client execution, login, credentials, session values, process memory, packet capture, gameplay, or proprietary binary upload occurred.

```yaml
closeout:
  source_pr_terminal: CLOSED_UNMERGED_SUPERSEDED
  coordinator_decision: ACCEPT_WITH_EDITS
  promoted_to_trusted_main: true
  promotion_pr: 724
  promotion_merge: 4c9667d7770613ff24cf10f497c8826eb12dabab
  material_findings_open: 0
  ownership_released: true
  blocker: none
```
