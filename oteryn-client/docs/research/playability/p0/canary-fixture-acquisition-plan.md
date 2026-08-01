# P0 Canary Fixture Acquisition Plan

Status cut: client repository `main@9c03a448457b1715818e094fdfdeade4a1450434`  
Producer cut inspected: `blakinio/canary@bc0068ab80bbf003e128fce0589b4cc89d2682d3`  
Producer release/profile: Canary `3.6.1`, client `1525`, `ProtocolProfileId::Current`  
Lane: `OTC2-20260801-playability-p0-canary` / PR #140  
Capture, deployment and implementation authorized: **false**

## 1. Objective

Define a safe, reproducible evidence chain for exact Canary Current packet layouts, ordering and state dependencies without committing credentials, session keys, private traffic, proprietary assets or unsupported hand-written opcode guesses.

Fixtures exist to prove a bounded parser/encoder contract. They do not authorize connection to official services, anti-cheat work, private-user capture or redistribution of protected content.

## 2. Evidence precedence

For a future client protocol package, evidence authority is:

1. exact accepted Canary source commit, build/profile and configuration;
2. exact producer unit/integration tests or controlled source-derived encoder output;
3. project-owned controlled Canary instance with approved synthetic account/state;
4. restricted private capture used only to resolve a source/layout/order conflict;
5. minimized original synthetic fixture derived from accepted facts;
6. legacy client behavior as supporting evidence only.

A private capture or legacy parser cannot silently override the exact accepted producer source. A source declaration alone cannot prove runtime configuration/order when feature gates or state alter the emitted sequence.

## 3. Fixture classes

### 3.1 Source-derived original synthetic fixtures

Preferred for deterministic parser development.

Method:

- pin exact Canary commit/profile/client build;
- identify one send/parse method and its direct layout gates;
- construct project-created values at safe bounds;
- encode the exact producer layout using a test-only producer helper or an independently reviewed original fixture builder;
- record expected normalized domain event/command;
- include positive, boundary and malformed variants;
- never copy a proprietary payload or user data.

Suitable first families:

- map/tile minimal records;
- creature known/unknown lifecycle;
- movement/position/speed;
- player health/mana/stats/skills/conditions;
- inventory/container minimal records;
- channel/message classifications;
- attack/follow/fight modes;
- profile/build feature flags.

### 3.2 Producer test-hook fixtures

When a layout is deeply stateful or difficult to reconstruct safely, add a separate Canary task after authorization to expose a test-only deterministic encoder or observable output buffer.

Requirements:

- separate producer repository task/branch/PR;
- no production behavior change unless separately justified;
- fixed synthetic state and deterministic output;
- exact profile/build/configuration input;
- bounded outputs and no credentials/private values;
- producer CI and review;
- exported fixture manifest/hash consumed by the client task;
- lifecycle archive in the producer repository.

Client workers do not modify `blakinio/canary` under this P0 task.

### 3.3 Controlled project-owned runtime fixtures

Use only when source-derived tests cannot prove sequence, compression, stateful known-creature behavior or build-specific layouts.

Required environment:

- project-owned isolated non-production Canary instance;
- exact server binary/source/config/profile/build recorded;
- approved disposable synthetic account/character;
- original/project-approved asset/runtime data;
- deterministic test map/entities/items/features;
- network access limited to the test operator/harness;
- capture authorization, retention and deletion approved;
- no unrelated users or private conversations.

Capture only the minimum scenario and direction needed. Prefer server-side pre-encryption output/test hook over decrypted network capture.

### 3.4 Restricted private captures

Last-resort diagnostic evidence only.

Allowed purpose:

- confirm disputed ordering/field shape/compression behavior at a controlled project-owned instance;
- compare exact source expectation with emitted bytes;
- derive a sanitized fact/minimized synthetic fixture.

Never commit or publish:

- account session values;
- OAuth codes/tokens;
- game login tickets or game session credentials;
- XTEA/session keys or full decrypted streams;
- IP addresses/private hostnames;
- character/private chat/user data;
- proprietary asset bytes;
- unrelated packets.

The raw capture remains in a restricted artifact store with owner, readers, retention and deletion date. Git receives only approved hashes, structural facts and independently generated synthetic bytes.

## 4. Fixture manifest

Every fixture or restricted evidence item has a machine-readable companion record:

