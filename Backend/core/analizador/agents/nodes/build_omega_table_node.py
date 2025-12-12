"""
Nodo: Build Omega Table - Ensambla la Tabla Ω final

Convierte raw_scenarios en estructura OmegaTable con ScenarioEntry.
Construye el CaseSummary desde los 3 escenarios analizados por el LLM.
"""

from core.analizador.models.omega_table import OmegaTable, ScenarioEntry
from core.analizador.models.scenario_state import ScenarioState


def build_omega_table_node(state: ScenarioState) -> ScenarioState:
    """
    Construye la Tabla Ω final a partir de los escenarios procesados por el LLM.

    En el nuevo workflow simplificado:
    - Los 3 primeros escenarios en raw_scenarios son: mejor, peor, promedio
    - Pueden haber escenarios intermedios adicionales del caso promedio
    - El CaseSummary se construye automáticamente desde estos escenarios

    Args:
        state: Estado actual con 'raw_scenarios' poblado por LLM

    Returns:
        Estado actualizado con 'omega_table' poblada (incluyendo resumen)
    """
    print("=" * 80)
    print("NODO: Build Omega Table")
    print("=" * 80)
    print(f"Escenarios recibidos: {len(state.raw_scenarios)}")
    print()

    scenario_entries = []

    for raw_scenario in state.raw_scenarios:
        # Convertir diccionario a ScenarioEntry (estructura simplificada)
        entry = ScenarioEntry(
            id=raw_scenario["id"],
            semantic_id=raw_scenario.get("semantic_id", ""),
            condition=raw_scenario["condition"],
            state=raw_scenario["state"],
            cost_T=raw_scenario.get("cost_T", "0"),
            probability_P=raw_scenario.get("probability_P", "0")
        )

        scenario_entries.append(entry)
        print(f"  [OK] Escenario: {entry.id} - {entry.condition[:60]}...")

    print()

    # Construir resumen de casos desde el análisis LLM
    case_summary_metadata = build_case_summary_metadata(state)

    if case_summary_metadata:
        print("RESUMEN DE CASOS:")
        print(f"  - Mejor caso: T={case_summary_metadata['best_case']['T']}, P={case_summary_metadata['best_case']['P']}")
        print(f"  - Peor caso: T={case_summary_metadata['worst_case']['T']}, P={case_summary_metadata['worst_case']['P']}")
        if case_summary_metadata.get('average_case'):
            print(f"  - Caso promedio: {case_summary_metadata['average_case'].get('T_avg', 'N/A')}")
    else:
        print("[WARN]  No se pudo construir resumen de casos")

    print()

    # Construir metadata completa (incluye análisis LLM detallado)
    metadata = {
        "algorithm_type": "iterative" if state.is_iterative else "recursive",
        "loop_count": len(state.loops) if state.loops else 0,
        "nesting_level": max(
            [loop.nesting_level for loop in state.loops], default=0
        ) if state.loops else 0,
        "parameters": state.parameters,
        "llm_analysis": state.llm_analysis if state.llm_analysis else {},
        "best_case": case_summary_metadata.get("best_case") if case_summary_metadata else {},
        "worst_case": case_summary_metadata.get("worst_case") if case_summary_metadata else {},
        "average_case": case_summary_metadata.get("average_case") if case_summary_metadata else {}
    }

    # Construir tabla completa (sin summary)
    omega_table = OmegaTable(
        algorithm_name=state.algorithm_name,
        scenarios=scenario_entries,
        control_variables=[cv.name for cv in state.control_variables] if state.control_variables else [],
        metadata=metadata
    )

    print(f"[OK] Tabla Omega construida: {len(scenario_entries)} escenarios")
    print()

    return state.model_copy(update={"omega_table": omega_table})


def build_case_summary_metadata(state: ScenarioState) -> dict | None:
    """
    Construye metadata de resumen desde el análisis LLM.

    Extrae información de mejor, peor y promedio caso desde state.llm_analysis
    y raw_scenarios para construir un dict que va en metadata.

    Args:
        state: Estado con llm_analysis y raw_scenarios

    Returns:
        Dict con best_case, worst_case, average_case o None si faltan datos
    """
    if not state.llm_analysis:
        return None

    best_scenario = None
    worst_scenario = None
    avg_scenario = None

    # Buscar escenarios por semantic_id
    for scenario in state.raw_scenarios:
        semantic_id = scenario.get("semantic_id", "")

        if semantic_id == "best_case":
            best_scenario = scenario
        elif semantic_id == "worst_case":
            worst_scenario = scenario
        elif semantic_id == "average_case":
            avg_scenario = scenario

    # Validar que se encontraron mejor y peor caso (mínimo)
    if not best_scenario or not worst_scenario:
        return None

    # Construir dict para mejor caso
    best_case_dict = {
        "scenario_id": best_scenario["id"],
        "semantic_id": "best_case",
        "T": best_scenario.get("cost_T", "n"),
        "P": best_scenario.get("probability_P", "1"),
        "description": best_scenario.get("input_description", "Mejor caso"),
        "input_characteristics": state.llm_analysis.get("best_case", {}).get("input_characteristics", {})
    }

    # Construir dict para peor caso
    worst_case_dict = {
        "scenario_id": worst_scenario["id"],
        "semantic_id": "worst_case",
        "T": worst_scenario.get("cost_T", "n"),
        "P": worst_scenario.get("probability_P", "1"),
        "description": worst_scenario.get("input_description", "Peor caso"),
        "input_characteristics": state.llm_analysis.get("worst_case", {}).get("input_characteristics", {})
    }

    # Construir dict para caso promedio
    average_case_dict = {}
    if avg_scenario:
        average_case_dict = {
            "scenario_id": avg_scenario["id"],
            "semantic_id": "average_case",
            "T_avg": avg_scenario.get("cost_T", "n"),
            "formula": avg_scenario.get("average_cost_formula", ""),
            "simplified": avg_scenario.get("average_cost_simplified", avg_scenario.get("cost_T", "n")),
            "description": avg_scenario.get("input_description", "Caso promedio"),
            "scenarios_breakdown": state.llm_analysis.get("average_case", {}).get("scenarios_breakdown", [])
        }
    else:
        # Si no hay caso promedio, usar valores por defecto
        average_case_dict = {
            "T_avg": "n",
            "formula": "Caso promedio no calculado"
        }

    return {
        "best_case": best_case_dict,
        "worst_case": worst_case_dict,
        "average_case": average_case_dict
    }
