# OTClient Fork Agent Instructions

## Owner-funded AI and credential budget — highest priority

- Agents MUST NOT invoke Codex, OpenAI API, paid/limited AI review services, or any other mechanism that consumes the repository owner's personal AI quota, credits, tokens, subscription limits, or metered allowance unless the owner gives explicit permission for that specific use.
- Agents MUST NOT use, export, copy, inspect, forward, or authenticate with owner-supplied API keys, access tokens, session tokens, personal credentials, or secrets for AI/model services unless the owner explicitly authorizes that exact credential/service use.
- Availability of a credential, environment variable, CLI login, browser session, connector, MCP/plugin, or previously granted access does NOT constitute permission to consume owner-funded AI resources.
- Prior permission is not standing permission. Authorization must be explicit for the current task/use; if scope, provider, model, or expected consumption materially changes, ask again.
- If a workflow, policy, review gate, script, or tool would normally invoke Codex or another owner-funded AI service, skip that invocation and use a non-owner-funded alternative when one is genuinely available. If the requirement cannot be satisfied without such use, stop and report the exact blocker instead of consuming quota.
- Never weaken, bypass, or falsely mark a review/validation gate as satisfied merely because owner-funded AI use is forbidden.


## Local model resource policy — mandatory

- Local AI/model work on a physical host or shared GPU pool MUST use at most one resident or actively inferencing model at a time. Parallel workers may prepare prompts/evidence, but actual model residency/inference is serialized.
- Before loading or invoking a different local model, unload the previous model and re-check provider residency. For Ollama, `ollama ps` or `/api/ps` must show either no loaded model or only the exact target model; more than one resident model, a different resident model, or UNKNOWN/unavailable residency state means fail closed and do not start inference.
- Multi-model evaluation is sequential: model A -> unload/verify -> model B -> unload/verify. Do not intentionally keep multiple heavy local models warm for comparison, voting, audit panels or throughput.
- Model/session wrappers should use bounded keep-alive and best-effort unload on exit. Task completion/handoff should release task-loaded models when practical and record any model that could not be verified unloaded.
- This resource rule grants no model authority, runtime authority, Track A authority, credentials, merge authority or review status.

## Central Spark PR pre-review — standing owner authorization

- The owner explicitly authorizes the central controller in `blakinio/github-projects-control` to perform recurring advisory PR pre-review for this repository using exactly `gpt-5.3-codex-spark` through ChatGPT-managed Codex authentication on its trusted private runner. This is a standing, bounded repository-automation exception to the owner-funded AI restriction above; it does **not** authorize repository agents to invoke Codex, OpenAI API, hosted Code Review, or any other AI service themselves.
- The central controller may inspect only bounded PR metadata/diff text and may post only concrete P0/P1 findings. A clean Spark pass is intentionally silent. Target PR code is not checked out or executed by the Spark runner.
- Keep a PR Draft while implementation is still in progress. Mark it Ready only when this repository's normal readiness rules already permit that transition. The controller considers only eligible ready, internal, non-bot, exact-head, green-CI, bounded changes.
- Do not automatically request `@codex review`, enable hosted Codex Automatic Reviews, invoke Codex CLI, use `OPENAI_API_KEY`, or select another model/provider as a fallback. Any such direct AI use still requires separate explicit owner authorization for the current task/use.
- Spark pre-review is advisory and does not replace self-review, required independent review, required checks, E2E/runtime evidence, branch protection, or any merge gate. Never infer that Spark ran or passed merely because no comment appeared. Do not delay or weaken a repository merge gate solely to manufacture Spark evidence.
- If the central controller posts a P0/P1 finding before merge, treat it as an unresolved material review finding: address or explicitly disposition it under the repository's normal review rules, then rerun any validation invalidated by the resulting change.
- `no-spark-review` opts a PR out of the central controller. `spark-review` may force consideration of an otherwise ignored path class, but it never bypasses draft, fork, bot, CI, exact-head, size, model, or safety fences.

## Native login-to-ingame direct Spark — standing owner authorization

