# Track A canonical coverage registry

This directory is the canonical machine-readable Track A coverage registry. The immutable quantitative baseline comes from closed Draft PR #304 at exact head `43a60bd96cc644b656b200c9edbfb75578b330b6`, coordinator-disposed `ACCEPT_WITH_EDITS` as bounded inventory/provenance evidence only, exact-client fenced to official native Linux Tibia `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

The registry has three layers:

1. **immutable accepted baseline** — exact #304 blobs for inventories, selected subsets, provenance and supersessions;
2. **finite denominator registries** — one canonical row for every currently normalized protocol, Tibia-owned QMeta, P0 item and P1 item;
3. **current-main overlay** — programme dispositions that may advance independently of the historical baseline.

Never rewrite baseline records to make them look current. A complete denominator is not semantic completion.

## Canonical machine-readable entry points

- `protocol_messages.jsonl` — exact generated-message inventory: 349 identifiers = 189 server→client + 160 client→server.
- `protocol_message_semantics.jsonl` — E51 denominator: 349/349 identifiers, deterministic lexical family label plus explicit semantic state. Current semantic support remains `UNKNOWN/349`; lexical grouping is not semantic proof.
- `runtime_type_semantics.jsonl` — E52 denominator: 642/642 unique `tibia::` QMeta records from exact retained run `31790507112`, job `94736106350`; semantic role remains `UNKNOWN/642`. The historical 47 handler records are a bounded subset of this denominator.
- `p0_items.jsonl` — normalized P0 denominator: 180 individual read/state/action requirements grouped under the 16 normative programme headings. The 16 headings are grouping only.
- `p1_items.jsonl` — normalized P1 denominator: 28 bridge/read/evidence requirements. The seven profile discovery targets are an implementation subset, not the global denominator.
- `capabilities.jsonl`, `runtime_types.jsonl`, `bridge_fields.jsonl`, `protocol_direct_qmeta_cases.json`, `gameaction_connects.json`, `legacy_qobject_connect_edges.json` — preserved historical/bounded evidence.
- `provenance.json`, `supersessions.jsonl` — accepted source provenance and retained `DISPROVEN/SUPERSEDED` / `UNKNOWN` evidence.
- `coverage-summary.json` — current quantitative boundary.
- `current-main-overlay.json` — current programme-state overlay.
- `canonical-manifest.json` — immutable source-fence and Git-blob map.
- `validate_registry.py` — deterministic baseline, denominator and overlay validator.

## Current normalized denominator boundary

| Surface | Complete denominator | Semantic numerator |
|---|---:|---:|
| generated protocol messages | 349 / 349 | UNKNOWN / 349 |
| full retained `tibia::` QMeta | 642 / 642 | UNKNOWN / 642 |
| P0 individual requirements | 180 / 180 | UNKNOWN / 180 |
| P1 individual requirements | 28 / 28 | UNKNOWN / 28 |

`100%` in the denominator column means every denominator member is represented. It does **not** mean support, correctness, live authority or restart stability is proven.

The separate `612` versus historical `1004` action/QMeta definition conflict, current canonical live semantics, restart/relogin proof and stale global coordinator checkpoint remain unresolved programme work.

## Validation

Run:

```bash
python3 docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit/validate_registry.py \
  docs/agents/evidence/OTC-20260815-track-a-coverage-registry-audit
```

Expected terminal marker:

```text
CANONICAL_COVERAGE_REGISTRY_VALIDATION=PASS
```
