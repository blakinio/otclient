from __future__ import annotations

import json
import re
from typing import Callable

from .runtime import EXPECTED_CLIENT_SHA256, EXPECTED_CLIENT_SIZE, EXPECTED_TARGET_CONTAINER
from .typed_presence import (
    READ_ONLY_PRESENCE_PROBE,
    STATIC_LAYOUT_PROBE,
    TypedPresenceLayout,
    TypedPresenceResolverError,
)


def _build_diagnostic_probe() -> str:
    probe = READ_ONLY_PRESENCE_PROBE
    replacements = (
        (
            'pat=struct.pack("<Q",expected_vptr); hits=[]',
            'pat=struct.pack("<Q",expected_vptr); raw_hits=[]; hits=[]',
        ),
        (
            '    if obj%8==0:\n     try: qprivate=struct.unpack("<Q",os.pread(fd,8,obj+8))[0]',
            '    if obj%8==0:\n     raw_hits.append(obj)\n     try: qprivate=struct.unpack("<Q",os.pread(fd,8,obj+8))[0]',
        ),
        (
            ' hits=sorted(set(hits))\n if len(hits)!=1: raise SystemExit("TYPED_OBJECT_COUNT="+str(len(hits)))',
            ' raw_hits=sorted(set(raw_hits)); hits=sorted(set(hits))\n if len(hits)!=1: raise SystemExit("TYPED_OBJECT_COUNT="+str(len(hits))+" RAW_VPTR_COUNT="+str(len(raw_hits)))',
        ),
    )
    for old, new in replacements:
        if old not in probe:
            raise RuntimeError("diagnostic probe source shape changed")
        probe = probe.replace(old, new, 1)
    return probe


DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE = _build_diagnostic_probe()
_COUNT_RE = re.compile(r"TYPED_OBJECT_COUNT=(\d+) RAW_VPTR_COUNT=(\d+)")
_SAFE_CODES = (
    "START_TICKS_MISMATCH",
    "EXACT_FENCE_MISMATCH",
    "CLIENT_MAPPING_MISSING",
    "NO_BOUNDED_RW_MAPPINGS",
    "RW_SCAN_BOUND_EXCEEDED",
    "START_TICKS_CHANGED_DURING_READ",
)


def _safe_live_failure(exc: Exception) -> str:
    text = str(exc)
    match = _COUNT_RE.search(text)
    if match:
        return f"TYPED_OBJECT_COUNT={int(match.group(1))}:RAW_VPTR_COUNT={int(match.group(2))}"
    for code in _SAFE_CODES:
        if code in text:
            return code
    return type(exc).__name__


def read_action_protocol_presence(
    *,
    reader_id: str,
    type_name: str,
    mangled_name: str,
    pid: int,
    start_ticks: int,
    runner: Callable[[list[str]], str],
    container: str = EXPECTED_TARGET_CONTAINER,
) -> dict[str, object]:
    try:
        raw_layout = runner(
            [
                "docker", "exec", container, "python3", "-c", STATIC_LAYOUT_PROBE,
                str(pid), str(start_ticks), str(EXPECTED_CLIENT_SIZE), EXPECTED_CLIENT_SHA256,
                type_name, mangled_name,
            ]
        ).strip()
        layout_doc = json.loads(raw_layout)
        if layout_doc.get("state") != "AVAILABLE":
            raise TypedPresenceResolverError("static layout probe unavailable")
        layout = TypedPresenceLayout(
            type_name=type_name,
            mangled_name=mangled_name,
            vptr=int(layout_doc["vptr_offset"]),
            typeinfo=int(layout_doc["typeinfo_offset"]),
        )
    except Exception as exc:
        return {
            "state": "UNAVAILABLE",
            "reader_id": reader_id,
            "reason": f"STATIC_LAYOUT_FAILED:{type(exc).__name__}",
            "semantic_promotion_allowed": False,
        }

    try:
        raw = runner(
            [
                "docker", "exec", container, "python3", "-c", DIAGNOSTIC_READ_ONLY_PRESENCE_PROBE,
                str(pid), str(start_ticks), str(EXPECTED_CLIENT_SIZE), EXPECTED_CLIENT_SHA256,
                hex(layout.vptr), reader_id, type_name,
            ]
        ).strip()
        doc = json.loads(raw)
    except Exception as exc:
        return {
            "state": "UNAVAILABLE",
            "reader_id": reader_id,
            "reason": f"LIVE_TYPED_PROBE_FAILED:{_safe_live_failure(exc)}",
            "layout_evidence": layout.evidence(),
            "semantic_promotion_allowed": False,
        }

    doc["layout_evidence"] = layout.evidence()
    doc["semantic_promotion_allowed"] = False
    return doc
