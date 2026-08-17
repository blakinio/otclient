# Track A canonical coverage registry

This directory is the canonical machine-readable Track A coverage registry once the integration tree containing it is on `main`.

## Authority boundary

The quantitative baseline comes from closed source Draft PR #304 at exact head `43a60bd96cc644b656b200c9edbfb75578b330b6`, previously coordinator-disposed `ACCEPT_WITH_EDITS` as **bounded inventory/provenance evidence only**. The baseline is exact-client fenced to official native Linux Tibia `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

The canonical registry deliberately has two layers:

1. **immutable accepted baseline** — exact #304 blobs for inventories, selected subsets, provenance and supersessions;
2. **current-main overlay** — current programme dispositions that may advance independently of the historical inventory source.

Never rewrite historical baseline records to make them look current. Read `canonical-manifest.json` and `current-main-overlay.json` together.

## Canonical machine-readable entry points

- `capabilities.jsonl` — 16 top-level P0 requirement-group records; this is not an item-level live-read denominator.
- `protocol_messages.jsonl` — exact 349-name generated-message inventory, 189 server→client + 160 client→server.
- `runtime_types.jsonl` — bounded 47-handler QMeta/runtime inventory; this is not the full Tibia-owned runtime-type denominator.
- `provenance.json` — accepted source/run/job/head provenance.
- `supersessions.jsonl` — retained `DISPROVEN/SUPERSEDED` and scope-`UNKNOWN` evidence.
- `bridge_fields.jsonl`, `protocol_direct_qmeta_cases.json`, `gameaction_connects.json`, `legacy_qobject_connect_edges.json` — supporting bounded selected-set evidence.
- `coverage-summary.json` — current canonical coverage boundary, not a semantic-completion score.
- `current-main-overlay.json` — live programme-state overlay for this registry generation.
- `canonical-manifest.json` — source-fence and exact Git-blob map.
- `validate_registry.py` — deterministic baseline and overlay validator.

Exact historical source files whose wording became stale are retained with `source-` prefixes. They are provenance artifacts, not current programme instructions.

## Nonclaims

`349/349`, `47/47`, `2184/2184`, `16/16`, `7/7`, `40/41` and `29/31` retain their original bounded meanings. They do **not** establish global protocol semantics, full QMeta/runtime semantics, P0/P1 item-level completion, canonical live runtime authority, restart/relogin stability, or Track A completion.

E51, E52, normalized P0/P1 denominators, the `612` vs historical `1004` action/QMeta denominator conflict, and physical runtime semantic/restart proof remain separate work.

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
