# Exact-version Qt connect callsite census

## Scope

This record preserves a bounded static census for the official native Linux Tibia client `15.32.df7b29`, SHA256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

The scanner enumerated direct x86-64 `E8 rel32` calls from executable `PT_LOAD` segments to three PLT targets recovered by the preceding Qt symbol census. It did not reconstruct sender/receiver objects, signal/slot identities, indirect calls, or semantic ownership.

## Evidence

```yaml
symbol_census:
  run: 31793668176
  head: 6cf46ed2cb1c277c5bde247e7d4ba5cc668ff35b
  result: PASS
callsite_census:
  run: 31799755489
  job: 94764705414
  head: 3d0a54a9edd658555df44929494c902abfd846ec
  runner: synology-otclient-01
  result: PASS
  counts:
    QObject_connectImpl: 2078
    QObject_connect_legacy_string_api: 41
    QObject_disconnectImpl: 65
    total: 2184
```

The exact completion markers were `TOTAL_QT_CONNECT_CALLSITES=2184` and `TRACK_A_QT_CONNECT_CALLSITE_CENSUS_COMPLETE=true`.

## Classification

`PROVEN`: the exact binary contains the counted direct calls to the three exact PLT targets under the scanner's stated instruction boundary.

`UNKNOWN`: which calls are Tibia-owned semantic connections; sender and receiver types/instances; signal and slot identities; connection types; indirect or wrapper-mediated connections; relationships to protocol queues, storages, controllers, or generated messages.

## Next experiment

Run `31800072490` / job `94765746423` successfully produced all 41 bounded GDB neighborhoods after one failed system-`objdump` availability hypothesis (`31799979849`). The neighborhoods prove that candidate legacy calls commonly load signal and slot string pointers into `rdx` and `r8` immediately before the call, but the raw neighborhood log does not itself validate every pointed-to string.

Next, structurally resolve the nearest printable C-string targets loaded into `rdx` and `r8` for every legacy callsite. Classify every callsite as a recovered candidate edge or explicit `UNCLASSIFIED`, then decide whether any edge belongs to a high-value Tibia protocol/storage/controller path before attempting the larger `connectImpl` population.
