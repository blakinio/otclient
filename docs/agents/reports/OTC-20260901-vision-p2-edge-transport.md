# OTC Vision P2 Edge Transport Report

## Delivery classification

```yaml
feature_scope:
  type: infrastructure
  user_facing: false
  backend_required: false
  frontend_required: false
  integration_required: true
  e2e_required: false
  completion_claim: partial_producer
runtime_access: none
mutation_authorized: false
physical_action_count: 0
```

This worker implements only the bounded Phase 2 edge-transport producer. The Control Center consumer/integration remains owned by `OTC-VISION-P2-CONTROL-BRIDGE`; this report makes no claim that Phase 2 as a whole is complete.

## Implemented slice

- outbound-only Synology-edge TCP initiator; no Synology listener is created;
- mutually authenticated HELLO/HELLO_ACK using distinct directional HMAC-SHA256 pairing keys (minimum 32 bytes each);
- random per-connection identity plus strict peer, connection, sequence, timestamp, schema and protocol-major binding;
- canonical signed JSON metadata with a 256 KiB frame bound;
- authority-neutral envelope fields are fixed to peer identity only, mutation false, physical budget zero, evidence-fresh false and action-resume false;
- duplicate JSON keys, wrong peer/key/version, replay, stale/future frames and authority-expansion attempts fail closed;
- reconnect requires a new explicit connection ID and cannot reset the replay window by rebinding the same ID;
- generic shell/process/GUI-control/secret-getter payload keys are rejected recursively;
- post-handshake generic send permits only HEARTBEAT and OBSERVATION metadata; artifact transfer has a separate path;
- content-addressed artifact-ref v1 carries SHA-256, exact size and plain media type;
- artifact bytes are transferred separately after the signed descriptor, bounded to 32 MiB, and receiver-side length/hash verification is provided;
- send failure latches the channel closed so a failed stream is never silently retried;
- concurrent sends are serialized and receive unique monotonic sequence numbers;
- pairing keys are redacted from object representations and never enter frame metadata.

## TDD evidence

RED-to-GREEN failures were observed for the missing module, duplicate-key rejection, content-addressed artifacts, reconnect binding, frame bounds, forbidden control payloads, outbound mutual-auth client, versioned artifact metadata, replay-window reset, failed-stream latching, concurrent sequence allocation, directional key reuse, separate artifact transfer, artifact size bounds, receiver length binding, artifact-path bypass and media-type admission.

Final focused result:

```text
python -m unittest tests.tools.tibia_re_control_center.test_agent_edge_transport
Ran 29 tests ... OK
```

Component result:

```text
python -m unittest tests.tools.tibia_re_control_center.test_agent_protocol tests.tools.tibia_re_control_center.test_agent_edge_transport
Ran 46 tests ... OK
```
Additional checks:

```text
python -m ruff check tools/tibia_re_control_center/agent_edge_transport.py tests/tools/tibia_re_control_center/test_agent_edge_transport.py
All checks passed!
python -m py_compile <both changed Python files>
PASS
git diff --check
PASS
```

A broader pre-existing Control Center agent-suite probe ran 170 tests and reported 5 errors in `agent_vision`/`agent_api` tests. The exact failures reproduce when those unowned tests are run individually. No production or test file from those failing areas imports `agent_edge_transport`; repository search finds references only in this worker's new focused test. They are recorded as unrelated current-suite/environment failures and were not modified or hidden by this worker.

## Runtime and authority evidence

No Synology/Kasm/Official Tibia runtime was observed or mutated. No login, credentials, GUI input, process control, process memory, network payload capture, canonical registration/lease mutation or physical action occurred.

The implementation authenticates transport peers only. It intentionally cannot establish Track A admission, runtime semantic freshness, `IN_GAME`, action authority or evidence freshness. Those remain downstream deterministic responsibilities.

## Handoff

The worker slice is ready for coordinator classification, not self-merge. The next consumer is `OTC-VISION-P2-CONTROL-BRIDGE`, which should consume the signed/verified metadata and content-addressed artifact interface rather than introducing a second edge protocol.

## Fresh resumed-worker validation

