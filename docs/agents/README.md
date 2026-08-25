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

## Track A official-client runtime admission — mandatory

For every Track A `official-client-re` worker, **at task claim/resume before substantial Track A work**, read and obey all of:

```text
TIBIA_RESEARCH_TRACKS.md
contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
decisions/ADR-0001-track-a-canonical-live-runtime.md
contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
```

At claim/resume/checkpoint, the active Track A task must persist the complete admission record required by `TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md`; static/no-runtime workers record `runtime_access: none`. Before the first runtime-related operation, and again after any authority/identity-changing fact, re-evaluate and re-persist admission before proceeding. `UNKNOWN`, `REQUIRED_NOT_PROVEN`, `REQUIRED_UNAVAILABLE`, or `REQUIRED_UNIMPLEMENTED` on a required gate means refuse that operation.

For `read_only`, live observation is legal only when non-invasiveness, a declared non-conflicting target/namespace/ownership boundary, and `target_uniqueness: PROVEN` are fresh; otherwise use `none` for static/artifact work or refuse the live observation.

Canonical reuse/mutation requires current Gate A, any required reviewed generation rebind, Gate B on the authoritative exact-runtime registration, current-task ownership/target uniqueness, equal current lease-generation binding after any rebind, and the final cancellation-safe whole-lifetime supervisor. Missing registration routes only to bootstrap; a generation mismatch with unchanged runtime identity routes only to reviewed rebind; stale registered PID/start identity on the same boot routes only to reviewed `canonical_recovery`; a prior-boot adoption registration whose fresh singleton target proves a different boot epoch routes only to reviewed `canonical_boot_epoch_recovery`; an ephemeral sandbox may never use or alias the canonical namespace.

After merged PR #331, `programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md` additionally routes Track A execution by evidence class. Deterministic/disposable work (static analysis, workflow/Lua validation, unit/integration tests, Linux build, `ldd`, hosted real-artifact `Xvfb` startup smoke, registries and evidence processing) defaults to GitHub-hosted runners. Synology/self-hosted is reserved for the serialized physical runtime: one canonical persistent session, real display/input, login/relogin, walking/clicking, LAN/runtime integration, long-lived observation and direct physical gameplay E2E. Hosted startup liveness is not physical gameplay E2E. Parallel workers must not create one logged-in persistent session each; physical mutation is serialized through the one canonical runtime authority when it exists and passes current admission gates.

Historical runtime evidence is discovery input only. Until fresh authoritative evidence proves otherwise, preserve exactly:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Stale task text, PR prose, a visible `:98`, reachable `6082`, numeric PID/session, or standalone lease validation cannot override this admission gate. Track A workers must not mutate or live-observe another task's owned runtime surface, including PR #303-owned state, and Track B never shares Track A canonical authority or mutable runtime state.

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

W1-W6 are completed and cannot be relaunched. The W7 plan and its separate planning-task archive are merged. W7-ENTRY-CONTRACT is completed and archived; W7-IDENTITY and W7-CANARY-ENTRY may launch only after a fresh overlap/contract/lease check and must restack on producer merge `9ecc43a4465f6565bc1c12ea61f170a96edcbe35`. W7-LOGIN-E2E remains bound by the dependency order in `CURRENT_PARALLEL_WAVE.md`.

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
