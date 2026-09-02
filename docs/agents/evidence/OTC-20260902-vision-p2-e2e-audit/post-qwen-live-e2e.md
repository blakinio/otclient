# Post-Qwen physical E2E evidence

## Fresh capture

- admitted official client remained exact and singleton before capture.
- production Kasm capture duration: `8733 ms`.
- geometry: `810,263,1020,650`.
- source monotonic ns: `372661727635814`.
- acquisition completed ns: `372669258682289`.
- secret policy: `secret-mask:9591b3883823c2fa580e633a8f294065de809a5b61ba5b32d73b6ddf4b24de2d`.
- mask mode: full-frame zero before persistence.
- capture SHA-256: `ebbcca421d8e9a727af1143849547450b36e120e2f540cee0262de417125d97c`.
- secret-safe: true; black: true; blank: true.
- persisted masked PNG count during capture: 1; raw frame persisted: false.
- post-capture PID/start/client-SHA/XID and all-container candidate count remained exact; physical action count: `0`.

## Repaired exact-Qwen sensor

- local model host precondition: API down and zero model processes.
- Ollama version: `0.32.14`; bundled backend: Vulkan; serialized single-model configuration.
- residency before inference: empty.
- exact Qwen digest: match.
- reconstructed model input: byte-identical to fresh physical masked capture SHA.
- production `AgentVisionSensor`: PASS.
- screen class: `UNKNOWN`.
- visible text count: `0` (text values not persisted).
- model profile / evidence ref / capture SHA bindings: all match.
- `visual_only=true`; `structural_authority=false`.
- residency after inference: empty.
- cleanup: API down, zero model processes, task PID file absent.

## Full composition blocker

- fresh Synology edge-process match groups in Kasm/runner: `0`; host edge-named processes: none.
- fresh Molehill edge-process matches after excluding the diagnostic process: `0`.
- production edge module: outbound client/channel only; no production listener/daemon entrypoint.
- test listeners are local test-thread fixtures only.
- production runtime-signal contract/sample/source/config instantiations outside resolver implementation: none.
- accepted runtime-signals ruling: no production `REVIEWED_CAUSAL` producer is promoted.

Classification: Qwen repair `PHYSICALLY_REVALIDATED_PASS`; full trusted edge/runtime-signal/reconciliation physical E2E `BLOCKED_REAL_DEPLOYMENT_MISSING`. No synthetic edge/runtime authority was created. Runtime access is released to `none`; physical action count remains `0`.
