"""
Nodo: Generate Scenarios - Genera escenarios

VERSION MVP: Solo genera EL MEJOR CASO

Genera escenarios basados en el análisis LLM del mejor caso.
"""

from core.analizador.models.scenario_state import ScenarioState


def generate_scenarios_node(state: ScenarioState) -> ScenarioState:
    """
    Genera escenario del MEJOR CASO.

    VERSION MVP: Solo genera 1 escenario (mejor caso) con características específicas.

    Args:
        state: Estado actual con 'llm_analysis' poblado

    Returns:
        Estado actualizado con 'raw_scenarios' poblado con 1 escenario
    """
    scenarios = []

    if state.is_iterative and state.loops:
        # ALGORITMOS ITERATIVOS - solo mejor caso
        scenarios.extend(generate_best_case_iterative(state))

    else:
        # Algoritmos sin loops (casos triviales)
        scenarios.append({
            "id": "S_best",
            "semantic_id": "S_best",
            "condition": "Caso base",
            "state": "EJECUCION_SIMPLE",
            "iteration_value": "1",
            "early_exit": False,
            "input_description": "Cualquier entrada (algoritmo constante)",
            "input_characteristics": {},
            "num_iterations": 1
        })

    return state.model_copy(update={"raw_scenarios": scenarios})


def generate_best_case_iterative(state: ScenarioState) -> list:
    """
    Genera SOLO el escenario del MEJOR CASO para algoritmos iterativos.

    VERSION MVP: Solo genera 1 escenario.

    Returns:
        Lista con 1 diccionario con el escenario del mejor caso
    """
    scenarios = []

    # Obtener análisis LLM del mejor caso
    llm_analysis = state.llm_analysis or {}
    best_case = llm_analysis.get("best_case", {})

    # Generar escenario del mejor caso usando datos del LLM
    scenarios.append({
        "id": "S_best",
        "semantic_id": "S_best",
        "condition": best_case.get("input_description", "Mejor caso"),
        "state": "MEJOR_CASO",
        "iteration_value": str(best_case.get("num_iterations", 1)),
        "early_exit": True,
        "input_description": best_case.get("input_description", "Mejor caso"),
        # NUEVO: Campos específicos para análisis línea por línea
        "input_characteristics": best_case.get("input_characteristics", {}),
        "num_iterations": best_case.get("num_iterations", 1)
    })

    return scenarios
