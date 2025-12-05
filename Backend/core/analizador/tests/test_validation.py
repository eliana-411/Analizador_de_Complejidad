"""
Tests de Validación para el Módulo Analizador

Verifica que:
1. Estructura de datos es correcta (validación estructural)
2. Campos tienen valores semánticamente coherentes (validación semántica)
3. Matemáticas son consistentes (validación matemática)
"""

import pytest
import sympy as sp
from core.analizador.models.omega_table import OmegaTable, ScenarioEntry


class TestStructuralValidation:
    """Tests de validación estructural - formato de datos correcto"""

    def test_scenario_entry_has_required_fields(self):
        """ScenarioEntry debe tener todos los campos requeridos"""
        scenario = ScenarioEntry(
            id="S1",
            semantic_id="best_case",
            condition="x == 1",
            state="BEST_CASE",
            cost_T="7",
            probability_P="1/n"
        )

        assert scenario.id == "S1"
        assert scenario.semantic_id == "best_case"
        assert scenario.condition == "x == 1"
        assert scenario.state == "BEST_CASE"
        assert scenario.cost_T == "7"
        assert scenario.probability_P == "1/n"

    def test_omega_table_has_required_fields(self):
        """OmegaTable debe tener algorithm_name, scenarios, control_variables, metadata"""
        table = OmegaTable(
            algorithm_name="test",
            scenarios=[],
            control_variables=["n"],
            metadata={}
        )

        assert table.algorithm_name == "test"
        assert isinstance(table.scenarios, list)
        assert isinstance(table.control_variables, list)
        assert isinstance(table.metadata, dict)

    def test_omega_table_metadata_structure(self):
        """Metadata debe tener estructura esperada para análisis LLM"""
        table = OmegaTable(
            algorithm_name="busquedaLineal",
            scenarios=[],
            control_variables=["n"],
            metadata={
                'algorithm_type': 'iterative',
                'llm_analysis': {
                    'best_case': {
                        'scenario_type': 'best_case',
                        'total_cost_T': '7',
                        'probability_P': '1/n'
                    }
                },
                'best_case': {
                    'T': '7',
                    'P': '1/n'
                }
            }
        )

        assert 'algorithm_type' in table.metadata
        assert 'llm_analysis' in table.metadata
        assert 'best_case' in table.metadata


class TestSemanticValidation:
    """Tests de validación semántica - coherencia de valores"""

    def test_scenario_semantic_ids_are_valid(self):
        """semantic_id debe ser uno de los valores esperados"""
        valid_semantic_ids = [
            "best_case",
            "worst_case",
            "average_case",
            "S_intermediate_1",
            "best_case_fallback"
        ]

        for semantic_id in valid_semantic_ids:
            scenario = ScenarioEntry(
                id=f"S_{semantic_id}",
                semantic_id=semantic_id,
                condition="test",
                state="TEST",
                cost_T="n",
                probability_P="1"
            )
            assert scenario.semantic_id == semantic_id

    def test_algorithm_type_is_valid(self):
        """algorithm_type debe ser 'iterative' o 'recursive'"""
        for alg_type in ['iterative', 'recursive']:
            table = OmegaTable(
                algorithm_name="test",
                scenarios=[],
                control_variables=["n"],
                metadata={'algorithm_type': alg_type}
            )
            assert table.metadata['algorithm_type'] in ['iterative', 'recursive']

    def test_iterative_has_line_by_line_analysis(self):
        """Algoritmos iterativos deben tener line_by_line_analysis en metadata"""
        table = OmegaTable(
            algorithm_name="busquedaLineal",
            scenarios=[],
            control_variables=["n"],
            metadata={
                'algorithm_type': 'iterative',
                'llm_analysis': {
                    'best_case': {
                        'line_by_line_analysis': [
                            {
                                'line_number': 1,
                                'code': 'i <- 1',
                                'C_op': 1,
                                'Freq': '1',
                                'Total': '1'
                            }
                        ]
                    }
                }
            }
        )

        llm_best = table.metadata['llm_analysis']['best_case']
        assert 'line_by_line_analysis' in llm_best
        assert isinstance(llm_best['line_by_line_analysis'], list)
        assert len(llm_best['line_by_line_analysis']) > 0

    def test_recursive_has_recurrence_relation(self):
        """Algoritmos recursivos deben tener recurrence_relation en metadata"""
        table = OmegaTable(
            algorithm_name="factorial",
            scenarios=[],
            control_variables=["n"],
            metadata={
                'algorithm_type': 'recursive',
                'llm_analysis': {
                    'best_case': {
                        'recurrence_relation': 'T(n) = T(n-1) + 2',
                        'base_case_cost': '1',
                        'base_case_condition': 'n = 0'
                    }
                }
            }
        )

        llm_best = table.metadata['llm_analysis']['best_case']
        assert 'recurrence_relation' in llm_best
        assert 'T(n)' in llm_best['recurrence_relation']


