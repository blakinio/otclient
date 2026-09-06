from __future__ import annotations

import hashlib
import pathlib
import shlex
import struct
import sys

EXPECTED_SIZE = 52_105_824
EXPECTED_SHA256 = "552dcf794c41dae8c3dca10b740cd23e2f2ebcaf82d86576e8a67d924409e4e1"

RTTI = {
    "game_client": (
        "N5tibia6client11TGameClientE",
        0x30ACD08,
        "tibia::client::TGameClient",
    ),
    "character_controller": (
        "N5tibia10gamewindow29TCharacterSelectionControllerE",
        0x30C29A8,
        "tibia::gamewindow::TCharacterSelectionController",
    ),
    "player_protocol_handler": (
        "N5tibia4game29TPlayerProtocolMessageHandlerE",
        0x30BE640,
        "tibia::game::TPlayerProtocolMessageHandler",
    ),
    "gameserver_game_session": (
        "N5tibia4game22TGameserverGameSessionE",
        0x30AEFA0,
        "tibia::game::TGameserverGameSession",
    ),
    "worldmap_handler": (
        "N5tibia8worldmap31TWorldmapProtocolMessageHandlerE",
        0x30BF1F0,
        "tibia::worldmap::TWorldmapProtocolMessageHandler",
    ),
}


def _parse_elf(raw: bytes):
    if raw[:4] != b"\x7fELF" or raw[4] != 2 or raw[5] != 1:
        raise RuntimeError("CURRENT_CLIENT_NOT_ELF64_LE")
    shoff = struct.unpack_from("<Q", raw, 0x28)[0]
    shentsize = struct.unpack_from("<H", raw, 0x3A)[0]
    shnum = struct.unpack_from("<H", raw, 0x3C)[0]
    sections = []
    for index in range(shnum):
        offset = shoff + index * shentsize
        _, stype, flags, addr, file_offset, size, _, _, _, entsize = struct.unpack_from(
            "<IIQQQQIIQQ", raw, offset
        )
        sections.append((stype, flags, addr, file_offset, size, entsize))
    relocs: list[tuple[int, int]] = []
    for stype, _, _, file_offset, size, entsize in sections:
        if stype != 4:  # SHT_RELA
            continue
        step = entsize or 24
        for offset in range(file_offset, file_offset + size, step):
            if offset + 24 > len(raw):
                break
            r_offset, _, r_addend = struct.unpack_from("<QQq", raw, offset)
            relocs.append((r_offset, r_addend))
    return sections, relocs


def _helpers(raw: bytes, sections, relocs):
    def off_to_va(offset: int):
        for _, _, addr, file_offset, size, _ in sections:
            if file_offset <= offset < file_offset + size:
                return addr + offset - file_offset
        return None

    def va_to_off(va: int):
        for _, _, addr, file_offset, size, _ in sections:
            if addr <= va < addr + size:
                return file_offset + va - addr
        raise ValueError(hex(va))

    def u32(va: int) -> int:
        return struct.unpack_from("<I", raw, va_to_off(va))[0]

    def i32(va: int) -> int:
        return struct.unpack_from("<i", raw, va_to_off(va))[0]

    def qword(va: int) -> int:
        return struct.unpack_from("<Q", raw, va_to_off(va))[0]

    def bytes_at(va: int, size: int) -> bytes:
        offset = va_to_off(va)
        return raw[offset : offset + size]

    def executable(va: int) -> bool:
        return any((flags & 4) and addr <= va < addr + size for _, flags, addr, _, size, _ in sections)

    by_addend: dict[int, list[int]] = {}
    by_offset: dict[int, list[int]] = {}
    for r_offset, addend in relocs:
        by_addend.setdefault(addend, []).append(r_offset)
        by_offset.setdefault(r_offset, []).append(addend)

    def relocated_value(va: int):
        values = by_offset.get(va, [])
        if values and len(set(values)) == 1:
            return values[0]
        try:
            return qword(va)
        except (ValueError, struct.error):
            return None

    def exact_rtti_vptr(mangled: str) -> int:
        needle = mangled.encode() + b"\0"
        name_vas = []
        start = 0
        while True:
            pos = raw.find(needle, start)
            if pos < 0:
                break
            if pos == 0 or raw[pos - 1] == 0:
                va = off_to_va(pos)
                if va is not None:
                    name_vas.append(va)
            start = pos + 1
        candidates = []
        for name_va in name_vas:
            for target in by_addend.get(name_va, []):
                typeinfo = target - 8
                for target2 in by_addend.get(typeinfo, []):
                    header = target2 - 8
                    try:
                        if qword(header) != 0:
                            continue
                    except (ValueError, struct.error):
                        continue
                    vptr = header + 16
                    first = relocated_value(vptr)
                    if first and executable(first):
                        candidates.append(vptr)
        candidates = sorted(set(candidates))
        if len(candidates) != 1:
            raise RuntimeError(f"RTTI_NOT_UNIQUE:{mangled}:{candidates!r}")
        return candidates[0]

    def qstring(base: int, index: int) -> str:
        relative = u32(base + 8 * index)
        length = u32(base + 8 * index + 4)
        return bytes_at(base + relative, length).decode("utf-8")

    return u32, i32, bytes_at, exact_rtti_vptr, qstring


