#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[2]
TRACK_A = "official-client-re"
CANONICAL_NAMESPACE = "canonical-live-runtime"
CANONICAL_STATE_ROOT = "/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime"
CANONICAL_RUNTIME_ACCESS = {
    "canonical_reuse_or_mutation",
    "canonical_bootstrap",
    "canonical_rebind",
}

ADMISSION_FIELDS = (
    "runtime_access",
    "runtime_owner_task",
    "runtime_namespace",
    "canonical_registration",
    "canonical_lease_generation",
    "registration_lease_generation",
    "gate_a",
    "generation_rebind",
    "gate_b",
    "bootstrap",
    "target_uniqueness",
    "mutation_authorized",
)

RUNTIME_ACCESS_VALUES = {
    "none",
    "read_only",
    "ephemeral_isolated",
    *CANONICAL_RUNTIME_ACCESS,
}

TRACK_A_SENSITIVE_PREFIXES = (
    ".github/scripts/tibia-official-client-re-",
    ".github/workflows/tibia-official-client-re-",
    "tools/tibia_runtime_bridge/",
    "tools/tibia_worldmap_reconstruction/",
)

BOOTSTRAP_TRANSITION = ".github/scripts/tibia-official-client-re-canonical-live-transition.py"
BOOTSTRAP_ARCHIVE = "docs/agents/tasks/archive/OTC-20260816-track-a-canonical-bootstrap-implementation.md"
BOOTSTRAP_MERGE = "d16091ca29ff7c9330115e9ce0fdbfb41646e0dc"


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


def parse_frontmatter(path: Path) -> dict[str, str]:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        raise SystemExit(f"{path}: task file has no YAML front matter")

    values: dict[str, str] = {}
    for line in lines[1:]:
        if line.strip() == "---":
            return values
        match = re.fullmatch(r"([A-Za-z0-9_]+):\s*(.*)", line)
        if not match:
            continue
        value = match.group(2).strip()
        if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
            value = value[1:-1]
        values[match.group(1)] = value
    raise SystemExit(f"{path}: unterminated YAML front matter")


def fail_task(path: Path, message: str) -> None:
    raise SystemExit(f"{path}: Track A runtime admission invalid: {message}")


def positive_generation(path: Path, values: dict[str, str], field: str) -> int:
    value = values[field]
    if not re.fullmatch(r"[1-9][0-9]*", value):
        fail_task(path, f"{field} must be a positive integer, got {value!r}")
    return int(value)


def is_canonical_namespace(value: str) -> bool:
    normalized = value.rstrip("/")
    return normalized in {CANONICAL_NAMESPACE, CANONICAL_STATE_ROOT}


def task_matches_expected_branch(values: dict[str, str], expected_branch: str | None) -> bool:
    return bool(expected_branch and values.get("branch") == expected_branch)


def bootstrap_implementation_promoted() -> bool:
    transition_path = ROOT / BOOTSTRAP_TRANSITION
    archive_path = ROOT / BOOTSTRAP_ARCHIVE
    if not transition_path.is_file() or not archive_path.is_file():
        return False
    transition = transition_path.read_text(encoding="utf-8")
    archive = archive_path.read_text(encoding="utf-8")
    transition_markers = (
        '"""Cancellation-safe Track A canonical bootstrap, rebind and Gate B."""',
        "def _bootstrap(",
        "def _rebind(",
        "def _gateb(",
        "fcntl.flock(lock_fd, fcntl.LOCK_EX)",
        "[str(args.worker), 'bootstrap', str(manifest_path)]",
        "_commit(staged)",
        "_candidates()",
    )
    archive_markers = (
        "task_id: OTC-20260816-track-a-canonical-bootstrap-implementation",
        "status: completed",
        "implementation_pr: 371",
        f"implementation_merge_commit: {BOOTSTRAP_MERGE}",
        "ownership_released: true",
        "consumer_next_action: refresh OTC-20260816-track-a-canonical-runtime-e2e from trusted main and perform fresh RUNTIME admission before any physical bootstrap or login",
    )
    return all(marker in transition for marker in transition_markers) and all(
        marker in archive for marker in archive_markers
    )


