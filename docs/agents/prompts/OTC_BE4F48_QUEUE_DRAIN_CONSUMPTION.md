# OTC-BE4F48-QUEUE-DRAIN-CONSUMPTION

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous Track A exact-current source-only discriminator.

## Objective

Resolve only the newly promoted queue-drain boundary for official Linux client `15.32.be4f48`:

```text
proved exact queued GameclientMessage 16-byte identity
-> owned queue callback 0xbd2190
-> causal consumption of that exact queued object
-> next uniquely bound writer edge only while object/buffer identity remains intact
```

Do not reopen the completed #870 analyzer family and do not broaden into a generic TCP/socket/writer census.

## Fresh-state recovery

1. Refresh trusted `main` and treat live Git/PR/task state as authority.
2. Read root `AGENTS.md`, Track A mandatory admission documents, and `docs/agents/evidence/OTC-20260903-be4f48-post869-870-promotion/20260903-coordinator-promotion.md` plus its `result.json`.
3. Verify the exact client fence has not been superseded:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

4. Verify no open task/PR already owns this exact alias/paths.
5. Create a new independent Track A task, branch and Draft PR before substantial implementation.

## Promoted facts you may trust under this exact fence

```text
sendLogin adapter target=0xbd3050
serialized queue object identity=16-byte pair {object=allocation+0x10, owner=allocation}
that pair is copied unchanged into TProtocolMessageQueue storage
queue insertion vslot target=0xbd24a0
owned drain candidate count=1
owned drain candidate=0xbd2190
owned drain FDE=0xbd2190..0xbd2495
causal consumption of exact queued GameclientMessage by 0xbd2190=NOT_PROVEN
final queue writer=UNKNOWN
final TCP writer=UNKNOWN
final writer contract=UNKNOWN
```

Known downstream packet/frame seeds are discovery input only and must not be promoted without a causal path from the exact queued object.

## Bounded discriminator

Use the smallest object/dataflow analysis capable of proving or falsifying consumption:

1. Re-derive the exact 16-byte queue-item identity and queue insertion before following the consumer.
2. Analyze only the unique owned callback `0xbd2190` and the queue members/storage proven to carry that item.
3. Prove consumption only if the exact queued object/owner pair (or a uniquely identity-preserving derivative) flows into the callback's semantic consumer path.
4. Require a second independent ownership/vtable/caller cross-check before assigning a writer identity.
5. If causal consumption is proven and there is exactly one next writer edge preserving object/buffer identity, follow that one edge only.
6. Stop immediately when identity forks, a callback target is non-unique, or the next writer edge cannot be distinguished statically.

Forbidden escalation: global socket/QMeta/TCP sweep, broad call graph, feature changes, runtime observation, process memory, packet capture, OCR/Vision, official-client execution, login or official-service E2E.

## TDD / validation contract

Any new analyzer/contract must follow RED -> GREEN:

- repository-only RED before exact-client materialization;
- exact SHA/size/version guard;
- deterministic sanitized JSON output;
- no proprietary client bytes in artifacts;
- no secrets/account/session values;
- `runtime_access:none`;
- scoped syntax/static checks and `git diff --check`;
- exact-head CI, Track A governance and self-hosted boundary as applicable;
- independent falsification for a positive consumption/writer identity.

Green analyzer tests alone are not a PASS.

## Terminal outcomes

Stop with one of:

```text
QUEUE_DRAIN_CONSUMPTION_PROVEN
FINAL_QUEUE_WRITER_PROVEN
SOURCE_BLOCKER
```

`FINAL_QUEUE_WRITER_PROVEN` is legal only if causal consumption of the exact queued object is already proven and the next writer identity is unique under two independent static checks. Do not claim final TCP writer unless separately and causally proven.

## Track B boundary

Do not modify PR #284. Do not guess Field6. Do not authorize an official-service E2E. This lane produces source evidence only; any material result must later be consumed by a clean coordinator promotion.

## Required final status

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
SERIALIZED_QUEUE_OBJECT_IDENTITY_PROVEN=true|false
OWNED_DRAIN_CALLBACK=0xbd2190|UNKNOWN
QUEUED_GAMECLIENTMESSAGE_CAUSAL_CONSUMPTION=true|false
NEXT_UNIQUE_WRITER_EDGE=<proved target or UNKNOWN>
FINAL_QUEUE_WRITER_IDENTIFIED=true|false
FINAL_TCP_WRITER_IDENTIFIED=true|false
FINAL_WRITER_CONTRACT=<proved or UNKNOWN>
TRACK_B_PR_284_MODIFIED=false
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TERMINAL_RESULT=QUEUE_DRAIN_CONSUMPTION_PROVEN|FINAL_QUEUE_WRITER_PROVEN|SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<exact boundary or none>
NEXT_ACTION=<one concrete repository-owned continuation step or coordinator promotion>
```
