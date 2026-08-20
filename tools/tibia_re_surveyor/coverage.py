from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Dict, Iterable, List, Mapping, Sequence, Tuple

STATUS_ORDER = ("DONE", "PARTIAL", "NOT_STARTED", "BLOCKED")
_ROW_RE = re.compile(r"^\| \*\*([A-H])\*\* \|(.+?)\|(.+?)\|(.+?)\|(.+?)\|\s*$")
_CHECKLIST_RE = re.compile(r"^\|\s*([A-H]\d{2})\s*\|\s*([^|]+?)\s*\|")
_ID_RE = re.compile(r"\b([A-H]\d{2})\b")
_RANGE_RE = re.compile(r"^([A-H])(\d{2})[–-]([A-H]?)(\d{2})$")
_SUMMARY_RE = re.compile(r"^(done|partial|not_started|blocked):\s*(\d+)\s*$", re.MULTILINE)


class CoverageParseError(ValueError):
    pass


@dataclass(frozen=True)
class CoverageRow:
    row_id: str
    title: str
    status: str

    @property
    def area(self) -> str:
        return self.row_id[0]


def _expand_token(token: str) -> List[str]:
    token = token.strip().strip("`")
    if not token or token == "—":
        return []
    match = _RANGE_RE.fullmatch(token)
    if match:
        prefix, start_raw, end_prefix, end_raw = match.groups()
        if end_prefix and end_prefix != prefix:
            raise CoverageParseError(f"cross-area range is invalid: {token}")
        start = int(start_raw)
        end = int(end_raw)
        if end < start:
            raise CoverageParseError(f"descending range is invalid: {token}")
        return [f"{prefix}{value:02d}" for value in range(start, end + 1)]
    if _ID_RE.fullmatch(token):
        return [token]
    raise CoverageParseError(f"unrecognized coverage token: {token!r}")


def expand_cell(cell: str) -> List[str]:
    normalized = cell.replace("`", "").strip()
    if normalized in {"", "—"}:
        return []
    output: List[str] = []
    for part in normalized.split(","):
        output.extend(_expand_token(part))
    return output


def parse_checklist_titles(text: str) -> Dict[str, str]:
    titles: Dict[str, str] = {}
    for line in text.splitlines():
        match = _CHECKLIST_RE.match(line)
        if not match:
            continue
        row_id, title = match.groups()
        title = title.strip().replace("`", "")
        if row_id in titles and titles[row_id] != title:
            raise CoverageParseError(f"duplicate checklist title for {row_id}")
        titles[row_id] = title
    return titles


def parse_matrix(text: str, checklist_text: str = "") -> List[CoverageRow]:
    titles = parse_checklist_titles(checklist_text) if checklist_text else {}
    statuses: Dict[str, str] = {}
    seen_area_rows = set()
    for line in text.splitlines():
        match = _ROW_RE.match(line)
        if not match:
            continue
        area, done, partial, not_started, blocked = match.groups()
        if area in seen_area_rows:
            continue
        seen_area_rows.add(area)
        for status, cell in zip(STATUS_ORDER, (done, partial, not_started, blocked)):
            for row_id in expand_cell(cell):
                if not row_id.startswith(area):
                    raise CoverageParseError(f"{row_id} appears in area {area}")
                if row_id in statuses:
                    raise CoverageParseError(f"duplicate canonical status for {row_id}")
                statuses[row_id] = status
    if seen_area_rows != set("ABCDEFGH"):
        missing = sorted(set("ABCDEFGH") - seen_area_rows)
        raise CoverageParseError(f"canonical area rows missing: {missing}")
    if len(statuses) != 169:
        raise CoverageParseError(f"expected 169 canonical rows, got {len(statuses)}")
    if titles and set(titles) != set(statuses):
        missing_titles = sorted(set(statuses) - set(titles))
        extras = sorted(set(titles) - set(statuses))
        raise CoverageParseError(
            f"checklist/matrix ID mismatch: missing_titles={missing_titles}, extras={extras}"
        )
    rows = [
        CoverageRow(row_id, titles.get(row_id, row_id), status)
        for row_id, status in sorted(statuses.items())
    ]
    expected = {key.upper(): int(value) for key, value in _SUMMARY_RE.findall(text)}
    actual = status_counts(rows)
    for status in STATUS_ORDER:
        if status in expected and expected[status] != actual[status]:
            raise CoverageParseError(
                f"summary mismatch for {status}: declared={expected[status]} actual={actual[status]}"
            )
    return rows


def status_counts(rows: Iterable[CoverageRow]) -> Dict[str, int]:
    counts = {status: 0 for status in STATUS_ORDER}
    for row in rows:
        if row.status not in counts:
            raise CoverageParseError(f"unknown status {row.status}")
        counts[row.status] += 1
    return counts


def parse_critical_dependencies(text: str) -> List[dict]:
    in_section = False
    dependencies: List[dict] = []
    for line in text.splitlines():
        if line.startswith("## 5. Critical dependency matrix"):
            in_section = True
            continue
        if in_section and line.startswith("## "):
            break
        if not in_section or not line.startswith("|"):
            continue
        cells = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(cells) != 4 or cells[0] in {"Dependency / proof gate", "---"}:
            continue
        if all(set(cell) <= {"-", ":"} for cell in cells):
            continue
        rows = sorted(set(_ID_RE.findall(cells[2])))
        dependencies.append(
            {
                "dependency": cells[0].replace("`", ""),
                "state": cells[1].replace("`", ""),
                "rows": rows,
                "required_transition": cells[3].replace("`", ""),
            }
        )
    return dependencies


def rank_next(rows: Sequence[CoverageRow], dependencies: Sequence[Mapping[str, object]], limit: int = 20) -> List[dict]:
    dependency_by_row: Dict[str, List[Mapping[str, object]]] = {}
    for dep in dependencies:
        for row_id in dep.get("rows", []):
            dependency_by_row.setdefault(str(row_id), []).append(dep)
    base_score = {"BLOCKED": 100, "NOT_STARTED": 60, "PARTIAL": 40, "DONE": 0}
    ranked: List[Tuple[int, CoverageRow, List[Mapping[str, object]]]] = []
    for row in rows:
        if row.status == "DONE":
            continue
        deps = dependency_by_row.get(row.row_id, [])
        score = base_score[row.status] + (25 if deps else 0)
        ranked.append((score, row, deps))
    ranked.sort(key=lambda item: (-item[0], item[1].row_id))
    result = []
    for score, row, deps in ranked[:limit]:
        result.append(
            {
                "row_id": row.row_id,
                "title": row.title,
                "status": row.status,
                "priority_score": score,
                "canonical_dependencies": [
                    {
                        "dependency": dep["dependency"],
                        "state": dep["state"],
                        "required_transition": dep["required_transition"],
                    }
                    for dep in deps
                ],
            }
        )
    return result
