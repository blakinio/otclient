# Retained identity-window search exhaustion

## Purpose

Record the bounded retained-evidence search performed after recovery of the direct `18/14` geometry object and handler-owner vptr. This prevents duplicate artifact mining and distinguishes a genuine missing-input blocker from an unexplored retained-evidence path.

Task: `OTC-20260816-track-a-worldmap-extent-static-re`

Historical exact-client fence:

```text
version  15.32.df7b29
size     51965216
sha256   e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe
```

No current runtime/client execution was used.

## Exact identity windows required

Current highest-value static discriminators are:

```text
handler owner vptr        0x030871d8 -> header 0x030871c8..0x030871d7
18/14 geometry object     0x0308ce70 -> header 0x0308ce60..0x0308ce6f
18/14 control-like block  0x02f683d0 -> header 0x02f683c0..0x02f683cf
```

Under the already validated Itanium-vtable method for this exact build, a recovered header/typeinfo relation can assign the object class without relying on proximity or naming guesses.

## Retained files searched

The continuation inspected the retained local copies downloaded from same-repository GitHub Actions artifacts:

```text
worldmap-static-census/static-elf-re.txt
p0-exact-static/static-elf-re.txt
p0-exact-static/player-position-graph.txt
p0-exact-static/player-position-disasm.txt
worldmap-provenance/map-provenance-persistent-raw.log
worldmap-provenance/map-provenance-persistent-gdb.stdout
worldmap-provenance/map-provenance-persistent-events.tsv
worldmap-provenance/map-provenance-persistent-strips.tsv
track-a-login-envelope-static-provenance/track-a-login-envelope-static-provenance.txt
track-a-tcp-member-rtti/track-a-tcp-member-rtti.txt
track-a-transport-vtable-rtti/track-a-transport-vtable-rtti.txt
outbound-owner-vtables/track-a-outbound-owner-vtables.txt
writer-vtable/result.json
writer-vtable/validation.log
```

Artifact archives were also enumerated to verify that no uninspected member containing a broader relocation/data-rel-ro dump was present:

```text
9248797952  track-a-p0-static-elf-31892019505
9246756211  richer exact-static census
9227370490  track-a-persistent-provenance-dump
9233690471  login-envelope static provenance
9231716774  tcp-member RTTI
9228087310  transport-vtable RTTI
9228275973  outbound-owner vtables
9246854524  P2 writer vtable group
```

The login/window image artifact contains XWD screenshots only and is not a static identity source.

## Search result

A recursive textual search for:

```text
0x0308ce70 / 0x308ce70
0x030871d8 / 0x30871d8
0x02f683d0 / 0x2f683d0
0x0308ce60 / 0x308ce60
0x030871c8 / 0x30871c8
0x02f683c0 / 0x2f683c0
0x1cabb60
0x1cdba40
0x1cd9ad7
```

returns only the already-known semantic-string anchors in the exact-static census for the latter three values:

```text
0x1cabb60  full _Sp_counted_ptr_inplace<TWorldMapViewport,...> string start
0x1cdba40  full _Sp_counted_ptr_inplace<TWorldmapProtocolMessageHandler,...> string start
0x1cd9ad7  tibia::worldmap::TWorldMapExtentX literal/string
```

No retained text artifact contains any of the three vptr values or their required preceding header-window addresses as a resolved relocation/data dump.

The raw provenance memory dump contains the **runtime values** from which static vptrs `0x0308ce70`, `0x030871d8` and control-like vptr `0x02f683d0` are derived, but it starts dereferenced object snapshots at the vptr and does not preserve the ELF `.data.rel.ro` bytes immediately preceding those vptrs. Therefore it cannot prove the Itanium typeinfo pointer.

## Counted-type probe coverage gap

The historical P0 exact-ELF graph probe searched the needle:

```text
N5tibia8worldmap17TWorldMapViewportE
```

and found both the plain RTTI name and that substring inside the longer counted-type string. Its relocation collector used only the exact addresses of those substring hits as targets.

The full counted viewport string starts at:

```text
0x1cabb60
```

while the viewport substring inside it begins later. Therefore the historical probe did **not** test relocations targeting the full counted-type string start. The same issue is relevant to the full counted protocol-handler string at `0x1cdba40`.

This is a proven probe-coverage gap; it is not evidence that the corresponding control-block RTTI/vtable relation does not exist.

## What remains unavailable

The retained evidence inspected does not provide:

1. the `.data.rel.ro` / relocation words at any of the three exact identity header windows;
2. a relocation graph whose target is full counted viewport string start `0x1cabb60`;
3. a relocation graph whose target is full counted protocol-handler string start `0x1cdba40`;
4. direct code/data xrefs or writers to geometry-object offsets `+0x48/+0x4c`;
5. the additional exact code/RTTI windows needed to name `0xced1b0`, its `self+0x30` dependency, and downstream render/camera/picker consumers.

## Blocker classification

```yaml
classification: MORE_STATIC_RE_NEEDED
retained_identity_search: EXHAUSTED_FOR_CURRENT_DOWNLOADED_SET
fresh_exact_binary_materialization: BLOCKED
STATIC_PATCH_GRAPH_READY: false
mutation_authorized: false
runtime_required_now: false
```

The next high-value advance requires **new exact static evidence**, not another scan of the same retained files. Acceptable examples are a previously uninspected retained same-repository artifact containing the exact windows, or a coordinator/governance-compliant staging of the fenced exact client sufficient to extract only the missing bounded bytes/relocations.

Do not repeat the already-failed identical official CDN staging attempt. Do not use Synology as an unauthorized static-analysis fallback.
