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
MATERIALIZER = ROOT / ".github/scripts/track_a_current_client_package_materialize.py"
spec = importlib.util.spec_from_file_location("track_a_current_client_package_materialize", MATERIALIZER)
if spec is None or spec.loader is None:
    raise SystemExit("FIELD6_SEED_RED: materializer import unavailable")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)

if not hasattr(module, "materialize_seed"):
    raise SystemExit("FIELD6_SEED_RED: materialize_seed missing")

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

client = b"\x7fELF-seed-client"
package_data = b"verified-package-data"
asset_data = b"verified-asset-data"
module.EXPECTED_VERSION = "fixture-version"
module.EXPECTED_CLIENT_SIZE = len(client)
module.EXPECTED_CLIENT_SHA256 = digest(client)
module.EXPECTED_CLIENT_PACKED_SHA256 = digest(b"packed-client-fixture")
package_manifest = {
    "version": module.EXPECTED_VERSION,
    "files": [
        {
            "localfile": "bin/client",
            "url": "bin/client.lzma",
            "packedhash": module.EXPECTED_CLIENT_PACKED_SHA256,
            "packedsize": 123,
            "unpackedhash": digest(client),
            "unpackedsize": len(client),
        },
        {
            "localfile": "share/data.bin",
            "url": "share/data.bin.lzma",
            "packedhash": digest(b"packed-data"),
            "packedsize": 44,
            "unpackedhash": digest(package_data),
            "unpackedsize": len(package_data),
        },
    ],
}
assets_manifest = {
    "files": [{
        "localfile": "assets/a.dat",
        "url": "assets/a.dat.lzma",
        "packedhash": digest(b"packed-asset"),
        "packedsize": 55,
        "unpackedhash": digest(asset_data),
        "unpackedsize": len(asset_data),
    }]
}
