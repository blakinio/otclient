---
task_id: OTC2-20260801-secret-lifecycle-remediation
status: active
agent: "GPT-5.6 Thinking"
lane: otclient-v2
track: greenfield-rust
workstream: security
phase: implementation
branch: fix/OTC2-20260801-secret-lifecycle-remediation
base_branch: main
created: 2026-08-01T08:42:00+02:00
updated: 2026-08-01T09:18:00+02:00
last_verified_commit: "5f8ad839f731ff647318f30100c2c07c7e8e7422"
required_base_commit: "86bf2fe08c24925353db9f7c336dbb6dffd40ef0"
risk: high
related_pr: "#124"
depends_on:
  - OTC2-20260731-rust-client-post-w7-audit
  - remediation plan merge 658241fc190ae2c249bba5ae510bed6f0b216cf9
  - remediation plan archive merge 86bf2fe08c24925353db9f7c336dbb6dffd40ef0
blocks:
  - OTC2-20260801-nonblocking-shutdown-remediation
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-secret-lifecycle-remediation.md
  - oteryn-client/crates/identity/src/lib.rs
  - oteryn-client/crates/platform/src/lib.rs
  - oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
shared_path_lease:
  - PR #23 comment transfers only two W7 catalogue rows and one bounded R1 changelog entry to PR #124
modules_touched: []
crates_touched:
  - oteryn-identity
  - oteryn-platform
features_touched:
  - technical-login project-owned secret lifetime and cleanup claims
reuses:
  - oteryn-platform::SecretString
  - existing owned-byte drop-overwrite pattern
contracts_produced:
  - bounded callback-attempt owner with redacted formatting and drop overwrite
  - zeroing project-owned request/response intermediate builders
contracts_consumed:
  - W7 entry contracts
  - merged post-W7 remediation plan
contracts_touched:
  - Identity callback request and decoded query ownership
  - Platform request/DTO serialization ownership
implementation_authorized: true
policy_version: 2
task_kind: implementation
context_pressure: medium
decomposition_decision: phased
execution_mode: codex
performance_evidence:
  - no runtime, latency, throughput or compatibility claim
security_evidence:
  - synthetic-only allocation inventory completed before implementation
  - no real credential, endpoint, private capture or proprietary material used
  - source head 5f8ad839f731ff647318f30100c2c07c7e8e7422 passed exact Windows workspace and supply-chain validation
---

# Goal

Remediate `OTC2-AUD-001` by improving actual project-owned secret cleanup and narrowing documentation to deterministic best-effort overwrite of project-owned buffers only.

# Live preflight

- exact launch `main`: `86bf2fe08c24925353db9f7c336dbb6dffd40ef0`;
- audit, audit archive, remediation plan and remediation-plan archive are merged;
- open PRs #23, #48 and #97 did not own Identity, Platform or the two technical-login evidence paths;
- PR #23 explicitly transferred only the required W7 catalogue-row and bounded changelog edits to PR #124 through a durable coordination comment;
- no dependency, manifest, lockfile, deny-policy, workflow or cross-repository change entered the branch.

# Implemented ownership changes

| Stage/allocation | Implemented disposition |
|---|---|
| PKCE entropy arrays | stack owners overwrite their arrays on drop |
| rejected state/verifier input | `SecretString::new` overwrites rejected input bytes before release |
| authorization URL containing state | one short-lived `Url`, dropped immediately after direct browser launch; external copies documented |
| callback scratch and complete HTTP request | bounded owners overwrite visible project-owned bytes on drop |
| callback target | enclosing non-`Clone` `CallbackAttempt` redacts `Debug`, validates bounds through its constructor and overwrites the target allocation on drop |
| formatted callback URL | removed; the callback path/query is parsed directly without constructing a second sensitive `Url` |
| decoded callback values | code/state/error values enter zeroing ownership immediately after percent decoding |
| verifier handoff | moved directly into token exchange without `.to_owned()` |
| token-exchange form | serialized inside a zeroing text owner and transferred into zeroing request bytes |
| bearer prefix | constructed inside a zeroing byte owner and dropped after the HTTP adapter copies the header |
| token/ticket/session DTO fields | custom deserialization moves each secret string immediately into `SecretString` |
| Gateway JSON request | borrowed DTO serialized directly into a bounded zeroing writer, avoiding `json!` secret copies |
| response body | existing bounded `SecretBytes` preserved and oversized rejected bytes overwritten |
| ureq/TLS/URL/OS/browser storage | explicitly outside the project-owned overwrite guarantee |

# Public/API decision

