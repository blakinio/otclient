# Canary Current inbound logical-message fixtures

These are original synthetic hexadecimal fixtures for the bounded P2 decoder. They represent already decrypted and deframed logical messages only.

Provenance:

- producer repository: `blakinio/canary`
- producer revision: `bc0068ab80bbf003e128fce0589b4cc89d2682d3`
- generated index: `oteryn-canary-source-index-v1`
- source file: `src/server/network/protocol/protocolgame.cpp`
- local-player producer: Current/non-legacy local branch of `sendAddCreature`, source body beginning after `sendAllowBugReport`
- pending-state producer: `sendPendingStateEntered`, source line 8502
- enter-world producer: `sendEnterWorld`, source line 8512
- session-end producer: `sendSessionEndInformation`, source line 2932
- session-end enum: `src/server/server_definitions.hpp::SessionEndInformations`

The fixtures contain no credential, session key, private capture, proprietary asset byte or copied producer implementation body. The local-player values and store URL are original synthetic field values used only to exercise the proven Current layout; the URL is never exposed by the decoder. Unknown session-end reason `0x01`, invalid login precision, zero identity and trailing data are negative cases and must fail closed.

Tile-clear fixtures prove only the complete Current absent-tile branch of
`sendUpdateTile`: opcode `0x69`, position encoded as `u16le/u16le/u8`, marker
`0x01` and terminator `0xFF`. Wrong marker, wrong terminator and trailing data
are negative cases. Coordinates are synthetic and no map contents are copied.

Validation checkpoint:

- focused Windows runner: `30831813507`, job `91747353789`, PASS;
- pinned Rust 1.94 formatting and strict package Clippy: PASS;
- protocol-canary package tests: 45 PASS;
- architecture tests and workspace dependency policy: PASS;
- exact current-main restack parent: `9ce5f2992889d4a780c5fb1d16566a3fbc59e14c`;
- restacked product commit before this checkpoint: `aaed93ff323d31ab9ae3e41be9ce67aff841f0ae`.
