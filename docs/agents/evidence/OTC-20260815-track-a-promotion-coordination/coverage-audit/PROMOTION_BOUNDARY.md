# Track A coverage audit — coordinator promotion boundary

Source Draft PR: #304 (`research/OTC-20260815-track-a-coverage-registry-audit`)
Source exact head: `43a60bd96cc644b656b200c9edbfb75578b330b6`
Coordinator disposition: `ACCEPT_WITH_EDITS`
Exact-head source CI: run `31882010038` — `SUCCESS`
Client fence: official native Linux Tibia `15.32.df7b29`, size `51965216`, SHA-256 `e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe`

## Accepted bounded quantitative baseline

- protocol identifier inventory: `349/349` (`189` inbound, `160` outbound) — inventory only;
- directly enumerated inbound QMeta links: `27/349`;
- generated-message semantic support: `UNKNOWN/349`;
- ProtocolMessageHandler QMeta inventory: `47/47`;
- direct Qt callsite raw census: `2184/2184` with semantic classification `UNKNOWN/2184`;
- legacy string-connect selected subset: `40/41`;
- high-information GameAction sender metaobjects: `29/31` (`1` mismatch, `1` unresolved);
- P0 top-level requirement registry: `16/16`, while global P0 live-read coverage remains `UNKNOWN/UNKNOWN`;
- bridge-v1 profile-target inventory: `7/7`, while overall P1 field/evidence coverage remains `UNKNOWN/UNKNOWN`;
- P2 closure: `UNKNOWN/5`;
- restart/relogin stability: `UNKNOWN/1`.

## Provenance boundary

The promoted `source-snapshot/` files are exact Git blobs from the reviewed #304 head. The source validator proves internal registry integrity: classification/ID/provenance-reference validity, message-list decode/hash/count/uniqueness, selected-set denominators, arithmetic and retained supersession evidence.

It does **not** independently or cryptographically regenerate every compressed registry item from every historical source log. The coordinator independently rechecked the load-bearing exact-build source evidence for the 349 protocol inventory, 47 QMeta handler census and 2184 direct Qt callsite census before accepting this slice.

## Non-promotion boundary

This snapshot does not make inventory percentages semantic-completion percentages. It does not establish full protocol-message semantics, full QMeta semantics, a finite global P0 live-read denominator, authoritative direct player state, live bridge authority/session epoch, restart/relogin stability, P2 final egress/transforms, or A3/A4 action parity.

No runtime/login/gameplay experiment and no secret access are part of this promotion. Track A remains incomplete until the independently gated programme requirements are satisfied.
