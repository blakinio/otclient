# Current Parallel Agent Wave

Status: closed; no worker launch authorized  
Last closed wave: `OTERYN-W6-SYNTHETIC-ASSETS`  
Evidence cut: `main` `a8e95bbce06eda7eb7954843cb7833fbf87160cc`

Live Git, active tasks, open PRs, reviews and exact checks remain authoritative. This document authorizes no implementation lane. A future wave requires a separate planning task, branch and draft PR, accepted plan, and separate planning-task archive before any worker starts or claims a shared-path lease.

## 1. Completed wave history

W1 through W6 are completed and must not be relaunched.

| Wave | Delivery | Lifecycle evidence | State |
|---|---|---|---|
| W1 foundation | merged foundation primitives | separately archived | completed |
| W2 diagnostics/evidence | all authorized lanes merged | separately archived and closed | completed |
| W3 deterministic test support | merged worker | separately archived and closed | completed |
| W4 Windows shell | merged worker | separately archived and closed | completed |
| W5 renderer surface | plan #84/#85, worker #86/#87, closure #88/#89 | all merged and archived | completed |
| W6 synthetic assets | plan #90/#91, worker #92/#94 | implementation merged as `3cea444505bfcc5dc4b08b12d1046ef0c34a0f7a`; task archived | completed |

W6 delivered only the bounded synthetic/original asset schema and compiler slice recorded in the archived W6 task. It did not deliver asset runtime mounting, renderer integration, real game import, production packs, updater/signing, protocol, Identity, networking, UI or production compatibility.

## 2. Released ownership and leases

After PR #94:

- `W6-ASSET` is archived and cannot be relaunched;
- `oteryn-client/crates/asset-types/**` and `oteryn-client/tools/asset-compiler/**` have no active W6 owner;
- the W6 Cargo workspace, `Cargo.lock`, dependency-policy and shared-document lease is released;
- no W6 task owns `deny.toml`, repository layout, Rust workspace documentation, module catalogue, build matrix or changelog;
- any future asset work requires a new bounded accepted task and must consume the merged W6 contract rather than redefine it.

## 3. Current live-state reconciliation

At this evidence cut:

- PR #93 merged as `bdb73eea3c862f31e87fca81317ab3511c3a85a0` and its task was archived separately by PR #95 as `a8e95bbce06eda7eb7954843cb7833fbf87160cc`;
- PR #23 remains a legacy OTUI/Lua presentation-only draft and owns no Rust Identity, session, directory, transport, protocol or application-entry path;
- PR #48 remains isolated operational non-merge work and owns no Rust implementation path;
- no active Rust task or other open PR owns Identity, account session, world directory, game-entry contracts, transport, `protocol-canary`, technical login composition or login E2E paths;
- `docs/agents/CHANGELOG.md` is no longer leased by PR #93 after merge/archive;
- every previous Rust Cargo, lockfile, dependency-policy and shared-document lease is released.

## 4. No accepted current wave

No coordinator may create worker tasks, worker branches, worker PRs or shared-path leases from this closed record.

A future coordinator must first:

1. inspect current `main`, all active tasks, open PRs, reviews and exact CI;
2. read root and nested `AGENTS.md`, the Rust program/workstreams/multi-agent protocol, architecture, lifecycle, audits and current external contracts;
3. create one bounded planning task, branch and early draft PR;
4. publish exact lanes, ownership, producer/consumer declarations, dependencies, lease policy, evidence matrix, blockers and acceptance criteria;
5. merge the plan through repository gates;
6. archive the planning task separately;
7. repeat the live overlap check before launching any worker.

## 5. Exactly one next bounded recommendation

Plan `OTERYN-W7-TECHNICAL-LOGIN` as a separate coordination-only package.

The planning package may evaluate a maximum `1 coordinator + 4 workers` for:

- one producer of typed account/session/directory/game-entry lifecycle contracts;
- one Oteryn Authorization Code + PKCE/account-session/game-entry consumer;
- one minimal Canary Current-profile transport/admission consumer and sole initial transport/protocol interface producer;
- one final technical-login composition/fake-service E2E consumer.

The plan must remain bounded to one explicitly configured Canary world/issuer and one selected character, must not invent missing Platform/Gateway/Canary contracts, and must preserve typed recoverable failure, one-shot credential clearing, exact-version evidence and no production-compatibility claim.

This recommendation is not an accepted wave and pre-claims no path, contract, dependency or shared lease.

## 6. Preserved blockers

- A Rust Identity/Gateway/Canary consumer does not yet exist or prove compatibility.
- Exact current Platform client-facing schemas and status documents require revalidation because some older contract headers conflict with later implemented evidence.
- Canary Current compatibility requires an exact selected producer revision, build string, transport/login evidence and synthetic provenance-safe fixtures.
- General multi-world/gameplay-channel identifier mapping and channel-aware issuer routing remain outside the one-exact-issuer milestone.
- Repository tests cannot prove actual production network, TLS, secret-manager or deployed-revision state.
- No proprietary credentials, packet captures or assets may enter Git.
