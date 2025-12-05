"""
Test de Flujo Completo - Workflow de 5 Nodos

Script simple para probar el workflow completo.
Solo necesitas definir el pseudocódigo y si es iterativo/recursivo.

Muestra el output de cada nodo en tiempo real.

Uso:
    python test_flujo_completo.py
"""

from core.analizador.models.scenario_state import ScenarioState
from core.analizador.agents.workflow import get_workflow


# ==========================================
# CONFIGURACIÓN: Cambia estos valores
# ==========================================

# Opción 1: Búsqueda Lineal (Iterativo)
ALGORITMO = """busquedaLineal(int A[], int n, int x)
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

ES_ITERATIVO = True
NOMBRE_ALGORITMO = "busquedaLineal"


# Opción 2: Factorial (Recursivo) - Descomenta para probar
# ALGORITMO = """factorial(int n)
# begin
#     if (n = 0) then
#     begin
#         return 1
#     end
#     else
#     begin
#         return n * factorial(n-1)
#     end
# end"""
#
# ES_ITERATIVO = False
# NOMBRE_ALGORITMO = "factorial"


# Opción 3: Suma (Iterativo simple) - Descomenta para probar
# ALGORITMO = """suma(int A[], int n)
# begin
#     int s
#     int i
#
#     s <- 0
#     i <- 1
#
#     while (i <= n) do
#     begin
#         s <- s + A[i]
#         i <- i + 1
#     end
#
#     return s
# end"""
#
# ES_ITERATIVO = True
# NOMBRE_ALGORITMO = "suma"


# ==========================================
# EJECUCIÓN DEL WORKFLOW
# ==========================================

