# OTC-BE4F48-QUEUE-SIGNAL-BF-QMETA-INDEX-CONNECTION

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-QMETA-INDEX-CONNECTION autonomicznie.
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

If newer promotion evidence supersedes this exact boundary, follow it instead.

## Exact client fence

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

## Promoted starting facts

```text
QUEUE_SIGNAL_NAME=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_BODY=0xbd2190
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
QUEUE_STATIC_METAOBJECT=0x30b73e0
QUEUE_SIGNAL_METHOD_ROW=0x1ce47c0
QUEUE_SIGNAL_NAME_ADDRESS=0x1ceda8e
EXACT_SIGNAL_REFERENCE_COUNT=1
EXACT_SIGNAL_CONNECT_CANDIDATE_COUNT=0
NEXT_QUEUE_SIGNAL_ENDPOINT=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
```

The consumed exact-body/name xref task proved that direct exact-signal references only expose the already-known self-relay QSlot callable. Do not repeat that search.

## Single objective

Determine whether the exact queue signal can be connected downstream through **QMeta method-index / static-metacall / index-based connection semantics** that do not carry a direct reference to body `0xbd2190` or its name storage.

Start only from the exact tuple:

```text
METAOBJECT=0x30b73e0
METHOD_INDEX=0xbf
METHOD_ROW=0x1ce47c0
SIGNAL_NAME=clientMessageReadyToProcess
OWNER=tibia::protocol::TProtocolMessageQueue
```

Allowed proof path:

```text
exact queue metaobject + exact method index 0xbf
  -> exact index-bearing/static-metacall/connection-registration context
  -> one Qt connection primitive or registration edge causally using that exact tuple
  -> at most one unique receiver/slot endpoint identity edge
```

The task may inspect exact integer/index constants only when they are causally bound to the exact queue metaobject or method row; a raw executable-wide search for value `0xbf` is forbidden.

A positive connection claim must prove all of:

1. exact queue metaobject ownership;
2. exact signal method index `0xbf` rather than an unrelated constant;
3. exact connection-registration semantics rather than signal activation/emission;
4. one unique endpoint identity or one exact next callable edge.

## Bounded search / anti-loop

Do not:

- redo #885 QSlot construction;
- redo #890 receiver typing;
- redo #895 queue-constructor connect enumeration;
- redo #900 body/method/name exact-xref enumeration;
- perform a generic/global search for `0xbf`;
- perform a global QObject/QMeta/connect/socket/writer census;
- infer endpoint identity from class-name proximity or generic QMeta tables;
- mutate Track B #284.

Admit at most one uniquely causal method-index connection setup. If the exact metaobject/index path becomes non-unique, stop and report the first boundary.

## Safety

Forbidden:

- official-client execution;
- login or credentials/session access;
- process-memory access;
- packet capture;
- OCR/Vision;
- official-service E2E;
- runtime Field6 observation;
- Track B #284 mutation;
- guessing final writer/Field6/order.

## TDD / implementation contract

1. start from fresh trusted `main` on a dedicated source branch/Draft PR;
2. persist task ownership with complete `runtime_access:none` governance fields;
3. prove repository-only RED before client materialization;
4. implement the smallest exact metaobject/index discriminator only;
5. exact-guard version/size/SHA;
6. emit deterministic sanitized JSON only;
7. delete transient client bytes before artifact upload;
8. run exact-head focused workflow, CI, Track A governance and self-hosted PR boundary;
9. perform fresh whole-diff falsification.

## Terminal outcomes

Use only:

```text
QUEUE_SIGNAL_BF_QMETA_INDEX_CONNECTION_PROVEN
SOURCE_BLOCKER
```

A positive result must report at minimum:

```text
QUEUE_STATIC_METAOBJECT=0x30b73e0
QUEUE_SIGNAL_INDEX=0xbf
QMETA_INDEX_CONNECTION_SITE=<exact callsite>
QMETA_INDEX_CONNECTION_PRIMITIVE=<exact identity>
NEXT_UNIQUE_RELAY_EDGE=<exact edge|UNKNOWN>
NEXT_ENDPOINT_IDENTITY=<exact identity|UNKNOWN>
NEXT_RELAY_IDENTITY_PRESERVED=true|false
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<exact value|UNKNOWN>
```

If blocked:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact non-unique/unproven method-index connection boundary>
```

Always preserve unless independently proven:

```text
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
```

Stop when this exact method-index connection question is terminal. Do not consume the parallel sendLogin adapter task's scope.
