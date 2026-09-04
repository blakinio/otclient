# be4f48 sendLogin receiver identity plan

1. Prove repository-only RED with `receiver_identity.py` absent; package/client steps must skip.
2. Implement one exact-fenced static analyzer bounded to connection owner FDE `0x7c6700..0x7cc933`, receiver field `+0x88`, and only directly evidence-derived ownership/type edges.
3. Re-derive the selected `connectImpl@0x7c6b9f` receiver provenance, then search reaching field definition/ownership without global QMeta/QObject census.
4. Promote receiver class identity only with independent QMeta/RTTI/vtable/constructor evidence; otherwise stop SOURCE_BLOCKER at the first non-unique edge.
5. If receiver identity is proven, prove or reject the complete sender/receiver pair and adapter causality; do not enter queue-signal/writer scope.
6. Persist sanitized result, exact-head CI/governance/self-hosted boundary, whole-diff falsification, then hand off to clean coordinator promotion. No runtime/E2E/Track B mutation.
