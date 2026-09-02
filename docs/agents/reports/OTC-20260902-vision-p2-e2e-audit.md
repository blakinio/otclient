# OTC-20260902 Vision P2 fresh E2E audit report

## Audit target

- Programme: `OTC-VISION-P2-READONLY`.
- Worker alias: `OTC-VISION-P2-E2E-AUDIT`.
- Trusted `main` at dispatch: `8441fc1cce1600033b505d68ebc5c0141b337394`.
- Accepted Wave 2 integration head under audit: `7d4bae503030a00a51fad409d46bc43a39ad2314`.
- Wave 2 PR: #856; coordinator classification review: `5087863607` = `ACCEPT` for repository/integration scope only.
- Wave 2 exact-head required CI: terminal with `CI / Required` success and no failed/pending/null check conclusions.

## Independence and authority

This task is a fresh falsification/audit lane. It is not authorized to repair implementation code. Static audit begins with `runtime_access:none`. Real official-client observation may occur only after fresh read-only admission and exact target/runtime identity proof under the trusted Track A contracts.

Frozen authority remains: no credentials, login, relogin, character selection, gameplay, GUI input, anti-idle input, process control, process-memory access, packet/payload capture, mutation, or physical action. Physical action budget/count remain `0/0`.

## Required attacks

Attempt to falsify at minimum:

- exact target/client uniqueness and currentness fences;
- stale capture or runtime evidence becoming current;
- model/OCR content forging provenance, semantic state, or authority;
- secret-bearing capture reaching persistence/model/evidence;
- wrong peer or replayed transport evidence becoming current;
- restart/reconnect restoring stale authority;
- foreign/multiple model residency or parallel inference;
- `WORLD_VISUAL` promoting semantic in-game state without stronger reviewed runtime proof;
- nonzero physical action budget or a bound production executor;
- any forbidden input/login/process/memory/network behavior;
- misleading task/PR/ownership lifecycle.

## Evidence status

- Coordinator deterministic pre-audit: `COMPLETE` on a fresh checkout stacked exactly from `7d4bae503...`.
- Security/provenance subset: `184/184 PASS`.
- Broad Control Center discovery: `569 tests`, `5 errors`, `2 skipped`; all five errors reproduce identically on clean `main@8441fc1...`, so they are not Wave 2 regressions.
- Fresh independent model audit: `DEFERRED` until the physical E2E evidence exists, to avoid consuming the constrained Codex quota twice.
- Fresh runtime preflight: `PASS` for host/container/display reachability, but `NO_TARGET` for the official client: no `client` PID, no Tibia/client window, no client candidate in any running container, and canonical registration is absent.
- Fresh read-only admission: `BLOCKED` because there is no exact official-client target to admit.
- Real admitted read-only E2E: `BLOCKED` by target absence; this Phase 2 audit is not authorized to launch/bootstrap the client.
- Material Wave 2 finding from deterministic pre-audit: `NONE`.
- Direct Codex worker/reviewer invocations for Wave 3 so far: `0`.

## Completion rule

`PASS` requires exact-head evidence, fresh independent audit with zero open material findings, a real admitted read-only E2E on the canonical official-client runtime, physical action count `0`, no forbidden side effects, and truthful lifecycle state. Hosted/fake evidence cannot substitute for the physical read-only E2E.


## Deterministic pre-audit notes

The fresh checkout merge-base with the accepted Wave 2 generation is exactly `7d4bae503030a00a51fad409d46bc43a39ad2314`. Before this checkpoint, only the Wave 3 task/report existed above that generation.

The five broad-suite errors are outside Wave 2 changed paths and reproduce individually on clean `main@8441fc1cce1600033b505d68ebc5c0141b337394`: four Windows-local API connection resets and one vision test ending in `MODEL_INFERENCE_FAILED`. They are retained as baseline/environment evidence and are not silently counted as passing.

The required runtime contract was read from trusted base before physical observation. The authorized `Synology` device is now online. Non-invasive preflight proved `otclient-track-a-kasmvnc` running and `DISPLAY=:1` reachable at `1024x768`, but no Tibia/client window or `client` process exists; an all-running-container candidate scan found none and the canonical runtime registration is absent. No screenshot, admission, model inference, input, login, credential access, process control, memory access, packet capture, or mutation was attempted.


## Owner-authorized runtime setup and new fence blocker

At the owner's explicit instruction, the coordinator (outside the Wave 3 auditor authority) created `/home/kasm-user/Desktop/Tibia.desktop` and started the official Tibia launcher without login, credential access, character selection or gameplay input. The launcher updated the installed official Linux package to `15.32.be4f48`.

