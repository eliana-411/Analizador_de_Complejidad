"""
Tests End-to-End con Múltiples Algoritmos

Verifica que el workflow completo funciona correctamente con:
- Algoritmos iterativos (búsqueda lineal, suma, máximo)
- Algoritmos recursivos (factorial, fibonacci, binary search)
- Diferentes estructuras (loops simples, anidados, recursión)
"""

import pytest
from core.analizador.models.scenario_state import ScenarioState
from core.analizador.agents.workflow import get_workflow


# ==========================================
# ALGORITMOS ITERATIVOS
# ==========================================

BUSQUEDA_LINEAL = """busquedaLineal(int A[], int n, int x)
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


SUMA_ARRAY = """suma(int A[], int n)
begin
    int s
    int i

    s <- 0
    i <- 1

    while (i <= n) do
    begin
        s <- s + A[i]
        i <- i + 1
    end

    return s
end"""


MAXIMO_ARRAY = """maximo(int A[], int n)
begin
    int max
    int i

    max <- A[1]
    i <- 2

    while (i <= n) do
    begin
        if (A[i] > max) then
        begin
            max <- A[i]
        end
        i <- i + 1
    end

    return max
end"""


BUBBLE_SORT = """bubbleSort(int A[], int n)
begin
    int i
    int j
    int temp

    for i <- 1 to n-1 do
    begin
        for j <- 1 to n-i do
        begin
            if (A[j] > A[j+1]) then
            begin
                temp <- A[j]
                A[j] <- A[j+1]
                A[j+1] <- temp
            end
        end
    end
end"""


# ==========================================
# ALGORITMOS RECURSIVOS
# ==========================================

FACTORIAL = """factorial(int n)
begin
    if (n = 0) then
    begin
        return 1
    end
    else
    begin
        return n * factorial(n-1)
    end
end"""


FIBONACCI = """fibonacci(int n)
begin
    if (n = 0 or n = 1) then
    begin
        return n
    end
    else
    begin
        return fibonacci(n-1) + fibonacci(n-2)
    end
end"""


BINARY_SEARCH = """binarySearch(int A[], int left, int right, int x)
begin
    int mid

    if (left > right) then
    begin
        return -1
    end

    mid <- (left + right) / 2

    if (A[mid] = x) then
    begin
        return mid
    end
    else if (A[mid] > x) then
    begin
        return binarySearch(A, left, mid-1, x)
    end
    else
    begin
        return binarySearch(A, mid+1, right, x)
    end
