"""
Modelo para información de recursión en algoritmos recursivos.

Define la estructura RecursionInfo que almacena información sobre
la estructura recursiva de un algoritmo.
"""

from pydantic import BaseModel, Field
from typing import List


class RecursionInfo(BaseModel):
    """
    Información sobre la estructura recursiva de un algoritmo.

    Almacena:
    - Número de llamadas recursivas por invocación
    - Patrones de transformación de parámetros
    - Información del caso base
    - Tipo de recurrencia
    """
    num_calls: int = Field(
        description="Número de llamadas recursivas por invocación (1 para factorial, 2 para quicksort)"
    )
    call_pattern: List[str] = Field(
        default_factory=list,
        description="Lista de transformaciones de parámetros (ej: ['n-1'], ['n/2', 'n/2'])"
    )
    base_case_condition: str = Field(
        default="n == 0",
        description="Condición del caso base (ej: 'n == 0', 'p >= r')"
    )
    base_case_cost: str = Field(
        default="1",
        description="Costo del caso base (usualmente constante)"
    )
    recurrence_type: str = Field(
        default="subtract",
        description="Tipo de recurrencia: 'subtract' (n-1), 'divide' (n/2), 'mixed'"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "num_calls": 2,
                "call_pattern": ["n/2", "n/2"],
                "base_case_condition": "n <= 1",
                "base_case_cost": "1",
                "recurrence_type": "divide"
            }
        }
