# Control Center Package D — real Official Tibia adapter design

Date: 2026-08-23
Task: `OTC-20260823-tibia-re-control-center-package-d`
Status: design approved in chat as option 3; written-spec review pending
Trusted base at design start: `main@6e8ce50a734097363484c6173570eb934d759b83`

## 1. Goal

Implement the first real `OFFICIAL_TIBIA` Control Center adapter without creating a second runtime-authority system and without promoting static Package D PREP assumptions into live authority.

The first executable slice is conditional. `turn` is the preferred candidate; `move` is only a separately proved fallback. Exactly one action family may be promoted in the first runtime slice, and only after fresh current evidence proves its semantic path, external authority, shared input serialization, finite effect bound and authoritative post-effect confirmation.

If any required runtime fact remains `UNKNOWN`, `REQUIRED_NOT_PROVEN`, `REQUIRED_UNAVAILABLE` or equivalent, Package D remains fail-closed. A blocked physical slice is a valid intermediate result; inventing or bypassing authority is not.

## 2. Non-goals

This package does not:

- replace Track A lease, registration, generation rebind, Gate B or whole-lifetime supervision;
- use Control Center `dispatch_gate` as Track A authority;
- expose GUI coordinates, raw key combinations, QMeta IDs, addresses, pointers, opcodes, process IDs, window IDs, display IDs, bridge handles, lease capabilities or credentials through Scenario/ActionRequest/evidence APIs;
- promote all 23 Scenario v1 actions at once;
- infer `IN_GAME`, R/A maturity or target identity from historical evidence;
- bootstrap/login merely to make the Package D task progress;
- create a second logged-in Official Tibia session without separate authority.

## 3. Existing foundations to reuse

Package D is a consumer of the current trusted-base mechanisms:

- `tools/tibia_re_control_center/official_adapter_contract.py` — static fail-closed PREP boundary and exact Scenario-v1 mapping/effect-bound checks;
- `tools/tibia_re_control_center/model.py`, `scenario.py`, `execution.py` — semantic request/result and one-shot Control Center commit semantics;
- `.github/scripts/tibia-official-client-re-canonical-live-lease.py` — authoritative task/session lease state;
- `.github/scripts/tibia-official-client-re-canonical-live-guard.py` — cancellation-safe whole-lifetime coordination flock/supervisor semantics;
- `.github/scripts/tibia-official-client-re-canonical-live-transition.py` — authoritative registration, adoption, generation rebind and Gate B implementation;
- Track A admission/bootstrap contracts and current runtime ownership records.

The Package D PREP evidence remains the starting readiness matrix. Its `UNKNOWN` R/A grades are not live facts.

## 4. Architecture

Package D has four logical boundaries.

### 4.1 Semantic adapter

`OfficialTibiaAdapter` accepts only typed Control Center requests. It reuses Scenario v1 parameter validation and exact finite `EffectBound` validation before any runtime preparation.

Responsibilities:

- identity/capability/runtime-status projection;
- semantic action mapping;
- advisory preflight;
- orchestration of one mutation attempt through the external Track A authority provider;
- typed result and reconciliation normalization.

It never performs raw GUI/process/network operations itself.

### 4.2 Track A authority bridge

A narrow `TrackAAuthorityBridge` adapts the current canonical lease/transition infrastructure to the Control Center execution lifecycle.

It must not copy Track A authority into Control Center state. It provides only a bounded guarded execution transaction for one already-validated action.

The preferred implementation is to extend the existing canonical transition supervisor with a dedicated guarded-dispatch transaction rather than invent another flock/lease implementation. The existing transition supervisor already owns the canonical `coordination.lock`, validates the lease, uses the promoted cancellation-safe subreaper model, and contains the authoritative registration/Gate-B logic.

The guarded-dispatch transaction must keep the canonical coordination flock continuously held across:

1. current lease validation;
2. current registration and Gate-B/target-uniqueness validation;
3. shared GUI/input-lock acquisition;
4. guarded worker READY handshake;
5. Control Center one-shot `commit_dispatch()` decision;
6. exactly one physical effect after COMMIT;
7. immediate authoritative reconciliation needed to classify the effect;
8. worker/descendant exit and safe release.

A fresh lease/generation/registration/identity/cancellation change before COMMIT refuses dispatch. After COMMIT, uncertainty is represented as possible dispatch/ambiguity; there is no blind retry.

### 4.3 Shared GUI/input serialization

Package D PREP could not locate a current reviewed shared GUI/input-lock primitive. Therefore physical dispatch remains blocked until one of these is true:

1. a current existing trusted-base primitive is located, reviewed and reused; or
2. a new canonical input lock is implemented and made normative for Track A GUI mutation actors.

If a new primitive is required, the design uses one fail-closed local filesystem lock in the manager-owned canonical runtime namespace, conceptually `canonical-live-runtime/input.lock`.

Properties:

- exclusive `flock` held by the external guarded-dispatch supervisor, not by Scenario/UI code;
- safe regular file only, mode-restricted, current owner only, symlink/replacement checks;
- no lease or mutation authority semantics of its own;
- bounded/cancellation-aware acquisition;
- never acquired while holding the Control Center local `dispatch_gate`;
- held continuously from before final current GUI target validation through physical effect and the immediate confirmation observation;
- released only by the external supervisor after the guarded attempt terminates.

