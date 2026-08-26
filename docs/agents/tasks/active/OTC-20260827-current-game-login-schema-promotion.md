---
task_id: OTC-20260827-current-game-login-schema-promotion
status: validating
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P2-NETWORK
track_id: official-client-re
task_kind: integration
phase: validate
branch: docs/OTC-20260827-current-game-login-schema-promotion
related_pr: 719
base_branch: main
base_main: e621a1407d124a71dc9437912e1676aa8929cc11
created: 2026-08-27T00:36:00+02:00
updated: 2026-08-27T00:43:00+02:00
risk: high
execution_mode: repository_static
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
runtime_owner_task: NOT_APPLICABLE
mutation_authorized: false
owner_funded_ai_api_authorized: false
promotion_authority: coordinator
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
validation_level: focused
owned_paths:
  - docs/agents/evidence/OTC-20260827-current-game-login-schema-promotion/**
  - docs/agents/tasks/active/OTC-20260827-current-game-login-schema-promotion.md
modules_touched:
  - official-client-re
  - protocol-research
reuses:
  - source PR #711 exact artifact 9625060590
  - trusted-main wire-writer promotion #706/#707
depends_on:
  - source task OTC-20260826-current-game-login-schema
  - source Draft PR #711
blocks:
  - Track B PR #284 payload mutation until this promotion reaches trusted main
cross_repo_tasks: []
implementation_authorized: true
---

# Current game-login schema coordinator promotion

Independently audit and promote only the accepted sanitized facts from source Draft PR #711 onto current protected `main` without merging its research workflow/analyzer and without mutating Track B PR #284.

## Acceptance

- [x] Resolve current protected `main` and start from exact current main.
- [x] Resolve live source PR #711, exact head and changed-file inventory.
- [x] Independently re-download source artifact `9625060590`.
- [x] Re-hash ZIP and `result.json` and match GitHub/source identifiers.
- [x] Independently inspect current exact-client, serializer, nested-message and producer evidence.
- [x] Preserve unsupported password/session/AuthInfo user-facing semantics as `UNKNOWN`.
- [x] Keep source workflow/analyzer and Track B files out of promotion scope.
- [x] Open promotion PR #719 from exact current main and mark Ready after full docs-only diff review.
- [ ] Obtain exact-head repository checks/governance/review evidence required by current policy.
- [ ] Merge promotion to trusted `main` only if all merge gates pass.
- [ ] Close #711 unmerged as consumed/superseded and archive/release source lifecycle if repository convention remains unchanged.
- [ ] Re-resolve Track B #284 from post-promotion trusted main and consume only promoted facts.

## Independent audit result

```yaml
main_at_start: e621a1407d124a71dc9437912e1676aa8929cc11
source_pr: 711
source_live_head: 39e1f7343d8c3932356a78db1eae00147e810d7d
source_evidence_head: d24b6e61d1086094112020db6e7d959c24bdb34a
producer_run: 33017207072
producer_job: 98338388458
artifact: 9625060590
artifact_digest: sha256:be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
redownloaded_zip_sha256: be50b5baf632095f3eccc90aad6b0b9ff409d3dac626c8580b35deb36b245a74
result_json_sha256: 1940d58a7fcb2615da7f9d47179e6dbdf41397f89b8b522af52da75b076154dc
audit_result: PASS_BOUNDED
decision: ACCEPT_WITH_EDITS
material_findings_open: 0
source_changed_files: 7
source_review_threads: 0
source_submitted_reviews: 0
promotion_pr: 719
promotion_pr_ready: true
```

## Promoted boundary

Accepted only:

- current exact client fence `15.32.75d4a0 / d1a16819... / 52105824`;
- current generated message ABI slots needed to interpret captured serializers;
- exact `GameclientMessageLogin` wire field numbers/types/storage;
- field 7 nested `LoginRSAEncryptedBlock` identity;
- exact `LoginRSAEncryptedBlock` wire field numbers/types/storage;
- current `TLoginProtocolMessageHandler +0x60 -> 0xe25620` producer;
- retained source type `TAuthenticationAndEncryptionInfo`;
- structural rejection of Track B's legacy raw login body as matching the current typed native payload;
- prior trusted-main rejection of another generic outer-framing guess remains in force.

Withheld as `UNKNOWN`:

- password/session semantic field names;
- password/session-to-RSA field mapping;
- retained AuthInfo user-facing field names;
- causal explanation of Track B structured `0x14`.

## Current next action

Consume exact-head CI/governance/review for PR #719 and merge only if all repository gates pass. Do not alter Track B #284 before trusted-main promotion.