class TestMathematicalValidation:
    """Tests de validación matemática - consistencia numérica"""

    def test_probabilities_sum_to_one(self):
        """Las probabilidades de todos los escenarios deben sumar 1"""
        scenarios = [
            ScenarioEntry(
                id="S1",
                semantic_id="best_case",
                condition="x in pos 1",
                state="BEST",
                cost_T="7",
                probability_P="1/3"
            ),
            ScenarioEntry(
                id="S2",
                semantic_id="worst_case",
                condition="x not found",
                state="WORST",
                cost_T="4*n+2",
                probability_P="2/3"
            )
        ]

        # Sumar probabilidades usando sympy
        total_prob = sum(sp.sympify(s.probability_P) for s in scenarios)
        simplified = sp.simplify(total_prob)

        assert simplified == 1, f"Probabilidades no suman 1: {simplified}"

    def test_cost_expressions_are_parseable(self):
        """cost_T debe ser parseable por sympy"""
        valid_costs = [
            "n",
            "2*n + 4",
            "n**2",
            "3*n**2 + 2*n + 1",
            "n*log(n)",
            "T(n) = T(n-1) + 2"  # Recursivo
        ]

        for cost in valid_costs:
            scenario = ScenarioEntry(
                id="S_test",
                semantic_id="test",
                condition="test",
                state="TEST",
                cost_T=cost,
                probability_P="1"
            )

            # Para iterativos, debe ser parseable directamente
            if "T(n)" not in cost:
                try:
                    expr = sp.sympify(cost)
                    assert expr is not None
                except:
                    pytest.fail(f"No se pudo parsear cost: {cost}")

    def test_line_costs_sum_to_total_cost(self):
        """
        Para algoritmos iterativos, la suma de line_costs.Total
        debe ser igual a total_cost_T
        """
        line_by_line = [
            {'line_number': 1, 'code': 'i <- 1', 'C_op': 1, 'Freq': '1', 'Total': '1'},
            {'line_number': 2, 'code': 'while i<=n', 'C_op': 2, 'Freq': 'n+1', 'Total': '2*n+2'},
            {'line_number': 3, 'code': 'i <- i+1', 'C_op': 2, 'Freq': 'n', 'Total': '2*n'}
        ]

        total_cost_T = "4*n + 3"

        # Sumar line costs
        sum_line_costs = sum(sp.sympify(line['Total']) for line in line_by_line)
        simplified_sum = sp.simplify(sum_line_costs)

        # Comparar con total esperado
        expected_total = sp.sympify(total_cost_T)

        assert sp.simplify(simplified_sum - expected_total) == 0, \
            f"Suma de líneas ({simplified_sum}) != total ({expected_total})"

    def test_frequency_n_plus_one_for_loop_headers(self):
        """Encabezados de loops deben tener frecuencia n+1"""
        # Ejemplo: while con n iteraciones → encabezado ejecuta n+1
        line_by_line = [
            {
                'line_number': 5,
                'code': 'while (i <= n and not encontrado) do',
                'C_op': 2,
                'Freq': 'n+1',  # REGLA N+1
                'Total': '2*n+2'
            },
            {
                'line_number': 6,
                'code': 'if (A[i] = x) then',
                'C_op': 2,
                'Freq': 'n',  # Cuerpo ejecuta n veces
                'Total': '2*n'
            }
        ]

        # Verificar que encabezado tiene n+1
        header = line_by_line[0]
        assert 'n+1' in header['Freq'] or header['Freq'] == 'n+1', \
            f"Encabezado de loop debe tener Freq=n+1, tiene: {header['Freq']}"


class TestWorkflowIntegration:
    """Tests de integración del workflow completo"""

    def test_workflow_produces_valid_omega_table(self):
        """El workflow debe producir una OmegaTable válida con estructura correcta"""
        from core.analizador.models.scenario_state import ScenarioState
        from core.analizador.agents.workflow import get_workflow

        # Pseudocódigo simple
        pseudocode = """suma(int A[], int n)
begin
    int s
    s <- 0
    for i <- 1 to n do
    begin
        s <- s + A[i]
    end
    return s
end"""

        state = ScenarioState(
            pseudocode=pseudocode,
            algorithm_name="suma",
            is_iterative=True,
            parameters={"A[]": "array", "n": "int"}
        )

        workflow = get_workflow()
        result = workflow.invoke(state)

        # Verificar que se generó OmegaTable
        assert result["omega_table"] is not None
        omega_table = result["omega_table"]

        # Verificar estructura básica
        assert omega_table.algorithm_name == "suma"
        assert len(omega_table.scenarios) > 0
        assert 'algorithm_type' in omega_table.metadata

        # Verificar que hay escenarios de mejor, peor caso (mínimo)
        semantic_ids = [s.semantic_id for s in omega_table.scenarios]

        # Si no hay fallback, debería haber best_case y worst_case
        # Si hay fallback, tendrá best_case_fallback, worst_case_fallback
        has_cases = any('best' in sid for sid in semantic_ids) and \
                    any('worst' in sid for sid in semantic_ids)

        assert has_cases, f"Debe tener mejor y peor caso. Tiene: {semantic_ids}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
