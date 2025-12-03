"""
Nodo: Build Omega Table - Ensambla la Tabla Ω final

Convierte raw_scenarios en estructura OmegaTable con ScenarioEntry.
"""

from Backend.mapeo.models.scenario_state import ScenarioState
from Backend.mapeo.models.omega_table import OmegaTable, ScenarioEntry


def build_omega_table_node(state: ScenarioState) -> ScenarioState:
    """
    Construye la Tabla Ω final a partir de los escenarios procesados.

    Args:
        state: Estado actual con 'raw_scenarios' completos (con costos y probabilidades)

    Returns:
        Estado actualizado con 'omega_table' poblada
    """
    scenario_entries = []

    for raw_scenario in state.raw_scenarios:
        # Convertir diccionario a ScenarioEntry
        entry = ScenarioEntry(
            id=raw_scenario["id"],
            condition=raw_scenario["condition"],
            state=raw_scenario["state"],
            cost_T=raw_scenario.get("cost_T", "0"),
            probability_P=raw_scenario.get("probability_P", "0"),
            line_costs=raw_scenario.get("line_costs", [])
        )

        scenario_entries.append(entry)

    # Construir tabla completa
    omega_table = OmegaTable(
        algorithm_name=state.algorithm_name,
        scenarios=scenario_entries,
        control_variables=[cv.name for cv in state.control_variables],
        metadata={
            "loop_count": len(state.loops),
            "nesting_level": max([loop.nesting_level for loop in state.loops], default=0),
            "is_iterative": state.is_iterative,
            "parameters": state.parameters
        }
    )

    return state.model_copy(update={"omega_table": omega_table})
