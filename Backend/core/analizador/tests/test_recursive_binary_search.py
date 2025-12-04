"""
Test para algoritmo recursivo: Binary Search

Verifica que el analizador genere correctamente la relación de recurrencia
T(n) = T(n/2) + C para búsqueda binaria recursiva.
"""

import pytest
from core.analizador.models.scenario_state import ScenarioState
from core.analizador.agents.workflow import create_mapeo_workflow


# Pseudocódigo de binary search recursivo
PSEUDOCODE_BINARY_SEARCH = """
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


def test_binary_search_recursive_detection():
    """
    Test 1: Verificar detección de recursión
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_BINARY_SEARCH,
        algorithm_name="binarySearch",
        is_iterative=True,
        parameters={"A[]": "array", "low": "int", "high": "int", "x": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    assert result.is_recursive == True
    assert len(result.recursive_calls) >= 2, "Binary search tiene 2 llamadas recursivas (en if/else)"


def test_binary_search_recursion_type():
    """
    Test 2: Verificar tipo de recurrencia (divide-and-conquer)
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_BINARY_SEARCH,
        algorithm_name="binarySearch",
        is_iterative=True,
        parameters={"A[]": "array", "low": "int", "high": "int", "x": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    assert result.recursion_info is not None
    # Binary search tiene múltiples llamadas pero solo ejecuta UNA por rama
    assert result.recursion_info.recurrence_type == "divide", "Debe ser tipo divide (n/2)"


def test_binary_search_scenarios():
    """
    Test 3: Verificar escenarios generados (balanced/skewed para divide-and-conquer)
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_BINARY_SEARCH,
        algorithm_name="binarySearch",
        is_iterative=True,
        parameters={"A[]": "array", "low": "int", "high": "int", "x": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    # Para divide-and-conquer, debe generar escenarios balanced y skewed
    assert len(result.raw_scenarios) >= 1, "Debe generar escenarios"
    scenario_ids = [s["id"] for s in result.raw_scenarios]

    # Verificar que tenga escenarios de división
    assert any("balanced" in s_id.lower() or "standard" in s_id.lower() for s_id in scenario_ids)


def test_binary_search_recurrence():
    """
    Test 4: Verificar relación de recurrencia T(n) = T(n/2) + C
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_BINARY_SEARCH,
        algorithm_name="binarySearch",
        is_iterative=True,
        parameters={"A[]": "array", "low": "int", "high": "int", "x": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    omega_table = result.omega_table
    assert omega_table is not None

    # Verificar al menos un escenario
    assert len(omega_table.scenarios) > 0

    # Buscar escenario con patrón n/2
    found_divide_pattern = False
    for scenario in omega_table.scenarios:
        cost_T = scenario.cost_T
        if "T(n/2)" in cost_T or "T((n/2))" in cost_T:
            found_divide_pattern = True
            print(f"\nEscenario {scenario.id}: {cost_T}")

    # Al menos un escenario debe tener patrón n/2
    assert found_divide_pattern, "Debe haber al menos un escenario con T(n/2)"


def test_binary_search_omega_table():
    """
    Test 5: Verificar Tabla Omega completa
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_BINARY_SEARCH,
        algorithm_name="binarySearch",
        is_iterative=True,
        parameters={"A[]": "array", "low": "int", "high": "int", "x": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    omega_table = result.omega_table

    print(f"\n=== TABLA OMEGA: BINARY SEARCH ===")
    print(omega_table.to_markdown_table())

    for scenario in omega_table.scenarios:
        print(f"\n{omega_table.scenario_to_markdown_justification(scenario.id)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
