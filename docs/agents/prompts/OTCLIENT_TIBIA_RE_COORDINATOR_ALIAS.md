# OTCLIENT-TIBIA-RE coordinator alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-COORD
track_id: official-client-re
role: promotion_integration_coordinator
promotion_authority: coordinator_only
default_execution_class: github_hosted
default_runtime_access: none
run_scope: autonomous_program
continuation_policy: continue_until_real_stop
```

## Resolution

This is an additive alias wrapper, not a standalone programme prompt. On every invocation load and obey the current trusted-base versions of:

```text
AGENTS.md
docs/agents/README.md
docs/agents/TIBIA_RESEARCH_TRACKS.md
docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
```

Then resolve current `main`, active Track A tasks, open PRs, ownership, exact heads, checks, review threads and durable `next_action` values. Current repository state overrides stale prompt/PR/chat wording.

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-COORD autonomicznie.
```

## Coordinator preset

Coordinate the five Track A research lanes:

```text
P2-NETWORK
P0-STATE
P1-BRIDGE
RUNTIME
COVERAGE-AUDIT
```

For every dispatch or resume, require concrete current values for:

```yaml
TASK_ID:
TASK_RECORD:
LANE:
BASE_MAIN:
BRANCH:
WORKTREE:
OWNED_PATHS:
DEPENDENCIES:
EXECUTION_CLASS:
RUNTIME_ACCESS:
PERSISTENT_SESSION_ROLE:
PHYSICAL_E2E_REQUIRED:
```

Default routing is:

- P2-NETWORK, P0-STATE, P1-BRIDGE and COVERAGE-AUDIT -> GitHub-hosted, `runtime_access: none`;
- RUNTIME -> `synology-otclient-01` for physical work, with fresh Track A runtime admission;
- non-RUNTIME workers consume durable RUNTIME evidence instead of creating their own logged-in Global sessions.

Researchers stop at Draft PR/evidence handoff. The coordinator independently reviews, reconciles and promotes only accepted bounded slices; green CI alone is never semantic proof.

## Persistent Synology runtime invariant

Treat the desired physical topology as one programme resource, not one resource per worker:

```text
one persistent Synology X11 desktop
+ one persistent private VNC view bound to that desktop
+ one canonical exact-client runtime/session
```

Once that topology is authoritatively established, worker/job rotation must not routinely destroy it. The owner should retain continuous VNC visibility while research workers attach/release control serially. Prefer reuse of the existing registered client/session through current Gate A -> required rebind -> Gate B rather than repeating bootstrap/login from zero.

The desktop/VNC/client lifetime must be independent from an individual GitHub Actions job. A completed research task normally releases controller authority only; it must not implicitly logout, kill the client, stop X11, stop VNC or clean the canonical state.

This is a target/invariant, not a claim that any historical display/port is current. Preserve until fresh authoritative evidence proves otherwise:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Never hard-code `:98`, `6082`, PID or session as canonical merely because they worked historically. VNC reachability/visibility is not mutation authority.

If registration is absent, route creation only to `canonical_bootstrap`; if only registration lease generation is stale and identity is unchanged, route to reviewed `canonical_rebind`; if registered PID/start identity is stale on the same boot but a full reviewed probe proves exactly one current same-fence target, route only to reviewed `canonical_recovery`; if the authoritative registration is prior-boot and repeated fresh singleton proof establishes a different boot epoch, route only to reviewed `canonical_boot_epoch_recovery`. Never authorize a second logged-in Track A session merely to unblock a lane.

## Safety

Keep Track B isolated. Do not live-observe or mutate PR #303-owned runtime surfaces from unrelated tasks. Never persist VNC/login credentials or owner secrets in prompts, registration or evidence. Do not use owner-funded Codex/OpenAI API/paid AI quota without exact current owner authorization.
