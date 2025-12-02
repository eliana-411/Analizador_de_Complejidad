"""
Core - Modulos centrales del sistema
=====================================

Este paquete contiene los componentes fundamentales del sistema:
- state.py: Estado global compartido por el workflow
- schemas.py: Modelos de validacion con Pydantic

Uso:
----
    from core.state import GlobalState, create_initial_state
    from core.schemas import AnalysisRequest, AnalysisResponse
"""

from .state import GlobalState, create_initial_state, update_state
from .schemas import (
    # Input/Output API
    AnalysisRequest,
    AnalysisResponse,
    ErrorResponse,

    # Agent outputs
    ValidationResult,
    ComplexityAnalysis,
    MathRepresentation,
    ResolutionResult,
    AsymptoticNotation,
    FinalReport,

    # Internal schemas
    ScenarioCost,
    TechniqueInfo,

    # Utilities
    validate_asymptotic_notation,
)

__all__ = [
    # State
    "GlobalState",
    "create_initial_state",
    "update_state",

    # API Schemas
    "AnalysisRequest",
    "AnalysisResponse",
    "ErrorResponse",

    # Agent Output Schemas
    "ValidationResult",
    "ComplexityAnalysis",
    "MathRepresentation",
    "ResolutionResult",
    "AsymptoticNotation",
    "FinalReport",

    # Internal Schemas
    "ScenarioCost",
    "TechniqueInfo",

    # Utilities
    "validate_asymptotic_notation",
]