- The owner explicitly authorizes repository workers executing the exact `OTCLIENT-TIBIA-RE-NATIVE-LOGIN-TO-INGAME` alias/task family to invoke exactly `gpt-5.3-codex-spark` directly through ChatGPT-managed Codex authentication or another repository-approved managed path. This section is the explicit standing exception to the generic prior-permission rule above for that exact alias/task family only.
- Allowed use is bounded repository/code analysis, reverse-engineering assistance, implementation assistance, falsification, and review inside the declared native-login task. Spark may inspect repository code/diffs and sanitized secret-free evidence needed for those purposes.
- This exception does **not** authorize any other model/provider, OpenAI API use, `OPENAI_API_KEY`, hosted Codex Code Review as fallback, or exporting/reading/using owner-supplied AI API keys, tokens, sessions, or other AI credentials.
- Do not send Tibia credentials, 2FA values, session/auth secrets, secret-bearing process-memory or packet material, or raw proprietary official-client binaries to Spark. Preserve all repository/client secret and proprietary-artifact rules.
- Direct Spark use never creates or expands Track A runtime ownership, login/session budget, mutation authority, admission PASS, lease/registration authority, promotion authority, or completion evidence. Spark output is advisory and never replaces exact-SHA proof, current runtime evidence, fresh audit, real E2E, exact-head CI, review, or merge gates.
- If exact `gpt-5.3-codex-spark` or the approved managed authentication path is unavailable, do not silently fall back to another model/provider. Continue with a genuinely permitted non-owner-funded alternative when one exists or report the exact blocker if the task cannot proceed.
- This native-login exception is distinct from the central Spark PR pre-review authorization above; neither exception broadens the other.

## Instruction order

1. This root `AGENTS.md`.
2. The nearest nested `AGENTS.md`, when present.
3. `docs/agents/**`.
4. Relevant documentation under `docs/**`.
5. The active task record and linked ADRs.

Follow the more restrictive safety rule when instructions overlap.

## Repository allowlist — highest priority

- Routine write operations are allowed only in `blakinio/otclient`.
- `opentibiabr/otclient` is read-only upstream.
- Never mutate upstream issues, PRs, branches, tags, releases, files, workflows, comments, or reviews.
- Before every GitHub write, verify `repository_full_name` is exactly `blakinio/otclient`.
- A valid PR has both base and head repositories equal to `blakinio/otclient` and targets `main`.
- Treat an `upstream` Git remote as fetch-only.

## Global context efficiency baseline

- Work autonomously until the bounded task is complete or a real blocker/required decision is reached.
- Do not narrate routine file reads, searches, tool calls, commands, or unchanged checks.
- Send user-facing progress only for a material milestone, blocker, required decision, or material scope/risk change; keep each update to at most three short sentences.
- Run the full repository/task preflight once per bounded task or continuation session. Afterwards verify only state that may have changed and can invalidate the next action.
- Repeat the full preflight only after a material external repository-state change, a long interruption/session replacement, or evidence that durable task state conflicts with live state.
- Search before reading large indexes or documents in full and load only task-relevant documentation/source evidence.
- Do not paste full logs, diffs, artifacts, or whole source files when exact identifiers and focused excerpts are sufficient.
- Treat chat history as disposable. Keep durable task/handoff state compact and leave exactly one concrete next action when handing work off.
- When the next action is safe and autonomous, continue without waiting for acknowledgement.

## Mandatory startup protocol

Before implementation:

1. Read this file and `docs/agents/README.md`.
2. Read `docs/agents/ACTIVE_WORK.md` only as a coordination snapshot, then inspect `docs/agents/tasks/active/**` and all open PRs; task files and live GitHub state are authoritative when the index is stale.
3. Read `docs/agents/MODULE_CATALOG.md` and search modules, C++ services, Lua helpers, widgets, protocol code, and test support before adding an abstraction.
4. Read `docs/agents/REPOSITORY_MAP.md`, `KNOWN_RISKS.md`, and `BUILD_TEST_MATRIX.md`.
5. Read relevant contracts in `docs/agents/CROSS_REPO_CONTRACTS.md`.
6. Open overlapping tasks and check paths, modules, opcodes, feature flags, assets, and dependencies.
7. Check `git status --short --branch`, `git branch -vv`, `git remote -v`, and `git worktree list`.
8. Record uncertainty instead of inventing Canary or asset state.

## Work visibility and reuse — mandatory

Every agent must make work discoverable:

- create `docs/agents/tasks/active/OTC-YYYYMMDD-short-slug.md` before substantial implementation;
- declare `owned_paths`, `modules_touched`, `reuses`, `depends_on`, `blocks`, and cross-repository task IDs;
- publish the branch and open a draft PR early;
- do not manually add, remove, or edit rows in `docs/agents/ACTIVE_WORK.md` from a normal feature/fix/docs task branch;
- treat the individual task file and the live draft PR as the task's source of truth and discovery mechanism;
- until a deterministic generator is merged, leave `ACTIVE_WORK.md` unchanged unless the PR is a dedicated coordination/index repair;
- after a generator exists, update `ACTIVE_WORK.md` only through that generator in a dedicated coordination or post-merge step, not by hand;
- update the task after discoveries, decisions, failures, tests, review changes, and before context exhaustion;
- update `docs/agents/MODULE_CATALOG.md` in the same PR that adds a reusable module, changes a public interface, deprecates a module, or introduces a protocol/UI integration point;
- update `docs/agents/CHANGELOG.md` for completed behavior-level or architecture-level changes;
- use ADRs under `docs/agents/decisions/` for durable decisions.

