# OTCLIENT-TIBIA-RE — world/minimap static G1

```yaml
report_date: 2026-08-19
repository: blakinio/otclient
task_id: OTC-20260819-track-a-world-minimap-static-g1
pr: 593
alias: TIBIA-RE-WORLD-MINIMAP
execution_class: github_hosted
runtime_access: none
physical_e2e_required: false
e2e_result: NOT_APPLICABLE
e2e_reason: documentation-only GitHub-hosted static evidence; no executable, UI, runtime, network, or product behavior changed
evidence_status: historical_unverified_transcription
promotion_authority: false
remediation_date: 2026-09-01
trusted_main_at_remediation: 54a20bbd8721e92d069974af14d6ebd2f4f5a55d
```

## Executive result

G1 preserves the 2026-08-19 producer transcription but, after fresh independent audit, **does not promote its F11/F12/F13 address/offset/formula details into current trusted authority**. Both primary artifacts expired and exact historical replay now fails closed because the public package moved.

```text
F11 Minimap controller / visible area / floor state  PARTIAL -> PARTIAL (no new G1 promotion)
F12 Minimap markers                                  PARTIAL -> PARTIAL (no new G1 promotion)
F13 World<->screen coordinate transforms             PARTIAL -> PARTIAL (no new G1 promotion)
F08 Server-delivered map extent/control              BLOCKED unchanged
F10 Worldmap patch causal propagation                BLOCKED unchanged
```

Current trusted Track A fence at remediation: `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`. Historical G1 producer fence: `15.32 / 52109920 / ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`. These are deliberately not conflated.

## Historical producer record and audit remediation

Producer v1:

```text
head       eff3ddf9c2054c1398975d1a2939a5cd01259b63
run/job    32249741341 / 96057873107
result     SUCCESS (historical)
artifact   9363988901
artifact_status EXPIRED / HTTP 410 on 2026-09-01
zip sha    68e1864b990742814d11501fbf6757fcf5da4677d3718bf093227173ba4d5745
```

Producer v2:

```text
head       91004362eaa5562cf268fff455c161b6f55dc7c2
run/job    32250742374 / 96060897630
result     SUCCESS (historical)
artifact   9364339983
artifact_status EXPIRED / HTTP 410 on 2026-09-01
zip sha    ba5cdae01c702c618a9944de6b4630605ed3eae85b0bed3f0ba66ec69d3ba81f
```

Both original runs matched the then-current 2026-08-19 public package fence:

```text
packed sha256   1fc26d66cef90723d29293f177fcff41c8e937e7aac830f08e82c2f4c69eb354
unpacked sha256 ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8
unpacked size   52109920
```

No raw packed or unpacked client was retained in either artifact.

Fresh independent audit (`gpt-5.6-luna`, medium, session `01a05dcd-59a6-7523-94c4-5c6e7d585f11`) returned `AUDIT_FAIL`:

- `WM-G1-AUD-001` — stale main snapshot;
- `WM-G1-AUD-002` — expired primary producer artifacts;
- `WM-G1-AUD-003` — missing structured E2E `NOT_APPLICABLE` result/reason.

Remediation re-ran the exact historical producer jobs. Both failed closed before analysis because the September 1 public `client.lzma` no longer matched the historical packed fence; v1 observed packed SHA `439db64ead9b62aa0870094fa0ce30e8e0ccaf35844de1a515692770a7019036`. Cleanup passed and no raw client was retained. The current trusted repository fence is `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`. Therefore the historical G1 values below are useful hypotheses only, not promotion authority.

## Producer correction carried forward

G0 audit finding `WM-MINIMAP-AUD-001` remains controlling: nearby executable relative tables are not enough to assign method entry addresses.

G1 v1 instead required the exact Qt method-ID discriminator, bounds check, relative jump table, table-base addition and final indirect jump. That recovers direct **method case** mappings for the targeted Qt metaobjects.

A separate v1 convenience step that searched forward for a first direct `call` could cross into the following method case. Those `first_direct_call` values are rejected. Producer v2 was added specifically to emit direct bounded disassembly windows without that inference.

