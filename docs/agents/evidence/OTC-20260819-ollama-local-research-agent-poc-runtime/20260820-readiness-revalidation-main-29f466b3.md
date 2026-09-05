# TIBIA-RE Ollama PoC — trusted-main readiness revalidation

```yaml
revalidated_at: 2026-08-20T10:35:00+02:00
trusted_main: 29f466b32192641f53ef691759e6589a6a185bd5
runtime_access: none
official_client_touched: false
```

## Trusted-main observation capability changed

The previous `CONTROL_CENTER_EXECUTABLE_OBSERVATION_PATH_NOT_READY` blocker is no longer current.

Trusted main now contains the accepted Surveyor v2 implementation from PR #616 (`6f17e25af655854624b34e0b05f9888618269aba`) and its lifecycle closeout, plus the owner-gated read-only physical operator from PR #618 (`02fce7e25696ffea3e11c4fc89f458e27f47bef4`) and PR #619 lifecycle closeout.

`tools/tibia_re_surveyor/**` is present on trusted main and provides deterministic collect-all output, evidence bundles, runtime observation, privacy scanning and manifest hashing. Therefore repository-side normalized observation is executable rather than design-only.
## Remaining canonical gaps

PR #613 remains Draft/Open contract/design remediation. Its current body explicitly states that Package A remains blocked pending exact-head CI and a fresh independent audit; executable Control Center Package A is therefore not on trusted main.

The accepted Surveyor/operator does not create mutation authority. It has no gameplay/input/process-control path and cannot satisfy the PoC's bounded action-policy, dispatch-time preflight or canonical before/after experiment-artifact responsibilities.

A physical read-only Surveyor v2 run reached exact-target and bridge `3/3` proof but aborted on an unrelated container census timeout. Open PR #620 owns that fail-closed robustness repair. This does not revert repository-side executable observation to design-only, but a successful current physical collect-all is not yet proven by this task.

```yaml
readiness:
  trusted_base_sha: 29f466b32192641f53ef691759e6589a6a185bd5
  normalized_observation_executable: true
  bounded_action_policy_executable: false
  dispatch_preflight_executable: false
  evidence_store_executable: false
  runtime_identity_fencing_executable: true
  stop_cancellation_semantics_executable: true
  chosen_experiment_supported: false
```
## Updated stop reason

The first false prerequisite in prompt order is now the bounded canonical action-policy path. The exact stop reason is:

```text
BLOCKER=CONTROL_CENTER_EXECUTABLE_ACTION_PATH_NOT_READY
```

This PoC must not implement missing broad Control Center Package A/Package D semantics merely to continue. The separate local model-selection gate is also unresolved: none of the five installed models passed the current strict `3/3` proposal schema-consensus shootout.

No physical workflow, runtime admission, client observation or mutation was initiated by this revalidation because the hard readiness gate already stops before live execution.
