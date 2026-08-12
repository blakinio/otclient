#!/usr/bin/env python3
"""Ephemerally reconstruct a Tibia package from the official manifest.

No package bytes are written to Git. Every transformation is accepted only when
its SHA-256 matches the manifest's unpackedhash.
"""
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

MANIFEST = Path(os.environ.get("TIBIA_MANIFEST", "/tmp/tibia-package/package.json"))
OUT = Path(os.environ.get("TIBIA_PACKAGE_OUT", "/tmp/tibia-package/runtime"))
BASE = os.environ["TIBIA_BASE_URL"].rstrip("/")
SOCKS = os.environ.get("TIBIA_SOCKS", "127.0.0.1:25344")
WORKERS = int(os.environ.get("TIBIA_DOWNLOAD_WORKERS", "8"))
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_rel(rel: str) -> PurePosixPath:
    p = PurePosixPath(rel)
    if p.is_absolute() or not p.parts or ".." in p.parts:
        raise RuntimeError("unsafe manifest path")
    return p


def lzma_raw_from_header(data: bytes, header_off: int) -> bytes:
    if len(data) < header_off + 14:
        raise lzma.LZMAError("short header")
    prop = data[header_off]
    lc = prop % 9
    rest = prop // 9
    lp = rest % 5
    pb = rest // 5
    if lc > 8 or lp > 4 or pb > 4 or lc + lp > 4:
        raise lzma.LZMAError("invalid properties")
    dict_size = int.from_bytes(data[header_off + 1 : header_off + 5], "little")
    if dict_size <= 0 or dict_size > (1 << 30):
        raise lzma.LZMAError("invalid dictionary")
    filt = {"id": lzma.FILTER_LZMA1, "dict_size": dict_size, "lc": lc, "lp": lp, "pb": pb}
    return lzma.decompress(data[header_off + 13 :], format=lzma.FORMAT_RAW, filters=[filt])


def decode_verified(data: bytes, rel: str, expected_hash: str) -> tuple[bytes, str, str]:
    """Return (unpacked bytes, output relative path, verified transform name)."""
    out_rel = rel[:-5] if rel.endswith(".lzma") else rel

    # Some manifest objects may already be stored in their final representation.
    if digest(data) == expected_hash:
        return data, out_rel, "identity"

    # CipSoft's normal packed object envelope: 32-byte prefix + 13-byte
    # LZMA-alone header + raw LZMA stream. The exact client uses this shape.
    if rel.endswith(".lzma") and len(data) >= 46:
        try:
            out = lzma_raw_from_header(data, 32)
            if digest(out) == expected_hash:
                return out, out_rel, "cipsoft-envelope"
        except lzma.LZMAError:
            pass

    # Very small package entries use compact representations. Accept only a
    # candidate that independently reproduces the signed manifest hash.
    candidates: list[tuple[str, bytes]] = []
    for off in (0, 32):
        if off < len(data):
            candidates.append((f"tail-{off}", data[off:]))
            try:
                candidates.append((f"alone-{off}", lzma.decompress(data[off:], format=lzma.FORMAT_ALONE)))
            except lzma.LZMAError:
                pass

    if rel.endswith(".lzma"):
        # Bounded scan for an embedded LZMA-alone header. This is not heuristic
        # acceptance: the output must match unpackedhash exactly.
        stop = min(64, max(0, len(data) - 13))
        for off in range(stop + 1):
            try:
                out = lzma_raw_from_header(data, off)
            except lzma.LZMAError:
                continue
            candidates.append((f"embedded-header-{off}", out))

    if expected_hash == digest(b""):
        candidates.append(("manifest-empty", b""))

    seen: set[str] = set()
    for name, out in candidates:
        h = digest(out)
        if h in seen:
            continue
        seen.add(h)
        if h == expected_hash:
            return out, out_rel, name

    raise RuntimeError(f"no hash-verified unpack transform for {rel}; packed_size={len(data)}")


def collect_entries(doc: object) -> dict[str, tuple[str, str]]:
    rows: list[tuple[str, str, str]] = []

    def walk(v: object) -> None:
        if isinstance(v, dict):
            if all(isinstance(v.get(k), str) and v.get(k) for k in ("url", "packedhash", "unpackedhash")):
                rows.append((str(v["url"]), str(v["packedhash"]).lower(), str(v["unpackedhash"]).lower()))
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)

    walk(doc)
    entries: dict[str, tuple[str, str]] = {}
    for rel, packed, unpacked in rows:
        safe_rel(rel)
        old = entries.get(rel)
        if old and old != (packed, unpacked):
            raise RuntimeError("conflicting manifest entry")
        entries[rel] = (packed, unpacked)
    return entries


def fetch_one(item: tuple[str, tuple[str, str]]) -> tuple[int, int, str]:
    rel, (packed_hash, unpacked_hash) = item
    quoted = urllib.parse.quote(rel, safe="/._-~")
    url = BASE + "/" + quoted
    with tempfile.NamedTemporaryFile(prefix="tibia-packed-", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        cmd = [
            "curl", "--socks5-hostname", SOCKS, "--compressed", "-fL", "--retry", "3",
            "--connect-timeout", "15", "--max-time", "300", "-A", UA, "-e", url,
            "-H", "Accept: */*", "-H", "Accept-Language: en-US,en;q=0.9",
            "-H", "Cache-Control: no-cache", url, "-o", str(tmp),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        packed = tmp.read_bytes()
        if digest(packed) != packed_hash:
            raise RuntimeError(f"packed hash mismatch: {rel}")
        unpacked, out_rel, transform = decode_verified(packed, rel, unpacked_hash)
        p = safe_rel(out_rel)
        target = OUT.joinpath(*p.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(unpacked)
        if p.parts and p.parts[0] == "bin":
            target.chmod(0o755)
        return len(packed), len(unpacked), transform
    finally:
        tmp.unlink(missing_ok=True)


def main() -> None:
    doc = json.loads(MANIFEST.read_text())
    entries = collect_entries(doc)
    if not entries:
        raise SystemExit("manifest has no file entries")
    OUT.mkdir(parents=True, exist_ok=True)
    packed_total = unpacked_total = done = 0
    transforms: dict[str, int] = {}
    items = sorted(entries.items())
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = [ex.submit(fetch_one, item) for item in items]
        try:
            for f in concurrent.futures.as_completed(futures):
                packed, unpacked, transform = f.result()
                packed_total += packed
                unpacked_total += unpacked
                done += 1
                transforms[transform] = transforms.get(transform, 0) + 1
                if done % 100 == 0:
                    print(f"PACKAGE_FILES_RECONSTRUCTED={done}", flush=True)
        except Exception:
            for pending in futures:
                pending.cancel()
            raise
    print(f"PACKAGE_FILES_RECONSTRUCTED={done}")
    print(f"PACKAGE_PACKED_BYTES_VERIFIED={packed_total}")
    print(f"PACKAGE_UNPACKED_BYTES_VERIFIED={unpacked_total}")
    for name, count in sorted(transforms.items()):
        print(f"PACKAGE_TRANSFORM_{name.upper().replace('-', '_')}={count}")


if __name__ == "__main__":
    main()
