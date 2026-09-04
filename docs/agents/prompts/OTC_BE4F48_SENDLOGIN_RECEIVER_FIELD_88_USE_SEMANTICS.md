# OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-88-USE-SEMANTICS

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-SENDLOGIN-RECEIVER-FIELD-88-USE-SEMANTICS autonomicznie.
```

Recommended effort: **Extra High**.

## Exact authority

At task start refresh protected `main`, current governance, open Track A tasks/PRs and the latest coordinator promotion. LIVE GitHub state is authoritative.

Starting lifecycle:

```text
promotion PR #896
promotion merge 71e1af0db234a4011689e51bdbcc0ee7d9ee97c8
archive PR #897
archive merge 5bedd83b38b276f5b7691f7efe2ef5f91611f42f
```

Read first:

- `docs/agents/evidence/OTC-20260904-be4f48-post894-895-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post894-895-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If a newer promotion supersedes the fence or boundary, use the newer authority.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

## Promoted starting facts

```text
SENDLOGIN_SENDER_IDENTITY=tibia::authentication::TLoginProtocolMessageHandler
SENDLOGIN_SIGNAL=sendLoginMessage
SENDLOGIN_CONNECTIMPL_CALLSITE=0x7c6b9f
SENDLOGIN_ADAPTER_TARGET=0xbd3050
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
OWNER_EDGE=0x7c67b8->0x7e8f30
OWNER_OBJECT_IDENTITY=UNKNOWN
OWNER/CALLEE_IDENTITY_PATHS_EXHAUSTED=true
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

The owner-class proof modes from #884, #889 and #894 are consumed. Do not attempt to identify the owner class again.

## Single objective

Change proof mode to the exact **receiver-field value** already proven at `+0x88`.

Starting only from the sendLogin `connectImpl@0x7c6b9f` context and the promoted backward-slice provenance, determine whether the object loaded from `[entry-rdi-derived-rbx+0x88]` has uniquely provable immediate use/type semantics.

Allowed positive proof classes include only evidence tied to that exact loaded field value, such as:

- exact argument handoff proving it is the `QObject::connectImpl` receiver;
- one object-tied primary-vptr / Itanium RTTI decode of the loaded field object;
- one exact QMeta/static-metaobject/type identity tied to that loaded object;
- one unique direct method/constructor/metaobject edge whose `this` is the same loaded field object;
- exact adapter/slot semantics that uniquely identify the receiver class.

Generic QObject shape, owner adjacency, historical layouts, string proximity, or a type found elsewhere at offset `+0x88` are not proof.

## Bounded search rule

Admitted path only:

```text
sendLogin connectImpl@0x7c6b9f
  -> promoted receiver field value [entry-rdi-derived-rbx+0x88]
  -> exact immediate field-value use/argument semantics
  -> at most one unique object-tied type/QMeta/vptr edge
```

Stop at the first non-unique field-value use or type edge.

Do **not**:

- repeat #884 caller discovery;
- repeat #889 owner-FDE type analysis;
- repeat #894 `0x7e8f30` callee identity analysis;
- perform a global `+0x88` field census;
- perform a global RTTI/QMeta/QObject/vtable census;
- inspect queue signal/QSlot/writer scope;
- mutate Track B #284.

## Strict safety

Forbidden:

- official-client execution;
- login or credential/session/cookie/character/world access;
- process-memory access;
- packet capture;
- OCR/Vision;
- official-service E2E;
- runtime Field6 observation;
- guessed Field6 value or pre-success order.

## TDD / implementation contract

1. Start from fresh trusted `main` with a dedicated independent source branch/Draft PR.
2. Persist complete Track A task ownership/admission metadata before material implementation.
3. Produce repository-only RED before any client materialization.
4. Implement the smallest exact field-value discriminator only.
5. Enforce exact version/size/SHA before source analysis.
6. Retain/upload deterministic sanitized JSON only; delete transient raw client bytes.
7. Run `git diff --check`, scoped syntax/compile validation, exact-head CI, Track A governance and self-hosted PR boundary where applicable.
8. Perform fresh whole-diff falsification before terminal handoff.

## Terminal outcomes

Positive only if the exact field value's identity is uniquely proven:

```text
terminal_result=SENDLOGIN_RECEIVER_FIELD_USE_IDENTITY_PROVEN
SENDLOGIN_RECEIVER_IDENTITY=<exact type>
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=true
```

Otherwise:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact non-unique/unproven field-use/type boundary>
```

Do not upgrade `COMPLETE_SENDER_RECEIVER_PAIR_PROVEN` or `SENDLOGIN_CAUSAL_BINDING_PROVEN` unless the exact evidence genuinely proves those stronger claims.

## Required final report

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
SENDLOGIN_CONNECTIMPL_CALLSITE=0x7c6b9f
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
RECEIVER_FIELD_VALUE_USE=<exact bounded description|UNKNOWN>
RECEIVER_FIELD_VALUE_USE_PROVEN=true|false
SENDLOGIN_RECEIVER_IDENTITY=<value|UNKNOWN>
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=true|false
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=true|false
SENDLOGIN_CAUSAL_BINDING_PROVEN=true|false
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<SENDLOGIN_RECEIVER_FIELD_USE_IDENTITY_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

Stop when the exact receiver-field-use question is terminal. Do not consume the parallel queue exact-signal task.