# Central Track A Current Client Fence Design

## Goal

Replace duplicated active current-client identity constants with one strict machine-readable canonical fence source. A weekly official-client update should change the approved fence in one place, while identity/admission consumers follow it automatically and build-specific semantic evidence remains pinned.

## Scope

The canonical source is `docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json`.
It owns only official native-Linux client identity: version, executable size, and SHA-256.
It does not authorize login, GUI input, gameplay, process control, memory reads, network payload capture, or semantic promotion.

Historical evidence, archived tasks, and exact-build reverse-engineering workflows remain immutable/build-pinned. They are not migrated merely because their files contain an older SHA.

## Manifest

Schema version is `1`. The document contains exactly:

- `schema_version`
- `current`
- `approved_history`

Each fence contains exactly `version`, `size`, and `sha256`.
`current` is the only fence accepted for new/current live identity.
`approved_history` contains earlier canonical current fences that may be accepted only as metadata-reconciliation sources. The current tuple must not also occur in history; duplicate history tuples are invalid.

Initial current fence:
`15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.

Initial approved history includes at least the immediately superseded canonical fence:
`15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`.

## Loader

Create `tools/tibia_re_control_center/current_client_fence.py` with a frozen `ClientFence` value type and strict manifest loader.

Public interfaces:

- `current_client_fence() -> ClientFence`
- `approved_historical_fences() -> tuple[ClientFence, ...]`
- `approved_reconciliation_sources() -> tuple[ClientFence, ...]` returning current plus history
- CLI `github-env <path> [--prefix NAME]` for workflows
- CLI `shell [--prefix NAME]` for shell consumers

Malformed/missing/extra fields, invalid size, invalid SHA, unsafe or missing current provenance, duplicate history, or current-in-history fail closed.
## Consumers

Migrate only identity/admission consumers that are expected to follow the official current client:

- canonical live transition/session/bootstrap/existing-runtime probe;
- canonical runtime admission library;
- canonical current-client validation/governance;
- Kasm canonical bootstrap identity checks;
- Surveyor v2 read-only identity checks;
- canonical client-fence reconciliation.

Tests for these consumers must derive the current tuple from the manifest rather than restating it.

Do not migrate exact-build semantic workflows whose correctness depends on offsets, QMeta/vptrs, protocol layouts, helper binaries, or other build-specific evidence. An old fence in such a workflow remains intentional until that semantic lane is separately revalidated.

## Reconciliation

Canonical client-fence reconciliation accepts a source registration only when its exact `(version, size, sha256)` tuple is in `approved_reconciliation_sources()`.

A fresh approved probe must still prove exactly `current` before commit. Existing namespace/display/remote-view binding, lease generation, three-probe stability, atomic replacement, fsync, rollback, and fail-closed behavior remain unchanged.

This allows a stale registration to skip one or more weekly releases only if every source fence involved was previously canonical and retained in approved history.
## Weekly promotion rule

A future current-client promotion changes the manifest instead of editing each consumer. CI must verify that:

1. the manifest is structurally valid;
2. all migrated identity/admission consumers reference the loader/manifest and do not hardcode the current tuple;
3. if `current` changes relative to the PR base, the old base `current` appears in the new `approved_history`;
4. the new current exact tuple is still independently established by the ordinary official-client provenance lane;
5. no history entry gains current-runtime authority merely by being listed.

## Safety invariants

- Manifest identity is data, not authority.
- Current fence acceptance never grants actions.
- Historical fence acceptance is reconciliation-source-only.
- Semantic runtime evidence remains separately reviewed and freshness-bound.
- Build-specific reverse-engineering evidence never auto-promotes across versions.
- Manual edits of durable runtime registration remain forbidden.
- Missing or malformed manifest fails closed.

## Acceptance

The change is complete when all migrated consumers resolve the same current tuple from the manifest, the stale-registration reconciliation can advance the observed `d1a168...` registration to exact current `552dcf...` without touching the client process, Surveyor can then issue fresh read-only admission, and Vision P2 can finish its remaining capture/Qwen/reconciliation gate with `UNKNOWN` acceptable.