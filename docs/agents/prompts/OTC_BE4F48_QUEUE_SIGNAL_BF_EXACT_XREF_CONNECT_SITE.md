# OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous exact-current Track A source-only discriminator.

## Owner invocation

```text
Uruchom OTC-BE4F48-QUEUE-SIGNAL-BF-EXACT-XREF-CONNECT-SITE autonomicznie.
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
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_BODY=0xbd2190
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
QUEUE_SIGNAL_RECEIVER_IDENTITY=tibia::protocol::TProtocolMessageQueue
QUEUE_SIGNAL_CONNECTION_ROLE=SIGNAL_RELAY
SELF_RELAY_CONNECTIMPL_CALLSITE=0xbe2eee
QSLOT_FUNCTION_TARGET=0xbd2190
QUEUE_CONSTRUCTOR_FDE=0xbe2a50..0xbe3086
DIRECT_CONNECTIMPL_CALLS_IN_CONSTRUCTOR=0xbe2e54,0xbe2eee
AFTER_SELF_RELAY_CONNECT_COUNT=0
ADDITIONAL_EXACT_SIGNAL_CANDIDATES_IN_CONSTRUCTOR=0
NEXT_UNIQUE_RELAY_EDGE=UNKNOWN
NEXT_ENDPOINT_IDENTITY=UNKNOWN
FINAL_WRITER_CONTRACT=UNKNOWN
FIELD6_VALUE=UNKNOWN
```

The constructor-local proof modes from #885, #890 and #895 are consumed. Do not repeat QSlot construction, receiver typing or queue-constructor `connectImpl` enumeration.

## Single objective

Change proof mode from constructor-local enumeration to an **exact-signal-only reference discriminator**.

Starting from exact signal body `0xbd2190`, exact signal index `0xbf`, and the proven `TProtocolMessageQueue` identity, identify exact-current code/data reference sites that can be causally tied to construction of this specific `clientMessageReadyToProcess` connection. Admit only sites with exact signal identity evidence; then determine whether exactly one downstream `QObject::connectImpl` setup and endpoint can be proven.

If a static-metaobject address or method table is needed, derive and exact-fence it from the current binary in this task; do not promote an analyzer constant by assumption.

## Bounded search rule

This task may perform an executable-wide **exact-needle** search only for evidence uniquely anchored to this signal, such as:

- direct references to exact signal body `0xbd2190`;
- exact `TProtocolMessageQueue` static-metaobject/method metadata once independently derived;
- exact signal index/name metadata tied to `clientMessageReadyToProcess`;
- a bounded local slice from such a reference to one `QObject::connectImpl` setup.

It may then inspect at most **one unique causally linked connect site** and at most **one endpoint identity edge**.

Stop if:

- exact-signal references are non-unique and cannot be disambiguated by local causal dataflow;
- no reference can be tied to a connect setup;
- more than one downstream connect site survives the exact-signal discriminator;
- endpoint identity is non-unique.

Do **not** perform a generic executable-wide census of:

- all `QObject::connectImpl` callers;
- all QObject/QSlot instances;
- all sockets/network/transport/writer classes;
- all queue constructors;
- all signal bodies.

Do not redo #885 QSlot construction, #890 receiver typing or #895 constructor-local enumeration.

## Strict safety

Forbidden:

- official-client execution;
- login or credential/session/cookie/character/world access;
- process-memory access;
- packet capture;
- OCR/Vision;
- official-service E2E;
- runtime Field6 observation;
- Track B #284 mutation;
- guessing writer identity, Field6 value or pre-success order.

## TDD / implementation contract

1. Start from fresh trusted `main` on a dedicated independent source branch/Draft PR.
2. Persist complete Track A task ownership/admission metadata before material implementation.
3. Produce repository-only RED before client materialization.
4. Implement the smallest exact-signal-reference discriminator; reject generic connect/socket census helpers in contract tests.
5. Enforce exact version/size/SHA before analysis.
6. Emit deterministic sanitized JSON only and remove raw client bytes before artifact upload.
7. Run `git diff --check`, scoped syntax/compile validation, exact-head CI, Track A governance and self-hosted PR boundary where applicable.
8. Perform fresh whole-diff falsification before terminal handoff.

## Terminal outcomes

Positive only when one exact-signal connect setup and endpoint are uniquely proven:

```text
terminal_result=QUEUE_SIGNAL_BF_EXACT_XREF_CONNECT_SITE_PROVEN
NEXT_UNIQUE_RELAY_EDGE=<exact connect site>
NEXT_ENDPOINT_IDENTITY=<exact identity>
NEXT_RELAY_IDENTITY_PRESERVED=true
```

Otherwise:

```text
terminal_result=SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<first exact non-unique/unproven exact-signal reference/connect boundary>
```

Do not call an endpoint a queue/TCP writer unless exact source semantics independently prove that stronger role.

## Required final report

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
QUEUE_SIGNAL=clientMessageReadyToProcess
QUEUE_SIGNAL_INDEX=0xbf
QUEUE_SIGNAL_BODY=0xbd2190
QUEUE_SIGNAL_ARGV1_IDENTITY=exact GameclientMessage shared pair
EXACT_SIGNAL_REFERENCE_COUNT=<n>
EXACT_SIGNAL_CONNECT_CANDIDATE_COUNT=<n>
NEXT_UNIQUE_RELAY_EDGE=<value|UNKNOWN>
NEXT_ENDPOINT_IDENTITY=<value|UNKNOWN>
NEXT_RELAY_IDENTITY_PRESERVED=true|false
QUEUE_SIGNAL_WRITER_IDENTITY=<value|UNKNOWN>
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<value|UNKNOWN>
FIELD6_VALUE=UNKNOWN
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TRACK_B_PR_284_MODIFIED=false
terminal_result=<QUEUE_SIGNAL_BF_EXACT_XREF_CONNECT_SITE_PROVEN|SOURCE_BLOCKER>
FIRST_MISSING_BOUNDARY=<none|precise boundary>
NEXT_ACTION=<clean coordinator promotion or one newly admitted bounded step>
```

Stop when the exact-signal xref/connect-site question is terminal. Do not consume the parallel sendLogin field-use task.