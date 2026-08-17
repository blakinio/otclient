#!/usr/bin/env python3
from __future__ import annotations

import json
import os
from pathlib import Path
import subprocess
import sys
import time


def git(*args: str) -> str:
    run = subprocess.run(["git", *args], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if run.returncode:
        print(run.stderr, file=sys.stderr)
        raise SystemExit(run.returncode)
    return run.stdout.strip()


def main() -> int:
    mode = os.environ.get("FAKE_WORKER_MODE", "success")
    request = json.loads(sys.stdin.read())
    if mode == "malformed":
        print("not-json")
        return 0
    if mode == "nonzero":
        print("fixture failure", file=sys.stderr)
        return 3
    if mode == "timeout":
        time.sleep(3)
        return 0

    owned = request.get("owned_paths") or []
    first = str(owned[0]) if owned else "fixture/**"
    if mode == "escape":
        changed = "outside.txt"
    elif first.endswith("/**"):
        changed = first[:-3].rstrip("/") + "/worker.txt"
    else:
        changed = first
    path = Path(changed)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("deterministic external worker fixture\n", encoding="utf-8")

    if mode == "dirty":
        head = git("rev-parse", "HEAD")
    else:
        git("config", "user.name", "orchestrator-fixture")
        git("config", "user.email", "orchestrator-fixture@example.invalid")
        git("add", "--", changed)
        git("commit", "-m", "test: deterministic external worker fixture")
        head = git("rev-parse", "HEAD")

    if mode == "head_mismatch":
        head = "f" * 40

    result = {
        "schema_version": 1,
        "task_id": request["task_id"],
        "branch": request["branch"],
        "base_sha": request["base_sha"],
        "head_sha": head,
        "status": "completed",
        "changed_paths": [changed],
        "validation": [
            {
                "command": "deterministic external worker fixture",
                "result": "PASS",
                "evidence": "fake-real-worker",
            }
        ],
        "evidence": ["fake-real-worker:committed"],
        "context": {
            "pressure": "low",
            "growth": "stable",
            "score": 1,
            "provider_remaining_ratio": None,
        },
        "next_action": "none",
    }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
