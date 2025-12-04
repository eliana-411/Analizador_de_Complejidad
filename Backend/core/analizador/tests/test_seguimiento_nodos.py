"""
Test de Seguimiento de Nodos - Analizador de Complejidad

Este test ejecuta el workflow nodo por nodo y muestra lo que retorna cada uno,
permitiendo hacer un seguimiento completo del proceso de análisis.
"""

from core.analizador.models.scenario_state import ScenarioState
from core.analizador.agents.nodes.parse_lines_node import parse_lines_node
from core.analizador.agents.nodes.analyze_loops_node import analyze_loops_node
from core.analizador.agents.nodes.identify_control_vars_node import identify_control_vars_node
from core.analizador.agents.nodes.analyze_recursion_node import analyze_recursion_node
from core.analizador.agents.nodes.generate_scenarios_node import generate_scenarios_node
from core.analizador.agents.nodes.calculate_costs_node import calculate_costs_node
from core.analizador.agents.nodes.calculate_probabilities_node import calculate_probabilities_node
from core.analizador.agents.nodes.build_omega_table_node import build_omega_table_node


# ============================================================================
# PSEUDOCÓDIGOS DE PRUEBA
# ============================================================================

# Algoritmo recursivo simple: Factorial
FACTORIAL = """
int factorial(int n)
begin
    if (n == 0) then
    begin
        return 1
    end
    else
    begin
        return n * CALL factorial(n-1)
    end
end
"""

# Algoritmo recursivo divide-and-conquer: Binary Search
BINARY_SEARCH = """
int binarySearch(int A[], int low, int high, int x)
begin
    if (low > high) then
    begin
        return -1
    end

    int mid ← (low + high) / 2

    if (A[mid] == x) then
    begin
        return mid
    end

    if (A[mid] > x) then
    begin
        return CALL binarySearch(A, low, mid-1, x)
    end
    else
    begin
        return CALL binarySearch(A, mid+1, high, x)
    end
end
"""

# Algoritmo iterativo simple: Suma
SUMA = """
int suma(int A[], int n)
begin
    int suma ← 0
    int i

    for i ← 1 to n do
    begin
        suma ← suma + A[i]
    end

    return suma
end
"""


# ============================================================================
# FUNCIONES DE IMPRESIÓN
# ============================================================================

def print_separator(char="=", length=100):
    """Imprime una línea separadora"""
    print(char * length)


def print_header(text):
    """Imprime un encabezado destacado"""
    print_separator()
    print(f"  {text}")
    print_separator()


def print_node_header(node_name, step_number):
    """Imprime encabezado de nodo"""
    print(f"\n{'▶' * 3} PASO {step_number}: {node_name} {'▶' * 3}")
    print("-" * 100)


def print_field(label, value, indent=0):
    """Imprime un campo con formato"""
    spaces = "  " * indent
    if isinstance(value, list):
        print(f"{spaces}{label}: [{len(value)} elementos]")
        for i, item in enumerate(value[:5]):  # Mostrar máximo 5
            print(f"{spaces}  [{i}] {item}")
        if len(value) > 5:
            print(f"{spaces}  ... (+{len(value) - 5} más)")
    elif isinstance(value, dict):
        print(f"{spaces}{label}:")
        for k, v in list(value.items())[:5]:  # Mostrar máximo 5
            print(f"{spaces}  {k}: {v}")
        if len(value) > 5:
            print(f"{spaces}  ... (+{len(value) - 5} más)")
    else:
        print(f"{spaces}{label}: {value}")


# ============================================================================
# FUNCIÓN PRINCIPAL DE SEGUIMIENTO
# ============================================================================

