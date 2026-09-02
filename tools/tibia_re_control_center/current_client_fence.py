from __future__ import annotations

import argparse
import json
import re
import shlex
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[2]
CURRENT_CLIENT_FENCE_MANIFEST = REPO_ROOT / "docs/agents/contracts/TRACK_A_CURRENT_CLIENT_FENCE_V1.json"
_VERSION_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._+-]{0,127}$")
_SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
_PREFIX_RE = re.compile(r"^[A-Z][A-Z0-9_]*$")


@dataclass(frozen=True, slots=True)
class ClientFence:
    version: str
    size: int
    sha256: str

    def as_tuple(self) -> tuple[str, int, str]:
        return (self.version, self.size, self.sha256)

@dataclass(frozen=True, slots=True)
class CurrentClientFenceManifest:
    schema_version: int
    current: ClientFence
    current_provenance: str
    approved_history: tuple[ClientFence, ...]


def _parse_fence(value: Any, *, label: str) -> ClientFence:
    if not isinstance(value, dict) or set(value) != {"version", "size", "sha256"}:
        raise ValueError(f"{label} fence fields invalid")
    version = value.get("version")
    size = value.get("size")
    sha256 = value.get("sha256")
    if not isinstance(version, str) or _VERSION_RE.fullmatch(version) is None:
        raise ValueError(f"{label} version invalid")
    if isinstance(size, bool) or not isinstance(size, int) or size <= 0:
        raise ValueError(f"{label} size invalid")
    if not isinstance(sha256, str) or _SHA256_RE.fullmatch(sha256) is None:
        raise ValueError(f"{label} sha256 invalid")
    return ClientFence(version=version, size=size, sha256=sha256)


def load_current_client_fence_manifest(
    path: Path | str | None = None,
) -> CurrentClientFenceManifest:
    manifest_path = Path(path) if path is not None else CURRENT_CLIENT_FENCE_MANIFEST
    try:
        raw = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError("current client fence manifest unreadable") from exc
    if not isinstance(raw, dict) or set(raw) != {
        "schema_version",
        "current",
        "current_provenance",
        "approved_history",
    }:
        raise ValueError("manifest fields invalid")
    if raw.get("schema_version") != 1:
        raise ValueError("manifest schema version invalid")
    current_provenance = raw.get("current_provenance")
    if not isinstance(current_provenance, str):
        raise ValueError("current provenance invalid")
    provenance_path = PurePosixPath(current_provenance)
    if (
        provenance_path.is_absolute()
        or ".." in provenance_path.parts
        or provenance_path.parts[:3] != ("docs", "agents", "evidence")
        or provenance_path.suffix != ".json"
    ):
        raise ValueError("current provenance invalid")
    provenance_file = REPO_ROOT.joinpath(*provenance_path.parts)
    if provenance_file.is_symlink() or not provenance_file.is_file():
        raise ValueError("current provenance invalid")
    history_raw = raw.get("approved_history")
    if not isinstance(history_raw, list):
        raise TypeError("approved history invalid")
    current = _parse_fence(raw.get("current"), label="current")
    history = tuple(
        _parse_fence(item, label=f"approved_history[{index}]")
        for index, item in enumerate(history_raw)
    )
    if current in history:
        raise ValueError("current fence in history")
    if len(set(history)) != len(history):
        raise ValueError("duplicate history fence")
    return CurrentClientFenceManifest(
        schema_version=1,
        current=current,
        current_provenance=current_provenance,
        approved_history=history,
    )


def current_client_fence(path: Path | str | None = None) -> ClientFence:
    return load_current_client_fence_manifest(path).current


def approved_historical_fences(
    path: Path | str | None = None,
) -> tuple[ClientFence, ...]:
    return load_current_client_fence_manifest(path).approved_history


def approved_reconciliation_sources(
    path: Path | str | None = None,
) -> tuple[ClientFence, ...]:
    manifest = load_current_client_fence_manifest(path)
    return (manifest.current, *manifest.approved_history)


def _env_lines(prefix: str) -> tuple[str, ...]:
    if _PREFIX_RE.fullmatch(prefix) is None:
        raise ValueError("environment prefix invalid")
    fence = current_client_fence()
    return (
        f"{prefix}_VERSION={fence.version}",
        f"{prefix}_SIZE={fence.size}",
        f"{prefix}_SHA={fence.sha256}",
        f"{prefix}_SHA256={fence.sha256}",
    )

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Read the canonical Track A current-client fence")
    subparsers = parser.add_subparsers(dest="command", required=True)
    shell = subparsers.add_parser("shell")
    shell.add_argument("--prefix", default="TRACK_A_CURRENT_CLIENT")
    github_env = subparsers.add_parser("github-env")
    github_env.add_argument("path", type=Path)
    github_env.add_argument("--prefix", default="EXPECTED")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    lines = _env_lines(args.prefix)
    if args.command == "shell":
        for line in lines:
            name, value = line.split("=", 1)
            print(f"{name}={shlex.quote(value)}")
        return 0
    if args.command == "github-env":
        with args.path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write("\n".join(lines) + "\n")
        return 0
    raise AssertionError("unreachable")


if __name__ == "__main__":
    raise SystemExit(main())