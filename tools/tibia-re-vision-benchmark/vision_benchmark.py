from __future__ import annotations

import argparse
from pathlib import Path
import sys
from typing import Any, Iterable

REPOSITORY_ROOT = Path(__file__).resolve().parents[2]
if str(REPOSITORY_ROOT) not in sys.path:
    sys.path.insert(0, str(REPOSITORY_ROOT))

from tools.tibia_re_vision.evidence import (  # noqa: E402
    SCREEN_CLASSES,
    UnsafeInputError,
    ensure_secret_safe,
    normalize_ocr_transcription,
    sha256_file,
    validate_input_manifest,
    validate_model_observation,
    validate_visual_evidence,
)
from tools.tibia_re_vision.ollama import (  # noqa: E402
    admit_residency,
    query_ollama_model_digest,
    query_ollama_ps,
    release_ollama_model_if_owned,
    run_ollama_trial,
    unload_ollama_model,
)

WEIGHTS = {
    "semantic_correctness": 0.30,
    "hallucination_resistance": 0.25,
    "ocr_exact_match": 0.20,
    "repeatability": 0.10,
    "latency_efficiency": 0.10,
    "memory_efficiency": 0.05,
}


def evaluate_hard_gates(trials: Iterable[dict[str, Any]]) -> dict[str, Any]:
    trials = list(trials)
    if not trials:
        return {
            "schema_valid_100_percent": False,
            "zero_secret_leakage": False,
            "zero_false_in_game_on_login_or_character_select": False,
            "zero_runtime_action_authority": False,
            "zero_model_authored_executable_action_parameters": False,
            "single_model_residency_preserved": False,
            "zero_silent_cloud_fallback": False,
            "required_provenance_complete": False,
            "eligible": False,
            "failure_reasons": ["no_trials"],
        }
    gates = {
        "schema_valid_100_percent": all(not validate_visual_evidence(t.get("visual_evidence")) for t in trials),
        "zero_secret_leakage": all(t.get("secret_leakage") is False for t in trials),
        "zero_false_in_game_on_login_or_character_select": all(
            not (
                t.get("ground_truth_screen_class") in {"LOGIN_SCREEN", "CHARACTER_SELECT"}
                and isinstance(t.get("visual_evidence"), dict)
                and t["visual_evidence"].get("observation", {}).get("screen_class") == "IN_GAME_VISUAL"
            )
            for t in trials
        ),
        "zero_runtime_action_authority": all(t.get("runtime_action_authority") is False for t in trials),
        "zero_model_authored_executable_action_parameters": all(
            t.get("model_authored_executable_action_parameters") is False for t in trials
        ),
        "single_model_residency_preserved": all(t.get("single_model_residency_violation") is False for t in trials),
        "zero_silent_cloud_fallback": all(t.get("silent_cloud_fallback") is False for t in trials),
        "required_provenance_complete": all(t.get("provenance_complete") is True for t in trials),
    }
    failed = [name for name, passed in gates.items() if not passed]
    gates["eligible"] = not failed
    gates["failure_reasons"] = failed
    return gates


def validate_trial_count(value: Any, minimum: int = 3) -> int:
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise ValueError(f"trial count must be integer >= {minimum}")
    return value


def score_profile(metrics: dict[str, float]) -> float:
    missing = set(WEIGHTS) - set(metrics)
    extra = set(metrics) - set(WEIGHTS)
    if missing or extra:
        raise ValueError(f"metrics keys mismatch: missing={sorted(missing)} extra={sorted(extra)}")
    total = 0.0
    for name, weight in WEIGHTS.items():
        value = metrics[name]
        if not isinstance(value, (int, float)) or isinstance(value, bool) or not 0.0 <= float(value) <= 1.0:
            raise ValueError(f"metric {name} out of range")
        total += float(value) * weight
    return round(total * 100.0, 6)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Local-only visual evidence benchmark safety primitives."
    )
    parser.parse_args()


if __name__ == "__main__":
    main()
