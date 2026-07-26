# Foundation Risk Register

Scale:

- likelihood: low / medium / high;
- impact: low / medium / high / critical;
- gate: earliest program gate that must close the risk.

## Product and scope

| ID | Risk | Likelihood | Impact | Evidence/state | Mitigation/owner | Gate |
|---|---|---:|---:|---|---|---|
| R-001 | Greenfield scope expands into full feature parity before a playable vertical slice | high | high | `SUPPORTED` by size of legacy feature surface | enforce MPS inventory, one observable package/PR, defer Later features; program owner | every gate |
| R-002 | Agents recreate legacy module/global architecture in Rust | medium | critical | known legacy structure and migration pressure | nested `AGENTS.md`, architecture-edge CI, no legacy runtime dependency; WS-R01/WS-R04 | Gate 1 |
| R-003 | Empty placeholder crates become de facto public architecture | medium | medium | audit gate explicitly prohibits them | create only package-required paths; catalogue and ADR review; WS-R01 | Gate 1 |
| R-004 | Legacy client maintenance is abandoned before Rust parity | medium | high | dual-client period required | preserve legacy architecture/workstreams and separate tasks; repository owner | production migration |

## Protocol and server compatibility

| ID | Risk | Likelihood | Impact | Evidence/state | Mitigation/owner | Gate |
|---|---|---:|---:|---|---|---|
| R-010 | Canary assumptions copied from another client or stale source | high | critical | protocol frequently version/build gated | exact selected Canary commit, producer paths, golden/malformed fixtures and shared tasks; WS-R06 | Gate 5 |
| R-011 | `Current` profile changes after adapter selection | high | high | current main evolves and build-specific branches exist | exact pair matrix; fail unsupported capabilities; periodic revalidation; WS-R06 | Gate 5+ |
| R-012 | One numeric client version is treated as complete compatibility | medium | high | 15.25 build prefixes change payload shape | include build string/profile/feature mask in session and fixtures; WS-R05/R06 | Gate 5 |
| R-013 | Wire-format details leak into game domain/UI | medium | critical | common shortcut during adapter implementation | architecture checker; typed adapter boundary; review shared events; WS-R01/R04/R06 | Gate 1 onward |
| R-014 | Malformed packet causes panic, allocation spike or busy loop | medium | critical | external untrusted bytes | bounds, checked arithmetic, negative fixtures/fuzzing, fatal-session taxonomy; WS-R05/R06 | Gate 5 |
| R-015 | Initial Rust adapter attempts all legacy protocol profiles | medium | high | Canary supports multiple profiles | Current 15.25 only for MPS; later independent packages; WS-R06 | Gate 5 |
| R-016 | Native Oteryn protocol is designed prematurely from client assumptions | medium | critical | no accepted native game protocol contract | no `protocol-oteryn` implementation before cross-repo ADR/contract; WS-R07 | Gate 8 |

## Gameplay channels and sessions

| ID | Risk | Likelihood | Impact | Evidence/state | Mitigation/owner | Gate |
|---|---|---:|---:|---|---|---|
| R-020 | Gameplay channels are confused with network streams | medium | high | confusion occurred in design discussion | typed `WorldChannelId`, separate terminology/tests; WS-R03/R05 | Gate 4 |
| R-021 | Platform world ID, login-list world ID and Canary channel ID are silently equated | high | critical | current contract explicitly says they differ | shared mapping contract before native channel tickets; WS-R03/R06 + Platform/Canary | Gate 4/5 |
| R-022 | Current Gateway v1 is assumed to route arbitrary multi-channel sessions | high | critical | contract explicitly supports one exact issuer/process | fail closed; controlled single-issuer E2E only; new cross-repo protocol for channels | Gate 4/5 |
| R-023 | Relog retains old target/container/entity/task state | medium | high | session replacement bugs exist in legacy history | session-scoped owners, generation IDs, 100-cycle tests; WS-R02/R04/R13 | Gate 3/5 |
| R-024 | Old Channel 1 callback disconnects/mutates Channel 2 | medium | critical | legacy regression class proven | exact source/session generation on every callback; race tests; WS-R02/R05 | Gate 3/5 |
| R-025 | Initial one-shot credential is replayed for reconnect or new channel | medium | critical | explicit security invariant | distinct credential types; consume/clear; replay negatives; WS-R03/R05 | Gate 4/5 |
| R-026 | Client cannot know whether logout committed after timeout | medium | high | distributed lifecycle uncertainty | exact server result/resume/fencing contract; do not guess; WS-R03/R06 cross-repo | Gate 5 |
| R-027 | Same character becomes active on two channels | low/medium | critical | server cluster session lock exists but native route integration incomplete | server-authoritative lease/fencing E2E; client disables new actions while relogging; cross-repo | Gate 5/production |

