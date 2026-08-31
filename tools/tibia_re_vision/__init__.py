"""Reusable, non-authoritative local vision evidence and Ollama safety primitives."""

from .evidence import (
    SCREEN_CLASSES,
    UnsafeInputError,
    ensure_secret_safe,
    normalize_ocr_transcription,
    sha256_file,
    validate_input_manifest,
    validate_model_observation,
    validate_visual_evidence,
)
from .ollama import (
    admit_residency,
    query_ollama_model_digest,
    query_ollama_ps,
    release_ollama_model_if_owned,
    run_ollama_trial,
    unload_ollama_model,
)

__all__ = [
    "SCREEN_CLASSES",
    "UnsafeInputError",
    "admit_residency",
    "ensure_secret_safe",
    "normalize_ocr_transcription",
    "query_ollama_model_digest",
    "query_ollama_ps",
    "release_ollama_model_if_owned",
    "run_ollama_trial",
    "sha256_file",
    "unload_ollama_model",
    "validate_input_manifest",
    "validate_model_observation",
    "validate_visual_evidence",
]
