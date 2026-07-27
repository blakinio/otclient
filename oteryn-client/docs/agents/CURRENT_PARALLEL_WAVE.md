# Current Parallel Agent Wave

Status: accepted launch plan after foundation completion  
Wave ID: `OTERYN-W2-DIAGNOSTICS-EVIDENCE`  
Evidence cut: `main` `acbc78c618e6998fe29d16833f5c907d8ae8d1e8`

Live Git, active task records and open PRs remain authoritative. This document replaces `INITIAL_PARALLEL_WAVE.md` as the launch plan; the initial-wave document remains historical evidence.

## 1. Confirmed transition state

- Foundation implementation PR #54 merged as `7a68f6e7d92eb6b05078bb001e4881d78544a82b`.
- Foundation lifecycle PR #58 merged as `acbc78c618e6998fe29d16833f5c907d8ae8d1e8`.
- Lane W1-F is archived and must not be launched again.
- The W1-F Cargo/lockfile/shared integration lease is released.
- No open PR owns a greenfield Rust product crate, diagnostics contract or Rust workspace integration lease.
- Open PR #48 is an isolated non-merge operational workflow.
- Open PRs #37 and #23 own legacy client paths and do not authorize edits under the Rust product workspace.
- The Canary, asset-input and Windows-platform evidence lanes have no live task/PR owner at this evidence cut.

## 2. Objective

Continue Gate 1 with one small diagnostics/redaction contract package while retaining three useful evidence lanes that do not compete for Rust workspace paths.

The wave uses:

```text
1 coordinator
1 implementation worker
3 isolated evidence workers
```

Maximum active sessions: five including the coordinator.

## 3. Dependency graph

```text
merged oteryn-foundation (#54)
             |
             v
+---------------------------+
| W2-DIAG diagnostics and   |
| secret-redaction contract |
+-------------+-------------+
              |
              v
     reviewed safe contract

Independent evidence lanes:

W2-CP Canary evidence --------> later protocol/domain packages
W2-AR asset evidence ----------> later synthetic asset package
W2-PR Windows evidence --------> later platform/application shell

W2-C coordinates ownership, leases, merge order and task archives.
```

W2-DIAG does not depend on the three research lanes. Research lanes do not edit its crate, Cargo files or public contract.

## 4. Lane W2-C — Coordinator/integrator

Prompt: `prompts/COORDINATOR_AGENT.md`

Responsibilities:

- verify current `main`, active tasks, open PRs and required checks before every lane claim;
- register only non-overlapping worker tasks and draft PRs;
- prevent any relaunch of completed W1-F;
- grant the Rust workspace/shared-path lease only to W2-DIAG in this wave;
- keep research findings as evidence/recommendations rather than accepted product contracts;
- require exact producer/base commits and exact-head CI;
- merge/archive each lane independently through the repository gate;
- close or defer every lane before recommending the next implementation wave.

The coordinator does not implement the diagnostics crate while coordinating.

## 5. Lane W2-DIAG — Structured diagnostics and secret redaction

Prompt: `prompts/NEXT_DIAGNOSTICS_AGENT.md`

Workstream: WS-R14  
Contract role: producer  
Required producer/base:

```text
oteryn-foundation merge: 7a68f6e7d92eb6b05078bb001e4881d78544a82b
foundation archive/main: acbc78c618e6998fe29d16833f5c907d8ae8d1e8
```

Purpose:

- add exactly one `oteryn-diagnostics` crate under `oteryn-client/crates/diagnostics/`;
- define a narrow structured diagnostic-event contract;
- classify fields by safe/sensitive handling;
- enforce redaction when diagnostic values are created, not only at an upload boundary;
- provide deterministic secret-redaction regression tests;
- reuse `oteryn-foundation` only for generic technical time/generation/cancellation primitives when justified.

Required design boundaries:

- standard-library-first; any external dependency requires a fresh version, license, advisory and source preflight;
- no global logger or subscriber installation;
- no `tracing` product integration, sink registry or runtime service composition;
- no filesystem, network, telemetry upload, crash-report upload or support-bundle implementation;
- no replay recorder/runner implementation;
- no protocol packets, authentication values, endpoints, private chat or personal paths in test data;
- no arbitrary untrusted string may silently become a safe diagnostic field;
- public `Debug`/`Display` behavior must not expose values classified as sensitive;
- diagnostics remain optional for correctness and own no authoritative game state.

Expected exclusive path:

```text
oteryn-client/crates/diagnostics/**
```