## Identity and security

| ID | Risk | Likelihood | Impact | Evidence/state | Mitigation/owner | Gate |
|---|---|---:|---:|---|---|---|
| R-030 | Main password fallback reappears in Oteryn flow | low/medium | critical | explicit legacy/target invariant | no password fields in Oteryn UI/model, negative tests, fail closed; WS-R03 | Gate 4 |
| R-031 | Stale/forged/duplicate loopback callback completes wrong transaction | medium | critical | desktop OAuth attack surface | strict state/path/origin/generation and one completion; WS-R03 | Gate 4 |
| R-032 | Tokens/tickets leak to features, logs, replay or crash reports | medium | critical | broad diagnostics/extensions risk | typed secret wrappers, redaction at creation, no Debug/Serialize, tests; WS-R03/R14 | Gate 1/4 |
| R-033 | Credential rotation/drift causes outage or unsafe fallback | medium | high | current service credentials have current/previous windows | server-managed rotation contract, health checks, no client fallback; Platform/Canary ops | production |
| R-034 | Bounded pre-hardening E2E is mistaken for production proof | medium | high | authoritative contract warns against it | exact hardened deployed revisions/TLS/network/secret evidence before enablement | Gate 5/production |
| R-035 | Dependency/FFI vulnerability undermines Rust safety | medium | high | graphics/window/audio stacks contain native/unsafe boundaries | deny/advisory/license policy, isolate unsafe modules, update review; WS-R01/owners | Gate 1 onward |

## Assets and updater

| ID | Risk | Likelihood | Impact | Evidence/state | Mitigation/owner | Gate |
|---|---|---:|---:|---|---|---|
| R-040 | Proprietary game assets are committed or redistributed without rights | high | critical | technical availability exists, legal approval absent | explicit prohibited list, provenance registry, local importer/approved source only; WS-R09/legal | before real assets |
| R-041 | Technical download source is treated as license evidence | high | critical | legacy installer uses external packages | separate rights determination from installer behavior; WS-R09/legal | before real assets |
| R-042 | Asset parser/archive allows path traversal, overflow or bomb | medium | critical | untrusted packages and compression | bounded importers, path/symlink rejection, fuzz/security corpus; WS-R09 | Gate 2/7 |
| R-043 | Mixed client/protocol/asset versions enter gameplay | medium | critical | several versioned sources | signed compatibility manifest and pre-entry gate; WS-R09/R15 | Gate 2/7 |
| R-044 | Runtime uses staging/cache as authoritative data | low/medium | high | known legacy installer risk | immutable verified active set, atomic switch/rollback; WS-R09/R15 | Gate 2/7 |
| R-045 | Atlas/texture strategy is frozen without real statistics | high | medium/high | real asset counts/dimensions blocked | synthetic benchmark first; non-content inventory after rights approval; WS-R08/R09 | Gate 2 |
| R-046 | Update system executes unverified code | low/medium | critical | launcher is separate trust boundary | signed manifest+hash, staging, atomic activation, rollback, no TLS-only trust; WS-R15 | Gate 7 |

## Performance and runtime

