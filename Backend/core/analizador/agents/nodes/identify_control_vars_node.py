"""
Nodo: Identify Control Variables - Identifica variables de control

Para MVP: Solo identifica variables índice de loops (PRIMARY).
Versión completa identificará banderas y variables que afectan terminación.
"""

from Backend.analizador.models.scenario_state import ControlVariable, ScenarioState


def identify_control_vars_node(state: ScenarioState) -> ScenarioState:
    """
    Identifica variables de control del algoritmo.

    MVP: Solo variables PRIMARY (índices de loops).

    Args:
        state: Estado actual con 'loops' pobladas

    Returns:
        Estado actualizado con 'control_variables' poblado
    """
    control_vars = []

    # Para MVP: solo identificar variables índice de loops
    for loop in state.loops:
        control_vars.append(
            ControlVariable(
                name=loop.control_variable,
                type="PRIMARY",
                scope="loop_index",
                affects_termination=False,  # MVP: sin salidas tempranas
            )
        )

    # TODO: Versión completa identificará:
    # - Banderas booleanas (SECONDARY)
    # - Variables en condiciones de loops
    # - Variables que causan return/break

    return state.model_copy(update={"control_variables": control_vars})
