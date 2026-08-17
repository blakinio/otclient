#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path


OLD_FILTER = '''                    if (
                        int(attr.map_state) == VIEWABLE
                        and int(attr.width) == TARGET_WIDTH
                        and int(attr.height) == TARGET_HEIGHT
                    ):
                        candidates.append(
                            WindowCandidate(xid, int(attr.width), int(attr.height))
                        )
'''

NEW_FILTER = '''                    if int(attr.map_state) == VIEWABLE:
                        candidates.append(
                            WindowCandidate(xid, int(attr.width), int(attr.height))
                        )
'''

OLD_SELECT = '''    matches: list[int] = []
    for candidate in candidates:
        pid = pid_for_xid(candidate.xid)
        if pid == expected_pid:
            matches.append(candidate.xid)
    if len(matches) > 1:
        raise WindowOwnerError("multiple viewable windows resolve to expected PID")
    return matches[0] if matches else None
'''

NEW_SELECT = '''    matches: list[WindowCandidate] = []
    for candidate in candidates:
        pid = pid_for_xid(candidate.xid)
        if pid == expected_pid:
            matches.append(candidate)
    if not matches:
        return None

    geometry_counts: dict[tuple[int, int], int] = {}
    for candidate in matches:
        key = (candidate.width, candidate.height)
        geometry_counts[key] = geometry_counts.get(key, 0) + 1
    print(
        "WORLDMAP_XRES_OWNED_VIEWABLE_COUNT=" + str(len(matches)),
        file=sys.stderr,
    )
    for (width, height), count in sorted(geometry_counts.items()):
        print(
            f"WORLDMAP_XRES_OWNED_GEOMETRY={width}x{height};count={count}",
            file=sys.stderr,
        )

    max_area = max(candidate.width * candidate.height for candidate in matches)
    largest = [
        candidate
        for candidate in matches
        if candidate.width * candidate.height == max_area
    ]
    if len(largest) != 1:
        raise WindowOwnerError("largest owned viewable window is ambiguous")
    selected = largest[0]
    print(
        f"WORLDMAP_XRES_SELECTED_GEOMETRY={selected.width}x{selected.height}",
        file=sys.stderr,
    )
    return selected.xid
'''

OLD_ERROR = '    raise WindowOwnerError("no viewable 1920x1080 window owned by expected PID")\n'
NEW_ERROR = '    raise WindowOwnerError("no viewable window owned by expected PID")\n'


class TransformRefused(RuntimeError):
    pass


def transform(text: str) -> str:
    anchors = {
        "geometry_filter": (OLD_FILTER, NEW_FILTER),
        "owned_selector": (OLD_SELECT, NEW_SELECT),
        "terminal_error": (OLD_ERROR, NEW_ERROR),
    }
    output = text
    for name, (old, new) in anchors.items():
        count = output.count(old)
        if count != 1:
            raise TransformRefused(f"{name}_anchor_count:{count}")
        output = output.replace(old, new, 1)

    required = (
        "WORLDMAP_XRES_OWNED_VIEWABLE_COUNT=",
        "WORLDMAP_XRES_OWNED_GEOMETRY=",
        "WORLDMAP_XRES_SELECTED_GEOMETRY=",
        "largest owned viewable window is ambiguous",
        "if int(attr.map_state) == VIEWABLE:",
    )
    missing = [token for token in required if token not in output]
    if missing:
        raise TransformRefused("required_missing:" + ",".join(missing))
    if "and int(attr.width) == TARGET_WIDTH" in output or "and int(attr.height) == TARGET_HEIGHT" in output:
        raise TransformRefused("target_geometry_filter_survived")
    return output


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    if not args.source.is_file():
        print("WORLDMAP_XRES_GEOMETRY_CENSUS_REPAIR_REFUSED=source_missing")
        return 44
    try:
        repaired = transform(args.source.read_text(encoding="utf-8"))
    except TransformRefused as exc:
        print(f"WORLDMAP_XRES_GEOMETRY_CENSUS_REPAIR_REFUSED={exc}")
        return 44
    args.output.write_text(repaired, encoding="utf-8")
    args.output.chmod(0o600)
    print("WORLDMAP_XRES_GEOMETRY_CENSUS_REPAIR=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