```text
fixture_id
fixture_revision
capability_family
scenario_id
producer_repository
producer_commit
server_release
client_version_and_build_string
protocol_profile
transport_profile
configuration_hash_or_sanitized_identifier
message_direction
source_method_and_path
numeric_opcode_from_generated_source_index
state_and_order_prerequisites
feature/build gates
input_value_summary without secrets/private data
encoded_length/hash
expected normalized event/command or stable error
positive/boundary/negative classification
provenance and generator/tool revision
privacy/proprietary classification
committable or artifact-only
review/approval
supersedes/superseded_by
```

The fixture bytes and manifest must agree on exact hash. A fixture missing its producer cut/profile/build and source method is not compatibility evidence.

## 5. Acquisition sequence

### Phase 0 — generated source index

Before fixture creation, mechanically index exact `protocolgame.cpp/.hpp` and profile sources:

- direction;
- numeric opcode;
- handler/send method;
- profile/build/feature gate;
- state prerequisite;
- layout fields and bounded counts;
- direct source dependencies;
- existing producer tests.

Review the index against the exact commit. Store the full generated output as an artifact or focused evidence document, not as a manually edited public API.

### Phase 1 — bootstrap and map spine

Acquire the smallest coherent sequence:

1. Current transport/challenge/login profile fixture;
2. first accepted game-session packet sequence after authentication;
3. initial map description with one floor/tile/local player;
4. required player state/side-system packets around that sequence;
5. one clean session-end/logout.

The sequence manifest records exact ordering, optional/conditional packets and state transitions. Do not use only a standalone map payload if parser correctness depends on known-creature or profile state.

### Phase 2 — minimum visible world

Fixtures:

- tile with no/one/multiple stack entries;
- known and unknown creature add;
- creature movement/removal/teleport;
- item/appearance/effect/projectile minimal and bounded cases;
- floor/view edge updates;
- speed/health/basic player state;
- client movement/turn commands and authoritative updates.

Requires approved synthetic appearance/resource mapping from asset work.

### Phase 3 — core gameplay

Fixtures grouped independently:

- look/use/use-with/move item;
- inventory/equipment/container open/update/close/seek;
- chat local/channel/private/NPC;
- attack/follow/fight modes and creature combat feedback;
- stats/skills/conditions/cooldowns/death;
- party/base social where classified.

Each group has its own parser/encoder package and state harness.

### Phase 4 — daily/exact-profile systems

Only after product selection:

- depot/stash/quick loot;
- NPC shop/player trade/market;
- VIP/guild/team finder;
- quests/prey/task hunting;
- bestiary/charms/cyclopedia/bosstiary;
- imbuement/forge;
- vocation/Monk/weapon proficiency;
- taskboard/soul seals/wheel/gems;
- sound/ambient/modern presentation-support packets.

Build-specific layouts require fixtures for every supported build string, not one generic Current sample.

## 6. State harness requirements

A parser test harness tracks explicit state rather than parsing packets in isolation:

- selected protocol/profile/build and feature mask;
- transport sequence/compression state where tested;
- session/domain generation;
- map viewport/floor context;
- known-creature cache;
- item/appearance registry version;
- open container/channel/trade/market/modal context as relevant;
- local player identity and accepted capabilities;
- expected next/allowed message families;
- bounded allocation/depth/count budgets.

Unexpected state/order produces a stable typed error or explicit recovery action. It must not silently reinterpret a payload as another profile/build layout.

## 7. Positive and boundary fixture rules

For each variable-width/count field include:

- empty where valid;
- one entry;
- representative multiple entries;
- exact accepted maximum or bounded near-maximum generated safely;
- minimum/maximum numeric value where semantically valid;
- supported optional feature absent/present;
- known/unknown creature or resource path where applicable;
- supported build-specific short/long shape.

Fixtures should be small and purpose-specific. Large world/session recordings are poor unit fixtures and belong only in restricted replay evidence.

## 8. Negative corpus

Every external parser family needs minimized cases for:

- empty/truncated at each field boundary;
- trailing bytes where the frame/layout must be exact;
- oversized count/string/list/depth/dimension;
- arithmetic overflow/range conversion;
- duplicate or invalid identifier/reference;
- impossible position/floor/direction/state;
- unknown item/appearance/message/classification;
- known-creature cache mismatch;
- stale session/entity/container/resource generation;
- unsupported profile/build/feature gate;
- wrong short/long build-specific shape;
- invalid UTF-8/text/control/markup policy where relevant;
- malformed compressed/encrypted frame in transport tests;
- message received before prerequisite bootstrap/open-state;
- repeated terminal/session-end packet;
- uncertain post-write command replay.

Fuzzing/property tests may expand this corpus, but retained regressions remain minimized and source-linked.

## 9. Transport evidence

