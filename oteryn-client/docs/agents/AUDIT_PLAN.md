# Foundation Audit Plan

Status: mandatory Gate 0 before production workspace bootstrap.

## 1. Audit objective

Establish verified inputs for the greenfield Rust client without allowing the current OTClient implementation to dictate the target architecture.

The auditor answers:

- what behavior must be supported first;
- what exact Canary contract exists;
- what Oteryn Identity/session contracts exist;
- which assets can legally and technically be used;
- what performance baseline and target hardware apply;
- which assumptions remain unknown;
- what smallest implementation package can start safely.

The auditor does not implement production client code.

## 2. Evidence levels

Every finding is labeled:

- `PROVEN`: verified from source, contract, test or exact runtime evidence;
- `SUPPORTED`: multiple consistent indicators but missing one required proof;
- `INFERRED`: reasonable interpretation, explicitly non-authoritative;
- `UNKNOWN`: insufficient evidence;
- `BLOCKED`: required evidence is inaccessible or requires another repository/environment;
- `REJECTED`: investigated hypothesis contradicted by evidence.

File timestamps and comments alone are low-trust. Current source, exact contracts and runtime/fixture evidence take precedence.

## 3. Required audit outputs

Create under `oteryn-client/docs/audits/foundation/`:

```text
README.md
01-product-and-feature-inventory.md
02-canary-compatibility.md
03-oteryn-identity-and-session.md
04-assets-and-licensing.md
05-performance-baseline.md
06-platform-and-hardware.md
07-test-and-fixture-inventory.md
08-risk-register.md
09-gap-and-decision-log.md
10-bootstrap-recommendation.md
```

Supporting machine-readable inventories may use JSON/TOML under `oteryn-client/docs/audits/foundation/artifacts/` when schemas are documented.

## 4. Product and feature inventory

Inventory user-visible and engine-critical behavior from the legacy client and intended Oteryn product.

Classify each item:

```text
minimum playable
required before beta
post-beta
not planned
unknown contract
```

At minimum cover:

- authentication and account state;
- character/world/gameplay-channel selection;
- map and movement;
- creatures, appearances and effects;
- combat target/state;
- inventory/equipment/containers;
- chat;
- battle list;
- minimap;
- action bars/hotkeys/cooldowns;
- settings/layout/accessibility;
- audio;
- reconnect/relog/logout;
- updater/assets/diagnostics;
- major modern server-driven features.

Record behavior, not legacy module structure.

## 5. Canary compatibility audit

Identify the exact initial Canary revision or candidate range.

For each minimum-playable message family record:

- producer source path and commit;
- opcode/schema/message identifier;
- direction;
- field order, widths, signedness and optional values;
- version/feature gate;
- login/session requirements;
- existing legal fixture/test evidence;
- unsupported/unknown behavior;
- candidate normalized `GameEvent`/`GameCommand` mapping.

Do not copy assumptions from another client fork without Canary proof.

Output a compatibility matrix and a prioritized fixture acquisition plan. Never commit live credentials or proprietary packet captures.

## 6. Oteryn Identity and session audit

Verify current contracts for:

- Authorization Code + PKCE;
- loopback callback;
- account/token lifetime;
- character/world/gameplay-channel directory;
- one-shot game-ticket issuance;
- authoritative routing;
- game-session/resume semantics;
- relog between gameplay channels;
- supported/unsupported combinations;
- rollout order with Canary and future Oteryn.

Separate proven current contracts from desired future architecture. Server implementation details are out of client scope unless required to define a client contract.

## 7. Asset and licensing audit

Inventory required types, formats, counts, dimensions, animation semantics, fonts, sounds and shaders.

For each source class record:

- provenance;
- redistribution/modification rights;
- whether bytes may enter the repository;
- importer requirements;
- runtime conversion requirements;
- known identifiers/mappings;
- security/parser risks.

Create an explicit prohibited-material list. Do not copy proprietary assets into audit fixtures.

## 8. Performance baseline audit

Define reproducible legacy/reference scenes and capture available evidence for:

- frame-time distribution;
- CPU/GPU utilization;
- memory;
- draw calls/instances where observable;
- startup and asset loading;
- dense combat/town/UI cases;
- repeated relog and long-session behavior.

When runtime measurement is unavailable, define the exact measurement procedure and mark results blocked. Do not invent performance numbers.

Recommend minimum, recommended and high-refresh Windows hardware tiers with evidence or leave them unresolved.

## 9. Platform/dependency audit

Evaluate candidate Rust dependencies through primary documentation and current versions at audit time. Candidates include, but are not automatically selected:

- `wgpu`;
- `winit`;
- async runtime/network stack;
- audio backend;
- text shaping/font stack;
- image/audio compression;
- WebAssembly runtime;
- tracing/crash integration.

Record license, maintenance, Windows support, unsafe/FFI surface, binary size and architecture fit. Final dependency choices require bootstrap/package decisions, not popularity alone.

## 10. Test/fixture inventory

Identify reusable legal evidence:

- current synthetic protocol fixtures;
- test builders and fake services;
- map/item/entity behavior tests;
- login/session negative cases;
- UI flows;
- benchmark scenes;
- asset metadata.

Legacy C++ test infrastructure may inform expected behavior but is not linked into the Rust workspace.

## 11. Risk register

Cover at least:

- incorrect Canary assumptions;
- asset rights/provenance;
- greenfield scope expansion;
- renderer/UI overengineering;
- protocol/domain leakage;
- performance claims without fixtures;
- authentication/ticket replay;
- relog/reconnect lifecycle races;
- dependency/supply-chain risk;
- absence of Windows GPU/runtime CI;
- parallel-agent contract conflicts;
- premature native Oteryn protocol design.

Each risk has likelihood, impact, mitigation, owner/workstream and gate.

## 12. Bootstrap recommendation

The final audit document recommends exactly one first implementation package, with:

- workstream;
- owned paths;
- prerequisite evidence;
- concrete artifacts;
- acceptance tests;
- explicit non-goals;
- unresolved blockers.

Expected default recommendation is a narrow workspace/toolchain foundation package, but the auditor must follow evidence.

## 13. Audit acceptance

The audit is accepted only when:

- all required documents exist;
- findings are evidence-labeled;
- exact Canary/Oteryn unknowns are not disguised as decisions;
- no proprietary assets/secrets are added;
- legacy source is treated as evidence, not architecture;
- architecture deviations are proposed through ADRs;
- open PR/task overlaps are documented;
- the bootstrap recommendation is narrow and executable;
- complete diff and documentation checks pass.
