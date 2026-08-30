#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import stat
import tarfile
import tempfile

EXPECTED_SEED_SIZE = 412272538
EXPECTED_SEED_SHA256 = "64031ba091884c5b1be71416394b8ada6dac9529cfed60e7b4856c04b7e5b016"
EXPECTED_VERSION = "15.32.75d4a0"
EXPECTED_CLIENT_SIZE = 52105824
EXPECTED_CLIENT_SHA256 = "d1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a"
EXPECTED_PACKAGE_ROWS = 1634
EXPECTED_ASSET_ROWS = 7094
EXPECTED_REGULAR_FILES = 8732
META_FILES = {"package.json", "package.json.version", "assets.json", "assets.json.sha256"}
SHA256_RE = re.compile(r"[0-9a-f]{64}")


def fail(code: str) -> None:
    raise SystemExit(code)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def normalize_path(raw: str, *, allow_root: bool = False) -> str | None:
    if not isinstance(raw, str) or not raw or "\x00" in raw or "\\" in raw:
        fail("SEED_MEMBER_PATH_INVALID")
    while raw.startswith("./"):
        raw = raw[2:]
    if raw in ("", "."):
        if allow_root:
            return None
        fail("SEED_MEMBER_PATH_INVALID")
    if raw.startswith("/"):
        fail("SEED_MEMBER_PATH_INVALID")
    path = PurePosixPath(raw)
    if path.is_absolute() or any(part in ("", ".", "..") for part in path.parts):
        fail("SEED_MEMBER_PATH_INVALID")
    normalized = path.as_posix()
    if normalized.startswith("../") or "/../" in normalized:
        fail("SEED_MEMBER_PATH_INVALID")
    return normalized


def verify_seed_container(seed: Path, *, expected_uid: int | None = None) -> None:
    try:
        info = seed.lstat()
    except FileNotFoundError:
        fail("SEED_ARCHIVE_MISSING")
    if not stat.S_ISREG(info.st_mode) or seed.is_symlink():
        fail("SEED_ARCHIVE_NOT_REGULAR")
    if expected_uid is not None and info.st_uid != expected_uid:
        fail("SEED_ARCHIVE_OWNER_INVALID")
    if info.st_mode & 0o022:
        fail("SEED_ARCHIVE_WRITABLE_BY_NONOWNER")
    if info.st_size != EXPECTED_SEED_SIZE:
        fail("SEED_ARCHIVE_SIZE_MISMATCH")
    if sha256_file(seed) != EXPECTED_SEED_SHA256:
        fail("SEED_ARCHIVE_SHA256_MISMATCH")


def load_json(path: Path, code: str) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        fail(code)
    if not isinstance(value, dict):
        fail(code)
    return value


def manifest_rows(value: dict, expected_count: int, code: str) -> list[dict]:
    rows = value.get("files")
    if not isinstance(rows, list) or len(rows) != expected_count:
        fail(code)
    if not all(isinstance(row, dict) for row in rows):
        fail(code)
    return rows


def expected_row_digest(row: dict) -> tuple[str, int]:
    if row.get("unpack") is False:
        digest = row.get("packedhash")
        size = row.get("packedsize")
    else:
        digest = row.get("unpackedhash")
        size = row.get("unpackedsize")
    if not isinstance(digest, str) or not SHA256_RE.fullmatch(digest):
        fail("SEED_MANIFEST_HASH_INVALID")
    if not isinstance(size, int) or isinstance(size, bool) or size < 0:
        fail("SEED_MANIFEST_SIZE_INVALID")
    return digest, size


