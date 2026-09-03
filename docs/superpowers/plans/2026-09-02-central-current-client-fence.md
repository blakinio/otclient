# Central Track A Current Client Fence Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make one strict canonical manifest the only mutable source of the current official-client identity for Track A identity/admission consumers.

**Architecture:** A machine-readable manifest stores the current exact tuple and approved historical reconciliation sources. A strict Python loader supplies typed values to Python, shell, and GitHub Actions consumers; build-specific semantic workflows remain intentionally pinned.

**Tech Stack:** Python 3.12, JSON, Bash, GitHub Actions YAML, unittest, Ruff.

**Spec:** `docs/superpowers/specs/2026-09-02-central-current-client-fence-design.md`

## Global Constraints

- Current fence is `15.32.be4f48 / 52105824 / 552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1`.
- Historical source `15.32.75d4a0 / 52105824 / d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a` remains reconciliation-source-only.
- No login, GUI input, gameplay, process control, memory access, packet payload capture, or semantic promotion is added.
- Exact-build semantic workflows remain build-pinned.
- TDD: failing tests before implementation changes.
- Direct Codex usage remains zero.

---
### Task 1: Canonical manifest and strict loader

**Files:**
- Create: `docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json`
- Create: `tools/tibia_re_control_center/current_client_fence.py`
- Create: `tests/tools/tibia_re_control_center/test_current_client_fence.py`

**Interfaces:**
- Produces `ClientFence`, `current_client_fence()`, `approved_historical_fences()`, `approved_reconciliation_sources()` and CLI `github-env` / `shell`.

- [ ] Write tests for exact schema, current tuple, historical tuple, malformed/extra fields, duplicate history, current-in-history, CLI output.
- [ ] Run focused tests and verify RED because loader/manifest do not exist.
- [ ] Implement frozen typed loader and CLI with strict JSON validation and shell-safe output.
- [ ] Run focused tests and verify GREEN.
- [ ] Commit manifest/loader/tests.

### Task 2: Migrate foundational current-identity consumers

**Files:**
- Modify canonical transition/session/bootstrap/probe scripts.
- Modify `tools/tibia_re_control_center/agent_runtime_admission.py`.
- Modify their current-fence/admission tests.

**Interfaces:**
- Consumes Task 1 typed current fence.
- Produces unchanged legacy constants/API surfaces whose values now originate from the manifest.
- [ ] Add RED guards proving these consumers must equal the manifest and may not embed the current tuple directly.
- [ ] Run focused tests and verify expected failures.
- [ ] Replace duplicated current constants with loader-derived values; shell session resolves the same manifest fail-closed.
- [ ] Run admission/current-fence/governance/bridge/Vision composition regressions.
- [ ] Commit foundational migration.

### Task 3: Migrate read-only workflows and generic reconciliation

**Files:**
- Modify `track-a-surveyor-v2-readonly.yml` and focused operator test.
- Modify `track-a-kasm-canonical-bootstrap.yml`.
- Modify `track-a-canonical-client-fence-reconciliation.yml`.
- Modify reconciliation helper/tests and stable reconciliation contract text.
- Modify current-client/governance workflows as needed to validate central source.

**Interfaces:**
- Workflows load manifest after trusted checkout into job environment.
- Reconciliation accepts only manifest current/history source tuples and still requires fresh exact current probe.

- [ ] Add RED tests for manifest-driven Surveyor/bootstrap and historical-source reconciliation.
- [ ] Verify RED on hardcoded workflows/old two-fence reconciliation.
- [ ] Implement manifest loading and generic approved-history reconciliation without changing guard/atomic/rollback semantics.
- [ ] Run focused workflow, governance, reconciliation, YAML, Ruff, and diff checks.
- [ ] Commit workflow/reconciliation migration.
### Task 4: Promotion guard, governance, PR and live continuation

**Files:**
- Modify `.github/scripts/test_track_a_canonical_current_client_fence.py` to enforce centralization and base-current rotation.
- Modify Package A boundary only with an exact branch/base/repo/path exception if required.
- Create active task record for this centralization.
- Update stable contracts/ADR to point normatively at the manifest rather than a mutable hardcoded current tuple.

- [ ] Add/verify guard that migrated consumers contain no hardcoded current tuple outside manifest/test fixtures.
- [ ] Verify a simulated future manifest promotion requires prior base current in `approved_history`.
- [ ] Run broad affected suites, Track A governance, self-hosted boundary audit, Package A positive/negative matrix, YAML, Ruff and `git diff --check`.
- [ ] Push Draft PR, require terminal exact-head CI, coordinator ACCEPT, then squash merge with expected head SHA.
- [ ] Restack/refresh Wave 2 and Wave 3 only as required by the new trusted main.
- [ ] Run metadata-only canonical reconciliation on Synology runner, then Surveyor fresh admission.
- [ ] Execute the one remaining Vision P2 `view-only capture -> exact Qwen -> reconcile_vision()` run; accept `UNKNOWN/runtime_current=false`; release runtime access to `none`.

## Plan self-review

- Spec coverage: manifest, typed loader, identity consumers, read-only workflows, generic reconciliation, promotion guard, live continuation are all assigned.
- Scope boundary: build-specific semantic workflows and historical evidence are explicitly excluded.
- No placeholders: every task has exact paths/interfaces and validation intent.
- Type consistency: all consumers use `ClientFence`/manifest interfaces from Task 1.