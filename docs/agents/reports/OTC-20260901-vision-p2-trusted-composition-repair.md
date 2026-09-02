# OTC Vision P2 trusted composition repair report

## Final repository/static state

The bounded Phase 2 trusted-composition integration is complete and merged. No Official Tibia, Synology or Kasm live observation or mutation was used; `runtime_access:none` and physical action budget/count `0/0` remained frozen throughout.

## Integrated result

Merged replacement PR #854 combines the frozen capture-edge, control-bridge and edge-transport source semantics behind one application-owned composition boundary:

- reviewed runtime-authority configuration and reviewed capture policy are composition-owned, not caller/task/API/MCP/transport-selected;
- capture secret safety is recomputed from persisted PNG bytes and the pinned mask policy;
- raw edge observations cannot self-assert secret-safe capture;
- trusted capture is accepted only when its runtime binding matches the current admitted namespace/container/display/PID/start/XID/client version/size/SHA and current task/run;
- edge transport remains authority-neutral and cannot mint Track A/runtime/mutation authority;
- replay state is stored in the existing Control Center SQLite store and survives reconstruction;
- replay load, HMAC/replay verification and persisted ledger update execute in one existing SQLite `BEGIN IMMEDIATE` transaction domain.

## TDD and falsification evidence

The final independent coordinator review identified a concurrency hole in the first durable replay adapter: two reconstructed verifier objects could load the same old ledger before either persisted the advanced window.

A deterministic regression test was added in `test_vision_p2_trusted_replay_atomicity.py`. On `a09c054301770fab2588722970d3c183b6626dce` it failed exactly with `load=0` and `save=0` transaction depths. The minimal production repair on `062a5c173b3410ec8fc2e5efaaefa1c4e34d15d6` wrapped the whole load -> verify -> save path in the existing store transaction domain.

Final replacement head `700e1d5481368b3ef3ebc0501477b566042c55b8` passed:

- Track A agent runtime governance `33600382622`: SUCCESS;
- Track A canonical current-client fence `33600382560`: SUCCESS;
- Track A canonical live governance `33600382576`: SUCCESS;
- Package A `33600382566`: SUCCESS;
- Package B `33600382549`: SUCCESS, including full regression, fresh falsification audit and real browser/CLI E2E;
- CI `33600382928`: SUCCESS, including the non-draft Linux release/tests build path.

The full 17-file diff was reviewed with no unrelated or forbidden path, and final review hygiene was `0` review submissions / `0` review threads.

## Merge and replacement history

Draft PR #846 was closed unmerged only because the GitHub connector's Draft→Ready GraphQL mutation failed on the unsupported `Repository.fullDatabaseId` field. Non-draft replacement PR #854 reused the exact same branch/head, reran its own merge-grade checks, and squash-merged successfully as:

`2e57cb1f0b57d44b1adf553d06b18e22e145c77e`

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

Implementation work is complete, merged and ownership is released. The task is archived by the lifecycle closeout PR. Live read-only runtime observation remains a separate later serialized programme gate and is not implied by this repository/static completion.