"""
Nodo: LLM Analyze Best Case - Análisis completo del mejor caso vía LLM

Este nodo invoca al LLM para realizar un análisis completo de complejidad
del MEJOR CASO, incluyendo:
- Identificación de entrada que minimiza operaciones
- Análisis línea por línea con C_op, Freq, Total
- Cálculo de costo total T(S)
- Cálculo de probabilidad P(S)
"""

from typing import Dict, Any
from core.analizador.models.scenario_state import ScenarioState
from core.analizador.tools.llm_analyzer import LLMAnalyzer


def llm_analyze_best_case_node(state: ScenarioState) -> ScenarioState:
    """
    Analiza el mejor caso usando LLM con análisis línea por línea completo.

    El LLM es responsable de:
    - Identificar qué entrada causa el mejor caso
    - Contar operaciones elementales línea por línea
    - Calcular frecuencias considerando loops y regla n+1
    - Aplicar regla n+1 para encabezados de loops
    - Calcular probabilidad P(S)
    - Generar costo total (iterativo: fórmula cerrada, recursivo: recurrencia)

    Args:
        state: Estado actual del workflow con pseudocode, algorithm_name, is_iterative

    Returns:
        Estado actualizado con raw_scenarios poblado con el escenario de mejor caso
    """
    print("=" * 80)
    print("NODO: LLM Analyze Best Case")
    print("=" * 80)
    print(f"Algoritmo: {state.algorithm_name}")
    print(f"Tipo: {'Iterativo' if state.is_iterative else 'Recursivo'}")
    print(f"Líneas de código: {len(state.lines) if state.lines else 0}")
    print()

    try:
        # Invocar LLM para análisis completo del mejor caso
        analyzer = LLMAnalyzer(temperature=0.0)

        print("[WAIT] Invocando LLM para análisis del MEJOR CASO...")
        llm_result = analyzer.analyze_best_case(
            pseudocode=state.pseudocode,
            algorithm_name=state.algorithm_name,
            is_iterative=state.is_iterative
        )

        print("[OK] LLM respondió exitosamente")
        print()
        print("RESULTADO DEL LLM:")
        print(f"  - Tipo: {llm_result.get('scenario_type')}")
        
        # Detectar formato y mostrar campos apropiados
        if "input_condition" in llm_result:
            # Formato nuevo (iterativo)
            print(f"  - Entrada: {llm_result.get('input_condition', 'N/A')[:80]}...")
            print(f"  - Costo T(S): {llm_result.get('T_of_S')}")
            print(f"  - Probabilidad P(S): {llm_result.get('P_of_S')}")
        else:
            # Formato antiguo (recursivo)
            print(f"  - Entrada: {llm_result.get('input_description', 'N/A')[:80]}...")
            print(f"  - Costo T(S): {llm_result.get('total_cost_T')}")
            print(f"  - Probabilidad P(S): {llm_result.get('probability_P')}")

        if state.is_iterative:
            num_lines = len(llm_result.get('line_by_line_analysis', []))
            print(f"  - Líneas analizadas: {num_lines}")
        else:
            print(f"  - Recurrencia: {llm_result.get('recurrence_relation', 'N/A')}")
        print()

        # Convertir respuesta del LLM a formato interno
        scenario = convert_llm_to_scenario(llm_result, "best_case")

        print("[OK] Escenario convertido a formato interno")
        print(f"  - ID: {scenario['id']}")
        print(f"  - Semantic ID: {scenario['semantic_id']}")
        print()

        # Actualizar estado con el escenario de mejor caso
        return state.model_copy(update={
            "raw_scenarios": [scenario],
            "llm_analysis": {"best_case": llm_result}
        })

    except Exception as e:
        print(f"[ERROR] ERROR en análisis LLM: {str(e)}")
        print()

        # Agregar error al estado
        errors = list(state.errors) if state.errors else []
        errors.append(f"Error en análisis LLM de mejor caso: {str(e)}")

        # Crear escenario de fallback
        print("[WARN]  Usando escenario de fallback...")
        fallback_scenario = create_fallback_scenario(state, "best_case")

        return state.model_copy(update={
            "raw_scenarios": [fallback_scenario],
            "errors": errors
        })


