#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import lzma
import os
from pathlib import Path
import re
import tempfile
import threading
import time

ROOT = Path(__file__).resolve().parents[2]
MATERIALIZER = ROOT / ".github/scripts/track_a_current_client_package_materialize.py"
ACQUIRE = ROOT / ".github/scripts/track_a_current_client_package_acquire.sh"
LIVE_WORKFLOW = ROOT / ".github/workflows/track-a-current-login-field6-runtime.yml"
CONTRACT_WORKFLOW = ROOT / ".github/workflows/track-a-current-client-package-materializer.yml"

spec = importlib.util.spec_from_file_location("track_a_current_client_package_materialize", MATERIALIZER)
if spec is None or spec.loader is None:
    raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: materializer import unavailable")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

for name in ("DEFAULT_FILE_WORKERS", "MAX_FILE_WORKERS", "validate_file_workers", "run_bounded_downloads"):
    if not hasattr(module, name):
        raise SystemExit(f"FIELD6_MATERIALIZER_CONTRACT_RED: missing {name}")

# Production acquisition is deliberately serial. V3 proved serial access continued
# without an HTTP error until the old 18-minute job timeout, while terminal V4
# failed almost immediately after the production wrapper moved to eight workers.
# Keep the bounded-concurrency primitive for fixtures/tools, but fail closed unless
# production/default behavior is one request stream and the live job has time to
# finish that verified serial materialization.
if module.DEFAULT_FILE_WORKERS != 1:
    raise SystemExit("FIELD6_MATERIALIZER_CDN_THROTTLE_RED: DEFAULT_FILE_WORKERS must be 1")
if module.MAX_FILE_WORKERS != 16:
    raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: MAX_FILE_WORKERS must be 16")
if module.validate_file_workers(1) != 1 or module.validate_file_workers(16) != 16:
    raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: valid worker bounds rejected")
for invalid in (0, 17):
    try:
        module.validate_file_workers(invalid)
    except SystemExit:
        pass
    else:
        raise SystemExit(f"FIELD6_MATERIALIZER_CONTRACT_RED: invalid worker count accepted: {invalid}")

items = list(range(12))
active = 0
max_active = 0
lock = threading.Lock()


def worker(item: int) -> int:
    global active, max_active
    with lock:
        active += 1
        max_active = max(max_active, active)
    try:
        time.sleep(0.08)
        return item * 3
    finally:
        with lock:
            active -= 1


started = time.monotonic()
result = module.run_bounded_downloads(items, 4, worker)
elapsed = time.monotonic() - started

if result != [item * 3 for item in items]:
    raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: manifest result order was not preserved")
if not 2 <= max_active <= 4:
    raise SystemExit(f"FIELD6_MATERIALIZER_CONTRACT_RED: observed max_active={max_active}, expected 2..4")
if elapsed >= 0.65:
    raise SystemExit(f"FIELD6_MATERIALIZER_CONTRACT_RED: elapsed={elapsed:.3f}s proves bounded helper is serial or stalled")

source = MATERIALIZER.read_text(encoding="utf-8")
for needle in (
    "ThreadPoolExecutor",
    "max_workers=file_workers",
    "future.result()",
    "--file-workers",
    "PACKED_FILE_HASH_MISMATCH",
    "UNPACKED_FILE_HASH_MISMATCH",
    "EXACT_CLIENT_HASH_FENCE_MOVED",
):
    if needle not in source:
        raise SystemExit(f"FIELD6_MATERIALIZER_CONTRACT_RED: source missing {needle!r}")

acquire_source = ACQUIRE.read_text(encoding="utf-8")
for needle in ("FILE_WORKERS='1'", '--file-workers "$FILE_WORKERS"'):
    if needle not in acquire_source:
        raise SystemExit(f"FIELD6_MATERIALIZER_CDN_THROTTLE_RED: acquisition wrapper missing {needle!r}")

live_workflow_source = LIVE_WORKFLOW.read_text(encoding="utf-8")
match = re.search(r"(?ms)^  live-observation:\n.*?^    timeout-minutes:\s*(\d+)\s*$", live_workflow_source)
if match is None:
    raise SystemExit("FIELD6_MATERIALIZER_CDN_THROTTLE_RED: live-observation timeout not found")
