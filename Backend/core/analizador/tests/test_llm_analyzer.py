"""
Tests para el LLM Analyzer - Análisis de Características de Entrada

Estos tests validan que el LLM puede analizar correctamente diferentes
tipos de algoritmos y determinar sus características de sensibilidad.
"""

import pytest
from core.analizador.tools.llm_analyzer import get_llm_analyzer


# Test data: diferentes tipos de algoritmos
BUSQUEDA_LINEAL = """busquedaLineal(int A[], int n, int x)
begin
    int i
    bool encontrado

    encontrado ← F
    i ← 1

    while (i ≤ n and not encontrado) do
    begin
        if (A[i] = x) then
        begin
            encontrado ← T
        end
        i ← i + 1
    end

    return encontrado
end"""

SUMA_ARREGLO = """suma(int A[], int n)
begin
    int total, i
    total ← 0

    for i ← 1 to n do
    begin
        total ← total + A[i]
    end

    return total
end"""

FACTORIAL = """factorial(int n)
begin
    if (n ≤ 1) then
    begin
        return 1
    end

    return n * factorial(n - 1)
end"""


def test_llm_analyzer_busqueda_lineal():
    """
    Test: Búsqueda lineal debe ser detectada como sensible a posición.
    """
    analyzer = get_llm_analyzer(temperature=0.0)

    result = analyzer.analyze_input_scenarios(
        pseudocode=BUSQUEDA_LINEAL,
        algorithm_name="busquedaLineal"
    )

    # Validar estructura
    assert "is_sensitive" in result
    assert "sensitivity_type" in result
    assert "best_case_input" in result
    assert "worst_case_input" in result
    assert "parameter_q_applicable" in result
    assert "parameter_q_meaning" in result

    # Validar detección de sensibilidad
    assert result["is_sensitive"] is True, "Búsqueda lineal debe ser sensible a entrada"

    # Validar tipo de sensibilidad (debería ser position)
    assert result["sensitivity_type"] in ["position", "organization"], \
        f"Tipo de sensibilidad esperado: position, obtenido: {result['sensitivity_type']}"

    # Validar que q es aplicable
    assert result["parameter_q_applicable"] is True, \
        "Búsqueda lineal debe usar parámetro q (probabilidad de existencia)"

    print("\n✅ Test búsqueda lineal:")
    print(f"   - Sensibilidad: {result['sensitivity_type']}")
    print(f"   - Mejor caso: {result['best_case_input']}")
    print(f"   - Peor caso: {result['worst_case_input']}")
    print(f"   - Parámetro q: {result['parameter_q_meaning']}")


def test_llm_analyzer_suma():
    """
    Test: Suma de arreglo debe ser detectada como NO sensible.
    """
    analyzer = get_llm_analyzer(temperature=0.0)

    result = analyzer.analyze_input_scenarios(
        pseudocode=SUMA_ARREGLO,
        algorithm_name="suma"
    )

    # Validar estructura
    assert "is_sensitive" in result

    # Suma NO debe ser sensible (siempre recorre todo)
    assert result["is_sensitive"] is False, \
        "Suma de arreglo NO debe ser sensible a entrada"

    # Tipo debe ser "none"
    assert result["sensitivity_type"] == "none", \
        f"Suma debe tener sensitivity_type='none', obtenido: {result['sensitivity_type']}"

    # q NO debe aplicar
    assert result["parameter_q_applicable"] is False, \
        "Suma no necesita parámetro q"

    print("\n✅ Test suma:")
    print(f"   - Sensibilidad: {result['sensitivity_type']}")
    print(f"   - Mejor caso: {result['best_case_input']}")
    print(f"   - Peor caso: {result['worst_case_input']}")


def test_llm_analyzer_factorial():
    """
    Test: Factorial recursivo (análisis básico).
    """
    analyzer = get_llm_analyzer(temperature=0.0)

    result = analyzer.analyze_input_scenarios(
        pseudocode=FACTORIAL,
        algorithm_name="factorial"
    )

    # Validar estructura
    assert "is_sensitive" in result

    # Factorial típicamente NO es sensible (solo depende de n)
    # Nota: Esto puede variar según interpretación del LLM
    print("\n✅ Test factorial:")
    print(f"   - Sensibilidad: {result['is_sensitive']}")
    print(f"   - Tipo: {result['sensitivity_type']}")
    print(f"   - Mejor caso: {result['best_case_input']}")
    print(f"   - Peor caso: {result['worst_case_input']}")


def test_fallback_heuristic():
    """
    Test: Heurística de respaldo funciona si el LLM falla.
    """
    from core.analizador.tools.llm_analyzer import LLMAnalyzer

    analyzer = LLMAnalyzer(temperature=0.0)

    # Simular análisis con pseudocódigo que tiene "encontrado"
    result = analyzer._fallback_heuristic_analysis(BUSQUEDA_LINEAL)

    assert result["is_sensitive"] is True
    assert result["sensitivity_type"] == "position"
    assert result["parameter_q_applicable"] is True

    print("\n✅ Test fallback heuristic:")
    print(f"   - Detectó sensibilidad correctamente")


if __name__ == "__main__":
    """
    Ejecutar tests manualmente:
    python -m pytest Backend/core/analizador/tests/test_llm_analyzer.py -v -s
    """
    pytest.main([__file__, "-v", "-s"])
