#!/usr/bin/env python3
"""Fail-closed controller lease for the Track A canonical live runtime.

This tool coordinates *authority* to mutate a future canonical Track A live
runtime. It does not discover, start, stop, attach to, log in, or otherwise
mutate the Tibia client itself.

The durable lease record stores only a SHA-256 digest of the capability token.
The raw token is written to a caller-selected mode-0600 task-local file.
"""

from __future__ import annotations

import argparse
import fcntl
import hashlib
import json
import os
import re
import secrets
import stat
import subprocess
import sys
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterator, Sequence

SCHEMA_VERSION = 1
RUNTIME_ID = "track-a-canonical-live"
DEFAULT_STATE_DIR = Path(
    "/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime"
)
DEFAULT_TTL_SECONDS = 45 * 60
MIN_TTL_SECONDS = 60
MAX_TTL_SECONDS = 45 * 60
IDENT_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._:/-]{0,199}$")


class LeaseError(RuntimeError):
    def __init__(self, code: str, message: str) -> None:
        super().__init__(message)
        self.code = code


@dataclass(frozen=True)
class LeaseIdentity:
    task_id: str
    session_id: str


@dataclass(frozen=True)
class LeaseResult:
    generation: int
    expires_at: int | None
    stale_takeover: bool = False
    idempotent: bool = False


def _now_epoch(now: float | None = None) -> int:
    return int(time.time() if now is None else now)


def _validate_identity(value: str, field: str) -> str:
    if not IDENT_RE.fullmatch(value):
        raise LeaseError("invalid_identity", f"invalid {field}")
    return value


