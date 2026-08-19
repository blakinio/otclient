# TIBIA-RE-AUTH-SESSION — source exact-head validation

```yaml
source_pr: 556
source_head: 411d0e287d08406c682ef063fb3f3f61341d9295
current_main_at_coordinator_start: e4357137e47836d67eb19ceb13a8e313f69bf778
changed_files: 3
review_threads_open: 0
runtime_access: none
```

The coordinator independently re-fetched live PR metadata and exact-head checks.

## Source changed paths

```text
.github/workflows/track-a-auth-session-current-build-static.yml
docs/agents/evidence/OTC-20260819-track-a-auth-session-current-build-static/current-build-static-result.md
docs/agents/tasks/active/OTC-20260819-track-a-auth-session-current-build-static.md
```

No Track B, shared coverage-matrix, physical runtime, credential, client package, or unrelated product-code path is in the source diff.

## Exact-head checks

On source head `411d0e287d08406c682ef063fb3f3f61341d9295`:

```text
Track A current-build auth session static discriminator 32229840214 = SUCCESS
Track A agent runtime governance                         32229840231 = SUCCESS
CI                                                       32229840436 = SUCCESS
review threads                                           0
```

## Ancestry / promotion consequence

Against coordinator-start `main@e4357137e47836d67eb19ceb13a8e313f69bf778`, the source branch is:

```text
ahead_by: 7
behind_by: 9
merge_base: 82e5f435c3aa4172115bf7f6a0cd7a5cc6da3d50
```

Therefore the researcher history is not promoted directly. Any accepted result must use a clean current-main promotion branch; changing task text such as `base_main` cannot substitute for actual Git ancestry freshness.

## Current-fence correction

The source task was written while #555 was still described as an independent Draft. Current trusted `main` already contains #555 merge `2e572789a2bc4b64c5e906c4515c15c625f6bc9e` and #561 closeout. The exact package identity used by #556 matches that canonical fence, but stale lifecycle wording must be corrected during promotion.
