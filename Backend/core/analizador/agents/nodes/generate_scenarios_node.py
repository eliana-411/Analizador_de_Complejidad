"""
Nodo: Generate Scenarios - Genera taxonomía de escenarios

Genera múltiples escenarios basados en:
- Variables de control (para iterativos)
- Patrones de recursión (para recursivos)
"""

from core.analizador.models.scenario_state import ScenarioState


def generate_scenarios_node(state: ScenarioState) -> ScenarioState:
    """
    Genera casos atómicos para la Tabla Ω.

    Para algoritmos iterativos:
    - S_k=1 (éxito temprano)
    - S_k=k (éxito intermedio)
    - S_k=n (ejecución completa sin éxito)
    - S_fallo (fallo después de revisar todos)

    Para algoritmos recursivos:
    - S_balanced (división balanceada - mejor/promedio caso)
    - S_skewed (división desbalanceada - peor caso)

    Args:
        state: Estado actual con 'control_variables' o 'recursion_info' pobladas

    Returns:
        Estado actualizado con 'raw_scenarios' poblado
    """
    scenarios = []

    if state.is_recursive and state.recursion_info:
        # ALGORITMOS RECURSIVOS
        scenarios.extend(generate_recursive_scenarios(state))

    elif state.is_iterative and state.loops:
        # ALGORITMOS ITERATIVOS
        scenarios.extend(generate_iterative_scenarios(state))

    else:
        # Algoritmos sin loops ni recursión (casos triviales)
        scenarios.append({
            "id": "S_base",
            "condition": "Caso base",
            "state": "EJECUCION_SIMPLE",
            "iteration_value": "1",
            "early_exit": False,
        })

    return state.model_copy(update={"raw_scenarios": scenarios})


def generate_iterative_scenarios(state: ScenarioState) -> list:
    """
    Genera escenarios para algoritmos iterativos.

    Returns:
        Lista de diccionarios con escenarios
    """
    scenarios = []

    # Verificar si hay variables de control secundarias (flags de salida temprana)
    has_secondary_vars = any(
        cv.type == "SECONDARY" and cv.affects_termination
        for cv in state.control_variables
    )

    if has_secondary_vars:
        # Algoritmo con posible salida temprana (ej: búsqueda)
        scenarios.extend([
            {
                "id": "S_k=1",
                "condition": "Éxito inmediato (primera iteración)",
                "state": "EXITO_TEMPRANO",
                "iteration_value": "1",
                "early_exit": True
            },
            {
                "id": "S_k=k",
                "condition": "Éxito en iteración intermedia k",
                "state": "EXITO_INTERMEDIO",
                "iteration_value": "k",
                "early_exit": True
            },
            {
                "id": "S_k=n",
                "condition": "Búsqueda en última posición",
                "state": "EXITO_TARDIO",
                "iteration_value": "n",
                "early_exit": False
            },
            {
                "id": "S_fallo",
                "condition": "Elemento no encontrado",
                "state": "FALLO_COMPLETO",
                "iteration_value": "n+1",
                "early_exit": False
            }
        ])
    else:
        # Algoritmo sin salida temprana (ej: suma, ordenamiento)
        scenarios.append({
            "id": "S_estandar",
            "condition": "Ejecución completa sin interrupciones",
            "state": "EJECUCION_COMPLETA",
            "iteration_value": "n",
            "early_exit": False
        })

    return scenarios


def generate_recursive_scenarios(state: ScenarioState) -> list:
    """
    Genera escenarios para algoritmos recursivos.

    Returns:
        Lista de diccionarios con escenarios
    """
    scenarios = []

    recursion_type = state.recursion_info.recurrence_type

    if recursion_type == "divide":
        # Algoritmos divide-and-conquer (ej: merge sort, quicksort, binary search)
        scenarios.extend([
            {
                "id": "S_balanced",
                "condition": "División balanceada del problema",
                "state": "RECURSION_BALANCEADA",
                "recursion_pattern": "balanced"
            },
            {
                "id": "S_skewed",
                "condition": "División desbalanceada (peor caso)",
                "state": "RECURSION_DESBALANCEADA",
                "recursion_pattern": "skewed"
            }
        ])
    elif recursion_type == "subtract":
        # Recursión por decremento (ej: factorial, fibonacci)
        scenarios.append({
            "id": "S_standard",
            "condition": "Ejecución estándar recursiva",
            "state": "RECURSION_ESTANDAR",
            "recursion_pattern": "standard"
        })
    else:
        # Recursión mixta
        scenarios.append({
            "id": "S_standard",
            "condition": "Ejecución estándar recursiva",
            "state": "RECURSION_ESTANDAR",
            "recursion_pattern": "standard"
        })

    return scenarios
