# OTCLIENT ? TIBIA RE local vision benchmark execution

## Decision

```yaml
benchmark_result: PARTIAL
primary_model: null
leading_profile: ollama:qwen3-vl:4b-instruct-q4_K_M@sha256:ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
ocr_fallback_model: null
research_value_verdict: INCONCLUSIVE
track_b_help_verdict: USEFUL_DIAGNOSTIC_SENSOR_CANDIDATE_NOT_CURRENT_UNBLOCKER
current_track_b_blocker: BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE
selection_weighted_score: NOT_COMPUTED
selection_weighted_score_reason: representative selection-quality Tibia/Track-B dataset is unavailable and the first-pass candidate set is not fully executable on one comparable local backend
```

The programme reached a valid `PARTIAL` terminal decision. The deterministic harness and local model profiles were exercised, but the benchmark deliberately does **not** declare a winner from synthetic smoke data.

## FACT ? execution boundary

- Execution host: `MOLEHILL-PC`, Windows, Ryzen 7 9800X3D, 64 GiB RAM, Radeon RX 9070 XT with 17,095,983,104-byte Vulkan dedicated heap.
- Local model service: Ollama `0.32.14`; Docker Model Runner `1.2.5` was used only for backend-capability inspection.
- No Synology, official-client runtime, account credential, 2FA, auth/session secret, login, GUI input, gameplay, process attach/control, packet capture or network mutation was used by this task.
- Model output is normalized as `visual_only: true` and `structural_authority: false`. Capture hash, model identity and authority fields are supplied by the trusted harness, not by the model.
- Local inference was sequential. Final `ollama ps` and `docker model ps` were empty after explicit unload.

## FACT ? deterministic harness

The task added a Python-stdlib benchmark harness under `tools/tibia-re-vision-benchmark/` with strict schema validation, hard gates, weighted-score mechanics, single-model residency admission, loopback-only Ollama transport, strict JSON refusal, secret-input rejection and deterministic OCR normalization.

Focused suite: **22/22 PASS**. The tests include false `IN_GAME_VISUAL` rejection on login screens, model-authored authority/provenance rejection, cloud/non-loopback endpoint rejection, residency conflicts and preservation of OCR hallucinations rather than heuristic repair.

Frozen smoke inputs:

- `synthetic-login-smoke.png` SHA-256 `2dea29719c3e6f7c84c40717ead27bd56cfaacb69b06c4f19f0975b231bc47a6` ? generated, secret-safe login-like UI with five known visible strings;
- `black-negative.png` SHA-256 `c2885cde31402fef5a8f5d15ae4aef757a2053f5a7acb77e1d61d034693016c2` ? generated solid-black no-text control.

Both fixtures are `selection_quality: false`; they validate the harness/profile only.

## FACT ? Qwen3-VL bounded profile

Exact profile:

```yaml
model_id: Qwen/Qwen3-VL-4B-Instruct
ollama_name: qwen3-vl:4b-instruct-q4_K_M
digest_sha256: ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
format: gguf
architecture: qwen3vl
parameter_size: 4.4B
quantization: Q4_K_M
num_ctx: 4096
num_predict: 256
temperature: 0
resident_size_bytes: 3527545978
resident_vram_bytes: 3527545978
processor: 100_percent_GPU
```

Bounded synthetic suite, three login trials plus three black-negative trials:

| Metric | Result |
|---|---:|
| schema-valid requests | 6/6 |
| login classification `LOGIN_SCREEN` | 3/3 |
| expected visible-text recall | 1.0 |
| black negative non-empty text | 0/3 |
| black negative false `IN_GAME_VISUAL` | 0/3 |
| hard gates | PASS |
| cold total | 5.269 s |
| cold load | 3.855 s |
| warm API p50 | 0.800 s |
| warm API p95 (interpolated, small sample) | 1.144 s |
| final residency after explicit unload | empty |

A preceding diagnostic run did not bind Ollama context size and exposed context `262144`, approximately `44 GB` residency and CPU/GPU spill. Its performance numbers were rejected. TDD then required explicit `num_ctx=4096` and `num_predict=256`, and the clean bounded suite above supersedes that diagnostic for performance use.

