# UNKNOWN remote-view mapping repair

Date: 2026-08-28

## Live failure

The first trusted-main reconciliation attempt ran as workflow `33200286357`, job `98947751420`, from `main@79279315df2975e79558a15192e4c5c87b90194a` after the explicit recovery admission in #766.

It passed:

- pending recovery admission;
- deterministic pre-runtime verification;
- bounded registration decision `RECONCILE`;
- canonical lease acquisition and validation at live controller generation `40`;
- Gate A.

It then failed closed with:

```text
TRACK_A_CANONICAL_CLIENT_FENCE_RECONCILIATION_ERROR=source_registration_remote_mapping_invalid
```

The final registration verification step was skipped and no reconciliation PASS marker was emitted. The source registration was rejected before any registration commit. No process-memory observation, client mutation, GUI/input, login, credentials or gameplay action occurred.

## Root cause

The reconciliation helper required the predecessor registration to have:

```text
remote_view_mapping == PROVEN
```

That is stricter than the pre-existing canonical schema. `tibia-official-client-re-canonical-live-transition.py` accepts both `PROVEN` and `UNKNOWN` for `remote_view_mapping`.

The historical predecessor Kasm adoption probe at pre-#754 base `785d888e8392e32c8ba852d6db7c8de03db9d8be` emitted:

```yaml
remote_view_endpoint: https://synology:6902/
remote_view_mapping: UNKNOWN
```

The current exact Kasm adoption probe emits the same endpoint and the same `UNKNOWN` mapping. The v1 reconciliation contract requires continuity/equality of endpoint and mapping; it does not require a `PROVEN` mapping.

Therefore the live failure exposed an implementation-only overconstraint, not missing runtime evidence.

## TDD RED

Repair PR: #767

Exact RED head:

`9c0505ce184ebca402e94d0e6caef2bb7036974a`

Workflow run/job:

- run `33200847818`
- job `98949632562` — `Deterministic client-fence reconciliation contract` — expected **FAILURE**

Result: 14 focused tests ran; 13 passed and exactly the new regression test
`test_reconciles_when_stable_remote_view_mapping_is_unknown` failed at `_base_registration()` with `source_registration_remote_mapping_invalid`. The invalid-value safety test passed and the live PR-event job was skipped.

## Minimal GREEN

Production change is one semantic condition:

```python
remote_view_mapping not in {'PROVEN', 'UNKNOWN'}
```

The existing fresh-target equality check is unchanged, so `UNKNOWN -> PROVEN` and `PROVEN -> UNKNOWN` drift still fails closed. All exact source/target fence, inventory, fingerprint, window-PID, namespace, display, endpoint, generation, atomic commit/rollback and forced-UNKNOWN-state requirements remain unchanged.

Exact implementation GREEN head before evidence-only checkpoint:

`a88aff2fe4f8ebd773d1682328911abe42b81230`

- reconciliation run `33200969801`, job `98950035983` — **SUCCESS**; live PR-event job `98950037574` — **SKIPPED**;
- Track A governance run `33200969705`, jobs `98950034608` and `98950034993` — **SUCCESS**.

The final evidence/task checkpoint must receive its own fresh exact-head CI and focused/governance verification before merge. This repair PR remains `runtime_access: none`. A separate post-merge recovery-admission checkpoint is still required before any new live reconciliation trigger.
