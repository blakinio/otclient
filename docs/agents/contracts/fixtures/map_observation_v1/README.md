# Map Observation v1 fixtures

`records.jsonl` is the normative deterministic P0 corpus. Each line is one
record and its byte order is intentional. It contains no wall-clock data or
secret-bearing values.

Validate it from the repository root:

```text
python tools/agents/validate_map_observation_v1_fixtures.py
```

The corpus proves the producer contract's stable shapes; it is not a live map,
packet capture, game login trace, OTBM mapping, or runtime compatibility claim.
