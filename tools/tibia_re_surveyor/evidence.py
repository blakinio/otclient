from __future__ import annotations

import json
from pathlib import Path
import re
import subprocess
from typing import Dict, Iterable, List, Optional, Sequence

_ROW_ID_RE = re.compile(r"\b([A-H]\d{2})\b")
_TEXT_SUFFIXES = {".md", ".json", ".jsonl", ".yaml", ".yml", ".txt"}


class RepositoryReadError(RuntimeError):
    pass


class RepoReader:
    def read_text(self, relative_path: str) -> str:
        raise NotImplementedError

    def scan_evidence_mentions(
        self, row_ids: Sequence[str], current_client_sha256: str, max_refs_per_row: int = 8
    ) -> Dict[str, dict]:
        raise NotImplementedError


class LocalRepoReader(RepoReader):
    def __init__(self, root: Path):
        self.root = root.resolve()

    def read_text(self, relative_path: str) -> str:
        path = (self.root / relative_path).resolve()
        if self.root not in path.parents and path != self.root:
            raise RepositoryReadError("repository path escapes root")
        try:
            return path.read_text(encoding="utf-8")
        except (OSError, UnicodeError) as exc:
            raise RepositoryReadError(f"cannot read {relative_path}: {exc}") from exc

    def scan_evidence_mentions(
        self, row_ids: Sequence[str], current_client_sha256: str, max_refs_per_row: int = 8
    ) -> Dict[str, dict]:
        root = self.root / "docs" / "agents" / "evidence"
        index = _empty_index(row_ids)
        if not root.is_dir():
            return index
        allowed = set(row_ids)
        for path in sorted(root.rglob("*")):
            if not path.is_file() or path.suffix.lower() not in _TEXT_SUFFIXES:
                continue
            try:
                if path.stat().st_size > 1_000_000:
                    continue
                text = path.read_text(encoding="utf-8", errors="replace")
            except OSError:
                continue
            _consume_text(
                index,
                allowed,
                str(path.relative_to(self.root)),
                text,
                current_client_sha256,
                max_refs_per_row,
            )
        return index


class DockerRepoReader(RepoReader):
    def __init__(self, container: str, root: str, timeout: float = 30.0):
        if not re.fullmatch(r"[A-Za-z0-9_.-]+", container):
            raise ValueError("invalid repository container name")
        if not root.startswith("/") or "\x00" in root:
            raise ValueError("repository root must be absolute")
        self.container = container
        self.root = root.rstrip("/")
        self.timeout = timeout

    def _run(self, args: Sequence[str], timeout: Optional[float] = None) -> str:
        try:
            completed = subprocess.run(
                ["docker", "exec", self.container, *args],
                check=False,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                universal_newlines=True,
                timeout=self.timeout if timeout is None else timeout,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            raise RepositoryReadError(f"docker repository read failed: {exc}") from exc
        if completed.returncode != 0:
            detail = completed.stderr.strip()[:300]
            raise RepositoryReadError(f"docker repository read failed rc={completed.returncode}: {detail}")
        return completed.stdout

    def read_text(self, relative_path: str) -> str:
        if relative_path.startswith("/") or ".." in Path(relative_path).parts:
            raise RepositoryReadError("relative repository path required")
        return self._run(["cat", f"{self.root}/{relative_path}"])

    def scan_evidence_mentions(
        self, row_ids: Sequence[str], current_client_sha256: str, max_refs_per_row: int = 8
    ) -> Dict[str, dict]:
        script = r'''
import json, pathlib, re, sys
root = pathlib.Path(sys.argv[1])
allowed = set(json.loads(sys.argv[2]))
sha = sys.argv[3]
max_refs = int(sys.argv[4])
suffixes = {'.md','.json','.jsonl','.yaml','.yml','.txt'}
pattern = re.compile(r'\b([A-H]\d{2})\b')
out = {row:{'mention_count':0,'current_sha_match_count':0,'refs':[]} for row in allowed}
evidence = root / 'docs' / 'agents' / 'evidence'
if evidence.is_dir():
  for path in sorted(evidence.rglob('*')):
    if not path.is_file() or path.suffix.lower() not in suffixes:
      continue
    try:
      if path.stat().st_size > 1000000:
        continue
      text = path.read_text(encoding='utf-8', errors='replace')
    except OSError:
      continue
    ids = sorted(set(pattern.findall(text)) & allowed)
    if not ids:
      continue
    rel = str(path.relative_to(root))
    has_sha = sha in text
    for row in ids:
      item = out[row]
      item['mention_count'] += 1
      if has_sha:
        item['current_sha_match_count'] += 1
      if len(item['refs']) < max_refs:
        item['refs'].append({'path':rel,'current_sha_match':has_sha})
print(json.dumps(out, sort_keys=True, separators=(',',':')))
'''
        raw = self._run(
            [
                "python3",
                "-c",
                script,
                self.root,
                json.dumps(list(row_ids)),
                current_client_sha256,
                str(max_refs_per_row),
            ],
            timeout=60.0,
        )
        try:
            return json.loads(raw)
        except json.JSONDecodeError as exc:
            raise RepositoryReadError("invalid evidence-index response") from exc


def _empty_index(row_ids: Iterable[str]) -> Dict[str, dict]:
    return {
        row_id: {"mention_count": 0, "current_sha_match_count": 0, "refs": []}
        for row_id in row_ids
    }


def _consume_text(
    index: Dict[str, dict],
    allowed: set,
    relative_path: str,
    text: str,
    current_client_sha256: str,
    max_refs_per_row: int,
) -> None:
    row_ids = sorted(set(_ROW_ID_RE.findall(text)) & allowed)
    if not row_ids:
        return
    current_sha_match = current_client_sha256 in text
    for row_id in row_ids:
        item = index[row_id]
        item["mention_count"] += 1
        if current_sha_match:
            item["current_sha_match_count"] += 1
        if len(item["refs"]) < max_refs_per_row:
            item["refs"].append(
                {"path": relative_path, "current_sha_match": current_sha_match}
            )
