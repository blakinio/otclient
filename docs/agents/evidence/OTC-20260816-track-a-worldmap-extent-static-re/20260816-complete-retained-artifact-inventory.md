# OTC-20260816 — complete retained-artifact inventory and exact-static boundary

```yaml
evidence_date: 2026-08-16
repository: blakinio/otclient
task: OTC-20260816-track-a-worldmap-extent-static-re
pr: 367
execution_class: github_hosted
runtime_used_by_this_task: false
client_bytes_modified: false
owner_funded_ai_api_authorized: false
exact_client_version: 15.32.df7b29
exact_client_size: 51965216
exact_client_sha256: e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

## Scope and wording

This checkpoint corrects and strengthens the earlier retained-evidence exhaustion statement.

**FACT:** the GitHub Actions artifact inventory contains 493 artifacts. The inventory was paged across the repository and the admissible official-Linux Track A period was bounded. Pages 4 and 5 contain no `track-a-*` artifacts; older inventory is OTClient/Windows/build material and is not admissible as official native Linux Track A evidence.

**FACT:** every retained artifact in the bounded Track A inventory whose name/scope directly indicated `static`, `vtable`, `RTTI`, `provenance`, or relevant writer/xref analysis was either already consumed by this task or was newly downloaded and inspected in this continuation. The final large `track-a-single-item-drag-only` runtime bundle was also inspected because it was a plausible accidental carrier of broader GDB/static evidence.

This does **not** claim that every byte of every one of the 493 repository artifacts was decompressed. It claims a complete repository-level inventory review plus direct inspection of the admissible static/vtable/RTTI/provenance candidates that can answer the currently blocking identity/writer questions.

## Newly inspected retained artifacts

The continuation directly downloaded and searched the following previously unconsumed or incompletely consumed artifacts in addition to the existing P0/provenance set:

```text
9233690471  track-a-login-envelope-static-provenance-31839255046
9231716774  track-a-tcp-member-rtti-31833767461
9228275973  track-a-outbound-owner-vtables-31824546383
9228087310  track-a-transport-vtable-rtti-31824001391
9228921041  track-a-login-origin-write-xrefs-31826270686
9226966960  track-a-qiodevice-write-xrefs-31821085647
9246854524  track-a-p2-writer-vtable-group-31884379539
9246830425  track-a-p2-writer-vtable-group-31884286098
9246826386  track-a-p2-writer-vtable-group-31884269376
9246813407  track-a-p2-writer-vtable-group-31884222309
9246799418  track-a-p2-writer-vtable-group-31884166982
9229251044  track-a-network-writer-vtable-census-31827157926
9229184085  track-a-network-writer-vtable-census-31827016253
9229127873  track-a-network-writer-vtable-census-31826856086
9221392689  track-a-single-item-drag-only
```

Previously consumed exact-static/raw artifacts were re-opened in their full archives rather than relying on earlier summary snippets:

```text
9246756211  track-a-p0-static-elf-31883967070
9248797952  track-a-p0-static-elf-31892019505
9227370490  track-a-persistent-provenance-dump / run 31821458677
9228188750  track-a-finish-fixed-login
```

## Broad static reports do not contain the missing worldmap identity windows

The larger static reports are materially bigger when decompressed than their artifact ZIP sizes suggest. Examples inspected directly include:

```text
9233690471 -> static-provenance report ~842 KB
9231716774 -> tcp-member RTTI report ~736 KB
9228275973 -> outbound-owner-vtables report ~347 KB
9228087310 -> transport-vtable-RTTI report ~103 KB
9228921041 -> login-origin-write-xrefs report ~1.5 MB
9226966960 -> QIODevice write-xrefs report ~477 KB
```

These reports contain real generic ELF/vtable/RTTI machinery, but their emitted candidate sets are scoped around network/writer targets. Direct searches found no retained occurrence establishing any of:

```text
geometry object vptr/header   0x0308ce70 / 0x0308ce60..0x0308ce6f
handler owner vptr/header     0x030871d8 / 0x030871c8..0x030871d7
geometry control vptr/header  0x02f683d0 / 0x02f683c0..0x02f683cf
```

and no direct worldmap RTTI relation for those vptrs.

The final `writer-vtable-group` artifacts are repeated protocol-writer evidence around an unrelated typeinfo (`0x3080748`). The final `network-writer-vtable-census` artifacts identify network/sessiondump vtables (for example `0x308c408 -> typeinfo 0x30775a0 -> tibia::game::TSessiondumpGameSession`) and do not contain any of the worldmap identity targets above.

The `track-a-single-item-drag-only` artifact contains only two XWD screenshots plus drag timestamps and no ELF/GDB/static payload.

## Full P0 exact-static archives

The two P0 exact-static archives were reopened in full. They retain the exact target strings:

```text
TWorldMapExtent                                      0x1c8fee0
TWorldMapSubfieldExtent                              0x1c9fe20
counted TWorldMapStorage                             0x1ca9180
counted TWorldMapViewport                            0x1cabb60
TWorldMapCamera                                      0x1cabce0
counted TWorldMapCamera                              0x1cabd20
TWorldmapProtocolMessageHandler                      0x1cd59a0
counted TWorldmapProtocolMessageHandler              0x1cdba40
counted TWorldMapRenderProvider                      0x1cdb580
TWorldMapPicker                                      0x1cdb600
counted TWorldMapPicker                              0x1cdb640
TWorldMapRenderProvider                              0x1cddd20
TWorldMapViewport                                    0x1ce1b60
TWorldMapStorage                                     0x1ce1c00
literal tibia::worldmap::TWorldMapExtentX            0x1cd9ad7
```

Known retained type-name relocation leads remain:

```text
0x3089b78 -> 0x1cddd20  TWorldMapRenderProvider name
0x308b598 -> 0x1ce1b60  TWorldMapViewport name
```

No retained P0 report contains the inverse relation required to connect typeinfo to object vptr `0x308ce70`, and no retained relocation targets the **start** of the counted viewport type string `0x1cabb60`. The old graph probe's substring hit inside the counted string is therefore not a counted-control-block identity proof.

## Full raw persistent-provenance archive: stronger shared-control-block structure

The full artifact `9227370490` contains substantially more raw material than the earlier report summary:

```text
map-provenance-persistent-gdb.stdout   2,285,598 bytes
map-provenance-persistent-raw.log         46,503 bytes
map-provenance-persistent.log             13,501 bytes
map-provenance-persistent-strips.log       3,141 bytes
```

The raw snapshot yields a stronger direct structural fact for the exact `18/14` object.

Historical PIE base:

```text
0x5586665f8000
```

For the `owner+0x10` geometry dependency:

```text
object pointer       = 0x55867df448c0
object runtime vptr  = 0x558669684e70
object static vptr   = 0x0308ce70

