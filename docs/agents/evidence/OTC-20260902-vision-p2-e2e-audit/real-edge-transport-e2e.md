# Real authenticated edge transport E2E

- observed: 2026-09-02T16:42:26+02:00
- fresh admitted capture: 6630 ms, geometry `810,263,1020,650`.
- masked PNG SHA-256: `ebbcca421d8e9a727af1143849547450b36e120e2f540cee0262de417125d97c`; size `2007` bytes.
- raw frame persisted: false; full-frame zero mask applied before persistence.
- post-capture PID/start/SHA/XID remained exact; physical action count `0`.
- Synology production `EdgeOutboundClient`: PASS; heartbeat/artifact/observation sequences `2/3/4`.
- Molehill peer is private; mutual HELLO authentication: PASS.
- `TrustedVisionP2Runtime.durable_edge_verifier`: PASS for HELLO and subsequent frames.
- signed descriptor + `receive_artifact_bytes`: PASS.
- production PNG decoder: `1020x650`, every pixel zero.
- authority-neutral `runtime: null` observation: `AgentEdgeBridge.accept` PASS.
- all temporary pairing/script/port/safe-PNG/runner-checkout material was deleted.

## Narrow remaining finding

A production-only probe imported no fixture contract. The exact read-only observation admitted successfully and `RuntimeSignalResolver(reviewed_contracts=())` constructed successfully. Composition authority issuance then failed closed as `EDGE_RUNTIME_COMPOSITION_MISMATCH`, because an empty reviewed-contract signature is not admissible. Repository search finds concrete `ReviewedRuntimeSignalContract(...)` instantiations only in tests.

Classification: real cross-host transport `PASS`; remaining blocker is admission/semantic-authority coupling before `reconcile_vision()`, not missing transport or deployment. Runtime access is released to `none`.
