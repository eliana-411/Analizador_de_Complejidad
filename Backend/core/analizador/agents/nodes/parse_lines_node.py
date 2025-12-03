"""
Nodo: Parse Lines - Extrae las líneas del pseudocódigo

Primer nodo del workflow que divide el pseudocódigo en líneas
para procesamiento posterior.
"""

from Backend.analizador.models.scenario_state import ScenarioState


def parse_lines_node(state: ScenarioState) -> ScenarioState:
    """
    Extrae líneas del pseudocódigo.

    Args:
        state: Estado actual del workflow

    Returns:
        Estado actualizado con campo 'lines' poblado
    """
    lines = state.pseudocode.strip().split("\n")

    # Actualizar estado usando model_copy (Pydantic V2)
    return state.model_copy(update={"lines": lines})
