# Canary Protocol Source Index Generator

This standard-library-only tool generates bounded exact-source evidence from a separately checked-out Canary producer tree.

It records:

- exact producer revision, release/client constants and source hashes;
- literal client-to-server dispatch opcodes and handler/source anchors;
- server-to-client `send*` methods and the first local literal opcode when present;
- observed `ProtocolFeature` and build/version gates in each local function body;
- deterministic family, state-prerequisite and proposed package metadata;
- explicit unresolved declarations and sends without a local literal opcode;
- fixture feasibility/provenance metadata without packet bytes.

It does **not** copy producer function bodies, fetch network content, store credentials/session keys/private captures/proprietary assets, or claim that the inspected producer commit is deployed.

## Run

```text
python oteryn-client/tools/canary-protocol-index/generate.py \
  --source-root ../canary \
  --producer-revision bc0068ab80bbf003e128fce0589b4cc89d2682d3 \
  --protocol-output oteryn-client/docs/evidence/playability/p1/canary-current-source-index.md \
  --fixture-output oteryn-client/docs/evidence/playability/p1/canary-current-fixture-index.md \
  --json-output oteryn-client/tools/canary-protocol-index/generated/current-index.json
```

## Validate

```text
python -m unittest discover \
  -s oteryn-client/tools/canary-protocol-index \
  -p 'test_*.py'
```

Generate twice from the same exact source tree and require byte-identical outputs. `UNKNOWN`, `unresolved` and `declared-send-no-literal` are review blockers for the affected method, not permission to infer neighboring wire layouts.
