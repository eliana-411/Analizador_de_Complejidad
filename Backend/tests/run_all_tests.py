"""
Script para ejecutar todos los tests
=====================================
"""

import sys
import subprocess
from pathlib import Path


def ejecutar_test(nombre_archivo):
    """Ejecuta un test individual"""
    print(f"\n{'='*80}")
    print(f"Ejecutando: {nombre_archivo}")
    print('='*80)
    
    try:
        resultado = subprocess.run(
            [sys.executable, nombre_archivo],
            capture_output=False,
            cwd=Path(__file__).parent
        )
        return resultado.returncode == 0
    except Exception as e:
        print(f"❌ Error ejecutando {nombre_archivo}: {e}")
        return False


def main():
    tests = [
        "test_detector.py",
        "test_validador.py",
        "test_traductor.py",
        "test_corrector.py",
        "test_flujo.py"
    ]
    
    print("="*80)
    print("EJECUTANDO SUITE DE TESTS")
    print("="*80)
    
    resultados = {}
    
    for test in tests:
        exito = ejecutar_test(test)
        resultados[test] = exito
    
    # Resumen
    print("\n" + "="*80)
    print("RESUMEN DE TESTS")
    print("="*80)
    
    exitos = sum(1 for v in resultados.values() if v)
    total = len(resultados)
    
    for test, exito in resultados.items():
        print(f"{'✅' if exito else '❌'} {test}")
    
    print(f"\n{'='*80}")
    print(f"RESULTADO FINAL: {exitos}/{total} tests exitosos ({exitos*100//total}%)")
    print("="*80)
    
    return exitos == total


if __name__ == "__main__":
    exito = main()
    exit(0 if exito else 1)