**FACT:** this is the strongest local first-pass profile measured by this task. **It is not a formal winner**, because the tested images are synthetic and the programme's representative Tibia dataset is absent.

## FACT ? OvisOCR2 CPU profile

Exact model revision: `ATH-MaaS/OvisOCR2@1fc9221b7823a371d6e97f92d527cc847e24e107`.

The model ran locally through a fingerprinted Transformers CPU environment. Under both the benchmark-safe prompt and the model-card-recommended OCR prompt:

- expected login text recall: **1.0** across 3/3 login trials;
- black no-text control produced fabricated non-empty text: **3/3** trials;
- the same negative-control failure reproduced under both prompt profiles;
- recommended-profile median latency: about **17.42 s** on CPU;
- peak process RSS: about **2.296 GB**.

The normalization layer preserved those fabricated strings in evidence; it did not clean or repair them.

**FACT:** OvisOCR2 is locally executable and strong on the tested exact-text positive case, but fails the tested hallucination-resistance negative control repeatedly. Therefore `ocr_fallback_model` remains `null` rather than promoting it as an unqualified fallback.

## FACT ? Ovis2.5-2B current-host compatibility

Exact revision: `ATH-MaaS/Ovis2.5-2B@393c932b2a03e28eb9aaa503e3c4ab3ad384d958`.

Current-host result: `UNSUPPORTED_BACKEND` for the declared exact profile. No Ovis2.5 inference was performed.

Local Docker Model Runner classified the candidate as `vllm`; DMR `1.2.5` reported vLLM unavailable on the current Windows setup, while the verified host GPU is AMD rather than an NVIDIA CUDA device. The model-card quick profile also targets CUDA/FlashAttention. The task did not substitute a third-party GGUF, cloud endpoint or different model merely to force a comparison.

This result is **host/backend-specific**, not a claim that Ovis2.5 is generally unusable.

## FACT ? Track B live state at terminal evaluation

Revalidated live PR #284 head: `62383aded3acbeb5f405a12fe1f93849cd8e35f9`.

Its newest terminal checkpoint still states:

```text
BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE
```

The current requirement is exact-current static causality for all native `GameclientMessage*` sends around first game-server connect / `sendLogin` before login success. It explicitly forbids another identical official-service E2E until a promoted material outbound delta exists.

Cross-track request `PR #284 comment 5460730478` asks the next independently legal, materially changed Track B E2E to expose secret-safe:

1. pre-attempt keyframe;
2. first visible-state-change keyframe, if any;
3. terminal error/success keyframe;

with non-secret ordering/timestamp and content hash, while quarantining any credential/session-bearing frame.

At terminal evaluation there is no later handoff comment and no repo-owned Track B screenshot/keyframe dataset. A branch tree/search found static product assets, but no Track B evidence image suitable for this benchmark. No E2E was triggered merely to manufacture screenshots.

## UNKNOWN ? project-specific P3-P7 measurements

The following cannot be measured yet:

- representative `LOGIN_SCREEN / CHARACTER_SELECT / WORLD / WORLD_EXIT` accuracy on the actual Track B container;
- exact OCR accuracy for the real terminal rejection/popup;
- before/after visible-delta accuracy for a real evidence-derived login mutation;
- causal timestamp correlation between VisualEvidence and the structural/network markers already recorded by Track B;
- A/B comparison of structural-only versus structural+VisualEvidence hypothesis ranking;
- reduction in hypotheses, bounded E2Es, or time-to-valid-protocol-candidate.

The programme requires representative frozen Tibia evidence for a selection-quality winner. Synthetic smoke cannot legally fill this gap.

## INFERENCE ? will Vision help `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE`?

**Confidence: medium.** The measured Qwen profile is technically suitable as a local visual sensor: it produced stable schema-valid state/OCR output, passed the tested no-text negative control and runs warm in under roughly one second on the verified GPU profile. That makes it a credible candidate to add useful *diagnostic* evidence once real secret-safe frames are available.

Its plausible value is narrow and concrete:

- distinguish no visible transition from an actual login/character/world/error transition;
- extract visible fixed error/popup text without making it wire truth;
- describe appeared/disappeared/changed UI between pre/post keyframes;
- correlate visible effects with non-secret Track B timing/order markers;
- help rank which already-structurally-legal hypothesis should be investigated next.