The final implementation preserves the existing `CallbackAttempt` field shape for source compatibility, but makes the enclosing attempt non-`Clone`, redacts its formatting, validates constructor-created targets and overwrites the owned target allocation on drop. Rust prevents a direct move out of a type implementing `Drop`; callers with mutable field access can still deliberately replace the public field, so the documentation does not claim a universal non-extractable secret type.

No adjacent secret type, new dependency, ADR or substitute producer contract was introduced.

# Acceptance status

- project-owned raw entropy, callback scratch/request/target, decoded query values, verifier handoff, OAuth form, bearer-prefix precursor, Gateway JSON, secret DTO fields and sensitive response bodies now have bounded overwrite behavior where this branch owns the allocation;
- rejected `SecretString` and oversized response inputs are overwritten before release;
- browser URL, allocator/compiler, ureq/TLS, process argument and browser copies are explicitly outside the guarantee;
- errors and formatting remain closed and non-secret;
- no password fallback, persistence, retry, shutdown-state, architecture-policy or asset-open change entered the diff;
- shared documentation changed only after a durable narrow lease transfer from PR #23.

## Context checkpoint

```yaml
checkpoint_version: 1
updated_at: 2026-08-01T09:18:00+02:00
head: 9675a839a2fac9925133c481d35c4c06698206df
branch: fix/OTC2-20260801-secret-lifecycle-remediation
pr: 124
status: validating
context_routes:
  - AGENTS.md and oteryn-client/AGENTS.md
  - oteryn-client/docs/audits/post-w7/REMEDIATION_PLAN.md
  - oteryn-client/crates/identity/src/lib.rs
  - oteryn-client/crates/platform/src/lib.rs
  - oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
owned_paths:
  - docs/agents/tasks/active/OTC2-20260801-secret-lifecycle-remediation.md
  - oteryn-client/crates/identity/src/lib.rs
  - oteryn-client/crates/platform/src/lib.rs
  - oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
proven:
  - Main 86bf2fe08c24925353db9f7c336dbb6dffd40ef0 contained merged planning and archive state at launch.
  - Open PRs 23, 48 and 97 did not own affected Rust or evidence paths.
  - PR 23 transferred only the required catalogue and changelog edits through a durable comment.
  - Raw entropy, callback buffers, query values, form, bearer precursor, Gateway JSON and secret DTO fields now use project-owned overwrite owners.
  - Sensitive callback parsing no longer constructs a formatted URL copy.
  - No dependency, manifest, lockfile, workflow or policy file changed.
  - Source head 5f8ad839f731ff647318f30100c2c07c7e8e7422 passed Rust Client Windows, tests, Clippy, architecture and Supply Chain plus repository CI.
derived:
  - Existing owners and bounded builders were sufficient; a zeroization dependency was unnecessary.
  - Preserving CallbackAttempt field compatibility limits the claim to the enclosing owner and ordinary non-malicious lifecycle use.
unknown:
  - Final documentation/task head CI and review-thread state until emitted checks complete.
conflicts:
  - PR 23 must rebase after PR 124 and preserve the transferred catalogue/changelog corrections.
first_failure:
  marker: final-head-ci-pending
  evidence: Source head passed, but documentation and this task-record commit require exact-head emitted CI.
rejected_hypotheses:
  - Documentation narrowing alone remediates OTC2-AUD-001.
  - Project code can guarantee erasure of URL, TLS, OS or browser copies.
  - A new zeroization dependency is required for this bounded remediation.
changed_paths:
  - docs/agents/tasks/active/OTC2-20260801-secret-lifecycle-remediation.md
  - oteryn-client/crates/identity/src/lib.rs
  - oteryn-client/crates/platform/src/lib.rs
  - oteryn-client/docs/research/technical-login/W7_IDENTITY_EVIDENCE.md
  - oteryn-client/docs/architecture/TECHNICAL_LOGIN.md
  - docs/agents/MODULE_CATALOG.md
  - docs/agents/CHANGELOG.md
validation:
  - command: live main/open-PR/path ownership preflight
    result: PASS
    evidence: main 86bf2fe08c24925353db9f7c336dbb6dffd40ef0; open PRs 23/48/97 inspected.
  - command: bounded source allocation inventory
    result: PASS
    evidence: Identity callback/PKCE and Platform form/header/DTO/Gateway ownership traced before implementation.
  - command: Rust Client workflow on source head 5f8ad839f731ff647318f30100c2c07c7e8e7422
    result: PASS
    evidence: run 30689469936 passed Windows workspace and Supply Chain.
  - command: repository CI on source head 5f8ad839f731ff647318f30100c2c07c7e8e7422
    result: PASS
    evidence: run 30689470007 passed including CI / Required.
blockers:
  - Final exact-head CI and review gate are pending.
next_action: Complete final exact-head CI, review, readiness and merge for PR #124.
```
