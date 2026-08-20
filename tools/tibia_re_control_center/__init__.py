"""TIBIA RE Control Center Package A deterministic control core.

Package A is permanently runtime_access:none. Concrete official/Oteryn adapters,
network listeners and operator bypass surfaces are intentionally absent.
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
