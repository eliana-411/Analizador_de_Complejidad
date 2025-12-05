"""
Nodo: Send to Representation - Envía OmegaTable al módulo de representación matemática

Este es el último nodo del workflow, que toma la OmegaTable generada
y la envía al módulo de representación matemática para procesamiento.
"""

from core.analizador.models.scenario_state import ScenarioState


def send_to_representation_node(state: ScenarioState) -> ScenarioState:
    """
    Envía la OmegaTable al módulo de representación matemática.

    Este nodo:
    1. Valida que omega_table existe
    2. Prepara los datos en formato esperado por el módulo de representación
    3. Invoca el módulo de representación (cuando esté disponible)
    4. Almacena el resultado en el state

    Args:
        state: Estado con omega_table generada

    Returns:
        Estado actualizado con resultado de representación matemática
    """
    print("=" * 80)
    print("NODO: Send to Representation")
    print("=" * 80)
    print()

    if not state.omega_table:
        print("[ERROR] No hay omega_table para enviar")
        errors = list(state.errors) if state.errors else []
        errors.append("No se pudo enviar al módulo de representación: omega_table faltante")
        return state.model_copy(update={"errors": errors})

    omega_table = state.omega_table

    print(f"Preparando envío de OmegaTable: {omega_table.algorithm_name}")
    print(f"  - Escenarios: {len(omega_table.scenarios)}")
    print(f"  - Tipo: {omega_table.metadata.get('algorithm_type', 'N/A')}")
    print()

    # TODO: Aquí va la integración con el módulo de representación matemática
    # Por ahora, solo preparamos los datos en el formato correcto

    print("[INFO] Tabla Omega lista para ser procesada por módulo de representación")
    print()
    print("Estructura de datos enviada:")
    print(f"  - algorithm_name: {omega_table.algorithm_name}")
    print(f"  - control_variables: {omega_table.control_variables}")
    print(f"  - scenarios: {len(omega_table.scenarios)} escenarios")
    print(f"  - metadata.algorithm_type: {omega_table.metadata.get('algorithm_type')}")
    print(f"  - metadata.best_case: {omega_table.metadata.get('best_case', {}).get('T', 'N/A')}")
    print(f"  - metadata.worst_case: {omega_table.metadata.get('worst_case', {}).get('T', 'N/A')}")
    print()

    # Ejemplo de cómo sería la integración (cuando el módulo exista):
    # try:
    #     from core.representacion_matematica import procesar_tabla_omega
    #
    #     resultado_representacion = procesar_tabla_omega(omega_table)
    #
    #     return state.model_copy(update={
    #         "representation_result": resultado_representacion
    #     })
    # except Exception as e:
    #     print(f"[ERROR] Fallo al procesar con módulo de representación: {e}")
    #     errors = list(state.errors) if state.errors else []
    #     errors.append(f"Error en representación matemática: {str(e)}")
    #     return state.model_copy(update={"errors": errors})

    print("[OK] Nodo de envío completado (integración pendiente)")
    print()

    # Por ahora, solo retornamos el state sin cambios
    return state


def prepare_omega_table_for_representation(omega_table):
    """
    Prepara la OmegaTable en el formato esperado por el módulo de representación.

    Args:
        omega_table: OmegaTable generada por el workflow

    Returns:
        Dict con datos formateados para representación matemática
    """
    return {
        "algorithm_name": omega_table.algorithm_name,
        "algorithm_type": omega_table.metadata.get("algorithm_type"),
        "scenarios": [
            {
                "id": s.id,
                "semantic_id": s.semantic_id,
                "cost_T": s.cost_T,
                "probability_P": s.probability_P,
                "condition": s.condition
            }
            for s in omega_table.scenarios
        ],
        "best_case": omega_table.metadata.get("best_case"),
        "worst_case": omega_table.metadata.get("worst_case"),
        "average_case": omega_table.metadata.get("average_case"),
        "detailed_analysis": omega_table.metadata.get("llm_analysis"),
        "control_variables": omega_table.control_variables
    }
