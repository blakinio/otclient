# OTCLIENT-TIBIA-RE RUNTIME alias

```yaml
alias_prompt_contract_version: 1.0.0
alias: OTCLIENT-TIBIA-RE-RUNTIME
track_id: official-client-re
lane: RUNTIME
researcher_delivery: draft_only
execution_class: synology_physical_runtime
runner: synology-otclient-01
runtime_access: classify_fresh_on_claim_resume
persistent_session_role: canonical_runtime_owner
physical_e2e_required: task_dependent
```

## Resolution

This alias is an additive physical-runtime preset. Load current repository governance plus:

```text
docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md
docs/agents/prompts/OTCLIENT_TIBIA_RE_PROGRAMME.md
docs/agents/TIBIA_RESEARCH_TRACKS.md
docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md
docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md
docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md
docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
docs/agents/programs/OTCLIENT_TIBIA_RE_PARALLEL_RESEARCH_COORDINATION.md
```

Resolve live `main`, current RUNTIME task, PR ownership, authoritative lease/registration state and current runner evidence before any live observation or mutation.

Owner invocation:

```text
Uruchom OTCLIENT-TIBIA-RE-RUNTIME autonomicznie.
```

## First action on every claim/resume

Persist/re-evaluate the complete Track A runtime-admission record and classify exactly one of:

```text
read_only
ephemeral_isolated
canonical_reuse_or_mutation
canonical_bootstrap
canonical_rebind
canonical_recovery
canonical_boot_epoch_recovery
```

For physical canonical work, do not proceed until the current class's authority/identity gates pass. Historical runtime facts never substitute for current admission.

## Persistent Synology desktop/session contract

The desired canonical physical topology is:

```text
synology-otclient-01
  -> one long-lived canonical X11 desktop
  -> one long-lived private VNC service bound to that same desktop
  -> one canonical exact-client runtime/session kept reusable across worker/job rotation
```

Treat desktop, VNC and client/session lifetime as programme infrastructure, not worker lifetime. GitHub Actions jobs and research agents attach to/release control of the existing runtime; they must not routinely create and destroy a fresh desktop/session on every invocation.

When a healthy authoritative registered runtime already exists:

1. acquire current Gate A authority;
2. perform reviewed generation rebind if required;
3. pass Gate B against the exact registration and current process/display/window/VNC mapping;
4. reuse the same desktop/client/session;
5. perform only the bounded task stimulus/observation;
6. release controller authority while leaving the canonical desktop/VNC/client alive and idle unless a reviewed recovery/destructive operation explicitly requires otherwise.

Do **not** routinely logout, close the client, kill X11, stop/recreate VNC, delete canonical state or rebuild the login path merely because a task, workflow or agent session ended.

If the client is still authenticated/IN_GAME and safe to leave idle, preserve that session so the next authorized RUNTIME worker can reacquire it without repeating login. Never perform autonomous gameplay merely to keep it active.

If the client is disconnected or at login/character-select while the persistent desktop/VNC is healthy, prefer bounded recovery inside the existing desktop. Preserve the desktop and VNC service. Restart/replace the client only when technically required and only through the current reviewed recovery/bootstrap authority path.

If the authoritative registration is absent, ordinary reuse must refuse launch. Initial creation belongs only to `canonical_bootstrap` and only when a reviewed current implementation plus separate live authorization/gates allow it. Never create a second logged-in Global session as a shortcut.

If registration exists and only the lease generation is older while runtime identity is unchanged, use reviewed `canonical_rebind`. If the authoritative adoption PID/start identity is stale on the same boot but one current exact same-fence target is fully proven, use only reviewed `canonical_recovery`. If the registration is from a prior boot and repeated fresh singleton proof establishes a different current boot epoch, use only reviewed `canonical_boot_epoch_recovery`; never use rebind for identity replacement and never manually edit `runtime-registration.json`.

## Stable owner VNC visibility

The owner should be able to keep a continuous private VNC view of the same canonical desktop independently of worker/job turnover.

- The VNC service should remain running while the canonical desktop exists.
- The endpoint/mapping must be derived from current authoritative runtime evidence/registration and freshly proven when required; never guess historical values.
- VNC availability or a visible window is observation evidence only and never mutation authority.
- Do not commit or expose VNC passwords, login credentials, cookies, session tokens or private connection secrets.
- Do not expose VNC publicly; preserve the current private owner-access path.
- An owner viewer connecting/disconnecting must not be treated as a runtime state transition or worker authority change.

Current non-claims remain until fresh authoritative proof:

```yaml
display_98_current_canonical_status: UNKNOWN
rfb_6082_current_backend_mapping: UNKNOWN
current_exact_client_pid: NOT_REGISTERED
current_exact_client_session: NOT_REGISTERED
```

Do not hard-code `:98`, `6082`, PID or session as canonical.

## Physical evidence provider

RUNTIME is the serialized provider of real display/input/login/relogin/walking/clicking/restart and physical gameplay evidence for P2/P0/P1. Prefer one bounded experiment that answers the requesting lane's discriminator and persist durable evidence so other lanes do not need independent physical sessions.

Research output remains `DRAFT_NOT_PROMOTED`; coordinator review is required before canonical promotion/merge.

Keep Track B isolated. Do not mutate or live-observe PR #303-owned runtime surfaces unless the exact current task owns/authorizes them. Do not use owner-funded Codex/OpenAI API/paid AI quota without exact current owner authorization.
