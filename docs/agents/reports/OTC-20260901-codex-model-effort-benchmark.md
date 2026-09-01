# Codex model × reasoning-effort benchmark

## Scope

This report persists an empirical benchmark of the available Codex worker families `Luna`, `Terra`, and `Sol` under the repository's existing model/effort routing policy.

The benchmark used one frozen, safety-heavy real task: Draft PR #827 (`OTC-VISION-P2-CAPTURE-EDGE`) at exact head `53b6a7e515c0cd6820857f7910368cdbb0e1978d`.

The goal was not to declare a universal model winner. It was to measure whether raising reasoning effort on smaller models materially changes finding quality and whether that trade is cheaper than selecting a stronger model at lower effort.

## Frozen benchmark conditions

All compared runs used the same:

- repository: `blakinio/otclient`;
- PR: `#827`;
- exact head: `53b6a7e515c0cd6820857f7910368cdbb0e1978d`;
- frozen base snapshot: `main@fb0c489f2ed166e872c4f197c6a78375a8576685`;
- role: `auditor`;
- primary changed files: `4`;
- context budget: maximum `5` primary files;
- verified GitHub snapshot captured at `2026-09-01T19:28:07.614737Z`;
- snapshot CI: run `33546190410` SUCCESS;
- snapshot Track A governance: run `33546190253` SUCCESS;
- unresolved review threads: `0`;
- no runtime, credentials, login, GUI input, gameplay, process control, or mutation authority.

The later effort runs deliberately reused the original verified snapshot rather than refreshing PR metadata, so model/effort was the intended independent variable. Before those runs the exact PR head and clean worker state were revalidated.

## Results

| Model | Effort | Session | Tokens | Time (s) | Confirmed code findings | Notes |
| --- | --- | --- | ---: | ---: | ---: | --- |
| Luna | medium | `01a05e72-e50f-7b51-a5cb-57835f87eb76` | 55,832 | 60.586 | 1/3 | found caller-constructible reviewed policy boundary |
| Luna | high | `01a05e90-b6d1-7441-b20b-9f78ee1e2343` | 70,595 | 153.242 | 1/3 | found forgeable `CaptureEvidence`; higher cost without broader recall |
| Luna | xhigh | `01a05e93-57bb-78b2-9699-0f92f1b35404` | 118,931 | 272.649 | 3/3 | full confirmed code-bug recall plus real base-metadata inconsistency |
| Terra | medium | `01a05e73-fb1f-73e1-8a65-f81be423cc51` | 28,893 | 33.451 | 0/3 | cheapest; focused on lifecycle/checkpoint hygiene |
| Terra | high | `01a05e97-b93b-78f2-b0f2-07fad9b35fd6` | 57,039 | 59.864 | 1/3 | found reviewed-policy trust gap; also emitted one false local-dirty claim |
| Terra | xhigh | `01a05e99-14b9-7d90-8c25-b682105c9711` | 69,124 | 120.038 | 1/3 | no confirmed code-recall gain over Terra/high |
| Sol | medium | `01a05e74-ae95-7492-9b87-9b07dec6da1c` | 56,921 | 81.234 | 2/3 | found forgeable evidence and post-capture timestamp freshness flaw |

All seven runs returned `AUDIT_FAIL`. Dispatcher postflight confirmed the audited worker worktree was clean after every run.

## Ground-truth adjudication

Three code-level findings were mechanically reproduced after the model runs rather than accepted from model prose alone.

1. **Reviewed policy authority is caller-constructible.** A caller can instantiate `ReviewedSecretMaskPolicy` with an arbitrary non-empty region. The class validates shape/geometry but does not itself establish that the region set came from an authoritative reviewed registry/factory.
2. **`CaptureEvidence` is directly forgeable.** A manually constructed `CaptureEvidence(secret_safe=True, ...)` with matching artifact hash and runtime binding can pass `validated_vision_capture()` and become a `SecretSafeCapture` without proving that `CaptureEdge` or the reviewed mask policy produced it.
3. **Capture freshness can be timestamped too late.** `source_monotonic_ns` is assigned after RGB acquisition, preprocessing and post-capture binding/geometry checks. A sufficiently slow capture path can therefore make older pixels appear newer to the downstream freshness calculation.

