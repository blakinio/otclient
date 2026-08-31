# OTC-20260830 local vision-agent supervisor foundation

## Current checkpoint

Owner authorization is complete for **repository-only implementation** using **Subagent-Driven Development**.

Implementation branch:

`feat/OTC-20260830-local-vision-agent-supervisor-foundation`

Stacked Draft implementation PR:

`#810 feat(track-a): local vision agent supervisor foundation`

The implementation branch/PR is intentionally stacked on the owner-approved discovery/design/planning branch / Draft PR #808 so the approved spec and plan are present without prematurely merging #808.

Binding artifacts:

- `docs/superpowers/specs/2026-08-30-local-track-a-vision-agent-supervisor-design.md`
- `docs/superpowers/plans/2026-08-30-local-track-a-vision-agent-supervisor.md`
- `docs/agents/prompts/OTC_20260830_LOCAL_VISION_AGENT_SUPERVISOR_FOUNDATION_SDD.md`
- `docs/agents/prompts/OTC_20260830_LOCAL_VISION_AGENT_SUPERVISOR_FOUNDATION_SDD_ALIAS.md`
- parent Draft PR #808
- implementation Draft PR #810

Invocation alias:

`OTC-LOCAL-VISION-AGENT-SUPERVISOR-FOUNDATION-SDD`

## Fresh verification at execution start

- trusted live `main`: `82bd4ef6d11431a40e47d8eea6fa15f372edcdc4`;
- implementation head at execution start: `0cf3a1302579a5dad2a0de4f331d7f41451dd1d9`;
- parent PR #808 branch head: `3edc3f2a73b9eb9a40a2b5936114e7d9ada62533`;
- isolated worktree: `/workspace/scratch/d0853bfcfb8f/otclient-foundation` on the implementation branch, not `main`;
- PR #810 was created Draft and targets the parent planning branch, not `main`;
- the open PR/branch changed-file inventory showed no competing owner of the planned Control Center, extracted vision, vision benchmark, or foundation-test surfaces;
- current `main` changes since the planning snapshot are disjoint from the planned implementation surfaces;
- no Official Tibia runtime, CUA, credential, login, model, proxy, Docker or service state was modified while opening the implementation lane.

## SDD preflight

The previous execution-environment blocker is resolved by the current Codex worktree and subagent dispatcher. The plan-scoped ledger is:

`.superpowers/sdd/2026-08-30-local-track-a-vision-agent-supervisor/progress.md`

It records the live-state reconciliation, one self-consistency row per Task 1–10, all shared file/interface dependencies, and preflight rulings. The material naming ruling is that PR #790 raw evidence retains `IN_GAME_VISUAL`, while the normalized protocol state remains the spec-defined `WORLD_VISUAL`; both remain visual-only and neither can establish `WORLD_CONFIRMED`.

Clean baseline on the initial implementation head:

- Control Center: 253 tests passed, 2 skipped;
- vision benchmark: 34 tests passed;
- worktree clean after removal of generated Python caches.

No architecture question was open at preflight. No authority expansion occurred.

## Wave 1 implementation checkpoint

Task 1 — reusable PR #790 vision/Ollama safety core:

- implementation `0f2a0927c`;
- required missing-module RED recorded;
- reusable package: 7 tests PASS;
- frozen vision benchmark: 34 tests PASS;
- direct-script `--help`: PASS without provider access;
- independent review: spec compliant / Approved, zero findings.

Task 2 — strict agent protocol:

- implementation `622b466bd`;
- reviewed fixes `bb33609e4`, `b200e5fc1`, `6dc038c08`;
- required missing-module RED plus focused fix-round RED evidence recorded;
- final focused protocol suite: 17 tests PASS;
- final scoped re-review: all findings addressed, no new breakage.

Material protocol rulings are durable in the SDD ledger: raw PR #790 `IN_GAME_VISUAL` remains separate from normalized `WORLD_VISUAL`; the canonical task wire literal is `otclient.local-agent.task.v1`; event payloads preserve the exact declared field while using a recursively immutable, JCS-safe Mapping representation. Task 3 must extend existing persistence privacy and JSON traversal to `Mapping` before storing that representation.

Fresh combined Wave 1 readback on `6dc038c0863db3265cc8354c4cb6167ce0bdda50` passed 7 reusable-vision tests, 17 protocol tests, 34 frozen benchmark tests, and the offline direct-script help smoke. Live `main` advanced to `0b5e473aed4e61f05fc28005f1c0ec9cd99cbf61` through PR #814; its three package-materializer files are disjoint from this implementation.

