#!/usr/bin/env python3
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import lzma
import os
from pathlib import Path, PurePosixPath
import shutil
import subprocess
import tempfile
from typing import Callable, NamedTuple, TypeVar
import urllib.parse

EXPECTED_VERSION = '15.32.75d4a0'
EXPECTED_CLIENT_PACKED_SHA256 = '075810c54af2d6912000eab062763db29563f5a1f4bf1d984154b2d07fd5729f'
EXPECTED_CLIENT_SHA256 = 'd1a16819cec7e40cfee39c099d4868d2eb2d7c1c942078eda105233b5688817a'
EXPECTED_CLIENT_SIZE = 52105824
DEFAULT_FILE_WORKERS = 8
MAX_FILE_WORKERS = 16
CURL = '/usr/bin/curl'

ItemT = TypeVar('ItemT')
ResultT = TypeVar('ResultT')


class PackageFile(NamedTuple):
    local: PurePosixPath
    url: str
    packedhash: str
    unpackedhash: str
    packedsize: int
    unpackedsize: int


def die(message: str) -> None:
    raise SystemExit(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def validate_file_workers(value: int) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not 1 <= value <= MAX_FILE_WORKERS:
        die('FILE_WORKERS_INVALID')
    return value


def run_bounded_downloads(
    items: list[ItemT],
    file_workers: int,
    worker: Callable[[ItemT], ResultT],
) -> list[ResultT]:
    file_workers = validate_file_workers(file_workers)
    with ThreadPoolExecutor(max_workers=file_workers) as executor:
        futures = [executor.submit(worker, item) for item in items]
        try:
            return [future.result() for future in futures]
        except BaseException:
            for future in futures:
                future.cancel()
            raise


def safe_relative(value: str, label: str) -> PurePosixPath:
    if not isinstance(value, str) or not value:
        die(f'{label}_EMPTY')
    path = PurePosixPath(value)
    if path.is_absolute() or '..' in path.parts or '.' in path.parts or any(not p for p in path.parts):
        die(f'{label}_UNSAFE')
    return path


def decode_packed(packed: bytes) -> bytes:
    if len(packed) < 45:
        die('PACKED_FILE_HEADER_TOO_SHORT')
    prop = packed[32]
    if prop >= 9 * 5 * 5:
        die('PACKED_FILE_LZMA_PROPERTY_INVALID')
    lc = prop % 9
    z = prop // 9
    lp = z % 5
    pb = z // 5
    dictionary = int.from_bytes(packed[33:37], 'little')
    if dictionary < 4096:
        die('PACKED_FILE_LZMA_DICTIONARY_INVALID')
    try:
        return lzma.decompress(
            packed[45:],
            format=lzma.FORMAT_RAW,
            filters=[{
                'id': lzma.FILTER_LZMA1,
                'dict_size': dictionary,
                'lc': lc,
                'lp': lp,
                'pb': pb,
            }],
        )
    except lzma.LZMAError as exc:
        die(f'PACKED_FILE_LZMA_DECODE_FAILED:{type(exc).__name__}')


def fetch(url: str, socks_port: int, temp_dir: Path) -> bytes:
    parsed = urllib.parse.urlsplit(url)
    if parsed.scheme != 'https' or not parsed.hostname or parsed.username or parsed.password:
        die('FETCH_URL_NOT_HTTPS')
    if not Path(CURL).is_file() or not os.access(CURL, os.X_OK):
        die('PINNED_CURL_UNAVAILABLE')
    if not temp_dir.is_dir() or temp_dir.is_symlink():
        die('FETCH_TEMP_DIRECTORY_INVALID')

    fd, tmp_name = tempfile.mkstemp(
        prefix='track-a-current-package.',
        suffix='.download',
        dir=str(temp_dir),
    )
    os.close(fd)
    tmp = Path(tmp_name)
    env = os.environ.copy()
    for key in ('RUNNER_TRACKING_ID', 'TIBIA_TEST_EMAIL', 'TIBIA_TEST_PASSWORD'):
        env.pop(key, None)
    try:
        command = [
            CURL,
            '--socks5-hostname', f'127.0.0.1:{socks_port}',
            '--compressed',
            '--fail',
            '--location',
            '--retry', '3',
            '--connect-timeout', '10',
            '--max-time', '180',
            '--proto', '=https',
            '--proto-redir', '=https',
            '--silent',
            '--show-error',
            '--user-agent', 'otclient-track-a-package-materializer/3',
            '--output', str(tmp),
            url,
        ]
        try:
            completed = subprocess.run(
                command,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                env=env,
                timeout=200,
                check=False,
            )
        except (OSError, subprocess.SubprocessError):
            die('FETCH_FAILED:curl_invocation')
        if completed.returncode != 0:
            die(f'FETCH_FAILED:curl_{completed.returncode}')
        return tmp.read_bytes()
    finally:
        tmp.unlink(missing_ok=True)


def checked_int(row: dict, key: str) -> int:
    value = row.get(key)
    if isinstance(value, bool):
        die(f'MANIFEST_{key.upper()}_INVALID')
    try:
        result = int(value)
    except (TypeError, ValueError):
        die(f'MANIFEST_{key.upper()}_INVALID')
    if result < 0:
        die(f'MANIFEST_{key.upper()}_INVALID')
    return result


def checked_hash(row: dict, key: str) -> str:
    value = row.get(key)
    if not isinstance(value, str) or len(value) != 64:
        die(f'MANIFEST_{key.upper()}_INVALID')
    value = value.lower()
    if any(c not in '0123456789abcdef' for c in value):
        die(f'MANIFEST_{key.upper()}_INVALID')
    return value


def parse_manifest_rows(rows: list, base_url: str) -> list[PackageFile]:
    seen: set[str] = set()
    specs: list[PackageFile] = []
    client_rows = 0

    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            die(f'MANIFEST_FILE_ROW_INVALID:{index}')
        local = safe_relative(row.get('localfile'), 'MANIFEST_LOCALFILE')
        local_text = local.as_posix()
        if local_text in seen:
            die('MANIFEST_LOCALFILE_DUPLICATE')
        seen.add(local_text)
        remote = safe_relative(row.get('url'), 'MANIFEST_URL')
        packedhash = checked_hash(row, 'packedhash')
        unpackedhash = checked_hash(row, 'unpackedhash')
        packedsize = checked_int(row, 'packedsize')
        unpackedsize = checked_int(row, 'unpackedsize')

        if local_text == 'bin/client':
            client_rows += 1
            if packedhash != EXPECTED_CLIENT_PACKED_SHA256:
                die('EXACT_CLIENT_PACKED_HASH_FENCE_MOVED')
            if unpackedhash != EXPECTED_CLIENT_SHA256 or unpackedsize != EXPECTED_CLIENT_SIZE:
                die('EXACT_CLIENT_MANIFEST_FENCE_MOVED')

        url = base_url.rstrip('/') + '/' + urllib.parse.quote(remote.as_posix(), safe='/')
        specs.append(PackageFile(
            local=local,
            url=url,
            packedhash=packedhash,
            unpackedhash=unpackedhash,
            packedsize=packedsize,
            unpackedsize=unpackedsize,
        ))

    if client_rows != 1:
        die('EXACT_CLIENT_MANIFEST_ROW_COUNT_INVALID')

    for local_text in seen:
        parts = PurePosixPath(local_text).parts
        for depth in range(1, len(parts)):
            if PurePosixPath(*parts[:depth]).as_posix() in seen:
                die('MANIFEST_LOCALFILE_HIERARCHY_COLLISION')

    return specs


def materialize_file(
    spec: PackageFile,
    socks_port: int,
    staging: Path,
    download_dir: Path,
) -> str:
    local_text = spec.local.as_posix()
    packed = fetch(spec.url, socks_port, download_dir)
    if len(packed) != spec.packedsize:
        die(f'PACKED_FILE_SIZE_MISMATCH:{local_text}')
    if sha256(packed) != spec.packedhash:
        die(f'PACKED_FILE_HASH_MISMATCH:{local_text}')

    if len(packed) == spec.unpackedsize and sha256(packed) == spec.unpackedhash:
        unpacked = packed
    else:
        unpacked = decode_packed(packed)
    if len(unpacked) != spec.unpackedsize:
        die(f'UNPACKED_FILE_SIZE_MISMATCH:{local_text}')
    if sha256(unpacked) != spec.unpackedhash:
        die(f'UNPACKED_FILE_HASH_MISMATCH:{local_text}')

    destination = staging.joinpath(*spec.local.parts)
    destination.parent.mkdir(parents=True, exist_ok=True)
    fd = os.open(destination, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    with os.fdopen(fd, 'wb') as handle:
        handle.write(unpacked)
        handle.flush()
        os.fsync(handle.fileno())
    return local_text


def mark_runtime_executables(staging: Path) -> None:
    bindir = staging / 'bin'
    if not bindir.is_dir() or bindir.is_symlink():
        die('PACKAGE_BIN_DIRECTORY_INVALID')
    for path in bindir.rglob('*'):
        if not path.is_file() or path.is_symlink():
            continue
        with path.open('rb') as handle:
            prefix = handle.read(4)
        if prefix.startswith(b'\x7fELF') or prefix.startswith(b'#!'):
            os.chmod(path, 0o700)


def materialize(
    manifest_url: str,
    base_url: str,
    socks_port: int,
    output: Path,
    file_workers: int = DEFAULT_FILE_WORKERS,
) -> None:
    if output.exists() or output.is_symlink():
        die('OUTPUT_ALREADY_EXISTS')
    if not 1024 <= socks_port <= 65535:
        die('SOCKS_PORT_INVALID')
    file_workers = validate_file_workers(file_workers)
    base = urllib.parse.urlsplit(base_url)
    if base.scheme != 'https' or not base.hostname or base.username or base.password or base.query or base.fragment:
        die('BASE_URL_INVALID')

    output.parent.mkdir(parents=True, exist_ok=True)
    staging: Path | None = Path(tempfile.mkdtemp(prefix=output.name + '.staging.', dir=str(output.parent)))
    download_dir = staging / '.downloads'
    download_dir.mkdir(mode=0o700)
    try:
        manifest_bytes = fetch(manifest_url, socks_port, download_dir)
        try:
            manifest = json.loads(manifest_bytes)
        except (UnicodeDecodeError, json.JSONDecodeError):
            die('MANIFEST_JSON_INVALID')
        if not isinstance(manifest, dict) or manifest.get('version') != EXPECTED_VERSION:
            die('EXACT_CURRENT_VERSION_FENCE_MOVED')
        rows = manifest.get('files')
        if not isinstance(rows, list) or not rows:
            die('MANIFEST_FILES_INVALID')

        specs = parse_manifest_rows(rows, base_url)

        def worker(spec: PackageFile) -> str:
            return materialize_file(spec, socks_port, staging, download_dir)

        verified = run_bounded_downloads(specs, file_workers, worker)
        if verified != [spec.local.as_posix() for spec in specs]:
            die('PACKAGE_FILE_VERIFICATION_ORDER_INVALID')

        shutil.rmtree(download_dir)
        client = staging / 'bin/client'
        if not client.is_file() or client.is_symlink():
            die('EXACT_CLIENT_MISSING_FROM_PACKAGE')
        client_bytes = client.read_bytes()
        if len(client_bytes) != EXPECTED_CLIENT_SIZE:
            die('EXACT_CLIENT_SIZE_FENCE_MOVED')
        if sha256(client_bytes) != EXPECTED_CLIENT_SHA256:
            die('EXACT_CLIENT_HASH_FENCE_MOVED')

        mark_runtime_executables(staging)
        if output.exists() or output.is_symlink():
            die('OUTPUT_COLLISION_DURING_MATERIALIZATION')
        os.rename(staging, output)
        staging = None
    finally:
        if staging is not None and staging.exists():
            shutil.rmtree(staging)

    print(f'TRACK_A_EXACT_CURRENT_PACKAGE_FILE_COUNT={len(specs)}')
    print(f'TRACK_A_EXACT_CURRENT_PACKAGE_FILE_WORKERS={file_workers}')
    print('TRACK_A_EXACT_CURRENT_PACKAGE_ALL_FILES_VERIFIED=true')
    print('TRACK_A_EXACT_CURRENT_PACKAGE_EXECUTED_DOWNLOADED_CONTENT=false')
    print('TRACK_A_EXACT_CURRENT_PACKAGE_MATERIALIZED=true')


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument('--manifest-url', required=True)
    parser.add_argument('--base-url', required=True)
    parser.add_argument('--socks-port', required=True, type=int)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--file-workers', type=int, default=DEFAULT_FILE_WORKERS)
    args = parser.parse_args()
    materialize(
        args.manifest_url,
        args.base_url,
        args.socks_port,
        args.output,
        args.file_workers,
    )


if __name__ == '__main__':
    main()