The adjudication script produced the markers `LUNA_POLICY_PUBLIC_CONSTRUCTION=PASS`, `SOL_FORGED_EVIDENCE_ACCEPTED=PASS`, and `SOL_POST_CAPTURE_TIMESTAMP_ACCEPTED=PASS`.

A separate lifecycle inconsistency was also confirmed: task `base_main` had advanced to `fb0c489f...` while older `depends_on` / dispatch `BASE_MAIN` text still referenced `0fe1ecb...`. This is real durable-metadata hygiene, but it is distinct from the three code-safety findings above.

Terra/medium's exact-head checkpoint concern was not promoted to a code blocker because the verified parent snapshot proved CI/governance on current PR head `53b6a7e5...`; the task intentionally records an implementation content head before later checkpoint/documentation commits. Terra/high's statement that task/report files were locally uncommitted was a false positive: dispatcher preflight and postflight both reported `clean=True`.

## Quality / cost observations

Confirmed code findings per 100k tokens:

- Sol/medium: `3.51`;
- Luna/xhigh: `2.52`;
- Luna/medium: `1.79`;
- Terra/high: `1.75`;
- Terra/xhigh: `1.45`;
- Luna/high: `1.42`;
- Terra/medium: `0` on this safety-heavy target.

Increasing effort was not monotonic. Luna/high cost 26.4% more tokens than Luna/medium without increasing total confirmed recall. Luna/xhigh did reach 3/3, but used 113.0% more tokens than Luna/medium and took 272.649 seconds. Terra/high materially improved over Terra/medium, while Terra/xhigh used 21.2% more tokens than Terra/high and doubled wall time without increasing confirmed code recall.

Sol/medium was the strongest single-run quality/token point on this benchmark: 56,921 tokens for 2/3 confirmed code findings. Luna/xhigh achieved the highest single-run recall, but at more than twice the token cost and more than three times the wall time of Sol/medium.

A two-model independent review was especially competitive: `Sol/medium + Luna/medium` jointly covered all 3/3 confirmed code findings using 112,753 tokens and about 141.8 seconds sequentially, less than Luna/xhigh's 118,931 tokens and 272.649 seconds while also providing independent model-family diversity.

## Provisional routing guidance

This is one safety-heavy benchmark, so the following is empirical tie-breaking guidance, not a universal replacement for the existing smallest-sufficient-model policy.

- narrow docs/status/lifecycle work: Luna low/medium or Terra/medium;
- ordinary implementation/debugging: Terra/medium, escalating to Terra/high when complexity or evidence justifies it;
- safety/security/provenance/secret-boundary review: prefer Sol/medium over merely increasing Terra effort;
- high-confidence safety review: consider independent `Sol/medium + Luna/medium` before a single very expensive Luna/xhigh pass;
- Luna/xhigh can be useful when one worker must maximize recall, but it is exceptional because of token/time cost;
- this benchmark gives no evidence that Terra/xhigh should be a default route; Terra/high achieved the same confirmed code recall more cheaply;
- this benchmark gives no evidence that Luna/high should replace Luna/medium by default; its extra effort did not improve total confirmed recall here;
- Sol/high/xhigh remain escalation routes for unresolved hard cases; this benchmark did not test them.

Do not infer a global ordering such as `Sol > Luna > Terra` from this one target. Future benchmarks should include ordinary implementation, debugging, integration and low-risk documentation tasks and should aggregate medians rather than replacing policy from one run.

## Durable evidence

Machine-readable results and adjudication are stored at:

`docs/agents/evidence/OTC-20260901-codex-model-effort-benchmark/results.json`

Raw local Codex traces were intentionally not committed because they contain large repeated governance/source dumps. The durable record retains exact model, effort, session IDs, token counts, wall times, frozen GitHub identifiers, final findings and adjudication outcomes needed to reproduce or compare the benchmark.
