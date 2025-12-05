"""
Script de Integración: Analizador → Representación Matemática

Este script ejecuta el workflow del analizador y luego envía
los resultados al módulo de representación matemática.

Uso:
    python integrar_con_representacion.py
"""

from core.analizador.models.scenario_state import ScenarioState
from core.analizador.agents.workflow import get_workflow


def analizar_algoritmo(pseudocode: str, algorithm_name: str, is_iterative: bool):
    """
    Ejecuta el análisis de complejidad de un algoritmo.

    Args:
        pseudocode: Pseudocódigo del algoritmo
        algorithm_name: Nombre del algoritmo
        is_iterative: True si es iterativo, False si recursivo

    Returns:
        OmegaTable con el análisis completo
    """
    print("=" * 80)
    print("PASO 1: ANÁLISIS DE COMPLEJIDAD")
    print("=" * 80)
    print()

    # Crear estado inicial
    state = ScenarioState(
        pseudocode=pseudocode,
        algorithm_name=algorithm_name,
        is_iterative=is_iterative,
        parameters={}
    )

    # Ejecutar workflow
    workflow = get_workflow()
    resultado = workflow.invoke(state)

    # Verificar resultado
    if not resultado.get("omega_table"):
        print("[ERROR] No se generó omega_table")
        if resultado.get("errors"):
            print("\nErrores:")
            for error in resultado["errors"]:
                print(f"  - {error}")
        return None

    omega_table = resultado["omega_table"]

    print(f"[OK] Tabla Omega generada para '{algorithm_name}'")
    print(f"     - Escenarios: {len(omega_table.scenarios)}")
    print(f"     - Tipo: {omega_table.metadata.get('algorithm_type')}")
    print()

    return omega_table


def enviar_a_representacion(omega_table):
    """
    Envía la OmegaTable al módulo de representación matemática.

    Args:
        omega_table: OmegaTable generada por el analizador

    Returns:
        Resultado del módulo de representación
    """
    print("=" * 80)
    print("PASO 2: REPRESENTACIÓN MATEMÁTICA")
    print("=" * 80)
    print()

    # Preparar datos en formato esperado
    datos_para_representacion = {
        "algorithm_name": omega_table.algorithm_name,
        "algorithm_type": omega_table.metadata.get("algorithm_type"),

        # Escenarios simplificados
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

        # Resúmenes de casos
        "best_case": omega_table.metadata.get("best_case"),
        "worst_case": omega_table.metadata.get("worst_case"),
        "average_case": omega_table.metadata.get("average_case"),

        # Análisis detallado (opcional)
        "detailed_analysis": omega_table.metadata.get("llm_analysis"),

        # Variables de control
        "control_variables": omega_table.control_variables
    }

    print("Datos preparados para envío:")
    print(f"  - Algoritmo: {datos_para_representacion['algorithm_name']}")
    print(f"  - Tipo: {datos_para_representacion['algorithm_type']}")
    print(f"  - Escenarios: {len(datos_para_representacion['scenarios'])}")
    print()

    # TODO: Aquí integrar con el módulo de representación matemática
    # Ejemplo de cómo sería:

    print("[INFO] Invocando módulo de representación matemática...")
    print()

    # try:
    #     # Importar módulo de representación
    #     from core.representacion_matematica.processor import procesar_tabla_omega
    #
    #     # Procesar tabla
    #     resultado = procesar_tabla_omega(datos_para_representacion)
    #
    #     print("[OK] Representación matemática completada")
    #     return resultado
    #
    # except ImportError:
    #     print("[WARN] Módulo de representación matemática no encontrado")
    #     print("       Asegúrate de que core.representacion_matematica existe")
    #     return None
    #
    # except Exception as e:
    #     print(f"[ERROR] Error al procesar con representación matemática: {e}")
    #     return None

    # Por ahora, solo mostramos los datos que se enviarían
    print("DATOS QUE SE ENVIARÍAN:")
    print("-" * 80)
    print()

    print("1. MEJOR CASO:")
    if datos_para_representacion["best_case"]:
        print(f"   T(S) = {datos_para_representacion['best_case'].get('T', 'N/A')}")
        print(f"   P(S) = {datos_para_representacion['best_case'].get('P', 'N/A')}")
    print()

    print("2. PEOR CASO:")
    if datos_para_representacion["worst_case"]:
        print(f"   T(S) = {datos_para_representacion['worst_case'].get('T', 'N/A')}")
        print(f"   P(S) = {datos_para_representacion['worst_case'].get('P', 'N/A')}")
    print()

    print("3. CASO PROMEDIO:")
    if datos_para_representacion["average_case"]:
        print(f"   E[T] = {datos_para_representacion['average_case'].get('T_avg', 'N/A')}")
    print()

    print("4. ESCENARIOS:")
    for scenario in datos_para_representacion["scenarios"]:
        print(f"   - {scenario['id']}: T={scenario['cost_T']}, P={scenario['probability_P']}")
    print()

    print("[INFO] Integración con módulo de representación pendiente")
    print("       Implementa la función procesar_tabla_omega() en tu módulo")
    print()

    return datos_para_representacion


def main():
    """Función principal de integración"""

    # Ejemplo: Búsqueda Lineal
    pseudocode = """busquedaLineal(int A[], int n, int x)
begin
    int i
    bool encontrado

    encontrado <- F
    i <- 1

    while (i <= n and not encontrado) do
    begin
        if (A[i] = x) then
        begin
            encontrado <- T
        end
        i <- i + 1
    end

    return encontrado
end"""

    algorithm_name = "busquedaLineal"
    is_iterative = True

    # PASO 1: Analizar con el módulo analizador
    omega_table = analizar_algoritmo(pseudocode, algorithm_name, is_iterative)

    if not omega_table:
        print("\n[ERROR] No se pudo generar omega_table")
        return

    # PASO 2: Enviar al módulo de representación matemática
    resultado_representacion = enviar_a_representacion(omega_table)

    # PASO 3: Mostrar resultado final
    print("=" * 80)
    print("PROCESO COMPLETADO")
    print("=" * 80)
    print()
    print("[OK] Análisis de complejidad completado")
    print("[INFO] Para usar la representación matemática, implementa el módulo correspondiente")
    print()


if __name__ == "__main__":
    main()
