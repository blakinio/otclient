# Client regression-test backlog

This backlog records focused follow-up tests. Entries are not disabled or
expected-failure tests in the foundation suite; each should land with the
corresponding production correction when one is required.

| Case | Issue / PR | Area | Test level | Minimal fixture | Production fix needed | Priority |
| --- | --- | --- | --- | --- | --- | --- |
| Unknown opcode always advances or aborts without loop/OOM | Link the originating parser issue when selected | `ProtocolGame::parseMessage` | unit + protocol regression | builder containing one unknown opcode and bounded single-dispatch call | likely: extract one dispatch step with an explicit progress result | P0 |
| Ground border can be selected as use-with target | Link target-selection issue | `Tile::getTopMultiUseThing` / item flags | unit | synthetic ground-border and overlapping synthetic item | likely | P1 |
| Daily Reward sends the correct source flag | Link Daily Reward issue | `protocolgamesend.cpp`, reward module | unit + protocol contract | expected output bytes for one reward request | likely | P1 |
| Wheel conviction perks use the correct indices | Link Wheel issue | `modules/game_wheel` | Lua unit | small perk table and stub player | likely | P1 |
| Wheel fragment lookups use resource identifiers 84 and 85 | Link Wheel resource issue | `modules/gamelib/const.lua`, `modules/game_wheel` | Lua contract | parsed `ResourceTypes` table and static lookup scan | yes: plural uses currently do not match singular public constants | P0 |
| Forge refresh updates only the intended resource balances | Link Forge issue | Forge parser and module | protocol + Lua integration | resource-balance packets and fake local player | likely | P1 |
| VIP list retains every received entry | Link VIP issue | VIP parsing and game state | protocol regression | two-entry VIP packet builder | likely | P1 |
| Resource aliases never silently resolve to `BANK_BALANCE` | Follow-up contract PR | resource constants | C++/Lua contract | parsed resource table plus approved alias allow-list | no unless a bad alias exists | P0 |
| Tile top-use ordering remains stable with overlapping categories | Follow-up tile suite | `tile.cpp` | unit | synthetic ground, bottom, common, creature, and top items | no unless behaviour defect is exposed | P1 |
| Malformed OTML indentation reports the correct source location | Follow-up OTML suite | `otmlparser.cpp` | unit | small `.otml` fixture | unknown | P2 |
| Empty and corrupt configuration files have explicit outcomes | Follow-up configuration suite | startup/config loading | unit | empty file and invalid scalar fixture | possibly: isolate configuration reader | P2 |
| Client receives one framed packet from a loopback peer and closes | Follow-up protocol harness | `Connection` + `Protocol` | integration | local random-port server and one framed message | possibly: injectable connection callback | P1 |
| Core startup loads configuration and modules without GPU/audio | Architecture follow-up | application bootstrap | integration + startup | licensed repository configuration and stub adapters | yes: split bootstrap lifecycle | P2 |

Priorities: P0 protects process safety or a public wire/data contract; P1
protects common game-state behaviour; P2 requires a broader test seam or covers
lower-frequency startup/parser behaviour.
