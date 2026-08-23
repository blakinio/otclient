# OTCLIENT-TIBIA-RE Control Center Package B continuation alias

```yaml
alias_prompt_contract_version: 1.0.0
canonical_prompt_contract_version: 1.0.1
alias: OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-B-CONTINUE
repository: blakinio/otclient
track_id: official-client-re
lane: P2-CONTROL-API
risk: medium
runtime_access: none
official_client_access: false
mutation_authorized: false
credentials_allowed: false
login_allowed: false
gameplay_allowed: false
control_api_listener: loopback_only
run_scope: existing_package_b_task
continuation_policy: continue_until_real_stop
task_completion_policy: finalize_archive_and_stop_at_package_boundary
user_communication: low_noise
complete_control_center_programme: false
direct_owner_funded_ai_authorized_by_alias: false
```

Owner invocation:

```text
Kontynuuj OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-B-CONTINUE autonomicznie.
```

or simply:

```text
OTCLIENT-TIBIA-RE-CONTROL-CENTER-PACKAGE-B-CONTINUE
```

## Resolution rule

Do not reconstruct Package B from chat history. Resolve this alias through live repository state.

First read and obey the current instruction hierarchy, then load the canonical Package B prompt:

```text
AGENTS.md
docs/agents/README.md
docs/agents/PROMPTING_STANDARD.md
docs/agents/prompts/TIBIA_RE_CONTROL_CENTER_PACKAGE_B_PARALLEL_AGENT.md
```

Then discover the current Package B task record, PR, branch, exact head, checks, reviews, comments, ownership overlaps and applicable contracts from live GitHub/main.

Historical discovery anchors only:

```text
Task family: OTC-20260823-tibia-re-control-center-package-b
Known PR at alias creation: #666
Known branch at alias creation: feat/OTC-20260823-tibia-re-control-center-package-b
Known checkpoint head at alias creation: 91f918d59d34330c1d287b1ca945f4b935ca1fc6
```

These anchors are not authority. If live state differs, live state wins.

## Mission

Continue the existing Package B task autonomously to terminal closeout. Treat the existing implementation as an unverified candidate, not as proof of correctness.

The successor agent must independently falsify the implementation against current contracts, repair material findings, run exact-head validation, obtain required review/audit evidence, make CI green on the final head, merge through current repository policy, archive the task and release ownership.

Package B completion does not claim Package C, Package D, Package E or the complete Control Center programme.

## Hard safety boundary

Package B remains:

```text
runtime_access: none
official_client_access: false
mutation_authorized: false
credentials/login/gameplay: false
Control API listener: loopback_only
```

Allowed mutation is only through the explicit fake/test adapter path required by the canonical Package B contract.

Forbidden:

- Official Tibia process observation or mutation;
- Tibia login, logout, relog or character selection;
- gameplay input or transactions;
- process memory read/write, attach, injection, signals or process control;
- wildcard or non-loopback Control API binding;
- raw/debug/concrete-adapter endpoints or browser/CLI adapter bypass;
- any local setting that grants Official Track A mutation authority;
- credentials, Tibia secrets or secret-bearing evidence.

Remote desktop may be used only as a developer tool for repository, terminal and local browser E2E work. It must not be used to interact with the Official Tibia client for this task.

This alias itself does not authorize direct Codex/OpenAI/owner-funded AI use. Follow current `AGENTS.md` and current explicit owner authorization. Never weaken an audit/review gate because such a service is unavailable.

## Startup / continuation procedure

1. Fetch exact current `origin/main` and record its SHA.
2. Inspect the live Package B PR and exact head.
3. Inspect current checks, reviews, review threads and comments.
4. Read the active Package B task record and its evidence.
5. Read current Control Center contracts and `docs/agents/TASK_CLOSEOUT_AUDIT_E2E.md`.
6. Inspect active tasks and open PRs for Package C/D/E and shared-path overlap.
7. Reuse the existing Package B branch/task if live state proves it is the correct continuation target.
8. Never share a branch/worktree with another active agent; resolve ownership overlap before editing.
9. Do not stop after merely reporting status when the next action is safe and autonomous.

## Independent falsification audit

Do not accept the existing `audit_package_b.py` or tests as sufficient proof until the implementation has been compared directly with the current contracts.

Attempt to falsify at least:

1. exact loopback binding and refusal of wildcard/non-loopback modes;
2. fresh >=256-bit backend-epoch nonce;
3. nonce required for every `/v1/*` request;
4. exact Host allowlist and same-origin Origin enforcement;
5. no permissive CORS and no ambient cookie authentication;
6. nonce absent from URL, logs, artifacts, argv and prohibited browser storage;
7. bounded body/header/page/event/concurrency/queue/backpressure behavior;
8. stable safe error envelope with no arbitrary exception or secret leakage;
9. durable RequestLedger with canonical/normalized request hash;
10. every POST reserving final logical resource/transition identity and persisting `ACCEPTED` before domain execution;
11. execution using the exact reserved identity;
12. STOP/reset using the reserved `transition_id`;
13. same request/body replaying the same logical result across restart;
14. same request ID with different body conflicting deterministically;
15. FAILED requests replaying the same failure until a new request ID is used;
16. crash windows not creating duplicate resources or effects;
17. delayed old STOP/reset replay not mutating newer ControlState;
18. graceful shutdown preserving global/per-run safety state;
19. original run activation/deadline and Action/Budget semantics remaining truthful after restart;
20. browser and CLI exposing required semantic operations only through the Control API/domain path;
21. browser reload/new tab not duplicating active work;
22. UI separately representing runtime, authority, capability, evidence, freshness and session state;
23. UNKNOWN/STALE/UNSUPPORTED/NOT_PROVEN remaining truthful;
24. mutation authority not locally grantable;
25. mutating operations restricted to explicit fake/test adapter;
26. no Official Tibia/raw adapter bypass path;
27. Package A regression staying green;
28. artifacts/export bundles containing no nonce or secret material;
29. real browser + CLI + backend E2E passing on the final implementation environment.

