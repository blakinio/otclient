# Canary Current inbound logical-message fixtures

These are original synthetic hexadecimal fixtures for the bounded P2 decoder. They represent already decrypted and deframed logical messages only.

Provenance:

- producer repository: `blakinio/canary`
- producer revision: `bc0068ab80bbf003e128fce0589b4cc89d2682d3`
- generated index: `oteryn-canary-source-index-v1`
- source file: `src/server/network/protocol/protocolgame.cpp`
- pending-state producer: `sendPendingStateEntered`, source line 8502
- session-end producer: `sendSessionEndInformation`, source line 2932
- session-end enum: `src/server/server_definitions.hpp::SessionEndInformations`

The fixtures contain no credential, session key, private capture, proprietary asset byte or copied producer implementation body. Unknown session-end reason `0x01` and trailing data are negative cases and must fail closed.
