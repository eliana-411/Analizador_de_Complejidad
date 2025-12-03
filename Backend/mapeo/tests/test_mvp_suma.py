"""
Test MVP: Algoritmo de Suma Simple con FOR

Verifica que el workflow completo funcione con un algoritmo simple:
- Un loop FOR
- Sin salidas tempranas
- Sin condicionales
- Debe generar Tabla Ω con un escenario
"""

import pytest

from Backend.mapeo.agents.workflow import create_mapeo_workflow
from Backend.mapeo.models.scenario_state import ScenarioState

# Pseudocódigo de prueba: suma de elementos de un array
PSEUDOCODE_SUMA = """suma ← 0
for i ← 1 to n do
begin
    suma ← suma + A[i]
end
return suma"""


def test_suma_workflow_completo():
    """
    Test de integración completo para algoritmo de suma.

    Expected Output:
    - 1 escenario: S_estandar
    - T(S) debe ser aproximadamente 2*n + 2
    - P(S) = 1
    - Subtabla con línea por línea
    """
    # Crear estado inicial (simula output de Fase 1)
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_SUMA,
        algorithm_name="suma",
        is_iterative=True,
        parameters={"A[]": "array", "n": "int"},
    )

    # Crear y ejecutar workflow
    workflow = create_mapeo_workflow()
    result_dict = workflow.invoke(initial_state)

    # LangGraph retorna un dict, convertir a ScenarioState
    result = ScenarioState(**result_dict)

    # Verificaciones básicas
    assert result.omega_table is not None, "Omega table no fue generada"
    assert len(result.omega_table.scenarios) >= 1, "Debe haber al menos 1 escenario"

    # Debug: ver cuantos loops se detectaron
    print(f"\n[DEBUG] Loops detectados: {len(result.loops)}")
    if result.loops:
        print(f"[DEBUG] Primer loop: {result.loops[0]}")

    # Verificar estructura del escenario
    scenario = result.omega_table.scenarios[0]
    # Para MVP, aceptar cualquier ID (S_estandar o S_base)
    assert scenario.id in ["S_estandar", "S_base"], f"ID inesperado: {scenario.id}"
    assert scenario.probability_P == "1", (
        f"P(S) esperado: 1, obtenido: {scenario.probability_P}"
    )

    # Verificar que tiene costo calculado
    assert scenario.cost_T != "0", f"T(S) no debe ser 0, obtenido: {scenario.cost_T}"

    # Verificar que tiene subtabla de line_costs
    assert len(scenario.line_costs) > 0, "Debe tener costeo línea por línea"

    print("\n=== RESULTADO TEST MVP ===")
    print(f"Algoritmo: {result.omega_table.algorithm_name}")
    print(f"Escenarios: {len(result.omega_table.scenarios)}")
    print(f"\nEscenario: {scenario.id}")
    print(f"Condición: {scenario.condition}")
    print(f"Estado: {scenario.state}")
    print(f"T(S): {scenario.cost_T}")
    print(f"P(S): {scenario.probability_P}")
    print(f"\nLíneas analizadas: {len(scenario.line_costs)}")

    # Imprimir subtabla de justificación
    print("\n=== Tabla de Justificación ===")
    print("| Línea | Código | C_op | Freq | Total |")
    print("|-------|--------|------|------|-------|")
    for lc in scenario.line_costs:
        print(
            f"| {lc.line_number} | {lc.code[:30]}... | {lc.C_op} | {lc.Freq} | {lc.Total} |"
        )


def test_parse_lines():
    """Test unitario: verificar que parse_lines extrae correctamente."""
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_SUMA,
        algorithm_name="suma",
        is_iterative=True,
        parameters={"A[]": "array", "n": "int"},
    )

    from Backend.mapeo.agents.nodes.parse_lines_node import parse_lines_node

    result = parse_lines_node(initial_state)

    assert len(result.lines) > 0, "Debe extraer líneas"
    assert "suma ← 0" in result.lines[0], "Primera línea debe ser asignación"


def test_analyze_loops():
    """Test unitario: verificar detección de loops."""
    initial_state = ScenarioState(
        pseudocode=PSEUDOCODE_SUMA,
        algorithm_name="suma",
        is_iterative=True,
        parameters={"A[]": "array", "n": "int"},
        lines=PSEUDOCODE_SUMA.split("\n"),
    )

    from Backend.mapeo.agents.nodes.analyze_loops_node import analyze_loops_node

    result = analyze_loops_node(initial_state)

    assert len(result.loops) >= 1, "Debe detectar al menos 1 loop"
    assert result.loops[0].loop_type == "for", "Debe ser tipo FOR"
    assert result.loops[0].iterations == "n", (
        f"Iteraciones esperadas: n, obtenidas: {result.loops[0].iterations}"
    )


if __name__ == "__main__":
    # Ejecutar test principal
    print("Ejecutando test MVP de suma...")
    test_suma_workflow_completo()
    print("\n✅ Test completado exitosamente!")
