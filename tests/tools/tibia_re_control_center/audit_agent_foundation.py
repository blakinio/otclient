"""Static, offline security audit for the local agent foundation."""

from __future__ import annotations

import ast
import re
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

EXPECTED_MODEL = "qwen3-vl:4b-instruct-q4_K_M"
EXPECTED_DIGEST = "ee4b975b58c17ce268cd19d40db35d5edc64603035d2ffc1fee1968eb0947f7b"
EXPECTED_PROFILE = f"ollama:{EXPECTED_MODEL}@sha256:{EXPECTED_DIGEST}"
EXPECTED_MCP_TOOLS = (
    "agent_session_status",
    "agent_submit_task",
    "agent_control",
    "agent_events",
    "agent_result",
)
EXPECTED_OFFICIAL_CLIENT_SHA256 = "ed5469b9fa71349de688f719434d23875f76f28a3ebd08a36d30f7f6da0af6b8"

PRODUCTION_ROOTS = (
    ROOT / "tools" / "tibia_re_control_center",
    ROOT / "tools" / "tibia_re_vision",
)
FORBIDDEN_TEXT = (
    "xdotool",
    "pyautogui",
    "docker exec",
    "/proc/",
    "cua_repl",
)
SECRET_COLUMN_NAMES = (
    "password",
    "passwd",
    "access_token",
    "refresh_token",
    "session_token",
    "credential",
    "private_key",
)


def _source(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def _production_files() -> list[Path]:
    return sorted(
        path
        for root in PRODUCTION_ROOTS
        for path in root.rglob("*.py")
        if path.is_file()
    )


def _forbidden_violations(path: Path, source: str) -> list[str]:
    violations: list[str] = []
    lowered = source.casefold()
    for token in FORBIDDEN_TEXT:
        if token.casefold() in lowered:
            violations.append(f"{path} exposes forbidden {token!r}")
    if re.search(r"\bshell\s*=\s*True\b", source):
        violations.append(f"{path} enables shell=True")
    if re.search(r"\bget_secret\s*\(", source):
        violations.append(f"{path} exposes generic get_secret")
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        return violations + [f"{path} does not parse: {exc.msg}"]
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and node.id in {"__import__", "eval", "exec"}:
            violations.append(f"{path} exposes dynamic import machinery")
        if isinstance(node, ast.Constant) and node.value == "__import__":
            violations.append(f"{path} exposes dynamic import machinery")
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imported = (
                [alias.name for alias in node.names]
                if isinstance(node, ast.Import)
                else [node.module or ""]
            )
            if any(name == "subprocess" or name.startswith("subprocess.") for name in imported):
                violations.append(f"{path} introduces subprocess in production agent modules")
            if any(name == "importlib" or name.startswith("importlib.") for name in imported):
                violations.append(f"{path} exposes dynamic import machinery")
            if isinstance(node, ast.ImportFrom) and any(alias.name == "__import__" for alias in node.names):
                violations.append(f"{path} exposes dynamic import machinery")
        if isinstance(node, ast.Call):
            for keyword in node.keywords:
                if (
                    keyword.arg == "shell"
                    and isinstance(keyword.value, ast.Constant)
                    and keyword.value.value is True
                ):
                    violations.append(f"{path} enables shell=True")
            function = node.func
            function_name = function.id if isinstance(function, ast.Name) else None
            attribute_name = function.attr if isinstance(function, ast.Attribute) else None
            if function_name in {"__import__", "eval", "exec"} or attribute_name in {"import_module", "__import__"}:
                violations.append(f"{path} exposes dynamic import machinery")
            if (
                isinstance(function, ast.Name)
                and function.id == "getattr"
                and len(node.args) >= 2
                and isinstance(node.args[0], ast.Name)
                and node.args[0].id == "builtins"
            ):
                violations.append(f"{path} exposes dynamic import machinery")
        if isinstance(node, ast.Subscript) and isinstance(node.value, ast.Attribute):
            if isinstance(node.value.value, ast.Name) and node.value.value.id == "sys" and node.value.attr == "modules":
                violations.append(f"{path} exposes dynamic import machinery")
            if isinstance(node.value.value, ast.Name) and node.value.value.id == "builtins" and node.value.attr == "__dict__":
                violations.append(f"{path} exposes dynamic import machinery")
        if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Name):
            if node.value.id == "sys" and node.attr == "modules":
                violations.append(f"{path} exposes dynamic import machinery")
            if node.value.id == "builtins" and node.attr == "__import__":
                violations.append(f"{path} exposes dynamic import machinery")
    return violations


