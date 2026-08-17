# Track A coverage registry audit — draft

Task: `OTC-20260815-track-a-coverage-registry-audit`  
Base: `main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45`  
Client fence: `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`.

This is a **static/durable-evidence audit**. It performs no login, runtime mutation, gameplay action, secret access, or Track B work. It does not claim Track A completion.

## Verified quantitative boundary

| Metric | Result | Meaning |
|---|---:|---|
| Generated protocol identifier inventory | 349/349 | 189 inbound + 160 outbound names; inventory only |
| Direction assignment | 349/349 | exact census bucket/prefix metadata |
| Directly enumerated inbound QMeta case links | 27/349 | bounded structural links only |
| Generated-message semantic support | UNKNOWN/349 | no truthful global semantic numerator yet |
| ProtocolMessageHandler QMeta inventory | 47/47 | relocation-backed handler subset only |
| Raw direct Qt callsite census | 2184/2184 | 2078 connectImpl + 41 legacy + 65 disconnectImpl |
| Raw direct Qt semantic classification | UNKNOWN/2184 | full sender/receiver/signal/slot semantics unresolved |
| Legacy string connect selected subset | 40/41 | ordinal 2 (`0x84e2a0`) unclassified |
| High-information GameAction sender metaobjects | 29/31 | 1 mismatch + 1 unresolved |
| P0 top-level requirement groups | 16/16 | requirements registry only |
| P0 individual live-read coverage | UNKNOWN/UNKNOWN | denominator normalization missing |
| Bridge-v1 profile targets | 7/7 | implementation inventory only |
| P1 overall field/evidence coverage | UNKNOWN/UNKNOWN | finite required-field denominator missing |
| P2 closure | UNKNOWN/5 | five current-main closure questions remain |
| Restart/relogin read reacquisition | UNKNOWN/1 | not yet proven, not disproven |

`100%` above is never a programme-semantic completion claim.

## P0 denominator decision

`OTCLIENT_TIBIA_RE_EXPERIMENT_SWEEP.md` defines groups `0..15`, so this audit can truthfully inventory **16 top-level requirement groups**. Those groups contain multiple reads and actions, therefore they cannot be used as the denominator for global P0 live-read coverage without a coordinator-approved normalization rule. `p0_live_read_coverage` remains `UNKNOWN/UNKNOWN`.

## P1 / bridge boundary

PR #283 exposes seven exact-profile `DISCOVER` targets and derived `session-status.in_game_candidate`. Exact profile rediscovery and logged-out fail-closed behavior are bounded evidence; live `IN_GAME` authority, authoritative player position and write/action APIs remain unresolved. The 7/7 target inventory is not overall P1 coverage.

## P2 conflict/supersession boundary

Current-main reconciliation supersedes: gameplay-endpoint model rooted at `0xb5b880`, `0xb46bd0` as binary gameplay-frame sink, `0xc33259` as gameplay/network sink, and stale `TProtocolWriter` RTTI `0x3080700`. `supersessions.jsonl` preserves these and other stale claims. P2 still lacks concrete writer ownership, framing order, transformation boundary, final binary egress and causal harness proof.

## Highest-value next hypotheses

1. **P2 / PR #301:** `TGameserverDualConnection -> TProtocolWriter/TIODeviceWriter` ownership/dispatch.
2. **P0 / PR #302:** direct authoritative standalone player XYZ vs derived viewport center.
3. **Runtime/P1 / PR #303:** clean restart/relogin, fresh PID/PIE, structural read reacquisition + bridge marker correlation.
4. **E51:** full itemwise semantic protocol census for all 349 identifiers.
5. **E52:** full Tibia-owned QMeta/controller/storage denominator beyond the 47 handler subset.
6. **P0/P1 denominator decision:** normalize individual required read fields before reporting global percentages.

## Registry encoding

`protocol_messages.jsonl` has one record per direction. Every one of the 349 names is losslessly encoded as a zlib+base64 newline list plus raw SHA-256 and is expanded by `validate_registry.py`. The 27 directly enumerated QMeta inbound cases are explicit names. `runtime_types.jsonl` retains all 47 handler types. `capabilities.jsonl` retains all 16 programme groups. Selected 31/41 connect sets and all supersessions are separately machine-readable.

## Validation

Run:

```bash
python3 validate_registry.py .
```

Expected terminal marker: `COVERAGE_AUDIT_VALIDATION=PASS`.

No source from PR #289 is treated as branch-level authority; only bounded records with exact run/job/head provenance survive contradiction checks against current main/coordinator state.
