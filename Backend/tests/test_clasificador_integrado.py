"""
Test de integración del clasificador ML en el flujo completo
"""

import sys
from pathlib import Path

# Agregar Backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from flujo_analisis import FlujoAnalisis
from agentes.agenteReportador import AgenteReportador


def test_clasificador_en_flujo():
    """Prueba el flujo completo con clasificador integrado"""
    
    # Pseudocódigo de ejemplo: Búsqueda Binaria
    pseudocodigo = """
funcion busqueda_binaria(arreglo, objetivo):
    izquierda = 0
    derecha = longitud(arreglo) - 1
    
    mientras izquierda <= derecha:
        medio = (izquierda + derecha) / 2
        
        si arreglo[medio] == objetivo:
            retornar medio
        sino si arreglo[medio] < objetivo:
            izquierda = medio + 1
        sino:
            derecha = medio - 1
    
    retornar -1
    """
    
    print("="*80)
    print("TEST: CLASIFICADOR ML EN FLUJO COMPLETO")
    print("="*80)
    
    # Ejecutar flujo
    flujo = FlujoAnalisis(modo_verbose=True)
    resultado = flujo.analizar(
        entrada=pseudocodigo,
        tipo_entrada="pseudocodigo"
    )
    
    # Verificar clasificación
    print("\n" + "="*80)
    print("RESULTADO DE CLASIFICACIÓN")
    print("="*80)
    
    if resultado.get('clasificacion'):
        clasificacion = resultado['clasificacion']
        print(f"\n✅ Clasificación exitosa:")
        print(f"   Categoría: {clasificacion['categoria_principal']}")
        print(f"   Confianza: {clasificacion['confianza']*100:.2f}%")
        print(f"\n   Top 3:")
        for i, pred in enumerate(clasificacion['top_predicciones'], 1):
            print(f"   {i}. {pred['categoria']:30} {pred['probabilidad']*100:6.2f}%")
    else:
        print("\n⚠️ No se generó clasificación")
    
    # Generar reporte
    print("\n" + "="*80)
    print("GENERANDO REPORTE")
    print("="*80)
    
    reportador = AgenteReportador()
    reporte = reportador.generar_reporte_completo(resultado)
    
    # Guardar reporte
    output_file = Path(__file__).parent / "reporte_con_clasificador.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(reporte['markdown'])
    
    print(f"\n✅ Reporte guardado en: {output_file}")
    
    # Verificar que el reporte incluye clasificación
    if 'Clasificación de Estructura Algorítmica' in reporte['markdown']:
        print("✅ Reporte incluye sección de clasificación ML")
    else:
        print("⚠️ Reporte NO incluye sección de clasificación")
    
    print("\n" + "="*80)
    print("TEST COMPLETADO")
    print("="*80)


if __name__ == "__main__":
    test_clasificador_en_flujo()
