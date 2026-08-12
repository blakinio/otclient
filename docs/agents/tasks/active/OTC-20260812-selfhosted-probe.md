# OTC-20260812-selfhosted-probe

status: blocked
owned_paths:
  - .github/workflows/selfhosted-probe.yml
  - docs/agents/tasks/active/OTC-20260812-selfhosted-probe.md
modules_touched: []
reuses: []
depends_on: []
blocks: []

Objective: identify the dedicated self-hosted OTClient/OTS execution environment and verify whether an existing Tibia/OTClient runtime can be reached without reading or exposing credentials.

Evidence:
- PR #281 head `424d4b4ababba87304582cc5e32786e3b58bbc22` created a real `Self-hosted OTClient Probe` workflow run.
- Run `31643366053`, job `94271079061`, requested only label `self-hosted`.
- GitHub reports the job as `queued` with `runner_id=null`, `runner_name=null`, `runner_group_id=null`, and `runner_group_name=null`.
- Therefore no self-hosted runner currently available to this repository/workflow has accepted the job. This does not distinguish offline/busy runner from runner registered to another repository/group.
- No secrets or owner-funded AI services were used.

Acceptance:
- self-hosted runner execution is observed from GitHub Actions evidence;
- host/container/process inventory is recorded without secrets;
- no owner-funded AI service is invoked;
- next action is the concrete runtime login test or an exact infrastructure blocker.

Blocker: GitHub cannot assign even a generic `self-hosted` job for `blakinio/otclient`; runtime inventory and Tibia Global login cannot execute until the intended runner is online and available to this repository/workflow.

next_action: make the intended OTClient/OTS runner available to `blakinio/otclient`; then rerun PR #281 probe and continue directly with the runtime login test.
