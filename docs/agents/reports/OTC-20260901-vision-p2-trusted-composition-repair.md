# OTC Vision P2 trusted composition repair report

## Final repository/static state

The coordinator completed the bounded Phase 2 trusted-composition integration without Codex after explicit owner authorization to continue through MCP. No Official Tibia, Synology or Kasm live observation or mutation was used; `runtime_access:none` and physical action budget/count `0/0` remained frozen throughout.

## Integrated result

PR #846 now combines the frozen capture-edge, control-bridge and edge-transport source semantics behind one application-owned composition boundary:

- reviewed runtime-authority configuration and reviewed capture policy are composition-owned, not caller/task/API/MCP/transport-selected;
- capture secret safety is recomputed from the persisted PNG bytes and pinned mask policy;
- raw edge observations cannot self-assert secret-safe capture;
- trusted capture is accepted only when its runtime binding matches the current admitted namespace/container/display/PID/start/XID/client version/size/SHA and current task/run;
- edge transport remains authority-neutral and cannot mint Track A/runtime/mutation authority;
- replay state is stored in the existing Control Center SQLite store and survives reconstruction;
- replay load, HMAC/replay verification and persisted ledger update execute in one existing SQLite `BEGIN IMMEDIATE` transaction domain.

## TDD and falsification evidence

The final independent coordinator review identified a concurrency hole in the first durable replay adapter: two reconstructed verifier objects could load the same old ledger before either persisted the advanced window.

A deterministic regression test was added in `test_vision_p2_trusted_replay_atomicity.py`. On `a09c054301770fab2588722970d3c183b6626dce` it failed exactly with `load=0` and `save=0` transaction depths. The minimal production repair on `062a5c173b3410ec8fc2e5efaaefa1c4e34d15d6` wrapped the whole load -> verify -> save path in the existing store transaction domain.

Exact code-generation validation for `062a5c173b3410ec8fc2e5efaaefa1c4e34d15d6`:

- Track A agent runtime governance `33598991421`: SUCCESS;
- Package A `33598991422`: SUCCESS;
- Package B `33598991441`: SUCCESS;
- CI `33598991677`: SUCCESS.

Package B included full Control Center regression, fresh falsification audit, browser/CLI E2E and Ruff/whitespace validation. The prior replay-atomicity RED became GREEN in that run.

## Safety conclusion

Repository/static Phase 2 trusted composition is safe-by-default and fail-closed. Missing reviewed composition configuration leaves Official-client access unavailable. Peer authentication, capture metadata and caller-created Python objects do not grant runtime or physical authority.

Frozen authority remains:

```yaml
runtime_access: none
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
```

## Closeout

The remaining merge gate is purely repository lifecycle: update catalogue/changelog/PR metadata, run exact-head CI/governance for that final closeout generation, verify full diff/change list and review hygiene, mark #846 ready and squash-merge. Live read-only runtime observation remains a separate later serialized programme gate.
