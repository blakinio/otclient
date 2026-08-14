---
task_id: OTC-20260813-official-client-re-continuation
status: investigating
track_id: official-client-re
alias: OTCLIENT-TIBIA-RE
branch: ci/OTC-20260813-official-client-re-continuation
base_branch: main
pr: 289
task_kind: runtime-research
phase: static-protocol-metadata-mapping
risk: medium
runtime_platform: native_linux_only
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - .github/scripts/tibia-official-client-re-*
  - tests/tools/test_tibia_official_client_re_*.py
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/**
modules_touched:
  - official-client-re workflow and evidence only
reuses:
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-login-recovery-import.md
  - PR 283 runtime bridge after exact-SHA validation
depends_on:
  - synology-otclient-01 availability
blocks: []
cross_repository_tasks: []
---

# OTC-20260813 — Official Linux client RE continuation

## Objective

Continue Track A against the official native Linux Tibia client only. Recover and validate structural world/player/creature/inventory/protocol/action state without OCR assumptions, preserve runtime isolation from Track B, and promote only exact-version evidence with explicit confidence boundaries.

## Runtime ownership

```yaml
runner: synology-otclient-01
subject: official native Linux Tibia client only
state_directory: /home/runner/_work/_otclient_tibia_re_state
legacy_compatibility_state_directory: /work/_otclient_tibia_re_state
display: :98
warp_socks_port: 25354
bridge_socket: <state_directory>/runtime/otclient-tibia-re.sock
process_marker: OTCLIENT_TIBIA_RE_TRACK=official-client-re
container_names: none
```

Track B runtime/process/display/ports/state remain out of scope and must not be read, stopped, attached to, reconfigured or cleaned by this task.

## Acceptance inventory

- [x] Track A namespace isolation is proven on the dedicated runner.
- [x] Exact official Linux client version/size/SHA are version-fenced.
- [x] Official client reconstruction and normal owned launch have been proven.
- [x] Protocol surface inventory is persisted from the exact binary.
- [x] High-confidence QMeta/string clusters are persisted for Chat, Container, Effect, Market, NPC Trade, Player Trade, Quest and Game Event.
- [x] Capability/observation matrix is persisted with `FACT` versus `UNKNOWN` boundaries.
- [x] Embedded protobuf `Coordinate` schema is recovered as x=1/y=2/z=3, all `uint32`.
- [x] Selected high-value game message schemas are proven absent from the seven embedded `FileDescriptorProto` records, narrowing layout recovery to generated C++ metadata/accessors/disassembly/runtime objects.
- [ ] Login recovery / structural `IN_GAME` acceptance is re-proven for the current live session when a live-world experiment becomes necessary.
- [ ] Bridge session status is correlated with decoded world state.
- [ ] Authoritative player position and one reversible movement transition are proven structurally.
- [ ] Creature/player handler offsets and selected message field layouts are deterministically recovered.
- [ ] Outbound builder/serializer entry points are recovered for movement, `MoveObject`, `Attack`, `Follow`, `Talk` and `TradeObject`.

## Current exact-version facts

```yaml
official_client_version: 15.32.df7b29
official_client_size: 51965216
official_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
protocol_inventory:
  run: 31787489302
  job: 94726575137
  result: PASS
  totals: {protocol_handler_classes: 47, handle_message_names: 146, inbound_gameserver_messages: 189, outbound_gameclient_messages: 160}
qmeta_neighborhoods:
  run: 31787757301
  job: 94727417973
  result: PASS
symbol_surface:
  run: 31787886977
  job: 94727824870
  result: PASS
  finding: stripped binary exposes no usable qt_static_metacall/staticMetaObject/handler function symbols through GDB
protobuf_descriptor_census:
  parser_revision: 2
  head: f3082b8e9070d390251e5ecf0338ed800e58f5b1
  run: 31789613193
  job: 94733342439
  result: PASS
  valid_embedded_file_descriptors: 7
  coordinate: {x: [1, uint32], y: [2, uint32], z: [3, uint32]}
```

## Promoted static conclusions

- World map snapshot/strip/floor and dynamic create/change/delete paths are separate named inbound protocol surfaces.
- `MoveCreature` and explicit creature-state messages are present in the exact binary.
- Player basic/current/skills/state/inventory/goods/XP/death surfaces are present.
- Inventory/container create/change/delete, stash and depot-search surfaces are present; the main container group is class-locally clustered.
- Chat/channel/player-NPC speech surfaces are present; `handleTalkMessage` and channel lifecycle handlers form a compact Chat cluster.
- NPC trade, player trade, market, quest, game-event and graphical-effect groups have compact class-local method-name clusters.
- Outbound named surfaces include directional movement, `GoPath`, `MoveObject`, object use/look, `Attack`, `Follow`, party actions, `Talk`, NPC/player trade, market, container, stash/depot and buddy/friend actions.
- The embedded serialized descriptor set contains `shared.proto`, `appearances.proto`, `map.proto`, two sound descriptors and two Google protobuf descriptors; it does not contain the selected Gameserver/Gameclient message schemas.
- Protocol/message names do **not** establish wire opcodes, message field layouts, executable handler offsets or safe callable builder offsets by themselves.

## Evidence index

Canonical evidence for the current phase:

- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-official-client-protocol-surface-inventory.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-handler-qmeta-neighborhoods.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-capability-observation-matrix.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/20260814-protobuf-descriptor-census-and-xref-gate.md`
- `docs/agents/evidence/OTC-20260813-official-client-re/README.md`

## Xref gate

### v1 terminal evidence

```yaml
head: 55dc75c830e571490be30a5c83a922a528c5931f
run: 31788735824
job: 94730524231
job_conclusion: cancelled_by_timeout
python_complete_marker: true
finding:
  selected_literal_absolute_qword_refs: 0
  selected_literal_direct_riprefs_reported: 0
limitation: repeated full executable rescan per literal occurrence caused timeout pressure
```

The completed Python output is preserved as partial exact-version evidence; the cancelled GitHub job is not promoted as a PASS.

### v2 replacement

```yaml
workflow: .github/workflows/tibia-official-client-re-xref-graph-v2.yml
head: cfbe04c03de34f83646a82569c90dafaf342c129
run: 31789670398
algorithm: one linear executable RIP-relative LEA/MOV scan indexed by target VA
state_at_checkpoint: in_progress
result_claimed: false
```

## Anti-stall checkpoint

```yaml
checkpoint_version: 4
updated_at: 2026-08-14T11:50:00+02:00
owner_resume: explicit
branch: ci/OTC-20260813-official-client-re-continuation
pr: 289
status: investigating
last_progress:
  - corrected descriptor census parser before promotion
  - descriptor census revision 2 PASS with exact field evidence
  - recorded xref-v1 completed-output/cancelled-job boundary
  - replaced multiplicative xref scan with linear v2 workflow
  - persisted new evidence document and evidence index
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 1
stall_warnings: 0
blockers: []
```

## Rejected interpretations

- Pixels, socket counts or a visible window are not structural `IN_GAME` proof.
- String offsets are not function offsets.
- Protocol/message names are not wire opcodes.
- Absence from embedded `FileDescriptorProto` records is not absence of the message/type from the client.
- QMeta string proximity is not sufficient where class ownership is ambiguous.
- Pre-world GDB attach must not be reintroduced as a normal login diagnostic because prior evidence shows it changes Qt/UI timing.

## Next action

```text
Inspect run 31789670398 once after terminal state. Persist exact linear RIP-reference findings. If literal RIP refs remain empty, move directly to generated protobuf descriptor/default-instance/accessor and Qt integer-offset metadata reconstruction rather than another literal-string xref variant.
```
