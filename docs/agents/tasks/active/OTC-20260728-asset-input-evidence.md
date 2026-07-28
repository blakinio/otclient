---
task_id: OTC-20260728-asset-input-evidence
coordination_id: ""
status: awaiting_ci
agent: "GPT-5.6 Thinking"
track: greenfield-rust
workstream: WS-R09
parallel_wave: OTERYN-W2-DIAGNOSTICS-EVIDENCE
parallel_lane: W2-AR
parallel_lane_state: validating
coordinator_task: none
branch: docs/OTC-20260728-asset-input-evidence
base_branch: main
created: 2026-07-28T23:43:00+02:00
updated: 2026-07-28T23:48:00+02:00
last_verified_commit: "b6cb8655d19528c1560519982683942fdd891dda"
required_base_commit: "a6c8d1cfcac9364612c2ac56a9dc12618581adc9"
risk: low
related_issue: ""
related_pr: "#65"
depends_on:
  - merged foundation audit PR #47
  - merged current parallel-wave plan PR #59
blocks:
  - safe selection of the first synthetic asset-types/compiler slice
owned_paths:
  - oteryn-client/docs/research/asset-inputs/**
  - docs/agents/tasks/active/OTC-20260728-asset-input-evidence.md
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
  - repository MIT source license only for code/documentation covered by it
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

# Acceptance criteria

- [x] Required asset families are classified by safe source and rights state without treating technical availability as permission.
- [x] Repository MIT licensing is not incorrectly extended to third-party or proprietary content.
- [x] A content-free inventory schema captures origin, license, hashes, dimensions/counts and compatibility without embedding bytes.
- [x] Importer threat checklist covers bounds, arithmetic, decompression, archives/paths, cancellation, determinism and secret/private-path handling.
- [x] One small synthetic asset-types/compiler recommendation is specific and implementable without freezing official Tibia/Canary formats.
- [x] No real sprite, thing, sound, font, archive, manifest, protocol constant, Cargo, workflow, architecture or external-repository change.
- [x] Exact changed files stay inside the isolated research path and task lifecycle.
- [ ] Exact-head required CI passes; PR merges and archives separately.

# Confirmed context

- Required `main` base is `a6c8d1cfcac9364612c2ac56a9dc12618581adc9`.
- Foundation audit classifies complete distributable game-content rights and exact official 15.25 schema as blocked.
- Root MIT license covers the OTClient software/documentation grant it names; it does not by itself establish redistribution rights for unrelated third-party game assets.
- Open PR #37 concerns the maintained legacy auto-installer and remains blocked on a real-release rehearsal; it does not own Rust asset research paths or authorize Rust reuse of downloaded content.
- PR #48 keeps official Tibia Linux bytes on an isolated NAS and explicitly uploads no binaries/assets; it provides no redistribution authorization.
- No current task or PR owns `oteryn-client/docs/research/asset-inputs/**`.

# Delivered evidence

- `README.md` records evidence labels, rights/provenance conclusions and the implementation boundary.
- `SOURCE_AND_RIGHTS_MATRIX.md` defines required rights records, source classes and per-family current dispositions.
- `NON_CONTENT_INVENTORY_SCHEMA.md` defines deterministic metadata-only inventory fields, canonicalization, rights integration and rejection cases without storing content or private paths.
- `IMPORTER_THREAT_CHECKLIST.md` covers hostile input admission, checked arithmetic, archives/paths, media parsers, determinism, cancellation, execution isolation, diagnostics and required negatives.
- `SYNTHETIC_SLICE_RECOMMENDATION.md` scopes one original 4×4 synthetic sprite-sheet/compiler slice with invented IDs and no official/legacy content or production pack ABI.

# Material findings

1. Technical availability, local installation or successful download does not establish redistribution permission.
2. Root MIT licensing cannot be extended to unrelated third-party/proprietary content without asset-specific evidence.
3. User-local compatibility assets remain blocked on legal/product policy, consent, safe path handling and non-redistribution proof.
4. A useful metadata inventory can be deterministic and content-free: hashes, counts, dimensions, format/compatibility labels and rights references only.
5. The first WS-R09 implementation can prove typed metadata, bounds, deterministic transformation, provenance propagation, staging cleanup and private-path-free diagnostics using only original synthetic inputs.

# Source/evidence review

Reviewed on the required base:

- `oteryn-client/docs/audits/foundation/04-assets-and-licensing.md`;
- `oteryn-client/docs/architecture/ASSET_PIPELINE.md`;
- `oteryn-client/docs/architecture/SECURITY_MODEL.md`;
- root `LICENSE`;
- PR #37 and #48 scope/safety statements as technical evidence only.

No asset bytes, archives, external repositories or private user directories were read or modified.

# Validation

| Revision | Check | Result | Evidence |
|---|---|---|---|
| `a6c8d1cfcac9364612c2ac56a9dc12618581adc9` | live ownership/source preflight | PASS | W2-AR path unclaimed; no real bytes proposed |
| `b6cb8655d19528c1560519982683942fdd891dda` | complete content/scope review | PASS | five evidence docs plus task only; no content/schema/code change |
| final task-record head | exact-head required CI | pending | docs and Rust-governance path checks required |

# Boundaries preserved

- no legal conclusion beyond recorded evidence; unresolved rights remain blocked;
- no scraping, extraction, download or inspection of private user asset directories;
- no content bytes, user-identifying paths, archive manifests or proprietary metadata dumps;
- no accepted production schema/pack/compiler contract;
- no legacy installer behavior or security-policy change;
- no Rust importer/runtime/build/performance compatibility claim.

# Remaining work

1. Pass exact-head required CI.
2. Mark PR #65 ready, inspect full files/diff/comments/reviews/threads/base and squash-merge.
3. Archive this task in a separate lifecycle PR.

# Completion

- Final status: awaiting exact-head CI
- PR: #65
- Merge commit: pending
- Archived at: pending
