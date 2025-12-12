"""
Nodo: LLM Analyze Average Case - Análisis completo del caso promedio vía LLM

Este nodo invoca al LLM para realizar un análisis completo de complejidad
del CASO PROMEDIO, incluyendo:
- Identificación de todos los escenarios posibles
- Desglose de escenarios intermedios con T(S) y P(S)
- Cálculo de E[T] = Σ T(S)·P(S)
- Simplificación del costo promedio
"""

from typing import Dict, Any, List
from core.analizador.models.scenario_state import ScenarioState
from core.analizador.tools.llm_analyzer import LLMAnalyzer
from .llm_analyze_best_case_node import create_fallback_scenario


def llm_analyze_average_case_node(state: ScenarioState) -> ScenarioState:
    """
    Analiza el caso promedio usando LLM.

    El LLM recibe contexto de mejor y peor caso y genera:
    - Desglose de todos los escenarios intermedios
    - Costo T(S) y probabilidad P(S) de cada escenario
    - Fórmula del caso promedio E[T]
    - Costo promedio simplificado

    Args:
        state: Estado actual del workflow (debe tener mejor y peor caso ya analizados)

    Returns:
        Estado actualizado agregando escenarios intermedios y caso promedio
    """
    print("=" * 80)
    print("NODO: LLM Analyze Average Case")
    print("=" * 80)
    print(f"Algoritmo: {state.algorithm_name}")
    print(f"Tipo: {'Iterativo' if state.is_iterative else 'Recursivo'}")
    print(f"Escenarios previos: {len(state.raw_scenarios)}")
    print()

    try:
        # Extraer resúmenes de mejor y peor caso
        best_case_summary = _get_case_summary(state, "best_case")
        worst_case_summary = _get_case_summary(state, "worst_case")

        print("📋 CONTEXTO para caso promedio:")
        print(f"  - Mejor caso: {best_case_summary}")
        print(f"  - Peor caso: {worst_case_summary}")
        print()

        # Invocar LLM para análisis del caso promedio
        analyzer = LLMAnalyzer(temperature=0.0)

        print("[WAIT] Invocando LLM para análisis del CASO PROMEDIO...")
        llm_result = analyzer.analyze_average_case(
            pseudocode=state.pseudocode,
            algorithm_name=state.algorithm_name,
            is_iterative=state.is_iterative,
            best_case_summary=best_case_summary,
            worst_case_summary=worst_case_summary
        )

        print("[OK] LLM respondió exitosamente")
        print()
        print("📊 RESULTADO DEL LLM:")
        print(f"  - Tipo: {llm_result.get('scenario_type')}")
        print(f"  - Fórmula E[T]: {llm_result.get('average_cost_formula', 'N/A')[:80]}...")
        print(f"  - Costo simplificado: {llm_result.get('average_cost_simplified')}")

        # Contar escenarios intermedios
        breakdown = llm_result.get('scenarios_breakdown', [])
        print(f"  - Escenarios intermedios: {len(breakdown)}")
        print()

        # Convertir respuesta del LLM a escenarios
        scenarios = convert_average_case_to_scenarios(llm_result, state.is_iterative)

        print(f"[OK] Generados {len(scenarios)} escenarios del caso promedio")
        for scen in scenarios:
            print(f"  - {scen['id']}: {scen['condition'][:60]}...")
        print()

        # Agregar escenarios a los existentes (incluyendo el escenario S_avg)
        # Primero agregar escenarios intermedios, luego el escenario agregado
        updated_scenarios = list(state.raw_scenarios) + scenarios
        
        # Crear escenario agregado del caso promedio (S_avg)
        avg_scenario = {
            "id": "S_avg",
            "semantic_id": "average_case",
            "condition": llm_result.get("input_condition", "Caso promedio"),
            "state": "AVERAGE",
            "cost_T": llm_result.get("T_of_S_simplified") or llm_result.get("T_of_S", "n"),
            "probability_P": llm_result.get("P_of_S", "1"),
            "input_description": llm_result.get("input_condition", ""),
            "input_characteristics": {},
            "average_cost_formula": llm_result.get("average_cost_formula", ""),
            "average_cost_simplified": llm_result.get("T_of_S_simplified", "")
        }
        updated_scenarios.append(avg_scenario)

        # Actualizar análisis LLM con caso promedio
        updated_llm_analysis = dict(state.llm_analysis) if state.llm_analysis else {}
        updated_llm_analysis["average_case"] = llm_result

        return state.model_copy(update={
            "raw_scenarios": updated_scenarios,
            "llm_analysis": updated_llm_analysis
        })

    except Exception as e:
        print(f"[ERROR] ERROR en análisis LLM: {str(e)}")
        print()

        # Agregar error al estado
        errors = list(state.errors) if state.errors else []
        errors.append(f"Error en análisis LLM de caso promedio: {str(e)}")

        # Para caso promedio, no agregar fallback si falla
        # (los casos mejor y peor ya están)
        print("[WARN]  Caso promedio no generado - continuando con mejor/peor caso")

        return state.model_copy(update={"errors": errors})


def _get_case_summary(state: ScenarioState, case_type: str) -> str:
    """
    Extrae resumen de un caso ya analizado para pasarlo como contexto.

    Args:
        state: Estado actual del workflow
        case_type: "best_case" o "worst_case"

    Returns:
        String con resumen del caso (T(S) y P(S))
    """
    if not state.llm_analysis or case_type not in state.llm_analysis:
        return "No disponible"

    case_data = state.llm_analysis[case_type]
    cost_T = case_data.get("total_cost_T", "n")
    prob_P = case_data.get("probability_P", "1")

    return f"T(S) = {cost_T}, P(S) = {prob_P}"


def convert_average_case_to_scenarios(llm_result: Dict[str, Any], is_iterative: bool) -> List[Dict[str, Any]]:
    """
    Convierte respuesta del caso promedio a lista de escenarios INTERMEDIOS.

    El caso promedio puede generar múltiples escenarios intermedios:
    - S_1, S_2, ..., S_k (encontrado en posiciones)
    - S_∅ (no encontrado)

    NOTA: No incluye el escenario S_avg consolidado, ese se agrega después.
    NOTA: No incluye line_costs. El análisis completo se almacena en metadata.

    Args:
        llm_result: Dict con la respuesta del LLM
        is_iterative: True si el algoritmo es iterativo, False si es recursivo

    Returns:
        Lista de escenarios intermedios en formato interno
    """
    scenarios = []

    # Procesar scenarios_breakdown si existe (solo escenarios intermedios)
    if "scenarios_breakdown" in llm_result and llm_result["scenarios_breakdown"]:
        for idx, scenario_info in enumerate(llm_result["scenarios_breakdown"], 1):
            description = scenario_info.get("description", "")
            scenarios.append({
                "id": scenario_info.get("scenario_id", f"S_intermediate_{idx}"),
                "semantic_id": f"S_intermediate_{idx}",
                "condition": description,
                "state": "INTERMEDIATE",
                "cost_T": scenario_info.get("T", "n"),
                "probability_P": scenario_info.get("P", "1/n"),
                "input_description": description,
                "input_characteristics": {}
                # NOTA: Los escenarios intermedios NO llevan is_iterative según la estructura de referencia
            })

    return scenarios
