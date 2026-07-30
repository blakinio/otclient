# Agent Coordination Documentation

Persistent operating memory for autonomous agents across the legacy client and the greenfield Rust client.

## Read order

1. `../../AGENTS.md`.
2. Determine the track from the changed paths.
3. For new Rust-client work, read `../../oteryn-client/AGENTS.md`, its architecture and agent program.
4. When several Rust-client agents may run concurrently, read the multi-agent execution protocol and latest accepted/closed wave record before claiming work.
5. For legacy C++/Lua client work, read the legacy architecture/workstream owner and inspect source/module/test conventions.
6. Read `ACTIVE_WORK.md` only as a coordination snapshot.
7. Inspect all records under `tasks/active/` and all live open PRs/checks/review threads.
8. Read `MODULE_CATALOG.md`, `REPOSITORY_MAP.md`, `KNOWN_RISKS.md` and `BUILD_TEST_MATRIX.md`.
9. Read `CROSS_REPO_CONTRACTS.md` for protocol, identifiers, login, routing, gameplay channels or assets.
10. Read relevant tasks, ADRs, audits, source and tests.

## Product tracks

### Greenfield Oteryn Rust client

Normative entry point: `../../oteryn-client/README.md`.

| Document | Purpose |
|---|---|
| `../../oteryn-client/docs/architecture/ARCHITECTURE.md` | Stable target architecture and runtime boundaries. |
| `../../oteryn-client/docs/architecture/REPOSITORY_LAYOUT.md` | Planned workspace, crates and dependency direction. |
| `../../oteryn-client/docs/architecture/CLIENT_LIFECYCLE.md` | Account/game sessions, gameplay-channel login and relog. |
| `../../oteryn-client/docs/architecture/PROTOCOL_BOUNDARY.md` | Canary/Oteryn adapter isolation. |
| `../../oteryn-client/docs/architecture/SECURITY_MODEL.md` | Trust boundaries and invariants. |
| `../../oteryn-client/docs/architecture/TECHNICAL_LOGIN.md` | Bounded W7 technical Identity/Gateway/Canary admission architecture. |
| `../../oteryn-client/docs/agents/PROGRAM.md` | Ordered audit-first implementation gates. |
| `../../oteryn-client/docs/agents/WORKSTREAMS.md` | Agent ownership and package routing. |
| `../../oteryn-client/docs/agents/MULTI_AGENT_EXECUTION.md` | Parallel lane, shared-path lease and contract/merge protocol. |
| `../../oteryn-client/docs/agents/CURRENT_PARALLEL_WAVE.md` | `OTERYN-W7-TECHNICAL-LOGIN` accepted plan, exact ownership, blockers and launch gates. |
| `../../oteryn-client/docs/agents/INITIAL_PARALLEL_WAVE.md` | Historical first-wave launch plan and dependency evidence. |
| `../../oteryn-client/docs/agents/templates/PARALLEL_TASK.md` | Additional task metadata for parallel work. |
| `../../oteryn-client/docs/agents/prompts/COORDINATOR_AGENT.md` | Exact W7 coordinator/integrator prompt. |
| `../../oteryn-client/docs/agents/prompts/W7_ENTRY_CONTRACT_AGENT.md` | Sole entry/session/directory contract producer prompt. |
| `../../oteryn-client/docs/agents/prompts/W7_IDENTITY_AGENT.md` | PKCE/Identity/Gateway consumer prompt with dynamic-loopback evidence. |
| `../../oteryn-client/docs/agents/prompts/W7_CANARY_ENTRY_AGENT.md` | Sole Current-profile transport/admission producer prompt. |
| `../../oteryn-client/docs/agents/prompts/W7_LOGIN_E2E_AGENT.md` | Final fake-service/executable composition consumer prompt. |
| `../../oteryn-client/docs/agents/prompts/WORKER_AGENT_BASE.md` | Common historical worker prefix; exact current lane prompts take precedence. |
| `../../oteryn-client/docs/agents/prompts/NEXT_SYNTHETIC_ASSET_AGENT.md` | Historical W6-ASSET prompt; completed work must not be relaunched. |
| `../../oteryn-client/docs/agents/prompts/NEXT_RENDERER_SURFACE_AGENT.md` | Historical W5-RENDER prompt; completed work must not be relaunched. |
| `../../oteryn-client/docs/agents/prompts/NEXT_WINDOWS_SHELL_AGENT.md` | Historical W4-SHELL prompt; completed work must not be relaunched. |
| `../../oteryn-client/docs/agents/prompts/NEXT_TEST_SUPPORT_AGENT.md` | Historical W3-TEST prompt; completed work must not be relaunched. |
| `../../oteryn-client/docs/agents/prompts/NEXT_DIAGNOSTICS_AGENT.md` | Historical W2-DIAG prompt; completed work must not be relaunched. |
| `../../oteryn-client/docs/agents/AUDIT_PLAN.md` | Mandatory foundation audit. |
| `../../oteryn-client/docs/agents/prompts/FIRST_AUDIT_AGENT.md` | Historical standalone prompt for the completed first audit. |

