# OTC-20260813 Track A live-session handover

```yaml
task_id: OTC-20260813-track-a-live-session-handover
project_lane: otclient
track: official-client-re
status: ready
execution_mode: chat-github
branch: docs/OTC-20260813-track-a-live-handover
owned_paths:
  - docs/agents/tasks/active/OTC-20260813-track-a-live-session-handover.md
  - docs/agents/reports/OTCLIENT-20260813-track-a-live-session-login-handover.md
reuses:
  - docs/agents/TIBIA_RESEARCH_TRACKS.md
  - docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md
depends_on: []
blocks: []
```

## Objective

Persist the material Track A findings from the 2026-08-13 live official-Linux-client session, including the login/session-recovery procedure, Worldmap/action findings, position/pathing correction, and exact claim boundaries, so continuation does not depend on chat history.

## Scope and authority

Documentation only. No official-client runtime mutation, login attempt, secret access, protocol injection, Track B mutation, Oteryn dependency, production effect, or owner-funded AI usage is authorized by this task.

## Acceptance inventory

- Track A and Track B are explicitly distinguished according to `docs/agents/TIBIA_RESEARCH_TRACKS.md`.
- The historical login/session-recovery sequence is documented without credentials or secret values.
- The role of Xvfb, SOCKS/WARP confinement, `proxychains4`, `xdotool`, character-row detection, and post-entry validation is explicit.
- The document does not falsely claim the login sequence is already revalidated on `synology-otclient-01`.
- Decoded Worldmap, native action, downstream message-name, position, collision/pathing, and passive-logging findings are recorded with `PROVEN`, `DERIVED`, `OWNER_OBSERVED`, `UNKNOWN`, or `REVALIDATION_REQUIRED` boundaries.
- No transient PID, heap pointer, external runner/container, secret, password, email address, cookie, token, or proprietary client bytes are promoted as canonical state.

## Evidence status

The repository-owned canonical baseline is `docs/agents/reports/OTCLIENT-20260813-tibia-re-canonical-state.md`. Additional findings in this task are durable handover observations from the 2026-08-13 owner session and must be revalidated inside the canonical Track A namespace before becoming current-runtime proof.

## Next action

Review and merge the companion report, then recover the same login/session flow on `synology-otclient-01` under a Track A-owned namespace and replace `REVALIDATION_REQUIRED` items with repository-owned Linux-runtime evidence.