def _validate_reason(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not value or len(value) > 256 or "\n" in value or "\r" in value:
        raise LeaseError("invalid_stale_reason", "invalid stale takeover reason")
    return value


def _token_digest(token: str) -> str:
    return hashlib.sha256(token.encode("ascii")).hexdigest()


def _fsync_dir(path: Path) -> None:
    fd = os.open(path, os.O_RDONLY | getattr(os, "O_DIRECTORY", 0))
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def _atomic_write_text(path: Path, text: str, mode: int = 0o600) -> None:
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    os.chmod(path.parent, 0o700)
    fd, tmp_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    tmp = Path(tmp_name)
    try:
        os.fchmod(fd, mode)
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(tmp, path)
        os.chmod(path, mode)
        _fsync_dir(path.parent)
    except Exception:
        try:
            os.close(fd)
        except OSError:
            pass
        try:
            tmp.unlink()
        except FileNotFoundError:
            pass
        raise


def _read_private_token(path: Path) -> str:
    try:
        st = path.stat()
    except FileNotFoundError as exc:
        raise LeaseError("token_file_missing", "lease token file is missing") from exc
    if not stat.S_ISREG(st.st_mode):
        raise LeaseError("token_file_invalid", "lease token path is not a regular file")
    if stat.S_IMODE(st.st_mode) & 0o077:
        raise LeaseError("token_file_permissions", "lease token file must be mode 0600")
    if hasattr(os, "getuid") and st.st_uid != os.getuid():
        raise LeaseError("token_file_owner", "lease token file is not owned by current uid")
    token = path.read_text(encoding="ascii").strip()
    if not re.fullmatch(r"[0-9a-f]{64}", token):
        raise LeaseError("token_file_invalid", "lease token file content is invalid")
    return token


class LeaseManager:
    def __init__(self, state_dir: Path) -> None:
        self.state_dir = state_dir
        self.lock_path = state_dir / "coordination.lock"
        self.state_path = state_dir / "lease.json"

    def _prepare(self) -> None:
        self.state_dir.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.state_dir, 0o700)
        if not self.lock_path.exists():
            fd = os.open(self.lock_path, os.O_CREAT | os.O_RDWR, 0o600)
            os.close(fd)
        os.chmod(self.lock_path, 0o600)

    @contextmanager
    def locked(self) -> Iterator[None]:
        self._prepare()
        fd = os.open(self.lock_path, os.O_RDWR)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            yield
        finally:
            fcntl.flock(fd, fcntl.LOCK_UN)
            os.close(fd)

    def _load_state_unlocked(self) -> dict[str, Any] | None:
        if not self.state_path.exists():
            return None
        try:
            data = json.loads(self.state_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise LeaseError("state_corrupt", "lease state is unreadable or invalid JSON") from exc
        if not isinstance(data, dict):
            raise LeaseError("state_corrupt", "lease state must be an object")
        if data.get("schema_version") != SCHEMA_VERSION or data.get("runtime_id") != RUNTIME_ID:
            raise LeaseError("state_schema_mismatch", "lease state schema/runtime identity mismatch")
        if data.get("status") not in {"active", "released"}:
            raise LeaseError("state_corrupt", "lease state status is invalid")
        generation = data.get("generation")
        if not isinstance(generation, int) or generation < 1:
            raise LeaseError("state_corrupt", "lease generation is invalid")
        if data["status"] == "active":
            required = (
                "controller_task",
                "controller_session",
                "token_sha256",
                "acquired_at",
                "renewed_at",
                "expires_at",
            )
            if any(data.get(key) in (None, "") for key in required):
                raise LeaseError("state_corrupt", "active lease is missing required fields")
            if not re.fullmatch(r"[0-9a-f]{64}", str(data["token_sha256"])):
                raise LeaseError("state_corrupt", "active lease token digest is invalid")
        return data

    def _write_state_unlocked(self, data: dict[str, Any]) -> None:
        payload = json.dumps(data, sort_keys=True, indent=2) + "\n"
        _atomic_write_text(self.state_path, payload, 0o600)

    @staticmethod
    def _active_and_fresh(state: dict[str, Any], now: int) -> bool:
        return state.get("status") == "active" and int(state.get("expires_at", 0)) > now

    @staticmethod
    def _identity_matches(state: dict[str, Any], identity: LeaseIdentity) -> bool:
        return (
            state.get("controller_task") == identity.task_id
            and state.get("controller_session") == identity.session_id
        )

    @staticmethod
    def _token_matches(state: dict[str, Any], token: str) -> bool:
        expected = str(state.get("token_sha256", ""))
        return secrets.compare_digest(expected, _token_digest(token))

    def acquire(
        self,
        identity: LeaseIdentity,
        token_file: Path,
        ttl_seconds: int,
        *,
        stale_reason: str | None = None,
        now: float | None = None,
    ) -> LeaseResult:
        now_epoch = _now_epoch(now)
        stale_reason = _validate_reason(stale_reason)
        with self.locked():
            previous = self._load_state_unlocked()
            if previous is not None and self._active_and_fresh(previous, now_epoch):
                if self._identity_matches(previous, identity) and token_file.exists():
                    token = _read_private_token(token_file)
                    if self._token_matches(previous, token):
                        previous["renewed_at"] = now_epoch
                        previous["expires_at"] = now_epoch + ttl_seconds
                        self._write_state_unlocked(previous)
                        return LeaseResult(
                            generation=int(previous["generation"]),
                            expires_at=int(previous["expires_at"]),
                            idempotent=True,
                        )
                raise LeaseError(
                    "lease_conflict",
                    "a non-expired canonical live controller lease already exists",
                )

            stale_takeover = bool(
                previous is not None
                and previous.get("status") == "active"
                and int(previous.get("expires_at", 0)) <= now_epoch
            )
            if stale_takeover and stale_reason is None:
                raise LeaseError(
                    "stale_takeover_reason_required",
                    "expired lease takeover requires an explicit reason",
                )

            generation = 1 if previous is None else int(previous["generation"]) + 1
            token = secrets.token_hex(32)
            token_digest = _token_digest(token)
            takeover_from: dict[str, Any] | None = None
            if stale_takeover and previous is not None:
                takeover_from = {
                    "generation": int(previous["generation"]),
                    "controller_task": previous.get("controller_task"),
                    "controller_session": previous.get("controller_session"),
                    "expired_at": int(previous.get("expires_at", 0)),
                    "reason": stale_reason,
                }

            state: dict[str, Any] = {
                "schema_version": SCHEMA_VERSION,
                "runtime_id": RUNTIME_ID,
                "status": "active",
                "generation": generation,
                "controller_task": identity.task_id,
                "controller_session": identity.session_id,
                "token_sha256": token_digest,
                "acquired_at": now_epoch,
                "renewed_at": now_epoch,
                "expires_at": now_epoch + ttl_seconds,
                "takeover_from": takeover_from,
            }
            _atomic_write_text(token_file, token + "\n", 0o600)
            self._write_state_unlocked(state)
            return LeaseResult(
                generation=generation,
                expires_at=int(state["expires_at"]),
                stale_takeover=stale_takeover,
            )

    def renew(
        self,
        identity: LeaseIdentity,
        token_file: Path,
        ttl_seconds: int,
        *,
        now: float | None = None,
    ) -> LeaseResult:
        now_epoch = _now_epoch(now)
        token = _read_private_token(token_file)
        with self.locked():
            state = self._load_state_unlocked()
            self._require_current_unlocked(state, identity, token, now_epoch)
            assert state is not None
            state["renewed_at"] = now_epoch
            state["expires_at"] = now_epoch + ttl_seconds
            self._write_state_unlocked(state)
            return LeaseResult(int(state["generation"]), int(state["expires_at"]))

    def release(
        self,
        identity: LeaseIdentity,
        token_file: Path,
        *,
        now: float | None = None,
    ) -> LeaseResult:
        now_epoch = _now_epoch(now)
        token = _read_private_token(token_file)
        with self.locked():
            state = self._load_state_unlocked()
            if state is None or state.get("status") != "active":
                raise LeaseError("lease_not_active", "no active lease exists")
            if not self._identity_matches(state, identity):
                raise LeaseError("lease_identity_mismatch", "controller identity mismatch")
            if not self._token_matches(state, token):
                raise LeaseError("lease_token_mismatch", "lease token mismatch")
            generation = int(state["generation"])
            state.update(
                {
                    "status": "released",
                    "last_controller_task": state.get("controller_task"),
                    "last_controller_session": state.get("controller_session"),
                    "released_at": now_epoch,
                    "controller_task": None,
                    "controller_session": None,
                    "token_sha256": None,
                    "expires_at": None,
                    "renewed_at": None,
                }
            )
            self._write_state_unlocked(state)
            try:
                token_file.unlink()
            except FileNotFoundError:
                pass
            return LeaseResult(generation, None)

    def validate(
        self,
        identity: LeaseIdentity,
        token_file: Path,
        *,
        now: float | None = None,
    ) -> LeaseResult:
        now_epoch = _now_epoch(now)
        token = _read_private_token(token_file)
        with self.locked():
            state = self._load_state_unlocked()
            self._require_current_unlocked(state, identity, token, now_epoch)
            assert state is not None
            return LeaseResult(int(state["generation"]), int(state["expires_at"]))

    def _require_current_unlocked(
        self,
        state: dict[str, Any] | None,
        identity: LeaseIdentity,
        token: str,
        now_epoch: int,
    ) -> None:
        if state is None or state.get("status") != "active":
            raise LeaseError("lease_not_active", "no active lease exists")
        if not self._identity_matches(state, identity):
            raise LeaseError("lease_identity_mismatch", "controller identity mismatch")
        if not self._token_matches(state, token):
            raise LeaseError("lease_token_mismatch", "lease token mismatch")
        if int(state.get("expires_at", 0)) <= now_epoch:
            raise LeaseError("lease_expired", "controller lease has expired")

    def status(self, *, now: float | None = None) -> dict[str, Any]:
        now_epoch = _now_epoch(now)
        with self.locked():
            state = self._load_state_unlocked()
            if state is None:
                return {
                    "schema_version": SCHEMA_VERSION,
                    "runtime_id": RUNTIME_ID,
                    "status": "absent",
                    "generation": 0,
                    "controller_task": None,
                    "controller_session": None,
                    "expires_at": None,
                    "expired": False,
                }
            public = {
                "schema_version": SCHEMA_VERSION,
                "runtime_id": RUNTIME_ID,
                "status": state["status"],
                "generation": int(state["generation"]),
                "controller_task": state.get("controller_task"),
                "controller_session": state.get("controller_session"),
                "acquired_at": state.get("acquired_at"),
                "renewed_at": state.get("renewed_at"),
                "expires_at": state.get("expires_at"),
                "released_at": state.get("released_at"),
                "expired": bool(
                    state.get("status") == "active"
                    and int(state.get("expires_at", 0)) <= now_epoch
                ),
                "takeover_from": state.get("takeover_from"),
            }
            return public

    def guard_run(
        self,
        identity: LeaseIdentity,
        token_file: Path,
        command: Sequence[str],
        *,
        now: float | None = None,
    ) -> tuple[LeaseResult, int]:
        if not command:
            raise LeaseError("guard_command_missing", "guard-run requires a command")
        now_epoch = _now_epoch(now)
        token = _read_private_token(token_file)
        with self.locked():
            state = self._load_state_unlocked()
            self._require_current_unlocked(state, identity, token, now_epoch)
            assert state is not None
            result = LeaseResult(int(state["generation"]), int(state["expires_at"]))
            completed = subprocess.run(list(command), check=False)
            return result, int(completed.returncode)


def _identity_from_args(args: argparse.Namespace) -> LeaseIdentity:
    return LeaseIdentity(
        _validate_identity(args.task_id, "task-id"),
        _validate_identity(args.session_id, "session-id"),
    )


def _ttl_from_args(args: argparse.Namespace) -> int:
    ttl = int(args.ttl_seconds)
    if not MIN_TTL_SECONDS <= ttl <= MAX_TTL_SECONDS:
        raise LeaseError(
            "invalid_ttl",
            f"ttl must be between {MIN_TTL_SECONDS} and {MAX_TTL_SECONDS} seconds",
        )
    return ttl


def _add_identity(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--task-id", required=True)
    parser.add_argument("--session-id", required=True)
    parser.add_argument("--token-file", required=True, type=Path)


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=Path, default=DEFAULT_STATE_DIR)
    sub = parser.add_subparsers(dest="operation", required=True)

    acquire = sub.add_parser("acquire")
    _add_identity(acquire)
    acquire.add_argument("--ttl-seconds", type=int, default=DEFAULT_TTL_SECONDS)
    acquire.add_argument("--stale-takeover-reason")

    renew = sub.add_parser("renew")
    _add_identity(renew)
    renew.add_argument("--ttl-seconds", type=int, default=DEFAULT_TTL_SECONDS)

    release = sub.add_parser("release")
    _add_identity(release)

    validate = sub.add_parser("validate")
    _add_identity(validate)

    status_parser = sub.add_parser("status")
    status_parser.add_argument("--json", action="store_true")

    guard = sub.add_parser("guard-run")
    _add_identity(guard)
    guard.add_argument("command", nargs=argparse.REMAINDER)
    return parser


def _print_result(operation: str, result: LeaseResult) -> None:
    prefix = "TRACK_A_CANONICAL_LEASE"
    print(f"{prefix}_{operation.upper().replace('-', '_')}=true")
    print(f"{prefix}_GENERATION={result.generation}")
    if result.expires_at is not None:
        print(f"{prefix}_EXPIRES_AT_EPOCH={result.expires_at}")
    if operation == "acquire":
        print(f"{prefix}_STALE_TAKEOVER={str(result.stale_takeover).lower()}")
        print(f"{prefix}_IDEMPOTENT={str(result.idempotent).lower()}")


def main(argv: Sequence[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    manager = LeaseManager(args.state_dir)
    try:
        if args.operation == "status":
            public = manager.status()
            if args.json:
                print(json.dumps(public, sort_keys=True))
            else:
                print(f"TRACK_A_CANONICAL_LEASE_STATUS={public['status']}")
                print(f"TRACK_A_CANONICAL_LEASE_GENERATION={public['generation']}")
                print(
                    "TRACK_A_CANONICAL_LEASE_CONTROLLER_TASK="
                    + str(public.get("controller_task") or "none")
                )
                print(
                    "TRACK_A_CANONICAL_LEASE_CONTROLLER_SESSION="
                    + str(public.get("controller_session") or "none")
                )
                print(
                    "TRACK_A_CANONICAL_LEASE_EXPIRED="
                    + str(bool(public.get("expired"))).lower()
                )
            return 0

        identity = _identity_from_args(args)
        if args.operation == "acquire":
            result = manager.acquire(
                identity,
                args.token_file,
                _ttl_from_args(args),
                stale_reason=args.stale_takeover_reason,
            )
            _print_result("acquire", result)
            return 0
        if args.operation == "renew":
            result = manager.renew(identity, args.token_file, _ttl_from_args(args))
            _print_result("renew", result)
            return 0
        if args.operation == "release":
            result = manager.release(identity, args.token_file)
            _print_result("release", result)
            return 0
        if args.operation == "validate":
            result = manager.validate(identity, args.token_file)
            _print_result("validate", result)
            return 0
        if args.operation == "guard-run":
            command = list(args.command)
            if command and command[0] == "--":
                command = command[1:]
            result, rc = manager.guard_run(identity, args.token_file, command)
            _print_result("guard_run", result)
            print(f"TRACK_A_CANONICAL_LEASE_GUARD_COMMAND_RC={rc}")
            return rc
        raise AssertionError(args.operation)
    except LeaseError as exc:
        print(f"TRACK_A_CANONICAL_LEASE_ERROR={exc.code}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
