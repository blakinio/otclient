# Module and Extension Model

## 1. Goals

The client is modular without turning frame-critical code into a dynamic plugin graph. Boundaries are enforced by Rust crates, typed contracts, capability negotiation and architecture tests.

## 2. Module classes

### Engine modules

Compile-time crates required by the product:

- platform;
- runtime/jobs;
- transport;
- domain/simulation/world storage;
- renderer;
- UI core;
- input;
- audio;
- assets;
- settings;
- diagnostics.

They are statically composed and may not be unloaded during a session.

### First-party feature modules

Compile-time crates that provide user-facing game functionality:

- enter game;
- character and gameplay-channel selection;
- game interface;
- inventory and containers;
- chat;
- battle list;
- minimap;
- action bars;
- market;
- settings UI.

They may be activated or hidden according to server capabilities, account permissions and product configuration. Compile-time composition avoids dynamic-dispatch costs in hot loops and keeps review/CI deterministic.

### Optional extensions

Third-party or experimental extensions run as WebAssembly guests. They are not required for the initial playable client.

## 3. First-party feature contract

A feature owns:

- feature-specific application state;
- domain subscriptions/read models;
- commands it is authorized to request;
- view models and UI registration;
- settings schema and migrations;
- lifecycle cleanup;
- focused tests.

A feature does not own:

- protocol opcodes;
- socket access;
- authoritative world state;
- renderer internals;
- another feature's private state;
- account credentials.

Representative registration contract:

```rust
pub trait FeatureModule {
    fn descriptor(&self) -> FeatureDescriptor;
    fn register(&self, registry: &mut FeatureRegistry) -> Result<(), FeatureError>;
}
```

Runtime update interfaces should be specialized rather than one universal per-frame callback. Most features react to typed state changes and user actions.

## 4. Feature descriptors

Descriptors are compile-time data and may include:

```text
FeatureId
version
required domain capabilities
required server capabilities
registered panels/actions/settings
persistence scopes
localization bundles
asset dependencies
debug-only flag
```

Server capability negotiation controls availability, not code download or arbitrary execution.

## 5. Communication

Preferred flow:

```text
GameEvent -> simulation/read model -> feature view model -> UI
User action -> feature command -> application validation -> GameCommand -> adapter
```

Features may publish narrow application events. A generic global event bus is not a substitute for typed ownership and should not become an unbounded broadcast channel.

Direct mutation between feature states is forbidden. Shared concepts belong in a lower common contract or an application coordinator.

## 6. State scopes

- `process`: renderer/device/runtime caches;
- `account`: permitted account preferences and directory state;
- `character`: hotkeys/layouts where product policy allows;
- `game session`: targets, containers, entity handles and combat state;
- `widget`: focus, scroll and ephemeral presentation;
- `extension`: isolated private storage.

Every state type declares its scope and reset trigger.

## 7. Lifecycle

First-party features have deterministic phases:

```text
register -> activate -> account/game session bind -> unbind -> deactivate -> shutdown
```

Activation and session binding are different. A feature can remain registered while no game session exists.

All subscriptions, tasks, timers and handles are owned and cancellable. Stale callbacks carry generation/session identity checks.

## 8. UI registration

Feature UI registration is declarative:

- panel descriptor;
- default docking location;
- commands/actions;
- keyboard focus policy;
- settings pages;
- accessibility metadata;
- view-model factories.

`ui-core` provides primitives and layout. `ui-runtime` composes registered surfaces. Neither knows concrete game features at the lower layer.

## 9. WebAssembly extension capabilities

Candidate capabilities:

```text
ui.panel.create
game.read.player.basic
game.read.target.basic
game.command.use_item
game.command.send_chat
audio.play.extension_asset
storage.private
network.approved_endpoint
```

Capabilities are explicit, user/product-policy controlled and revocable. Sensitive capabilities may be unavailable in production.

The host enforces:

- module signature/provenance policy;
- API version compatibility;
- linear-memory limit;
- execution/fuel budget;
- bounded host handles;
- storage quota;
- event-rate limits;
- redacted diagnostics;
- termination on repeated policy violations.

Extensions never receive raw sockets, pointers, process APIs, credential-store access or unrestricted filesystem/network access.

## 10. Versioning

Internal crates evolve together until a public stability milestone. Stable extension APIs use explicit semantic versions and capability discovery.

Breaking extension API changes require:

- versioned host ABI;
- migration/deprecation period when promised;
- compatibility tests;
- documented unsupported behavior.

## 11. Architecture enforcement

A dedicated architecture check must verify at least:

- forbidden crate edges;
- protocol adapters absent from domain/UI dependencies;
- feature crates absent from engine primitives;
- no legacy `src/`, `modules/` or `mods/` dependencies;
- no native dynamic plugin dependency;
- allowed unsafe-code locations;
- cycle-free feature dependency graph.
