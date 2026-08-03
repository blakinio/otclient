from pathlib import Path

required = {
    Path("oteryn-client/crates/protocol-canary/src/tile.rs"): [
        "decode_unknown_remote_player_appearance",
        "decode_current_unknown_remote_player_appearance",
        "GameEvent::EntityAppeared",
    ],
    Path("oteryn-client/tests/integration/canary-world-protocol/fixtures/remote-player-appearance.hex"): [
        "6A ",
        "61 00",
    ],
}

for path, markers in required.items():
    text = path.read_text(encoding="utf-8")
    for marker in markers:
        if marker not in text:
            raise RuntimeError(f"missing {marker!r} in {path}")
