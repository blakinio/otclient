"""TIBIA RE Control Center deterministic core and local Package B control plane.

Package A remains runtime_access:none and exposes no adapter bypass. Package B adds
non-exported loopback HTTP/CLI/UI modules backed only by the explicit FAKE_TEST adapter;
Official Tibia runtime/client access remains absent.
"""

from .artifact import ArtifactStore
from .comparison import ComparisonProfile, ComparisonResult, compare_runs
from .engine import EngineRunResult, ScenarioEngine
from .execution import CancellationToken, MutationCoordinator
from .model import (
    ActionRequest,
    ActionResult,
    Authority,
    EffectBound,
    SideEffectBudget,
    ValidationError,
)
from .recorder import Recorder
from .scenario import parse_and_validate, validation_result
from .store import DeterministicDurableStore

__all__ = [
    "ActionRequest",
    "ActionResult",
    "ArtifactStore",
    "Authority",
    "CancellationToken",
    "ComparisonProfile",
    "ComparisonResult",
    "DeterministicDurableStore",
    "EffectBound",
    "EngineRunResult",
    "MutationCoordinator",
    "Recorder",
    "ScenarioEngine",
    "SideEffectBudget",
    "ValidationError",
    "compare_runs",
    "parse_and_validate",
    "validation_result",
]
