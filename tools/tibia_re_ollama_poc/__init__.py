"""Internal runtime-independent helpers for TIBIA-RE local Ollama PoC."""

from .client import (
    Generation,
    InferenceOptions,
    ModelInfo,
    OllamaClient,
    OllamaError,
    OllamaModelError,
    OllamaProtocolError,
    OllamaTransportError,
)
from .core import (
    ContractError,
    InvalidModelOutput,
    NO_ACTION,
    SecretMaterialError,
    build_conclusion_prompt,
    build_proposal_prompt,
    canonical_json,
    deterministic_baseline,
    dispatch_preflight,
    freeze_candidate_set,
    freeze_evidence_bundle,
    parse_conclusion,
    parse_proposal,
    proposal_rubric,
    run_conclusion_trials,
    run_proposal_trials,
    sha256_json,
    validate_secret_safe,
    verify_candidate_set,
    verify_evidence_bundle,
)

__all__ = [name for name in globals() if not name.startswith("_")]
