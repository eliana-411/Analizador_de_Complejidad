"""
Test para algoritmo recursivo: Factorial

Verifica que el analizador genere correctamente la relación de recurrencia
T(n) = T(n-1) + C para el algoritmo factorial recursivo.
"""

import pytest
from core.analizador.models.scenario_state import ScenarioState
from core.analizador.agents.workflow import create_mapeo_workflow


# Pseudocódigo de factorial recursivo
PSEUDOCODE_FACTORIAL = """
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


def test_factorial_recursive_detection():
    """
    Test 1: Verificar que se detecte como algoritmo recursivo
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_FACTORIAL,
        algorithm_name="factorial",
        is_iterative=True,  # Se actualizará a False al detectar recursión
        parameters={"n": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    # Verificar detección de recursión
    assert result.is_recursive == True, "Debe detectar que el algoritmo es recursivo"
    assert len(result.recursive_calls) > 0, "Debe detectar llamadas recursivas"


def test_factorial_recursion_analysis():
    """
    Test 2: Verificar análisis de estructura recursiva
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_FACTORIAL,
        algorithm_name="factorial",
        is_iterative=True,
        parameters={"n": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    # Verificar RecursionInfo
    assert result.recursion_info is not None, "Debe tener recursion_info"
    assert result.recursion_info.num_calls == 1, "Factorial tiene 1 llamada recursiva"
    assert result.recursion_info.recurrence_type == "subtract", "Factorial es recursión por decremento"


def test_factorial_scenario_generation():
    """
    Test 3: Verificar generación de escenarios
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_FACTORIAL,
        algorithm_name="factorial",
        is_iterative=True,
        parameters={"n": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    # Verificar escenarios generados
    assert len(result.raw_scenarios) >= 1, "Debe generar al menos un escenario"
    assert result.raw_scenarios[0]["id"] == "S_standard", "Debe generar escenario estándar para recursión subtract"


def test_factorial_recurrence_relation():
    """
    Test 4: Verificar relación de recurrencia generada
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_FACTORIAL,
        algorithm_name="factorial",
        is_iterative=True,
        parameters={"n": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    # Verificar Tabla Omega
    assert result.omega_table is not None, "Debe generar Tabla Omega"
    assert len(result.omega_table.scenarios) > 0, "Debe tener escenarios en la tabla"

    # Verificar relación de recurrencia
    scenario = result.omega_table.scenarios[0]
    cost_T = scenario.cost_T

    # Debe ser una relación de recurrencia, no fórmula cerrada
    assert "T(n)" in cost_T, "Debe contener T(n) en la relación de recurrencia"
    assert "T(n-1)" in cost_T, "Factorial debe tener T(n-1)"

    print(f"\nRelación de recurrencia generada: {cost_T}")


def test_factorial_omega_table():
    """
    Test 5: Verificar estructura completa de la Tabla Omega
    """
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_FACTORIAL,
        algorithm_name="factorial",
        is_iterative=True,
        parameters={"n": "int"}
    )

    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)
    result = ScenarioState(**result_dict)

    omega_table = result.omega_table
    assert omega_table is not None

    # Verificar estructura
    assert omega_table.algorithm_name == "factorial"
    assert len(omega_table.scenarios) > 0

    # Verificar escenario
    scenario = omega_table.scenarios[0]
    assert scenario.id is not None
    assert scenario.condition is not None
    assert scenario.state is not None
    assert scenario.cost_T is not None
    assert scenario.probability_P is not None

    # Imprimir tabla para inspección manual
    print(f"\n=== TABLA OMEGA: FACTORIAL ===")
    print(omega_table.to_markdown_table())
    print(f"\n{omega_table.scenario_to_markdown_justification(scenario.id)}")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
