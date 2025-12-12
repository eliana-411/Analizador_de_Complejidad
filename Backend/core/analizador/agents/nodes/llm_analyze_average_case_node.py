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

        print("CONTEXTO para caso promedio:")
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
        print("RESULTADO DEL LLM:")
        print(f"  - Tipo: {llm_result.get('scenario_type')}")
        
        # Detectar formato y mostrar campos apropiados
        if "input_condition" in llm_result:
            # Formato nuevo (iterativo)
            print(f"  - Fórmula E[T]: {llm_result.get('average_cost_formula', 'N/A')[:80]}...")
            print(f"  - Costo T(S): {llm_result.get('T_of_S', 'N/A')}")
            print(f"  - Costo simplificado: {llm_result.get('T_of_S_simplified', 'N/A')}")
        else:
            # Formato antiguo (recursivo)
            print(f"  - Fórmula E[T]: {llm_result.get('average_cost_formula', 'N/A')[:80]}...")
            print(f"  - Costo simplificado: {llm_result.get('average_cost_simplified', 'N/A')}")

        # Contar escenarios intermedios
        breakdown = llm_result.get('scenarios_breakdown', [])
        print(f"  - Escenarios intermedios: {len(breakdown)}")
        print()

        # Convertir respuesta del LLM a escenarios
        scenarios = convert_average_case_to_scenarios(llm_result)

        print(f"[OK] Generados {len(scenarios)} escenarios del caso promedio")
        for scen in scenarios:
            print(f"  - {scen['id']}: {scen['condition'][:60]}...")
        print()

        # Agregar escenarios a los existentes
        updated_scenarios = list(state.raw_scenarios) + scenarios

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


def convert_average_case_to_scenarios(llm_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convierte respuesta del caso promedio a lista de escenarios.
    Compatible con ambos formatos: antiguo (recursivo) y nuevo (iterativo).

    El caso promedio puede generar múltiples escenarios intermedios:
    - S_1, S_2, ..., S_k (encontrado en posiciones)
    - S_∅ (no encontrado)
    - S_avg (escenario consolidado de promedio)

    NOTA: No incluye line_costs. El análisis completo se almacena en metadata.

    Args:
        llm_result: Dict con la respuesta del LLM

    Returns:
        Lista de escenarios en formato interno (estructura simplificada)
    """
    # Detectar formato
    is_new_format = "input_condition" in llm_result
    scenarios = []

    # Procesar scenarios_breakdown si existe
    if "scenarios_breakdown" in llm_result and llm_result["scenarios_breakdown"]:
        for scenario_info in llm_result["scenarios_breakdown"]:
            scenarios.append({
                "id": scenario_info.get("scenario_id", f"S_{len(scenarios)+1}"),
                "semantic_id": f"S_intermediate_{len(scenarios)+1}",
                "condition": scenario_info.get("description", ""),
                "state": "INTERMEDIATE",
                "cost_T": scenario_info.get("T", "n"),
                "probability_P": scenario_info.get("P", "1/n"),
                "input_description": scenario_info.get("description", ""),
                "input_characteristics": {}
            })

    # Agregar escenario consolidado de caso promedio
    # Extraer campos según formato
    if is_new_format:
        # Formato NUEVO (iterativo): input_condition, T_of_S, P_of_S
        condition = llm_result.get("input_condition", "Caso promedio (esperanza)")
        cost_T = llm_result.get("T_of_S_simplified", llm_result.get("T_of_S", "n"))
        probability_P = llm_result.get("P_of_S", "1")
    else:
        # Formato ANTIGUO (recursivo): input_description, total_cost_T, probability_P
        condition = llm_result.get("input_description", "Caso promedio (esperanza)")
        cost_T = llm_result.get("average_cost_simplified", llm_result.get("total_cost_T", "n"))
        probability_P = llm_result.get("probability_P", "1")
    
    scenarios.append({
        "id": "S_avg",
        "semantic_id": "average_case",
        "condition": condition,
        "state": "AVERAGE",
        "cost_T": cost_T,
        "probability_P": probability_P,
        "input_description": condition,
        "input_characteristics": {},
        "average_cost_formula": llm_result.get("average_cost_formula", ""),
        "average_cost_simplified": cost_T
    })

    return scenarios
