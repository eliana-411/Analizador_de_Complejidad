"""
Script de Demostración: Analizador de Complejidad
Ejecuta el workflow y muestra paso a paso todo lo que genera.
"""

from core.analizador.models.scenario_state import ScenarioState
from core.analizador.agents.workflow import create_mapeo_workflow


# ============================================================================
# PSEUDOCÓDIGOS DE PRUEBA
# ============================================================================

QUICKSORT_PSEUDO = """
quickSort(int A[], int izq, int der)
begin
    int pivote
    if (izq < der) then
    begin
        pivote <- particionar(A, izq, der)
        CALL quickSort(A, izq, pivote - 1)
        CALL quickSort(A, pivote + 1, der)
    end
end

particionar(int A[], int izq, int der)
begin
    int pivote, i, j, temp
    
    pivote <- A[der]
    i <- izq - 1
    
    for j <- izq to der - 1 do
    begin
        if (A[j] <= pivote) then
        begin
            i <- i + 1
            temp <- A[i]
            A[i] <- A[j]
            A[j] <- temp
        end
    end
    
    temp <- A[i + 1]
    A[i + 1] <- A[der]
    A[der] <- temp
    
    return i + 1
end
"""

BUSQUEDA_LINEAL = """
busquedaLineal(int A[], int n, int x)
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
end
"""


# ============================================================================
# FUNCIÓN AUXILIAR: Acceso seguro a atributos
# ============================================================================

def safe_get(obj, attr, default="N/A"):
    """Obtiene un atributo de forma segura, retorna default si no existe"""
    try:
        return getattr(obj, attr, default)
    except:
        return default


# ============================================================================
# FUNCIÓN PARA MOSTRAR RESULTADOS
# ============================================================================

def mostrar_resultado_completo(result, titulo):
    """
    Imprime TODOS los datos generados por el workflow
    """
    print("\n" + "="*80)
    print(f" {titulo}")
    print("="*80)
    
    # Estado del algoritmo
    print("\n📋 INFORMACIÓN DEL ALGORITMO")
    print("-" * 80)
    print(f"Nombre: {safe_get(result, 'algorithm_name')}")
    print(f"Es iterativo: {safe_get(result, 'is_iterative')}")
    print(f"Es recursivo: {safe_get(result, 'is_recursive')}")
    print(f"Parámetros: {safe_get(result, 'parameters')}")
    
    # Líneas parseadas
    lines = safe_get(result, 'lines', [])
    if lines:
        print("\n📄 LÍNEAS PARSEADAS")
        print("-" * 80)
        for i, line in enumerate(lines[:10], 1):
            print(f"{i:3d}. {line}")
        if len(lines) > 10:
            print(f"     ... (+{len(lines) - 10} líneas más)")
    
    # Loops detectados
    loops = safe_get(result, 'loops', [])
    if loops:
        print("\n🔁 LOOPS DETECTADOS")
        print("-" * 80)
        for loop in loops:
            print(f"• {safe_get(loop, 'loop_type', 'unknown').upper()} (líneas {safe_get(loop, 'start_line')}-{safe_get(loop, 'end_line')})")
            print(f"  Variable: {safe_get(loop, 'control_variable')}")
            print(f"  Iteraciones: {safe_get(loop, 'iterations')}")
    
    # Llamadas recursivas
    is_recursive = safe_get(result, 'is_recursive', False)
    recursive_calls = safe_get(result, 'recursive_calls', [])
    
    if is_recursive and recursive_calls:
        print("\n🔄 LLAMADAS RECURSIVAS")
        print("-" * 80)
        for i, call in enumerate(recursive_calls, 1):
            if isinstance(call, dict):
                linea = call.get('line', call.get('line_number', '?'))
                texto = call.get('call_text', call.get('text', call.get('call', str(call))))
                print(f"{i}. Línea {linea}: {texto}")
            else:
                print(f"{i}. {call}")
        
        recursion_info = safe_get(result, 'recursion_info', None)
        if recursion_info:
            print("\n📊 ANÁLISIS DE RECURSIÓN")
            print("-" * 80)
            
            # Imprimir todos los atributos que tenga
            if hasattr(recursion_info, '__dict__'):
                for key, value in recursion_info.__dict__.items():
                    print(f"{key}: {value}")
            else:
                # Intentar atributos comunes
                for attr in ['base_case', 'num_calls', 'recurrence_type', 'tree_structure', 
                            'recurrence_relation', 'parameter_changes']:
                    val = safe_get(recursion_info, attr, None)
                    if val is not None:
                        print(f"{attr}: {val}")
    
    # Variables de control
    control_vars = safe_get(result, 'control_variables', [])
    if control_vars:
        print("\n🎛️  VARIABLES DE CONTROL")
        print("-" * 80)
        for var in control_vars:
            print(f"• {safe_get(var, 'name')} (tipo: {safe_get(var, 'type')})")
    
    # Escenarios generados
    raw_scenarios = safe_get(result, 'raw_scenarios', [])
    if raw_scenarios:
        print("\n🎬 ESCENARIOS GENERADOS")
        print("-" * 80)
        for i, scenario in enumerate(raw_scenarios, 1):
            print(f"\n{i}. {scenario.get('id', 'Sin ID')}")
            print(f"   Condición: {scenario.get('condition', 'N/A')}")
            print(f"   Estado: {scenario.get('state', 'N/A')}")
            if 'cost_T' in scenario:
                print(f"   T(S): {scenario['cost_T']}")
            if 'probability_P' in scenario:
                print(f"   P(S): {scenario['probability_P']}")
    
    # TABLA OMEGA (lo más importante)
    omega_table = safe_get(result, 'omega_table', None)
    if omega_table:
        print("\n" + "="*80)
        print("📊 TABLA OMEGA (RESULTADO FINAL)")
        print("="*80)
        
        print(f"\nAlgoritmo: {safe_get(omega_table, 'algorithm_name')}")
        print(f"Variables de control: {safe_get(omega_table, 'control_variables')}")
        
        scenarios = safe_get(omega_table, 'scenarios', [])
        if scenarios:
            print("\n┌─────────────────┬────────────────────────┬─────────────────┬────────────────────────┬────────┐")
            print("│ Escenario       │ Condición              │ Estado          │ T(S)                   │ P(S)   │")
            print("├─────────────────┼────────────────────────┼─────────────────┼────────────────────────┼────────┤")
            
            for scenario in scenarios:
                escenario = str(safe_get(scenario, 'id', ''))[:15]
                condicion = str(safe_get(scenario, 'condition', ''))[:22]
                estado = str(safe_get(scenario, 'state', ''))[:15]
                costo = str(safe_get(scenario, 'cost_T', ''))[:22]
                prob = str(safe_get(scenario, 'probability_P', ''))[:6]
                
                print(f"│ {escenario:<15} │ {condicion:<22} │ {estado:<15} │ {costo:<22} │ {prob:<6} │")
            
            print("└─────────────────┴────────────────────────┴─────────────────┴────────────────────────┴────────┘")
            
            # Desglose línea por línea
            print("\n📝 DESGLOSE LÍNEA POR LÍNEA")
            print("-" * 80)
            for scenario in scenarios:
                print(f"\n▸ Escenario: {safe_get(scenario, 'id')}")
                line_costs = safe_get(scenario, 'line_costs', [])
                
                if line_costs and len(line_costs) > 0:
                    print("┌──────┬────────────────────────────────┬───────────┬────────────┬─────────────┐")
                    print("│ Línea│ Código                         │ Costo Base│ Frecuencia │ Total       │")
                    print("├──────┼────────────────────────────────┼───────────┼────────────┼─────────────┤")
                    for lc in line_costs[:10]:
                        linea = str(safe_get(lc, 'line_number', ''))[:5]
                        codigo = str(safe_get(lc, 'code_snippet', ''))[:30]
                        base = str(safe_get(lc, 'base_cost', ''))[:9]
                        freq = str(safe_get(lc, 'frequency', ''))[:10]
                        total = str(safe_get(lc, 'total_cost', ''))[:11]
                        print(f"│ {linea:<4} │ {codigo:<30} │ {base:<9} │ {freq:<10} │ {total:<11} │")
                    print("└──────┴────────────────────────────────┴───────────┴────────────┴─────────────┘")
                    if len(line_costs) > 10:
                        print(f"     ... (+{len(line_costs) - 10} líneas más)")
                else:
                    print("(Sin desglose línea por línea)")
            
            # Metadata
            metadata = safe_get(omega_table, 'metadata', {})
            if metadata:
                print("\n📋 METADATA")
                print("-" * 80)
                for key, value in metadata.items():
                    print(f"{key}: {value}")
    else:
        print("\n⚠️  NO SE GENERÓ TABLA OMEGA")
    
    # Warnings
    warnings = safe_get(result, 'warnings', [])
    if warnings:
        print("\n⚠️  ADVERTENCIAS")
        print("-" * 80)
        for warning in warnings:
            print(f"• {warning}")
    
    print("\n" + "="*80 + "\n")


