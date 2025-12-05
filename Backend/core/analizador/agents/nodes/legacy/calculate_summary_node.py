"""
Nodo: Calculate Summary - Calcula resumen de mejor/peor/promedio caso

Este nodo genera el resumen consolidado que incluye:
1. Mejor caso (escenario con mínimo T(S))
2. Peor caso (escenario con máximo T(S))
3. Caso promedio (E[T] = Σ T(S)·P(S))
"""

import sympy as sp
from typing import Dict, Any, List
from core.analizador.models.scenario_state import ScenarioState


def calculate_summary_node(state: ScenarioState) -> ScenarioState:
    """
    Calcula resumen de mejor/peor/promedio caso.

    Args:
        state: Estado con raw_scenarios poblado con costos y probabilidades

    Returns:
        Estado actualizado con summary poblado

    Example summary:
        {
            "best_case": {
                "scenario_id": "S_1",
                "semantic_id": "S_best",
                "T": "7",
                "P": "q·(1/4)",
                "description": "Elemento en primera posición"
            },
            "worst_case": {
                "scenario_id": "S_∅",
                "semantic_id": "S_worst_not_found",
                "T": "4*n+2",
                "P": "1-q",
                "description": "Elemento no encontrado"
            },
            "average_case": {
                "T_avg": "q·(n+1)/2 + (1-q)·n",
                "formula": "Σ T(S)·P(S) = q·(n+1)/2 + (1-q)·n"
            }
        }
    """
    scenarios = state.raw_scenarios

    if not scenarios:
        # No hay escenarios, retornar sin cambios
        return state

    # 1. Identificar mejor caso (mínimo T(S))
    best_scenario = find_best_case(scenarios)

    # 2. Identificar peor caso (máximo T(S))
    worst_scenario = find_worst_case(scenarios)

    # 3. Calcular caso promedio E[T] = Σ T(S)·P(S)
    average_case = calculate_average_case(scenarios)

    # 4. Construir resumen
    summary = {
        "best_case": {
            "scenario_id": best_scenario["id"],
            "semantic_id": best_scenario.get("semantic_id", ""),
            "T": best_scenario.get("cost_T", ""),
            "P": best_scenario.get("probability_P", ""),
            "description": best_scenario.get("input_description", "")
        },
        "worst_case": {
            "scenario_id": worst_scenario["id"],
            "semantic_id": worst_scenario.get("semantic_id", ""),
            "T": worst_scenario.get("cost_T", ""),
            "P": worst_scenario.get("probability_P", ""),
            "description": worst_scenario.get("input_description", "")
        },
        "average_case": average_case
    }

    return state.model_copy(update={"summary": summary})


def find_best_case(scenarios: List[Dict]) -> Dict:
    """
    Encuentra el escenario con costo mínimo (mejor caso).

    Args:
        scenarios: Lista de escenarios con cost_T

    Returns:
        Escenario con menor costo
    """
    # Primero intentar por semantic_id
    best_by_semantic = next(
        (s for s in scenarios if s.get("semantic_id") == "S_best"),
        None
    )

    if best_by_semantic:
        return best_by_semantic

    # Si no hay semantic_id, buscar por costo mínimo
    return min(scenarios, key=lambda s: estimate_cost_complexity(s.get("cost_T", "n")))


def find_worst_case(scenarios: List[Dict]) -> Dict:
    """
    Encuentra el escenario con costo máximo (peor caso).

    Args:
        scenarios: Lista de escenarios con cost_T

    Returns:
        Escenario con mayor costo
    """
    # Primero buscar por semantic_id específicos de peor caso
    worst_by_semantic = next(
        (s for s in scenarios if s.get("semantic_id") in ["S_worst", "S_worst_not_found", "S_worst_found"]),
        None
    )

    if worst_by_semantic:
        return worst_by_semantic

    # Si no hay semantic_id, buscar por costo máximo
    return max(scenarios, key=lambda s: estimate_cost_complexity(s.get("cost_T", "n")))


def calculate_average_case(scenarios: List[Dict]) -> Dict[str, str]:
    """
    Calcula el caso promedio E[T] = Σ T(S)·P(S).

    Args:
        scenarios: Lista de escenarios con cost_T y probability_P

    Returns:
        Dict con T_avg y formula
    """
    try:
        # Sumar T(S) * P(S) para cada escenario
        terms = []

        for scenario in scenarios:
            T_s = scenario.get("cost_T", "0")
            P_s = scenario.get("probability_P", "0")

            # Parsear con sympy
            try:
                T_sym = sp.sympify(T_s)
                P_sym = sp.sympify(P_s.replace("·", "*"))  # Reemplazar · por *
                terms.append(T_sym * P_sym)
            except Exception:
                # Si falla parseo, omitir este término
                continue

        # Sumar todos los términos
        if not terms:
            return {
                "T_avg": "n",
                "formula": "Σ T(S)·P(S) = n"
            }

        total = sum(terms)
        simplified = sp.simplify(total)

        return {
            "T_avg": str(simplified),
            "formula": f"Σ T(S)·P(S) = {str(simplified)}"
        }

    except Exception as e:
        # Fallback: retornar fórmula genérica
        return {
            "T_avg": "Σ T(S)·P(S)",
            "formula": f"Σ T(S)·P(S) (no se pudo simplificar: {str(e)})"
        }


def estimate_cost_complexity(cost_str: str) -> int:
    """
    Estima la complejidad de un costo para comparación.

    Esta es una heurística simple para ordenar costos por magnitud.

    Args:
        cost_str: String de costo (ej: "n", "n**2", "4*k+2")

    Returns:
        Valor estimado de complejidad (mayor = más costoso)
    """
    cost_lower = cost_str.lower()

    # Orden de complejidad aproximado
    if 'n**3' in cost_lower or 'n³' in cost_lower:
        return 1000
    elif 'n**2' in cost_lower or 'n²' in cost_lower:
        return 500
    elif 'n*log' in cost_lower or 'log' in cost_lower and 'n' in cost_lower:
        return 100
    elif 'n' in cost_lower:
        return 10
    elif 'log' in cost_lower:
        return 5
    elif 'k' in cost_lower:
        # k es variable, asumir complejidad lineal
        return 10
    else:
        # Constante
        return 1
