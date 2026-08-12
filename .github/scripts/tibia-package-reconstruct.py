#!/usr/bin/env python3
"""Ephemerally reconstruct official Tibia package/assets from CipSoft manifests.

Package entries are accepted only when both packedhash and unpackedhash verify.
The official assets-current manifest omits unpackedhash for most entries; that
mode must be opted into explicitly and still requires every downloaded packed
object to match its manifest packedhash before deterministic decoding.
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
import time
import urllib.parse

MANIFEST = Path(os.environ.get("TIBIA_MANIFEST", "/tmp/tibia-package/package.json"))
OUT = Path(os.environ.get("TIBIA_PACKAGE_OUT", "/tmp/tibia-package/runtime"))
BASE = os.environ["TIBIA_BASE_URL"].rstrip("/")
SOCKS = os.environ.get("TIBIA_SOCKS", "127.0.0.1:25344")
WORKERS = int(os.environ.get("TIBIA_DOWNLOAD_WORKERS", "6"))
ALLOW_MISSING_UNPACKED = os.environ.get("TIBIA_ALLOW_MISSING_UNPACKED_HASH", "0") == "1"
UA = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36"


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_rel(rel: str) -> PurePosixPath:
    p = PurePosixPath(rel)
    if p.is_absolute() or not p.parts or ".." in p.parts:
        raise RuntimeError("unsafe manifest path")
    return p


def lzma_filter_from_header(data: bytes, header_off: int) -> dict[str, int]:
    if len(data) < header_off + 13:
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
    return {"id": lzma.FILTER_LZMA1, "dict_size": dict_size, "lc": lc, "lp": lp, "pb": pb}


def lzma_raw_from_header(data: bytes, header_off: int, require_eof: bool = True) -> bytes:
    filt = lzma_filter_from_header(data, header_off)
    payload = data[header_off + 13 :]
    if require_eof:
        return lzma.decompress(payload, format=lzma.FORMAT_RAW, filters=[filt])
    dec = lzma.LZMADecompressor(format=lzma.FORMAT_RAW, filters=[filt])
    return dec.decompress(payload)


def decode_object(data: bytes, rel: str, expected_hash: str | None) -> tuple[bytes, str, str]:
    """Return (unpacked bytes, output relative path, transform name)."""
    out_rel = rel[:-5] if rel.endswith(".lzma") else rel

    if expected_hash:
        if digest(data) == expected_hash:
            return data, out_rel, "identity"

        if rel.endswith(".lzma") and len(data) >= 45:
            try:
                out = lzma_raw_from_header(data, 32)
                if digest(out) == expected_hash:
                    return out, out_rel, "cipsoft-envelope"
            except lzma.LZMAError:
                pass

        candidates: list[tuple[str, bytes]] = []
        for off in (0, 32):
            if off < len(data):
                candidates.append((f"tail-{off}", data[off:]))
                try:
                    candidates.append((f"alone-{off}", lzma.decompress(data[off:], format=lzma.FORMAT_ALONE)))
                except lzma.LZMAError:
                    pass

        if rel.endswith(".lzma"):
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

    # assets-current packed-hash-only mode: packed bytes were already verified.
    if not ALLOW_MISSING_UNPACKED:
        raise RuntimeError(f"unpackedhash missing outside explicit assets mode: {rel}")
    if not rel.endswith(".lzma"):
        return data, out_rel, "packedhash-identity"
    if len(data) < 45:
        raise RuntimeError(f"short CipSoft asset envelope: {rel}; packed_size={len(data)}")
    try:
        out = lzma_raw_from_header(data, 32, require_eof=False)
    except lzma.LZMAError as exc:
        raise RuntimeError(f"CipSoft asset decode failed: {rel}") from exc
    return out, out_rel, "packedhash-cipsoft-envelope"


def collect_entries(doc: object) -> dict[str, tuple[str, str | None]]:
    rows: list[tuple[str, str, str | None]] = []

    def walk(v: object) -> None:
        if isinstance(v, dict):
            url = v.get("url")
            packed = v.get("packedhash")
            unpacked = v.get("unpackedhash")
            if isinstance(url, str) and url and isinstance(packed, str) and packed:
                if isinstance(unpacked, str) and unpacked:
                    rows.append((url, packed.lower(), unpacked.lower()))
                elif ALLOW_MISSING_UNPACKED:
                    rows.append((url, packed.lower(), None))
            for x in v.values():
                walk(x)
        elif isinstance(v, list):
            for x in v:
                walk(x)

    walk(doc)
    entries: dict[str, tuple[str, str | None]] = {}
    for rel, packed, unpacked in rows:
        safe_rel(rel)
        old = entries.get(rel)
        if old and old != (packed, unpacked):
            raise RuntimeError("conflicting manifest entry")
        entries[rel] = (packed, unpacked)
    return entries


def fetch_one(item: tuple[str, tuple[str, str | None]]) -> tuple[int, int, str, bool]:
    rel, (packed_hash, unpacked_hash) = item
    quoted = urllib.parse.quote(rel, safe="/._-~")
    url = BASE + "/" + quoted
    with tempfile.NamedTemporaryFile(prefix="tibia-packed-", delete=False) as tf:
        tmp = Path(tf.name)
    try:
        cmd = [
            "curl", "--socks5-hostname", SOCKS, "--http1.1", "--compressed", "-fL",
            "--retry", "4", "--retry-all-errors", "--retry-delay", "1",
            "--connect-timeout", "20", "--max-time", "300", "-A", UA, "-e", url,
            "-H", "Accept: */*", "-H", "Accept-Language: en-US,en;q=0.9",
            "-H", "Cache-Control: no-cache", url, "-o", str(tmp),
        ]
        last_error: subprocess.CalledProcessError | None = None
        for attempt in range(1, 7):
            tmp.write_bytes(b"")
            try:
                subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                last_error = None
                break
            except subprocess.CalledProcessError as exc:
                last_error = exc
                if attempt == 6:
                    break
                time.sleep(min(2 ** attempt, 12))
        if last_error is not None:
            raise RuntimeError(f"download failed after bounded retries: {rel}") from last_error

        packed = tmp.read_bytes()
        if digest(packed) != packed_hash:
            raise RuntimeError(f"packed hash mismatch: {rel}")
        unpacked, out_rel, transform = decode_object(packed, rel, unpacked_hash)
        p = safe_rel(out_rel)
        target = OUT.joinpath(*p.parts)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(unpacked)
        if p.parts and p.parts[0] == "bin":
            target.chmod(0o755)
        return len(packed), len(unpacked), transform, unpacked_hash is not None
    finally:
        tmp.unlink(missing_ok=True)


def main() -> None:
    doc = json.loads(MANIFEST.read_text())
    entries = collect_entries(doc)
    if not entries:
        raise SystemExit("manifest has no file entries")
    OUT.mkdir(parents=True, exist_ok=True)
    packed_total = unpacked_total = done = unpacked_hash_count = 0
    transforms: dict[str, int] = {}
    items = sorted(entries.items())
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        futures = [ex.submit(fetch_one, item) for item in items]
        try:
            for f in concurrent.futures.as_completed(futures):
                packed, unpacked, transform, had_unpacked_hash = f.result()
                packed_total += packed
                unpacked_total += unpacked
                done += 1
                unpacked_hash_count += int(had_unpacked_hash)
                transforms[transform] = transforms.get(transform, 0) + 1
                if done % 100 == 0:
                    print(f"PACKAGE_FILES_RECONSTRUCTED={done}", flush=True)
        except Exception:
            for pending in futures:
                pending.cancel()
            raise
    print(f"PACKAGE_FILES_RECONSTRUCTED={done}")
    print(f"PACKAGE_PACKED_BYTES_VERIFIED={packed_total}")
    print(f"PACKAGE_UNPACKED_BYTES_WRITTEN={unpacked_total}")
    print(f"PACKAGE_UNPACKED_HASH_VERIFIED_COUNT={unpacked_hash_count}")
    print(f"PACKAGE_PACKED_HASH_ONLY_COUNT={done-unpacked_hash_count}")
    for name, count in sorted(transforms.items()):
        print(f"PACKAGE_TRANSFORM_{name.upper().replace('-', '_')}={count}")


if __name__ == "__main__":
    main()