Until trusted-base governance recognizes this primitive for relevant Track A GUI mutations, the first physical action remains refused.

### 4.4 Semantic action worker and reconciler

The guarded worker receives only a semantic one-action envelope and current non-secret runtime identity material from the authority transaction. It maps that semantic action to the currently proven physical path internally.

The Control Center parent and guarded worker use a strict two-phase handshake:

```text
worker under Track A guard + input lock
  -> READY(action_hash, current_fence_digest)
Control Center
  -> commit_dispatch()
  -> COMMIT or ABORT
worker
  -> on COMMIT: cross exactly one physical boundary
  -> reconcile authoritative effect
  -> RESULT
```

The handshake transport is local and private to the process tree. No raw key/coordinate/handle material is serialized into ActionRequest, Control API requests or durable evidence.

If READY is received but Control Center commit refuses, the worker performs zero physical effect and exits. If COMMIT is sent, the worker must never execute the action more than once even if confirmation times out.

## 5. Why the guarded-dispatch transaction belongs in the existing Track A transition/supervisor layer

Running current `gate-b` before ordinary `guard-run` would leave a race between Gate B and physical dispatch. Running the current transition `gate-b` as a child *inside* `guard-run` would attempt to acquire the same canonical flock again and risks self-deadlock or an invalid authority model.

Therefore the clean seam is a new operation inside the existing canonical transition supervisor. It can reuse `_probe_reg`/registration logic while already owning the canonical flock, then hold that same authority through the action worker. This extends the current authority state machine instead of duplicating it.

The new operation must reuse the guard helper's cancellation-safe child-subreaper behavior and wait for all guarded descendants before releasing serialization.

## 6. Runtime admission phases

### Phase D0 — repository design/tests

```yaml
runtime_access: none
mutation_authorized: false
```

Allowed: code, deterministic tests, fake authority/worker integration, workflow validation. No Official Tibia process/window/session observation.

### Phase D1 — current runtime inventory/admission

Before the first live operation, update the active task with a fresh Track A admission record. The actual class is selected from current state, never assumed:

- registration present and current generation -> candidate `canonical_reuse_or_mutation` only after Gate A/B requirements are freshly satisfied;
- registration present but stale generation -> `canonical_rebind` first;
- registration absent with exactly one current exact client -> `canonical_bootstrap` / `adopt-existing` metadata transition as defined by trusted base;
- registration absent with zero clients -> create-bootstrap is considered only if separately authorized and needed for an independent purpose; Package D does not bootstrap/login merely to manufacture action evidence;
- ambiguous ownership/candidate/session -> refuse runtime access.

### Phase D2 — semantic candidate proof

For `turn` first, prove with current runtime evidence:

- exact current semantic physical path;
- reference UI behavior parity;
- required input lock;
- one bounded effect compatible with Scenario v1 `EffectBound`;
- authoritative before/after confirmation that distinguishes effect from no-effect;
- no hidden additional effect (for example movement when only turning was requested);
- target/window/runtime identity stability across the attempt.

Only after these facts are current may `turn` capability change from unsupported/UNKNOWN to the exact supported grade justified by evidence.

If `turn` fails these gates, it remains unsupported. `move` may be investigated only as a new separately bounded candidate with its own proof; it is not an automatic runtime fallback.

### Phase D3 — one physical E2E

Exactly one first-slice physical effect may be dispatched after all D1/D2 gates pass.

Success requires the full Control Center path, not a manual action:

```text
ActionRequest
-> validate + exact EffectBound
-> reserve budget
-> wait/acquire external Track A guarded-dispatch authority
-> acquire shared input lock
-> final current Gate B/capability/identity checks
-> worker READY
-> commit_dispatch() COMMITTED
-> exactly one physical effect
-> authoritative reconciliation
-> ActionResult CONFIRMED/PASS
```

A manual key press or direct helper invocation does not count as Package D E2E.

## 7. STOP, generations and races

The Control Center local `dispatch_gate` is never held while waiting for Track A authority or input serialization.

If STOP wins before local commit:

- `control_generation` changes;
- pending guarded work becomes stale;
- `commit_dispatch()` refuses;
- worker receives ABORT or loses bounded wait and performs zero effect.

If local durable commit wins:

- budget is already `AT_RISK` / dispatch `POSSIBLY_DISPATCHED`;
- the guarded worker may cross the physical boundary once;
- cancellation/failure afterward cannot be reported as a retryable pre-dispatch failure;
- unresolved outcome becomes `AMBIGUOUS` unless authoritative reconciliation proves the exact result.

Track A lease generation, registration generation, PID/start identity, display/window identity, target uniqueness or adapter generation changes invalidate READY and require a fresh transaction before COMMIT.

## 8. Capability promotion rule

Default Official capabilities remain non-actionable.

A capability may advertise `action_supported=true` only when all of the following are bound to current evidence:

