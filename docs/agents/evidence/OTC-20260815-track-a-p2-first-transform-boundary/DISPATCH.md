# Dispatch contract

```yaml
TASK_ID: OTC-20260815-track-a-p2-first-transform-boundary
TASK_RECORD: docs/agents/tasks/active/OTC-20260815-track-a-p2-first-transform-boundary.md
PROJECT_LANE: otclient
LANE: P2-NETWORK
BASE_MAIN: 8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
BRANCH: research/OTC-20260815-track-a-p2-first-transform-boundary
WORKTREE: github-only://blakinio/otclient/refs/heads/research/OTC-20260815-track-a-p2-first-transform-boundary
OWNED_PATHS:
  - docs/agents/tasks/active/OTC-20260815-track-a-p2-first-transform-boundary.md
  - docs/agents/evidence/OTC-20260815-track-a-p2-first-transform-boundary/**
  - .github/workflows/tibia-official-client-re-p2-first-transform-boundary.yml
  - .github/scripts/tibia-official-client-re-p2-first-transform-boundary.py
DEPENDENCIES:
  - main@8fca1c3eee453d0d4ef8a47e0f15c9dbae491b45
  - coordinator PR #300 head 5e6457b5afd717e3c92bb06a7219d8246c51f3b2 (pinned unmerged accepted-evidence dependency)
```

Ownership was checked against the live Track A Draft set before dispatch: active #302 owns only P0 task/evidence/workflow/script paths; active #303 owns only RUNTIME task/evidence/workflow/script paths; no open P2 Draft or matching `track-a-p2-first-transform-boundary` branch existed.

The task is static-only and disjoint from queued/historical final-socket run `31825417040`.