end"""


# ==========================================
# TESTS ITERATIVOS
# ==========================================

class TestIterativeAlgorithms:
    """Tests para algoritmos iterativos"""

    @pytest.mark.timeout(90)
    def test_busqueda_lineal_produces_omega_table(self):
        """Búsqueda lineal debe generar tabla con mejor, peor y promedio caso"""
        state = ScenarioState(
            pseudocode=BUSQUEDA_LINEAL,
            algorithm_name="busquedaLineal",
            is_iterative=True,
            parameters={"A[]": "array", "n": "int", "x": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        omega_table = result["omega_table"]
        assert omega_table is not None
        assert omega_table.algorithm_name == "busquedaLineal"

        # Debe tener al menos 2 escenarios (mejor y peor)
        assert len(omega_table.scenarios) >= 2

        # Verificar metadata
        assert omega_table.metadata.get('algorithm_type') == 'iterative'

    @pytest.mark.timeout(90)
    def test_suma_array_produces_omega_table(self):
        """Suma de array debe generar tabla (caso no sensible a entrada)"""
        state = ScenarioState(
            pseudocode=SUMA_ARRAY,
            algorithm_name="suma",
            is_iterative=True,
            parameters={"A[]": "array", "n": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        omega_table = result["omega_table"]
        assert omega_table is not None

        # Suma siempre ejecuta n veces → un solo caso o casos con mismo costo
        assert len(omega_table.scenarios) >= 1

    @pytest.mark.timeout(90)
    def test_maximo_array_produces_omega_table(self):
        """Máximo de array debe generar tabla"""
        state = ScenarioState(
            pseudocode=MAXIMO_ARRAY,
            algorithm_name="maximo",
            is_iterative=True,
            parameters={"A[]": "array", "n": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        omega_table = result["omega_table"]
        assert omega_table is not None
        assert len(omega_table.scenarios) >= 1

    @pytest.mark.timeout(120)
    def test_bubble_sort_produces_omega_table(self):
        """Bubble sort (loops anidados) debe generar tabla"""
        state = ScenarioState(
            pseudocode=BUBBLE_SORT,
            algorithm_name="bubbleSort",
            is_iterative=True,
            parameters={"A[]": "array", "n": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        omega_table = result["omega_table"]
        assert omega_table is not None

        # Verificar que detectó loops anidados en metadata
        assert omega_table.metadata.get('loop_count', 0) >= 2


# ==========================================
# TESTS RECURSIVOS
# ==========================================

class TestRecursiveAlgorithms:
    """Tests para algoritmos recursivos"""

    @pytest.mark.timeout(90)
    def test_factorial_produces_omega_table(self):
        """Factorial debe generar tabla con relación de recurrencia"""
        state = ScenarioState(
            pseudocode=FACTORIAL,
            algorithm_name="factorial",
            is_iterative=False,
            parameters={"n": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        omega_table = result["omega_table"]
        assert omega_table is not None
        assert omega_table.algorithm_name == "factorial"

        # Verificar que es recursivo
        assert omega_table.metadata.get('algorithm_type') == 'recursive'

        # Debe tener escenarios
        assert len(omega_table.scenarios) >= 1

        # Verificar que tiene recurrence_relation en metadata
        if 'llm_analysis' in omega_table.metadata:
            if 'best_case' in omega_table.metadata['llm_analysis']:
                llm_best = omega_table.metadata['llm_analysis']['best_case']
                # Puede tener recurrence_relation si el LLM lo generó
                # (fallback no tendrá este campo)
                if 'recurrence_relation' in llm_best:
                    assert 'T(n)' in llm_best['recurrence_relation']

    @pytest.mark.timeout(90)
    def test_fibonacci_produces_omega_table(self):
        """Fibonacci debe generar tabla con doble recursión"""
        state = ScenarioState(
            pseudocode=FIBONACCI,
            algorithm_name="fibonacci",
            is_iterative=False,
            parameters={"n": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        omega_table = result["omega_table"]
        assert omega_table is not None
        assert omega_table.metadata.get('algorithm_type') == 'recursive'

    @pytest.mark.timeout(90)
    def test_binary_search_produces_omega_table(self):
        """Binary search (recursivo) debe generar tabla"""
        state = ScenarioState(
            pseudocode=BINARY_SEARCH,
            algorithm_name="binarySearch",
            is_iterative=False,
            parameters={"A[]": "array", "left": "int", "right": "int", "x": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        omega_table = result["omega_table"]
        assert omega_table is not None

        # Binary search es sensible a entrada → debe tener mejor y peor caso
        assert len(omega_table.scenarios) >= 2


# ==========================================
# TESTS DE ROBUSTEZ
# ==========================================

class TestRobustness:
    """Tests de robustez: casos edge, errores, fallbacks"""

    def test_empty_pseudocode_handles_gracefully(self):
        """Pseudocódigo vacío debe manejarse sin crash"""
        state = ScenarioState(
            pseudocode="",
            algorithm_name="empty",
            is_iterative=True,
            parameters={}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        # Puede tener errores, pero no debe crashear
        assert result is not None
        assert isinstance(result.get("errors", []), list)

    def test_single_line_algorithm(self):
        """Algoritmo de una sola línea debe funcionar"""
        pseudocode = """identity(int x)
begin
    return x
end"""

        state = ScenarioState(
            pseudocode=pseudocode,
            algorithm_name="identity",
            is_iterative=True,
            parameters={"x": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        assert result["omega_table"] is not None

    @pytest.mark.timeout(90)
    def test_workflow_with_fallback_still_produces_table(self):
        """Si LLM falla, fallback debe generar tabla básica"""
        # Usar pseudocódigo muy complejo que pueda hacer fallar al LLM
        complex_code = """complex(int n)
begin
    """ + "\n    ".join([f"x{i} <- x{i-1} + {i}" for i in range(1, 20)]) + """
end"""

        state = ScenarioState(
            pseudocode=complex_code,
            algorithm_name="complex",
            is_iterative=True,
            parameters={"n": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        # Debe generar tabla incluso si usa fallback
        assert result["omega_table"] is not None
        omega_table = result["omega_table"]
        assert len(omega_table.scenarios) >= 1


# ==========================================
# UTILIDADES
# ==========================================

def print_omega_table_summary(omega_table):
    """Imprime resumen de OmegaTable para debugging"""
    print(f"\nAlgoritmo: {omega_table.algorithm_name}")
    print(f"Tipo: {omega_table.metadata.get('algorithm_type')}")
    print(f"Escenarios: {len(omega_table.scenarios)}")

    for scenario in omega_table.scenarios:
        print(f"  - {scenario.id} ({scenario.semantic_id}): T={scenario.cost_T}, P={scenario.probability_P}")

    if 'best_case' in omega_table.metadata:
        best = omega_table.metadata['best_case']
        print(f"\nMejor caso: T={best.get('T')}, P={best.get('P')}")

    if 'worst_case' in omega_table.metadata:
        worst = omega_table.metadata['worst_case']
        print(f"Peor caso: T={worst.get('T')}, P={worst.get('P')}")


if __name__ == "__main__":
    # Ejecutar con verbose y mostrar salida
    pytest.main([__file__, "-v", "-s", "--tb=short"])
