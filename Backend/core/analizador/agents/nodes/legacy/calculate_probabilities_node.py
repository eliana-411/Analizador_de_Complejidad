"""
Nodo: Calculate Probabilities - Asigna probabilidades P(S) a escenarios

Calcula probabilidades según modelo matemático:
- Para algoritmos con parámetro q: P(S_k) = q·(1/n), P(S_∅) = 1-q
- Para algoritmos sin q: P(S) = 1/n (equiprobable)
- Para algoritmos no sensibles: P(S) = 1 (un solo escenario)
"""

from core.analizador.models.scenario_state import ScenarioState


def calculate_probabilities_node(state: ScenarioState) -> ScenarioState:
    """
    Asigna probabilidades P(S) a cada escenario según modelo matemático.

    El cálculo de P(S) depende de:
    1. Si el algoritmo usa parámetro q (probabilidad de existencia)
    2. Cuántos escenarios hay en total
    3. El tipo de escenario (éxito vs fallo)

    Fórmulas:
    - Con q (búsqueda): P(S_k) = q·(1/n) para k=1..n, P(S_∅) = 1-q
    - Sin q (equiprobable): P(S) = 1/n_scenarios
    - No sensible: P(S) = 1

    Args:
        state: Estado actual con 'raw_scenarios' y 'llm_analysis' poblados

    Returns:
        Estado actualizado con probabilidades asignadas
    """
    updated_scenarios = []

    # Obtener análisis LLM para determinar si necesitamos parámetro q
    llm_analysis = state.llm_analysis or {}
    needs_q = llm_analysis.get("parameter_q_applicable", False)

    # Caso especial: un solo escenario → P(S) = 1
    if len(state.raw_scenarios) == 1:
        scenario = state.raw_scenarios[0]
        scenario_with_prob = {**scenario, "probability_P": "1"}
        updated_scenarios.append(scenario_with_prob)

        return state.model_copy(update={"raw_scenarios": updated_scenarios})

    # Múltiples escenarios: calcular según modelo
    for scenario in state.raw_scenarios:
        probability = calculate_scenario_probability(
            scenario=scenario,
            all_scenarios=state.raw_scenarios,
            needs_q=needs_q
        )

        scenario_with_prob = {**scenario, "probability_P": probability}
        updated_scenarios.append(scenario_with_prob)

    return state.model_copy(update={"raw_scenarios": updated_scenarios})


def calculate_scenario_probability(scenario: dict, all_scenarios: list, needs_q: bool) -> str:
    """
    Calcula la probabilidad de un escenario específico.

    Args:
        scenario: Escenario actual
        all_scenarios: Lista de todos los escenarios
        needs_q: Si se debe usar el parámetro q

    Returns:
        String con la expresión de probabilidad (ej: "q·(1/n)", "1-q", "1/n")
    """
    scenario_id = scenario["id"]

    if needs_q:
        # Modelo con parámetro q (típico de búsqueda)
        return calculate_probability_with_q(scenario_id, all_scenarios)
    else:
        # Modelo equiprobable sin q
        n_scenarios = len(all_scenarios)
        return f"1/{n_scenarios}" if n_scenarios > 1 else "1"


def calculate_probability_with_q(scenario_id: str, all_scenarios: list) -> str:
    """
    Calcula probabilidad usando el modelo con parámetro q.

    Modelo matemático:
    - P(S_∅) = 1-q (probabilidad de que el elemento NO exista)
    - P(S_k) = q·(1/n) para k=1,2,...,n (cada posición equiprobable dentro de los que existen)

    Args:
        scenario_id: ID del escenario ("S_1", "S_k", "S_n", "S_∅")
        all_scenarios: Lista completa de escenarios

    Returns:
        Expresión de probabilidad como string
    """
    # Escenario de fallo (elemento no existe)
    if scenario_id == "S_∅":
        return "1-q"

    # Escenarios de éxito (S_1, S_k, S_n, etc.)
    # Contar cuántos escenarios de éxito hay
    success_scenarios = [s for s in all_scenarios if s["id"] != "S_∅"]
    n_success = len(success_scenarios)

    if n_success == 0:
        # No debería pasar, pero manejamos el caso
        return "q"

    # P(S_k) = q · (1/n)
    # Nota: n es el número de posiciones posibles (n_success)
    return f"q·(1/{n_success})"


def format_probability_expression(expr: str) -> str:
    """
    Formatea expresiones de probabilidad para consistencia.

    Args:
        expr: Expresión de probabilidad

    Returns:
        Expresión formateada

    Examples:
        "q*(1/4)" -> "q·(1/4)"
        "1/4" -> "1/4"
        "1" -> "1"
    """
    # Reemplazar * por · para multiplicación
    expr = expr.replace("*", "·")

    # Asegurar espacios consistentes
    expr = expr.replace(" ", "")

    return expr
