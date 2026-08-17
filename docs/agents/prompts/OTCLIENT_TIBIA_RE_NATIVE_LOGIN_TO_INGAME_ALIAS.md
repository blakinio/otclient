# OTCLIENT-TIBIA-RE native login-to-ingame alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME
track_id: official-client-re
lane: RUNTIME
risk: critical
runtime_access: current_task_must_classify_before_live_work
owner_funded_ai_api_authorized: false
run_scope: single_task
continuation_policy: continue_within_task_until_success_or_real_stop
user_communication: low_noise
```

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME autonomicznie.
```

Resolve this alias through live repository state and load:

```text
AGENTS.md
docs/agents/AGENTS.md
docs/agents/PROMPTING_HANDOVER.md
docs/agents/PROMPTING_STANDARD.md
docs/agents/ANTI_STALL_AND_EXECUTION_BUDGET.md
docs/agents/TIBIA_RESEARCH_TRACKS.md
docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_NATIVE_LOGIN_TO_INGAME.md
```

Before any runtime operation, verify current `main`, active tasks, open PRs, current Track A runtime owner/admission/lease/registration/generation, and current state of PR #475/#498/#499. Do not inherit authority from this alias or from historical PR/task prose.

Objective: use native semantic control below the login UI to take the exact official native Linux Tibia client `15.32.df7b29` / `51965216` / SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe` through legal auth/session reuse or native credential auth, native character-model resolution, native character login and the complete game-login state machine until cross-layer causal proof shows the selected character is actually in active gameplay.

Do not use login-form OCR, image matching, blind coordinate clicking, GUI credential entry, auth bypass, TLS weakening, server-response spoofing, guessed C++ objects/ABI/thread affinity, or another task's runtime. Preserve credential safety and current serialized-session governance exactly as required by the full prompt and trusted-base contracts.

A login-success packet is not completion. Normal task success is only:

```text
RESULT: SUCCESS
CHARACTER_ACTUALLY_LOGGED_INTO_GAME: YES
CAUSAL_PROOF: COMPLETE
```

`ROTATE`, `WAITING`, `BLOCKED` and `EXTERNAL_ACTION_REQUIRED` remain valid worker-invocation outcomes when required by current anti-stall, authority or safety contracts; they must never be mislabeled as task DONE.
