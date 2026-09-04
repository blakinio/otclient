# OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-OWNER

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-OWNER autonomicznie.
```

Recommended effort: **High**.

## Exact authority

At task start refresh protected `main`, repository governance, open PR/task ownership and the latest coordinator promotion. GitHub LIVE STATE is the only current authority.

Starting promotion/lifecycle:

```text
promotion PR #881
promotion merge 2023254a4c6f0bac3a5ac4e8b06426d9dfed0862
archive PR #882
```

Read before implementation:

- `docs/agents/evidence/OTC-20260904-be4f48-post879-880-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post879-880-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If a newer promotion supersedes the fence or boundary, follow the newer authority instead of this prompt.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No address, offset, RTTI, QMeta, vtable, field semantic or historical value from another client build is authoritative without fresh exact-current evidence.

## Promoted starting facts

```text
sendlogin_sender_identity=tibia::authentication::TLoginProtocolMessageHandler
sendlogin_signal=sendLoginMessage
sendlogin_connectimpl_callsite=0x7c6b9f
sendlogin_adapter_target=0xbd3050
sendlogin_receiver_provenance=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
sendlogin_receiver_field_reads_in_selected_fde=165
sendlogin_receiver_field_writes_in_selected_fde=0
sendlogin_receiver_identity=UNKNOWN
sendlogin_causal_binding_proven=false
FIRST_MISSING_BOUNDARY=RECEIVER_FIELD_DEFINITION_OUTSIDE_SELECTED_CONNECTION_OWNER_FDE
```

The stack-aware receiver argument chain through the hidden-sret connection setup is already promoted exact-current evidence. Do not reopen that solved question unless fresh evidence falsifies it.

## Single objective

Resolve only the definition/ownership/type chain for the exact field:

```text
entry-rdi-derived owner object
  -> field +0x88
  -> initializer/member store that defines the receiver pointer
  -> exact receiver object/class identity
```

Then, and only if the receiver class identity is independently proven, reconcile that result with the already-proven `QObject::connectImpl@0x7c6b9f` sender/receiver pair and state whether the `sendLoginMessage -> QSlot(adapter 0xbd3050)` causal binding is proven or rejected.

A positive type claim requires at least two agreeing exact-current proof classes where practical, for example:

- bounded constructor/member-store provenance;
- RTTI/typeinfo/vtable identity of the stored object;
- exact QMeta/static-metaobject identity;
- unique allocation/constructor return tied to the `+0x88` store;
- independent caller/ownership cross-check.

Pointer adjacency, generic QObject shape, repeated field reads, historical offsets or a guessed class name are not type proof.

## Bounded search rule

Start from the promoted `[entry-rdi-derived-rbx+0x88]` provenance and derive the owner/caller/constructor boundary from exact-current evidence.

You may follow only the smallest identity-preserving chain required to reach the defining store. Stop immediately if the initializer/constructor edge becomes non-unique.

Do **not** perform:

- a global constructor census;
- a global `+0x88` reference census across unrelated objects;
- a global RTTI/QMeta/QObject/connect search;
- queue signal `0xbf` / QSlot writer analysis;
- a protocol rewrite or Track B mutation.

## Strict safety / anti-loop

Forbidden:

- official-client execution;
- login or credential/session/cookie/character/world access;
- process-memory access;
- packet capture;
- OCR/Vision;
- official-service E2E;
- runtime Field6 observation;
- modifying Track B PR #284;
- guessing Field6 value or complete pre-login message order.

If static source evidence cannot uniquely type the receiver through this bounded ownership chain, terminate with the first exact unresolved boundary rather than opening another analyzer family.

## TDD / implementation contract

For any new analyzer/contract:

1. start from fresh trusted `main` on a dedicated non-overlapping source branch/Draft PR;
2. persist task ownership before material implementation;
3. first produce repository-only **RED** before any WARP package/client materialization;
4. implement the smallest GREEN discriminator;
5. enforce exact version/size/SHA fence before analysis;
6. emit deterministic sanitized JSON only;
7. delete transient raw client bytes before artifact upload;
8. run `git diff --check`, scoped syntax/compile validation, exact-head CI, Track A governance and self-hosted PR boundary where applicable;
9. perform fresh whole-diff falsification before a terminal claim.

Green analyzer tests are not scientific PASS by themselves.

## Terminal outcomes

Use the materially accurate result:

```text
SENDLOGIN_RECEIVER_FIELD_OWNER_PROVEN
SOURCE_BLOCKER
```

A proven result requires at minimum:

```text
receiver_field_provenance=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
receiver_field_definition_site=<exact site>
receiver_owner_chain=<exact bounded chain>
receiver_endpoint_identity=<exact class/type>
receiver_identity_proven=true
complete_sender_receiver_pair_proven=true|false
sendlogin_causal_binding_proven=true|false
```

If the type is proven but causality is rejected, preserve that falsification explicitly.

If blocked:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact non-unique initializer/owner/type edge>
```

## Track B gate

This source task does not directly authorize #284 mutation or E2E. Even a positive receiver identity must first pass a clean coordinator promotion with current queue/QSlot/writer and Field6/pre-login evidence.

Until then:

```text
TRACK_B_PR_284_MODIFIED=false
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
OFFICIAL_SERVICE_E2E_COUNT=0
RUNTIME_ACCESS=none
```

## Required final report

Persist and report at minimum:

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_FIELD_DEFINITION=<value|UNKNOWN>
SENDLOGIN_RECEIVER_OWNER_CHAIN=<value|UNKNOWN>
SENDLOGIN_RECEIVER_IDENTITY=<value|UNKNOWN>
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=true|false
SENDLOGIN_CAUSAL_BINDING_PROVEN=true|false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<SENDLOGIN_RECEIVER_FIELD_OWNER_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

Stop when this field-owner question is terminal. Do not consume the parallel QSlot task's scope.
