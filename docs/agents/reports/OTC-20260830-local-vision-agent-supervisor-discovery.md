# OTC-20260830 local vision-agent supervisor discovery

## Purpose

Preserve the current discovery state before any architectural or runtime change. The owner wants to reuse local vision/OCR to accelerate official-client research and ultimately allow a bounded local agent to navigate login/character-select/world transitions, verify outcomes and collect research samples while remaining observable and chat-controllable.

This report is discovery evidence only. It does not authorize implementation, official-client observation, credentials, login, GUI input, process control, gameplay or semantic promotion.

## Trusted repository state

Discovery was reconciled against `main` at `18ff83053f5c5d85c9bce6debab0f7fef6b79ecd`, the squash merge of PR #801 (`feat(track-a): add Kasm canonical bootstrap`). Current Track A admission and KasmVNC contracts still require explicit task authority and the applicable Gate A/Gate B/bootstrap/recovery boundaries before any live input/login action.

## Existing Tibia vision evidence

Merged PR #790 executed `TIBIA-RE-VISION-BENCHMARK` on Molehill-PC. Terminal benchmark result remained `PARTIAL`, with no formally promoted `PRIMARY_MODEL`, because representative Track B screenshots were unavailable and synthetic smoke could not be extrapolated into project-specific production authority.

The leading tested local profile was:

```text
qwen3-vl:4b-instruct-q4_K_M
sha256: ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
```

Verified bounded smoke evidence from PR #790:

- login classification: `3/3`;
- expected-text recall: `1.0`;
- solid-black no-text false text: `0/3`;
- false `IN_GAME_VISUAL`: `0/3`;
- all benchmark hard gates: PASS;
- final local-model residency: empty.

OvisOCR2 exact revision `1fc9221...` achieved text recall `1.0` but fabricated non-empty text on the solid-black negative control `3/3` in both tested prompt profiles. It was correctly not promoted as an OCR fallback. Ovis2.5-2B remained unsupported on the tested Windows/AMD backend profile.

Conclusion: Qwen3-VL is already the best evidenced local vision/OCR sensor candidate for the next representative Tibia dataset. OCR/vision must remain `visual_only` evidence and must not independently create `IN_GAME` or other structural authority.

## Existing local supervisor stack

The owner already has a local stack under:

```text
C:/Users/barte/Documents/ChatGPT/llm/supervisor
```

Observed reusable components:

- `supervisor.ps1` lifecycle wrapper;
- local Ollama runtime under `runtime/Ollama`;
- `mcp/local_worker_server.py` plus tests and README;
- `policies/LOCAL_MODEL_ROUTING.yaml`;
- `policies/SECURITY_POLICY.md`;
- benchmark/evidence directories, model state and isolated worktrees;
- pinned Hermes Agent image integration and fixed Ollama proxy design.

`local_worker_server.py --self-test` returned `local_worker_server self-test passed`. The MCP server is already registered in the local Codex configuration as `mcp_servers.local_workers` and currently exposes bounded low-risk delegation/file/capability tools.

Current local-worker routing makes `gemma4:12b` the default bounded code/text worker. The separate `qwen3.5:9b` text/review fallback remains disabled after its prior benchmark produced false-positive review findings. That policy finding does not invalidate the separately benchmarked `qwen3-vl:4b-instruct-q4_K_M` Tibia vision profile.

## Local models observed

Ollama client/runtime version observed: `0.32.14`.

Installed models included:

```text
qwen3-vl:4b-instruct-q4_K_M  4.4B Q4_K_M  completion,vision,tools
qwen3.5:9b                   9.7B Q4_K_M  completion,vision,tools,thinking
gemma4:12b                   11.9B Q4_K_M completion,vision,audio,tools,thinking
qwen2.5-coder:14b            14.8B Q4_K_M completion,tools,insert
gpt-oss:20b                  20.9B MXFP4  completion,tools,thinking
muse-glimmer:latest          27.9B Q4_K_M completion,vision,tools,thinking
```

No model was resident at the final check. The repository's mandatory single-local-model residency policy remains applicable: actual model inference must be serialized and a model switch requires unload plus residency revalidation.

## Docker / Hermes state after Docker Desktop start

Fresh local readback after the owner started Docker Desktop:

```text
Docker Server=29.6.1 Client=29.6.1
Ollama API ready=true
OllamaVersion=0.32.14
DockerReady=true
FixedProxyReady=false
```

The pinned Hermes image is already local:

```text
nousresearch/hermes-agent@sha256:abd7ccd3ef5eeadc4d56c6fac054cd0b2e1dc5ec7e69fe0d1938dda5c180d456
```

The internal network `muse-supervisor-internal` already exists. The `muse-ollama-proxy` container also exists but was `Exited (255)` at discovery time. Therefore `supervisor doctor` currently fails only because the fixed Ollama proxy is not running. No `supervisor start` or proxy restart was performed in this discovery task.

## Computer-use state

The local Codex configuration contains `mcp_servers.cua_repl`, pointing at the installed OpenAI desktop/Codex application, but it is explicitly:

```text
enabled = false
```

This is a candidate computer-use layer only. It was not enabled or tested. Future design must decide whether to reuse CUA or implement a narrower X11/Kasm-specific executor.

## Reuse recommendation for the future design

Do not build a second local-agent platform from scratch. The architecture should preferentially reuse:

1. existing supervisor lifecycle and single-model residency controls;
2. existing MCP local-worker channel for bounded supervisor-to-local-model delegation;
3. PR #790 vision harness semantics and Qwen3-VL profile for image/OCR classification;
4. PR #801 canonical Kasm/bootstrap infrastructure for the physical runtime;
5. existing Kasm read-only `ffmpeg x11grab` capture path;
6. either the disabled CUA layer or a narrower exact-action X11 executor after security comparison;
7. a new thin session/dashboard/chat layer for owner visibility and two-way communication.

The local agent should not be allowed to infer authority from model output. Proposed future control flow is `capture -> local vision classification -> deterministic policy/state machine -> narrowly authorized action -> independent runtime confirmation -> evidence bundle`. Runtime signals remain stronger than OCR for semantic state claims.

## Architecture decisions still open

The following are intentionally not decided by this report:

- CUA versus narrow X11 action executor;
- credential handoff mechanism for autonomous login;
- exact allowed action vocabulary and budgets;
- dashboard transport/authentication;
- owner/supervisor message precedence and pause/stop semantics;
- evidence retention and screenshot redaction policy;
- whether the local agent may autonomously repeat login/world-entry cycles and how many;
- which runtime signals must confirm each OCR-derived screen classification.

These questions require an explicit architectural design and owner approval before implementation.

## Current boundary

```text
runtime_access=none
implementation_authorized=false
login_allowed=false
gui_input_authorized=false
process_control_authorized=false
physical_action_count=0
```

No official Tibia client runtime was touched by this discovery. No OCR inference was newly run against the official client, no GUI input was sent, no credentials were accessed and no supervisor/Hermes proxy state was changed.
