"""
Estado del Workflow de Mapeo de Escenarios (Fase 2)

Define el estado que fluye a través del workflow de LangGraph
para el análisis de escenarios.
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from core.analizador.models.omega_table import OmegaTable


class ControlVariable(BaseModel):
    """
    Variable que controla el flujo de ejecución del algoritmo.

    Variables de control determinan cuándo termina el algoritmo
    o cuántas iteraciones ejecuta.
    """
    name: str  # Nombre de la variable (ej: "i", "encontrado")
    type: str  # "PRIMARY" | "SECONDARY"
    scope: str  # "loop_index" | "flag" | "counter"
    affects_termination: bool  # ¿Causa salida temprana o modifica iteraciones?

    class Config:
        json_schema_extra = {
            "example": {
                "name": "encontrado",
                "type": "SECONDARY",
                "scope": "flag",
                "affects_termination": True
            }
        }


class LoopInfo(BaseModel):
    """
    Información sobre un loop en el pseudocódigo.

    Usado para determinar frecuencias de ejecución de líneas.
    """
    loop_id: str  # Identificador único del loop
    loop_type: str  # "for" | "while" | "repeat"
    start_line: int  # Línea donde comienza el loop
    end_line: int  # Línea donde termina el loop
    nesting_level: int  # Nivel de anidamiento (0 = top level)
    control_variable: str  # Variable índice del loop
    iterations: str  # Expresión de iteraciones: "n", "n-1", "log(n)", etc.

    class Config:
        json_schema_extra = {
            "example": {
                "loop_id": "loop_0",
                "loop_type": "for",
                "start_line": 2,
                "end_line": 6,
                "nesting_level": 0,
                "control_variable": "i",
                "iterations": "n"
            }
        }


class ScenarioState(BaseModel):
    """
    Estado completo del workflow de Fase 2: Mapeo de Escenarios.

    Este estado fluye a través de todos los nodos del workflow de LangGraph,
    actualizándose progresivamente hasta generar la Tabla Ω final.
    """

    # ===== INPUT (de Fase 1: Validación) =====
    pseudocode: str  # Pseudocódigo validado
    algorithm_name: str  # Nombre del algoritmo
    is_iterative: bool  # True si es iterativo, False si recursivo
    parameters: Dict[str, str] = Field(default_factory=dict)  # {"A[]": "array", "n": "int"}

    # ===== PROCESAMIENTO INTERNO =====
    # Paso 1: Parsing
    lines: List[str] = Field(default_factory=list)  # Líneas del pseudocódigo

    # Paso 2: Análisis de Loops
    loops: List[LoopInfo] = Field(default_factory=list)  # Info de todos los loops

    # Paso 3: Identificación de Variables de Control
    control_variables: List[ControlVariable] = Field(default_factory=list)

    # Paso 4: Generación de Escenarios (pre-costeo)
    raw_scenarios: List[Dict] = Field(default_factory=list)
    # Lista de diccionarios con {id, condition, state, iteration_value}

    # ===== OUTPUT PRINCIPAL =====
    omega_table: Optional[OmegaTable] = None  # Tabla Ω completa con todos los escenarios

    # ===== METADATA Y ERRORES =====
    errors: List[str] = Field(default_factory=list)  # Errores encontrados
    warnings: List[str] = Field(default_factory=list)  # Warnings no críticos

    class Config:
        json_schema_extra = {
            "example": {
                "pseudocode": "suma ← 0\nfor i ← 1 to n do\nbegin\n    suma ← suma + A[i]\nend\nreturn suma",
                "algorithm_name": "suma",
                "is_iterative": True,
                "parameters": {"A[]": "array", "n": "int"},
                "lines": [],
                "loops": [],
                "control_variables": [],
                "raw_scenarios": [],
                "omega_table": None,
                "errors": [],
                "warnings": []
            }
        }

    def add_error(self, error_msg: str):
        """Agrega un error al estado."""
        self.errors.append(error_msg)

    def add_warning(self, warning_msg: str):
        """Agrega un warning al estado."""
        self.warnings.append(warning_msg)

    def has_errors(self) -> bool:
        """Verifica si hay errores."""
        return len(self.errors) > 0