def validate_track_a_task(path: Path) -> bool:
    values = parse_frontmatter(path)
    if values.get("track_id") != TRACK_A:
        return False

    missing = [field for field in ADMISSION_FIELDS if not values.get(field)]
    if missing:
        fail_task(path, f"missing admission fields {missing}")

    runtime_access = values["runtime_access"]
    if runtime_access not in RUNTIME_ACCESS_VALUES:
        fail_task(path, f"unsupported runtime_access={runtime_access!r}")

    mutation = values["mutation_authorized"]
    if mutation not in {"true", "false"}:
        fail_task(path, "mutation_authorized must be true or false")

    if values["gate_a"] not in {"PASS", "REQUIRED_NOT_PROVEN", "NOT_APPLICABLE"}:
        fail_task(path, f"invalid gate_a={values['gate_a']!r}")
    if values["generation_rebind"] not in {
        "PASS",
        "REQUIRED_UNAVAILABLE",
        "REQUIRED_NOT_PROVEN",
        "NOT_APPLICABLE",
    }:
        fail_task(path, f"invalid generation_rebind={values['generation_rebind']!r}")
    if values["gate_b"] not in {"PASS", "REQUIRED_NOT_PROVEN", "NOT_APPLICABLE"}:
        fail_task(path, f"invalid gate_b={values['gate_b']!r}")
    if values["bootstrap"] not in {
        "PASS",
        "REQUIRED_UNIMPLEMENTED",
        "REQUIRED_NOT_PROVEN",
        "NOT_APPLICABLE",
    }:
        fail_task(path, f"invalid bootstrap={values['bootstrap']!r}")
    if values["canonical_registration"] not in {"ABSENT", "PRESENT", "UNKNOWN", "NOT_APPLICABLE"}:
        fail_task(path, f"invalid canonical_registration={values['canonical_registration']!r}")
    if values["target_uniqueness"] not in {"PROVEN", "UNKNOWN", "NOT_APPLICABLE"}:
        fail_task(path, f"invalid target_uniqueness={values['target_uniqueness']!r}")

    task_id = values.get("task_id")
    if runtime_access in CANONICAL_RUNTIME_ACCESS:
        if not task_id or values["runtime_owner_task"] != task_id:
            fail_task(path, "canonical runtime_owner_task must equal the current task_id")
        if not is_canonical_namespace(values["runtime_namespace"]):
            fail_task(path, "canonical runtime access must use the authoritative canonical namespace")

    canonical_gates = ("gate_a", "generation_rebind", "gate_b", "bootstrap")

    if runtime_access == "none":
        if mutation != "false":
            fail_task(path, "runtime_access=none cannot authorize mutation")
        for field in canonical_gates:
            if values[field] != "NOT_APPLICABLE":
                fail_task(path, f"runtime_access=none requires {field}=NOT_APPLICABLE")
        if values["canonical_registration"] != "NOT_APPLICABLE":
            fail_task(path, "runtime_access=none requires canonical_registration=NOT_APPLICABLE")
        if values["target_uniqueness"] != "NOT_APPLICABLE":
            fail_task(path, "runtime_access=none requires target_uniqueness=NOT_APPLICABLE")

    elif runtime_access == "read_only":
        if mutation != "false":
            fail_task(path, "read_only can never authorize mutation")
        for field in canonical_gates:
            if values[field] != "NOT_APPLICABLE":
                fail_task(path, f"read_only requires {field}=NOT_APPLICABLE")
        if values["target_uniqueness"] != "PROVEN":
            fail_task(path, "read_only live observation requires target_uniqueness=PROVEN")
        namespace = values["runtime_namespace"]
        if namespace in {"UNKNOWN", "NOT_APPLICABLE"}:
            fail_task(path, "read_only live observation requires an explicit non-conflicting runtime_namespace")
        owner = values["runtime_owner_task"]
        if owner not in {"NOT_APPLICABLE", task_id}:
            fail_task(path, "read_only cannot observe another task's owned runtime surface")

    elif runtime_access == "ephemeral_isolated":
        for field in canonical_gates:
            if values[field] != "NOT_APPLICABLE":
                fail_task(path, f"ephemeral_isolated requires canonical {field}=NOT_APPLICABLE")
        if values["canonical_registration"] != "NOT_APPLICABLE":
            fail_task(path, "ephemeral_isolated cannot use canonical registration")
        if values["runtime_owner_task"] != task_id:
            fail_task(path, "ephemeral_isolated runtime_owner_task must equal task_id")
        namespace = values["runtime_namespace"]
        if namespace in {"UNKNOWN", "NOT_APPLICABLE"}:
            fail_task(path, "ephemeral_isolated requires a proven task-owned runtime_namespace")
        if "canonical-live-runtime" in namespace:
            fail_task(path, "ephemeral_isolated cannot use or alias the reserved canonical namespace")
        if mutation == "true" and values["target_uniqueness"] != "PROVEN":
            fail_task(path, "ephemeral mutation requires target_uniqueness=PROVEN")

    elif runtime_access == "canonical_reuse_or_mutation":
        if values["canonical_registration"] != "PRESENT":
            fail_task(path, "canonical reuse requires authoritative registration PRESENT")
        if mutation == "true":
            required = {
                "gate_a": "PASS",
                "gate_b": "PASS",
                "bootstrap": "NOT_APPLICABLE",
                "target_uniqueness": "PROVEN",
            }
            for field, expected in required.items():
                if values[field] != expected:
                    fail_task(path, f"authorized canonical mutation requires {field}={expected}")
            if values["generation_rebind"] not in {"PASS", "NOT_APPLICABLE"}:
                fail_task(path, "authorized canonical mutation requires rebind PASS or NOT_APPLICABLE")
            lease_generation = positive_generation(path, values, "canonical_lease_generation")
            registration_generation = positive_generation(path, values, "registration_lease_generation")
            if lease_generation != registration_generation:
                fail_task(
                    path,
                    "authorized canonical mutation requires registration_lease_generation "
                    "to equal canonical_lease_generation after any required rebind",
                )

    elif runtime_access == "canonical_bootstrap":
        if values["canonical_registration"] not in {"ABSENT", "UNKNOWN"}:
            fail_task(path, "bootstrap admission requires registration ABSENT or UNKNOWN")
        if values["generation_rebind"] != "NOT_APPLICABLE":
            fail_task(path, "bootstrap cannot use generation rebind")
        if values["gate_b"] != "NOT_APPLICABLE":
            fail_task(path, "bootstrap cannot use ordinary Gate B")

        if mutation == "false":
            if values["bootstrap"] not in {
                "REQUIRED_UNIMPLEMENTED",
                "REQUIRED_NOT_PROVEN",
                "PASS",
            }:
                fail_task(path, "fail-closed bootstrap checkpoint has invalid bootstrap state")
        else:
            if not bootstrap_implementation_promoted():
                fail_task(path, "reviewed canonical bootstrap implementation is not present on trusted base")
            required = {
                "canonical_registration": "ABSENT",
                "canonical_lease_generation": "UNKNOWN",
                "registration_lease_generation": "NOT_APPLICABLE",
                "gate_a": "REQUIRED_NOT_PROVEN",
                "generation_rebind": "NOT_APPLICABLE",
                "gate_b": "NOT_APPLICABLE",
                "bootstrap": "PASS",
                "target_uniqueness": "UNKNOWN",
                "bootstrap_attempt_limit": "1",
                "credentials_allowed": "false",
                "login_allowed": "false",
                "gameplay_allowed": "false",
            }
            for field, expected in required.items():
                if values.get(field) != expected:
                    fail_task(path, f"authorized bootstrap transaction requires {field}={expected}")
            source = values.get("live_runtime_authorization_source", "").strip()
            if not source or source.upper() in {"NONE", "NOT_APPLICABLE", "UNKNOWN"}:
                fail_task(path, "authorized bootstrap transaction requires explicit live_runtime_authorization_source")

    elif runtime_access == "canonical_rebind":
        if mutation != "false":
            fail_task(path, "rebind is metadata authority transition, not client mutation authority")
        if values["canonical_registration"] != "PRESENT":
            fail_task(path, "rebind requires an existing authoritative registration")
        if values["generation_rebind"] not in {"REQUIRED_UNAVAILABLE", "REQUIRED_NOT_PROVEN"}:
            fail_task(path, "current task-level rebind admission remains fail-closed")
        if values["bootstrap"] != "NOT_APPLICABLE":
            fail_task(path, "rebind cannot use bootstrap")
        lease_generation = positive_generation(path, values, "canonical_lease_generation")
        registration_generation = positive_generation(path, values, "registration_lease_generation")
        if lease_generation == registration_generation:
            fail_task(path, "canonical_rebind requires a real older registration generation mismatch")

    return True