The current C++/Lua/OTUI code is evidence only for the Rust track and must not become a Rust runtime dependency.

Parallel Rust work is permitted only through a live accepted wave, unique tasks/branches/worktrees, non-overlapping ownership and one producer per public contract. Cargo/lockfile, dependency policy, Rust CI and other shared integration paths are serialized through the task-based lease protocol; manually resolving `Cargo.lock` conflicts is prohibited.

W1-W6 are completed and cannot be relaunched. W7 workers remain unauthorized until the W7 planning PR and its separate planning-task archive merge and a fresh overlap/contract/lease check passes. After activation, use only the exact current prompts and dependency order in `CURRENT_PARALLEL_WAVE.md`.

W7 proof boundaries:

- Platform registers the no-port loopback base `http://127.0.0.1/callback`, while its current tests explicitly prove an otherwise matching OS-assigned dynamic port for authorization and token exchange; workers must revalidate this exact producer behavior and must not bind fixed port 80.
- repository/fake tests or legacy OTClient E2E do not prove real Rust Identity/Gateway/Canary compatibility;
- deployed TLS, firewall, client configuration, issuer mapping, secret injection and exact runtime revisions remain external evidence;
- Gateway v1 does not provide general multi-world/gameplay-channel issuer routing;
- current token-family revocation bounds W7 to one bootstrap attempt.

### Legacy OTClient

The existing roots `src/`, `modules/`, `mods/`, `data/`, CMake and legacy tests remain operational during migration.

| Document | Purpose |
|---|---|
| `../architecture/LEGACY_OTCLIENT_ARCHITECTURE.md` | Maintained architecture needed for legacy work. |
| `LEGACY_OTCLIENT_WORKSTREAMS.md` | Detailed legacy ownership and acceptance routing. |
| `programs/OTCLIENT_UPSTREAM_INTELLIGENCE.md` | Durable read-only upstream/fork audit program. |
| `prompts/OTCLIENT_NEW_AGENT_PROMPT.md` | Standalone startup prompt for a fresh legacy-client agent. |

Legacy work follows exact path owners, existing lifecycle/protocol/security rules and live PR/task state. It must not create a second target architecture or claim to be the greenfield Rust implementation.

## Shared documents

| Document | Purpose |
|---|---|
| `OTERYN_WORKSTREAM_MAP.md` | Top-level track router. |
| `MODULE_CATALOG.md` | Existing/planned reusable systems and interfaces. |
| `REPOSITORY_MAP.md` | Fast path-to-responsibility navigation. |
| `KNOWN_RISKS.md` | Cross-cutting and track-specific risks. |
| `BUILD_TEST_MATRIX.md` | Current validation policy for both tracks. |
| `CROSS_REPO_CONTRACTS.md` | Canary/Oteryn integration contract registry and exact W7 evidence cut. |
| `CHANGELOG.md` | Curated completed behavior/architecture changes. |

## Sources of truth

- Git, current `main`, open PRs and checks are authoritative for branch/merge/live state.
- Active task files are authoritative for ownership, progress, failures, parallel leases and handoff.
- `ACTIVE_WORK.md` can be stale.
- `oteryn-client/docs/architecture/**` is authoritative for the new client.
- `MULTI_AGENT_EXECUTION.md` defines parallel execution but does not override architecture/live state.
- `CURRENT_PARALLEL_WAVE.md` records exact current launch authorization, ownership, dependencies, blockers and acceptance.
- Historical wave/prompt documents never authorize duplicate work.
- Cross-repository facts require current producer/consumer evidence; external repositories remain read-only unless a separate authorized task exists there.
- Protocol analysis is internal Oteryn/Canary compatibility work and must not be published as third-party gameplay manipulation or anti-cheat tooling.
- ADRs preserve durable decisions.

## Lifecycle

### Start

- inspect current `main`, open PRs, review threads and active tasks;
- route the task to greenfield or legacy paths;
- read the nearest nested `AGENTS.md`;
- for parallel Rust work, verify the accepted lane, producer commits, blocker state and shared-path lease;
- never launch a historical/completed lane;
- search for existing owners and reusable work;
- create a bounded task, branch/worktree and early draft PR;
- declare ownership, dependencies and cross-repository evidence.

### During

- update the task after discoveries, failures, decisions, tests and reviews;
- keep the PR body current;
- update catalogues/contracts/ADRs when public boundaries change;
- respect the unique shared-path lease and do not duplicate another lane's contract;
- mark `integration_ready` rather than editing leased shared paths;
- preserve security, licensing, exact-version and no-secret gates.

### Finish

- restack on required producer/current `main` when dependencies changed;
- regenerate lockfiles; never manually merge them;
- inspect the full changed-file list and diff;
- run proportional focused checks and exact-head required CI;
- update task/docs/contracts/catalogue as applicable;
- merge only through the root autonomous merge gate;
- archive every merged task separately;
- leave one concrete next action.

## Avoiding duplicate work

Search by responsibility, path, crate/module, protocol field, identifier, feature capability, asset schema, test fixture, task ownership, parallel contract role and open PR. Extend the owning architecture/interface rather than creating a parallel framework.
