# Cold-auth QMeta static dispatch

Status: **DRAFT / NOT PROMOTED**

```yaml
TASK_ID: OTC-20260818-native-cold-auth-qmeta
TASK_RECORD: docs/agents/tasks/active/OTC-20260818-native-cold-auth-qmeta.md
PROJECT_LANE: otclient
LANE: COVERAGE-AUDIT
BASE_MAIN: bd167a8a9b4192b3c87c21423e2af37e897f5e79
BRANCH: research/OTC-20260818-native-cold-auth-qmeta
WORKTREE: github-only-isolated-branch
OWNED_PATHS:
  - .github/workflows/track-a-native-cold-auth-qmeta.yml
  - docs/agents/tasks/active/OTC-20260818-native-cold-auth-qmeta.md
  - docs/agents/evidence/OTC-20260818-native-cold-auth-qmeta/**
DEPENDENCIES:
  - blakinio/otclient#498
  - blakinio/otclient#475@135c808d40934e3f9dfafe8cb0efb83aade92858
ROUTING_CONTRACT: docs/agents/programs/OTCLIENT_TIBIA_RE_HYBRID_EXECUTION_ROUTING.md
EXECUTION_CLASS: github_hosted
RUNTIME_ACCESS: none
PERSISTENT_SESSION_ROLE: none
PHYSICAL_E2E_REQUIRED: false
```

Objective is strictly native cold authentication below the visual form. The worker must not use or validate login through GUI controls, OCR, screenshots, coordinate clicking, Tab/Return submission, or blind input.