Compare endpoint-by-endpoint with the current:

```text
docs/agents/contracts/TIBIA_RE_CONTROL_CENTER_CONTROL_API_V1.md
```

Also inspect the current Artifact, Execution, Scenario, Adapter and Policy Boundary contracts. Verify contract completeness rather than merely satisfying tests written with the implementation.

Pay special attention to run/scenario/action/event/artifact browsing, run control, experiments, recorder/network/compare/logger surfaces, pagination, safe error semantics, restart recovery and browser/CLI parity.

## Repair loop

For every material finding:

1. document the finding in the Package B task/evidence;
2. fix the root cause on the correct Package B branch;
3. add or strengthen a regression test;
4. run focused validation;
5. commit and push;
6. rerun invalidated audit/E2E checks on the new exact head;
7. inspect CI again.

Do not paper over failures by loosening tests, weakening safety rules, skipping checks or relabeling UNKNOWN as success.

## Exact-head validation

Before readiness/merge, run sequentially on the exact final Package B head, using current repository commands when they have evolved:

```text
ruff check tools/tibia_re_control_center tests/tools/tibia_re_control_center
python -m compileall -q tools/tibia_re_control_center tests/tools/tibia_re_control_center
python -m unittest discover -s tests/tools/tibia_re_control_center -v
python tests/tools/tibia_re_control_center/audit_package_b.py
python tests/tools/tibia_re_control_center/e2e_package_b.py
git diff origin/main...HEAD --check
```

Do not intentionally run the real browser E2E in parallel with a heavy full suite if resource/CDP contention can make the result non-deterministic.

The browser E2E must use the real Package B backend and a real browser/headless browser. Mock-only browser tests are not completion evidence.

Inspect the Package B GitHub workflow itself. Do not assume browser or Node/CDP dependencies are present on a runner. Repair CI deterministically if needed.

Only exact-head green results count.

## Browser / CLI parity

Verify semantic parity from the contract, not just status-display parity.

Browser and CLI must remain thin clients over the same secured Control API/domain path. Neither may import or invoke an adapter/coordinator to bypass the API. If the contract requires an operator operation on both clients and one surface lacks it, repair the implementation and add parity/E2E coverage.

## Review and merge

Keep the Package B PR Draft while implementation or material audit repair remains in progress.

Mark Ready only when current repository readiness rules are met. Resolve material review findings, rerun invalidated validation and require exact-head CI before merge.

Follow current `AGENTS.md` autonomous merge policy. Use the repository-required merge method and never bypass branch protection or valid review/check failures.

If central Spark pre-review is eligible under current repository policy, treat it only as advisory; do not infer that it ran merely because no comment appeared.

## Shared paths and concurrent packages

Package C/D/E may be active concurrently. Before editing shared files such as catalogue/changelog/index/governance surfaces, revalidate ownership from live task/PR state. Serialize or defer overlapping shared edits rather than racing another worker.

Do not enter another package's owned lane just to simplify Package B closeout.

## Terminal closeout

A merged implementation PR is not enough by itself.

Follow current closeout rules until:

- Package B implementation is merged into current `main`;
- required Package B E2E is PASS on the final implementation head;
- fresh required audit/review is PASS;
- Package A regression is PASS;
- exact-head CI is PASS;
- all related PR/review states are terminal;
- final merged SHA is recorded in task/evidence;
- the active Package B task is archived according to current governance;
- ownership is released;
- current `main` is re-read to verify the result actually landed;
- Official Tibia client/runtime access for this task remains NONE.

Stop only at that bounded Package B boundary. Do not automatically select another package after Package B becomes terminal.

## Legal invocation outcomes

`DONE` is legal only after terminal merge + archive + ownership release.

Use `WAITING` only for a genuine external wait that cannot be advanced autonomously. Use `BLOCKED` only for a real technical/policy blocker that cannot be removed within current tools and authority. Use `ROTATE` only when repository/context policy requires handoff while durable state contains exactly one next action.

Do not use `DONE` for "code is ready", "tests are green" or "PR is open".

## Final response contract

Return exactly:

```text
STATUS=DONE|WAITING|BLOCKED|ROTATE
TASK=OTC-20260823-tibia-re-control-center-package-b
PR=<number/state>
FINAL_HEAD=<sha>
PACKAGE_B_E2E=PASS|FAIL|BLOCKED
AUDIT=PASS|FAIL|BLOCKED
CI=PASS|FAIL|PENDING
OFFICIAL_CLIENT_ACCESS=NONE
OWNERSHIP=RELEASED|HELD
NEXT_ACTION=<exactly one action or NONE>
```