- exact semantic action kind/version;
- current runtime build fence;
- current Track A R/A evidence grade justified by evidence, never guessed;
- current physical semantic path;
- current shared input-lock requirement;
- current authoritative confirmation source;
- required state predicate (for example a separately proven active-world state if needed);
- current adapter generation.

Capability publication is evidence-derived status only. It still does not grant authority to a future action.

## 9. Error model

Pre-dispatch typed refusals include at minimum:

- runtime not admitted;
- Track A lease/registration/Gate B/rebind requirement not satisfied;
- shared input lock unavailable/untrusted;
- semantic action path not proven;
- authoritative confirmation unavailable;
- runtime/adapter/control generation changed;
- target identity not unique/current;
- effect-bound or action-hash mismatch;
- Control Center STOP/recovery/budget/commit refusal.

After local dispatch commit, failures must preserve possible-dispatch semantics. No result path may relabel an uncertain committed action as `NOT_DISPATCHED`.

## 10. Security and privacy

- Lease capability contents remain outside Control Center domain objects and durable artifacts.
- Credentials/session secrets are not required by the adapter action API and are never passed to the semantic worker.
- Raw physical mappings remain implementation-private and may be persisted only as sanitized evidence that does not expose secret/session material or unstable raw runtime handles.
- Runtime evidence stores hashes/stable provenance rather than character-bearing window titles or framebuffer dumps unless a separately approved artifact policy allows them.
- No remote network listener is required for the guarded handshake; use parent/child standard streams or another local task-private IPC primitive.

## 11. Planned implementation boundaries

Initial producer paths after written-spec approval:

- `tools/tibia_re_control_center/official_adapter.py` — semantic adapter and injected authority/transport/reconciler interfaces;
- `tests/tools/tibia_re_control_center/test_package_d_official_adapter.py` — TDD contract/integration tests;
- `.github/scripts/tibia-official-client-re-canonical-live-transition.py` — guarded-dispatch extension only if no equally safe existing primitive is found;
- matching transition tests;
- `.github/scripts/tibia-official-client-re-input-lock.py` plus deterministic tests only if no existing reviewed shared input lock is found.

`official_adapter_contract.py` remains the static PREP baseline and should not be weakened. Production enablement composes on top of it.

Shared `MODULE_CATALOG.md`, `CHANGELOG.md` and normative contracts are not pre-claimed. Revalidate live ownership immediately before any required edit and serialize/defer on overlap.

## 12. Testing strategy

### Deterministic/TDD

Write failing tests before implementation for:

1. unsupported-by-default Official capability state;
2. semantic/effect-bound/hash validation before authority work;
3. no physical worker start when admission/preflight fails;
4. external authority wait occurs outside local `dispatch_gate`;
5. input lock required before READY;
6. final Gate B/current identity validation occurs under the external guard;
7. STOP/control-generation change between READY and commit produces zero effect;
8. local commit refusal produces zero effect;
9. COMMIT can produce at most one worker effect;
10. post-COMMIT timeout/failure becomes possible-dispatch/AMBIGUOUS unless reconciled;
11. action transport never leaks raw mapping/runtime handles into public result/evidence structures;
12. guarded-dispatch supervisor retains coordination and input locks across worker descendants/cancellation;
13. stale lease/registration generation refuses before physical boundary;
14. direct invocation of the raw worker without the guarded transaction refuses or has no mutation capability;
15. exact first-slice capability cannot be enabled without an evidence-backed promotion record.

### Repository fake E2E

Use fake lease/registration/probe/input-lock/worker/reconciler providers to prove the complete two-phase path through Control Center commit without any Official Tibia access.

### Fresh independent validation

Run exact-head repository CI plus the relevant existing fresh deterministic audit/falsification path. Any new Track A transition primitive receives its own deterministic cancellation/lock/identity tests.

### Physical E2E

Run only after fresh Track A admission and current first-slice semantic proof. Physical E2E performs one bounded action through the Control Center API/domain path and records sanitized authoritative before/after evidence.

## 13. Acceptance criteria

Package D first slice is complete only when:

- a real `OfficialTibiaAdapter` exists and remains fail-closed by default;
- Track A authority is reused rather than duplicated;
- a reviewed shared GUI/input serialization primitive is in force;
- exact current Gate B/identity checks occur under continuously held external authority;
- Control Center one-shot commit occurs after READY and immediately before the physical boundary;
- exactly one action family has current evidence-backed promotion;
- one physical E2E through the real Control Center path is `CONFIRMED/PASS` on the exact current runtime, or the task explicitly terminates blocked without falsely claiming the slice;
- STOP/generation/ambiguity semantics pass deterministic race tests;
- no raw transport/runtime secrets or handles leak across the semantic boundary;
- exact-head required CI and fresh audit are green;
- lifecycle evidence/task archive accurately records runtime admission, action evidence, result and nonclaims.

## 14. First implementation decision after spec approval

Start TDD at `runtime_access:none` and build the semantic adapter + fake guarded-dispatch protocol first. In parallel with no runtime access, inspect current trusted-base Track A mutation paths for an existing shared GUI/input lock. Only after deterministic boundaries are green and repository ownership is revalidated should the task update its admission record and attempt current physical runtime admission.
