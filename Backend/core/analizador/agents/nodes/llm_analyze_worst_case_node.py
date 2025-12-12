"""
Nodo: LLM Analyze Worst Case - Análisis completo del peor caso vía LLM

Este nodo invoca al LLM para realizar un análisis completo de complejidad
del PEOR CASO, incluyendo:
- Identificación de entrada que maximiza operaciones
- Análisis línea por línea con C_op, Freq, Total
- Cálculo de costo total T(S)
- Cálculo de probabilidad P(S)
"""

from typing import Dict, Any
from core.analizador.models.scenario_state import ScenarioState
from core.analizador.tools.llm_analyzer import LLMAnalyzer
# Reutilizar funciones del nodo de mejor caso
from .llm_analyze_best_case_node import convert_llm_to_scenario, create_fallback_scenario


def llm_analyze_worst_case_node(state: ScenarioState) -> ScenarioState:
    """
    Analiza el peor caso usando LLM con análisis línea por línea completo.

    El LLM es responsable de:
    - Identificar qué entrada causa el peor caso
    - Contar operaciones elementales línea por línea
    - Calcular frecuencias para el peor escenario
    - Aplicar regla n+1 para encabezados de loops
    - Calcular probabilidad P(S)
    - Generar costo total

    Args:
        state: Estado actual del workflow (debe tener mejor caso ya analizado)

    Returns:
        Estado actualizado agregando el escenario de peor caso a raw_scenarios
    """
    print("=" * 80)
    print("NODO: LLM Analyze Worst Case")
    print("=" * 80)
    print(f"Algoritmo: {state.algorithm_name}")
    print(f"Tipo: {'Iterativo' if state.is_iterative else 'Recursivo'}")
    print(f"Escenarios previos: {len(state.raw_scenarios)}")
    print()

    try:
        # Invocar LLM para análisis completo del peor caso
        analyzer = LLMAnalyzer(temperature=0.0)

        print("[WAIT] Invocando LLM para análisis del PEOR CASO...")
        llm_result = analyzer.analyze_worst_case(
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
        scenario = convert_llm_to_scenario(llm_result, "worst_case")

        print("[OK] Escenario convertido a formato interno")
        print(f"  - ID: {scenario['id']}")
        print(f"  - Semantic ID: {scenario['semantic_id']}")
        print()

        # Agregar escenario de peor caso a los existentes
        updated_scenarios = list(state.raw_scenarios) + [scenario]

        # Actualizar análisis LLM con peor caso
        updated_llm_analysis = dict(state.llm_analysis) if state.llm_analysis else {}
        updated_llm_analysis["worst_case"] = llm_result

        return state.model_copy(update={
            "raw_scenarios": updated_scenarios,
            "llm_analysis": updated_llm_analysis
        })

    except Exception as e:
        print(f"[ERROR] ERROR en análisis LLM: {str(e)}")
        print()

        # Agregar error al estado
        errors = list(state.errors) if state.errors else []
        errors.append(f"Error en análisis LLM de peor caso: {str(e)}")

        # Crear escenario de fallback
        print("[WARN]  Usando escenario de fallback...")
        fallback_scenario = create_fallback_scenario(state, "worst_case")

        updated_scenarios = list(state.raw_scenarios) + [fallback_scenario]

        return state.model_copy(update={
            "raw_scenarios": updated_scenarios,
            "errors": errors
        })
