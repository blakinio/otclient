# OTC-20260812-selfhosted-probe

status: active
owned_paths:
  - .github/workflows/selfhosted-probe.yml
  - docs/agents/tasks/active/OTC-20260812-selfhosted-probe.md
modules_touched: []
reuses: []
depends_on: []
blocks: []

Objective: identify the dedicated self-hosted OTClient/OTS execution environment and verify whether an existing Tibia/OTClient runtime can be reached without reading or exposing credentials.

Acceptance:
- self-hosted runner execution is observed from GitHub Actions evidence;
- host/container/process inventory is recorded without secrets;
- no owner-funded AI service is invoked;
- next action is the concrete runtime login test or an exact infrastructure blocker.