No measured evidence yet shows how many hypotheses or E2Es this saves, so the formal research-value verdict remains `INCONCLUSIVE`.

## FACT ? what Vision cannot unblock

Vision cannot recover or prove:

- the native pre-login `GameclientMessage*` outbound sequence;
- the final queue/TCP serializer;
- packet field order/types/widths;
- the correct missing protocol delta;
- successful official-service authentication or world entry.

Therefore it does **not** remove Track B's current blocker and Track B should not wait for Vision before continuing the native outbound-sequence research lane.

## RECOMMENDATION

1. Continue `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` on its current structural blocker; do not add another service E2E for Vision.
2. When Track B independently earns the next materially changed E2E, satisfy comment `5460730478` in the same run and hand off only accepted secret-safe pre/change/terminal keyframes.
3. Evaluate the bounded Qwen profile first on those frozen frames. Keep its output additive and non-authoritative.
4. Do not promote OvisOCR2 as fallback unless a future Tibia-specific negative-control suite proves its hallucination behavior acceptable under a revised exact profile.
5. Reconsider Ovis2.5 only if a supported local AMD/Linux backend profile is explicitly proven; do not substitute a different third-party model under the same benchmark identity.
6. Declare a formal winner/role split only after the representative frozen dataset and P7 A/B research-value measurement exist. `NO_WINNER` remains acceptable.

## Durable evidence

- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-4b-instruct-smoke.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-unbounded-context-diagnostic.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-synthetic-suite.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovisocr2-cpu-smoke.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovisocr2-cpu-recommended-prompt-smoke.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovis-backend-compatibility.json`
- `docs/agents/tasks/active/OTC-20260829-tibia-re-vision-benchmark-execution.md`
- `docs/superpowers/plans/2026-08-29-tibia-re-vision-benchmark-execution.md`

## Closeout boundary

Implementation and evidence production for this invocation are complete at the `PARTIAL` benchmark boundary. P3-P7 Track B representative evaluation is not silently converted to PASS; it is deferred to a future task/invocation after an accepted screenshot handoff exists. PR #790 still requires the repository-mandated fresh independent post-implementation audit and exact-final-head checks before merge/archive.

## FACT — Qwen3-VL bounded profile

Exact profile:

```text
model: qwen3-vl:4b-instruct-q4_K_M
digest: ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
format: GGUF
quantization: Q4_K_M
num_ctx: 4096
num_predict: 256
temperature: 0
```

On the frozen synthetic login fixture plus solid-black negative control, three trials per case produced:

- login classification `LOGIN_SCREEN`: 3/3;
- expected visible-text recall: 1.0;
- black negative-control false text: 0/3;
- black negative-control false `IN_GAME_VISUAL`: 0/3;
- strict schema/hard gates: PASS;
- cold API total: 5.2685395 s; cold load: 3.8546923 s;
- warm API p50: 0.7998541 s; p95: 1.14383672 s;
- resident size and VRAM: 3,527,545,978 bytes;
- observed residency context: 4096;
- processor: 100% GPU;
- explicit unload: PASS; final Ollama and Docker Model Runner residency empty.

An earlier warm diagnostic left the model at its unbounded default context 262144, which produced about 44 GB residency and CPU/GPU spill. That profile is rejected for performance comparison. The harness now explicitly bounds `num_ctx=4096` and `num_predict=256`; the clean bounded rerun above supersedes the diagnostic performance numbers.

Primary evidence:

```text
docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-synthetic-suite.json
docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-unbounded-context-diagnostic.json
```

## FACT — OvisOCR2

Exact profile tested locally:

```text
model: ATH-MaaS/OvisOCR2
revision: 1fc9221b7823a371d6e97f92d527cc847e24e107
backend: Transformers CPU
python: 3.12.0
torch: 2.13.0+cpu
transformers: 5.16.1
dtype: bfloat16
```

Across two prompt profiles, each repeated three times, OvisOCR2 found all five expected strings on the synthetic login fixture. In both prompt profiles it also produced non-empty fabricated prompt-like text on the solid-black no-text control in 3/3 trials.

Recommended-prompt profile metrics:

- text recall: 1.0;
- black false-text count: 3/3;
- p50 latency: 17.4179759 s;
- peak process RSS: 2,295,803,904 bytes.

Because Qwen already achieved the same synthetic text recall while passing the no-text negative control, the current evidence does not justify the model-switch cost or hallucination risk of an OvisOCR2 fallback.

Primary evidence:

```text
docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovisocr2-cpu-smoke.json
docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovisocr2-cpu-recommended-prompt-smoke.json
```

## FACT — Ovis2.5-2B

Current revision `393c932b2a03e28eb9aaa503e3c4ab3ad384d958` could not enter real inference on the verified host through its exact advertised local profile. Docker Model Runner identifies the model as `vllm`; local Docker Model Runner v1.2.5 reports `vllm: Not Installed — only supported on Linux`, while the verified owner host is Windows with AMD Radeon RX 9070 XT and no NVIDIA CUDA path.

A prior unrelated scratch `AttributeError` is not used as proof. The terminal classification is `UNSUPPORTED_BACKEND` for this exact host/profile, not a claim that Ovis2.5-2B is globally unsupported.

Primary evidence:

```text
docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovis-backend-compatibility.json
```

## FACT — Track B integration boundary

Current Track B PR #284 head is `62383aded3acbeb5f405a12fe1f93849cd8e35f9`. Its durable next action remains `BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE`: recover the exact-current native `GameclientMessage*` sequence around the first game-server connect / `sendLogin`; no further official-service game E2E is allowed until a material outbound delta is promoted.

The current 41-file PR inventory contains no screenshot/keyframe/image handoff. Cross-track comment `5460730478` records the required future visual contract: secret-safe pre-attempt, first visible-state-change, and terminal keyframes with non-secret order/timestamp and hashes, without triggering an identical retry.

Therefore no real Track B frame entered local inference in this task.

## INFERENCE — usefulness for OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE

Vision is technically viable as an additive diagnostic sensor, but its incremental research value for the current login blocker is not yet measured. The bounded Qwen profile is fast enough to classify a small keyframe set locally and, on the tested controls, did not invent text or promote a false in-game state.

The most plausible value is after a future materially justified Track B E2E: correlate structural markers/packet timing with visible client state, extract the terminal visible error, and distinguish “no visible transition”, “popup/error appeared”, or “world/character screen changed”. This can rank hypotheses and reduce manual screenshot inspection.

Vision cannot prove the missing native pre-login outbound message sequence, packet fields, final queue/TCP writer, or server acceptance. It therefore cannot remove the current Track B blocker by itself.

## Hard-gate status

```yaml
schema_valid_output: PASS
secret_leakage_or_persistence: PASS
false_in_game_on_tested_login_or_negative_controls: PASS_FOR_QWEN_TESTED_CASES
model_runtime_or_action_authority: PASS
model_authored_executable_action_parameters: PASS
single_model_residency: PASS
silent_cloud_provider_fallback: PASS
required_provenance: PASS
```

These gates apply only to the evidence actually executed. They do not upgrade synthetic fixtures into representative selection evidence.

## Missing evidence and effect

Exactly missing for a `WINNER` or `ROLE_SPLIT` decision:

- accepted secret-safe real Linux Tibia/Track B keyframes with provenance;
- representative screen-state / error / UI-delta cases, not only synthetic smoke;
- A/B comparison of the same Track B structural evidence with and without normalized VisualEvidence;
- measured change in correct hypothesis ranking, false hypotheses, bounded experiments, or steps/time to the valid candidate.

Without those inputs, `research_value_verdict` is `INCONCLUSIVE` and `primary_model`/`ocr_fallback_model` remain null by contract.

## Recommendation

Keep the bounded Qwen profile and harness available for the next materially justified Track B E2E. Do not delay current static native pre-login outbound-sequence research waiting for Vision. When Track B can legally run its next changed E2E, capture the three secret-safe keyframes requested in comment `5460730478` and rerun the representative benchmark; that is the first point where Vision can be judged on actual project acceleration rather than technical feasibility.
