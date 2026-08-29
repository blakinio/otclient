# TIBIA RE Vision Benchmark ? 2026-08-29 Execution Result

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
```

The programme reached a valid `PARTIAL` result. Real local models were executed, but no formal winner is declared because the representative secret-safe Track B/Tibia screenshot dataset required for selection-quality P3-P7 evaluation is not available.

## FACT ? execution boundary

- Host: `MOLEHILL-PC`, Windows, Ryzen 7 9800X3D, 64 GiB RAM, Radeon RX 9070 XT; Vulkan dedicated heap observed as 17,095,983,104 bytes.
- Local inference: Ollama `0.32.14` and a local Transformers CPU environment. Docker Model Runner `1.2.5` was used only for backend-capability inspection.
- No Synology/official-client runtime, credentials, login, GUI/gameplay input, process attach/control, packet capture, cloud inference or owner-funded API was used.
- Model output stays `visual_only: true` and `structural_authority: false`; trusted capture/model/authority metadata is added by the harness, not authored by the model.
- Inference was sequential and the final Ollama/Docker Model Runner resident sets were empty.

## FACT ? deterministic harness

The repository harness under `tools/tibia-re-vision-benchmark/` validates strict `VisualEvidence`, hard-gate precedence, fixed weighted-score mechanics, one-model admission, loopback-only Ollama transport, exact installed-model digest, capture-byte SHA binding, secret-safe manifest admission, strict model JSON, and deterministic OCR normalization.

The frozen inputs are:

- `synthetic-login-smoke.png`: `2dea29719c3e6f7c84c40717ead27bd56cfaacb69b06c4f19f0975b231bc47a6`;
- `black-negative.png`: `c2885cde31402fef5a8f5d15ae4aef757a2053f5a7acb77e1d61d034693016c2`.

Both are explicitly `selection_quality: false`. The original drawing helper was removed during closeout because two fresh regenerations were mutually identical but produced SHA `cc485d0af96acc4a6d464783819477194c8604267871baa1303855ed0041a782`, not the already-scored frozen input. The committed bytes plus manifest SHA are therefore the immutable test inputs; no model result was rebound to a regenerated image.

## FACT ? Qwen3-VL leading profile

```yaml
model_id: Qwen/Qwen3-VL-4B-Instruct
ollama_name: qwen3-vl:4b-instruct-q4_K_M
digest_sha256: ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b
format: gguf
quantization: Q4_K_M
num_ctx: 4096
num_predict: 256
temperature: 0
```

The final post-audit-remediation real run verified the installed digest before inference, bound each manifest SHA to the actual image bytes, executed three login plus three black-negative trials, and released the exact owned model through the local Ollama API:

| Metric | Result |
|---|---:|
| schema-valid requests | 6/6 |
| login `LOGIN_SCREEN` | 3/3 |
| expected text recall | 1.0 |
| black negative false text | 0/3 |
| black negative false `IN_GAME_VISUAL` | 0/3 |
| hard gates | PASS |
| cold total | 5.098 s |
| cold load | 3.705 s |
| warm API p50 | 0.782 s |
| warm API p95 | 1.120 s |
| final model residency | empty |

A prior bounded resource observation on the same exact digest/profile recorded context `4096`, resident/VRAM size `3,527,545,978` bytes and `100% GPU`. An earlier unbounded diagnostic had loaded context `262144`, about 44 GB residency and CPU/GPU spill; those performance numbers were rejected and the harness now pins the bounded context/output profile.

Qwen is the leading profile for the next representative benchmark, not a formal `primary_model` selection.

## FACT ? OvisOCR2

Exact revision: `ATH-MaaS/OvisOCR2@1fc9221b7823a371d6e97f92d527cc847e24e107`, tested locally through a fingerprinted Transformers CPU profile.

Across two prompt profiles, each repeated three times:

- expected synthetic-login text recall: `1.0`;
- solid-black no-text control produced fabricated non-empty text: `3/3` under each prompt profile;
- recommended-profile p50: about `17.42 s`;
- peak process RSS: about `2.296 GB`.

The normalization layer preserved the fabricated strings instead of repairing them. Because Qwen matched the positive text result while passing the same negative control, the measured evidence does not justify the model-switch cost or hallucination risk of an OvisOCR2 fallback. `ocr_fallback_model` remains `null`.

## FACT ? Ovis2.5-2B

Exact revision: `ATH-MaaS/Ovis2.5-2B@393c932b2a03e28eb9aaa503e3c4ab3ad384d958`.

Current-host result: `UNSUPPORTED_BACKEND` for the declared profile. Docker Model Runner exposes this candidate as `vllm`; local DMR reports vLLM unavailable on the Windows runner, and the verified AMD host has no NVIDIA CUDA path. No Ovis2.5 inference was performed and no third-party GGUF/cloud/different model was substituted. This is a host/profile classification, not a general claim about the model.

## FACT ? Track B boundary

Live PR #284 head was revalidated as `62383aded3acbeb5f405a12fe1f93849cd8e35f9`. Its current terminal blocker remains:

```text
BLOCKED_REQUIRED_CURRENT_NATIVE_PRE_LOGIN_OUTBOUND_SEQUENCE_EVIDENCE
```

Track B must recover exact-current static causality for native `GameclientMessage*` sends around first game-server connect / `sendLogin`. Its current evidence explicitly forbids another identical official-service E2E until a promoted material outbound delta exists.

Cross-track comment `5460730478` requests that the next independently legal, materially changed E2E expose secret-safe pre-attempt, first-visible-change, and terminal keyframes with non-secret order/timestamp and hashes. At evaluation time there is no later accepted handoff and no repo-owned Track B evidence screenshot/keyframe dataset. No E2E was triggered merely to manufacture images.

## UNKNOWN ? representative P3-P7 evidence

Missing evidence is exactly:

- real secret-safe Track B/Tibia screen-state, OCR and before/after delta cases;
- causal correlation between those frames and the structural/network markers;
- A/B comparison of structural-only versus structural+VisualEvidence hypothesis ranking;
- measured reduction in false hypotheses, bounded experiments/E2Es, steps or time to a valid protocol candidate.

Therefore `research_value_verdict` remains `INCONCLUSIVE`, and a selection weighted score is not computed.

## INFERENCE ? project value

Confidence: medium. The bounded Qwen profile is technically suitable as an additive local diagnostic sensor. On the executed controls it is stable, fast after load, avoids the tested no-text hallucination and cannot author authority/provenance fields. In a future legal Track B E2E it can classify visible state, extract terminal visible errors and correlate visible UI deltas with non-secret structural timing.

It cannot recover or prove the missing native outbound message sequence, packet fields, final queue/TCP writer, server acceptance or world entry. It therefore does not remove Track B's current blocker and Track B should continue static native outbound-sequence research without waiting for Vision.

## Recommendation

Continue `OTCLIENT-TIBIA-GLOBAL-LOGIN-FINAL-CONTINUE` on the current structural blocker. When that lane independently earns its next materially changed E2E, capture the three secret-safe keyframes requested by comment `5460730478` in the same run and evaluate the bounded Qwen profile first. Only a representative frozen dataset plus P7 A/B measurement can promote `WINNER`, `ROLE_SPLIT`, or a positive research-value verdict.

## Durable evidence

- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-synthetic-suite-final.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-synthetic-suite.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/qwen3-vl-unbounded-context-diagnostic.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovisocr2-cpu-smoke.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovisocr2-cpu-recommended-prompt-smoke.json`
- `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/ovis-backend-compatibility.json`

## Closeout state

Implementation and real-model evidence are complete at the `PARTIAL` benchmark boundary. Fresh independent audit of implementation head `7621916c76c19aa0951384538a8387c02cafcd04` is `PASS_BOUNDED` with zero open material findings; the audit record is `docs/agents/evidence/OTC-20260829-tibia-re-vision-benchmark-execution/20260829-independent-audit.md`. Final exact-head GitHub CI/governance, review hygiene, merge and task archival remain before repository closeout.