## Wave 2 implementation and review checkpoint

Published implementation code head:

`28c613e3ae5894dae42e1f9309bf8f9f6398e9c9`

The branch is still based on the approved planning head `3edc3f2a73b9eb9a40a2b5936114e7d9ada62533`. Live `main` was refreshed to `9f79685f6d073c160397eeefdbc2beb27e8921ad`. PR #810 remains Draft. All local Task 3–6 commits were recreated as tree-identical GitHub commits and fast-forwarded through checkpoint parent `29cc136f0f15ff8073eaf24f01c0c9db0b11b1e6`; this record commit follows that parent.

Key published commit mapping:

- Task 3: `56cb9a593`, `e36042193`, `56ff36778`, `812cba560`;
- Task 4 candidate: `d822a1ade`;
- Task 5: `858bb4fba`, `12ce9c5ed`, `7112fa569`, `be2649658`, `4ba8ee61c`, `9c73fce24`;
- Task 6: `cc37f47cd`, `28c613e3a`.

Task 3 — existing-store agent persistence:

- implementation `06c249b08`;
- reviewed fixes `c031a864c`, `fa2de84d0`, `c81b180b5`;
- focused persistence suite: 18 tests PASS;
- Package B regression: 24 tests PASS with the repository's two expected skips;
- final independent re-review: all Important findings addressed, no new findings, clean;
- reuses the existing SQLite/WAL store and shared event ledger; no second database/control plane was added.

Task 5 — exact Qwen sensor and logical model slot:

- implementation `e72c9e26e`;
- reviewed fixes `06f1ca2f4`, `638983278`, `b7ad58477`, `81e5c1f0a`, `8887f7830`;
- final focused/stable suite: 62 tests PASS with one expected real-Windows conditional skip;
- frozen PR #790 benchmark: 34 tests PASS;
- final independent review: both residual findings addressed, no new findings, spec compliant / quality approved / clean;
- no live Ollama/model/runtime/network process was used.

Task 4 — persistent coordinator:

- implementation candidate `d822a1ade` (local SDD equivalent `f6243238a`);
- focused suite: 18 tests PASS; Package A: 76 PASS; Package B: 39 PASS;
- independent adversarial review: Critical 3 / Important 6 / Minor 1, spec non-compliant, fix required;
- reproduced load-bearing failures include effect execution after STOP admission, non-atomic PAUSE/event persistence, and duplicate executor invocation after post-effect persistence failure;
- ordinary durable ledger fixes remain possible inside the existing store, but the frozen `execute(request) -> receipt` contract has no final-commit/cancellation handshake capable of proving STOP dominance and crash-safe exactly-once effect admission.

Task 6 — deterministic visual/runtime reconciliation:

- implementation `cc37f47cd` (local SDD equivalent `2b93f0559`);
- scoped privacy/full-observation fix `28c613e3a` (local SDD equivalent `a65d0afef`);
- focused reconciler: 10 tests PASS;
- full Control Center discovery: 371 tests PASS with 3 skips;
- frozen benchmark: 34 tests PASS;
- independent re-review closed secret-shaped reference retention and incomplete `VisionObservation` validation with no new scoped finding;
- the core finite table is fail-closed for visual-only world state, `STRUCTURAL_ONLY`, conflicts and exit semantics;
- one Important remains: the frozen three-field runtime observation and two-argument reconciler cannot authenticate producer identity, current run/runtime binding or freshness from opaque refs.

## Architecture review packages

`ARCHITECT_REVIEW_REQUIRED`

Task 4 problem:

- Binding public executor contract: `execute(request) -> receipt`.
- Required property: SYSTEM/OWNER STOP must dominate and latch durably; no future physical effect may occur after STOP without explicit OWNER RESUME and fresh reconciliation; effect ambiguity and replay must be crash-safe.
- Conflict: a final effect commit can race STOP after the coordinator's last boolean check, while holding the coordinator lock would starve STOP behind the external executor call. The public protocol exposes no cancellation/final-commit handshake.
- Recommended ruling: retain the frozen base protocol for Null/read-only use, add a reviewed `GuardedBoundedActionExecutor` extension with a one-shot final-commit callback and cancellation handle, refuse effect-capable executors that lack it, and reuse `MutationCoordinator` plus the same SQLite action/budget ledger.
- Alternatives: accept a weaker pre-mark-and-wait semantic that cannot prove STOP request dominance, or keep the phase strictly Null-only and defer effect-capable fake semantics.

