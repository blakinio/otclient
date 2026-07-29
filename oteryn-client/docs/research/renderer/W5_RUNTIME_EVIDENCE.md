# W5 Renderer Runtime Evidence

Status: implementation evidence complete; interactive Windows/GPU evidence blocked

## Scope

This record separates deterministic automated evidence for PR #86 from runtime claims that were not observed. The W5 package owns only renderer surface lifecycle and one constant clear/present path.

## Automated evidence

| Evidence | Result | Boundary |
|---|---|---|
| Locked workspace metadata and generated `Cargo.lock` | PASS on hosted Windows | Proves the exact dependency graph resolves on the tested revision. |
| `cargo fmt --all --check` | PASS on hosted Windows | Formatting only. |
| `cargo clippy --workspace --all-targets --locked -- -D warnings` | PASS on hosted Windows | Compiles the Windows adapter and denies warnings; not an interactive launch. |
| `cargo test --workspace --all-targets --locked` | PASS on hosted Windows | Includes deterministic CPU-side surface lifecycle tests. |
| Architecture checker | PASS on hosted Windows | Confirms the `app -> renderer -> foundation` graph and category policy. |
| cargo-deny advisories/licenses/bans/sources | PASS | Confirms the exact reviewed dependency graph and narrow policy exceptions. |
| Repository CI | Required on final exact head | Does not add legacy-runtime compatibility evidence. |

The preliminary fully green Rust graph is run `30468058146` on head `6c0683b4ed702a913b41d170dd6840b360a0a29b`. A later documentation commit supersedes it as merge evidence and must receive a fresh exact-head graph.

## Deterministic lifecycle coverage

The CPU tests cover:

- non-zero configuration and zero-size suspension;
- stale `ProcessGeneration` rejection without partial mutation;
- configured presentation, suboptimal presentation and checked frame counting;
- timeout and occlusion as bounded skips;
- outdated/lost surface decisions with a fixed recovery-attempt limit;
- suspend/resume using the latest non-zero size;
- overflow failure without partial mutation;
- idempotent close and rejection of post-close presentation.

## Interactive evidence blocked

The following were not observed and are not claimed:

- launching and visibly presenting the constant clear color in an interactive Windows desktop session;
- real user-driven resize, minimize/zero-size, restore and DPI changes;
- OS suspend/resume behavior;
- actual outdated/lost surface recovery and device-loss behavior;
- adapter selection across named GPUs, drivers, virtual machines or remote sessions;
- minimum supported Windows release;
- frame time, throughput, memory, power or performance behavior.

Hosted Windows compilation and tests cannot satisfy these items. A later named-environment runtime package must record exact OS build, GPU, driver, session type, observed steps and results before changing any compatibility statement.

## Safety boundaries

- no game/map/entity rendering;
- no asset bytes, textures, shader modules/pipelines or render graph;
- no UI, protocol, identity, network, audio, persistence or extension runtime;
- no direct Win32/windows-sys/raw-window-handle dependency and no unsafe source;
- no renderer singleton, background service, scheduler, reusable async runtime, new worker thread or continuous redraw loop;
- fatal renderer failures use the existing shell close path and renderer resources release before the window.
