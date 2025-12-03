"""
Nodo: Calculate Costs - Calcula T(S) para cada escenario

Usa LineCostCalculator para obtener costeo línea por línea.
"""

from Backend.analizador.models.scenario_state import ScenarioState
from Backend.analizador.tools.line_cost_calculator import LineCostCalculator


def calculate_costs_node(state: ScenarioState) -> ScenarioState:
    """
    Calcula el costo T(S) para cada escenario usando análisis línea por línea.

    Args:
        state: Estado actual con 'raw_scenarios' poblado

    Returns:
        Estado actualizado con costos calculados en 'raw_scenarios'
    """
    calculator = LineCostCalculator()
    updated_scenarios = []

    for scenario in state.raw_scenarios:
        # Calcular T(S) y obtener desglose línea por línea
        try:
            cost_formula, line_costs = calculator.calculate_scenario_cost(
                lines=state.lines,
                scenario=scenario,
                loops=state.loops
            )

            # Actualizar escenario con costo calculado
            scenario_with_cost = {
                **scenario,
                "cost_T": cost_formula,
                "line_costs": line_costs  # Lista de LineCost objects
            }

            updated_scenarios.append(scenario_with_cost)

        except Exception as e:
            # Si hay error en el cálculo, agregar warning
            state.add_warning(f"Error calculando costo para {scenario['id']}: {str(e)}")
            updated_scenarios.append(scenario)

    return state.model_copy(update={"raw_scenarios": updated_scenarios})