def convert_llm_to_scenario(llm_result: Dict[str, Any], scenario_type: str) -> Dict[str, Any]:
    """
    Convierte respuesta del LLM al formato ScenarioEntry esperado.
    Compatible con ambos formatos: antiguo (recursivo) y nuevo (iterativo).

    NOTA: No incluye line_costs en el escenario. El análisis línea por línea
    completo se almacena en state.llm_analysis y luego en metadata.

    Args:
        llm_result: Dict con la respuesta del LLM
        scenario_type: "best_case", "worst_case", "average_case"

    Returns:
        Dict con formato compatible con ScenarioEntry (estructura simplificada)
    """
    # Detectar formato: nuevo iterativo usa 'input_condition', antiguo usa 'input_description'
    is_new_format = "input_condition" in llm_result
    
    # Extraer campos según formato
    if is_new_format:
        # Formato NUEVO (iterativo): input_condition, T_of_S, P_of_S
        condition = llm_result.get("input_condition", "")
        cost_T = llm_result.get("T_of_S", "n")
        probability_P = llm_result.get("P_of_S", "1")
    else:
        # Formato ANTIGUO (recursivo): input_description, total_cost_T, probability_P
        condition = llm_result.get("input_description", "")
        cost_T = llm_result.get("total_cost_T", "n")
        probability_P = llm_result.get("probability_P", "1")
    
    # Construir escenario en formato interno (sin line_costs)
    scenario = {
        "id": f"S_{scenario_type}",
        "semantic_id": scenario_type,
        "condition": condition,
        "state": scenario_type.upper(),
        "cost_T": cost_T,
        "probability_P": probability_P,
        "input_description": condition,  # Mantener para compatibilidad
        "input_characteristics": llm_result.get("input_characteristics", {}),
        "is_iterative": llm_result.get("is_iterative", True)
    }

    # Para recursivos, agregar información de recurrencia
    if not llm_result.get("is_iterative", True):
        scenario["recurrence_relation"] = llm_result.get("recurrence_relation", "")
        scenario["base_case_cost"] = llm_result.get("base_case_cost", "")
        scenario["base_case_condition"] = llm_result.get("base_case_condition", "")

    return scenario


def create_fallback_scenario(state: ScenarioState, scenario_type: str) -> Dict[str, Any]:
    """
    Crea escenario de fallback si el LLM falla.

    Args:
        state: Estado actual del workflow
        scenario_type: "best_case", "worst_case", "average_case"

    Returns:
        Dict con escenario genérico básico (estructura simplificada)
    """
    # Determinar descripción según tipo
    descriptions = {
        "best_case": "Mejor caso (fallback heurístico)",
        "worst_case": "Peor caso (fallback heurístico)",
        "average_case": "Caso promedio (fallback heurístico)"
    }

    # Determinar costo básico según tipo
    costs = {
        "best_case": "1" if state.is_iterative else "T(n) = 1",
        "worst_case": "n" if state.is_iterative else "T(n) = T(n-1) + 1",
        "average_case": "n/2" if state.is_iterative else "T(n) = T(n/2) + 1"
    }

    return {
        "id": f"S_{scenario_type}_fallback",
        "semantic_id": f"{scenario_type}_fallback",
        "condition": descriptions.get(scenario_type, "Escenario desconocido"),
        "state": scenario_type.upper(),
        "cost_T": costs.get(scenario_type, "n"),
        "probability_P": "1",
        "input_description": descriptions.get(scenario_type, ""),
        "input_characteristics": {},
        "is_iterative": state.is_iterative
    }
