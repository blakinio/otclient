---
task_id: OTC-20260818-native-login-prompt-refresh-v3
status: completed
agent: null
session_id: null
session_role: released
project_lane: otclient
lane: DOCUMENTATION
track_id: official-client-re
task_kind: documentation
phase: closed
execution_mode: github_only
branch: docs/OTC-20260818-native-login-prompt-refresh-v3
base_branch: main
related_pr: 516
implementation_merge: be0d3fd5468e70e8d97b66b838cd14ba24c56c73
closed: 2026-08-18T11:27:00+02:00
risk: medium
runtime_access: none
RUNTIME_ACCESS: none
EXECUTION_CLASS: github_hosted
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
mutation_authorized: false
owned_paths: []
ownership_released: true
prompt_contract_version: 3.0.0
alias_prompt_contract_version: 1.2.0
---

# Terminal result

The canonical native-login prompt refresh is complete and promoted to `main` by PR #516.

Promoted surfaces:

```text
docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
  prompt_contract.version = 3.0.0

docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME_ALIAS.md
  alias_prompt_contract_version = 1.2.0
  canonical_prompt_contract_version = 3.0.0
```

The v3 prompt now incorporates current-main native authentication work and the released runtime handoff:

```text
#505 merge 17cc0dc1bf29c440cc08e443bdce98e4dde7be5d
  exact TGameClient cold-auth QMeta method 17 / static fence

#507 merge 2e6992da330e8a52d03b94b8d6a9de6fa79a6800
  opt-in one-shot form-less native auth bridge / SCM_RIGHTS

#510 merge 13c5939ef89900a0998d56d2bf625c3906c9a68e
  protected controlling-TTY -> sealed-memfd secret source

#475 released head 8bf26dde309c46f08be414c4d2aef3e3599d7f5a
  prior worker/runtime/session authority released; old authority is not inherited
```

The successor is explicitly routed toward fresh no-client Track A inventory/admission and physical E2E rather than further generic auth infrastructure.

# Preserved hard invariants

```text
exact official Linux client 15.32.df7b29 / 51965216 / e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
login-form OCR/image/coordinates/Tab/Return/blind input forbidden
unsafe credential env/argv/plaintext/log/screenshot/GDB-history ingress forbidden
native QMeta/Qt-thread/object/ABI/runtime fences required
historical 0xd47300 not a standalone character-login control entry
runtime-discovered character selection required
2FA/auth/TLS/server acceptance bypass forbidden
one-session serialization and fresh runtime admission required
login success is not IN_GAME
FullMap + >=10 map-description strips + active gameplay/local-player + character/world identity required
no generic bridge/static expansion unless a concrete physical failure proves one missing dependency
exact gpt-5.3-codex-spark standing exception preserved with secret/proprietary-binary exclusions
```

# Prompt evaluation and audit

Baseline: v2.0.0 from merged PR #501.

Final representative matrix:

```text
positive cases: 6/6 PASS
negative cases: 7/7 PASS
boundary cases: 6/6 PASS
total: 19/19 PASS
```

Fresh falsification found and repaired before promotion:

```text
PROMPT-V3-AUD-001 MEDIUM — first draft used non-normative continuation/task-completion values.
PROMPT-V3-AUD-002 MEDIUM — trust/context authority boundary was not explicit enough.
```

Final audit:

```text
result=PASS
open_material_findings=0
changed_paths=3 expected/3 actual
trust_boundary_explicit=true
prompting_standard_enums_aligned=true
programme_boundary_native_login_only=true
```

# Validation

Exact implementation head:

```text
de2b996f514a22490ade32351a3698c7fdde905d
```

Required checks on that exact head:

```text
Track A agent runtime governance
  run 32121261485 = SUCCESS

CI draft/final
  run 32121261701 = SUCCESS

CI ready-state generation
  run 32121340892 = SUCCESS
```

PR #516 auto-merged after the protected required-check generation completed.

Review threads at readiness: `0`.

E2E:

```text
result=NOT_APPLICABLE
reason=documentation-only prompt/alias task; no official-client runtime, credentials, login, gameplay or protected environment was operated. Physical native-login E2E remains required by the promoted prompt itself.
```

# Closeout

```yaml
closeout:
  implementation_complete: true
  vertical_slice_complete: true
  audit:
    result: PASS
    material_findings_open: 0
  e2e:
    result: NOT_APPLICABLE
    reason: documentation-only prompt/alias update
  final_ci:
    head: de2b996f514a22490ade32351a3698c7fdde905d
    result: PASS
  pull_requests:
    unresolved_review_threads: 0
    terminal_prs:
      - blakinio/otclient#516 merged as be0d3fd5468e70e8d97b66b838cd14ba24c56c73
  task_status: completed
  task_archived: true
  ownership_released: true
```

No runtime, secret, login/session, client-binary or gameplay authority is retained by this task.
