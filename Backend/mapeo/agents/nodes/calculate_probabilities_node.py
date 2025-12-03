"""
Nodo: Calculate Probabilities - Asigna probabilidades P(S) a escenarios

Para MVP: P(S) = 1 (un solo escenario).
Versión completa calculará probabilidades según distribución de casos.
"""

from Backend.mapeo.models.scenario_state import ScenarioState


def calculate_probabilities_node(state: ScenarioState) -> ScenarioState:
    """
    Asigna probabilidades P(S) a cada escenario.

    MVP: P(S) = 1 para el escenario único.

    Args:
        state: Estado actual con 'raw_scenarios' con costos calculados

    Returns:
        Estado actualizado con probabilidades asignadas
    """
    updated_scenarios = []

    for scenario in state.raw_scenarios:
        # MVP: Un solo escenario → P(S) = 1
        if len(state.raw_scenarios) == 1:
            probability = "1"
        else:
            # Heurística simple: equiprobables
            probability = f"1/{len(state.raw_scenarios)}"

        # TODO: Versión completa calculará:
        # - P(S_k=1) = 1/n (éxito en primera posición)
        # - P(S_k=k) = 1/n (para cada k específico)
        # - P(S_fallo) = depende del dominio (elemento no está)
        # - Considerar distribuciones no uniformes

        scenario_with_prob = {
            **scenario,
            "probability_P": probability
        }

        updated_scenarios.append(scenario_with_prob)

    return state.model_copy(update={"raw_scenarios": updated_scenarios})
