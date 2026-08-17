---
task_id: OTC-TEST-A
project_lane: otclient
status: ready
branch: feat/test-a
orchestrator_priority: 10
context_pressure: low
context_growth: stable
context_score: 3
owned_paths:
  - src/a/**
depends_on: []
---
# A
## Context checkpoint
```yaml
checkpoint_version: 1
head: aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa
branch: feat/test-a
status: ready
context_pressure: low
context_growth: stable
context_score: 3
owned_paths:
  - src/a/**
next_action: implement A
```
