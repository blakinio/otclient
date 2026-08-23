# OTC-20260823 — Control Center Package D PREP evidence

## Terminal scope

This evidence closes only `OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-D-PREP`.

- implementation merge: PR #668 -> `292767ed19856f75be0c6e297bc7567013ee8f54`
- task authority: `runtime_access:none`, `official_client_access:false`, `mutation_authorized:false`, `credentials_allowed:false`, `login_allowed:false`, `gameplay_allowed:false`, `network_listener_allowed:false`
- no Official Tibia process/container/window/display/memory/session, KasmVNC/Remote Desktop surface, canonical live lease/registration, Gate A/B, bootstrap/rebind, login, credential, network listener, or physical gameplay operation was performed by this task
- physical Official Tibia E2E: `NOT_APPLICABLE_WITH_REASON` — real Package D runtime authority is explicitly outside PREP
- future real Package D remains a separately admitted runtime task

## Delivered repository boundary

`tools/tibia_re_control_center/official_adapter_contract.py` is a hard-disabled typed preparation boundary. `AdapterKind.OFFICIAL_TIBIA` identity grants no capability or authority. Static capabilities have `read_supported=false` and `action_supported=false`; runtime/client state is `UNKNOWN`, authority is `NOT_ADMITTED`, freshness is `UNKNOWN`; optimistic reported state is diagnostic only; `execute()` always refuses with `OFFICIAL_RUNTIME_NOT_ADMITTED`.

`tests/tools/tibia_re_control_center/test_package_d_prep.py` proves the repository-only path from semantic `ActionRequest` through mapping/preflight to deterministic refusal. It also proves that raw transport/runtime handles are not exposed, exact Scenario v1 `EffectBound` is revalidated, optimistic `MUTATION_ALLOWED` cannot enable mutation, and the skeleton has no coordinator physical-dispatch surface or runtime/raw-dispatch dependency imports.

## Track A reuse map — source-backed, reuse never replace

| Concern | Current durable source inspected | D-PREP disposition |
| --- | --- | --- |
| coordination lease / canonical authority coordination | `.github/scripts/tibia-official-client-re-canonical-live-lease.py` | `SOURCE_PRESENT_REUSE_LATER`; coordinates fail-closed authority only; D-PREP did not execute or import it |
| whole-lifetime external guard / supervisor | `.github/scripts/tibia-official-client-re-canonical-live-guard.py` | `SOURCE_PRESENT_REUSE_LATER`; guarded command and descendants remain under the external guard; D-PREP did not execute it |
| canonical registration identity | `.github/scripts/tibia-official-client-re-canonical-live-transition.py` (`runtime-registration.json` schema and `_probe_reg`) | `SOURCE_PRESENT_REUSE_LATER`; current identity must be revalidated by a future admitted runtime worker |
| registration generation rebind | `.github/scripts/tibia-official-client-re-canonical-live-transition.py` (`_rebind`) | `SOURCE_PRESENT_REUSE_LATER`; D-PREP did not rebind or mutate registration |
| Gate A | `docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md` plus current-lease validation mechanisms above | `CONTRACT_PRESENT_CURRENT_RUNTIME_RESULT_UNKNOWN`; no static promotion to PASS |
| Gate B / target uniqueness | `.github/scripts/tibia-official-client-re-canonical-live-transition.py` (`_gateb`, `_probe_reg`, candidate uniqueness checks) | `SOURCE_PRESENT_REUSE_LATER`; no Gate B invocation in D-PREP |
| GUI/shared input lock | required by `TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`, `TIBIA_RE_CONTROL_CENTER_EXECUTION_V1.md`, and `TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md` | `UNKNOWN_NOT_LOCATED_IN_CURRENT_STATIC_REUSE_SURFACE`; future runtime adapter must resolve/acquire the current required input lock before any mutation candidate can become ready |
| runtime bridge | `tools/tibia_runtime_bridge/**` exists on `main@292767ed19856f75be0c6e297bc7567013ee8f54` | `READ_ONLY_REUSE_SURFACE`; D-PREP introduces no import/call into it and makes no capability claim from its mere existence |
| capability/readiness/evidence registry | `tools/tibia_re_control_center/model.py`, Scenario/Adapter contracts, plus current Track A evidence contracts | `CURRENT_OFFICIAL_PRODUCER_UNVERIFIED`; all live R/A grades remain `UNKNOWN` |
| result/evidence confirmation | `tools/tibia_re_control_center/execution.py`, `model.py`, `TIBIA_RE_CONTROL_CENTER_ARTIFACT_V1.md`, `TIBIA_RE_CONTROL_CENTER_ADAPTER_V1.md` | generic result semantics exist; Official Tibia authoritative post-effect producer is `UNKNOWN_REQUIRES_CURRENT_AUTHORITATIVE_RECONCILIATION` |

