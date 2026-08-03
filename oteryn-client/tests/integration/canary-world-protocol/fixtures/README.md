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

Login side-preamble fixtures prove the exact pinned Current order after local
player initialization and before pending-state: `sendAllowBugReport` emits fixed
`1A 00`, followed by `sendTibiaTime` as `EF + two opaque u8 clock components`.
The synthetic clock bytes are not retained and no world-light state is inferred.
