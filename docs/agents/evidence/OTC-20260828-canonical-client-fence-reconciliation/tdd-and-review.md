# Canonical client-fence reconciliation — TDD and review evidence

Date: 2026-08-28

## Scope

This evidence covers the repository-only implementation and review of `client_fence_reconciliation_v1`. It does not claim that the live canonical registration has been reconciled. Live use remains forbidden until this implementation is merged to protected `main`, a separate explicit recovery-admission checkpoint is merged, and the trusted-main workflow revalidates that admission.

## Root cause

The downstream gameWindowState memory-free preflight stopped fail-closed in run `33193448068`, job `98924502254`, at `REGISTRATION_CLIENT_VERSION_MISMATCH`. No target-uniqueness proof, read-only admission, process-memory observation, GUI action or semantic promotion followed that failure.

Repository current authority had already advanced in PR #754 to exact official Linux client:

- version `15.32.75d4a0`
- size `52105824`
- SHA-256 `d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a`

The only approved predecessor in this recovery contract is:

- version `15.32`
- size `52109920`
- SHA-256 `ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8`

Existing `rebind`, same-boot stale-registration recovery and boot-epoch recovery intentionally preserve the registered exact client fence. Adoption requires registration absence and bootstrap must not replace an existing authoritative registration. Therefore no existing reviewed transition could legally repair this mismatch.

## TDD RED — implementation

Exact test/design-only head:

`95a49119f8f8866c9761bcb587ca62719f416dc1`

Workflow run/job:

- run `33195284267`
- job `98930734507` — `Deterministic client-fence reconciliation contract`

Expected result: **FAILURE**.

All nine focused tests reached the intentional pre-implementation assertion:

`AssertionError: canonical client-fence reconciliation implementation missing`

The production helper did not exist at this head. The trusted-main live job was skipped. This establishes a real implementation RED before production code.

## Implementation GREEN

After adding the bounded helper, exact implementation head `97458286ba473b51ef9e8033f330e97bfbc7fe3a` produced the following deterministic results before a workflow-assertion defect:

- 9 new reconciliation tests: PASS;
- 42 existing canonical-transition tests: PASS;
- 10 existing Kasm adoption-probe tests: PASS;
- Track A agent runtime governance: PASS;
- actionlint/YAML validation: PASS.

That job then failed only because the workflow searched for the predecessor fence as one prose line while the contract intentionally represented it as three YAML fields. No implementation test failed.

The assertion was corrected without changing reconciliation semantics. Exact head:

`fe998516ecfd816fb053e0b56158d6aa7f9466e1`

Focused run/job:

- run `33195900581`
- job `98932830802` — **SUCCESS**

Track A governance on the same exact head:

- run `33195900573`
- job `98932830815` — `Fresh admission behavior audit` — **SUCCESS**
- job `98932831016` — `Deterministic admission-policy audit` — **SUCCESS**

The PR-triggered live reconciliation job `98932832051` was **SKIPPED**, as required: unmerged code is never runtime authority.

## Independent admission-review RED

Merge review found a separate authority defect before any live use: the implementation task remained `runtime_access: none`, while the proposed trusted-main workflow would eventually acquire the canonical lease and reconcile registration metadata. A live workflow must not silently expand a `none` checkpoint.

A second test-first head introduced explicit pending `canonical_recovery` admission for the named fence migration without changing production governance:

`e45da7114663d9276ce9225889ae1aa4ae746dea`

Run/job:

- run `33196302067`
- job `98934193806` — expected **FAILURE**

The new `test_pending_client_fence_recovery_is_an_explicit_governance_mode` failed exactly because the then-current global validator required `registration_lease_generation` to be a positive integer and rejected `UNKNOWN` before Gate A. This is the circular dependency being fixed: the current exact-fence transition cannot consume the superseded registration merely to discover its generation.

The companion `test_legacy_canonical_recovery_does_not_gain_unknown_generation_admission` passed at the RED head, proving that the existing recovery class remained fail-closed and that the needed rule should be mode-specific rather than a global relaxation.

## Explicit recovery-admission GREEN

The admission contract and global validator were then extended only for the reviewed mode:

```yaml
runtime_access: canonical_recovery
recovery_mode: client_fence_reconciliation_v1
client_fence_reconciliation_contract: TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_V1
canonical_registration: PRESENT
canonical_lease_generation: UNKNOWN
registration_lease_generation: UNKNOWN
gate_a: REQUIRED_NOT_PROVEN
generation_rebind: NOT_APPLICABLE
gate_b: NOT_APPLICABLE
bootstrap: NOT_APPLICABLE
target_uniqueness: UNKNOWN
mutation_authorized: false
```

Exact GREEN head for that governance/test/workflow boundary:

`3bc47b1442723a9f7e60a5cc5e9c2526ad9550c0`

Run/job:

- run `33196798715`
- job `98935886243` — `Deterministic client-fence reconciliation contract` — **SUCCESS**
- live job `98935887305` — **SKIPPED**