companion pointer at owner+0x18 = 0x55867df448b0
companion static vptr           = 0x02f683d0
object - companion              = 0x10 bytes
companion refcount DWORDs       = 13, 1
companion+0x10 begins with the exact object vptr 0x558669684e70
```

**FACT:** the companion/control-like allocation begins exactly `0x10` bytes before the object, contains a polymorphic vptr followed by two reference-count-like DWORDs, and the exact object begins inline at companion `+0x10`.

The same paired pattern repeats in the owner's adjacent dependencies:

```text
owner+0x20 object / owner+0x28 companion
  companion static vptr ~0x02f70c60
  object static vptr    ~0x0308cfd8

owner+0x30 object / owner+0x38 companion
  companion static vptr ~0x02f70c98
  object static vptr    ~0x0308d078
```

**INFERENCE:** this layout is strongly consistent with libstdc++ `std::_Sp_counted_ptr_inplace<T,...>` / `std::make_shared<T>` combined allocation. Because the exact build independently contains `St23_Sp_counted_ptr_inplace<...TWorldMapViewport...>`, the `18/14` object is now a **very strong** `TWorldMapViewport` correlation.

**UNKNOWN:** there is still no retained typeinfo relocation tying static control vptr `0x02f683d0` directly to the counted `TWorldMapViewport` RTTI. Therefore the class identity is intentionally not promoted from inference to fact.

The 2.28 MB GDB stdout and raw log were searched for direct reads of the vtable header words before `0x308ce70`, `0x30871d8` or `0x2f683d0`. They preserve object/control contents and vtable-entry observations, but not the required `vptr-16/vptr-8` header words.

## Track B/build cache explicitly excluded

Actions inventory/cache inspection found large historical BuildKit/artifact blobs associated with PR #284 / `tibia-global-login-lab`.

They are not used here:

- PR #284 is Track B, not Track A;
- cross-track dependency is prohibited by its own scope/governance;
- its artifact/cache provenance does not establish an admissible official exact-client ELF for this Track A static task.

No Track B binary/cache is silently substituted for the fenced official Linux client.

## Current RUNTIME cross-check does not provide a producer

Trusted `main` advanced through runtime graphics work (#398–#405). RUNTIME v7 reached the exact-client launch and bounded window wait after the Qt XCB graphics repair, but again failed closed with:

```text
TRACK_A_CANONICAL_SESSION_ERROR=client_window_missing
TRACK_A_CANONICAL_TRANSITION_ERROR=bootstrap_worker_failed
```

No authoritative canonical registration or Gate B was produced. The v7 attempt was archived on main as governance-invalid and did not stage exact static bytes for this task.

No trusted-main mechanism was found that authorizes this GitHub-hosted STATIC-RE task to silently use Synology as a static-analysis fallback. The physical runtime lane therefore remains separate.

## Final retained-evidence classification

```yaml
artifact_inventory_review: COMPLETE
admissible_static_vtable_rtti_provenance_candidates: INSPECTED
required_worldmap_vtable_header_words: NOT_RETAINED
geometry_0x48_0x4c_direct_writer_xrefs: NOT_RETAINED
render_camera_picker_complete_constraint_graph: NOT_RETAINED
geometry_object_viewport_identity: VERY_STRONG_INFERENCE_NOT_DIRECT_RTTI_PROOF
static_patch_graph_ready: false
classification: BLOCKED_EXACT_STATIC_BYTES_NOT_DURABLY_STAGED
```

## Minimal exact evidence required to continue

The research does not need another broad exploratory run. It needs bounded exact-client evidence:

1. exact QWORD header/relocation resolution for one or more of:

```text
0x030871c8..0x030871d7  -> owner vptr 0x030871d8
0x0308ce60..0x0308ce6f  -> geometry object vptr 0x0308ce70
0x02f683c0..0x02f683cf  -> geometry control vptr 0x02f683d0
```

2. static writer/xref evidence for geometry object fields:

```text
+0x18/+0x1c/+0x30/+0x34
+0x48/+0x4c
```

3. enough exact disassembly/vtable ownership to complete the storage -> render provider -> camera -> picker clipping/culling/transform graph and audit fixed allocations/loop bounds/masks/packing assumptions.

Until those bytes are durably staged by an admissible producer, patch design or client-byte mutation would exceed the evidence.
