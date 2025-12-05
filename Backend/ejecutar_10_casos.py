"""
Script Automatizado de 10 Casos de Prueba
==========================================

Ejecuta el análisis completo sobre los 10 pseudocódigos de prueba
y genera un reporte consolidado con todos los resultados.

Casos incluidos:
1. Búsqueda Lineal
2. Búsqueda Binaria
3. Bubble Sort
4. Merge Sort
5. Quick Sort
6. Fibonacci Recursivo
7. Factorial Recursivo
8. Torres de Hanoi
9. BST Insert
10. Matrix Multiplication
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

# Agregar Backend al path
sys.path.insert(0, str(Path(__file__).parent))

from flujo_analisis import FlujoAnalisis
from agentes.agenteReportador import AgenteReportador
from tools.metricas import reset_metricas, obtener_metricas, guardar_metricas


# ==================== CONFIGURACIÓN ====================
CARPETA_CASOS = Path(__file__).parent / "data" / "pseudocodigos" / "correctos"
CARPETA_RESULTADOS = Path(__file__).parent / "resultados_10_casos"

CASOS = [
    "01-busqueda-lineal.txt",
    "02-busqueda-binaria.txt",
    "03-bubble-sort.txt",
    "04-merge-sort.txt",
    "05-quick-sort.txt",
    "06-fibonacci-recursivo.txt",
    "07-factorial-recursivo.txt",
    "08-torres-hanoi.txt",
    "09-bst-insert.txt",
    "10-matrix-multiplication.txt"
]


def ejecutar_caso(flujo: FlujoAnalisis, archivo: str, numero: int) -> dict:
    """
    Ejecuta análisis de un caso individual.
    
    Returns:
        dict con resultado del análisis
    """
    print(f"\n{'='*80}")
    print(f"CASO {numero}/10: {archivo}")
    print(f"{'='*80}")
    
    ruta_archivo = CARPETA_CASOS / archivo
    
    if not ruta_archivo.exists():
        print(f"❌ Archivo no encontrado: {ruta_archivo}")
        return None
    
    try:
        resultado = flujo.analizar_desde_archivo(str(ruta_archivo), auto_corregir=True)
        
        if resultado['exito']:
            print(f"✅ Análisis completado exitosamente")
        else:
            print(f"⚠️ Análisis completado con errores")
        
        return resultado
    
    except Exception as e:
        print(f"❌ Error ejecutando caso: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def generar_tabla_resumen(resultados: list) -> str:
    """Genera tabla Markdown con resumen de los 10 casos"""
    lineas = ["## 📊 Resumen de los 10 Casos de Prueba", ""]
    
    lineas.append("| # | Algoritmo | Válido | Clasificación | Mejor | Promedio | Peor |")
    lineas.append("|---|-----------|--------|---------------|-------|----------|------|")
    
    for i, (archivo, resultado) in enumerate(resultados, 1):
        if resultado is None:
            lineas.append(f"| {i} | {archivo} | ❌ | - | - | - | - |")
            continue
        
        # Nombre del algoritmo
        nombre = archivo.replace('.txt', '').replace('-', ' ').title()
        
        # Estado de validación
        valido = "✅" if resultado.get('exito', False) else "❌"
        
        # Clasificación
        clasificacion = "N/A"
        if resultado.get('clasificacion'):
            clasificacion = resultado['clasificacion'].get('categoria', 'N/A')
        
        # Complejidades
        mejor = caso_prom = peor = "N/A"
        if resultado.get('complejidades') and 'complejidades' in resultado['complejidades']:
            comp = resultado['complejidades']['complejidades']
            mejor = comp.get('mejor_caso', 'N/A')
            caso_prom = comp.get('caso_promedio', 'N/A')
            peor = comp.get('peor_caso', 'N/A')
        
        lineas.append(f"| {i} | {nombre} | {valido} | {clasificacion} | {mejor} | {caso_prom} | {peor} |")
    
    lineas.append("")
    return '\n'.join(lineas)


def generar_reporte_consolidado(resultados: list) -> str:
    """Genera reporte Markdown consolidado con todos los casos"""
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    lineas = [
        "# 📋 Informe de 10 Casos de Prueba",
        "",
        f"**Fecha de generación:** {fecha}",
        f"**Total de casos:** {len(resultados)}",
        "",
        "---",
        ""
    ]
    
    # Tabla resumen
    lineas.append(generar_tabla_resumen(resultados))
    
    # Estadísticas generales
    exitosos = sum(1 for _, r in resultados if r and r.get('exito', False))
    lineas.append("## 📈 Estadísticas Generales")
    lineas.append("")
    lineas.append(f"- **Casos exitosos:** {exitosos}/{len(resultados)} ({exitosos/len(resultados)*100:.1f}%)")
    lineas.append(f"- **Casos con errores:** {len(resultados) - exitosos}/{len(resultados)}")
    lineas.append("")
    
    # Detalles de cada caso
    lineas.append("---")
    lineas.append("")
    lineas.append("# 📝 Detalle de Cada Caso")
    lineas.append("")
    
    reportador = AgenteReportador()
    
    for i, (archivo, resultado) in enumerate(resultados, 1):
        nombre = archivo.replace('.txt', '').replace('-', ' ').title()
        lineas.append(f"## {i}. {nombre}")
        lineas.append("")
        
        if resultado is None:
            lineas.append("❌ **Error:** No se pudo ejecutar este caso")
            lineas.append("")
            continue
        
        # Generar reporte individual
        try:
            reporte_individual = reportador.generar_markdown(resultado)
            lineas.append(reporte_individual)
        except Exception as e:
            lineas.append(f"❌ **Error generando reporte:** {str(e)}")
        
        lineas.append("")
        lineas.append("---")
        lineas.append("")
    
    return '\n'.join(lineas)


def main():
    """Función principal"""
    print("="*80)
    print("  EJECUCIÓN AUTOMATIZADA DE 10 CASOS DE PRUEBA")
    print("="*80)
    print()
    print(f"📂 Carpeta de casos: {CARPETA_CASOS}")
    print(f"📂 Carpeta de resultados: {CARPETA_RESULTADOS}")
    print()
    
    # Crear carpeta de resultados
    CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    
    # Reiniciar métricas
    reset_metricas()
    
    # Inicializar flujo (verbose=False para salida limpia)
    print("🔧 Inicializando sistema...")
    flujo = FlujoAnalisis(modo_verbose=False)
    print("✅ Sistema inicializado")
    print()
    
    # Ejecutar cada caso
    resultados = []
    for i, archivo in enumerate(CASOS, 1):
        resultado = ejecutar_caso(flujo, archivo, i)
        resultados.append((archivo, resultado))
    
    # Generar reporte consolidado
    print(f"\n{'='*80}")
    print("GENERANDO REPORTE CONSOLIDADO")
    print(f"{'='*80}\n")
    
    reporte_md = generar_reporte_consolidado(resultados)
    
    # Guardar reporte Markdown
    ruta_reporte_md = CARPETA_RESULTADOS / "informe_10_casos.md"
    with open(ruta_reporte_md, 'w', encoding='utf-8') as f:
        f.write(reporte_md)
    
    print(f"✅ Reporte Markdown: {ruta_reporte_md}")
    
    # Guardar métricas JSON
    ruta_metricas = CARPETA_RESULTADOS / "metricas.json"
    guardar_metricas(str(ruta_metricas))
    print(f"✅ Métricas JSON: {ruta_metricas}")
    
    # Guardar resultados individuales
    ruta_resultados_json = CARPETA_RESULTADOS / "resultados_completos.json"
    resultados_serializables = []
    for archivo, resultado in resultados:
        if resultado:
            # Convertir a serializable (algunos objetos no lo son)
            resultado_limpio = {
                'archivo': archivo,
                'exito': resultado.get('exito', False),
                'clasificacion': resultado.get('clasificacion'),
                'complejidades': resultado.get('complejidades', {}).get('complejidades') if resultado.get('complejidades') else None,
                'errores': resultado.get('errores', [])
            }
            resultados_serializables.append(resultado_limpio)
    
    with open(ruta_resultados_json, 'w', encoding='utf-8') as f:
        json.dump(resultados_serializables, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Resultados JSON: {ruta_resultados_json}")
    
    # Resumen final
    print(f"\n{'='*80}")
    print("  RESUMEN FINAL")
    print(f"{'='*80}\n")
    
    exitosos = sum(1 for _, r in resultados if r and r.get('exito', False))
    print(f"✅ Casos exitosos: {exitosos}/{len(resultados)}")
    print(f"❌ Casos con errores: {len(resultados) - exitosos}/{len(resultados)}")
    print()
    
    # Mostrar métricas
    metricas = obtener_metricas()
    print(f"⏱️  Tiempo total: {metricas['metadata']['duracion_total_segundos']:.2f} segundos")
    
    if metricas['tokens']['llamadas_llm'] > 0:
        print(f"🤖 Llamadas LLM: {metricas['tokens']['llamadas_llm']}")
        print(f"💰 Tokens totales: {metricas['tokens']['total_tokens']:,}")
        print(f"💵 Costo estimado: ${metricas['tokens']['costo_total_usd']:.6f} USD")
    
    print()
    print(f"📄 Revisa el informe completo en: {ruta_reporte_md}")
    print()
    print("="*80)


if __name__ == "__main__":
    main()