A fresh exact-target recheck then observed exactly one live `client` process: PID `28379`, executable `/home/kasm-user/.local/share/CipSoft GmbH/Tibia/packages/Tibia/bin/client`, size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`, display `:1.0`, with a visible Tibia window.

This does **not** satisfy current trusted-base admission. `TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md` still fences the official client to `15.32.75d4a0`, size `52105824`, SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`. The audit therefore fails closed and keeps `runtime_access:none`; no screenshot/model inference or E2E observation is admitted. A separately reviewed trusted-base client-fence advance is required.

Direct Codex usage remains `0`.
## Refreshed generation restack ? supersedes earlier blockers

Trusted `main` is now `c16d180d336ba8aa9e1656807c79a44e81c15c66` after reviewed client-fence PR #858. Refreshed Wave 2 integration head `a746dbfaa60a129fc3fa2f91e1b1e48038837a4a` has coordinator ACCEPT review `5089081225` and fully terminal green associated CI. Wave 3 was therefore restacked from its superseded `7d4bae503...` generation onto `a746dbfaa...`; the merge produced no textual conflicts.

A fresh static security/provenance matrix on the restacked tree passes **184/184** and the trusted current-client fence test passes. The only governance precheck failure was task-schema compatibility: this Wave 3 task still lacked the ten explicit admission fields introduced by #858. They are now persisted as `NOT_APPLICABLE` while `runtime_access:none` remains in force.

The earlier `client fence mismatch` section above is historical and no longer current. The trusted fence now matches `15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`. No historical PID/window observation is reused as current admission evidence. The next step is a fresh non-invasive Synology target proof, followed by explicit `read_only` admission only if ownership/namespace/uniqueness all prove clean.

Direct Codex usage remains `0`; Wave 3 physical action count remains `0`.
## Audit-only stacked PR representation

After the clean restack commit, `git diff a746dbfaa...3c8f4f04a` contains exactly three Wave 3-owned paths: the audit task, report and `static-preaudit.md`. Running the actual Package A boundary against a main-based stacked diff produced a RED consisting only of five documentation paths (the two inherited Wave 2 docs plus the three Wave 3 docs); no implementation path violated the boundary.

Wave 3 is explicitly `implementation_authorized:false`, so it will not modify Package A workflow to whitelist itself. PR #857 is instead retargeted onto the accepted Wave 2 branch, making the GitHub PR diff match the task's real ownership and dependency. This is representation/lifecycle correction, not a safety-gate bypass; physical E2E still requires fresh Track A `read_only` admission.
## Fresh read-only admission ? current generation

After the audit-only PR retarget, a fresh non-invasive Synology preflight proved the current physical target rather than reusing historical PID/window evidence. `otclient-track-a-kasmvnc` and display `:1` are current; exactly one `client` process exists across all running containers. PID `28379` / start ticks `36180734` / display `:1.0` maps to the official package `15.32.be4f48`, size `52105824`, SHA-256 `552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`, with a PID-bound top-level `Tibia` window. Canonical registration is absent.

The audit therefore persists `runtime_access:read_only`, `runtime_owner_task:OTC-20260902-vision-p2-e2e-audit`, explicit target namespace, `target_uniqueness:PROVEN`, all canonical control gates `NOT_APPLICABLE`, and `mutation_authorized:false`. This grants observation only. Screenshot/model inference remains forbidden until this admission record is durably committed/pushed.


## Physical capture and real-Qwen material finding ? 2026-09-02T14:46:03+02:00

A fresh `read_only` admission on exact live client PID `28379` / start `36180734` / XID `0x01e00017` enabled one physical production capture. `KasmX11FfmpegFrameSource` completed in `9003 ms`; the client identity remained stable. A conservative full-frame mask zeroed pixels before persistence, so no raw frame was retained. The validated masked artifact is `capture:ebbcca421d8e9a727af1143849547450b36e120e2f540cee0262de417125d97c`; model-bound source/acquisition monotonic values are `369728093658595` / `369734002783431`. Physical action count remained `0`.

Molehill's owner-approved model supervisor exposed Ollama `0.32.14`, zero resident models and the exact Qwen3-VL digest `ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b`. The production `AgentVisionSensor` consumed a byte-identical reconstruction of the masked physical artifact and failed closed as `MODEL_INFERENCE_FAILED`. ROCm logged a rocBLASLt `TensileLibrary_lazy_gfx1201.dat` load failure despite that file existing and being readable. One bounded switch to the bundled Vulkan library successfully loaded the model and decoded all three image batches, but the production sensor still failed. A direct unchanged provider diagnostic then exposed the real contract failure: `ValueError` with invalid/missing strict model-observation fields for keys, `screen_class`, `visible_text`, `ui_objects`, `appeared`, `disappeared`, and `changed`.

This is a **material Wave 3 finding** in the production vision provider/prompt contract. The auditor is `implementation_authorized:false`, so it does not patch `agent_vision.py`. The local model host was restored to its pre-run state: Ollama API down, zero Ollama/llama-server processes, no task PID files. Runtime access is released back to `none`; a post-repair rerun must re-admit from fresh physical evidence. No Codex was used.
