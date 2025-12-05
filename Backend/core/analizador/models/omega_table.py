"""
Modelos para la Tabla Omega (Ω) - Tabla Universal de Escenarios

Este módulo define las estructuras de datos para representar:
- LineCost: Costo de una línea individual en un escenario
- ScenarioEntry: Un escenario/evento atómico en la Tabla Ω
- OmegaTable: Tabla completa con todos los escenarios
"""

from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import sympy as sp


class LineCost(BaseModel):
    """
    Costo de una línea específica del pseudocódigo para un escenario dado.

    Representa la descomposición de T(S) línea por línea.
    """
    line_number: int
    code: str  # Contenido de la línea de pseudocódigo
    C_op: int  # Costo invariante (número de operaciones elementales)
    Freq: str  # Multiplicador/frecuencia ("n", "k", "1", "n-1", etc.)
    Total: str  # C_op × Freq = costo total de esta línea

    class Config:
        json_schema_extra = {
            "example": {
                "line_number": 11,
                "code": "if (A[i] = x)",
                "C_op": 2,
                "Freq": "n",
                "Total": "2*n"
            }
        }


class ScenarioEntry(BaseModel):
    """
    Una fila en la Tabla Ω que representa un escenario/evento atómico.

    Cada escenario corresponde a un camino de ejecución específico del algoritmo,
    definido por condiciones lógicas sobre las variables de control.

    NOTA: Los detalles del análisis línea por línea se almacenan en
    OmegaTable.metadata, no dentro de cada escenario.
    """
    id: str  # Identificador único: S_k=1, S_k=k, S_fallo, S_p=0, etc.
    semantic_id: str = ""  # Identificador semántico: S_best, S_worst, S_intermediate, etc.
    condition: str  # Expresión lógica que activa este escenario
    state: str  # Estado cualitativo: EXITO_TEMPRANO, EXITO_INTERMEDIO, FALLO_COMPLETO, etc.
    cost_T: str  # T(S) = función de costo para este escenario ("4*k + 2", "n²", etc.)
    probability_P: str  # P(S) = probabilidad de ocurrencia ("1/n", "q·(1/n)", "1-q", etc.)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "S_k=1",
                "semantic_id": "best_case",
                "condition": "A[1] == x",
                "state": "EXITO_TEMPRANO",
                "cost_T": "6",
                "probability_P": "1/n"
            }
        }


class SummaryEntry(BaseModel):
    """
    Entrada de resumen para un caso específico (mejor/peor).

    Contiene información resumida sobre un escenario particular
    que representa el mejor o peor caso del algoritmo.
    """
    scenario_id: str  # ID del escenario (ej: "S_1", "S_∅")
    semantic_id: str  # ID semántico (ej: "S_best", "S_worst")
    T: str  # Función de costo T(S) para este caso
    P: str  # Probabilidad P(S) de este caso
    description: str  # Descripción de la entrada que causa este caso

    class Config:
        json_schema_extra = {
            "example": {
                "scenario_id": "S_1",
                "semantic_id": "S_best",
                "T": "7",
                "P": "q·(1/n)",
                "description": "Elemento en primera posición"
            }
        }


class CaseSummary(BaseModel):
    """
    Resumen completo de mejor caso, peor caso y caso promedio.

    Proporciona una vista consolidada de los casos clave del análisis
    de complejidad del algoritmo.
    """
    best_case: SummaryEntry  # Escenario de mejor caso (mínimo T(S))
    worst_case: SummaryEntry  # Escenario de peor caso (máximo T(S))
    average_case: Dict  # Caso promedio: {"T_avg": str, "formula": str}

    class Config:
        json_schema_extra = {
            "example": {
                "best_case": {
                    "scenario_id": "S_1",
                    "semantic_id": "S_best",
                    "T": "7",
                    "P": "q·(1/n)",
                    "description": "Elemento en primera posición"
                },
                "worst_case": {
                    "scenario_id": "S_∅",
                    "semantic_id": "S_worst_not_found",
                    "T": "4*n+2",
                    "P": "1-q",
                    "description": "Elemento no existe en el arreglo"
                },
                "average_case": {
                    "T_avg": "q·(n+1)/2 + (1-q)·n",
                    "formula": "Σ T(S)·P(S) = q·(n+1)/2 + (1-q)·n"
                }
            }
        }


