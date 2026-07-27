# Canary Current-Profile Evidence Agent Prompt

Use after the common prefix in `WORKER_AGENT_BASE.md`.

```text
Lane: W1-CP
Workstream: WS-R06 evidence preparation only
Task type: documentation/research; no implementation

Goal:

Revalidate the exact current Canary `ProtocolProfileId::Current` evidence needed for a future minimum-playable Rust adapter and produce a provenance-first fixture acquisition plan without adding protocol code, packet constants or external repository changes.

Expected owned paths, subject to live overlap check:

- oteryn-client/docs/research/canary-current/README.md
- oteryn-client/docs/research/canary-current/CURRENT_PROFILE_MATRIX.md
- oteryn-client/docs/research/canary-current/FIXTURE_ACQUISITION_MANIFEST.md
- oteryn-client/docs/research/canary-current/CHANNEL_AND_SESSION_GAPS.md
- one active task record

Forbidden paths:

- oteryn-client/Cargo.toml
- oteryn-client/Cargo.lock
- oteryn-client/crates/**
- oteryn-client/contracts/**
- oteryn-client/tools/architecture-check/**
- .github/workflows/**
- legacy runtime implementation paths
- any Canary or Oteryn Platform write

Required evidence sources:

- current `blakinio/canary` main and open PRs, read-only;
- current `blakinio/otclient` main, accepted foundation audit and cross-repository contracts;
- current `blakinio/Oteryn-Platform` authoritative session contract, read-only, only when relevant;
- primary source files defining client version, profile IDs, feature flags, transport/login layouts, build-string gates and multi-channel world-list behavior.

Deliverables:

1. README.md
   - exact repository revisions and review date;
   - evidence labels PROVEN/SUPPORTED/INFERRED/UNKNOWN/BLOCKED/REJECTED;
   - concise executive findings and one next implementation recommendation.

2. CURRENT_PROFILE_MATRIX.md
   - exact current client protocol version;
   - profile ID and transport/login layouts;
   - relevant feature/capability gates for the MPS;
   - known build-string-specific payload branches;
   - supported/unsupported initial adapter scope;
   - every statement linked to exact source path and commit.

3. FIXTURE_ACQUISITION_MANIFEST.md
   - minimum-playable message families only;
   - producer path, direction, profile/build/capability prerequisites;
   - required positive/minimal/max-bounded/truncated/malformed/wrong-gate/out-of-order fixtures;
   - fixture metadata schema and provenance rules;
   - explicit ban on live credentials/private captures/proprietary content;
   - priority and dependency order, but no packet bytes copied unless synthetic and proven safe.

4. CHANNEL_AND_SESSION_GAPS.md
   - exact distinction among Platform world ID, Canary login-list world ID, product WorldChannelId and process channel_id;
   - current classic multi-channel login behavior;
   - current native Gateway/Game Session issuer limitations;
   - logout/relog/reconnect unknowns and required cross-repository tasks;
   - no proposed server implementation beyond client-facing contract requirements.

Rules:

- external repositories are read-only;
- do not edit CROSS_REPO_CONTRACTS.md from this research lane;
- do not create CAN/OTS tasks unless the lane discovers a concrete implementation-ready atomic contract and the coordinator approves a separate task;
- do not claim a future adapter supports a revision merely because current source was inspected;
- do not freeze opcodes/field layouts in Rust code;
- do not copy assumptions from third-party forks;
- do not broaden scope to all legacy profiles or advanced feature families;
- preserve failed searches and contradictory evidence.

Acceptance:

- exact current revisions and source paths are recorded;
- MPS Current-profile scope is distinguishable from later features and legacy profiles;
- build-string and capability risks are explicit;
- fixture plan is synthetic/provenance-safe and implementation-ready;
- multi-channel/native-session gaps are not disguised as client decisions;
- changed files are limited to the isolated research path and task lifecycle;
- documentation and repository required checks pass on exact head;
- task merges and archives independently.

Final handoff:

Recommend exactly one future WS-R06 package, normally one verified login/session or map message family after required domain/protocol-core producers merge. Do not implement it in this PR.
```