def audit_forbidden_surfaces() -> None:
    violations: list[str] = []
    for path in _production_files():
        path_violations = _forbidden_violations(path.relative_to(ROOT), _source(path))
        violations.extend(path_violations)
    dynamic_sources = (
        "import importlib\nimportlib.import_module('subprocess')",
        "loader = __import__\nloader('subprocess')",
        "import sys\nsys.modules['subprocess']",
        "import builtins\nname = '__' + 'import__'\ngetattr(builtins, name)('subprocess')",
    )
    for source in dynamic_sources:
        if not _forbidden_violations(Path("dynamic-subprocess.py"), source):
            raise AssertionError("dynamic subprocess import bypassed the production surface audit")
    if violations:
        raise AssertionError("forbidden production surface(s): " + "; ".join(violations))


def audit_no_credential_persistence() -> None:
    store_path = ROOT / "tools" / "tibia_re_control_center" / "persistent_store.py"
    source = _source(store_path)
    ddl = "\n".join(line for line in source.splitlines() if "CREATE TABLE" in line)
    for name in SECRET_COLUMN_NAMES:
        if re.search(rf"\b{name}\b", ddl, flags=re.IGNORECASE):
            raise AssertionError(f"persistent schema exposes credential column {name!r}")
    if "def _ensure_persistable" not in source or "SECRET_MATERIAL_REJECTED" not in source:
        raise AssertionError("persistent store is missing its secret rejection guard")
    agent_source = _source(ROOT / "tools" / "tibia_re_control_center" / "agent_session.py")
    if "ensure_no_secret_material(asdict(parsed_input), key_path=\"agent_task\")" not in agent_source:
        raise AssertionError("agent task persistence is not guarded before durable write")


def audit_exact_model_profile() -> None:
    from tools.tibia_re_control_center.agent_vision import (
        QWEN_NUM_CTX,
        QWEN_NUM_PREDICT,
        QWEN_TEMPERATURE,
        QWEN_VISION_DIGEST,
        QWEN_VISION_MODEL,
        QWEN_VISION_PROFILE_ID,
    )

    assert QWEN_VISION_MODEL == EXPECTED_MODEL
    assert QWEN_VISION_DIGEST == EXPECTED_DIGEST
    assert QWEN_VISION_PROFILE_ID == EXPECTED_PROFILE
    assert (QWEN_NUM_CTX, QWEN_NUM_PREDICT, QWEN_TEMPERATURE) == (4096, 256, 0)
    plan = _source(ROOT / "docs" / "superpowers" / "plans" / "2026-08-30-local-track-a-vision-agent-supervisor.md")
    expected = (
        f"Qwen profile is exactly `{EXPECTED_MODEL}`",
        f"digest `{EXPECTED_DIGEST}`",
        "`num_ctx=4096`, `num_predict=256`, `temperature=0`",
    )
    if any(fragment not in plan for fragment in expected):
        raise AssertionError("Task plan does not retain the exact Qwen profile")