class OmegaTable(BaseModel):
    """
    Tabla Universal Ω completa del algoritmo.

    Contiene todos los escenarios posibles identificados durante el análisis,
    junto con metadata del algoritmo que incluye:
    - algorithm_type: "iterative" | "recursive"
    - llm_analysis: Análisis completo del LLM (mejor, peor, promedio casos)
    - line_by_line_details: Desglose línea por línea de cada escenario
    - best_case, worst_case, average_case: Resúmenes de casos principales

    Esta estructura simplificada permite pasar la tabla al módulo de
    representación matemática de forma directa.
    """
    algorithm_name: str
    scenarios: List[ScenarioEntry]
    control_variables: List[str]
    metadata: Dict = Field(default_factory=dict)

    def get_min_cost_scenario(self) -> Optional[ScenarioEntry]:
        """
        Obtiene el escenario con costo mínimo (para Ω - lower bound).

        Returns:
            Escenario con menor costo, o None si no hay escenarios
        """
        if not self.scenarios:
            return None

        # Comparar costos (simplificado: asumir costos comparables)
        # En versión completa, usar evaluación simbólica para n grande
        return min(self.scenarios, key=lambda s: self._cost_complexity(s.cost_T))

    def get_max_cost_scenario(self) -> Optional[ScenarioEntry]:
        """
        Obtiene el escenario con costo máximo (para O - upper bound).

        Returns:
            Escenario con mayor costo, o None si no hay escenarios
        """
        if not self.scenarios:
            return None

        return max(self.scenarios, key=lambda s: self._cost_complexity(s.cost_T))

    def _cost_complexity(self, cost_str: str) -> int:
        """
        Heurística simple para comparar complejidades.

        Retorna un valor numérico aproximado de la complejidad.
        Esto es simplificado; versión completa usaría análisis asintótico.
        """
        cost_str = cost_str.lower()

        # Orden de complejidad aproximado
        if 'log' in cost_str and 'n' in cost_str:
            return 100  # O(n log n)
        elif 'n**3' in cost_str or 'n³' in cost_str:
            return 1000
        elif 'n**2' in cost_str or 'n²' in cost_str:
            return 500
        elif 'n*log' in cost_str:
            return 100
        elif 'n' in cost_str:
            return 10
        elif 'log' in cost_str:
            return 5
        else:
            return 1  # O(1)

    def to_markdown_table(self) -> str:
        """
        Genera tabla Markdown de la Tabla Ω principal.

        Formato:
        | ID | Condición | Estado | T(S) | P(S) |
        """
        if not self.scenarios:
            return "No scenarios found"

        lines = [
            "| ID Escenario | Condición | Estado | T(S) | P(S) |",
            "| :--- | :--- | :--- | :--- | :--- |"
        ]

        for scenario in self.scenarios:
            lines.append(
                f"| {scenario.id} | {scenario.condition} | {scenario.state} | "
                f"{scenario.cost_T} | {scenario.probability_P} |"
            )

        return "\n".join(lines)

    def scenario_to_markdown_justification(self, scenario_id: str) -> str:
        """
        Genera subtabla de justificación (costeo línea por línea) para un escenario.

        Los datos se extraen de metadata['llm_analysis'][case]['line_by_line_analysis']

        Args:
            scenario_id: ID del escenario (ej: "S_k=1", "S_best_case")

        Returns:
            Tabla Markdown con formato:
            | Línea | Código | C_op | Freq | Total |
        """
        # Buscar escenario
        scenario = next((s for s in self.scenarios if s.id == scenario_id), None)

        if not scenario:
            return f"Scenario {scenario_id} not found"

        # Buscar análisis línea por línea en metadata
        line_costs = []
        if 'llm_analysis' in self.metadata:
            semantic_id = scenario.semantic_id
            # Mapear semantic_id a keys del LLM analysis
            case_key = semantic_id if semantic_id in self.metadata['llm_analysis'] else None

            if case_key and 'line_by_line_analysis' in self.metadata['llm_analysis'][case_key]:
                line_costs = self.metadata['llm_analysis'][case_key]['line_by_line_analysis']

        if not line_costs:
            return f"No line costs for scenario {scenario_id} in metadata"

        lines = [
            f"### Justificación de {scenario_id}",
            "",
            "| Línea | Código | C_op | Freq | Total |",
            "| :---: | :--- | :---: | :---: | :---: |"
        ]

        for lc in line_costs:
            lines.append(
                f"| {lc.get('line_number', 0)} | `{lc.get('code', '')}` | "
                f"{lc.get('C_op', 0)} | {lc.get('Freq', '1')} | {lc.get('Total', '0')} |"
            )

        # Agregar total
        lines.append(f"| **Total** | | | | **{scenario.cost_T}** |")

        return "\n".join(lines)

    class Config:
        json_schema_extra = {
            "example": {
                "algorithm_name": "busquedaLineal",
                "scenarios": [],
                "control_variables": ["i", "encontrado"],
                "metadata": {
                    "loop_count": 1,
                    "nesting_level": 1
                }
            }
        }
