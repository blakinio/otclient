# OTC-BE4F48-SENDLOGIN-ADAPTER-BD3050-RECEIVER-SEMANTICS

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-SENDLOGIN-ADAPTER-BD3050-RECEIVER-SEMANTICS autonomicznie.
```

Recommended effort: **Extra High**.

## Exact authority

At task start refresh protected `main`, current governance, open PR/task ownership and the latest Track A coordinator promotion. LIVE GitHub state is authoritative.

Starting lifecycle:

```text
promotion PR #901
promotion merge 6cd05e17f3c9e350a44654c7adce34f2e2d6c5d9
archive PR #902
archive merge 11aed31d8eaee28a5485984636e61a2c3d22933a
```

Read first:

- `docs/agents/evidence/OTC-20260904-be4f48-post899-900-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post899-900-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If newer promotion evidence supersedes this boundary, follow the newer authority instead.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No address, ABI, type or adapter semantic from another build is authoritative without exact-current proof.

## Promoted starting facts

```text
SENDLOGIN_SENDER_IDENTITY=tibia::authentication::TLoginProtocolMessageHandler
SENDLOGIN_SIGNAL=sendLoginMessage
SENDLOGIN_CONNECTIMPL_CALLSITE=0x7c6b9f
SENDLOGIN_RECEIVER_FIELD_LOAD_SITE=0x7c6b18
SENDLOGIN_RECEIVER_PROVENANCE=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
RECEIVER_FIELD_VALUE_USE=QOBJECT_CONNECTIMPL_RECEIVER_ARGUMENT
RECEIVER_FIELD_VALUE_USE_PROVEN=true
CONNECTIMPL_FORMAL_RECEIVER_REGISTER=rcx
SENDLOGIN_ADAPTER_TARGET=0xbd3050
SENDLOGIN_RECEIVER_IDENTITY=UNKNOWN
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=false
SENDLOGIN_CAUSAL_BINDING_PROVEN=false
```

The prior task already exhausted owner/caller/callee type discovery and the immediate `+0x88` field-value lifetime. Do not repeat those proof modes.

## Single objective

Resolve only the exact semantics of adapter callable `0xbd3050` for the sendLogin connection and determine whether it uniquely binds the already-proven `+0x88` receiver object to one receiver/member/slot identity.

Allowed proof path:

```text
connectImpl@0x7c6b9f
  -> exact QSlot/adapter construction for this connection
  -> callable target 0xbd3050
  -> derive exact adapter invocation ABI from current QSlot dispatch semantics
  -> prove whether the same receiver object is carried/dereferenced/dispatched
  -> at most one unique adapter-internal member/call edge
```

A positive identity claim requires exact object-tied evidence. Examples include:

- QSlot payload field that uniquely carries the proven receiver object into `0xbd3050`;
- adapter dereference of that exact receiver followed by one unique virtual/member target with exact type evidence;
- one exact direct/internal callable whose receiver/member semantics are unique;
- exact QMeta/static-metaobject evidence tied to the same receiver object.

Do not infer identity from a symbol-less address, generic QObject shape, stale ABI register state, historical type names or address proximity.

## Bounded search / anti-loop

Do not:

- rerun #884 caller discovery;
- rerun #889 owner-FDE identity scans;
- rerun #894 `0x7e8f30` callee identity work;
- rerun #899 exact field-value lifetime/type-edge scan;
- perform a global QSlot/QObject/vtable/RTTI/caller census;
- perform queue signal/writer work;
- mutate Track B #284.

Analyze only the exact sendLogin connection's QSlot construction, adapter FDE, and at most one unique adapter-internal object/member edge. Stop at the first non-unique ABI/object/member boundary.

## Safety

Forbidden:

- official-client execution;
- login or credential/session/cookie/character/world access;
- process-memory access;
- packet capture;
- OCR/Vision;
- official-service E2E;
- runtime Field6 observation;
- Track B #284 mutation;
- guessing Field6 or pre-success ordering.

## TDD / implementation contract

For a new discriminator:

1. start from fresh trusted `main` on a dedicated source branch/Draft PR;
2. persist task ownership with complete `runtime_access:none` governance fields;
3. prove repository-only RED before any exact-client materialization;
4. implement the smallest GREEN analyzer for this exact adapter path only;
5. exact-guard version/size/SHA before analysis;
6. emit deterministic sanitized JSON only;
7. delete transient client bytes before artifact upload;
8. run `git diff --check`, scoped syntax tests, exact-head focused workflow, CI, governance and self-hosted boundary;
9. perform fresh whole-diff falsification before terminal handoff.

## Terminal outcomes

Use only:

```text
SENDLOGIN_ADAPTER_RECEIVER_SEMANTICS_PROVEN
SOURCE_BLOCKER
```

A positive result must report at minimum:

```text
SENDLOGIN_ADAPTER_TARGET=0xbd3050
ADAPTER_INVOCATION_ABI=<exact proof>
ADAPTER_RECEIVER_OBJECT_PROVENANCE=<exact value|UNKNOWN>
ADAPTER_RECEIVER_OBJECT_MATCHES_FIELD_88=true|false
SENDLOGIN_RECEIVER_IDENTITY=<exact type|UNKNOWN>
SENDLOGIN_RECEIVER_IDENTITY_PROVEN=true|false
SENDLOGIN_SLOT_OR_MEMBER_IDENTITY=<exact identity|UNKNOWN>
SENDLOGIN_CAUSAL_BINDING_PROVEN=true|false
```

If blocked:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact non-unique adapter/object/member boundary>
```

Always preserve unless newly proven:

```text
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
```

Stop when this exact adapter question is terminal. Do not consume the parallel queue task's scope.
