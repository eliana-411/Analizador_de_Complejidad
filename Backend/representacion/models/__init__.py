"""
Modelos de datos para el Agente de Representación Matemática.

Este módulo exporta los modelos Pydantic utilizados para:
- Request: Input del agente
- Response: Output del agente
"""

from .math_request import MathRepresentationRequest
from .math_response import MathRepresentationResponse

__all__ = [
    "MathRepresentationRequest",
    "MathRepresentationResponse",
]
