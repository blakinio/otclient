---
task_id: OTC-20260829-tibia-re-vision-benchmark-execution
status: completed
agent: ChatGPT
session_role: coordinator
project_lane: otclient
lane: P0-DESIGN
track_id: official-client-re
task_kind: implementation
phase: archived
branch: main
base_branch: main
base_sha: f208a20cb4517e8b57bef91983337145d379267c
related_pr: 790
created: 2026-08-29T08:08:53+02:00
updated: 2026-08-29T09:06:00+02:00
completed: 2026-08-29T09:06:00+02:00
risk: high
execution_mode: local_owner_pc
run_scope: autonomous_program
policy_version: 2
runtime_access: none
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
owned_paths: []
---

# Terminal result

`TIBIA-RE-VISION-BENCHMARK` execution reached the declared safe terminal boundary:

```text
BENCHMARK_RESULT: PARTIAL
PRIMARY_MODEL: none
LEADING_PROFILE: qwen3-vl:4b-instruct-q4_K_M@sha256:ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
OCR_FALLBACK_MODEL: none
RESEARCH_VALUE_VERDICT: INCONCLUSIVE
TRACK_B_HELP: useful diagnostic sensor candidate; not the current unblocker
```

The representative Track B screenshot dataset did not exist. No identical official-service retry was performed merely to create screenshots, so P3-P7 project-specific selection/research-value measurement remains intentionally unclaimed.

# Verified implementation evidence

- Deterministic harness plus post-audit remediation: 34 focused tests PASS.
- Qwen bounded profile: 3/3 `LOGIN_SCREEN`, expected-text recall 1.0, black negative false text 0/3, false `IN_GAME_VISUAL` 0/3, all hard gates PASS, exact-model unload leaves residency empty.
- OvisOCR2 revision `1fc9221b7823a371d6e97f92d527cc847e24e107`: exact-text recall 1.0, but black no-text control fabricated text 3/3 under each of two prompt profiles; not promoted as fallback.
- Ovis2.5-2B revision `393c932b2a03e28eb9aaa503e3c4ab3ad384d958`: `UNSUPPORTED_BACKEND` on the verified Windows AMD exact-profile path; no cloud or undeclared substitute was used.
- Fresh independent audit of implementation head `7621916c76c19aa0951384538a8387c02cafcd04`: `PASS_BOUNDED`, seven findings remediated, zero material findings open.
- Exact final implementation head `db7f1d547bcaf7f2e6bdf4bc4c3c31654f26d065`: CI run `33239858690` SUCCESS; Track A governance run `33239858636` SUCCESS.
- PR #790 final hygiene: zero review submissions, zero review threads, zero conversation comments; squash-merged as `eeb6f76a8cd9602ab92599e21a57a016596fcf53`.

# Track B conclusion

At terminal evaluation PR #284 remained blocked on `BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE`. Vision cannot prove the native pre-login `GameclientMessage*` sequence, final queue/TCP serializer, packet field order, or server acceptance. It should be used only as additive `visual_only` / `structural_authority:false` evidence when a future materially changed Track B E2E independently becomes legal and can supply secret-safe pre/change/terminal keyframes.

Durable detailed report: `docs/agents/reports/OTCLIENT-20260829-tibia-re-vision-benchmark-execution.md`.
Independent audit: `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/20260829-independent-audit.md`.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-29T09:06:00+02:00
head: db7f1d547bcaf7f2e6bdf4bc4c3c31654f26d065
branch: main
pr: 790
status: completed
context_routes:
  - local-model-benchmark
  - official-client-research-design
  - track-b-read-only-coordination
owned_paths: []
proven:
  - benchmark terminal result is PARTIAL with primary_model null and ocr_fallback_model null
  - Qwen bounded exact profile passed synthetic state/OCR/negative-control hard gates and is the leading future representative candidate
  - OvisOCR2 is not promoted because black no-text hallucination reproduced 3 of 3 under both tested prompt profiles
  - Ovis2.5-2B is host/profile UNSUPPORTED_BACKEND and was not substituted
  - fresh independent audit PASS_BOUNDED with zero open material findings
  - exact final implementation head db7f1d547bcaf7f2e6bdf4bc4c3c31654f26d065 passed CI 33239858690 and Track A governance 33239858636
  - PR 790 merged as eeb6f76a8cd9602ab92599e21a57a016596fcf53 with zero review threads/comments
  - Track B representative screenshot handoff was unavailable and no E2E retry was triggered to manufacture it
derived:
  - Vision is a credible additive diagnostic sensor candidate for a future legal Track B run but is not the current structural unblocker
unknown:
  - representative real Track B state/OCR/delta accuracy
  - measured structural-only versus structural-plus-VisualEvidence reduction in hypotheses, E2Es or time
conflicts: []
first_failure:
  marker: REPRESENTATIVE_TRACK_B_SCREENSHOT_DATASET_UNAVAILABLE
  evidence: no accepted secret-safe Track B screenshot handoff existed while identical official-service retry remained forbidden
rejected_hypotheses:
  - synthetic smoke is sufficient to declare a formal winner
  - Vision can recover the current native pre-login outbound sequence
  - OvisOCR2 can be promoted despite repeated black-negative hallucination
changed_paths:
  - docs/agents/tasks/archive/OTC-20260829-tibia-re-vision-benchmark-execution.md
validation:
  - command: python -m unittest discover -s tools/tibia-re-vision-benchmark/tests -v
    result: PASS
    evidence: 34 focused tests passed on the final implementation line
  - command: fresh independent post-implementation audit
    result: PASS
    evidence: PASS_BOUNDED; material findings open 0
  - command: GitHub exact-final-head checks
    result: PASS
    evidence: CI 33239858690 SUCCESS; Track A governance 33239858636 SUCCESS on db7f1d547bcaf7f2e6bdf4bc4c3c31654f26d065
  - command: GitHub PR 790 review hygiene
    result: PASS
    evidence: zero review submissions, zero review threads and zero conversation comments before merge
blockers: []
next_action: merge this lifecycle archive PR after exact-head CI and review hygiene pass
```
