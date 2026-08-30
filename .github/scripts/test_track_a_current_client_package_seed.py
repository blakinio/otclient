#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import io
import json
import os
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

for name in (
    "EXPECTED_SEED_SHA256", "EXPECTED_SEED_SIZE", "EXPECTED_PACKAGE_ROWS",
    "EXPECTED_ASSET_ROWS", "EXPECTED_REGULAR_FILES", "materialize_seed",
):
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
assets_bytes = json.dumps(assets_manifest).encode()


def write_valid_seed(path: Path, *, package_bytes: bytes = package_data, extra: bool = False) -> None:
    with tarfile.open(path, "w:gz") as tar:
        add_file(tar, "./package.json", json.dumps(package_manifest).encode())
        add_file(tar, "./package.json.version", b"fixture-version\n")
        add_file(tar, "./assets.json", assets_bytes)
        add_file(tar, "./assets.json.sha256", (digest(assets_bytes) + "\n").encode())
        add_file(tar, "./bin/client", client, 0o700)
        add_file(tar, "./share/data.bin", package_bytes)
        add_file(tar, "./assets/a.dat", asset_data)
        if extra:
            add_file(tar, "./unexpected.bin", b"unexpected")


def bind_fixture(seed: Path) -> None:
    module.EXPECTED_SEED_SIZE = seed.stat().st_size
    module.EXPECTED_SEED_SHA256 = digest(seed.read_bytes())
    module.EXPECTED_VERSION = "fixture-version"
    module.EXPECTED_CLIENT_SIZE = len(client)
    module.EXPECTED_CLIENT_SHA256 = digest(client)
    module.EXPECTED_PACKAGE_ROWS = 2
    module.EXPECTED_ASSET_ROWS = 1
    module.EXPECTED_REGULAR_FILES = 7


def expect_failure(seed: Path, output: Path, marker: str) -> None:
    bind_fixture(seed)
    try:
        module.materialize_seed(seed, output, expected_uid=os.getuid())
    except SystemExit as exc:
        if marker not in str(exc):
            raise
    else:
        raise SystemExit(f"FIELD6_SEED_RED: expected {marker}")


with tempfile.TemporaryDirectory(prefix="field6-seed-contract.") as root_text:
    root = Path(root_text)
    seed = root / "seed.tar.gz"
    write_valid_seed(seed)
    bind_fixture(seed)
    output = root / "out"
    module.materialize_seed(seed, output, expected_uid=os.getuid())
    if (output / "bin/client").read_bytes() != client:
        raise SystemExit("FIELD6_SEED_RED: client mismatch")
    if (output / "share/data.bin").read_bytes() != package_data:
        raise SystemExit("FIELD6_SEED_RED: package file mismatch")
    if (output / "assets/a.dat").read_bytes() != asset_data:
        raise SystemExit("FIELD6_SEED_RED: asset mismatch")
    if not (output / "bin/client").stat().st_mode & 0o100:
        raise SystemExit("FIELD6_SEED_RED: client not executable")

    symlink_seed = root / "symlink.tar.gz"
    with tarfile.open(symlink_seed, "w:gz") as tar:
        info = tarfile.TarInfo("./escape")
        info.type = tarfile.SYMTYPE
        info.linkname = "/tmp/escape"
        tar.addfile(info)
    expect_failure(symlink_seed, root / "symlink-out", "SEED_MEMBER_TYPE_INVALID")

    traversal_seed = root / "traversal.tar.gz"
    with tarfile.open(traversal_seed, "w:gz") as tar:
        add_file(tar, "../escape", b"bad")
    expect_failure(traversal_seed, root / "traversal-out", "SEED_MEMBER_PATH_INVALID")

    duplicate_seed = root / "duplicate.tar.gz"
    with tarfile.open(duplicate_seed, "w:gz") as tar:
        add_file(tar, "./package.json", b"{}")
        add_file(tar, "package.json", b"{}")
    expect_failure(duplicate_seed, root / "duplicate-out", "SEED_MEMBER_DUPLICATE")

    tampered_seed = root / "tampered.tar.gz"
    write_valid_seed(tampered_seed, package_bytes=b"tampered")
    expect_failure(tampered_seed, root / "tampered-out", "SEED_MANIFEST_LOCALFILE_SIZE_MISMATCH")

    extra_seed = root / "extra.tar.gz"
    write_valid_seed(extra_seed, extra=True)
    expect_failure(extra_seed, root / "extra-out", "SEED_REGULAR_FILE_COUNT_MISMATCH")

print("TRACK_A_CURRENT_CLIENT_PACKAGE_SEED_CONTRACT=PASS")