Before creating a module, controller, widget helper, protocol utility, asset installer, message builder, test fixture, or platform abstraction, search the catalogue, open PRs, task records, and repository. Reuse or extend existing code when safe. Record why a new abstraction is necessary.

A new agent must be able to continue from Git, the PR, and task record without the previous chat.

## Multi-agent concurrency

- One agent uses one branch and one worktree.
- Never share a branch or worktree.
- `owned_paths` are advisory locks; resolve overlaps before editing.
- Avoid unrelated cleanup and broad formatting changes.
- Do not use `docs/agents/ACTIVE_WORK.md` as a writable shared lock or per-PR checklist.
- If an existing PR conflicts only in `docs/agents/ACTIVE_WORK.md`, take the current `main` version of that file, preserve the PR's own task record under `docs/agents/tasks/active/`, and continue validation.
- Edit other shared indexes narrowly and resolve their conflicts from current `main`.

## Autonomous delivery policy

Agents are expected to finish routine repository work end to end without waiting for approval at each step. Default workflow:

1. inspect repository and open PR state;
2. claim the task and affected paths;
3. create a branch and task record;
4. implement the smallest complete change;
5. run relevant validation;
6. create or update the PR;
7. inspect CI results and logs;
8. fix root causes and repeat until required checks pass;
9. resolve addressed review threads and update the PR body;
10. mark ready and squash-merge.

Agents may create branches, commits and PRs; update/discuss their own PRs; rerun a failed job once when it may be transient; repair CI; enable auto-merge; and merge their own PR without separate user confirmation.

### Autonomous merge gate

Merge only when all are true:

- base/head repositories are the approved user-owned repository;
- base is `main` and head is a task branch;
- full changed-file list and diff were reviewed with no unrelated or forbidden files;
- task acceptance criteria are satisfied;
- required local checks ran, or exact unavailable environment is documented;
- all required GitHub checks pass on current head;
- PR is mergeable with no unresolved requested changes or review threads;
- no blocker, cross-repository ordering hold, migration hold, or manual production gate remains;
- task, module catalogue, changelog, docs, and compatibility notes are current when applicable.

Use squash merge unless repository policy requires another method. Never bypass branch protection, dismiss valid failures, weaken tests, remove safety checks, or mark failing checks successful.

### CI repair loop

When CI fails:

1. identify workflow, job, step, commit SHA, and exact error;
2. determine whether cause is PR, stale base, CI configuration, or external infrastructure;
3. inspect logs before rerunning;
4. fix root cause in same PR when it belongs to the task;
5. use a separate narrow PR when unrelated CI repair would obscure the change;
6. rerun only failed jobs when appropriate;
7. record failure and fix in the task record.

A second identical failure must be investigated, not repeatedly rerun. Do not silence, skip, loosen, or delete checks to obtain green CI.

### Mandatory stop conditions

Stop automatic merge and document blocker for:

- any write to `opentibiabr/*`;
- secrets, private data, proprietary assets, database dumps, or credentials;
- destructive production migration without tested rollback;
- production deployment or irreversible external action outside the repository PR;
- unresolved path ownership overlap;
- an `atomic-required` cross-repository contract without both sides ready;
- forbidden binary/asset changes without explicit authorization and safety tooling.

## Git and commit policy

- Never push directly to `main`.
- Use a dedicated branch under `ai/`, `feat/`, `fix/`, `docs/`, `test/`, `refactor/`, `ci/`, or `chore/`.
- Track the matching remote branch, never `origin/main`.
- Prefer `git push origin HEAD:<branch>`.
- Use Conventional Commits and one logical change per PR.
- Use `--force-with-lease`, never plain `--force`, when rewrite is necessary.

## Change scope and evidence

- Inspect existing module, C++, Lua, OTML/OTUI, style, platform, and protocol conventions before editing.
- Review full diff and changed-file list before readiness and merge.
- Record exact commands, outcomes, and validation commit SHA.
- Never claim runtime, device, server compatibility, build, or CI success without evidence.
- Preserve failed approaches and blockers.

## Client assets gate — mandatory

