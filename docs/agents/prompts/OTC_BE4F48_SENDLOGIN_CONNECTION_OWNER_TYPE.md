# OTC-BE4F48-SENDLOGIN-CONNECTION-OWNER-TYPE

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-SENDLOGIN-CONNECTION-OWNER-TYPE autonomicznie.
```

Recommended effort: **High**.

## Exact authority

At task start refresh protected `main`, repository governance, open PR/task ownership and the latest coordinator promotion. Live GitHub state is the only current authority.

Starting lifecycle:

```text
promotion PR #886
promotion merge 4ca7f33386a3e9d602a942105626150b2359960b
archive PR #887
archive merge 6ab922152d288e56112b162518512859552f06e6
source PR #884 CLOSED UNMERGED AS CONSUMED
```

Read before implementation:

- `docs/agents/evidence/OTC-20260904-be4f48-post884-885-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post884-885-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If a newer promotion supersedes this fence or boundary, follow the newer authority instead of this prompt.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No address, offset, QMeta, RTTI, vtable, field semantic or historical value from another client build is authoritative without fresh exact-current evidence.

## Promoted starting facts

```text
sendlogin_sender_identity=tibia::authentication::TLoginProtocolMessageHandler
sendlogin_signal=sendLoginMessage
sendlogin_connectimpl_callsite=0x7c6b9f
sendlogin_adapter_target=0xbd3050
connection_owner_fde=0x7c6700..0x7cc933
sendlogin_receiver_provenance=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
sendlogin_receiver_field_definition=UNKNOWN
sendlogin_receiver_owner_chain=UNKNOWN
sendlogin_receiver_identity=UNKNOWN
sendlogin_causal_binding_proven=false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

Source PR #884 already performed the bounded target-specific direct-caller search for FDE `0x7c6700..0x7cc933` and found zero accepted direct callers. That result is consumed. **Do not repeat or widen that direct-caller search.**

## Single objective

Resolve only the exact class/type identity of the object entering the selected connection-owner FDE through `entry-rdi`, using a different bounded proof mode than #884.

Start from:

```text
connection_owner_fde=0x7c6700..0x7cc933
connection_owner_object=ENTRY_ARG:rdi
receiver_field=[entry-rdi-derived-rbx+0x88]
```

Within that bounded owner object, recover enough exact-current vtable/RTTI/QMeta/type construction evidence to answer:

```text
CONNECTION_OWNER_IDENTITY=<exact type|UNKNOWN>
CONNECTION_OWNER_IDENTITY_PROVEN=true|false
```

Only if the exact connection-owner identity is proven and the object layout gives one unique identity-preserving route to `+0x88`, you may additionally classify the receiver field/type. Otherwise stop at the first unresolved edge.

A positive type claim should use two agreeing proof classes where practical, for example:

- exact vptr store/load tied to the entry object plus matching typeinfo/vtable;
- exact QMeta/static-metaobject tied to that same object;
- one bounded constructor/member initialization edge already inside or uniquely reached from the selected owner object;
- independent type/ownership cross-check that does not require a global census.

String proximity, QObject-like shape, field adjacency, historical layouts, generic vtable resemblance or a guessed class name are not proof.

## Bounded search rule

Allowed search is strictly:

```text
selected owner FDE/object
  -> in-FDE identity evidence
  -> at most one unique identity-preserving vtable/RTTI/QMeta/type edge
  -> optional +0x88 receiver typing only if owner identity makes that route unique
```

Stop if the identity edge becomes non-unique.

Do **not** perform:

- the consumed #884 direct-caller scan again;
- a global constructor or caller census;
- a global RTTI/QMeta/QObject/vtable census;
- a global `+0x88` field search;
- queue signal `0xbf` / QSlot / writer work;
- Track B protocol implementation or mutation.

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
- guessing Field6 value or complete pre-login order.

If the owner class cannot be proven through the bounded object identity route, terminate `SOURCE_BLOCKER` with the exact first missing boundary. Do not invent another broad subsystem or analyzer family.

## TDD / validation

For any new analyzer/contract:

1. create a fresh independent source-only Track A task/branch/Draft PR from current trusted `main`;
2. persist non-overlapping ownership before implementation;
3. produce repository-only **RED** before any client package materialization;
4. implement the smallest GREEN discriminator;
5. exact-guard version/size/SHA before analysis;
6. emit deterministic sanitized output only;
7. retain zero proprietary client bytes in repository/artifacts;
8. run `git diff --check`, scoped syntax/Ruff where applicable, Track A governance, self-hosted PR boundary where applicable and exact-head CI;
9. perform fresh whole-diff falsification before a terminal claim.

Analyzer GREEN is not scientific PASS by itself.

## Terminal outcomes

Use one materially accurate result:

```text
SENDLOGIN_CONNECTION_OWNER_TYPE_PROVEN
SENDLOGIN_RECEIVER_TYPE_PROVEN
SOURCE_BLOCKER
```

Required terminal fields:

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
CONNECTION_OWNER_FDE=0x7c6700..0x7cc933
CONNECTION_OWNER_ENTRY_OBJECT=ENTRY_ARG:rdi
CONNECTION_OWNER_IDENTITY=<value|UNKNOWN>
CONNECTION_OWNER_IDENTITY_PROVEN=true|false
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_IDENTITY=<value|UNKNOWN>
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=true|false
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=true|false
SENDLOGIN_CAUSAL_BINDING_PROVEN=true|false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<SENDLOGIN_CONNECTION_OWNER_TYPE_PROVEN|SENDLOGIN_RECEIVER_TYPE_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

Stop when this owner/type question is terminal. Do not consume the parallel queue relay receiver task's scope.
