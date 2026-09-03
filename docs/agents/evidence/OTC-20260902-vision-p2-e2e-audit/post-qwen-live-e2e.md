# Post-Qwen physical E2E evidence

## Fresh capture

- exact admitted official client remained singleton and fence-matched before and after capture;
- production Kasm capture duration: `8733 ms`;
- geometry: `810,263,1020,650`;
- source/acquisition monotonic ns: `372661727635814` / `372669258682289`;
- full-frame zero mask was applied before persistence;
- capture SHA-256: `ebbcca421d8e9a727af1143849547450b36e120e2f540cee0262de417125d97c`;
- raw frame persisted: false; physical action count: `0`.

## Repaired exact-Qwen sensor

- Ollama `0.32.14`, exact Qwen digest, serialized single-model Vulkan backend;
- residency before/after inference: empty;
- model input bytes matched the fresh masked physical capture SHA;
- production `AgentVisionSensor`: PASS;
- screen class: `UNKNOWN`; visible-text count: `0`;
- model profile / evidence ref / capture SHA bindings: all match;
- `visual_only=true`; `structural_authority=false`;
- cleanup restored API down, zero model processes, no task PID file.

Classification: Qwen repair `PHYSICALLY_REVALIDATED_PASS`.

## Corrected remaining Phase 2 gate

The earlier `BLOCKED_REAL_DEPLOYMENT_MISSING` wording was too broad and is superseded by this section.

Facts retained from inventory:

- no Vision P2 edge process happened to be running on Synology or Molehill during the inventory;
- `agent_edge_transport.py` already provides the production outbound authenticated client/channel and accepts private/local destinations;
- the trusted composition already provides verifier/bridge/reconciliation consumers;
- no reviewed-causal runtime producer is currently promoted.

Those facts do **not** imply that Phase 2 needs a persistent edge daemon or a new runtime-signal producer. Phase 2 requires the actual read-only edge path to be exercised end-to-end. A one-shot receiver/control-side harness using the existing production verifier/bridge is sufficient if it receives a real outbound Synology edge connection and real observation/artifact traffic. Stronger reviewed runtime evidence is required only for semantic promotion such as `IN_GAME`; if unavailable, reconciliation may legitimately remain `UNKNOWN`.

Correct classification: `BLOCKED_REAL_EDGE_TRANSPORT_E2E_NOT_EXERCISED`.

At the correction checkpoint Molehill-PC's execution endpoint is offline, so the cross-host one-shot receiver cannot be started from the current session. This is an availability gate, not evidence that a new subsystem must be implemented. When Molehill is available, the next physical run must freshly re-admit `read_only`, exercise the real authenticated Synology -> Molehill edge path, and then reconcile with current available evidence. Physical action count remains `0`.