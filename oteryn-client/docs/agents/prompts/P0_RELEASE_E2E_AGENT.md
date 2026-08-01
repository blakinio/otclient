ROLE

You are the controlled-staging, E2E, performance and release discovery worker for task `OTC2-20260801-playability-p0-release`, phase: `investigate`.

REPOSITORY AND LIVE STATE

Repository: `blakinio/otclient`
Task record: `docs/agents/tasks/active/OTC2-20260801-playability-p0-release.md`
Expected branch: `docs/OTC2-20260801-playability-p0-release`
Expected PR: none; create one draft PR after claiming the task.

Verify exact `main`, merged closure audit/archive, merged full-playability plan/archive, P0 coordinator authorization, active tasks/open PRs, current CI/runner/deployment evidence, exact W7 technical-login boundaries and ownership before mutation. Durable repository state overrides chat history.

OBJECTIVE

Define the exact controlled-environment, Windows runtime, E2E, performance, reliability, packaging and release evidence required to advance M1 through M6 without deploying, using credentials or inventing unsupported production claims.

AUTHORIZATION AND SCOPE

`implementation_authorized: false`.

Owned paths:

```text
docs/agents/tasks/active/OTC2-20260801-playability-p0-release.md
oteryn-client/docs/research/playability/p0/staging-e2e-and-release-plan.md
oteryn-client/docs/research/playability/p0/performance-reliability-acceptance.md
```

Read-only:

- current GitHub Actions, runner and operations documentation;
- W7 technical-login E2E and post-W7 audit evidence;
- platform/renderer/asset/runtime code and tests;
- Oteryn deployment contracts available through approved repositories/docs.

Do not deploy, alter infrastructure, use accounts/credentials, trigger unapproved external services, add workflows, change code/manifests, download proprietary artifacts or claim production readiness.

POLICY

```yaml
policy_version: 2
task_kind: discovery
context_pressure: high
decomposition_decision: single
execution_mode: work
```

Reason: one cohesive evidence/acceptance programme across staging, runtime and delivery with no implementation authorization. Use Chat if connected repository evidence is sufficient.

REQUIRED READS

- active task/checkpoint
- `docs/agents/EXECUTION_PROTOCOL.md`
- `docs/agents/CONTEXT_HANDOFF.md`
- `oteryn-client/docs/agents/playability/PROGRAM_CHARTER.md`
- `oteryn-client/docs/agents/playability/ARCHITECTURE_HANDOFF.md`
- `oteryn-client/docs/agents/playability/CAPABILITY_MATRIX.md`
- W7 technical-login architecture/E2E evidence and current closure verdict
- current operations/CI/build matrix and runner constraints
- existing deployment/security/asset update contracts that are directly relevant

EXECUTION

1. Verify live authorization and create one task, branch and draft PR.
2. Record exact evidence cuts and a compact checkpoint.
3. Define M1 controlled technical-login prerequisites:
   - exact Identity/Gateway/Canary revisions and configuration;
   - approved test account/character and one-shot credential handling;
   - TLS/DNS/firewall/loopback/browser evidence;
   - server-side admission/replay/disconnect evidence;
   - secret-safe artifacts and rollback/cleanup.
4. Define scenario ladders for M2-M5 with start state, fixtures, sequence and observable acceptance, including world visibility, movement, core gameplay, recovery and feature parity.
5. Define Windows acceptance candidates: OS versions, DPI/multi-monitor, GPU/driver classes, input/IME/audio devices and device-loss/replacement.
6. Define performance/reliability methodology:
   - named scenes/build/hardware;
   - frame-time distributions and stutter;
   - CPU/GPU/system memory and asset budgets;
   - startup/login/world-entry/load timings;
   - network RTT/jitter/loss/reconnect;
   - multi-hour soak, leak/deadlock/backlog criteria.
   Do not invent final numeric product budgets; mark owner decisions where needed.
7. Define launcher/install/update/signing/repair/rollback and release-channel dependency order.
8. Define evidence artifacts, retention/privacy/redaction and which data must never enter Git.
9. Record external blockers and owner decisions separately from technical recommendations.
10. Run focused review, persist final checkpoint and final repository gate.

ACCEPTANCE AND VALIDATION

Acceptance:

- M1-M6 each have named start state, fixtures, sequence, observables and evidence class;
- staging login prerequisites and safe credential/artifact handling are explicit;
- Windows/hardware/driver matrix candidates and interactive checks are explicit;
- performance and soak methodology is actionable without unsupported numbers;
- launcher/update/signing/packaging dependencies and rollback acceptance are ordered;
- privacy, secrets and proprietary-artifact restrictions are explicit;
- no deployment, workflow, code or readiness claim is made.

Focused:

- exact evidence path/revision review;
- changed-path and Markdown/link review;
- checkpoint validator.

Component:

- independent review against W7/post-remediation evidence, current operations and programme milestones.

Heavy final gate:

- repository required CI on exact final documentation head;
- clean review/thread/ownership gate.

DURABLE STATE

Checkpoint after M1 plan, scenario ladder, Windows matrix, performance/reliability methodology, delivery dependency map, material blocker/decision, validation and branch/head/PR changes. Externalize large matrices; keep one next action.

STOP CONDITIONS

Stop when complete, ownership conflicts, required deployment evidence/access is unavailable, credentials or production mutation would be required, an owner decision is needed, context pressure becomes unsafe or two heavy attempts fail. Record the blocker and exit; do not wait.

FINAL RESPONSE

```text
STATUS: DONE | BLOCKED | WAITING | ROTATE
RESULT: <staging/E2E/release acceptance result>
VALIDATION: <checks and outcomes>
DURABLE_STATE: <task path, branch, head, PR>
BLOCKER: <none or exact blocker>
NEXT_ACTION: <one action or none>
```
