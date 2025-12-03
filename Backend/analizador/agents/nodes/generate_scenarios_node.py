"""
Nodo: Generate Scenarios - Genera taxonomía de escenarios

Para MVP: Un solo escenario de ejecución completa.
Versión completa generará múltiples escenarios basados en variables de control.
"""

from Backend.analizador.models.scenario_state import ScenarioState


def generate_scenarios_node(state: ScenarioState) -> ScenarioState:
    """
    Genera casos atómicos para la Tabla Ω.

    MVP: Un solo escenario de ejecución completa estándar (sin salidas tempranas).

    Args:
        state: Estado actual con 'control_variables' pobladas

    Returns:
        Estado actualizado con 'raw_scenarios' poblado
    """
    scenarios = []

    # MVP: Escenario único - ejecución completa
    if state.is_iterative and state.loops:
        # Para algoritmos con loops simples
        scenarios.append({
            "id": "S_estandar",
            "condition": "Ejecución completa sin interrupciones",
            "state": "EJECUCION_COMPLETA",
            "iteration_value": "n",  # Sin salida temprana
            "early_exit": False
        })
    else:
        # Para algoritmos sin loops (casos triviales)
        scenarios.append({
            "id": "S_base",
            "condition": "Caso base",
            "state": "EJECUCION_SIMPLE",
            "iteration_value": "1",
            "early_exit": False
        })

    # TODO: Versión completa generará:
    # - S_k=1 (éxito temprano)
    # - S_k=k (éxito intermedio)
    # - S_k=n+1 (fallo completo)
    # - Escenarios para cada variable de control SECONDARY

    return state.model_copy(update={"raw_scenarios": scenarios})