def main():
    """Ejecuta el workflow completo y muestra resultados"""

    print("\n" + "=" * 80)
    print("TEST DE FLUJO COMPLETO - WORKFLOW DE 5 NODOS")
    print("=" * 80)
    print(f"\nAlgoritmo: {NOMBRE_ALGORITMO}")
    print(f"Tipo: {'Iterativo' if ES_ITERATIVO else 'Recursivo'}")
    print("=" * 80)
    print()

    # Crear estado inicial
    estado_inicial = ScenarioState(
        pseudocode=ALGORITMO,
        algorithm_name=NOMBRE_ALGORITMO,
        is_iterative=ES_ITERATIVO,
        parameters={}
    )

    # Obtener workflow
    print("Obteniendo workflow...")
    workflow = get_workflow()
    print()

    # Ejecutar workflow (los nodos imprimen automáticamente)
    print("INICIANDO EJECUCIÓN DEL WORKFLOW:")
    print("=" * 80)
    print()

    resultado_final = workflow.invoke(estado_inicial)

    # ==========================================
    # MOSTRAR RESULTADOS FINALES
    # ==========================================

    print("\n" + "=" * 80)
    print("RESULTADOS FINALES")
    print("=" * 80)

    # Verificar si se generó tabla
    if not resultado_final.get("omega_table"):
        print("\n[ERROR] No se generó omega_table")

        # Mostrar errores
        if resultado_final.get("errors"):
            print("\nERRORES DETECTADOS:")
            for i, error in enumerate(resultado_final["errors"], 1):
                print(f"  {i}. {error}")

        return

    omega_table = resultado_final["omega_table"]

    # ==========================================
    # 1. INFORMACIÓN GENERAL
    # ==========================================
    print("\n1. INFORMACIÓN GENERAL")
    print("-" * 80)
    print(f"   Algoritmo: {omega_table.algorithm_name}")
    print(f"   Tipo: {omega_table.metadata.get('algorithm_type', 'N/A')}")
    print(f"   Control variables: {', '.join(omega_table.control_variables) if omega_table.control_variables else 'N/A'}")
    print(f"   Loops detectados: {omega_table.metadata.get('loop_count', 0)}")
    print(f"   Nivel de anidamiento: {omega_table.metadata.get('nesting_level', 0)}")

    # ==========================================
    # 2. ESCENARIOS GENERADOS
    # ==========================================
    print("\n2. ESCENARIOS GENERADOS")
    print("-" * 80)
    print(f"   Total de escenarios: {len(omega_table.scenarios)}")
    print()

    for i, scenario in enumerate(omega_table.scenarios, 1):
        print(f"   Escenario {i}: {scenario.id}")
        print(f"      Tipo semántico: {scenario.semantic_id}")
        print(f"      Condición: {scenario.condition[:80]}...")
        print(f"      Estado: {scenario.state}")
        print(f"      Costo T(S): {scenario.cost_T}")
        print(f"      Probabilidad P(S): {scenario.probability_P}")
        print()

    # ==========================================
    # 3. RESUMEN DE CASOS
    # ==========================================
    print("3. RESUMEN DE CASOS")
    print("-" * 80)

    if 'best_case' in omega_table.metadata and omega_table.metadata['best_case']:
        best = omega_table.metadata['best_case']
        print(f"   MEJOR CASO:")
        print(f"      T(S) = {best.get('T', 'N/A')}")
        print(f"      P(S) = {best.get('P', 'N/A')}")
        print(f"      Descripción: {best.get('description', 'N/A')[:60]}...")
        print()

    if 'worst_case' in omega_table.metadata and omega_table.metadata['worst_case']:
        worst = omega_table.metadata['worst_case']
        print(f"   PEOR CASO:")
        print(f"      T(S) = {worst.get('T', 'N/A')}")
        print(f"      P(S) = {worst.get('P', 'N/A')}")
        print(f"      Descripción: {worst.get('description', 'N/A')[:60]}...")
        print()

    if 'average_case' in omega_table.metadata and omega_table.metadata['average_case']:
        avg = omega_table.metadata['average_case']
        print(f"   CASO PROMEDIO:")
        print(f"      E[T] = {avg.get('T_avg', 'N/A')}")
        print(f"      Fórmula: {avg.get('formula', 'N/A')[:60]}...")
        if 'scenarios_breakdown' in avg and avg['scenarios_breakdown']:
            print(f"      Escenarios intermedios: {len(avg['scenarios_breakdown'])}")
        print()

    # ==========================================
    # 4. ANÁLISIS LÍNEA POR LÍNEA (si existe)
    # ==========================================
    if 'llm_analysis' in omega_table.metadata:
        print("4. ANÁLISIS LÍNEA POR LÍNEA")
        print("-" * 80)

        # Mejor caso
        if 'best_case' in omega_table.metadata['llm_analysis']:
            best_llm = omega_table.metadata['llm_analysis']['best_case']

            if 'line_by_line_analysis' in best_llm and best_llm['line_by_line_analysis']:
                print("\n   MEJOR CASO - Desglose línea por línea:")
                print("   " + "-" * 76)
                print(f"   {'#':<4} {'C_op':<6} {'Freq':<12} {'Total':<12} {'Código':<40}")
                print("   " + "-" * 76)

                for line in best_llm['line_by_line_analysis']:
                    line_num = line.get('line_number', 0)
                    c_op = line.get('C_op', 0)
                    freq = str(line.get('Freq', '1'))
                    total = str(line.get('Total', '0'))
                    code = line.get('code', '')[:40]

                    print(f"   {line_num:<4} {c_op:<6} {freq:<12} {total:<12} {code}")

                print("   " + "-" * 76)
                print(f"   TOTAL: {best_llm.get('total_cost_T', 'N/A')}")
                print()

            # Para recursivos, mostrar recurrencia
            if not ES_ITERATIVO and 'recurrence_relation' in best_llm:
                print("\n   MEJOR CASO - Relación de recurrencia:")
                print(f"      {best_llm['recurrence_relation']}")
                if 'base_case_cost' in best_llm:
                    print(f"      Caso base: {best_llm['base_case_condition']} → {best_llm['base_case_cost']}")
                print()

        # Peor caso (opcional, solo si es diferente)
        if 'worst_case' in omega_table.metadata['llm_analysis']:
            worst_llm = omega_table.metadata['llm_analysis']['worst_case']

            if 'line_by_line_analysis' in worst_llm and worst_llm['line_by_line_analysis']:
                print("\n   PEOR CASO - Desglose línea por línea:")
                print("   " + "-" * 76)
                print(f"   {'#':<4} {'C_op':<6} {'Freq':<12} {'Total':<12} {'Código':<40}")
                print("   " + "-" * 76)

                for line in worst_llm['line_by_line_analysis'][:5]:  # Primeras 5 líneas
                    line_num = line.get('line_number', 0)
                    c_op = line.get('C_op', 0)
                    freq = str(line.get('Freq', '1'))
                    total = str(line.get('Total', '0'))
                    code = line.get('code', '')[:40]

                    print(f"   {line_num:<4} {c_op:<6} {freq:<12} {total:<12} {code}")

                if len(worst_llm['line_by_line_analysis']) > 5:
                    print(f"   ... ({len(worst_llm['line_by_line_analysis']) - 5} líneas más)")

                print("   " + "-" * 76)
                print(f"   TOTAL: {worst_llm.get('total_cost_T', 'N/A')}")
                print()

    # ==========================================
    # 5. TABLA OMEGA SIMPLIFICADA
    # ==========================================
    print("\n5. TABLA OMEGA SIMPLIFICADA")
    print("-" * 80)
    print("\n   | ID | Condición | T(S) | P(S) |")
    print("   |----|-----------| -----|------|")

    for scenario in omega_table.scenarios:
        condition_short = scenario.condition[:30] + "..." if len(scenario.condition) > 30 else scenario.condition
        print(f"   | {scenario.id:<8} | {condition_short:<30} | {scenario.cost_T:<15} | {scenario.probability_P:<10} |")

    print()

    # ==========================================
    # VERIFICAR ERRORES
    # ==========================================
    if resultado_final.get("errors"):
        print("\n" + "=" * 80)
        print("ADVERTENCIAS/ERRORES DURANTE LA EJECUCIÓN")
        print("=" * 80)
        for i, error in enumerate(resultado_final["errors"], 1):
            print(f"   {i}. {error}")
        print()

    # ==========================================
    # RESUMEN FINAL
    # ==========================================
    print("=" * 80)
    print("FLUJO COMPLETADO EXITOSAMENTE")
    print("=" * 80)
    print(f"\nEscenarios generados: {len(omega_table.scenarios)}")
    print(f"Tipo de análisis: {'LLM' if 'llm_analysis' in omega_table.metadata else 'Fallback'}")

    # Verificar si usó fallback
    if any('fallback' in s.semantic_id for s in omega_table.scenarios):
        print("\n[AVISO] Se usaron escenarios de fallback (LLM pudo haber fallado)")
    else:
        print("\n[OK] Análisis LLM exitoso")

    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INTERRUMPIDO] Ejecución cancelada por el usuario")
    except Exception as e:
        print(f"\n\n[ERROR CRÍTICO] {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