def _check_target(raw: bytes, i32, bytes_at, table: int, ordinal: int, expected_target: int, expected_fence: str):
    target = table + i32(table + 4 * ordinal)
    if target != expected_target:
        raise RuntimeError(f"QMETA_TARGET_MISMATCH:{target:#x}!={expected_target:#x}")
    fence = bytes_at(target, 32)
    if fence.hex() != expected_fence:
        raise RuntimeError(f"QMETA_FENCE_MISMATCH:{expected_target:#x}")
    if raw.count(fence) != 1:
        raise RuntimeError(f"QMETA_FENCE_NOT_UNIQUE:{expected_target:#x}")


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        raise SystemExit("usage: current_sha_native_login_gate.py CLIENT OUTPUT_ENV")
    client = pathlib.Path(argv[1])
    output = pathlib.Path(argv[2])
    raw = client.read_bytes()
    if len(raw) != EXPECTED_SIZE or hashlib.sha256(raw).hexdigest() != EXPECTED_SHA256:
        raise RuntimeError("CURRENT_EXACT_CLIENT_MISMATCH")

    sections, relocs = _parse_elf(raw)
    u32, i32, bytes_at, exact_rtti_vptr, qstring = _helpers(raw, sections, relocs)

    proven = {}
    for name, (mangled, expected, _) in RTTI.items():
        actual = exact_rtti_vptr(mangled)
        if actual != expected:
            raise RuntimeError(f"RTTI_VPTR_MISMATCH:{name}:{actual:#x}!={expected:#x}")
        proven[name] = actual
        print(f"CURRENT_RTTI_{name.upper()}_VPTR=0x{actual:x}")

    # TGameClient: method 17 = onRequestLoginWithCredentials(QString,QString)
    game_base = 0x1CB3CF4
    game_data = 0x1CB3740
    game_row = tuple(u32(game_data + 4 * (14 + 6 * 17 + j)) for j in range(6))
    if qstring(game_base, 31) != "onRequestLoginWithCredentials" or game_row != (31, 2, 311, 2, 8, 26):
        raise RuntimeError("CURRENT_AUTH_QMETA_ROW_MISMATCH")
    _check_target(
        raw,
        i32,
        bytes_at,
        0x1D8F2C4,
        17,
        0xD18D70,
        "488b5110488b71084883c4485b5de94d679cff0f1f440000488bbfa009000048",
    )
    print("CURRENT_AUTH_CONTRACT=PASS")

    # TCharacterSelectionController: requestCharacterLogin(TCharacterLoginData)
    # and onCharacterSelectionConfirmed(QList<int> SelectedCharacters).
    char_base = 0x1CC3C14
    char_data = 0x1CC37C0
    request_row = tuple(u32(char_data + 4 * (74 + j)) for j in range(6))
    confirm_row = tuple(u32(char_data + 4 * (74 + 6 * 11 + j)) for j in range(6))
    if qstring(char_base, 1) != "requestCharacterLogin" or qstring(char_base, 3) != "tibia::authentication::TCharacterLoginData":
        raise RuntimeError("CURRENT_CHARACTER_REQUEST_STRINGS_MISMATCH")
    if qstring(char_base, 16) != "onCharacterSelectionConfirmed" or qstring(char_base, 17) != "QList<int>" or qstring(char_base, 18) != "SelectedCharacters":
        raise RuntimeError("CURRENT_CHARACTER_CONFIRM_STRINGS_MISMATCH")
    if request_row != (1, 1, 230, 2, 6, 13) or confirm_row != (16, 1, 245, 2, 10, 26):
        raise RuntimeError("CURRENT_CHARACTER_QMETA_ROW_MISMATCH")
    if (u32(char_data + 4 * 231), u32(char_data + 4 * 232)) != (0x80000003, 2):
        raise RuntimeError("CURRENT_CHARACTER_REQUEST_PARAM_MISMATCH")
    if tuple(u32(char_data + 4 * i) for i in (245, 246, 247)) != (43, 0x80000011, 18):
        raise RuntimeError("CURRENT_CHARACTER_CONFIRM_PARAM_MISMATCH")
    _check_target(
        raw,
        i32,
        bytes_at,
        0x1D97EE4,
        0,
        0xD516C0,
        "498b442408f30f6f08488b100f298c2480000000488b481048898c2490000000",
    )
    _check_target(
        raw,
        i32,
        bytes_at,
        0x1D97EE4,
        11,
        0xD51690,
        "498b7424084881c4f80000005b5d415c415d415e415fe995b9afff0f1f440000",
    )
    print("CURRENT_CHARACTER_CONTRACT=PASS")

    # TAuthenticationProcessController: selected-character progression surface.
    auth_base = 0x1CAB760
    auth_data = 0x1CAB140
    request_gs_row = tuple(u32(auth_data + 4 * (14 + 6 * 5 + j)) for j in range(6))
    start_gs_row = tuple(u32(auth_data + 4 * (14 + 6 * 27 + j)) for j in range(6))
    if qstring(auth_base, 7) != "requestCharacterGameserverLogin" or qstring(auth_base, 34) != "onStartGameServerLoginStateEntered":
        raise RuntimeError("CURRENT_GAMESERVER_STRINGS_MISMATCH")
    if request_gs_row != (7, 0, 325, 2, 262, 6) or start_gs_row != (34, 0, 355, 2, 8, 32):
        raise RuntimeError("CURRENT_GAMESERVER_QMETA_ROW_MISMATCH")
    _check_target(
        raw,
        i32,
        bytes_at,
        0x1D8EE20,
        5,
        0xD0F3A7,
        "31c9ba05000000e981faffff31c9ba04000000e975faffff4883c4305b5d415c",
    )
    _check_target(
        raw,
        i32,
        bytes_at,
        0x1D8EE20,
        27,
        0xD0F1E2,
        "4883c4305b5d415ce9b1e9a4ff488b4108ba08000000488d4c2410488d351cab",
    )
    print("CURRENT_GAMESERVER_ROUTE_CONTRACT=PASS")

    target_names = ("player_protocol_handler", "gameserver_game_session", "worldmap_handler")
    targets = ";".join(
        f"{name},{proven[name]:x},{RTTI[name][2]}" for name in target_names
    )
    output.write_text(
        "TARGETS=" + shlex.quote(targets) + "\n"
        + f"CHARACTER_CONTROLLER_VPTR={proven['character_controller']:x}\n",
        encoding="utf-8",
    )
    print("CURRENT_INGAME_MARKER_CONTRACT=PASS")
    print("CURRENT_EXACT_SHA_NATIVE_LOGIN_GATES=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