| ID | Risk | Likelihood | Impact | Evidence/state | Mitigation/owner | Gate |
|---|---|---:|---:|---|---|---|
| R-050 | Rust rewrite is assumed faster without measurements | high | high | no baseline exists | P0–P8 scenes, percentile evidence, named hardware; WS-R14 | Gate 2 onward |
| R-051 | Average FPS hides recurring p99 stalls | high | high | common benchmark failure | frame-time distribution and traces; performance policy; WS-R08/R14 | Gate 2 onward |
| R-052 | Broad mutex/global event bus recreates contention/coupling | medium | critical | convenient initial design | one-writer simulation, bounded queues, snapshots, architecture review; WS-R02/R04 | Gate 1/3 |
| R-053 | Asset/shader work blocks frame loop | medium | high | streaming/pipeline creation cost | worker upload, warm-up, budgets, P5 tests; WS-R08/R09 | Gate 2 |
| R-054 | UI retained tree grows without virtualization/dirty propagation | medium | high | large chat/battle/market datasets | UI virtualization fixtures and p95 layout budgets; WS-R10/R13 | Gate 6 |
| R-055 | Queue backlog grows unbounded during bursts/disconnects | medium | critical | async/network/worker design | bounded queues, coalescing/backpressure/fatal policy and metrics; WS-R02/R05 | Gate 1/5 |
| R-056 | Concrete hardware claims are selected without a runnable build | high | medium/high | no measurements available | keep tiers unresolved until P-scenes; product owner approval; WS-R14 | Gate 5/Beta |
| R-057 | GPU runner success is treated as physical hardware acceptance | medium | medium | CI noise/virtualization | named physical Windows matrix required for product claims; WS-R08/R14 | Beta/production |

## UI, input and accessibility

| ID | Risk | Likelihood | Impact | Evidence/state | Mitigation/owner | Gate |
|---|---|---:|---:|---|---|---|
| R-060 | Native UI core absorbs feature-specific policy | medium | high | broad UI framework scope | panel/view-model registries; no feature dependencies in core; WS-R10 | Gate 2/6 |
| R-061 | DPI/IME/raw-input behavior is discovered late | medium | high | Windows-specific complexity | early platform/UI spikes and matrix tests; WS-R02/R10/R11 | Gate 1/2 |
| R-062 | Original/licensed visual assets arrive after UI assumptions freeze | medium | medium/high | asset rights unresolved | synthetic design system first; explicit asset contracts; WS-R09/R10 | Gate 2/6 |
| R-063 | Accessibility/localization is bolted on after widget APIs stabilize | medium | high | new UI surface | accessibility tree, keyboard/focus and text expansion in core acceptance; WS-R10 | Gate 2 |

## Testing, CI and operations

| ID | Risk | Likelihood | Impact | Evidence/state | Mitigation/owner | Gate |
|---|---|---:|---:|---|---|---|
| R-070 | Tests require live server/proprietary assets and become non-reproducible | high | high | current evidence gap | synthetic wire/domain/asset/replay fixtures and fake services; WS-R06/R09/R14 | Gate 2/3/5 |
| R-071 | Two agents edit shared events/snapshots/schemas in parallel | medium | high | high-contention contracts identified | one owner per shared contract, narrow tasks and dependency PRs; coordination | every gate |
| R-072 | Cargo/CI policy is weakened to merge early code | low/medium | high | pressure during bootstrap | dedicated WS-R01 ownership; no feature PR CI edits; root merge gate | Gate 1 onward |
| R-073 | External repository revisions change after audit | high | medium/high | active Canary/Platform development | implementation task revalidates live main/PRs and records exact pair | every cross-repo package |
| R-074 | Audit unknowns are later cited as proven facts | medium | high | many blocked areas | preserve evidence labels in task/fixtures/contracts; review citations | Gate 1 onward |
| R-075 | Audit itself becomes a permanent design substitute | medium | medium | docs can become stale | source/ADRs/contracts remain authoritative; revalidate at package start | every gate |

## Highest-priority blockers

1. **R-021/R-022** — explicit channel identifier and native issuer-routing contract.
2. **R-040/R-041** — real game asset rights/provenance.
3. **R-010/R-012** — exact Canary Current-profile commit/build/fixtures.
4. **R-034** — hardened deployed native-auth E2E.
5. **R-050/R-056** — reproducible runtime baseline and hardware tiers.

None blocks the narrow WS-R01 workspace/toolchain bootstrap recommended by this audit.