## F11 — layer and visible area

Historical producer transcription reported:

- `TMinimapController +0x48` references the internal minimap view/layer state used by the relevant controller methods;
- current layer is signed `int32` at internal state `+0x60`;
- floor-up decrements the field and floor-down increments it;
- both controller actions and `setCurrentLayer` clamp the value to **0..15 inclusive**;
- the setter triggers the common viewport/recompute path and `currentLayerChanged` notification;
- visible-area refresh obtains the actual QML quick-item dimensions from `controller +0x90`;
- the direct path stores integer **width at state +0x84** and **height at state +0x88**, then recomputes the view.

These details are not re-promoted after audit because their primary artifact expired; they remain hypotheses for a future exact-build producer.

Still UNKNOWN for `DONE`: the complete source-level internal-state type/member model, all tile/cache boundary selection and eviction semantics, and any required live/restart-stability proof.

## F12 — marker storage and persistence

Historical producer transcription reported the following marker model:

- `TMinimapMarkerStorage` has three Qt signals followed by two non-signal methods;
- `startSavingMinimapMarkerFileContentToDisk` is a signal carrying shared `MinimapMarkerFileContent` ownership, not itself proven to perform the file write synchronously;
- `setMarkersFromMinimapMarkerFile` passes its payload through an exact virtual slot boundary;
- `onDelayedCallback` is gated by a byte at storage `+0x40` before entering its save-side virtual path;
- the historical transcription records strings/xrefs for `minimapmarkers.bin`, marker protobuf type names and explicit serialize/deserialize failure paths.

The bounded descriptor scan recovered **zero admissible `FileDescriptorProto` candidates**. This is recorded as non-recovery only.

Still UNKNOWN for `DONE`: exact protobuf field numbers/types, coordinate encoding, marker limits, duplicate/overwrite policy, and complete persistence/restart transaction semantics.

## F13 — exact layer transform term

The historical producer transcription reported direct helper bindings for the 2026-08-19 package; they are not current promotion authority.

For projection mode `0`, the transcribed 2026-08-19 forward subfield-to-stretched-pixel operation is:

```text
X = x + 32*L
Y = y + 32*L
```

and the inverse at the same layer is:

```text
x = X - 32*L
y = Y - 32*L
layer = L
```

The transcribed formulas algebraically imply this mode-0 round trip, but it is not independently revalidated primary evidence:

```text
(3,5,7) -> (227,229) -> (3,5,7)
```

Additional historical transcriptions:

- `setAdditionalColumnsAndRows` stores its four signed 32-bit arguments at viewport `+0xa0..+0xaf` and schedules recomputation through a timer;
- `translateBySubfieldOffset` component-wise adds the supplied two-integer offset to the viewport pair at `+0x88`.

Still UNKNOWN for `DONE`: complete non-zero projection/shearing/scale/rounding semantics and any required governed live click/pick round trip.

## Safety boundary

```yaml
synology_observed: false
kasmvnc_observed: false
official_client_executed: false
credentials_accessed: false
login_attempted: false
gameplay_attempted: false
process_memory_accessed: false
client_byte_mutation: false
raw_client_retained: false
```

This task does not inherit any runtime/login/mutation authority from PR #475. F08/F10 remain the separate worldmap causal frontier.

## Durable evidence

Primary record:

`docs/agents/evidence/OTC-20260819-track-a-world-minimap-static-g1/20260819-layout-schema-transform.md`

## Next discriminators

The highest-information follow-ups are:

1. recover the complete internal minimap view-state type and tile/cache boundary consumers of layer, width, height and zoom;
2. recover marker protobuf fields using a different exact descriptor/generated-code reconstruction strategy rather than repeating the exhausted bounded FileDescriptorProto scan;
3. finish the non-zero world-map projection/shearing/rounding formula family;
4. only when the row contract genuinely requires it and a separately legal runtime exists, correlate these static models against read-only/live behavior without borrowing #475 authority.

No additional client mutation or login is justified by this G1 static result. Re-promotion requires a fresh repository/static producer for the then-current exact build, not runtime borrowing from PR #475.