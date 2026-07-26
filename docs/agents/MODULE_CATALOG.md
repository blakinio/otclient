# OTClient Module and System Catalogue

Last reviewed: 2026-07-26

This catalogue makes reusable work visible across the greenfield Rust client and legacy OTClient. Verify source, tasks, tests and open PR state before use.

## Maintenance contract

Update this file in the same PR that adds or changes a reusable module/crate, public interface, protocol/UI integration point, test utility, platform abstraction, asset format or integration contract.

## Greenfield Rust client

| Module/system | Status | Responsibility/public surface | Primary paths | Reuse/safety notes |
|---|---|---|---|---|
| Greenfield architecture package | active PR #45 | Normative Rust client architecture, workspace plan, lifecycle, protocol boundary, module/security/performance/asset models, audit program and agent prompt | `oteryn-client/**` | New product target. Foundation audit must complete before production workspace bootstrap. Legacy code is evidence only. |
| Rust foundation audit | planned; blocked on PR #45 | Verified product/Canary/Oteryn/assets/performance/platform/test inputs and first bootstrap recommendation | `oteryn-client/docs/audits/foundation/**` | Audit-only; no production crates or speculative constants. |
| Planned Rust workspace | not created | Future apps/crates/features/tools described by repository layout and workstreams | `oteryn-client/apps`, `crates`, `features`, `tools` | Create only after audit gate and in narrow packages. |

## Legacy core client/module areas

| Module/system | Status | Responsibility/public surface | Primary paths | Reuse/safety notes |
|---|---|---|---|---|
| Shipped game modules | maintained legacy | Feature UI/controllers and interactions loaded through manifests | `modules/**` | Extend owning legacy module; do not structurally port into Rust. |
| Optional/custom mods | maintained legacy | Optional behavior outside shipped legacy core | `mods/**` | Not a substitute for core fixes and not the Rust extension model. |
| Protocol and features | maintained legacy | Packet parsing/output, feature flags and game state | `src/client/**`, `modules/game_features/**` | Exact Canary contracts required. Rust work consumes only audited evidence. |
| Protocol game callback guard | maintained legacy | Exact source-session validation through connection/game-end cleanup | `src/client/protocolgamecallbackguard.h`, `src/client/protocolgame.cpp`, `src/client/game.{h,cpp}` | Legacy lifecycle evidence; Rust uses generation-owned session architecture rather than linking this code. |
| Oteryn native identity login | maintained legacy | System-browser PKCE, loopback callback, Platform ticket, Gateway and one-shot handoff | `modules/client_entergame/oteryn_identity*.lua`, session guard, native helpers | Security/contract evidence for audit; Rust implementation is independent. No password fallback. |
| Client assets auto-install | maintained legacy | Secure things/sounds/runtime-extra installation | installer sources and `docs/client-assets-auto-install.md` | Strict hashes/final paths remain mandatory for legacy. Rust uses a new signed pack pipeline. |
| Runtime Stats controls | maintained legacy | Pause/resume legacy performance samples | `src/framework/util/stats.*`, Lua bindings | May help baseline audit; not a Rust diagnostics dependency. |
| User-directory override | maintained legacy | Redirects persisted legacy state | `src/main.cpp`, resource manager | Do not infer greenfield settings/security policy from this behavior. |

## Reusable legacy test infrastructure

| Module/tool | Status | Responsibility/public surface | Source/docs | Reuse notes |
|---|---|---|---|---|
| Client test foundation | maintained legacy | Deterministic C++/Lua builders, fakes, fixtures and loopback | `tests/**` | Useful as audit evidence; Rust workspace gets native Cargo test support. |
| InputMessageBuilder | maintained legacy | Framed parser inputs | `tests/support/builders/**` | Behavior/fixture reference only for Rust. |
| OutputMessageInspector | maintained legacy | Encoded output inspection | `tests/support/builders/**` | Behavior/fixture reference only for Rust. |
| Thing/Tile builders/assertions | maintained legacy | Synthetic legacy map/things | `tests/support/**` | Audit semantics/provenance before creating Rust equivalents. |
| Protocol loopback | maintained legacy | Bounded local socket integration | `tests/integration/protocol/**` | Does not prove Rust adapter compatibility. |

## Entry template

```md
### Module name
- Track: greenfield-rust | legacy-client
- Status:
- Responsibility/public surface:
- Source paths:
- Dependencies/lifecycle:
- Tests:
- Documentation:
- Used by:
- Task/PR:
- Last verified commit:
```
