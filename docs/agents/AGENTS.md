# Agent execution instructions

Before creating, claiming, resuming, updating, handing off, or closing any task under this directory:

1. Read `EXECUTION_PROTOCOL.md`.
2. Read `PROJECT_LANES.json`.
3. Select or preserve the correct `project_lane`; use `otclient-v2` for the OTClient v2 project and `otclient` for the existing project.
4. New OTClient v2 task IDs should use the `OTC2-` prefix; existing `OTC-` task IDs remain valid for the original project.
5. Treat the task record and Git/PR state as durable; treat the worker session as disposable.
6. Execute one bounded phase per session and persist a checkpoint before a long-running or failure-prone operation.
7. Do not remain active while waiting for CI, dependencies, external evidence, deployment, or a user reply.
8. On a blocker, preserve coherent work, record `status`, evidence, blocker and exactly one `next_action`, then end the session.
9. Record `execution_mode` and let the worker decide whether Chat/GitHub or Codex is appropriate.
10. At a synchronization barrier, run `python tools/agents/control_room.py --format markdown` and escalate only material decisions.

These rules supplement the repository root `AGENTS.md`. When rules overlap, follow the more restrictive safety requirement.
