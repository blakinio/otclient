---
task_id: OTC-20260902-vision-p2-e2e-audit
status: waiting
agent: ChatGPT
session_role: phase2_auditor
worker_alias: OTC-VISION-P2-E2E-AUDIT
programme_id: OTC-VISION-P2-READONLY
project_lane: otclient
lane: RUNTIME_INFRA
track_id: official-client-re
task_kind: audit
phase: wave_3_fresh_audit_e2e
branch: test/OTC-20260902-vision-p2-e2e-audit
base_branch: feat/OTC-20260902-vision-p2-vision-reconciliation
base_main: c16d180d336ba8aa9e1656807c79a44e81c15c66
audited_integration_head: a746dbfaa60a129fc3fa2f91e1b1e48038837a4a
created: 2026-09-02T11:28:36+02:00
updated_at: 2026-09-02T13:51:00+02:00
risk: high
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: true
  frontend_required: false
  integration_required: true
  e2e_required: true
execution_class: hybrid
execution_mode: github_plus_remote_read_only
execution_reason: perform static falsification and deterministic checks without owner-funded AI, then use only freshly admitted canonical read-only runtime observation for the required physical E2E
context_pressure: medium
context_growth: stable
context_score: 7
estimate_confidence: medium
decomposition_decision: single
decomposition_reason: one independent audit owns the exact accepted integration generation and its real read-only E2E evidence
continuation_policy: continue_until_real_stop
task_completion_policy: return_to_coordinator_for_classification
policy_version: 2
implementation_authorized: false
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
persistent_session_role: none
physical_e2e_required: true
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
anti_idle_input_authorized: false
process_control_authorized: false
network_payload_capture_allowed: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
owner_funded_ai_api_authorized: false
worktree: Molehill-PC:C:\Users\barte\AppData\Local\Temp\otclient-vision-p2-e2e-audit-pr857
owned_paths:
  - docs/agents/tasks/active/OTC-20260902-vision-p2-e2e-audit.md
  - docs/agents/reports/OTC-20260902-vision-p2-e2e-audit.md
  - docs/agents/evidence/OTC-20260902-vision-p2-e2e-audit/**
modules_touched: []
depends_on:
  - PR #856 exact accepted head a746dbfaa60a129fc3fa2f91e1b1e48038837a4a
  - coordinator refreshed classification review #5089081225 ACCEPT for Wave 2 repository/integration scope
blocks:
  - Phase 2 completion and merge of PR #856
current_blocker: material_finding_agent_vision_real_qwen_schema_failure
next_action: dispatch a separate bounded agent-vision provider-schema repair from trusted main; after repair promotion restack Wave 2 and Wave 3, freshly re-admit read_only, and rerun the physical E2E without reusing stale runtime or model evidence
invocation_started_at: 2026-09-02T11:28:36+02:00
last_progress_at: 2026-09-02T14:46:03+02:00
ci_checks_for_current_head: 0
ci_check_generation: refreshed_wave3_read_only_admission
terminal_ci_wait_started_at: null
terminal_ci_checks_for_current_generation: 0
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 0
context_reconstruction_attempts: 0
stall_warnings: 0
---

# OTC-VISION-P2-E2E-AUDIT

## Mission

Act as the fresh independent validator for Phase 2 and try to falsify the accepted Vision P2 integration on exact head `a746dbfaa60a129fc3fa2f91e1b1e48038837a4a`. Do not trust the Wave 2 worker narrative as evidence and do not become the implementation worker.

## Binding authority

- `AGENTS.md`
- `docs/agents/AGENTS.md`
- `docs/agents/DELIVERY_COMPLETENESS_AND_CLOSEOUT.md`
- `docs/agents/EXECUTION_PROTOCOL.md`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`
- `docs/agents/contracts/TRACK_A_KASMVNC_RUNTIME_ACCESS_V1.md`
- `docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md`
- `docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md`
- `docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md`
- `docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md`
- `docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md`
- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`

## Audit attacks

Attempt to disprove at minimum:

- exact target/client fence and uniqueness can be bypassed;
- a stale screenshot/runtime signal can be accepted as current;
- model/OCR payload can forge provenance, authority, or semantic state;
- secret-bearing capture can reach persistence/model/evidence;
- wrong peer/replayed transport evidence can become current;
- disconnect/reconnect/restart silently resumes or reuses stale state;
- foreign or multiple model residency is tolerated, evicted unsafely, or parallel inference occurs;
- `WORLD_VISUAL` can promote semantic in-game state without stronger reviewed runtime proof;
- Control Center can obtain nonzero physical budget or a bound executor in Phase 2;
- any GUI input, anti-idle, login, credential, process-memory, process-control, or network-payload behavior occurs;
- related Draft PRs, task state, or ownership become misleading.

## Runtime rule

Static audit starts with `runtime_access:none`. Before any physical observation, freshly prove the designated Synology container/display/window/client identity and satisfy the current read-only runtime-admission contract. A reachable desktop, visible window, historical PID/SHA, or existing authenticated session is discovery evidence only. Never send input or access credentials.

## Completion rule

A clean result requires exact-head evidence, zero open material findings, a real freshly admitted read-only E2E on the canonical official-client runtime, physical action count `0`, no forbidden side effect, and truthful lifecycle state. Hosted/fake tests cannot satisfy the physical E2E requirement.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-09-02T12:46:03Z
head: 89720d634f58761849a15b3a323044c535ca1f61
branch: test/OTC-20260902-vision-p2-e2e-audit
pr: 857
status: waiting
context_routes:
  - docs/agents/programs/OTC_VISION_P2_READONLY_COORDINATION_V1.md
  - docs/agents/prompts/OTC_20260901_VISION_P2_READONLY_MULTIAGENT.md
  - tools/tibia_re_control_center/agent_vision.py
  - tools/tibia_re_control_center/vision_p2_trusted_composition.py
owned_paths:
  - docs/agents/tasks/active/OTC-20260902-vision-p2-e2e-audit.md
  - docs/agents/reports/OTC-20260902-vision-p2-e2e-audit.md
  - docs/agents/evidence/OTC-20260902-vision-p2-e2e-audit/**
proven:
  - trusted main is c16d180d336ba8aa9e1656807c79a44e81c15c66 and refreshed accepted Wave 2 is a746dbfaa60a129fc3fa2f91e1b1e48038837a4a
  - refreshed static security and provenance subset passes 184 of 184 and current-client fence passes
  - a fresh durable read_only admission was pushed at 89720d634f58761849a15b3a323044c535ca1f61 after exact singleton PID 28379 start 36180734 XID 0x01e00017 version size SHA and all-container uniqueness proof
  - physical production KasmX11FfmpegFrameSource capture completed in 9003 ms with stable identity and zero physical actions
  - full-frame deterministic masking occurred before persistence; raw frame was not persisted and validated capture SHA is ebbcca421d8e9a727af1143849547450b36e120e2f540cee0262de417125d97c
  - model-bound physical capture source_monotonic_ns is 369728093658595 and acquisition_completed_ns is 369734002783431 with the same masked SHA
  - Molehill owner-approved supervisor exposed Ollama 0.32.14 with zero resident models and exact Qwen digest ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
  - production AgentVisionSensor on byte-identical masked physical evidence failed closed as MODEL_INFERENCE_FAILED while residency returned to empty
  - ROCm log showed rocBLASLt TensileLibrary_lazy_gfx1201.dat load failure even though the file exists and is readable
  - one bounded bundled Vulkan retry loaded and decoded all three image batches but production sensor still failed closed
  - direct unchanged provider diagnostic on Vulkan identified ValueError with seven missing or invalid strict model-observation schema fields
  - after diagnostics Molehill was restored to Ollama API down zero ollama or llama-server processes and no task PID files
  - no real reviewed causal runtime producer is currently promoted by the accepted runtime-signals slice; semantic world confirmation therefore remains unavailable without separate evidence
  - no deployed Vision P2 edge peer process was observed on Synology; only repository transport primitives are currently present
  - physical action count remains zero and no GUI input login credentials character selection gameplay memory access or packet capture occurred
  - direct Codex worker or reviewer usage remains zero
derived:
  - the physical capture/currentness path is operational and not the material blocker
  - the production local-model provider contract is a material Wave 3 finding because exact Qwen does not satisfy AgentVisionSensor strict observation schema on real physical masked evidence
  - Wave 3 implementation_authorized false requires returning this finding to a separate repair lane instead of editing agent_vision.py here
  - runtime_access is released back to none while waiting; every later physical rerun requires a fresh admission and cannot reuse PID/time/model evidence from this run
unknown:
  - exact minimal agent-vision prompt/schema repair and its real-model result
  - full post-repair physical capture to Qwen to edge/runtime-signal to reconciliation result
  - fresh independent final audit result after complete physical E2E evidence exists
conflicts:
  - none
first_failure:
  marker: exact Qwen production sensor cannot produce valid strict VisualEvidence on real masked physical capture
  evidence: AgentVisionSensor returned MODEL_INFERENCE_FAILED; direct same-provider diagnostic returned ValueError listing invalid observation keys screen_class visible_text ui_objects appeared disappeared and changed
rejected_hypotheses:
  - client currentness or capture latency is the failure: exact identity stayed stable and physical capture passed in 9003 ms
  - model digest or residency mismatch is the failure: pre-inference residency was empty and exact digest matched
  - ROCm alone explains the production failure: bundled Vulkan decoded the image too but the strict provider contract still failed
  - auditor should patch the sensor inline: rejected by implementation_authorized false and programme material-finding routing
changed_paths:
  - docs/agents/tasks/active/OTC-20260902-vision-p2-e2e-audit.md
  - docs/agents/reports/OTC-20260902-vision-p2-e2e-audit.md
  - docs/agents/evidence/OTC-20260902-vision-p2-e2e-audit/live-qwen-schema-finding.md
validation:
  - command: physical production capture via KasmX11FfmpegFrameSource and trusted capture composition
    result: PASS
    evidence: stable exact identity; 9003 ms capture; full-frame pre-persist mask; secret_safe true; raw frame not persisted; action count zero
  - command: production AgentVisionSensor with exact Qwen digest on byte-identical physical masked artifact
    result: FAIL
    evidence: MODEL_INFERENCE_FAILED with resident models empty after failure
  - command: one bundled Vulkan backend retry plus direct unchanged provider diagnostic
    result: FAIL
    evidence: image decoded 3 of 3 batches; direct provider returned seven strict observation schema validation errors; residency returned empty
  - command: post-diagnostic model-host restoration
    result: PASS
    evidence: Ollama API down; zero ollama or llama-server processes; task PID files absent
blockers:
  - material agent-vision real-provider schema failure requires a separate bounded repair and revalidation before Wave 3 can resume physical E2E
next_action: dispatch a separate bounded agent-vision provider-schema repair from trusted main; after promotion restack and freshly re-admit read_only before any further physical E2E
```
