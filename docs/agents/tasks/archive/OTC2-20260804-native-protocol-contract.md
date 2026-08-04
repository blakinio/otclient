---
task_id: OTC2-20260804-native-protocol-contract
status: done
created: 2026-08-04
completed: 2026-08-04
coordination_id: OTS-20260804-native-protocol-selection
implementation_pr: blakinio/otclient#265
implementation_merge_commit: bda9e749e5fefaa89180ede08e355028a4263fc0
canonical_contract_commit: 9035ae987db67c062a8778721a2c8e686ce76750
otheryn_correspondence_commit: 1807b6210375f6a18afabc817a01ccdfee80ddce
released_paths:
  - oteryn-client/docs/architecture/OTERYN_NATIVE_PROTOCOL_CORRESPONDENCE.md
---

# OTC2-20260804-native-protocol-contract — archived

## Result

The Rust consumer/automatic-selection correspondence for the native gameplay contract was completed and merged.

The record defines:

- bounded compiled candidate offers and authoritative Gateway selection validation;
- exact selected endpoint, schema and capability digest checks;
- immutable Game Session/adapter binding and fresh-session replacement behavior;
- independent `protocol-canary` and future `protocol-oteryn` ownership;
- semantic command/result, snapshot/delta, duplicate and resync consumer rules;
- parser/backpressure limits, fixture ownership and no-downgrade rollout behavior.

No Tokio, dependency, crate, codec, transport, Gateway, UI or gameplay runtime change was made. `protocol-oteryn` remains unimplemented and production Auto remains unchanged.

## Validation

Exact final implementation head `8e91cbe379d5173f5e27d369fe5628bea95131e5`:

- CI `30925535134`: PASS, including `CI / Required`;
- Rust Client `30925532657`: PASS, including Windows workspace tests and supply-chain checks;
- independent consumer consistency review: PASS, zero remaining material findings;
- review threads/requested changes: none.

## Final state

```yaml
implementation_status: contract_correspondence_only
user_facing_feature_complete: false
runtime_enabled: false
production_enabled: false
protocol_oteryn_exists: false
protocol_canary_changed: false
blockers: []
next_authorized_work:
  - Rust protocol-oteryn implementation prompt at canonical Platform revision
  - later automatic selection and exact integrated E2E prompt
```