Changes touching client-assets auto-installation must preserve:

- final paths `data/things/<version>/`, `data/sounds/<version>/`, and expected extras such as `bin/*`;
- staging/cache as transient only, never a runtime source of truth;
- `strictManifestSha256 = true` and `allowRawFallbackHashMismatch = false` unless a reviewed security design changes them;
- desktop extraction without unsupported Android `libarchive` linkage;
- explicit install-path and runtime-load verification in the PR.

Read `docs/client-assets-auto-install.md` before changing this area.

## Module and UI safety

- `modules/` contains shipped functionality; `mods/` contains optional/custom functionality.
- Do not place a core fix in `mods/` to avoid changing the owning module.
- Preserve dependencies, load order, controller lifecycle, event disconnects, key unbinds, widget destruction, and reload behavior.
- A new module requires `.otmod`, Lua, OTUI/OTML/style, localization, dependencies/startup, tests, and catalogue entry as applicable.
- Prefer module/controller-owned state over new globals.
- UI changes require relevant resolution/scaling and interaction checks when practical.

## Protocol and Canary coupling

When a change affects protocol parsing, protobuf, feature flags, payload-dependent UI, login, identifiers, or assets:

- create/link a `CAN-*` task and shared `OTS-*` ID;
- verify field order, widths, signedness, optionals, opcode/feature reuse, and version gates;
- define compatible client/server combinations and rollout order;
- validate with relevant Canary commit/version;
- update `docs/agents/CROSS_REPO_CONTRACTS.md`.

## Build and test policy

- Use current `CMakePresets.json`; do not guess build directories.
- Normal Windows release:

```bat
cmake --preset windows-release
cmake --build --preset windows-release
```

- Test-enabled presets come from current presets and `docs/agents/BUILD_TEST_MATRIX.md`; active PR #3 may change names/coverage.
- Lua/module changes require syntax/static checks and focused runtime validation.
- OTUI/style changes require load and interaction checks.
- Protocol changes require compatible Canary runtime or a precisely documented missing environment.
- Do not infer Android/browser/mobile compatibility from desktop builds.
- Recover caches by removing only the verified affected preset directory under `build/`.

## Data, asset, and security safety

- Do not commit proprietary CipSoft assets without confirmed redistribution rights.
- Do not silently replace things, sounds, fonts, images, certificates, manifests, or server lists.
- Document source, version, hash, and license for new distributable assets.
- Never commit tokens, passwords, keys, cookies, updater credentials, `.env`, personal data, private logs, or internal server details.
- Treat updater/download/archive/TLS/certificate/manifest/encryption/remote-content changes as high risk.
- Do not weaken hash or transport validation to make downloads succeed.

## PR communication

Agents may autonomously update and discuss their own PRs, reply to review feedback, and resolve threads after fixes. Do not comment on unrelated PRs unless needed for overlap/dependency coordination. All PR communication must be in English.

## GitHub connector routing — mandatory

- For GitHub repository, pull request, issue, review, and remote-file tasks, inspect and use the connected GitHub plugin or connector before falling back to local `git` or `gh`.
- Treat an explicit `@GitHub` selection as a request to use the connected GitHub plugin.
- Local `git` may be used for checkout, worktree, diff, branch, and commit operations. Use `gh` only for operations the connector does not support or when repository policy explicitly requires it.
- A missing local checkout, missing `gh` binary, or unauthenticated local `gh` session is not evidence that the GitHub connector is unavailable.

Before claiming that GitHub access is unavailable:

1. Inspect the available GitHub connector tools and determine whether the connector is registered and enabled and whether the required operations exist.
2. If an authenticated-identity operation exists and the connector is callable, call `github_get_user_login` or its equivalent; otherwise record the confirmed missing or disabled connector or missing identity operation.
3. If a repository lookup or listing operation exists and the connector is callable, call `github_get_repo` or `github_list_repositories` for the requested repository scope; otherwise record the missing capability.
4. If the required read operation exists and is callable, attempt it through the connector when it is safe and within the task's authority; otherwise record the unavailable capability.

Report a GitHub access blocker only after the applicable availability and capability checks above and, when an applicable operation exists and is safe to attempt, an actual connector call. Authentication or permission errors, a confirmed missing or disabled connector, a missing required operation, rate limiting, and transport or service failures are valid blockers when they prevent the task and no safe permitted connector, local `git`, or `gh` fallback can complete it. Include the exact availability and capability verification performed. When a call was attempted, include the failed operation and returned error; when no call was possible, identify the missing or disabled connector or unavailable operation instead.
