# OTC-BE4F48-SENDLOGIN-PEER-METAOWNER

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous Track A exact-current source-only discriminator.

## Objective

Resolve only the newly promoted sender-side boundary for official Linux client `15.32.be4f48`:

```text
static QMetaObject anchor 0x30b68a0 + signal index 0
-> exact peer class/metaobject owner
-> actual bounded Qt connection primitive and sender/receiver direction
-> causal relation to proved TProtocolMessageQueue::sendLogin adapter, if and only if uniquely proven
```

Do not reopen the completed #869 analyzer family and do not reuse `0x4d8670` as a connection helper.

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
adapter reference site=0x7c6b34
adapter reference owner FDE=0x7c6700..0x7cc933
peer target=0xd052a0
peer FDE=0xd052a0..0xd052c7
peer role=QT_SIGNAL_BODY_CALLING_QMETAOBJECT_ACTIVATE
peer QMetaObject::activate PLT target=0x4d7dc0
peer static-metaobject argument=0x30b68a0
peer signal index argument=0
0x4d8670=operator new(unsigned long)
0x4d8670 is NOT a Qt connection primitive
peer class owner=UNKNOWN
sender/receiver direction=UNKNOWN
causal signal->sendLogin binding=NOT_PROVEN
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
```

Historical addresses from other exact-client cuts remain non-authoritative unless freshly rederived.

## Bounded discriminator

Use the smallest evidence-driven route capable of proving or falsifying the missing boundary:

1. Decode the exact `QMetaObject`/meta-data/string-data ownership reachable from `0x30b68a0` and identify the peer class owner only when the layout/string evidence is unique and internally consistent.
2. Bind signal index `0` to that exact class/metaobject without inventing a semantic name when metadata is incomplete.
3. Reinspect only the already bounded connection-construction neighborhood that contains the proved adapter reference `0x7c6b34`.
4. Resolve PLT/relocation identities for candidate connection calls before assigning semantics.
5. Prove sender/receiver direction only from an actual Qt connection primitive/call contract plus object/dataflow identity; allocation helpers, adjacency and generic QObject references are insufficient.
6. If and only if the same bounded connection uniquely binds the proved peer signal to the proved `sendLogin` adapter, promote the causal binding. Otherwise stop at the first missing edge.

Forbidden escalation: global Qt connection census, broad subsystem BFS, generic RTTI sweep, runtime observation, process memory, packet capture, OCR/Vision, official-client execution, login or official-service E2E.

## TDD / validation contract

Any new analyzer/contract must follow RED -> GREEN:

- repository-only RED before exact-client materialization;
- exact SHA/size/version guard;
- deterministic sanitized JSON output;
- no proprietary client bytes in artifacts;
- no secrets or account/session values;
- `runtime_access:none`;
- scoped syntax/static checks and `git diff --check`;
- exact-head CI, Track A governance and self-hosted boundary as applicable;
- independent falsification for any positive promoted identity/direction.

Green analyzer tests alone are not a PASS.

## Terminal outcomes

Stop with one of:

```text
SENDLOGIN_PEER_METAOWNER_AND_DIRECTION_PROVEN
SOURCE_BLOCKER
```

A positive result requires all of:

```text
PEER_CLASS_OWNER=<exact unique identity>
PEER_SIGNAL_INDEX=0
ACTUAL_QT_CONNECTION_PRIMITIVE=<exact symbol/callsite>
SENDER_ENDPOINT_IDENTITY=<proved>
RECEIVER_ENDPOINT_IDENTITY=<proved>
SENDLOGIN_CAUSAL_BINDING_PROVEN=true
```

Anything weaker remains fail-closed.

## Track B boundary

Do not modify PR #284. Do not guess Field6. Do not authorize an official-service E2E. This lane produces source evidence only; any material result must later be consumed by a clean coordinator promotion.

## Required final status

```text
EXACT_CLIENT_FENCE_PROVEN=true|false
PEER_CLASS_OWNER=<proved or UNKNOWN>
ACTUAL_QT_CONNECTION_PRIMITIVE=<proved or UNKNOWN>
SENDER_ENDPOINT_IDENTITY=<proved or UNKNOWN>
RECEIVER_ENDPOINT_IDENTITY=<proved or UNKNOWN>
SENDLOGIN_CAUSAL_BINDING_PROVEN=true|false
PRE_SUCCESS_SEND_SEQUENCE=<proved advance or UNKNOWN>
TRACK_B_PR_284_MODIFIED=false
RUNTIME_ACCESS=none
OFFICIAL_SERVICE_E2E_COUNT=0
TERMINAL_RESULT=SENDLOGIN_PEER_METAOWNER_AND_DIRECTION_PROVEN|SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<exact boundary or none>
NEXT_ACTION=<one concrete repository-owned continuation step or coordinator promotion>
```
