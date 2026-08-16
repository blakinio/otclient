#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(label: str, text: str, needles: tuple[str, ...]) -> None:
    missing = [needle for needle in needles if needle not in text]
    if missing:
        raise SystemExit(f"{label}: missing mandatory Track A governance markers: {missing}")


def forbid(label: str, text: str, needles: tuple[str, ...]) -> None:
    present = [needle for needle in needles if needle in text]
    if present:
        raise SystemExit(f"{label}: forbidden/stale Track A governance markers present: {present}")


def main() -> int:
    agents = read("docs/agents/AGENTS.md")
    tracks = read("docs/agents/TIBIA_RESEARCH_TRACKS.md")
    admission = read("docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md")
    canonical = read("docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md")

    exact_fence = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
    registration = "/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json"

    require(
        "docs/agents/AGENTS.md",
        agents,
        (
            "contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md",
            "classify `runtime_access`",
            "missing registration means bootstrap",
            "generation mismatch means reviewed rebind",
            "Gate A + any required rebind + Gate B",
            "Historical `:98`, `6082`, PID/session evidence is never current authority",
            "Stale task/PR wording cannot relax this admission gate",
        ),
    )

    require(
        "docs/agents/TIBIA_RESEARCH_TRACKS.md",
        tracks,
        (
            "tibia_research_tracks_policy_version: 5",
            "Gate A — authoritative lease and final cancellation-safe whole-lifetime supervisor",
            "Registration generation rebind — fail closed before Gate B",
            "Gate B — authoritative exact-runtime registration and fresh preflight",
            "Initial creation/bootstrap — separate fail-closed transition",
            "display_98_current_canonical_status: UNKNOWN",
            "rfb_6082_current_backend_mapping: UNKNOWN",
            "current_exact_client_pid: NOT_REGISTERED",
            "current_exact_client_session: NOT_REGISTERED",
            exact_fence,
        ),
    )

    require(
        "TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md",
        admission,
        (
            "track_a_runtime_agent_admission_version: 1",
            "runtime_access: none | read_only | ephemeral_isolated | canonical_reuse_or_mutation | canonical_bootstrap | canonical_rebind",
            "mutation_authorized: true | false",
            "An `UNKNOWN`, `REQUIRED_NOT_PROVEN`, `REQUIRED_UNAVAILABLE`, or `REQUIRED_UNIMPLEMENTED` value on a required gate means **REFUSE the mutation**.",
            "### 1. `none`",
            "### 2. `read_only`",
            "### 3. `ephemeral_isolated`",
            "### 4. `canonical_reuse_or_mutation`",
            "### 5. `canonical_bootstrap`",
            "### 6. `canonical_rebind`",
            "bootstrap: REQUIRED_UNIMPLEMENTED",
            "generation_rebind: REQUIRED_UNAVAILABLE",
            "Manual edits to `runtime-registration.json` are forbidden as a rebind substitute.",
            "display_98_current_canonical_status: UNKNOWN",
            "rfb_6082_current_backend_mapping: UNKNOWN",
            "current_exact_client_pid: NOT_REGISTERED",
            "current_exact_client_session: NOT_REGISTERED",
            "PR #303",
            "Track B never shares Track A's canonical lease",
            registration,
            exact_fence,
            "### PASS — static P2 worker",
            "### PASS — isolated startup experiment",
            "### REFUSE — historical display shortcut",
            "### REFUSE — missing-registration shortcut",
            "### REFUSE — generation mismatch shortcut",
            "### Boundary — read-only evidence",
        ),
    )

    require(
        "OTCLIENT_TIBIA_RE_CANONICAL.md",
        canonical,
        (
            "prompt_contract_version: 1.2.0",
            "track_a_runtime_agent_admission_version: 1",
            "docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md",
            "none\nread_only\nephemeral_isolated\ncanonical_reuse_or_mutation\ncanonical_bootstrap\ncanonical_rebind",
            "Gate A passes, any required generation rebind passes, Gate B passes",
            "Missing registration does not fall through to reuse",
            "Registration/lease-generation mismatch does not fall through to reuse",
            "Manual editing of `runtime-registration.json` is never a substitute.",
            "display_98_current_canonical_status: UNKNOWN",
            "rfb_6082_current_backend_mapping: UNKNOWN",
            "current_exact_client_pid: NOT_REGISTERED",
            "current_exact_client_session: NOT_REGISTERED",
            "Do not mutate PR #303-owned runtime surfaces or Track B state",
        ),
    )

    forbid(
        "OTCLIENT_TIBIA_RE_CANONICAL.md",
        canonical,
        (
            "display_98_current_canonical_status: PROVEN",
            "rfb_6082_current_backend_mapping: PROVEN",
            "current_exact_client_pid: REGISTERED",
            "current_exact_client_session: REGISTERED",
        ),
    )

    print("TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
