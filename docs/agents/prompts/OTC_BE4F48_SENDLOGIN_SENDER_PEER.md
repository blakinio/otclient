# OTC-BE4F48-SENDLOGIN-SENDER-PEER

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous Track A, exact-current, source-only discriminator for the sender-side event/peer that causally binds native `TProtocolMessageQueue::sendLogin`.

## Objective

Close the first missing boundary promoted by `docs/agents/evidence/OTC-20260903-be4f48-prelogin-sequence-promotion/result.json`:

```text
exact-current sender-side native event/peer identity and direction for the connection that binds TProtocolMessageQueue::sendLogin
```

Do not reopen the completed #865 analyzer architecture. Start from its promoted exact-current facts and introduce only the smallest new falsifiable discriminator needed to identify the peer and causal direction.

## Fresh-state recovery

1. Read root `AGENTS.md`, `docs/agents/README.md`, and all mandatory Track A admission documents referenced there.
2. Refresh trusted `main`; live repository state wins over every SHA/run copied into this prompt.
3. Read:
   - `docs/agents/evidence/OTC-20260903-be4f48-prelogin-sequence-promotion/result.json`;
   - `docs/agents/evidence/OTC-20260903-be4f48-prelogin-sequence-promotion/20260903-coordinator-promotion.md`;
   - the archived promotion task for that evidence cut.
4. Verify source PR #865 remains terminal/consumed and do not resume it.
5. Resolve Track B PR #284 only to verify the cross-track hold. Do not modify its branch, task, workflow, code, runtime or E2E budget.
6. Search active Track A tasks/PRs for overlapping ownership before creating work.
7. Create a fresh task, fresh branch/worktree and early Draft PR with unique owned paths for this discriminator.

## Exact-client fence

Unless a newer trusted promotion has superseded it, the target is:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

Fail closed if the public package fence moved. Never silently apply addresses/offsets from another build.

## Promoted starting facts

Treat these as current anchors only after re-reading the promotion from fresh `main`:

```text
TProtocolMessageQueue::sendLogin QMeta index=196
queue signal_count=192
sendLogin QMeta target=0xde82a2
sendLogin external tail=0xde82ae -> 0xbd3050
sendLogin adapter FDE=0xbd3050..0xbd34dd
aligned adapter reference=0x7c6b34
adapter reference owner FDE=0x7c6700..0x7cc933
connection peer target=0xd052a0
connection helper target=0x4d8670
peer_qmeta_candidates=[]
bounded_gameclient_root_reachability=UNKNOWN_PEER_QMETA_IDENTITY
PRE_SUCCESS_SEND_SEQUENCE=UNKNOWN
```

These facts do not prove that the peer is a `TGameClient` QMeta method/signal. The prior hypothesis that it was directly identifiable through `TGameClient` QMeta was falsified.

## Required discriminator strategy

Work outward from the exact-current connection block and peer target, not from a new global search.

Allowed next evidence classes include, in bounded order:

1. exact peer FDE ownership and executable boundaries;
2. fresh RTTI/vtable/class-string ownership for the peer or its containing callable group;
3. constructor/destructor ownership links that bind the peer callable to a concrete current class;
4. fresh current QMeta or non-QMeta method-table evidence if the peer belongs to a different QObject/class;
5. bounded direct callers/xrefs only after a unique owner identity exists;
6. callsite-local dataflow that proves which endpoint is sender and which is receiver;
7. a second independent static derivation that falsifies the promoted identity/direction before promotion.

Do not add a broad BFS, generic whole-binary architecture crawler, global `+0x60` census, new protocol abstraction, feature toggle, or runtime experiment merely because the peer is still unknown.

## TDD and anti-loop

For every new analyzer/contract:

1. commit/record a real RED that fails before exact-client materialization when practical;
2. implement the smallest GREEN discriminator;
3. run once on the exact client;
4. inspect sanitized artifact output and treat scientific UNKNOWN as a valid terminal result;
5. if falsified, make at most one narrowly justified follow-up discriminator from the new evidence;
6. stop on the first real source boundary rather than increasing search breadth.

Green tests do not equal scientific proof.

## Safety

Static/source-only unless a future separate task independently proves runtime is necessary and obtains the required Track A authority. For this alias:

```text
runtime_access=none
official_client_execution=false
login=false
credentials=false
process_memory=false
packet_capture=false
official_service_e2e=false
raw_client_upload=false
```

Do not invoke local Vision/OCR for this task; it has no structural authority for callable identity or direction.

Never persist proprietary client bytes, credentials, sessions, cookies, character/world data or secret-bearing artifacts. Output only deterministic sanitized structural evidence.

## Acceptance

A positive result requires all of:

- exact current fence proven;
- peer callable identity proven to a concrete current owner/class/function role, not guessed from address proximity;
- sender/receiver direction of the connection proven from callsite-local dataflow or equivalent exact static evidence;
- causal relation to `TProtocolMessageQueue::sendLogin` proven;
- independent falsification/cross-check agrees;
- exact-head CI/governance and scoped syntax/static checks pass;
- `git diff --check` passes;
- Track B #284 remains unchanged.

If the owner identity or direction cannot be proven with the bounded discriminator, terminate as `SOURCE_BLOCKER` with the exact first missing boundary.

## Terminal output

Report at least:

```text
trusted_main=<sha>
source_head=<sha>
current_client_version=<version>
current_client_sha256=<sha256>
peer_target=<sanitized exact-current target or UNKNOWN>
peer_owner_identity=<identity or UNKNOWN>
peer_role=<signal|method|callable|UNKNOWN>
sender_endpoint_identity=<identity or UNKNOWN>
receiver_endpoint_identity=<identity or UNKNOWN>
sendlogin_causal_binding_proven=true|false
pre_login_sequence_advanced=true|false
runtime_access=none
official_service_e2e_count=0
track_b_pr_284_modified=false
terminal_result=SENDER_PEER_IDENTITY_PROVEN|SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<none or exact source boundary>
next_action=<one concrete step or none>
```

If `SENDER_PEER_IDENTITY_PROVEN`, do not mutate #284. Persist the source result and hand it to a clean coordinator promotion so it can be combined with the independent final-writer lane.
