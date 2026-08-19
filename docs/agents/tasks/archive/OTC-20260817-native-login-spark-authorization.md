---
task_id: OTC-20260817-native-login-spark-authorization
status: completed
session_role: released
project_lane: otclient
lane: DOCUMENTATION
track_id: official-client-re
task_kind: documentation
phase: closed
implementation_pr: 503
implementation_head: 1c571264caddaaa0491c77f64aa7b495b3c7d4e3
implementation_merge_commit: bd167a8a9b4192b3c87c21423e2af37e897f5e79
original_lifecycle_pr: 504
original_lifecycle_head: 42836648d05dd48f8b139f915dcec2d81d330158
original_lifecycle_disposition: close_unmerged_superseded_by_current_main_closeout
original_lifecycle_ci_run: 32070630285
original_lifecycle_ci_result: SUCCESS
original_lifecycle_governance_run: 32070612181
original_lifecycle_governance_result: SUCCESS
implementation_exact_head_ci_run: 32070457742
implementation_exact_head_ci_result: SUCCESS
implementation_exact_head_governance_run: 32070457472
implementation_exact_head_governance_result: SUCCESS
manual_prompt_policy_eval: PASS_7_OF_7
fresh_content_falsification: PASS
material_findings_open: 0
direct_codex_spark_authorized: true
direct_codex_spark_model: gpt-5.3-codex-spark
owner_funded_ai_api_authorized: false
alias_prompt_contract_version: 1.1.0
runtime_access: none
runtime_owner_task: NOT_APPLICABLE
runtime_namespace: NOT_APPLICABLE
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
physical_e2e_required: false
ownership_released: true
---

# Native-login Spark authorization — terminal archive

## Terminal disposition

The bounded documentation/governance task is complete and ownership is released.

Implementation PR #503 squash-merged as:

```text
bd167a8a9b4192b3c87c21423e2af37e897f5e79
```

That merge made the authorization durable in repository instructions and the native-login alias. Historical lifecycle PR #504 correctly prepared the corresponding archive/release state and had green CI/governance, but it was never merged and became stale in Git ancestry. The current closeout therefore archives the task from trusted current `main` rather than merging the old lifecycle branch.

## Authorization boundary

Authorized only for the exact `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` alias/task family:

```text
DIRECT_CODEX_SPARK_AUTHORIZED=true
MODEL=gpt-5.3-codex-spark
OPENAI_API_AUTHORIZED=false
OTHER_MODELS_OR_PROVIDERS_AUTHORIZED=false
```

The exception permits bounded repository/code analysis, reverse-engineering assistance, implementation assistance, falsification and review for that exact task family.

It does **not** authorize:

- owner-funded OpenAI API usage or `OPENAI_API_KEY` export;
- a different model/provider;
- passing Tibia account credentials, session/auth secrets or secret-bearing captures to the model;
- passing raw proprietary official-client binaries to the model;
- runtime admission, login, mutation, promotion or completion authority merely because Spark use is allowed.

Runtime and credential authority always remains governed by the separately applicable task/admission rules.

## Historical validation

Implementation exact-head validation:

```text
manual prompt-policy eval              PASS 7/7
fresh content falsification            PASS
material findings open                 0
CI                                     32070457742 = SUCCESS
Track A governance                     32070457472 = SUCCESS
implementation merge                   bd167a8a9b4192b3c87c21423e2af37e897f5e79
```

Original lifecycle #504 exact head `42836648d05dd48f8b139f915dcec2d81d330158` also passed:

```text
CI                                     32070630285 = SUCCESS
Track A governance                     32070612181 = SUCCESS
```

The lifecycle delay does not change the authorization semantics already merged through #503; this closeout only removes stale active-task state and records terminal ownership release.

## Safety

This lifecycle work is documentation-only with `runtime_access:none`. No official-client execution, login, credentials, GUI input, gameplay, transaction, process-memory access or runtime mutation occurs.