Expected shared-path lease:

```text
oteryn-client/Cargo.toml
oteryn-client/Cargo.lock
docs/agents/MODULE_CATALOG.md
docs/agents/BUILD_TEST_MATRIX.md
docs/agents/CHANGELOG.md
```

`oteryn-client/tools/architecture-check/**`, its fixtures and Rust CI remain read-only unless the implementation preflight proves a real missing policy rule. The `diagnostics` category already exists in the architecture checker and repository layout, so category bootstrap is not part of the default package.

Acceptance envelope:

- exactly one new production crate;
- bounded, deterministic and secret-safe public contracts;
- focused positive and negative redaction tests;
- no secret-bearing examples or fixtures;
- locked metadata, formatting, Clippy, workspace tests, architecture validation and supply-chain checks pass on the exact final head;
- full diff contains no runtime integrations or unrelated cleanup.

## 6. Lane W2-CP — Canary Current-profile evidence

Prompt: `prompts/CANARY_EVIDENCE_AGENT.md`

Owned paths:

```text
oteryn-client/docs/research/canary-current/**
docs/agents/tasks/active/<canary-evidence-task>.md
```

The lane revalidates exact Canary build/profile/capability and fixture-provenance evidence. It does not add packet constants, product crates, contracts or server changes.

## 7. Lane W2-AR — Asset input/provenance evidence

Prompt: `prompts/ASSET_RESEARCH_AGENT.md`

Owned paths:

```text
oteryn-client/docs/research/asset-inputs/**
docs/agents/tasks/active/<asset-research-task>.md
```

The lane refines safe source/provenance/statistics/import-threat evidence. It adds no real asset bytes, pack schema or compiler implementation.

## 8. Lane W2-PR — Windows platform/dependency evidence

Prompt: `prompts/PLATFORM_RESEARCH_AGENT.md`

Owned paths:

```text
oteryn-client/docs/research/windows-platform/**
docs/agents/tasks/active/<platform-research-task>.md
```

The lane evaluates current primary documentation for window/event/DPI/IME/raw-input/shutdown candidates. It adds no platform/application crate or Cargo dependency.

## 9. Shared-path leases

| Path group | Lease holder | Other lanes |
|---|---|---|
| Cargo workspace/lockfile | W2-DIAG | read-only |
| diagnostics crate/contract | W2-DIAG | no duplicate contract |
| architecture checker/fixtures | none by default | read-only unless a dedicated need is proven |
| Rust CI/toolchain/deny policy | none | read-only |
| Canary research docs | W2-CP | other lanes read-only |
| asset research docs | W2-AR | other lanes read-only |
| Windows research docs | W2-PR | other lanes read-only |
| current-wave coordination docs | W2-C | workers do not edit |

A worker claims a lease only through its active task and live draft PR after a fresh overlap check.

## 10. Merge rules

- W2-DIAG may merge independently of research lanes because it consumes only merged foundation contracts.
- W2-CP, W2-AR and W2-PR may merge in any order once their exact-head documentation checks pass.
- A research finding requiring architecture or shared-contract change stops and becomes a separate ADR/contract recommendation.
- After any shared documentation or producer merge, remaining lanes restack on current `main` and revalidate.
- Every merged lane receives a separate lifecycle archive PR.

## 11. Completion

This wave closes when:

- W2-DIAG is merged/archived or explicitly blocked with preserved evidence;
- the three evidence lanes are merged/archived or explicitly deferred;
- no active task retains an expired shared-path lease;
- the coordinator recommends one next bounded package from actual merged evidence.

Candidate next packages, not yet authorized:

- deterministic test support/fake-time helpers after diagnostics contracts stabilize;
- minimal Windows platform/application shell after W2-PR evidence is reviewed;
- synthetic asset-types/compiler slice after W2-AR evidence is reviewed;
- domain technical storage primitives;
- protocol-core only after domain contracts and exact Canary evidence exist.

## 12. Launch checklist

1. Start one coordinator session with `COORDINATOR_AGENT.md`.
2. Register this current wave and recheck live tasks/open PRs.
3. Launch `NEXT_DIAGNOSTICS_AGENT.md` only when no task owns diagnostics/Cargo/shared integration paths.
4. Launch the three research prompts in separate sessions only when their evidence paths remain unclaimed.
5. Require every worker to create its own task, branch/worktree and early draft PR.
6. Do not assign PR numbers in advance.
7. Let current Git/task state override this evidence cut when repository state changes.