Task 6 problem:

- Binding public observation: `RuntimeObservation(state, evidence_class, evidence_refs)` and `reconcile_state(visual, runtime)`.
- Required property: `WORLD_CONFIRMED`/`WORLD_EXIT` require separately reviewed stronger **current** runtime evidence; stale/forged evidence must fail closed.
- Conflict: opaque refs do not authenticate producer, run/runtime identity, observation time, deadline or causal review. Encoding freshness in the ref string would let callers self-assert authority.
- Recommended ruling: preserve the frozen observation wire shape but add a narrow trusted immutable reconciliation context/resolver owned by Control Center; the existing two-argument path remains a safe default that cannot promote without verified context.
- Alternatives: keep confirmed states unreachable in this repository-only phase, or amend the observation protocol with authenticated provenance fields.

The full problem/options/consequence/file packages and every per-agent model/effort/reason entry are durable in:

`.superpowers/sdd/2026-08-30-local-track-a-vision-agent-supervisor/progress.md`

Tasks 7–10 are not dispatched because Task 7 depends on both blocked components. No Critical/Important finding was hidden or adjudicated away.

## Current continuation

The next action is an independent supervising-architect ruling on the two packages above. After rulings, resume the Task 4 and Task 6 RED-to-GREEN fix/re-review loops. Task 7 may begin only after both dependency reviews are clean. PR #810 must remain Draft and unmerged.

## Safety boundary

Throughout this foundation implementation:

```yaml
runtime_access: none
mutation_authorized: false
credentials_allowed: false
login_allowed: false
relogin_allowed: false
character_selection_allowed: false
gameplay_allowed: false
gui_input_authorized: false
process_control_authorized: false
process_memory_access_allowed: false
physical_action_budget: 0
physical_action_count: 0
```

CUA must remain disabled. The production action executor must remain unbound/null. Do not update the stale Package D client promotion fence merely to make physical effects possible.

## Continuation checkpoint — Task 9 architecture boundary

Task 4 and Task 6 were fixed under the supervising architect rulings and re-reviewed clean. Tasks 7 and 8 are clean at `187ff4f1a012195175fe4ba81fdbef60d7727a1e` and `213ec25eb881f596fe2f378280c27da9ae82eb31`.

Task 9 has bounded fake/offline evidence at `b548aded4fdcf273eb77f4e090246589fdc67f00`, `7e60466fa90a3c3a30a0abce509bf01b31428bcb`, and `ecf12922c125afa42bbceb8423f40b3bfbefd376`: foundation audit, Package B audit, 201 focused agent tests (one expected skip), 454 full Control Center tests (three platform skips), and 34 frozen benchmark tests passed at relevant heads. Production authority remains frozen and the executor stays Null/unbound.

### ARCHITECT_REVIEW_REQUIRED

The approved design and Task 9 scenario I require unexpected foreign model residency to transition the persistent session to `WAITING_MODEL_SLOT`; the scheduler currently only raises `ModelSlotUnavailable`. `AgentSessionCoordinator` and `ControlDomainService` expose no owner integration seam. Direct test persistence would be false evidence.

```yaml
Problem: missing durable scheduler-to-session WAITING_MODEL_SLOT transition
Relevant spec: design Local model scheduler / Failure and recovery; Task 9 scenario I
Current implementation: ModelSlotScheduler raises ModelSlotUnavailable only; AgentSessionCoordinator and ControlDomainService expose no owner integration seam
Why normal implementation ruling is insufficient: required repair selects a cross-module session/model ownership contract absent from Task 4/5 public APIs
Options:
  - narrow durable coordinator transition invoked by existing sensor/scheduler failure path
  - defer/amend scenario I to exception-only behavior
  - broader orchestration interface
Recommended option: narrow coordinator transition in existing Control Center
Security/architecture consequence: preserves fail-closed single-slot semantics with no runtime/mutation authority
Consequence if wrong: false session state or accidental second control-plane boundary
Files/interfaces affected: agent_session.py, agent_vision.py, existing tests, possibly ControlDomainService composition
Current PR/head: '#810 Draft; local ecf12922c125afa42bbceb8423f40b3bfbefd376; remote head remains older/unpublished'
```

The reviewer demand to avoid the private fake runtime resolver seam was adjudicated inapplicable: `agent_reconcile.py` explicitly reserves it as the sole test-only injection point while the public two-argument API remains fail-closed. Per the owner anti-loop rule, Task 9 was not sent into a third automatic fix/re-review. Task 10 remains dependent on this decision.
