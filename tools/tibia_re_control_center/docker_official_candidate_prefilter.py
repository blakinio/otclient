#!/usr/bin/env python3
"""Daemon-side first-stage census for official Tibia client candidates in Docker.

This helper intentionally uses ``docker top`` rather than executing a command in
container userspace.  It only decides whether a container requires the existing
deep exact identity scan; it never proves an exact candidate by itself.
"""
from __future__ import annotations

from typing import Callable, Sequence


class ProcessCensusError(RuntimeError):
    pass


def _official_hint(comm: str, args: str) -> bool:
    if comm == "client" or comm.startswith("Tibia"):
        return True
    text = args.replace("\\", "/")
    lowered = text.lower()
    if "cipsoft gmbh/tibia/" in lowered or "/tibia/packages/tibia/" in lowered:
        return True
    # Historical/current official Linux launch layouts both end in a Tibia
    # directory plus bin/client. Keep this deliberately conservative.
    return "tibia" in lowered and "/bin/client" in lowered


def container_requires_deep_scan(
    container_id: str,
    runner: Callable[[Sequence[str]], str],
) -> bool:
    """Return whether daemon-visible process metadata has an official-client hint.

    ``docker top`` is provided by the Docker daemon and does not require Python,
    ``sh`` or any other executable inside the target container.  A failure or an
    empty/malformed census is fail-closed because inventory completeness would be
    unknown.
    """

    try:
        output = runner(["docker", "top", container_id, "-eo", "comm=,args="])
    except Exception as exc:  # caller maps this into its own fail-closed error type
        raise ProcessCensusError("docker_top_failed") from exc

    rows = [line.strip() for line in output.splitlines() if line.strip()]
    if not rows:
        raise ProcessCensusError("docker_top_empty")

    for line in rows:
        parts = line.split(None, 1)
        comm = parts[0]
        args = parts[1] if len(parts) == 2 else ""
        if _official_hint(comm, args):
            return True
    return False