# ============================================================================
# EJECUCIÓN PRINCIPAL
# ============================================================================

def main():
    """
    Ejecuta el analizador con diferentes algoritmos y muestra los resultados
    """
    
    # ========================================================================
    # TEST 1: QuickSort (Recursivo)
    # ========================================================================
    
    print("\n\n")
    print("█" * 80)
    print("█  DEMO 1: QUICKSORT (RECURSIVO)")
    print("█" * 80)
    
    try:
        state_quicksort = ScenarioState(
            pseudocode=QUICKSORT_PSEUDO,
            algorithm_name="quickSort",
            parameters={"A": "int[]", "izq": "int", "der": "int"},
            is_iterative=False
        )
        
        print("\n✓ Estado inicial creado")
        print("  Ejecutando workflow...")
        
        workflow = create_mapeo_workflow()
        result_dict = workflow.invoke(state_quicksort)
        result = ScenarioState(**result_dict)
        
        print("  ✓ Workflow completado\n")
        
        mostrar_resultado_completo(result, "QUICKSORT - RESULTADO COMPLETO")
        
    except Exception as e:
        print(f"\n❌ ERROR en QuickSort:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
    
    # ========================================================================
    # TEST 2: Búsqueda Lineal (Iterativo)
    # ========================================================================
    
    print("\n\n")
    print("█" * 80)
    print("█  DEMO 2: BÚSQUEDA LINEAL (ITERATIVO)")
    print("█" * 80)
    
    try:
        state_busqueda = ScenarioState(
            pseudocode=BUSQUEDA_LINEAL,
            algorithm_name="busquedaLineal",
            parameters={"A": "int[]", "n": "int", "x": "int"},
            is_iterative=True
        )
        
        print("\n✓ Estado inicial creado")
        print("  Ejecutando workflow...")
        
        workflow = create_mapeo_workflow()
        result_dict = workflow.invoke(state_busqueda)
        result = ScenarioState(**result_dict)
        
        print("  ✓ Workflow completado\n")
        
        mostrar_resultado_completo(result, "BÚSQUEDA LINEAL - RESULTADO COMPLETO")
        
    except Exception as e:
        print(f"\n❌ ERROR en Búsqueda Lineal:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