The Control Center local `dispatch_gate` is only a local one-shot serialization/commit mechanism. It is **not** Track A authority and must never be held while waiting to acquire external Track A authority/guards.

## Required future physical-dispatch order

A future separately admitted Official Tibia runtime adapter must preserve this order:

1. semantic validation plus exact finite `EffectBound`;
2. reserve Control Center external-effect budget;
3. acquire the **current external Track A authority/whole-lifetime guard**, without holding the local Control Center `dispatch_gate` while waiting;
4. acquire the current required GUI/shared input lock;
5. perform final current Track A registration identity, lease/generation, Gate/capability/authority and target-uniqueness checks;
6. call Control Center one-shot `commit_dispatch()`;
7. only if committed, perform exactly one bounded physical effect while continuously holding the same external Track A guard and required input lock;
8. obtain current authoritative post-effect reconciliation/confirmation;
9. conservatively update budget/result/evidence and classify ambiguity as possible dispatch rather than retrying blindly.

If STOP/control-generation changes while waiting for external authority or input locks, or any registration/lease/generation/identity/capability/authority fact changes, the waiting work is stale and must be invalidated before commit. Cached `MUTATION_ALLOWED` is never authority.

## Scenario v1 Official action readiness matrix

Static source presence does not promote current Track A maturity. Therefore every current action family is deliberately `R=UNKNOWN`, `A=UNKNOWN`; UI parity, exact Track A semantic path, per-action input-lock requirement, and current authoritative confirmation remain unverified by this `runtime_access:none` task. `EffectBound=yes` means only that the current Scenario v1 code provides an exact finite bound after semantic validation.

| action_kind | required capability | R | A | reference UI | Track A semantic path | finite EffectBound | GUI/shared input lock | post-effect confirmation | first real slice |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| move | move | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| turn | turn | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| stop_movement | stop_movement | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| say_controlled_text | say_controlled_text | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| cast_spell | cast_spell | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| use_consumable | use_consumable | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| eat_food | eat_food | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| use_rune | use_rune | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| select_target | select_target | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| attack | attack | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| cancel_attack | cancel_attack | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| follow | follow | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| cancel_follow | cancel_follow | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| open_container | open_container | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| close_container | close_container | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| use_item | use_item | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| look_item | look_item | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| move_item | move_item | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| equip | equip | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| unequip | unequip | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| open_panel | open_panel | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| close_panel | close_panel | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |
| logout | logout | UNKNOWN | UNKNOWN | unknown | unmapped/current evidence required | yes | UNKNOWN | current authoritative reconciliation required | no |

Common evidence: `tools/tibia_re_control_center/scenario.py:ACTION_KINDS`, `validate_action_parameters`, and `default_effect_bound`; `docs/agents/programs/OTCLIENT_TIBIA_RE_EXPERIMENT_EXECUTION_MODEL.md`; current Track A admission/execution contracts. Common gaps are current R/A revalidation, reference UI parity, admitted semantic Track A action path, per-action GUI/input-lock requirement, and authoritative per-action confirmation.

`FIRST_REAL_SLICE=NO_ACTION_CANDIDATE_READY`.

## Validation, audit and E2E evidence

### TDD red

- head `b42e1956eae85d3618d26bb6776eaacdce590d0c`
- Package A deterministic runner executed 122 pre-existing tests successfully before failing only because `tools.tibia_re_control_center.official_adapter_contract` did not yet exist (`ModuleNotFoundError`)
- this established the intended red contract before implementation and showed no pre-existing core regression

