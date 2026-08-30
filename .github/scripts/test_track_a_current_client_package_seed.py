#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
from pathlib import Path
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SEED_IMPORTER = ROOT / ".github/scripts/track_a_current_client_package_seed.py"

spec = importlib.util.spec_from_file_location("track_a_current_client_package_seed", SEED_IMPORTER)
if spec is None or spec.loader is None:
    raise SystemExit("FIELD6_SEED_RED: seed importer unavailable")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for name in ("EXPECTED_SEED_SHA256", "EXPECTED_SEED_SIZE", "materialize_seed"):
    if not hasattr(module, name):
        raise SystemExit(f"FIELD6_SEED_RED: missing {name}")


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def add_file(tar: tarfile.TarFile, name: str, data: bytes, mode: int = 0o600) -> None:
    info = tarfile.TarInfo(name)
    info.size = len(data)
    info.mode = mode
    tar.addfile(info, io.BytesIO(data))


client = b"\x7fELF-seed-client"
package_data = b"verified-package-data"
asset_data = b"verified-asset-data"
package_manifest = {
    "version": "fixture-version",
    "files": [
        {
            "localfile": "bin/client",
            "url": "bin/client.lzma",
            "packedhash": digest(b"packed-client"),
            "packedsize": 111,
            "unpackedhash": digest(client),
            "unpackedsize": len(client),
            "executable": True,
        },
        {
            "localfile": "share/data.bin",
            "url": "share/data.bin.lzma",
            "packedhash": digest(b"packed-data"),
            "packedsize": 222,
            "unpackedhash": digest(package_data),
            "unpackedsize": len(package_data),
        },
    ],
}
assets_manifest = {
    "files": [
        {
            "localfile": "assets/a.dat",
            "url": "assets/a.dat.lzma",
            "packedhash": digest(b"packed-asset"),
            "packedsize": 333,
            "unpackedhash": digest(asset_data),
            "unpackedsize": len(asset_data),
        }
    ]
}

with tempfile.TemporaryDirectory(prefix="field6-seed-contract.") as root_text:
    root = Path(root_text)
    seed = root / "seed.tar.gz"
    with tarfile.open(seed, "w:gz") as tar:
        add_file(tar, "./package.json", json.dumps(package_manifest).encode())
        add_file(tar, "./package.json.version", b"fixture-version\n")
        assets_bytes = json.dumps(assets_manifest).encode()
        add_file(tar, "./assets.json", assets_bytes)
        add_file(tar, "./assets.json.sha256", (digest(assets_bytes) + "\n").encode())
        add_file(tar, "./bin/client", client, 0o700)
        add_file(tar, "./share/data.bin", package_data)
        add_file(tar, "./assets/a.dat", asset_data)

    module.EXPECTED_SEED_SIZE = seed.stat().st_size
    module.EXPECTED_SEED_SHA256 = digest(seed.read_bytes())
    module.EXPECTED_VERSION = "fixture-version"
    module.EXPECTED_CLIENT_SIZE = len(client)
    module.EXPECTED_CLIENT_SHA256 = digest(client)
    output = root / "out"
    module.materialize_seed(seed, output)
    if (output / "bin/client").read_bytes() != client:
        raise SystemExit("FIELD6_SEED_RED: client mismatch")
    if (output / "share/data.bin").read_bytes() != package_data:
        raise SystemExit("FIELD6_SEED_RED: package file mismatch")
    if (output / "assets/a.dat").read_bytes() != asset_data:
        raise SystemExit("FIELD6_SEED_RED: asset mismatch")
    if not (output / "bin/client").stat().st_mode & 0o100:
        raise SystemExit("FIELD6_SEED_RED: client not executable")

    bad_seed = root / "bad.tar.gz"
    with tarfile.open(bad_seed, "w:gz") as tar:
        info = tarfile.TarInfo("./escape")
        info.type = tarfile.SYMTYPE
        info.linkname = "/tmp/escape"
        tar.addfile(info)
    module.EXPECTED_SEED_SIZE = bad_seed.stat().st_size
    module.EXPECTED_SEED_SHA256 = digest(bad_seed.read_bytes())
    try:
        module.materialize_seed(bad_seed, root / "bad-out")
    except SystemExit as exc:
        if "SEED_MEMBER_TYPE_INVALID" not in str(exc):
            raise
    else:
        raise SystemExit("FIELD6_SEED_RED: unsafe symlink seed accepted")

print("TRACK_A_CURRENT_CLIENT_PACKAGE_SEED_CONTRACT=PASS")
