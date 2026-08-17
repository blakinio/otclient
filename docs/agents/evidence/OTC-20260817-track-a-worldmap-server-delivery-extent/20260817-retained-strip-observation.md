# OTC-20260817 — retained exact-session worldmap strip observation

```yaml
evidence_date: 2026-08-17
source_artifact_id: 9227370490
source_artifact_name: track-a-persistent-provenance-dump
source_run_id: 31821458677
source_file: map-provenance-persistent-strips.tsv
source_events_file: map-provenance-persistent-events.tsv
new_runtime_used_by_this_task: false
```

## Scope

This task re-inspected the already-retained GitHub Actions artifact used by the earlier Track A provenance work. It did **not** launch, attach to, log into, mutate or otherwise operate a physical client session.

The retained TSV is used only as bounded observational evidence for the normal map-description/storage strip shape. It is not treated as a packet capture and its time clustering is not treated as an atomic protocol-message boundary.

## FACT — retained strip coordinates

Deterministic parsing of the five leading TSV columns (`timestamp`, `x`, `y`, `z`, observation index) gives:

```yaml
total_observations: 90
z_7_observations: 72
z_6_observations: 18
z_7_unique_x_range: 32537..32554
z_7_unique_x_count: 18
z_6_unique_x_range: 32538..32555
z_6_unique_x_count: 18
```

Using only a diagnostic `>10 ms` timestamp gap to split dense bursts yields three clusters of `33`, `55`, and `2` observations. In the first two dense clusters:

```text
cluster 0:
  z=7, y=32502 -> 25 records, 18 unique x, x=32537..32554
  z=6, y=32503 ->  8 records,  8 unique x, x=32548..32555

cluster 1:
  z=7, y=32516 -> 45 records, 18 unique x, x=32537..32554
  z=6, y=32517 -> 10 records, 10 unique x, x=32538..32547
```

The companion retained events file contains two `ChangeOnMap` observations and one `CreateOnMap`; it contains no retained `FullMap` event in that capture.

## INFERENCE — baseline consistency only

The two dense `z=7` rows each cover exactly 18 unique X coordinates. This is consistent with the independently proven client-local baseline width `18` and with a normal movement-edge/map-description strip surface.

The same bursts also contain observations on adjacent `z=6`, but the TSV does not prove those observations came from one atomic server message. Therefore it does **not** prove `SERVER_MULTI_FLOOR_BULK_DELIVERY_SUPPORTED=true`.

## Acceptance consequence

```yaml
NORMAL_OBSERVED_STRIP_WIDTH_18_CONSISTENT: true
PROVES_LARGER_RECTANGLE: false
PROVES_COMPLETE_FLOOR: false
PROVES_MULTI_FLOOR_BULK_MESSAGE: false
PROVES_WHOLE_MAP: false
PROVES_SERVER_MAXIMUM: false
```

This retained observation narrows the normal baseline but cannot establish the maximum server-deliverable extent. All larger/full-floor/multi-floor-bulk/whole-map maximum flags therefore remain governed by the direct current evidence package and stay `UNKNOWN` unless another accepted source proves them.
