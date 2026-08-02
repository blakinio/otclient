---
task_id: OTC2-20260801-playability-p1-canary-source-index
status: completed
agent: "P1 Canary source-index worker"
project_lane: otclient-v2
lane: otclient-v2
track: greenfield-rust
workstream: playability-p1-canary-source-index
phase: archived
branch: tools/OTC2-20260801-playability-p1-canary-source-index
base_branch: main
created: 2026-08-01T22:25:00+02:00
completed: 2026-08-02T22:34:30+02:00
archived: 2026-08-02T22:35:00+02:00
implementation_head: "4f59d70175b6795d2e57bc94226c90005a3af136"
required_base_commit: "3887a0b7369e99ad200990d42a5314f1d5531e97"
merge_commit: "67f8af3f5cd4abff53456e207fc374afd1add030"
risk: high
related_pr: 154
implementation_authorized: true
policy_version: 2
task_kind: implementation
execution_mode: github-only
validation_level: heavy
complete_user_facing_feature: false
missing_layers:
  - bounded runtime Canary parsers and encoders
  - controlled packet fixtures and approved staging identity
  - proof that the inspected producer cut equals deployment
shared_path_lease: []
---

# Goal

Generate deterministic exact-source Canary Current protocol and fixture-feasibility evidence without implementing runtime parsing or claiming deployment equality.

# Final acceptance

- [x] standard-library generator and four-test corpus are merged;
- [x] exact `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3` source hashes, release, client version and Current profile features are recorded;
- [x] 347 entries cover 159 client-to-server and 188 server-to-client paths;
- [x] dispatch phases separate livestream-viewer, gameplay-session and server-send evidence;
- [x] 122 literal inbound, 31 inline inbound, 6 explicit no-op and 0 unresolved inbound cases;
- [x] 174 literal outbound and 14 explicit `UNKNOWN` local opcodes;
- [x] four source-defined indirect/orchestrator declarations and zero missing definitions;
- [x] two exact generations are byte-identical;
- [x] fixture metadata forbids credentials, session keys, private captures, proprietary assets and copied producer bodies;
- [x] no workspace, lockfile, architecture, runtime or producer repository mutation;
- [x] protected implementation merge and separate lifecycle archive completed.

## Final evidence

```yaml
implementation:
  pr: 154
  head: 4f59d70175b6795d2e57bc94226c90005a3af136
  exact_base: 3887a0b7369e99ad200990d42a5314f1d5531e97
  merge: 67f8af3f5cd4abff53456e207fc374afd1add030
producer:
  repository: blakinio/canary
  revision: bc0068ab80bbf003e128fce0589b4cc89d2682d3
  release: 3.6.1
  client_version: 1525
validation:
  exact_source:
    run: 30765540499
    job: 91543471615
    result: PASS
  rust_client:
    run: 30765748166
    windows_job: 91544027137
    supply_chain_job: 91544027155
    result: PASS
  repository_ci:
    run: 30765748320
    required_job: 91544158579
    result: PASS
  ready_for_review_ci:
    run: 30765884954
    required_job: 91544510182
    result: PASS
  coordinator_audit:
    changed_paths: 7 exclusive source-index paths
    unresolved_inbound: 0
    missing_definitions: 0
    comments_reviews_threads: clean
remote_execution_cleanup:
  temporary_pr: 179
  state: closed_without_merge
  final_changed_files: 0
blockers: []
next_action: P1 remains open only for a fresh-session exact-head heavy gate, merge and archive of input-actions PR 157.
```