The previously dirty worker slice was independently revalidated before local commit. A stale test expected Python JSON recursion failure at depth 1100; on the current interpreter that depth parses successfully. Empirical tracing showed 1500+ triggers `RecursionError`; the test now uses depth 2000 and verifies the existing production catch maps it to `EDGE_FRAME_INVALID`. Production code did not require a fix.

Current local implementation commit: `c0015b470fd6792cbb03cd00bf0597c79bd54e11`.

Fresh results:
- focused edge transport: `29/29 PASS`;
- protocol + edge transport: `46/46 PASS`;
- Ruff / py_compile / checkpoint validator / Track A governance / `git diff --check`: PASS.

The commit is intentionally not pushed on the stale dispatch base. It waits for runtime-signals promotion PR #839, then will be restacked once on the resulting trusted main and revalidated before Draft PR #829 publication.

## Concurrent replay-window falsification and repair

Independent review after the first local checkpoint found that `EdgeTransportVerifier` updated replay/connection state without synchronization. A deterministic two-thread barrier test forced both verifications of the same signed `sequence=1` frame past validation before state commit; both were accepted, disproving the intended replay guarantee under concurrent receiver use.

The repair at `9fce716178820920cac1f605fc5402910c1bed6e` adds one verifier state `RLock`, keeps expensive parse/HMAC/payload validation outside the atomic state commit, then serializes the final replay check, connection binding and sequence advance. `bind_connection()` uses the same state lock. Invalid frames therefore still do not reserve sequence state, while concurrent duplicates can no longer both commit.

Fresh results after repair:
- focused edge transport: `30/30 PASS`;
- protocol + edge transport: `47/47 PASS`;
- Ruff / py_compile / checkpoint validator / Track A governance / `git diff --check`: PASS.

The branch remains local-only until PR #839 merges, after which it will be restacked once on trusted current main and revalidated before Draft PR #829 publication.

## Current-main restack and final worker-local gate

After coordinator promotion PR #839 merged, the worker branch was rebased cleanly onto current `main@e883543403d5430d7b1d287f59043b23c98f37d6`. The resulting diff still contains only the four declared owned paths.

Additional falsification/hardening retained on the restacked branch includes:
- deep snapshot of nested metadata before privacy admission/signing;
- explicit admitted local-network CIDRs rather than relying on broad `ipaddress.is_private` classification;
- normalized control-surface key rejection across separator variants;
- bounded/JSON-only metadata structure on sender and authenticated receiver;
- strict boolean rejection for protocol/budget integer fields and finite connection timeouts;
- atomic replay/connection state commit under concurrent verification.

Fresh post-restack results:
- focused edge transport: `30/30 PASS`;
- protocol + edge transport: `47/47 PASS`;
- Ruff / py_compile / checkpoint validator / Track A governance / `git diff --check`: PASS.

No live runtime observation or physical action was performed. The next gate is publication to Draft PR #829 and exact-head hosted CI; coordinator classification remains mandatory before any promotion.

## Exact-head CI portability repair

Published head `d6c3a1e5b1b253c11dea52bb10cf83c45b75d103` passed the repository `CI` and Track A governance workflows. Package A run `33555788479` and Package B run `33555788277` each failed exactly one test: `test_receiver_converts_json_recursion_failure_to_validation_error`; their independent audit jobs passed, and Package B browser/CLI E2E passed.

The hosted Ubuntu interpreter did not raise `RecursionError` for the test's fixed 2000-level JSON nesting, so verification continued to exact-key validation and returned `MISSING_FIELD`. This was a portability defect in the test assumption, not an absent production catch: `EdgeTransportVerifier.verify()` already maps a real `json.loads` `RecursionError` to `EDGE_FRAME_INVALID`.

The repair makes that exception-boundary test deterministic by injecting `RecursionError` at the parser seam and asserting the existing safe mapping. The real payload-depth and metadata-size protections remain separately exercised by non-mocked tests, so no safety criterion is weakened.

Local results after the repair remain focused `30/30 PASS` and protocol+transport `47/47 PASS`. A fresh exact-head hosted run is required after publication; no runtime access or physical action is involved.