def changed_paths(base: str) -> list[str]:
    completed = subprocess.run(
        ["git", "diff", "--name-only", "--diff-filter=ACMR", f"{base}...HEAD"],
        cwd=ROOT,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def audit_changed_tasks(base: str, expected_branch: str | None = None) -> None:
    paths = changed_paths(base)
    task_paths = [
        path
        for path in paths
        if path.startswith("docs/agents/tasks/active/") and path.endswith(".md")
    ]

    track_a_tasks = 0
    branch_bound_tasks = 0
    for relative in task_paths:
        path = ROOT / relative
        values = parse_frontmatter(path)
        if values.get("track_id") != TRACK_A:
            continue
        validate_track_a_task(path)
        track_a_tasks += 1
        if task_matches_expected_branch(values, expected_branch):
            branch_bound_tasks += 1

    sensitive = [path for path in paths if path.startswith(TRACK_A_SENSITIVE_PREFIXES)]
    if sensitive:
        if not expected_branch:
            raise SystemExit(
                "Track A runtime-sensitive files changed but the current PR head branch "
                "was not supplied to the admission audit"
            )
        if branch_bound_tasks == 0:
            raise SystemExit(
                "Track A runtime-sensitive files changed without an added/modified active "
                "Track A admission task bound to the current PR head branch "
                f"{expected_branch!r}: {sensitive}"
            )

    print(f"TRACK_A_AGENT_RUNTIME_CHANGED_TASKS={track_a_tasks}")
    print(f"TRACK_A_AGENT_RUNTIME_BRANCH_BOUND_TASKS={branch_bound_tasks}")


def static_policy_audit() -> None:
    readme = read("docs/agents/README.md")
    agents = read("docs/agents/AGENTS.md")
    tracks = read("docs/agents/TIBIA_RESEARCH_TRACKS.md")
    admission = read("docs/agents/contracts/TRACK_A_RUNTIME_AGENT_ADMISSION_V1.md")
    canonical = read("docs/agents/prompts/OTCLIENT_TIBIA_RE_CANONICAL.md")

    exact_fence = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"
    exact_size = "52109920"
    exact_version = "15.32"
    historical_fence = "e6c244bd39fe2e0632f6f000efd3147164696efa8e901718668e0442325ff7fe"
    registration = "/home/runner/_work/_otclient_tibia_re_state/canonical-live-runtime/runtime-registration.json"

    require(
        "docs/agents/README.md",
        readme,
        (
            "at task claim/resume before substantial Track A work",
            "At claim/resume/checkpoint, the active Track A task must persist",
            "runtime_access: none",
            "target_uniqueness: PROVEN",
            "read_only",
            "PR #303-owned state",
        ),
    )
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
            "tibia_research_tracks_policy_version: 6",
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
            "At Track A task claim/resume/checkpoint",
            "runtime_access: none | read_only | ephemeral_isolated | canonical_reuse_or_mutation | canonical_bootstrap | canonical_rebind",
            "target_uniqueness: PROVEN",
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
            "### PASS — bounded read-only live observation",
            "### REFUSE — historical display shortcut",
            "### REFUSE — missing-registration shortcut",
            "### REFUSE — generation mismatch shortcut",
            "### REFUSE — ambiguous read-only target",
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
            "At task claim/resume/checkpoint",
            "target_uniqueness: PROVEN",
            "Gate A passes, any required generation rebind passes, Gate B passes",
            "Missing registration does not fall through to reuse",
            "Registration/lease-generation mismatch does not fall through to reuse",
            "Manual editing of `runtime-registration.json` is never a substitute.",
            "display_98_current_canonical_status: UNKNOWN",
            "rfb_6082_current_backend_mapping: UNKNOWN",
            "current_exact_client_pid: NOT_REGISTERED",
            "current_exact_client_session: NOT_REGISTERED",
            "Do not mutate or live-observe PR #303-owned runtime surfaces",
        ),
    )
    require(
        "promoted bootstrap implementation",
        read(BOOTSTRAP_TRANSITION),
        (
            '"""Cancellation-safe Track A canonical bootstrap, rebind and Gate B."""',
            "def _bootstrap(",
            "def _rebind(",
            "def _gateb(",
            "fcntl.flock(lock_fd, fcntl.LOCK_EX)",
        ),
    )
    require(
        "bootstrap implementation archive",
        read(BOOTSTRAP_ARCHIVE),
        (
            "status: completed",
            "implementation_pr: 371",
            f"implementation_merge_commit: {BOOTSTRAP_MERGE}",
            "ownership_released: true",
        ),
    )
    if not bootstrap_implementation_promoted():
        raise SystemExit("trusted bootstrap implementation/archive proof is incomplete")

    for label, text in (
        ("tracks current fence", tracks),
        ("admission current fence", admission),
        ("bootstrap current fence", read("docs/agents/contracts/TRACK_A_CANONICAL_LIVE_BOOTSTRAP_V1.md")),
        ("ADR current fence", read("docs/agents/decisions/ADR-0001-track-a-canonical-live-runtime.md")),
    ):
        require(label, text, (exact_fence, exact_size, exact_version))

    transition = read(BOOTSTRAP_TRANSITION)
    session = read(".github/scripts/tibia-official-client-re-canonical-live-session.sh")
    require("current canonical transition fence", transition, ("VER = '15.32'", "SIZE = 52109920", "SHA = 'ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8'"))
    require("current canonical live-session fence", session, ("SIZE=52109920", "SHA=ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"))
    forbid("current canonical enforcement", transition + session, (historical_fence, "SIZE=51965216", "SIZE = 51965216"))

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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--changed-from", help="audit added/modified active tasks relative to this git ref")
    parser.add_argument("--expected-branch", help="require runtime-sensitive admission task to match this PR head branch")
    args = parser.parse_args()

    static_policy_audit()
    if args.changed_from:
        audit_changed_tasks(args.changed_from, args.expected_branch)

    print("TRACK_A_AGENT_RUNTIME_GOVERNANCE_PASS=true")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
