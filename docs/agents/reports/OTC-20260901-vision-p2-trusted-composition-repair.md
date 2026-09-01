# OTC Vision P2 trusted composition repair report

## State

Prepared by `OTC-VISION-P2-COORDINATOR` at `2026-09-01T23:28:41+02:00` from trusted `main@103fa3071ee4d82d7dff934034e2442c32bd3a81`.

Implementation has not started. The current real stop is Codex Spark quota exhaustion until `2026-09-02T04:15+02:00`, plus PR #829 remains `RETURN_FOR_REPAIR` for a worker-owned authentication-proof flaw.

## Accepted source inputs

- PR #827 head `6991b98f3f970c6ffc9d1bec9bf032aed89f0f2d`: coordinator `ACCEPT_WITH_EDITS` for a safe fail-closed capture boundary. It intentionally refuses trusted capture until a composition-owned reviewed policy, canonical evidence root and recomputable evidence validator exist.
- PR #830 head `971787f380d52d0e141c50b9201498b0c99e752d`: coordinator `ACCEPT_WITH_EDITS` for the safe bridge producer. Exact-head Package A/B, Track A and `CI / Required` are green, but production `ControlDomainService` still constructs `AgentSessionCoordinator` without `ReviewedRuntimeAuthorityConfiguration`.
- PR #829 is not yet an accepted input. Its current transport repairs may be consumed only after coordinator re-review returns `ACCEPT`.

## Coordinator findings driving this repair

The capture and bridge workers independently reached the same architectural boundary: same-process Python privacy, underscored factories, module-global tokens, object identity and caller-created registries are not a trusted authority source.

The application composition root must own reviewed runtime contracts, reviewed capture policy, canonical evidence root and durable replay-state attachment. Requests and edge payloads remain data only.

No live runtime evidence is claimed or required for this repository/static repair.