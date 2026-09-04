# OTC-BE4F48-SENDLOGIN-RECEIVER-IDENTITY

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-SENDLOGIN-RECEIVER-IDENTITY autonomicznie.
```

Recommended effort: **High**.

## Exact authority

At task start refresh protected `main`, repository governance, open PR/task ownership and the latest coordinator promotion. Live GitHub state is the only current authority.

The starting promotion is:

```text
PR #876
merge 44a35365e38b9483b9c43aff4c36c2379fdbfb3e
archive PR #877
```

Read before implementation:

- `docs/agents/evidence/OTC-20260904-be4f48-post874-875-promotion/20260904-coordinator-promotion.md`
- `docs/agents/evidence/OTC-20260904-be4f48-post874-875-promotion/result.json`
- `docs/agents/TIBIA_RESEARCH_TRACKS.md`
- current agent/governance instructions relevant to Track A.

If a newer promotion supersedes this exact fence or boundary, follow the newer authority instead of this prompt.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

No address, offset, QMeta, RTTI, vtable or semantic value from another client build is authoritative without fresh exact-current proof.

## Proven starting facts

Promoted exact-current facts include:

```text
peer_owner_identity=tibia::authentication::TLoginProtocolMessageHandler
peer_signal_name=sendLoginMessage
peer_signal_index=0
actual_qt_connection_callsite=0x7c6b9f
actual_qt_connection_primitive=QObject::connectImpl(...)
sender_endpoint_identity=tibia::authentication::TLoginProtocolMessageHandler
sendlogin_adapter_target=0xbd3050
sendlogin_adapter_bound_into_qslot_object=true
qslot_object_adapter_field_offset=0x10
receiver_endpoint_provenance=OBJECT_FIELD:[entry-rdi-derived-rbx+0x88]
receiver_endpoint_identity=UNKNOWN
sendlogin_causal_binding_proven=false
```

The hidden-sret ABI for the selected `connectImpl` call is already independently proven in the promoted source evidence. Do not spend a new discriminator re-proving it unless new evidence falsifies the promotion.

## Single objective

Resolve only:

```text
[entry-rdi-derived-rbx+0x88]
  -> exact receiver object/class/ownership identity
  -> complete sender/receiver pair for connectImpl @ 0x7c6b9f
  -> prove or reject causal binding from TLoginProtocolMessageHandler::sendLoginMessage
     through the QSlot object carrying adapter 0xbd3050
```

A positive result requires independent exact-current type/ownership evidence for the receiver, not only pointer provenance.

Useful admissible proof classes include a bounded combination of:

- exact QMeta/static-metaobject identity;
- RTTI/typeinfo/vtable identity;
- constructor/member-store ownership chain;
- unique object-field definition/use chain tied to the selected connection FDE;
- independent caller/owner cross-check.

Do not manufacture type identity from address adjacency, historical offsets, generic QObject shape or an untyped field load.

## Strict anti-loop / scope

Do not:

- reopen or rerun the completed #875 peer-metaowner analyzer;
- search globally for every QObject/QMeta/connect call;
- broaden into queue signal `0xbf` writer/receiver work;
- modify Track B PR #284;
- guess Field6 value or semantic name;
- infer complete pre-login order solely from the connection;
- execute the official client;
- perform login, credential/session access, process-memory reads, packet capture, OCR/Vision or official-service E2E.

If the receiver identity cannot be uniquely proved inside a bounded evidence-derived discriminator, stop at the first precise missing static boundary.

## TDD / implementation contract

For any new analyzer or contract:

1. create a dedicated non-overlapping task/branch/Draft PR from fresh trusted `main`;
2. persist task ownership before material implementation;
3. first prove a repository-only RED before any client package/materialization step;
4. implement the smallest GREEN discriminator;
5. require the exact client fence before analysis;
6. output deterministic sanitized JSON only;
7. delete transient raw client bytes before artifact upload;
8. run `git diff --check`, scoped syntax/compile validation, exact-head CI, Track A governance and self-hosted PR boundary where applicable;
9. perform fresh whole-diff falsification before terminal claim.

Green analyzer tests are not themselves scientific proof.

## Terminal outcomes

Use exactly one materially accurate result:

```text
SENDLOGIN_RECEIVER_IDENTITY_PROVEN
SOURCE_BLOCKER
```

`SENDLOGIN_RECEIVER_IDENTITY_PROVEN` requires at least:

```text
receiver_endpoint_identity=<exact class/type>
receiver_identity_proven=true
complete_sender_receiver_pair_proven=true
sendlogin_adapter_bound_to_receiver=true|false
sendlogin_causal_binding_proven=true|false
```

If receiver identity is proven but causality is disproven, preserve that falsification explicitly rather than forcing success.

If blocked, report:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact unresolved ownership/type edge>
```

## Track B gate

This task never directly authorizes a Track B mutation or E2E. Even if the full sender/receiver pair is proved, a clean coordinator promotion must first combine it with current queue/writer and Field6/pre-login evidence.

Until then:

```text
TRACK_B_PR_284_MODIFIED=false
TRACK_B_CURRENT_WIRE_DELTA=NOT_PROVEN
OFFICIAL_SERVICE_E2E_COUNT=0
```

## Required final report

Persist and report at minimum:

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
SENDLOGIN_SENDER_IDENTITY=<value>
SENDLOGIN_SIGNAL=<value>
SENDLOGIN_RECEIVER_PROVENANCE=<value>
SENDLOGIN_RECEIVER_IDENTITY=<value|UNKNOWN>
COMPLETE_SENDER_RECEIVER_PAIR_PROVEN=true|false
SENDLOGIN_CAUSAL_BINDING_PROVEN=true|false
PRE_SUCCESS_SEND_SEQUENCE=<value|UNKNOWN>
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<SENDLOGIN_RECEIVER_IDENTITY_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<one bounded repository-owned step or coordinator promotion>
```

Evidence before claims. Stop when the bounded receiver-identity question is terminal; do not consume the next writer task's scope.
