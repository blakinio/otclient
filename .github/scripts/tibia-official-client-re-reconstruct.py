#!/usr/bin/env python3
"""Reconstruct a hash-verified official native-Linux Tibia runtime for Track A."""

from __future__ import annotations

import concurrent.futures
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import subprocess
import tempfile
import urllib.parse


OUT = Path(os.environ["TIBIA_PACKAGE_OUT"])
SOCKS = os.environ.get("TIBIA_SOCKS", "127.0.0.1:25354")
PACKAGE_BASE = "https://static.tibia.com/launcher/tibiaclient-linux-current"
ASSET_BASE = "https://static.tibia.com/launcher/assets-current"
EXPECTED_PACKAGE_ENTRIES = 1634
EXPECTED_ASSET_ENTRIES = 7094
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/151.0.0.0 Safari/537.36"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_path(value: str) -> PurePosixPath:
    path = PurePosixPath(value)
    if path.is_absolute() or not path.parts or ".." in path.parts:
        raise RuntimeError("unsafe manifest path")
    return path


def fetch(url: str, target: Path) -> None:
    subprocess.run(
        [
            "curl", "--socks5-hostname", SOCKS, "--compressed", "-fL",
            "--retry", "4", "--retry-all-errors", "--retry-delay", "2",
            "--connect-timeout", "20", "--max-time", "300",
            "-A", UA, "-e", url, "-H", "Accept: */*", url, "-o", str(target),
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def load_manifest(base: str, name: str) -> object:
    with tempfile.NamedTemporaryFile(prefix="track-a-manifest-", delete=False) as handle:
        path = Path(handle.name)
    try:
        fetch(f"{base}/{name}", path)
        return json.loads(path.read_text(encoding="utf-8"))
    finally:
        path.unlink(missing_ok=True)


def rows(document: object) -> list[tuple[str, str, str | None]]:
    found: list[tuple[str, str, str | None]] = []

    def walk(value: object) -> None:
        if isinstance(value, dict):
            rel = value.get("url")
            packed = value.get("packedhash")
            unpacked = value.get("unpackedhash")
            if isinstance(rel, str) and isinstance(packed, str):
                safe_path(rel)
                found.append((rel, packed.lower(), unpacked.lower() if isinstance(unpacked, str) and unpacked else None))
            for child in value.values():
                walk(child)
        elif isinstance(value, list):
            for child in value:
                walk(child)

    walk(document)
    unique: dict[str, tuple[str, str | None]] = {}
    for rel, packed, unpacked in found:
        previous = unique.get(rel)
        if previous is not None and previous != (packed, unpacked):
            raise RuntimeError("conflicting manifest entry")
        unique[rel] = (packed, unpacked)
    return [(rel, *hashes) for rel, hashes in sorted(unique.items())]


def decode(packed: bytes, rel: str, expected: str | None, preserve_if_missing: bool) -> tuple[bytes, str]:
    if expected is None:
        if not preserve_if_missing:
            raise RuntimeError(f"missing unpacked hash: {rel}")
        return packed, rel
    output_rel = rel[:-5] if rel.endswith(".lzma") else rel
    if sha256(packed) == expected:
        return packed, output_rel
    if not rel.endswith(".lzma") or len(packed) < 45:
        raise RuntimeError(f"no hash-verified transform: {rel}")
    prop = packed[32]
    lc = prop % 9
    rest = prop // 9
    lp = rest % 5
    pb = rest // 5
    dictionary = int.from_bytes(packed[33:37], "little")
    if lc + lp > 4 or pb > 4 or dictionary <= 0 or dictionary > (1 << 30):
        raise RuntimeError(f"invalid LZMA header: {rel}")
    filt = {"id": lzma.FILTER_LZMA1, "dict_size": dictionary, "lc": lc, "lp": lp, "pb": pb}
    output = lzma.decompress(packed[45:], format=lzma.FORMAT_RAW, filters=[filt])
    if sha256(output) != expected:
        raise RuntimeError(f"unpacked hash mismatch: {rel}")
    return output, output_rel


def install(base: str, row: tuple[str, str, str | None], preserve_if_missing: bool) -> None:
    rel, packed_hash, unpacked_hash = row
    url = f"{base}/{urllib.parse.quote(rel, safe='/._-~')}"
    with tempfile.NamedTemporaryFile(prefix="track-a-object-", delete=False) as handle:
        temp = Path(handle.name)
    try:
        fetch(url, temp)
        packed = temp.read_bytes()
        if sha256(packed) != packed_hash:
            raise RuntimeError(f"packed hash mismatch: {rel}")
        output, output_rel = decode(packed, rel, unpacked_hash, preserve_if_missing)
        target = OUT.joinpath(*safe_path(output_rel).parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(output)
        if target.parts and "bin" in target.parts:
            target.chmod(0o700)
    finally:
        temp.unlink(missing_ok=True)


def batch(base: str, entries: list[tuple[str, str, str | None]], workers: int, preserve: bool, label: str) -> None:
    with concurrent.futures.ThreadPoolExecutor(max_workers=workers) as pool:
        for count, _ in enumerate(pool.map(lambda row: install(base, row, preserve), entries), 1):
            if count % 1000 == 0:
                print(f"TRACK_A_{label}_FILES={count}", flush=True)
    print(f"TRACK_A_{label}_FILES={len(entries)}")


def main() -> None:
    package = rows(load_manifest(PACKAGE_BASE, "package.json"))
    assets = rows(load_manifest(ASSET_BASE, "assets.json"))
    print(f"TRACK_A_PACKAGE_ENTRY_COUNT={len(package)}")
    print(f"TRACK_A_ASSET_ENTRY_COUNT={len(assets)}")
    if len(package) != EXPECTED_PACKAGE_ENTRIES or len(assets) != EXPECTED_ASSET_ENTRIES:
        raise RuntimeError("manifest cardinality changed")
    OUT.mkdir(parents=True, exist_ok=True)
    batch(PACKAGE_BASE, package, 8, False, "PACKAGE")
    batch(ASSET_BASE, assets, 12, True, "ASSET")
    print("TRACK_A_RUNTIME_RECONSTRUCTION_COMPLETE=true")


if __name__ == "__main__":
    main()
