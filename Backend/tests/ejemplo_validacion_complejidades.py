"""
Ejemplo de Uso: Validador de Complejidades
==========================================

Demuestra cómo usar el AgenteValidadorComplejidades para comparar
resultados del sistema con análisis LLM.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from agentes.agenteValidadorComplejidades import AgenteValidadorComplejidades
from flujo_analisis import FlujoAnalisis


def ejemplo_validacion_basica():
    """Ejemplo básico de validación de complejidades"""
    
    print("="*80)
    print("EJEMPLO 1: Validación Básica")
    print("="*80)
    
    # Pseudocódigo de ejemplo
    pseudocodigo = """
algoritmo busquedaLineal(int A[], int n, int x)
inicio
    para i desde 0 hasta n-1 hacer
        si A[i] == x entonces
            retornar i
        fin_si
    fin_para
    retornar -1
fin
    """
    
    # Complejidades calculadas por el sistema
    complejidades_sistema = {
        'mejor_caso': 'Ω(1)',
        'caso_promedio': 'Θ(n)',
        'peor_caso': 'O(n)'
    }
    
    # Validar
    validador = AgenteValidadorComplejidades(use_llm=True)
    resultado = validador.validar_complejidades(
        pseudocodigo=pseudocodigo,
        complejidades_sistema=complejidades_sistema,
        algorithm_name="busquedaLineal"
    )
    
    # Mostrar resultado
    print("\n" + "="*80)
    print("RESULTADO DE LA VALIDACIÓN")
    print("="*80)
    print(f"Concordancia: {resultado['concordancia']}")
    print(f"Confianza: {resultado['confianza']:.0%}")
    print(f"Recomendación: {resultado['recomendacion']}")


def ejemplo_validacion_con_flujo_completo():
    """Ejemplo integrando validación con el flujo completo"""
    
    print("\n\n" + "="*80)
    print("EJEMPLO 2: Validación Integrada con Flujo Completo")
    print("="*80)
    
    # 1. Ejecutar análisis completo
    print("\n1️⃣ Ejecutando análisis completo...")
    flujo = FlujoAnalisis(modo_verbose=False)
    resultado = flujo.analizar_desde_archivo(
        'data/pseudocodigos/correctos/02-busqueda-binaria.txt',
        auto_corregir=False
    )
    
    # 2. Extraer complejidades del sistema
    complejidades_sistema = resultado.get('complejidades', {}).get('complejidades', {})
    
    print(f"\n✅ Análisis completado")
    print(f"   Complejidades del sistema:")
    print(f"   - Mejor caso: {complejidades_sistema.get('mejor_caso', 'N/A')}")
    print(f"   - Caso promedio: {complejidades_sistema.get('caso_promedio', 'N/A')}")
    print(f"   - Peor caso: {complejidades_sistema.get('peor_caso', 'N/A')}")
    
    # 3. Validar con LLM
    print("\n2️⃣ Validando con LLM...")
    
    validacion = resultado.get('validacion', {})
    pseudocodigo = open('data/pseudocodigos/correctos/02-busqueda-binaria.txt', 'r', encoding='utf-8').read()
    
    validador = AgenteValidadorComplejidades(use_llm=True)
    validacion_resultado = validador.validar_complejidades(
        pseudocodigo=pseudocodigo,
        complejidades_sistema=complejidades_sistema,
        algorithm_name=validacion.get('algorithm_name', 'busquedaBinaria')
    )
    
    # 4. Decisión basada en validación
    print("\n3️⃣ Decisión final...")
    if validacion_resultado['concordancia']:
        print("✅ Las complejidades son correctas según el LLM")
        print("   Se puede confiar en los resultados del sistema")
    else:
        print("⚠️ Hay divergencias con el análisis del LLM")
        print("   Se recomienda revisión manual")
        
        if validacion_resultado['analisis_divergencias']:
            print("\n   Divergencias encontradas:")
            for div in validacion_resultado['analisis_divergencias']:
                print(f"   • {div['caso']}: Sistema={div['sistema']}, LLM={div['llm']}")


def ejemplo_validacion_batch():
    """Ejemplo validando múltiples algoritmos"""
    
    print("\n\n" + "="*80)
    print("EJEMPLO 3: Validación en Lote")
    print("="*80)
    
    casos_prueba = [
        {
            'archivo': 'data/pseudocodigos/correctos/01-busqueda-lineal.txt',
            'complejidades_esperadas': {
                'mejor_caso': 'Ω(1)',
                'caso_promedio': 'Θ(n)',
                'peor_caso': 'O(n)'
            }
        },
        {
            'archivo': 'data/pseudocodigos/correctos/03-bubble-sort.txt',
            'complejidades_esperadas': {
                'mejor_caso': 'Ω(n)',
                'caso_promedio': 'Θ(n²)',
                'peor_caso': 'O(n²)'
            }
        }
    ]
    
    validador = AgenteValidadorComplejidades(use_llm=True)
    flujo = FlujoAnalisis(modo_verbose=False)
    
    resultados = []
    
    for i, caso in enumerate(casos_prueba, 1):
        print(f"\n{'='*80}")
        print(f"Validando caso {i}/{len(casos_prueba)}: {Path(caso['archivo']).name}")
        print(f"{'='*80}")
        
        # Analizar
        resultado = flujo.analizar_desde_archivo(caso['archivo'], auto_corregir=False)
        complejidades_sistema = resultado.get('complejidades', {}).get('complejidades', {})
        
        # Validar
        pseudocodigo = open(caso['archivo'], 'r', encoding='utf-8').read()
        validacion = validador.validar_complejidades(
            pseudocodigo=pseudocodigo,
            complejidades_sistema=complejidades_sistema,
            algorithm_name=resultado.get('validacion', {}).get('algorithm_name', 'algoritmo')
        )
        
        resultados.append({
            'archivo': caso['archivo'],
            'concordancia': validacion['concordancia'],
            'confianza': validacion['confianza']
        })
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE VALIDACIONES")
    print("="*80)
    
    for res in resultados:
        estado = "✅" if res['concordancia'] else "❌"
        print(f"{estado} {Path(res['archivo']).name}: {res['confianza']:.0%}")
    
    total_concordancia = sum(1 for r in resultados if r['concordancia'])
    print(f"\nTotal: {total_concordancia}/{len(resultados)} casos con concordancia")


if __name__ == "__main__":
    print("\n🔬 EJEMPLOS DE VALIDACIÓN DE COMPLEJIDADES\n")
    
    try:
        # Descomentar el ejemplo que quieras ejecutar:
        
        # ejemplo_validacion_basica()
        # ejemplo_validacion_con_flujo_completo()
        ejemplo_validacion_batch()
        
        print("\n✅ Ejemplos completados exitosamente")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