def test_seguimiento_nodos(pseudocode, algorithm_name, parameters, is_iterative=True):
    """
    Ejecuta el workflow paso a paso mostrando la salida de cada nodo.

    Args:
        pseudocode: Pseudocódigo del algoritmo
        algorithm_name: Nombre del algoritmo
        parameters: Diccionario de parámetros
        is_iterative: Si es iterativo (True) o recursivo (False)
    """

    print_header(f"SEGUIMIENTO DE NODOS: {algorithm_name.upper()}")

    # Estado inicial
    print("\n📋 ESTADO INICIAL")
    print("-" * 100)
    print_field("Algorithm Name", algorithm_name)
    print_field("Is Iterative", is_iterative)
    print_field("Parameters", parameters)
    print("\nPseudocódigo:")
    for i, line in enumerate(pseudocode.strip().split('\n')[:10], 1):
        print(f"  {i:2}. {line}")

    state = ScenarioState(
        pseudocode=pseudocode,
        algorithm_name=algorithm_name,
        parameters=parameters,
        is_iterative=is_iterative
    )

    # ========================================================================
    # NODO 1: PARSE LINES
    # ========================================================================
    print_node_header("PARSE LINES", 1)
    state = parse_lines_node(state)

    print(f"✓ Líneas parseadas: {len(state.lines)}")
    print("\nPrimeras líneas:")
    for i, line in enumerate(state.lines[:10], 1):
        print(f"  {i:3}. {line}")
    if len(state.lines) > 10:
        print(f"       ... (+{len(state.lines) - 10} líneas más)")

    # ========================================================================
    # NODO 2: ANALYZE LOOPS
    # ========================================================================
    print_node_header("ANALYZE LOOPS", 2)
    state = analyze_loops_node(state)

    print(f"✓ Loops detectados: {len(state.loops)}")
    for loop in state.loops:
        print(f"\n  🔁 {loop.loop_type.upper()} Loop:")
        print(f"     ID: {loop.loop_id}")
        print(f"     Líneas: {loop.start_line} - {loop.end_line}")
        print(f"     Variable control: {loop.control_variable}")
        print(f"     Iteraciones: {loop.iterations}")

    print(f"\n✓ Llamadas recursivas detectadas: {len(state.recursive_calls)}")
    for call in state.recursive_calls:
        print(f"  🔄 Línea {call['line_number']}: {call['call_line']}")
        print(f"     Función: {call['function_name']}")
        print(f"     Argumentos: {call['arguments']}")

    print(f"\n✓ Es recursivo: {state.is_recursive}")

    # ========================================================================
    # NODO 3: BRANCHING (Identify Control Vars o Analyze Recursion)
    # ========================================================================

    if not state.is_recursive:
        # FLUJO ITERATIVO
        print_node_header("IDENTIFY CONTROL VARS", 3)
        state = identify_control_vars_node(state)

        print(f"✓ Variables de control identificadas: {len(state.control_variables)}")
        for cv in state.control_variables:
            print(f"\n  🎛️  {cv.name}:")
            print(f"     Tipo: {cv.type}")
            print(f"     Scope: {cv.scope}")
            print(f"     Afecta terminación: {cv.affects_termination}")

    else:
        # FLUJO RECURSIVO
        print_node_header("ANALYZE RECURSION", 3)
        state = analyze_recursion_node(state)

        if state.recursion_info:
            print("✓ Información de recursión extraída:")
            print(f"\n  Número de llamadas: {state.recursion_info.num_calls}")
            print(f"  Patrones de llamada: {state.recursion_info.call_pattern}")
            print(f"  Tipo de recurrencia: {state.recursion_info.recurrence_type}")
            print(f"  Condición caso base: {state.recursion_info.base_case_condition}")
            print(f"  Costo caso base: {state.recursion_info.base_case_cost}")
        else:
            print("⚠️  No se generó recursion_info")

    # ========================================================================
    # NODO 4: GENERATE SCENARIOS
    # ========================================================================
    print_node_header("GENERATE SCENARIOS", 4)
    state = generate_scenarios_node(state)

    print(f"✓ Escenarios generados: {len(state.raw_scenarios)}")
    for i, scenario in enumerate(state.raw_scenarios, 1):
        print(f"\n  🎬 Escenario {i}: {scenario['id']}")
        print(f"     Condición: {scenario['condition']}")
        print(f"     Estado: {scenario['state']}")
        if 'iteration_value' in scenario:
            print(f"     Valor iteración: {scenario['iteration_value']}")
            print(f"     Early exit: {scenario.get('early_exit', False)}")
        if 'recursion_pattern' in scenario:
            print(f"     Patrón recursión: {scenario['recursion_pattern']}")

    # ========================================================================
    # NODO 5: CALCULATE COSTS
    # ========================================================================
    print_node_header("CALCULATE COSTS", 5)
    state = calculate_costs_node(state)

    print(f"✓ Costos calculados para {len(state.raw_scenarios)} escenarios")
    for i, scenario in enumerate(state.raw_scenarios, 1):
        print(f"\n  📊 Escenario {scenario['id']}:")
        print(f"     T(S) = {scenario.get('cost_T', 'N/A')}")

        line_costs = scenario.get('line_costs', [])
        if line_costs:
            print(f"     Desglose ({len(line_costs)} líneas):")
            for lc in line_costs[:5]:
                print(f"       L{lc.line_number}: {lc.code[:40]:<40} | C_op={lc.C_op}, Freq={lc.Freq}, Total={lc.Total}")
            if len(line_costs) > 5:
                print(f"       ... (+{len(line_costs) - 5} líneas más)")

    # ========================================================================
    # NODO 6: CALCULATE PROBABILITIES
    # ========================================================================
    print_node_header("CALCULATE PROBABILITIES", 6)
    state = calculate_probabilities_node(state)

    print(f"✓ Probabilidades calculadas")
    for scenario in state.raw_scenarios:
        print(f"  {scenario['id']:15s} → P(S) = {scenario.get('probability_P', 'N/A')}")

    # ========================================================================
    # NODO 7: BUILD OMEGA TABLE
    # ========================================================================
    print_node_header("BUILD OMEGA TABLE", 7)
    state = build_omega_table_node(state)

    if state.omega_table:
        print("✓ Tabla Omega generada exitosamente")
        print(f"\n  Algoritmo: {state.omega_table.algorithm_name}")
        print(f"  Escenarios: {len(state.omega_table.scenarios)}")
        print(f"  Variables de control: {state.omega_table.control_variables}")

        print("\n  📋 TABLA OMEGA FINAL:")
        print("  " + "=" * 98)
        print(f"  {'ID':<15} {'Condición':<30} {'Estado':<20} {'T(S)':<25} {'P(S)'}")
        print("  " + "-" * 98)

        for scenario in state.omega_table.scenarios:
            print(f"  {scenario.id:<15} {scenario.condition[:30]:<30} {scenario.state[:20]:<20} {scenario.cost_T:<25} {scenario.probability_P}")

        print("  " + "=" * 98)
    else:
        print("⚠️  No se generó Tabla Omega")

    # ========================================================================
    # RESUMEN FINAL
    # ========================================================================
    print("\n")
    print_header("RESUMEN FINAL")

    if state.errors:
        print("\n❌ ERRORES:")
        for error in state.errors:
            print(f"  • {error}")

    if state.warnings:
        print("\n⚠️  ADVERTENCIAS:")
        for warning in state.warnings:
            print(f"  • {warning}")

    if not state.errors and not state.warnings:
        print("\n✅ Workflow completado exitosamente sin errores ni advertencias")

    print("\n")
    return state


