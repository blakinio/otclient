---
task_id: OTC-20260813-official-client-re-continuation
status: ready
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
job: 94733517691
job_conclusion: success
state_at_checkpoint: completed
finding:
  scanner: one linear executable PT_LOAD pass over direct x86-64 RIP-relative LEA/MOV references
  selected_literal_direct_riprefs: 0
  total_direct_riprefs: 0
limitation: the negative result applies only to the scanned direct instruction forms and exact selected literal addresses
```

## Qt connect census gate

```yaml
symbol_census:
  run: 31793668176
  head: 6cf46ed2cb1c277c5bde247e7d4ba5cc668ff35b
  result: PASS
  proven_plt_targets:
    QObject_connectImpl: 0x4dd800
    QObject_connect_legacy: 0x4dffd0
    QObject_disconnectImpl: 0x4de9e0
callsite_census:
  first_run: 31794273375
  repaired_run: 31799755489
  repaired_job: 94764705414
  repaired_head: 3d0a54a9edd658555df44929494c902abfd846ec
  state: PASS
  first_failure: workflow requested labels not exposed by synology-otclient-01; successful adjacent Track A jobs use only otclient/synology
  repair: use [otclient, synology]
  counts:
    QObject_connectImpl: 2078
    QObject_connect_legacy_string_api: 41
    QObject_disconnectImpl: 65
    total: 2184
```

## Anti-stall checkpoint

```yaml
checkpoint_version: 5
updated_at: 2026-08-14T14:30:00+02:00
owner_resume: explicit
branch: ci/OTC-20260813-official-client-re-continuation
pr: 289
status: ready
last_progress:
  - verified xref-v2 run 31789670398 PASS with zero direct selected-literal RIP references
  - verified Qt connect symbol census run 31793668176 PASS
  - isolated the queued callsite census to a runner-label mismatch and aligned it with successful adjacent Track A workflows
  - completed repaired callsite census run 31799755489 with 2184 direct calls
  - persisted the bounded experiment record and selected legacy string-connect neighborhood reconstruction
  - isolated legacy-neighborhood run 31799979849 failure to unavailable system objdump and reused the proven Track A toolroot GDB path
  - completed GDB neighborhood run 31800072490 for all 41 legacy string-connect callsites
  - completed string-edge run 31800240820 with 40 classified UI/controller edges and one explicit UNCLASSIFIED callsite
  - completed GameAction connectImpl correlation run 31800490781 with 86 bounded pairs and a 31-candidate near subset
unchanged_state_checks: 0
identical_failure_retries: 0
repair_cycles_for_current_gate: 3
stall_warnings: 0
blockers: []
```

## Recovery checkpoint

```yaml
recovery:
  policy_version: 1
  generation: 1
  session_id: 20260814-track-a-gemma-continuation
  session_started_at: 2026-08-14T14:00:00+02:00
  checkpointed_at: 2026-08-14T16:00:00+02:00
  last_progress_at: 2026-08-14T16:00:00+02:00
  phase: static-protocol-queue-serializer-convergence
  exact_head: 79adf63ea51194d101a279f8d7ba55ff82c858bd
  pull_request: 289
  active_operation: none
  external_run_ids: [31799755489, 31799979849, 31800072490, 31800240820, 31800490781, 31800999307, 31801334150, 31801505722, 31801581157, 31801659100, 31801723690, 31801845276, 31802254026, 31802346130, 31802470787, 31802657753, 31802808290, 31802935253, 31803012968, 31803088165]
  operation_started_at: null
  wait_deadline_at: null
  check_generation: experiment
  checks_used: 2
  status: ready
  safe_to_resume: true
  resume_condition: slot provenance and invoker semantics are committed and pushed
  next_action: follow TProtocolMessageQueue sendMessage and queue-processing helpers to exact serializer and network framing