This GREEN includes the focused reconciliation suite, existing canonical transition tests, existing Kasm adoption-probe tests and the Track A runtime governance audit. The legacy canonical recovery path still rejects an UNKNOWN registration generation; the new permission exists only when `recovery_mode: client_fence_reconciliation_v1` and the exact reviewed contract binding are present.

The live workflow now independently validates the exact pending admission from trusted `main` before inspecting the bounded registration-fence decision. Therefore merging the implementation while leaving the task at `runtime_access: none` cannot trigger live recovery successfully. A separate repository-only admission PR is mandatory after implementation merge.

## Reviewed safety properties

The implementation is deliberately a separate recovery subtype rather than a relaxation of any existing canonical transition.

The helper:

- accepts only the closed predecessor fence above;
- accepts only the already trusted current exact target fence;
- requires an active canonical lease for the same task/session with a generation newer than the source registration binding;
- must execute as a finite child of the existing cancellation-safe canonical `guard-run` supervisor and verifies that `coordination.lock` is already exclusively held;
- requires a mode-0600, current-UID-owned, fail-closed `existing_runtime_adoption_v1` predecessor registration with complete singleton inventory and self-consistent fingerprint/window PID binding;
- proves the current exact singleton through the reviewed Kasm adoption probe three times: before staging, before commit and after commit;
- requires stable canonical Docker container name, display, remote-view endpoint and mapping across the transition;
- replaces boot/PID/start/container-instance identity only from fresh current proof;
- increments `registration_generation` by exactly one and binds the record to the active controller `lease_generation`;
- forces `state: UNKNOWN` and cannot retain/promote old in-game semantics;
- performs a mode-0600 atomic write with state-directory fsync;
- may roll back only when the current record is still semantically equal to the transaction's own committed registration;
- emits only bounded dynamic authority markers for concrete controller/registration generations, Gate A and target uniqueness before commit; it does not emit raw PID, raw title, credentials or process memory;
- contains no client process-control, login, GUI/input, ptrace/injection, process-memory observation or gameplay primitive.

The canonical lease manager's existing `guard-run` implementation holds its coordination lock while the child command executes and invokes the child with the lock file descriptor inherited. The reconciliation helper does not introduce a second locking or lease authority.

## Concurrent protected-main movement

While this PR was being developed, protected `main` advanced through independent current-login-field6 work (#758 and #762). Those changes use their own `ephemeral_isolated` lane and do not modify this task's owned paths or canonical registration/lease authority.

Before merge, the reconciliation branch must be clean-restacked on the then-current protected `main`; `base_main` in the active task must be refreshed and all required exact-head checks rerun. Intermediate GREEN heads above are TDD/review evidence only, not final merge authority.

## Final-gate regression repair

The first clean restack onto `main@ab510dea1c02eb6288b3acbb0bd2fb1d89f5b757` produced exact head `13e954d672757e50b1b80bdf98f04849b42549ea`. The dedicated reconciliation workflow and both Track A governance audits were GREEN, but the older current-client-fence workflow failed in run `33199411721`, job `98944789902` after its focused fence/runtime component tests had passed.

The exact failure was not a reconciliation semantic defect. Its governance command was still hard-coded to historical branch `fix/OTC-20260828-canonical-current-client-fence`, so it rejected the correctly bound active task for branch `fix/OTC-20260828-canonical-client-fence-reconciliation`.

A one-line repository-only repair changed that workflow to use trusted pull-request context `GITHUB_HEAD_REF`. Repair PR #765 had exactly one changed file and one replacement line. Its current-fence run `33199585021`, job `98945379663` was **SUCCESS**, including focused fence contract, canonical runtime components, deterministic governance, YAML/diff validation, stale-fence scan and repository-only boundary. CI run `33199585637` also completed **SUCCESS** with `CI / Required` job `98945565798` and actionlint/yamllint success. PR #765 was squash-merged as `009c148a8ba7406acf07c5ce7f95a8f95f69b992`.

This gate repair grants no runtime authority and performs no live action. PR #763 is therefore restacked again on `main@009c148a8ba7406acf07c5ce7f95a8f95f69b992` before final exact-head verification.

## Promotion boundary

Repository GREEN is not live reconciliation success.

The legal sequence after this implementation merges is:

1. create a separate repository-only PR that changes this active task from `runtime_access: none` to the exact pending `client_fence_reconciliation_v1` admission above, with both generation values deliberately `UNKNOWN` and no live action;
2. merge that admission PR after exact-head governance/CI passes;
3. only then post the owner-authored exact `RECONCILE_CANONICAL_CLIENT_FENCE` trigger on #760;
4. accept only `ALREADY_CURRENT`, a complete approved predecessor reconciliation PASS, or a precise fail-closed blocker;
5. after an exact-current `state: UNKNOWN` registration is verified, run `PREFLIGHT_GAME_WINDOW_STATE_QUALIFICATION` again.

No owner login/character/world action is requested until that later memory-free gameWindowState preflight explicitly reports logger readiness.