if int(match.group(1)) != 45:
    raise SystemExit(
        f"FIELD6_MATERIALIZER_CDN_THROTTLE_RED: live-observation timeout must be 45, got {match.group(1)}"
    )

contract_workflow_source = CONTRACT_WORKFLOW.read_text(encoding="utf-8")
if "      - .github/workflows/track-a-current-login-field6-runtime.yml" not in contract_workflow_source:
    raise SystemExit(
        "FIELD6_MATERIALIZER_CDN_THROTTLE_RED: materializer contract must watch live field6 workflow"
    )


def digest(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def pack_lzma(payload: bytes) -> bytes:
    dictionary = 4096
    lc, lp, pb = 3, 0, 2
    prop = (pb * 5 + lp) * 9 + lc
    encoded = lzma.compress(
        payload,
        format=lzma.FORMAT_RAW,
        filters=[{
            "id": lzma.FILTER_LZMA1,
            "dict_size": dictionary,
            "lc": lc,
            "lp": lp,
            "pb": pb,
        }],
    )
    return bytes(32) + bytes([prop]) + dictionary.to_bytes(4, "little") + bytes(8) + encoded


client_payload = b"\x7fELF-fixture-client"
data_payload = b"verified-package-data" * 32
data_packed = pack_lzma(data_payload)
manifest_url = "https://fixture.invalid/package.json"
base_url = "https://fixture.invalid/package"
module.EXPECTED_VERSION = "fixture-version"
module.EXPECTED_CLIENT_SIZE = len(client_payload)
module.EXPECTED_CLIENT_SHA256 = digest(client_payload)
module.EXPECTED_CLIENT_PACKED_SHA256 = digest(client_payload)
manifest = {
    "version": module.EXPECTED_VERSION,
    "files": [
        {
            "localfile": "bin/client",
            "url": "bin/client.packed",
            "packedhash": digest(client_payload),
            "unpackedhash": digest(client_payload),
            "packedsize": len(client_payload),
            "unpackedsize": len(client_payload),
        },
        {
            "localfile": "share/data.bin",
            "url": "share/data.bin.packed",
            "packedhash": digest(data_packed),
            "unpackedhash": digest(data_payload),
            "packedsize": len(data_packed),
            "unpackedsize": len(data_payload),
        },
    ],
}
payloads = {
    manifest_url: json.dumps(manifest).encode("utf-8"),
    f"{base_url}/bin/client.packed": client_payload,
    f"{base_url}/share/data.bin.packed": data_packed,
}
fetch_lock = threading.Lock()
fetch_active = 0
fetch_max_active = 0


def fake_fetch(url: str, socks_port: int, temp_dir: Path) -> bytes:
    global fetch_active, fetch_max_active
    if socks_port != 25442 or not temp_dir.is_dir() or temp_dir.is_symlink():
        raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: fixture escaped task-owned fetch boundary")
    with fetch_lock:
        fetch_active += 1
        fetch_max_active = max(fetch_max_active, fetch_active)
    try:
        if url != manifest_url:
            time.sleep(0.05)
        return payloads[url]
    finally:
        with fetch_lock:
            fetch_active -= 1


module.fetch = fake_fetch
with tempfile.TemporaryDirectory(prefix="field6-materializer-contract.") as temp_root:
    root = Path(temp_root)
    output = root / "current-package"
    module.materialize(manifest_url, base_url, 25442, output, 2)
    if (output / "bin/client").read_bytes() != client_payload:
        raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: exact-client fixture was not preserved")
    if (output / "share/data.bin").read_bytes() != data_payload:
        raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: unpacked fixture was not verified")
    if not os.stat(output / "bin/client").st_mode & 0o100:
        raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: verified client was not made owner-executable")
    if (output / ".downloads").exists() or list(root.glob("current-package.staging.*")):
        raise SystemExit("FIELD6_MATERIALIZER_CONTRACT_RED: task-owned temporary state was retained")

if fetch_max_active != 2:
    raise SystemExit(
        f"FIELD6_MATERIALIZER_CONTRACT_RED: full fixture materializer observed fetch_max_active={fetch_max_active}, expected 2"
    )

print("TRACK_A_CURRENT_CLIENT_PACKAGE_MATERIALIZER_CONTRACT=PASS")
