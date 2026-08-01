---
task_id: OTC2-20260801-playability-p0-assets
status: active
agent: "P0 asset pipeline worker"
lane: otclient-v2
track: greenfield-rust
workstream: playability-p0-assets
phase: validation
branch: docs/OTC2-20260801-playability-p0-assets
base_branch: main
created: 2026-08-01T19:01:00+02:00
updated: 2026-08-01T19:34:00+02:00
last_verified_commit: "fd4a504637063b0108e4840da99bdaa0f45b5c22"
required_base_commit: "17f2a4bf86563609e6f9edb4c71ca40fbbda59b2"
risk: high
related_pr: 142
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-assets.md
  - oteryn-client/docs/research/playability/p0/asset-source-and-rights-matrix.md
  - oteryn-client/docs/research/playability/p0/asset-runtime-import-roadmap.md
shared_path_lease: []
implementation_authorized: false
policy_version: 2
task_kind: discovery
execution_mode: work
context_pressure: high
decomposition_decision: single
validation_level: focused
---

# Goal

Define the smallest legally and technically safe route from approved source inputs to runtime-visible sprites, text and audio, including provenance, importer/runtime boundaries and dependency order.

# Result

The lane produced:

- `asset-source-and-rights-matrix.md` — separate technical, provenance, local-import, redistribution, update-binding and production-approval states for original, third-party, user-owned, server-provided, proprietary and unknown sources;
- `asset-runtime-import-roadmap.md` — dependency-ordered producers for production pack contract, runtime open/verify/index/lookup, logical handles, bounded decode, renderer/text/audio realization, source-family importers and authenticated launcher/update activation.

The current schema/compiler remain explicitly synthetic test infrastructure. The result does not select a production source, infer redistribution rights or turn legacy PR #97 into a Rust runtime/rights contract.

# Scope

Read-only investigation of current asset types/compiler, architecture/operations and legacy operational asset evidence. No asset bytes, proprietary extraction, schema/code/workflow or rights claim was added.

# Acceptance

- [x] every source category has separate technical, provenance, local-import and redistribution status;
- [x] M2-M5 runtime metadata/resource requirements are explicit;
- [x] importer/runtime/signing packages are dependency ordered with sole producers;
- [x] threat boundaries, negative tests and fixture strategy are actionable;
- [x] owner/legal decisions and blockers are explicit;
- [ ] only the three owned paths change and exact-head required validation passes.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T19:34:00+02:00
head: fd4a504637063b0108e4840da99bdaa0f45b5c22
branch: docs/OTC2-20260801-playability-p0-assets
pr: 142
status: validating
context_routes:
  - docs/agents/EXECUTION_PROTOCOL.md
  - docs/agents/CONTEXT_HANDOFF.md
  - oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md
  - oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md
  - oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md
  - oteryn-client/docs/agents/prompts/P0_ASSET_PIPELINE_AGENT.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-assets.md
  - oteryn-client/docs/research/playability/p0/asset-source-and-rights-matrix.md
  - oteryn-client/docs/research/playability/p0/asset-runtime-import-roadmap.md
proven:
  - Current restack target main is 9c03a448457b1715818e094fdfdeade4a1450434.
  - Current asset schema-v1 owns bounded Blob/RGBA8 records, provenance/license text, SHA-256, canonical encoding and strict decode.
  - Current compiler owns strict JSON, bounded capability-rooted no-follow source reads and atomic output preservation.
  - No runtime mount/index/lookup, production importer, signature manifest, renderer/audio/UI handles or approved production source exists.
  - PR #97 is open legacy operational evidence for digest binding and pre-extraction verification, not a Rust or rights contract.
  - The two reports define source decisions, production metadata, threats, fixture policy and a bounded producer sequence.
derived:
  - The safest currently approved source is original project-created synthetic test material only.
  - M2 requires an owner-approved source/rights decision plus exact appearance requirements from PR #140.
  - Runtime consumers must wait for one accepted production pack/logical-handle producer.
unknown:
  - Approved production source, local-import and redistribution policy.
  - Exact Canary/Oteryn appearance and profile metadata.
  - Final UI/font/audio resource choices, pack budgets, signing and release-channel trust.
conflicts: []
first_failure:
  marker: none
  evidence: discovery completed without ownership or technical conflict.
rejected_hypotheses:
  - Treat technical availability as redistribution permission: rejected because rights and provenance are independent gates.
  - Declare synthetic Blob/RGBA8 schema production-ready: rejected because real appearance/text/audio and authenticated runtime contracts are absent.
  - Reuse legacy PR #97 as the Rust asset runtime: rejected because it is legacy operational evidence only.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-playability-p0-assets.md
  - oteryn-client/docs/research/playability/p0/asset-source-and-rights-matrix.md
  - oteryn-client/docs/research/playability/p0/asset-runtime-import-roadmap.md
validation:
  - command: live ownership and launch-gate preflight
    result: PASS
    evidence: PR #97 paths are disjoint/read-only and no shared lease exists.
  - command: exact asset-types/compiler contract review
    result: PASS
    evidence: schema bounds, provenance/license fields, digest/canonical decode, capability no-follow reads and output commit behavior are reflected without stronger claims.
  - command: legal/technical separation and threat-model review
    result: PASS
    evidence: local import, redistribution, remote acquisition, fixture privacy and owner decisions are separately classified.
blockers:
  - Production source/local-import/redistribution approval requires owner/legal decision.
  - Appearance/profile requirements depend on PR #140; release-required resources depend on PR #141/#143.
  - Signing, pack/channel trust and quantitative budgets require later producer/release decisions.
next_action: Run exact-head validation and clean review for PR #142, then merge and archive the asset discovery lane.
```