def verify_installed_tree(root: Path, regular_paths: set[str]) -> None:
    package = load_json(root / "package.json", "SEED_PACKAGE_MANIFEST_INVALID")
    assets = load_json(root / "assets.json", "SEED_ASSET_MANIFEST_INVALID")
    if package.get("version") != EXPECTED_VERSION:
        fail("SEED_PACKAGE_VERSION_MISMATCH")
    try:
        version_text = (root / "package.json.version").read_text(encoding="utf-8").strip()
        asset_sha_text = (root / "assets.json.sha256").read_text(encoding="ascii").strip()
    except (OSError, UnicodeDecodeError):
        fail("SEED_METADATA_INVALID")
    if version_text != EXPECTED_VERSION:
        fail("SEED_PACKAGE_VERSION_FILE_MISMATCH")
    if not SHA256_RE.fullmatch(asset_sha_text):
        fail("SEED_ASSET_SHA_FILE_INVALID")
    if sha256_file(root / "assets.json") != asset_sha_text:
        fail("SEED_ASSET_MANIFEST_SHA_MISMATCH")

    package_rows = manifest_rows(package, EXPECTED_PACKAGE_ROWS, "SEED_PACKAGE_ROW_COUNT_MISMATCH")
    asset_rows = manifest_rows(assets, EXPECTED_ASSET_ROWS, "SEED_ASSET_ROW_COUNT_MISMATCH")
    rows = package_rows + asset_rows
    expected_paths = set(META_FILES)
    executable_paths: set[str] = set()
    for row in rows:
        local = normalize_path(row.get("localfile"))
        assert local is not None
        if local in expected_paths:
            fail("SEED_MANIFEST_LOCALFILE_DUPLICATE")
        expected_paths.add(local)
        if row.get("executable") is True:
            executable_paths.add(local)
        digest, size = expected_row_digest(row)
        path = root / local
        try:
            info = path.lstat()
        except FileNotFoundError:
            fail("SEED_MANIFEST_LOCALFILE_MISSING")
        if not stat.S_ISREG(info.st_mode) or path.is_symlink():
            fail("SEED_MANIFEST_LOCALFILE_NOT_REGULAR")
        if info.st_size != size:
            fail("SEED_MANIFEST_LOCALFILE_SIZE_MISMATCH")
        if sha256_file(path) != digest:
            fail("SEED_MANIFEST_LOCALFILE_SHA256_MISMATCH")

    if len(regular_paths) != EXPECTED_REGULAR_FILES:
        fail("SEED_REGULAR_FILE_COUNT_MISMATCH")
    if regular_paths != expected_paths:
        fail("SEED_EXACT_FILE_SET_MISMATCH")

    client = root / "bin/client"
    try:
        client_info = client.lstat()
    except FileNotFoundError:
        fail("SEED_CLIENT_MISSING")
    if not stat.S_ISREG(client_info.st_mode) or client.is_symlink():
        fail("SEED_CLIENT_NOT_REGULAR")
    if client_info.st_size != EXPECTED_CLIENT_SIZE:
        fail("SEED_CLIENT_SIZE_MISMATCH")
    if sha256_file(client) != EXPECTED_CLIENT_SHA256:
        fail("SEED_CLIENT_SHA256_MISMATCH")
    executable_paths.add("bin/client")

    for path_text in regular_paths:
        os.chmod(root / path_text, 0o755 if path_text in executable_paths else 0o644)
    for directory in sorted((path for path in root.rglob("*") if path.is_dir()), key=lambda p: len(p.parts), reverse=True):
        os.chmod(directory, 0o755)
    os.chmod(root, 0o755)


def materialize_seed(seed: Path, output: Path, *, expected_uid: int | None = None) -> None:
    seed = Path(seed)
    output = Path(output)
    verify_seed_container(seed, expected_uid=expected_uid)
    if output.exists() or output.is_symlink():
        fail("SEED_OUTPUT_COLLISION")
    output.parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=f".{output.name}.seed-", dir=output.parent))
    regular_paths: set[str] = set()
    seen: set[str] = set()
    try:
        try:
            archive = tarfile.open(seed, "r:gz")
        except (OSError, tarfile.TarError):
            fail("SEED_ARCHIVE_FORMAT_INVALID")
        with archive:
            for member in archive:
                normalized = normalize_path(member.name, allow_root=True)
                if normalized is None:
                    if not member.isdir():
                        fail("SEED_MEMBER_TYPE_INVALID")
                    continue
                if normalized in seen:
                    fail("SEED_MEMBER_DUPLICATE")
                seen.add(normalized)
                target = staging / normalized
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    os.chmod(target, 0o755)
                    continue
                if not member.isfile():
                    fail("SEED_MEMBER_TYPE_INVALID")
                target.parent.mkdir(parents=True, exist_ok=True)
                source = archive.extractfile(member)
                if source is None:
                    fail("SEED_MEMBER_READ_FAILED")
                with source, target.open("xb") as handle:
                    shutil.copyfileobj(source, handle, length=1024 * 1024)
                os.chmod(target, 0o600)
                regular_paths.add(normalized)
        verify_installed_tree(staging, regular_paths)
        os.replace(staging, output)
        print(f"TRACK_A_FIELD6_SEED_REGULAR_FILES={len(regular_paths)}")
        print("TRACK_A_FIELD6_SEED_ALL_FILES_VERIFIED=true")
        print("TRACK_A_FIELD6_SEED_MATERIALIZED=true")
    finally:
        if staging.exists():
            shutil.rmtree(staging)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("seed", type=Path)
    parser.add_argument("output", type=Path)
    parser.add_argument("--require-root-owner", action="store_true")
    args = parser.parse_args()
    materialize_seed(args.seed, args.output, expected_uid=0 if args.require_root_owner else None)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
