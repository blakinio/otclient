---
task_id: OTC-20260728-asset-input-evidence
status: completed
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R09
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-AR
parallel_lane_state: archived
branch: docs/OTC-20260728-asset-input-evidence
base_branch: main
created: 2026-07-28T23:43:00+02:00
updated: 2026-07-28T23:55:00+02:00
last_verified_commit: "2e93f124eababc36c898ad4ebd3b54ee9052521c"
required_base_commit: "a6c8d1cfcac9364612c2ac56a9dc12618581adc9"
risk: low
related_pr: "#65"
depends_on:
  - merged foundation audit PR #47
  - merged current parallel-wave plan PR #59
blocks: []
owned_paths:
  - oteryn-client/docs/research/asset-inputs/**
  - docs/agents/tasks/archive/OTC-20260728-asset-input-evidence.md
shared_path_lease: []
contract_role: none
contracts_produced: []
contracts_consumed:
  - accepted asset security/provenance architecture
  - foundation asset and licensing audit
crates_touched: []
features_touched: []
contracts_touched:
  - evidence only; no accepted asset schema or pack contract
modules_touched: []
reuses:
  - foundation asset/licensing audit
  - accepted asset pipeline and security model
public_interfaces:
  - documentation evidence only
cross_repo_tasks: []
performance_evidence:
  - no importer or runtime performance claim
security_evidence:
  - no asset bytes, archives, captures, credentials or private paths
  - importer checklist fails closed on untrusted inputs
---

# Goal

Refine the legal/source/provenance boundary for future Rust asset work, define a content-free inventory schema, record importer threat controls and recommend one synthetic first slice without adding real asset bytes, pack schemas, compiler code or external-repository changes.

# Result

Merged PR #65 delivered:

- `README.md` with evidence labels and durable source/provenance rules;
- `SOURCE_AND_RIGHTS_MATRIX.md` with required rights records and current source/family dispositions;
- `NON_CONTENT_INVENTORY_SCHEMA.md` with deterministic metadata-only inventory and privacy/canonicalization rules;
- `IMPORTER_THREAT_CHECKLIST.md` covering hostile files, archives, media parsers, arithmetic, cancellation, determinism and diagnostics;
- `SYNTHETIC_SLICE_RECOMMENDATION.md` scoping one original 4×4 sprite-sheet/compiler slice with invented IDs and no production pack ABI.

# Material findings

- technical availability/local installation/download does not establish redistribution permission;
- root MIT licensing cannot be extended to unrelated third-party/proprietary content without asset-specific evidence;
- user-local compatibility assets remain blocked on legal/product policy, consent, safe path handling and non-redistribution proof;
- useful counts/dimensions/formats/hashes/compatibility/rights metadata can be retained without content or private paths;
- original synthetic inputs can prove typed metadata, bounds, deterministic transformation, provenance propagation and staged cleanup before official-format blockers are resolved.

# Validation

| Evidence | Result |
|---|---|
| exact six-file/full-content review on `2e93f124eababc36c898ad4ebd3b54ee9052521c` | PASS |
| Rust Client run `30402041989` | PASS: Windows workspace and Supply Chain |
| repository CI run `30402042094` | PASS: scope, syntax/workflow, Lua, analysis and `CI / Required` |
| ready-for-review CI run `30402181054` | PASS: all emitted required jobs; legacy Windows build skipped correctly |
| comments/reviews/unresolved threads | none |
| current base before merge | PASS: main remained `a6c8d1cfcac9364612c2ac56a9dc12618581adc9` |

# Merge

- PR: #65
- exact validated head: `2e93f124eababc36c898ad4ebd3b54ee9052521c`
- squash merge: `39138bb6673be070878225b4f872121ae5d39a6c`
- merged: 2026-07-28

# Boundaries preserved

- no asset bytes, archives, manifests or private directories;
- no legal conclusion beyond evidence; unresolved rights remain blocked;
- no production asset schema/pack/compiler/runtime contract;
- no Cargo, lockfile, CI, architecture, legacy installer or external-repository change;
- no importer/runtime/performance compatibility claim.

# Next action

A future WS-R09 worker should recheck live shared-path leases and implement only the original synthetic slice described by this package, with exact dependency/provenance review and no official/legacy content.

# Completion

- Final status: completed
- PR: #65
- Merge commit: `39138bb6673be070878225b4f872121ae5d39a6c`
- Archived at: `docs/agents/tasks/archive/OTC-20260728-asset-input-evidence.md`