Current transport facts from the producer profile:

- modern block-count outer length;
- modern padding-byte encrypted layout;
- sequence checksum inbound/outbound;
- official compression;
- sequence high bit signals compression;
- server challenge before login.

Transport fixtures are separate from domain packet fixtures:

- frame boundary/length/checksum/sequence;
- encrypted padding and exact payload extraction;
- compressed and uncompressed frames;
- partial reads/writes and multiple frames;
- sequence wrap/mismatch/duplicate/replay behavior from source evidence;
- terminal/connection close.

Raw network fixture storage must not include real keys or credentials. Use project-created deterministic test keys/bytes or producer test hooks.

## 10. Build/profile fixture matrix

For this programme the target begins with:

```text
ProtocolProfileId::Current
CLIENT_VERSION 1525
exact supported client build string(s): UNKNOWN until deployment/product selection
```

The source explicitly gates weapon proficiency detail layout for confirmed `15.25.794c2e` and `15.25.d96c64` prefixes and keeps unknown 15.25 builds on the shorter shape. Therefore:

- every accepted build string gets a named fixture row;
- unknown build behavior is tested separately;
- no client parser assumes all 15.25 payloads are byte-identical;
- future profile/build additions require separate fixtures and capability registry entries;
- legacy 11.00/8.60 profiles are outside the initial Rust Current target unless separately authorized.

## 11. Source-to-domain review

Each fixture review answers:

- What exact producer method/layout does this represent?
- Which fields are wire-only and disappear after validation?
- Which stable domain identifier/event/command results?
- What bounds and errors are enforced before allocation/state mutation?
- What state/order prerequisite exists?
- What stale-generation behavior is required?
- What capability/build/profile gates apply?
- Does UI/renderer/audio see only a view model/snapshot/intent?
- Is the fixture legally and privacy safe?

A wire fixture cannot become a public domain model by convenience.

## 12. Artifact and Git policy

### Committable

- original generated synthetic packet/frame bytes;
- fixture manifests without secrets/private endpoints/data;
- minimized malformed cases;
- exact public source commit/path/method references;
- hashes and sanitized expected results;
- producer test helpers after separate authorized merge.

### Restricted artifact-only

- controlled full traces;
- packet captures;
- detailed server/client logs;
- binaries/builds;
- private fixture corpora;
- screenshots/video containing controlled environment data.

### Prohibited

- official-service captures;
- third-party/private-user traffic;
- credentials/session keys/tickets/tokens;
- proprietary asset payloads;
- personal/private chat/data;
- anti-cheat reverse engineering or bypass material;
- unknown-origin fixtures.

## 13. Fixture production ownership

Recommended ownership:

- generated source index — one Canary protocol evidence task;
- producer deterministic test hooks — separate Canary repository tasks by bounded family;
- Rust fixture manifest/schema/harness — one client protocol-test-support producer;
- each packet family fixture — owned by its protocol package;
- restricted controlled runtime capture — release/E2E task with security/operations authorization;
- approved appearance/resource fixtures — asset producer;
- scenario mapping — P0/P1 coordinator using accepted reports.

No two workers publish competing fixture manifest, domain event/command or profile/build registry types.

## 14. Initial fixture backlog

Priority order:

1. Current profile/transport/challenge/login frame facts;
2. exact first post-admission bootstrap sequence;
3. minimal map/floor/tile/local-player;
4. known/unknown creature lifecycle;
5. movement/turn/teleport/speed;
6. base player health/mana/stats/skills/conditions/session end;
7. item/appearance/effect/projectile minimal set;
8. inventory/equipment/container;
9. chat/channel/private/NPC;
10. attack/follow/fight modes/combat feedback;
11. selected social/economy families;
12. selected modern build-specific feature families.

Only 1–6 are likely prerequisites for the first M2 vertical slice, subject to exact source order and product decision.

## 15. Blockers requiring producer or owner action

- exact deployed Canary commit/configuration/profile/build string must be named;
- a generated numeric dispatch/layout index does not yet exist;
- exact bootstrap order needs source tracing or controlled deterministic output;
- producer test hooks may be required for deeply stateful packets;
- approved synthetic appearance/item/resource mappings depend on asset decisions;
- controlled server/account/capture access requires operations/security authorization;
- release-required modern feature families require product classification.

## 16. P0 result

A safe fixture path exists without using official services or committing private/proprietary traffic: exact-source index → deterministic producer/synthetic fixtures → controlled runtime evidence only for unresolved state/order/build behavior → minimized original fixtures in Git. No capture or implementation is authorized by this document.