def _require_imported_calls(path: Path, source: str, required: set[str]) -> None:
    try:
        tree = ast.parse(source, filename=str(path))
    except SyntaxError as exc:
        raise AssertionError(f"{path} does not parse") from exc
    bindings: dict[str, str] = {}
    for node in tree.body:
        if not isinstance(node, ast.ImportFrom) or node.module != "tools.tibia_re_vision.evidence":
            continue
        for alias in node.names:
            bindings[alias.asname or alias.name] = alias.name
    shadowed = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store) and node.id in bindings:
            shadowed.add(node.id)
        elif isinstance(node, ast.arg) and node.arg in bindings:
            shadowed.add(node.arg)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.name in bindings:
            shadowed.add(node.name)
    if shadowed:
        raise AssertionError(f"{path} shadows imported PR #790 validators: {sorted(shadowed)!r}")
    calls = {
        node.func.id
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    missing_imports = sorted(required - set(bindings.values()))
    missing_calls = sorted(
        symbol for symbol in required
        if not any(local == symbol and local in calls for local, imported in bindings.items() if imported == symbol)
    )
    if missing_imports or missing_calls:
        raise AssertionError(
            f"{path} does not directly import/call PR #790 validators "
            f"(missing_imports={missing_imports!r}, missing_calls={missing_calls!r})"
        )


def audit_reusable_pr790_validation() -> None:
    evidence = ROOT / "tools" / "tibia_re_vision" / "evidence.py"
    benchmark = ROOT / "tools" / "tibia-re-vision-benchmark" / "vision_benchmark.py"
    frozen_tests = ROOT / "tools" / "tibia-re-vision-benchmark" / "tests"
    if not evidence.is_file() or not benchmark.is_file() or not frozen_tests.is_dir():
        raise AssertionError("PR #790 reusable vision benchmark surface is missing")
    evidence_source = _source(evidence)
    evidence_tree = ast.parse(evidence_source, filename=str(evidence))
    definitions = {
        node.name
        for node in ast.walk(evidence_tree)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    required = {"validate_input_manifest", "validate_visual_evidence", "ensure_secret_safe"}
    if not required.issubset(definitions):
        raise AssertionError("PR #790 evidence validators are not defined")
    manifest = next(
        node
        for node in ast.walk(evidence_tree)
        if isinstance(node, ast.FunctionDef) and node.name == "validate_input_manifest"
    )
    manifest_calls = {
        node.func.id
        for node in ast.walk(manifest)
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name)
    }
    if "ensure_secret_safe" not in manifest_calls:
        raise AssertionError("validate_input_manifest no longer enforces secret-safe metadata")

    agent_source = _source(ROOT / "tools" / "tibia_re_control_center" / "agent_vision.py")
    _require_imported_calls(
        ROOT / "tools" / "tibia_re_control_center" / "agent_vision.py",
        agent_source,
        {"validate_input_manifest", "validate_visual_evidence", "ensure_secret_safe"},
    )
    benchmark_source = _source(benchmark)
    _require_imported_calls(benchmark, benchmark_source, {"validate_visual_evidence"})

    try:
        _require_imported_calls(
            Path("comment-only.py"),
            "# validate_visual_evidence(validate_input_manifest(...))",
            {"validate_visual_evidence"},
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("comment-only PR #790 reuse claim was accepted")
    try:
        _require_imported_calls(
            Path("shadowed-validator.py"),
            "from tools.tibia_re_vision.evidence import validate_visual_evidence\n"
            "validate_visual_evidence = lambda _: None\n"
            "validate_visual_evidence({})",
            {"validate_visual_evidence"},
        )
    except AssertionError:
        pass
    else:
        raise AssertionError("shadowed PR #790 validator call was accepted")
    if not list(frozen_tests.glob("test_*.py")):
        raise AssertionError("frozen PR #790 benchmark tests are missing")


def audit_exact_mcp_allowlist() -> None:
    from tools.tibia_re_control_center.agent_mcp import _tools

    names = tuple(item.get("name") for item in _tools())
    if names != EXPECTED_MCP_TOOLS:
        raise AssertionError(f"MCP tool allowlist changed: {names!r}")


def audit_default_null_executor() -> None:
    from tools.tibia_re_control_center.agent_session import NullBoundedActionExecutor
    from tools.tibia_re_control_center.control_domain import ControlDomainService

    with tempfile.TemporaryDirectory() as temporary:
        domain = ControlDomainService(Path(temporary))
        try:
            if type(domain.agent.executor) is not NullBoundedActionExecutor:
                raise AssertionError("production Control Center executor is not the Null executor")
            status = domain.status()
            if status["agent"]["executor"] != "NULL":
                raise AssertionError("production status does not report the Null executor")
            if status["agent"]["mutation_authority"] != "NONE" or status["agent"]["physical_action_budget"] != 0:
                raise AssertionError("production foundation exposes mutation authority")
        finally:
            if not domain.close():
                raise AssertionError("offline default-executor audit could not close the domain")


def audit_official_client_fence_unchanged() -> None:
    source = _source(ROOT / "tools" / "tibia_re_control_center" / "official_adapter.py")
    match = re.search(r"^CURRENT_CLIENT_SHA256\s*=\s*['\"]([0-9a-f]{64})['\"]", source, flags=re.MULTILINE)
    if match is None or match.group(1) != EXPECTED_OFFICIAL_CLIENT_SHA256:
        raise AssertionError("OfficialTibiaAdapter.CURRENT_CLIENT_SHA256 changed under foundation plan")


def main() -> int:
    audit_forbidden_surfaces()
    audit_no_credential_persistence()
    audit_exact_model_profile()
    audit_reusable_pr790_validation()
    audit_exact_mcp_allowlist()
    audit_default_null_executor()
    audit_official_client_fence_unchanged()
    print("AGENT_FOUNDATION_AUDIT=PASS")
    print("RUNTIME_SURFACES=PASS")
    print("AUTHORITY_BOUNDARIES=PASS")
    print("MCP_ALLOWLIST=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
