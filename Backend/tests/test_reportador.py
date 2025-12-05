"""
Test del AgenteReportador
==========================
Prueba la generación de reportes en diferentes formatos
"""

import sys
import os
from pathlib import Path

# Configurar encoding UTF-8
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Agregar Backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from agentes.agenteReportador import AgenteReportador
from flujo_analisis import FlujoAnalisis


def test_reportador():
    print("="*80)
    print("TEST: AgenteReportador")
    print("="*80)
    
    # 1. Ejecutar un análisis completo
    print("\n1. EJECUTANDO ANÁLISIS...")
    print("-"*80)
    
    flujo = FlujoAnalisis(modo_verbose=False)
    
    # Caso de prueba: Lenguaje natural
    resultado = flujo.analizar(
        entrada="Buscar un elemento en un arreglo de forma secuencial",
        tipo_entrada="auto",
        auto_corregir=True
    )
    
    # Debug: verificar qué retornó
    if resultado is None:
        print("❌ ERROR: el flujo retornó None")
        return False
    
    print(f"✅ Análisis completado: {resultado.get('fase_actual', 'NO DEFINIDA')}")
    print(f"   Éxito: {resultado.get('exito', False)}")
    print(f"   Errores: {len(resultado.get('errores', []))}")
    
    # 2. Generar reporte
    print("\n2. GENERANDO REPORTE...")
    print("-"*80)
    
    # Verificar que el resultado sea válido
    if not resultado:
        print("❌ No hay resultado para generar reporte")
        return False
    
    reportador = AgenteReportador()
    reporte_completo = reportador.generar_reporte_completo(resultado)
    
    print(f"✅ Reporte generado")
    print(f"   - Markdown: {len(reporte_completo['markdown'])} caracteres")
    print(f"   - Diagramas: {len(reporte_completo['diagramas'])} disponibles")
    
    # 3. Mostrar reporte
    print("\n3. REPORTE MARKDOWN:")
    print("="*80)
    print(reporte_completo['markdown'])
    print("="*80)
    
    # 4. Mostrar diagramas
    print("\n4. DIAGRAMAS:")
    print("-"*80)
    
    for nombre, diagrama in reporte_completo['diagramas'].items():
        print(f"\n### {nombre.replace('_', ' ').title()}:")
        print(diagrama)
    
    # 5. Exportar a archivo
    print("\n5. EXPORTANDO A ARCHIVO...")
    print("-"*80)
    
    ruta_salida = Path(__file__).parent / "reporte_ejemplo.md"
    reportador.exportar_markdown(reporte_completo['markdown'], str(ruta_salida))
    
    print(f"✅ Exportado a: {ruta_salida}")
    
    print(f"\n{'='*80}")
    print("✅ TEST COMPLETADO EXITOSAMENTE")
    print("="*80)
    
    return True


if __name__ == "__main__":
    exito = test_reportador()
    exit(0 if exito else 1)
