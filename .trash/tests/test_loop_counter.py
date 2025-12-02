"""
Tests para Loop Counter Tool

Valida que el análisis de ciclos funciona correctamente.
"""

import sys
import os

# Configurar encoding UTF-8 para evitar problemas en Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Agregar el path del backend para importar los módulos
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from tools.loop_counter import LoopCounter


def test_analizar_for_basico():
    """Test: Analizar un FOR básico: for i <- 1 to n do"""
    counter = LoopCounter()
    resultado = counter.analizar_for("for i <- 1 to n do")

    print("Test: FOR básico")
    print(f"Input: 'for i <- 1 to n do'")
    print(f"Resultado: {resultado}")

    assert resultado["valido"] == True
    assert resultado["variable"] == "i"
    assert resultado["inicio"] == "1"
    assert resultado["fin"] == "n"
    assert resultado["iteraciones"] == "n"
    assert resultado["tipo"] == "lineal"
    assert resultado["complejidad"] == "O(n)"
    print("✓ Test pasado\n")


def test_analizar_for_con_flecha_unicode():
    """Test: FOR con símbolo Unicode 🡨"""
    counter = LoopCounter()
    resultado = counter.analizar_for("for i 🡨 1 to n do")

    print("Test: FOR con flecha Unicode")
    print(f"Input: 'for i 🡨 1 to n do'")
    print(f"Resultado: {resultado}")

    assert resultado["valido"] == True
    assert resultado["variable"] == "i"
    assert resultado["complejidad"] == "O(n)"
    print("✓ Test pasado\n")


def test_analizar_for_con_expresion():
    """Test: FOR con expresión: for i <- 1 to n-1 do"""
    counter = LoopCounter()
    resultado = counter.analizar_for("for i <- 1 to n-1 do")

    print("Test: FOR con expresión (n-1)")
    print(f"Input: 'for i <- 1 to n-1 do'")
    print(f"Resultado: {resultado}")

    assert resultado["valido"] == True
    assert resultado["fin"] == "n-1"
    assert resultado["iteraciones"] == "n-1"
    assert resultado["tipo"] == "lineal"
    print("✓ Test pasado\n")


def test_analizar_for_desde_cero():
    """Test: FOR desde 0: for i <- 0 to n-1 do"""
    counter = LoopCounter()
    resultado = counter.analizar_for("for i <- 0 to n-1 do")

    print("Test: FOR desde 0")
    print(f"Input: 'for i <- 0 to n-1 do'")
    print(f"Resultado: {resultado}")

    assert resultado["valido"] == True
    assert resultado["inicio"] == "0"
    assert resultado["iteraciones"] == "n"  # 0 a n-1 = n iteraciones
    print("✓ Test pasado\n")


def test_analizar_for_invalido():
    """Test: Entrada inválida"""
    counter = LoopCounter()
    resultado = counter.analizar_for("esto no es un for")

    print("Test: FOR inválido")
    print(f"Input: 'esto no es un for'")
    print(f"Resultado: {resultado}")

    assert resultado["valido"] == False
    assert "error" in resultado
    print("✓ Test pasado\n")


def test_analizar_while_incremento_lineal():
    """Test: WHILE con incremento lineal"""
    counter = LoopCounter()

    linea_while = "while (i <= n) do"
    cuerpo = [
        "if (A[i] = x) then",
        "begin",
        "encontrado <- T",
        "end",
        "i <- i + 1"
    ]

    resultado = counter.analizar_while(linea_while, cuerpo)

    print("Test: WHILE con incremento lineal")
    print(f"Input: '{linea_while}'")
    print(f"Cuerpo: {len(cuerpo)} líneas")
    print(f"Resultado: {resultado}")

    assert resultado["valido"] == True
    assert resultado["variable_control"] == "i"
    assert resultado["tipo_modificacion"]["tipo"] == "incremento_lineal"
    assert resultado["complejidad"] == "O(n)"
    print("✓ Test pasado\n")


def test_analizar_while_division():
    """Test: WHILE con división (búsqueda binaria)"""
    counter = LoopCounter()

    linea_while = "while (i > 1) do"
    cuerpo = [
        "i <- i / 2"
    ]

    resultado = counter.analizar_while(linea_while, cuerpo)

    print("Test: WHILE con división")
    print(f"Input: '{linea_while}'")
    print(f"Cuerpo: {cuerpo}")
    print(f"Resultado: {resultado}")

    assert resultado["valido"] == True
    assert resultado["tipo_modificacion"]["tipo"] == "division"
    assert resultado["complejidad"] == "O(log n)"
    print("✓ Test pasado\n")


