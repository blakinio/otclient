# OTC-BE4F48-SENDLOGIN-OWNER-EDGE-7E8F30-IDENTITY

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-SENDLOGIN-OWNER-EDGE-7E8F30-IDENTITY autonomicznie.
```

Recommended effort: **Extra High**.

## Exact authority

At task start refresh protected `main`, repository governance, open PR/task ownership and the latest coordinator promotion. GitHub LIVE STATE is the only current authority.

Starting promotion/lifecycle:

```text
promotion PR #891
promotion merge b4582b1e72d689b5d26fbd16c0ba2bbd20dca970
archive PR #892
archive merge 58cc12558babcfcadaa89bbdc49ca19ee1e58e5e
```

Read before implementation:

- `docs/agents/evidence/OTC-20260904-be4f48-post889-890-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post889-890-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current Track A governance/instructions.

If a newer promotion supersedes this exact fence or boundary, follow the newer authority instead of this prompt.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No address, offset, RTTI, QMeta, vtable, constructor semantic or type identity from another build is authoritative without fresh exact-current proof.

## Promoted starting facts

```text
sendlogin_sender_identity=tibia::authentication::TLoginProtocolMessageHandler
sendlogin_signal=sendLoginMessage
sendlogin_connectimpl_callsite=0x7c6b9f
sendlogin_adapter_target=0xbd3050
connection_owner_fde=0x7c6700..0x7cc933
connection_owner_entry_object=ENTRY_ARG:rdi
connection_owner_identity=UNKNOWN
unique_owner_bound_edge=0x7c67b8 -> 0x7e8f30
sendlogin_receiver_provenance=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
sendlogin_receiver_identity=UNKNOWN
sendlogin_causal_binding_proven=false
FIRST_MISSING_BOUNDARY=UNIQUE_ENTRY_OBJECT_EDGE_TYPE_NOT_PROVEN
```

The prior source lane already proved that `0x7c67b8 -> 0x7e8f30` is the only direct call in the selected owner FDE whose `rdi` backward-slices to the same entry owner object. Do not rediscover callers or rescan the owner FDE to choose another edge.

## Single objective

Resolve only the identity semantics of the exact already-selected callee edge:

```text
entry owner object
  -> callsite 0x7c67b8
  -> callee 0x7e8f30
  -> callee treatment of the same this/object pointer
  -> exact owner type identity if uniquely provable
```

A positive type claim must be grounded in exact-current evidence tied to the same object, for example:

- primary-vptr store or load with Itanium RTTI/typeinfo name;
- exact QMeta/static-metaobject identity tied to the object;
- exact constructor/delegating-constructor semantic in callee prologue;
- one unique internal identity-preserving edge whose object argument remains the same;
- an independent second proof class when practical.

A symbol-less callee address, generic QObject behavior, pointer adjacency, string proximity, historical class names or guessed layout are not type proof.

## Bounded search rule

Start exactly at:

```text
CALLSITE=0x7c67b8
CALLEE=0x7e8f30
OBJECT=the same ENTRY_ARG:rdi owner object promoted through #891
```

Analyze only the callee FDE and, if necessary, at most **one** additional unique identity-preserving internal edge from that callee. Stop immediately when the object/type route becomes non-unique.

Do **not** perform:

- another caller search for `0x7c6700` or `0x7e8f30`;
- another whole-owner-FDE identity scan from #889;
- a global constructor census;
- a global RTTI/QMeta/QObject/vtable census;
- a global `+0x88` field census;
- queue signal/QSlot/relay/writer work;
- protocol mutation or Track B work.

Only if this exact callee proves the owner class may you state whether that unique owner layout is sufficient to classify the already-promoted `+0x88` receiver field. If the owner type is proven but `+0x88` receiver type still is not uniquely implied, preserve receiver identity as `UNKNOWN`.

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
- guessing Field6 value or pre-success message order;
- widening into a repository-wide or executable-wide type census.

If this exact edge cannot prove the owner type, terminate at the first precise callee/type boundary instead of starting another analyzer family inside the same task.

## TDD / implementation contract

For any new analyzer/contract:

1. start from fresh trusted `main` on a dedicated non-overlapping source branch/Draft PR;
2. persist task ownership before material implementation;
3. first produce repository-only **RED** before WARP/client materialization;
4. implement the smallest GREEN discriminator for `0x7c67b8 -> 0x7e8f30` only;
5. enforce exact version/size/SHA fence before analysis;
6. emit deterministic sanitized JSON only;
7. delete transient raw client bytes before artifact upload;
8. run `git diff --check`, scoped syntax/compile validation, exact-head CI, Track A governance and self-hosted PR boundary where applicable;
9. perform fresh whole-diff falsification before a terminal claim.

Green analyzer tests are not scientific PASS by themselves.

## Terminal outcomes

Use the materially accurate result:

```text
SENDLOGIN_OWNER_EDGE_IDENTITY_PROVEN
SOURCE_BLOCKER
```

A positive result requires at minimum:

```text
owner_edge_callsite=0x7c67b8
owner_edge_callee=0x7e8f30
owner_object_identity=<exact type>
owner_object_identity_proven=true
owner_identity_proof_classes=<exact proof classes>
sendlogin_receiver_identity=<exact type|UNKNOWN>
sendlogin_receiver_identity_proven=true|false
complete_sender_receiver_pair_proven=true|false
sendlogin_causal_binding_proven=true|false
```

If blocked:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact non-unique/unproven callee type edge>
```

## Track B gate

This source task never directly authorizes Track B #284 mutation or E2E. Any positive owner/receiver identity must first pass a clean coordinator promotion together with current queue/relay/writer, Field6 and pre-login-order evidence.

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
OWNER_EDGE_CALLSITE=0x7c67b8
OWNER_EDGE_CALLEE=0x7e8f30
OWNER_OBJECT_IDENTITY=<value|UNKNOWN>
OWNER_OBJECT_IDENTITY_PROVEN=true|false
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
terminal_result=<SENDLOGIN_OWNER_EDGE_IDENTITY_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

Stop when this exact callee identity question is terminal. Do not consume the parallel queue relay task's scope.
