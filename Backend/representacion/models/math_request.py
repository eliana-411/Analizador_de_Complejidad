"""
Modelo de Request para el Agente de Representación Matemática.

Define la estructura de datos de entrada que el agente recibe desde el workflow.
"""

from pydantic import BaseModel, Field
from typing import Optional
from core.analizador.models.omega_table import OmegaTable


class MathRepresentationRequest(BaseModel):
    """
    Request para el Agente de Representación Matemática.
    
    Este modelo encapsula toda la información necesaria para generar
    las ecuaciones matemáticas desde la Tabla Omega.
    
    Attributes:
        omega_table: Tabla Omega completa con todos los escenarios del algoritmo
        algorithm_name: Nombre identificador del algoritmo
        is_iterative: True si es iterativo, False si es recursivo
    """
    
    omega_table: OmegaTable = Field(
        description="Tabla Universal Omega con escenarios mapeados"
    )
    
    algorithm_name: str = Field(
        description="Nombre del algoritmo analizado"
    )
    
    is_iterative: bool = Field(
        description="True si es iterativo (usa loops), False si es recursivo"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "omega_table": {
                    "algorithm_name": "busquedaLineal",
                    "scenarios": [
                        {
                            "id": "S_k=1",
                            "condition": "A[1] == x",
                            "state": "EXITO_TEMPRANO",
                            "cost_T": "6",
                            "probability_P": "1/n",
                            "line_costs": []
                        }
                    ],
                    "control_variables": ["i", "encontrado"],
                    "metadata": {"is_iterative": True}
                },
                "algorithm_name": "busquedaLineal",
                "is_iterative": True
            }
        }
