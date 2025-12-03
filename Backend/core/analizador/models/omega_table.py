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
    """
    id: str  # Identificador único: S_k=1, S_k=k, S_fallo, S_p=0, etc.
    condition: str  # Expresión lógica que activa este escenario
    state: str  # Estado cualitativo: EXITO_TEMPRANO, EXITO_INTERMEDIO, FALLO_COMPLETO, etc.
    cost_T: str  # T(S) = función de costo para este escenario ("4*k + 2", "n²", etc.)
    probability_P: str  # P(S) = probabilidad de ocurrencia ("1/n", "1/(n+1)", etc.)

    # ⭐ SUBTABLA DE JUSTIFICACIÓN (costeo línea por línea)
    line_costs: List[LineCost] = Field(default_factory=list)

    def calculate_total(self) -> str:
        """
        Suma todos los line_costs para verificar que coincide con cost_T.

        Returns:
            Formula simplificada con sympy
        """
        if not self.line_costs:
            return "0"

        # Sumar todos los totales usando sympy
        total = 0
        for line_cost in self.line_costs:
            try:
                total += sp.sympify(line_cost.Total)
            except:
                # Si no se puede parsear, ignorar
                pass

        simplified = sp.simplify(total)
        return str(simplified)

    class Config:
        json_schema_extra = {
            "example": {
                "id": "S_k=1",
                "condition": "A[1] == x",
                "state": "EXITO_TEMPRANO",
                "cost_T": "6",
                "probability_P": "1/n",
                "line_costs": []
            }
        }


class OmegaTable(BaseModel):
    """
    Tabla Universal Ω completa del algoritmo.

    Contiene todos los escenarios posibles identificados durante el análisis,
    junto con metadata del algoritmo.
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

        Args:
            scenario_id: ID del escenario (ej: "S_k=1")

        Returns:
            Tabla Markdown con formato:
            | Línea | Código | C_op | Freq | Total |
        """
        # Buscar escenario
        scenario = next((s for s in self.scenarios if s.id == scenario_id), None)

        if not scenario:
            return f"Scenario {scenario_id} not found"

        if not scenario.line_costs:
            return f"No line costs for scenario {scenario_id}"

        lines = [
            f"### Justificación de {scenario_id}",
            "",
            "| Línea | Código | C_op | Freq | Total |",
            "| :---: | :--- | :---: | :---: | :---: |"
        ]

        for lc in scenario.line_costs:
            lines.append(
                f"| {lc.line_number} | `{lc.code}` | {lc.C_op} | {lc.Freq} | {lc.Total} |"
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