# ============================================================================
# EJECUCIÓN DE TESTS
# ============================================================================

def main():
    """Ejecuta tests de seguimiento para diferentes algoritmos"""

    print("\n\n")
    print("=" * 100)
    print(" " * 30 + "TEST DE SEGUIMIENTO DE NODOS")
    print("=" * 100)

    # Test 1: Factorial (Recursivo simple)
    print("\n\n" + "█" * 100)
    print("█" + " " * 30 + "TEST 1: FACTORIAL (RECURSIVO)" + " " * 39 + "█")
    print("█" * 100)

    try:
        test_seguimiento_nodos(
            pseudocode=FACTORIAL,
            algorithm_name="factorial",
            parameters={"n": "int"},
            is_iterative=True  # Se detectará como recursivo automáticamente
        )
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    # Test 2: Binary Search (Recursivo divide-and-conquer)
    print("\n\n" + "█" * 100)
    print("█" + " " * 25 + "TEST 2: BINARY SEARCH (RECURSIVO)" + " " * 38 + "█")
    print("█" * 100)

    try:
        test_seguimiento_nodos(
            pseudocode=BINARY_SEARCH,
            algorithm_name="binarySearch",
            parameters={"A[]": "array", "low": "int", "high": "int", "x": "int"},
            is_iterative=True  # Se detectará como recursivo automáticamente
        )
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

    # Test 3: Suma (Iterativo)
    print("\n\n" + "█" * 100)
    print("█" + " " * 35 + "TEST 3: SUMA (ITERATIVO)" + " " * 40 + "█")
    print("█" * 100)

    try:
        test_seguimiento_nodos(
            pseudocode=SUMA,
            algorithm_name="suma",
            parameters={"A[]": "array", "n": "int"},
            is_iterative=True
        )
    except Exception as e:
        print(f"\n❌ ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