```

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-14T15:15:00Z
head: 79adf63ea51194d101a279f8d7ba55ff82c858bd
branch: ci/OTC-20260813-official-client-re-continuation
pr: 289
status: ready
context_routes:
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
owned_paths:
  - .github/workflows/tibia-official-client-re-*.yml
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
proven:
  - xref-v2 run 31789670398 completed successfully with TOTAL_DIRECT_RIPREFS=0 for its exact bounded scanner
  - Qt symbol census run 31793668176 recovered the three selected QObject connect/disconnect PLT targets
  - synology-otclient-01 is online and successful adjacent Track A workflows select it with otclient/synology
  - repaired callsite census run 31799755489 enumerated 2184 direct calls across three exact PLT targets
  - GDB neighborhood run 31800072490 emitted all 41 bounded legacy callsite disassemblies
  - string-edge run 31800240820 classified 40 legacy UI/controller edges and retained one explicit UNCLASSIFIED callsite
  - correlation run 31800490781 found 31 distance-at-most-64 GameAction metaobject/connectImpl candidates across all six families
  - corrected argument run 31801334150 reconstructed the hidden-return ABI, all 31 AutoConnection/null-types/slot-object arguments, 29 exact sender-metaobject matches, one mismatch and one bounded unresolved case
  - provenance run 31801723690 resolved QSlotObject invoke addresses for all 29 proven sender sites, with 24 unique addresses and no unresolved entries
  - invoker run 31801845276 proved selected invoke addresses are generic QSlotObject operation/member-pointer dispatchers rather than receiver serializers
  - payload run 31802254026 resolved both slot payload words for all 29 proven sender sites with zero unresolved values
  - QMeta run 31802470787 identifies shared receiver 0x8332d0 as tibia::game::TInternalGameActionRouter, an internal re-emitter rather than serializer
  - QMeta run 31802808290 identifies tibia::protocol::TProtocolMessageQueue and exact indices for queue, movement and high-value action methods
  - dispatch/build runs 31802935253 and 31803012968 map concrete builder bodies and internal discriminators for movement, MoveObject, Talk, Attack, Follow and TradeObject
derived:
  - the 41 legacy string-based connect calls are the smallest high-information subset for argument reconstruction
  - high-value GameAction send signals are absent from the recovered legacy string-edge set and should be tested against connectImpl/wrapper paths
unknown:
  - receiver identities for the six high-value GameAction send signals
  - exact serializer/framing and final network-send path downstream of TProtocolMessageQueue::sendMessage
  - whether proven internal message discriminators are preserved as final wire bytes
  - pointer-to-member signal indices for the proven sender-metaobject sites
conflicts: []
first_failure:
  marker: legacy_neighborhood_disassembler_unavailable
  evidence: run 31799979849 job 94765445120 stopped before Python output at command -v objdump
rejected_hypotheses:
  - runner unavailable: GitHub runner API reports synology-otclient-01 online and idle
  - system objdump available: run 31799979849 exited at the explicit availability check
changed_paths:
  - .github/workflows/tibia-official-client-re-qt-connect-callsite-census.yml
  - .github/workflows/tibia-official-client-re-qt-legacy-connect-neighborhoods.yml
  - .github/workflows/tibia-official-client-re-qt-legacy-connect-string-edges.yml
  - .github/workflows/tibia-official-client-re-gameaction-connectimpl-correlation.yml
  - .github/workflows/tibia-official-client-re-gameaction-connectimpl-arguments.yml
  - .github/workflows/tibia-official-client-re-gameaction-slot-provenance.yml
  - .github/workflows/tibia-official-client-re-gameaction-slot-invokers.yml
  - .github/workflows/tibia-official-client-re-gameaction-receiver-targets.yml
  - .github/workflows/tibia-official-client-re-shared-receiver-qmeta.yml
  - .github/workflows/tibia-official-client-re-gameaction-receiver-callee-xrefs.yml
  - .github/workflows/tibia-official-client-re-protocol-queue-action-dispatch.yml
  - docs/agents/tasks/active/OTC-20260813-official-client-re-continuation.md
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-qt-connect-callsite-census.md
  - docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-qt-connect-callsite-census.yaml
  - docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-qt-legacy-connect-string-edges.yaml
  - docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-gameaction-connectimpl-correlation.yaml
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-gameaction-connectimpl-arguments.md
  - docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-gameaction-connectimpl-arguments.yaml
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-gameaction-slot-provenance.md
  - docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-gameaction-slot-provenance.yaml
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-action-builders.md
  - docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-protocol-queue-action-builders.yaml
validation:
  - command: YAML safe_load and git diff --check
    result: PASS
    evidence: local exact working tree
blockers: []
next_action: follow TProtocolMessageQueue sendMessage and queue-processing helpers to exact serializer and network framing
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
Rebuild the PR #283 read-only bridge helper against the official client's bundled Qt 6.9 headers/libraries (or avoid exposing the extracted Qt 6.4 runtime through LD_LIBRARY_PATH), then repeat semantic world login and correlate bridge `session-status` with the already proven decoded map state. Separately resolve the concrete function behind the containing network owner's virtual slot `+0x90` before naming an exact serializer/framing entry.
```

## Live continuation checkpoint — 2026-08-14 16:35 CEST

```yaml
checkpoint_version: 6
head: 9af08efbf1aaf51c220205fb5142c1db361e03b6
branch: ci/OTC-20260813-official-client-re-continuation
pr: 289
status: ready
proven:
  - exact live world bootstrap run 31730884814 left the owned client running through WARP
  - persistent structural observer run 31806223531 armed exact map decoding
  - reversible movement run 31806312967 decoded the derived path (32546,32510,7) -> (32546,32509,7) -> (32546,32510,7)
  - player and creature handler QMeta outcomes plus selected live map-strip layout are persisted
  - requested outbound action builder bodies and internal discriminators are recovered
  - clientMessageReadyToProcess hands queue owner+0x88 to containing owner virtual slot +0x90
  - setup path constructs QTcpSocket at +0x196fee0
  - QMeta run 31806620571 identifies 0x3085ba0 as TCreatureStorage and rejects it as transport owner
  - exact PR 283 bridge source builds successfully in run 31809994339
derived:
  - player coordinate is derived from authoritative decoded strip geometry, not a direct standalone member read
unknown:
  - concrete function and exact serializer/framing semantics behind virtual slot +0x90
  - final wire-byte relationship of internal message discriminators
  - live bridge session-status correlation
current_failure:
  run: 31809994339
  job: 94798051385
  step: Bridge session DBus to private AT-SPI and inspect Tibia
  cause: extracted Ubuntu Qt 6.4 libQt6Core shadows the official client's required bundled Qt_6.9 runtime
  exact_error: "libQt6Core.so.6: version Qt_6.9 not found"
  repeated_identical_failures: 1
persisted_evidence:
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-live-structural-world-and-reversible-movement.md
  - docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-live-reversible-movement.yaml
  - docs/agents/evidence/OTC-20260813-official-client-re/20260814-protocol-queue-network-handoff.md
  - docs/agents/evidence/OTC-20260813-official-client-re/experiments/EXP-20260814-protocol-queue-network-handoff.yaml
local_worker_review:
  model: gemma4:12b
  result: position remains DERIVED and slot +0x90 must not yet be called the exact serializer
next_action: keep extracted build tools out of client LD_LIBRARY_PATH, launch with bundled Qt 6.9, and query bridge session-status after semantic world entry
```
