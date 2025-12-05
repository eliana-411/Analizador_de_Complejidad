"""
Nodo: Analyze Input Scenarios - Analiza características de entrada con LLM

VERSION MVP: Solo analiza MEJOR CASO

Este nodo utiliza un LLM para analizar el pseudocódigo y determinar:
1. Características de entrada del MEJOR CASO
2. Número exacto de iteraciones para el mejor caso
3. Características específicas de entrada (position, found, etc.)
"""

import json
from typing import Dict, Any
from core.analizador.models.scenario_state import ScenarioState
from core.analizador.tools.llm_analyzer import get_llm_analyzer


def analyze_input_scenarios_node(state: ScenarioState) -> ScenarioState:
    """
    Analiza el pseudocódigo con LLM para determinar SOLO EL MEJOR CASO.

    VERSION MVP: Solo analiza mejor caso con características específicas.

    Args:
        state: Estado actual con pseudocode poblado

    Returns:
        Estado actualizado con llm_analysis poblado con estructura:
        {
            "best_case": {
                "input_description": str,
                "num_iterations": int,
                "input_characteristics": dict
            }
        }
    """
    # DEBUG PRINT: Entrada al LLM
    print("=" * 60)
    print("ENTRADA AL LLM:")
    print("=" * 60)
    print(f"Algoritmo: {state.algorithm_name}")
    print(f"Pseudocódigo (primeras 200 chars):\n{state.pseudocode[:200]}...")
    print()

    try:
        # Obtener analizador LLM
        analyzer = get_llm_analyzer(temperature=0.0)

        # Analizar solo el mejor caso
        llm_result = analyzer.analyze_best_case_only(
            pseudocode=state.pseudocode,
            algorithm_name=state.algorithm_name
        )

        # DEBUG PRINT: Salida del LLM
        print("=" * 60)
        print("SALIDA DEL LLM (MEJOR CASO):")
        print("=" * 60)
        print(json.dumps(llm_result, indent=2, ensure_ascii=False))
        print()

        return state.model_copy(update={"llm_analysis": llm_result})

    except Exception as e:
        # Si LLM falla, usar heurística de respaldo
        print(f"\n[WARNING] LLM analysis failed: {str(e)}. Using fallback heuristics.\n")

        # Heurística de respaldo basada en detección de patrones
        llm_result = _fallback_best_case_analysis(state)

        # DEBUG PRINT: Salida del fallback
        print("=" * 60)
        print("SALIDA DEL FALLBACK (MEJOR CASO):")
        print("=" * 60)
        print(json.dumps(llm_result, indent=2, ensure_ascii=False))
        print()

        return state.model_copy(update={"llm_analysis": llm_result})


def _fallback_best_case_analysis(state: ScenarioState) -> Dict[str, Any]:
    """
    Análisis heurístico de respaldo si el LLM falla.

    VERSION MVP: Solo retorna características del MEJOR CASO.

    Usa reglas simples basadas en:
    - Variables de control detectadas
    - Presencia de salidas tempranas

    Args:
        state: Estado actual

    Returns:
        Dict con análisis del mejor caso:
        {
            "best_case": {
                "input_description": str,
                "num_iterations": int,
                "input_characteristics": dict
            }
        }
    """
    # Detectar si hay variables de control secundarias (salida temprana)
    has_early_exit = any(
        cv.type == "SECONDARY" and cv.affects_termination
        for cv in state.control_variables
    )

    if has_early_exit:
        # Algoritmos con salida temprana → mejor caso = primera iteración
        return {
            "best_case": {
                "input_description": "El elemento buscado se encuentra en la primera posición",
                "num_iterations": 1,
                "input_characteristics": {
                    "position": 1,
                    "found": True
                }
            }
        }

    else:
        # Algoritmos sin salida temprana → siempre n iteraciones
        # En este caso, el "mejor caso" es igual al caso general
        return {
            "best_case": {
                "input_description": "Cualquier entrada de tamaño n (algoritmo no es sensible)",
                "num_iterations": "n",  # Simbólico
                "input_characteristics": {
                    "sensitive": False
                }
            }
        }