def test_analizar_repeat():
    """Test: REPEAT-UNTIL"""
    counter = LoopCounter()

    cuerpo = [
        "x <- x + 1",
        "y <- y * 2"
    ]
    linea_until = "until (x > n)"

    resultado = counter.analizar_repeat(cuerpo, linea_until)

    print("Test: REPEAT-UNTIL")
    print(f"Cuerpo: {len(cuerpo)} líneas")
    print(f"Until: '{linea_until}'")
    print(f"Resultado: {resultado}")

    assert resultado["valido"] == True
    assert resultado["tipo_ciclo"] == "repeat-until"
    assert resultado["variable_control"] == "x"
    print("✓ Test pasado\n")


def test_detectar_anidamiento_simple():
    """Test: Detectar ciclos anidados (2 niveles)"""
    counter = LoopCounter()

    bloques = [
        {"nivel": 1, "iteraciones": "n", "complejidad": "O(n)"},
        {"nivel": 2, "iteraciones": "n", "complejidad": "O(n)"}
    ]

    resultado = counter.detectar_anidamiento(bloques)

    print("Test: Anidamiento de 2 niveles")
    print(f"Bloques: {bloques}")
    print(f"Resultado: {resultado}")

    assert resultado["nivel_anidamiento"] == 2
    assert resultado["complejidad_combinada"] == "O(n²)"
    print("✓ Test pasado\n")


def test_detectar_anidamiento_triple():
    """Test: Detectar ciclos anidados (3 niveles)"""
    counter = LoopCounter()

    bloques = [
        {"nivel": 1, "iteraciones": "n", "complejidad": "O(n)"},
        {"nivel": 2, "iteraciones": "n", "complejidad": "O(n)"},
        {"nivel": 3, "iteraciones": "n", "complejidad": "O(n)"}
    ]

    resultado = counter.detectar_anidamiento(bloques)

    print("Test: Anidamiento de 3 niveles")
    print(f"Bloques: {bloques}")
    print(f"Resultado: {resultado}")

    assert resultado["nivel_anidamiento"] == 3
    assert resultado["complejidad_combinada"] == "O(n³)"
    print("✓ Test pasado\n")


def test_detectar_anidamiento_con_logaritmico():
    """Test: Anidamiento mixto (lineal + logarítmico)"""
    counter = LoopCounter()

    bloques = [
        {"nivel": 1, "iteraciones": "n", "complejidad": "O(n)"},
        {"nivel": 2, "iteraciones": "log n", "complejidad": "O(log n)"}
    ]

    resultado = counter.detectar_anidamiento(bloques)

    print("Test: Anidamiento lineal + logarítmico")
    print(f"Bloques: {bloques}")
    print(f"Resultado: {resultado}")

    assert resultado["nivel_anidamiento"] == 2
    assert resultado["complejidad_combinada"] == "O(n log n)"
    print("✓ Test pasado\n")


def ejecutar_todos_los_tests():
    """Ejecuta todos los tests"""
    print("=" * 60)
    print("EJECUTANDO TESTS DE LOOP COUNTER")
    print("=" * 60 + "\n")

    tests = [
        test_analizar_for_basico,
        test_analizar_for_con_flecha_unicode,
        test_analizar_for_con_expresion,
        test_analizar_for_desde_cero,
        test_analizar_for_invalido,
        test_analizar_while_incremento_lineal,
        test_analizar_while_division,
        test_analizar_repeat,
        test_detectar_anidamiento_simple,
        test_detectar_anidamiento_triple,
        test_detectar_anidamiento_con_logaritmico
    ]

    tests_pasados = 0
    tests_fallados = 0

    for test in tests:
        try:
            test()
            tests_pasados += 1
        except AssertionError as e:
            print(f"✗ Test fallado: {test.__name__}")
            print(f"  Error: {e}\n")
            tests_fallados += 1
        except Exception as e:
            print(f"✗ Error inesperado en {test.__name__}: {e}\n")
            tests_fallados += 1

    print("=" * 60)
    print(f"RESUMEN: {tests_pasados} tests pasados, {tests_fallados} fallados")
    print("=" * 60)

    return tests_pasados, tests_fallados


if __name__ == "__main__":
    ejecutar_todos_los_tests()