### Exact implementation head

Head: `86556d290173d311f962c8fe3ae30224fb15cd80`.

- `TIBIA RE Control Center Package A` run `32635227212`: `SUCCESS`
- `Package A deterministic core` job `97183844519`: `133/133` tests PASS, including 12 D-PREP tests; `PACKAGE_A_MANDATORY_TESTS=65/65`; `RUNTIME_ACCESS_NONE=PASS`; Ruff PASS; `git diff --check` PASS
- general `CI` run `32635227340`: `SUCCESS`
- changed implementation paths: exactly `tools/tibia_re_control_center/official_adapter_contract.py` and `tests/tools/tibia_re_control_center/test_package_d_prep.py`

### Fresh post-implementation deterministic audit

Validator: pre-existing GitHub Actions `Fresh Package A falsification audit`, clean GitHub-hosted runner, job `97183844602`, run `32635227212`. The audit ran in an independent execution context with read-only repository token and no implementation authority. This is a deterministic CI validator, not a claimed human/model review.

Results on the final implementation head/merge ref:

- `PACKAGE_A_CHANGED_PATHS=2_DECLARED_ONLY`
- `PACKAGE_A_FRESH_AUDIT=PASS`
- `MATERIAL_FINDINGS_OPEN=0`
- `RUNTIME_ACCESS_NONE=PASS`
- `FAKE_ONE_STEP_E2E=PASS`
- STOP/cleanup/reset overlap fence PASS
- post-final-hook dispatch recheck PASS
- canonical action hash guard PASS
- artifact/scenario privacy gates PASS
- final-gate abort/revalidation PASS
- callback identity/reconciliation fences PASS
- mutation-run admission serialization PASS

D-PREP-specific acceptance is additionally falsified by the 12 D-PREP tests in the clean deterministic-core runner, including no capability advertisement, optimistic-status refusal, exact EffectBound validation, semantic/raw boundary enforcement and absence of physical dispatch methods/imports.

### Repository-only E2E

`ActionRequest -> validate/map -> preflight -> OFFICIAL_RUNTIME_NOT_ADMITTED`, with an explicitly optimistic synthetic runtime status, PASS. The adapter has no physical dispatch surface and `execute()` deterministically refuses. Therefore zero physical Official Tibia effects are possible through the delivered PREP class.

Physical Official Tibia E2E is `NOT_APPLICABLE_WITH_REASON`: PREP explicitly forbids runtime access and real Package D execution.

## Shared-index ownership decision

Fresh revalidation immediately before the would-be shared-index edit found active Draft PR #23 changes both:

- `docs/agents/MODULE_CATALOG.md`
- `docs/agents/CHANGELOG.md`

The canonical D-PREP prompt requires serialization/defer on overlap. These edits are therefore recorded as `DEFERRED_EXISTING_OWNER_PR_23`; D-PREP did not modify or steal ownership of either shared file.

## PR lifecycle

- PR #665 — task claim — merged as `cc9d5f5b9cb0b2a9d1b55fe86a129551f3eaee63` after exact-head `CI` and Track A governance PASS
- PR #667 — shared-path claim correction — merged as `f4295d618b6e86ac8135eb9aba461c506b5e29e2` after exact-head checks PASS
- PR #668 — implementation — exact final head `86556d290173d311f962c8fe3ae30224fb15cd80`, zero PR comments/threads at readiness, required checks PASS, merged as `292767ed19856f75be0c6e297bc7567013ee8f54`
- closeout PR — docs/evidence/archive only; terminal SHA/check evidence is recorded in the archived task after this closeout PR reaches terminal state

## Audit findings

No critical/high/material-medium finding remains open for the delivered PREP scope. The following are deliberate future-admission gaps, not claims of readiness: current Track A R/A grades, exact GUI/shared input-lock implementation path, reference UI parity, per-action semantic Track A dispatch path, and authoritative Official Tibia post-effect confirmation producer. They force `NO_ACTION_CANDIDATE_READY` and cannot enable mutation.
