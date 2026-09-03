# OTC-BE4F48-FINAL-LOGIN-WRITER

Repository: `https://github.com/blakinio/otclient`

Mode: autonomous Track A, exact-current, source-only discriminator for the final queue/TCP writer contract used by native game login.

## Objective

Close the second missing boundary promoted by `docs/agents/evidence/OTC-20260903-be4f48-prelogin-sequence-promotion/result.json`:

```text
sendLogin serialized queue object -> final queue/TCP writer contract
```

Do not reopen the completed #865 pre-login analyzer. Do not rerun the old writer search as a generic global sweep. Start from the already-proven current `sendLogin` QMeta/adapter facts and the independent exact-current writer evidence, then add only the smallest discriminator needed to bind the serialized login object to the unique final queue/TCP egress contract.

## Fresh-state recovery

1. Read root `AGENTS.md`, `docs/agents/README.md`, and all mandatory Track A admission documents referenced there.
2. Refresh trusted `main`; live repository state wins over every SHA/run copied into this prompt.
3. Read:
   - `docs/agents/evidence/OTC-20260903-be4f48-prelogin-sequence-promotion/result.json`;
   - `docs/agents/evidence/OTC-20260903-be4f48-prelogin-sequence-promotion/20260903-coordinator-promotion.md`;
   - the archived promotion task;
   - the exact-current writer source/evidence referenced by the promotion.
4. Verify source PR #865 is terminal/consumed. Do not modify or revive it.
5. Resolve Track B PR #284 only to verify the cross-track hold. Do not modify its branch, task, code, workflow, runtime or E2E budget.
6. Search active Track A tasks/PRs for overlapping writer ownership before creating work.
7. Create a fresh task, fresh branch/worktree and early Draft PR with unique writer-discriminator paths.

## Exact-client fence

Unless a newer trusted promotion superseded it, target:

```text
version=15.32.be4f48
size=52105824
sha256=552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1
```

Fail closed if the public package fence moved. Never transfer addresses/offsets from another client build.

## Promoted starting facts

After fresh-main verification, the current evidence cut contains:

```text
current_sendlogin_qmeta=PROVEN
sendLogin QMeta target=0xde82a2
sendLogin first external tail=0xde82ae -> 0xbd3050
sendLogin adapter FDE=0xbd3050..0xbd34dd
sendLogin adapter indirect calls=PROVEN
final_writer_contract=UNKNOWN
final_queue_writer=UNKNOWN
final_tcp_writer=UNKNOWN
```

The exact-current writer run is independently referenced in the promotion. Reuse its sanitized artifacts and code only as discovery input; do not promote discovery-only TCP/QMeta candidates into a final contract without a causal object/buffer path.

## Required discriminator strategy

Begin at the proven `sendLogin` adapter and its indirect calls. The preferred bounded order is:

1. classify each adapter indirect call target by fresh current vtable/RTTI/FDE ownership;
2. identify the call that consumes or forwards the serialized `GameclientMessageLogin`/queue message object;
3. prove the object/buffer transition into the queue writer using callsite-local register/stack/member dataflow;
4. follow only that uniquely bound writer object into the next write/send abstraction;
5. prove the final TCP/socket egress callable or an equivalent unique wire-writer contract;
6. recover framing/length/checksum/encryption ownership only when it lies on that proved path and is necessary to state the final contract;
7. independently falsify the final writer identity using a second source such as vtable ownership, unique direct caller, object field ownership, or a separate exact-current serialization path.

Do not use generic socket-function xref counts, symbol-name proximity, address adjacency, broad QMeta enumeration, or a whole-binary TCP writer sweep as proof. Discovery candidates are not final writer identity.

## TDD and anti-loop

For every new analyzer/contract:

1. create a real RED first, preferably before client materialization;
2. implement the smallest GREEN discriminator;
3. run once against the exact client;
4. inspect sanitized output and accept scientific UNKNOWN as terminal;
5. if one assumption is falsified, make only the smallest evidence-derived correction;
6. do not expand into a new writer architecture/framework merely to avoid `SOURCE_BLOCKER`.

Green analyzer tests are not proof that the final writer is identified.

## Safety

This alias is static/source-only:

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

Do not invoke local Vision/OCR for final-writer proof; visual output has no structural authority for queue/TCP dataflow.

Never persist proprietary client bytes or protected account/session material. Artifacts must be deterministic and sanitized.

## Acceptance

A positive result requires all of:

- exact current client fence proven;
- unique causal path from native `sendLogin` serialized message/queue object to a concrete queue writer proven;
- unique causal path from that writer to final TCP/socket egress or equivalent final wire-writer contract proven;
- object/buffer identity preserved across the boundary strongly enough to exclude unrelated queue/network writers;
- independent falsification/cross-check agrees;
- exact-head CI/governance plus scoped syntax/static checks pass;
- `git diff --check` passes;
- no mutation of Track B PR #284.

Do not require a semantic Field6 value to prove writer ownership; Field6 value is a separate unresolved boundary. Conversely, proving the writer does not authorize guessing Field6 or changing #284.

If final queue/TCP writer identity cannot be proven by the bounded path, terminate as `SOURCE_BLOCKER` with the exact first missing dataflow/ownership edge.

## Terminal output

Report at least:

```text
trusted_main=<sha>
source_head=<sha>
current_client_version=<version>
current_client_sha256=<sha256>
sendlogin_adapter_identified=true|false
serialized_queue_object_identity=<identity or UNKNOWN>
final_queue_writer_identified=true|false
final_queue_writer_identity=<identity or UNKNOWN>
final_tcp_writer_identified=true|false
final_tcp_writer_identity=<identity or UNKNOWN>
final_writer_contract=<sanitized contract or UNKNOWN>
field6_value=UNKNOWN|<only if independently proven elsewhere>
runtime_access=none
official_service_e2e_count=0
track_b_pr_284_modified=false
terminal_result=FINAL_WRITER_CONTRACT_PROVEN|SOURCE_BLOCKER
FIRST_MISSING_BOUNDARY=<none or exact source boundary>
next_action=<one concrete step or none>
```

If `FINAL_WRITER_CONTRACT_PROVEN`, do not mutate #284. Persist the source result and hand it to a clean coordinator promotion so it can be combined with the independent sender/peer lane before any Track B decision.
