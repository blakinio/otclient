#!/usr/bin/env python3
"""Fail-closed shared GUI/input serialization for Track A canonical runtime."""
from __future__ import annotations

import contextlib
import errno
import os
import stat
import sys
import time
from pathlib import Path
from typing import Callable, Iterator


class InputLockError(RuntimeError):
    def __init__(self, code: str):
        super().__init__(code)
        self.code = code


class InputLock:
    def __init__(self, state_root: Path):
        self.state_root = Path(state_root)
        self.path = self.state_root / "input.lock"

    def _open_safe(self) -> int:
        self.state_root.mkdir(parents=True, exist_ok=True, mode=0o700)
        flags = os.O_RDWR | os.O_CREAT
        if hasattr(os, "O_NOFOLLOW"):
            flags |= os.O_NOFOLLOW
        try:
            fd = os.open(self.path, flags, 0o600)
        except OSError as exc:
            raise InputLockError("input_lock_unsafe") from exc
        try:
            if hasattr(os, "fchmod"):
                os.fchmod(fd, 0o600)
            else:
                os.chmod(self.path, 0o600)
            st = os.fstat(fd)
            owner_ok = not hasattr(os, "getuid") or st.st_uid == os.getuid()
            mode_ok = sys.platform.startswith("win") or stat.S_IMODE(st.st_mode) == 0o600
            if not stat.S_ISREG(st.st_mode) or not mode_ok or not owner_ok:
                raise InputLockError("input_lock_unsafe")
            try:
                path_st = self.path.lstat()
            except OSError as exc:
                raise InputLockError("input_lock_unsafe") from exc
            if stat.S_ISLNK(path_st.st_mode):
                raise InputLockError("input_lock_unsafe")
            if hasattr(st, "st_ino") and hasattr(path_st, "st_ino"):
                if (st.st_dev, st.st_ino) != (path_st.st_dev, path_st.st_ino):
                    raise InputLockError("input_lock_unsafe")
            return fd
        except BaseException:
            os.close(fd)
            raise

    @staticmethod
    def _try_lock(fd: int) -> bool:
        if sys.platform.startswith("win"):
            import msvcrt

            os.lseek(fd, 0, os.SEEK_SET)
            if os.fstat(fd).st_size == 0:
                os.write(fd, b"\0")
                os.fsync(fd)
            os.lseek(fd, 0, os.SEEK_SET)
            try:
                msvcrt.locking(fd, msvcrt.LK_NBLCK, 1)
                return True
            except OSError as exc:
                if exc.errno in (errno.EACCES, errno.EDEADLK, errno.EAGAIN, 13, 36):
                    return False
                raise
        import fcntl

        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            return True
        except BlockingIOError:
            return False

    @staticmethod
    def _unlock(fd: int) -> None:
        if sys.platform.startswith("win"):
            import msvcrt

            os.lseek(fd, 0, os.SEEK_SET)
            msvcrt.locking(fd, msvcrt.LK_UNLCK, 1)
            return
        import fcntl

        fcntl.flock(fd, fcntl.LOCK_UN)

    @contextlib.contextmanager
    def acquire(
        self,
        *,
        timeout_seconds: float,
        cancelled: Callable[[], bool],
    ) -> Iterator[None]:
        if timeout_seconds <= 0:
            raise InputLockError("input_lock_timeout")
        if cancelled():
            raise InputLockError("input_lock_cancelled")
        fd = self._open_safe()
        locked = False
        deadline = time.monotonic() + timeout_seconds
        try:
            while True:
                if cancelled():
                    raise InputLockError("input_lock_cancelled")
                if self._try_lock(fd):
                    locked = True
                    break
                if time.monotonic() >= deadline:
                    raise InputLockError("input_lock_timeout")
                time.sleep(min(0.01, max(0.0, deadline - time.monotonic())))
            yield
        finally:
            if locked:
                self._unlock(fd)
            os.close(fd)
