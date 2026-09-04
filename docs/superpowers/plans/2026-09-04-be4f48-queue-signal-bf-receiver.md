# be4f48 queue signal 0xbf receiver plan

1. Prove repository-only RED with `signal_receiver.py` absent; package/client steps must skip.
2. Implement one exact-fenced static analyzer anchored only on `TProtocolMessageQueue` static metaobject `0x30b73e0`, signal index `0xbf`, and exact-current evidence-derived Qt connection sites.
3. Identify a unique connected receiver/slot for that exact signal without global Qt/socket/writer census.
4. Preserve exact `GameclientMessage` identity and promote receiver/writer only when the connection and object/dataflow remain causal and unique.
5. Follow at most one next writer edge and require an independent QMeta/RTTI/vtable/constructor/caller cross-check; otherwise stop SOURCE_BLOCKER.
6. Persist sanitized result, exact-head CI/governance/self-hosted boundary and fresh whole-diff falsification, then hand off to clean coordinator promotion. No runtime/E2E/Track B mutation.
