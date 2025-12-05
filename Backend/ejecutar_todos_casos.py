"""
Script Completo de Casos de Prueba
===================================

Ejecuta análisis sobre:
- 15 casos de pseudocódigo correcto
- 5 casos de lenguaje natural

Total: 20 casos de prueba
"""

import sys
import os
from pathlib import Path
from datetime import datetime
import json

sys.path.insert(0, str(Path(__file__).parent))

from flujo_analisis import FlujoAnalisis
from agentes.agenteReportador import AgenteReportador
from tools.metricas import reset_metricas, obtener_metricas, guardar_metricas


# ==================== CONFIGURACIÓN ====================
CARPETA_PSEUDOCODIGO = Path(__file__).parent / "data" / "pseudocodigos" / "correctos"
CARPETA_LENGUAJE_NATURAL = Path(__file__).parent / "data" / "pseudocodigos" / "lenguaje_natural"
CARPETA_RESULTADOS = Path(__file__).parent / "resultados_casos_prueba"

# Casos de pseudocódigo
CASOS_PSEUDOCODIGO = [
    "01-busqueda-lineal.txt",
    "02-busqueda-binaria.txt",
    "03-bubble-sort.txt",
    "04-merge-sort.txt",
    "05-quick-sort.txt",
    "06-fibonacci-recursivo.txt",
    "07-factorial-recursivo.txt",
    "08-torres-hanoi.txt",
    "09-bst-insert.txt",
    "10-matrix-multiplication.txt",
    "11-selection-sort.txt",
    "12-insertion-sort.txt",
    "13-potencia-recursiva.txt",
    "14-suma-recursiva.txt",
    "15-maximo-array.txt"
]

# Casos de lenguaje natural
CASOS_LENGUAJE_NATURAL = [
    "01-maximo-array.txt",
    "02-merge-sort.txt",
    "03-suma-n-numeros.txt",
    "04-numero-primo.txt",
    "05-invertir-array.txt"
]


def ejecutar_caso_archivo(flujo: FlujoAnalisis, archivo: str, carpeta: Path, numero: int, total: int, tipo: str) -> dict:
    """Ejecuta análisis de un caso desde archivo"""
    print(f"\n{'='*80}")
    print(f"CASO {numero}/{total}: {archivo} ({tipo})")
    print(f"{'='*80}")
    
    ruta_archivo = carpeta / archivo
    
    if not ruta_archivo.exists():
        print(f"[ERROR] Archivo no encontrado: {ruta_archivo}")
        return None
    
    try:
        resultado = flujo.analizar_desde_archivo(str(ruta_archivo), auto_corregir=True)
        
        if resultado['exito']:
            print(f"[OK] Análisis completado exitosamente")
        else:
            print(f"[WARN] Análisis completado con errores: {len(resultado.get('errores', []))} error(es)")
        
        return resultado
    
    except Exception as e:
        print(f"[ERROR] Error ejecutando caso: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def ejecutar_caso_texto(flujo: FlujoAnalisis, archivo: str, carpeta: Path, numero: int, total: int, tipo: str) -> dict:
    """Ejecuta análisis de un caso de lenguaje natural"""
    print(f"\n{'='*80}")
    print(f"CASO {numero}/{total}: {archivo} ({tipo})")
    print(f"{'='*80}")
    
    ruta_archivo = carpeta / archivo
    
    if not ruta_archivo.exists():
        print(f"[ERROR] Archivo no encontrado: {ruta_archivo}")
        return None
    
    try:
        # Leer contenido
        with open(ruta_archivo, 'r', encoding='utf-8') as f:
            texto = f.read().strip()
        
        print(f"[INPUT] Entrada: {texto[:80]}...")
        
        # Analizar como lenguaje natural
        resultado = flujo.analizar(
            entrada=texto,
            tipo_entrada="lenguaje_natural",
            auto_corregir=True
        )
        
        if resultado['exito']:
            print(f"[OK] Análisis completado exitosamente")
        else:
            print(f"[WARN] Análisis completado con errores: {len(resultado.get('errores', []))} error(es)")
        
        return resultado
    
    except Exception as e:
        print(f"[ERROR] Error ejecutando caso: {str(e)}")
        import traceback
        traceback.print_exc()
        return None


def generar_tabla_resumen(resultados: list) -> str:
    """Genera tabla Markdown con resumen de todos los casos"""
    lineas = ["## [STATS] Resumen de Todos los Casos de Prueba", ""]
    
    lineas.append("| # | Tipo | Algoritmo | Válido | Clasificación | Mejor | Promedio | Peor |")
    lineas.append("|---|------|-----------|--------|---------------|-------|----------|------|")
    
    for i, (archivo, tipo, resultado) in enumerate(resultados, 1):
        if resultado is None:
            lineas.append(f"| {i} | {tipo} | {archivo} | [ERROR] | - | - | - | - |")
            continue
        
        # Nombre del algoritmo
        nombre = archivo.replace('.txt', '').replace('-', ' ').title()
        
        # Estado de validación
        valido = "[OK]" if resultado.get('exito', False) else "[ERROR]"
        
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
        
        tipo_emoji = "[INPUT]" if tipo == "Pseudocódigo" else "[MSG]"
        lineas.append(f"| {i} | {tipo_emoji} {tipo} | {nombre} | {valido} | {clasificacion} | {mejor} | {caso_prom} | {peor} |")
    
    lineas.append("")
    return '\n'.join(lineas)


def generar_reporte_consolidado(resultados: list) -> str:
    """Genera reporte Markdown consolidado"""
    fecha = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    # Contar por tipo
    total_pseudocodigo = sum(1 for _, tipo, _ in resultados if tipo == "Pseudocódigo")
    total_lenguaje = sum(1 for _, tipo, _ in resultados if tipo == "Lenguaje Natural")
    
    lineas = [
        "# 📋 Informe Completo de Casos de Prueba",
        "",
        f"**Fecha de generación:** {fecha}",
        f"**Total de casos:** {len(resultados)}",
        f"- Pseudocódigo: {total_pseudocodigo}",
        f"- Lenguaje Natural: {total_lenguaje}",
        "",
        "---",
        ""
    ]
    
    # Tabla resumen
    lineas.append(generar_tabla_resumen(resultados))
    
    # Estadísticas generales
    exitosos = sum(1 for _, _, r in resultados if r and r.get('exito', False))
    exitosos_pseudo = sum(1 for _, tipo, r in resultados if tipo == "Pseudocódigo" and r and r.get('exito', False))
    exitosos_ln = sum(1 for _, tipo, r in resultados if tipo == "Lenguaje Natural" and r and r.get('exito', False))
    
    lineas.append("## 📈 Estadísticas Generales")
    lineas.append("")
    lineas.append(f"- **Total exitosos:** {exitosos}/{len(resultados)} ({exitosos/len(resultados)*100:.1f}%)")
    lineas.append(f"  - Pseudocódigo: {exitosos_pseudo}/{total_pseudocodigo} ({exitosos_pseudo/total_pseudocodigo*100:.1f}%)")
    lineas.append(f"  - Lenguaje Natural: {exitosos_ln}/{total_lenguaje} ({exitosos_ln/total_lenguaje*100:.1f}%)")
    lineas.append(f"- **Con errores:** {len(resultados) - exitosos}/{len(resultados)}")
    lineas.append("")
    
    # Detalles de cada caso
    lineas.append("---")
    lineas.append("")
    lineas.append("# [INPUT] Detalle de Cada Caso")
    lineas.append("")
    
    reportador = AgenteReportador()
    
    for i, (archivo, tipo, resultado) in enumerate(resultados, 1):
        nombre = archivo.replace('.txt', '').replace('-', ' ').title()
        tipo_emoji = "[INPUT]" if tipo == "Pseudocódigo" else "[MSG]"
        lineas.append(f"## {i}. {nombre} ({tipo_emoji} {tipo})")
        lineas.append("")
        
        if resultado is None:
            lineas.append("[ERROR] **Error:** No se pudo ejecutar este caso")
            lineas.append("")
            continue
        
        # Generar reporte individual
        try:
            reporte_individual = reportador.generar_markdown(resultado)
            lineas.append(reporte_individual)
        except Exception as e:
            lineas.append(f"[ERROR] **Error generando reporte:** {str(e)}")
        
        lineas.append("")
        lineas.append("---")
        lineas.append("")
    
    return '\n'.join(lineas)


def main():
    """Función principal"""
    print("="*80)
    print("  EJECUCION AUTOMATIZADA DE CASOS DE PRUEBA")
    print("="*80)
    print()
    print(f"Pseudocodigo: {len(CASOS_PSEUDOCODIGO)} casos")
    print(f"Lenguaje Natural: {len(CASOS_LENGUAJE_NATURAL)} casos")
    print(f"Total: {len(CASOS_PSEUDOCODIGO) + len(CASOS_LENGUAJE_NATURAL)} casos")
    print()
    
    # Crear carpeta de resultados
    CARPETA_RESULTADOS.mkdir(parents=True, exist_ok=True)
    
    # Reiniciar métricas
    reset_metricas()
    
    # Inicializar flujo
    print("Inicializando sistema...")
    flujo = FlujoAnalisis(modo_verbose=False)
    print("Sistema inicializado")
    print()
    
    # Ejecutar casos de pseudocódigo
    resultados = []
    contador = 1
    total_casos = len(CASOS_PSEUDOCODIGO) + len(CASOS_LENGUAJE_NATURAL)
    
    for archivo in CASOS_PSEUDOCODIGO:
        resultado = ejecutar_caso_archivo(flujo, archivo, CARPETA_PSEUDOCODIGO, contador, total_casos, "Pseudocódigo")
        resultados.append((archivo, "Pseudocódigo", resultado))
        contador += 1
    
    # Ejecutar casos de lenguaje natural
    for archivo in CASOS_LENGUAJE_NATURAL:
        resultado = ejecutar_caso_texto(flujo, archivo, CARPETA_LENGUAJE_NATURAL, contador, total_casos, "Lenguaje Natural")
        resultados.append((archivo, "Lenguaje Natural", resultado))
        contador += 1
    
    # Generar reporte consolidado
    print(f"\n{'='*80}")
    print("GENERANDO REPORTE CONSOLIDADO")
    print(f"{'='*80}\n")
    
    reporte_md = generar_reporte_consolidado(resultados)
    
    # Guardar reporte Markdown
    ruta_reporte_md = CARPETA_RESULTADOS / "informe_completo.md"
    with open(ruta_reporte_md, 'w', encoding='utf-8') as f:
        f.write(reporte_md)
    
    print(f"[OK] Reporte Markdown: {ruta_reporte_md}")
    
    # Guardar métricas JSON
    ruta_metricas = CARPETA_RESULTADOS / "metricas.json"
    guardar_metricas(str(ruta_metricas))
    print(f"[OK] Métricas JSON: {ruta_metricas}")
    
    # Guardar resultados individuales
    ruta_resultados_json = CARPETA_RESULTADOS / "resultados_completos.json"
    resultados_serializables = []
    for archivo, tipo, resultado in resultados:
        if resultado:
            resultado_limpio = {
                'archivo': archivo,
                'tipo': tipo,
                'exito': resultado.get('exito', False),
                'clasificacion': resultado.get('clasificacion'),
                'complejidades': resultado.get('complejidades', {}).get('complejidades') if resultado.get('complejidades') else None,
                'errores': resultado.get('errores', [])
            }
            resultados_serializables.append(resultado_limpio)
    
    with open(ruta_resultados_json, 'w', encoding='utf-8') as f:
        json.dump(resultados_serializables, f, indent=2, ensure_ascii=False)
    
    print(f"[OK] Resultados JSON: {ruta_resultados_json}")
    
    # Resumen final
    print(f"\n{'='*80}")
    print("  RESUMEN FINAL")
    print(f"{'='*80}\n")
    
    exitosos = sum(1 for _, _, r in resultados if r and r.get('exito', False))
    print(f"OK Casos exitosos: {exitosos}/{len(resultados)} ({exitosos/len(resultados)*100:.1f}%)")
    print(f"XX Casos con errores: {len(resultados) - exitosos}/{len(resultados)}")
    print()
    
    # Mostrar métricas
    metricas = obtener_metricas()
    print(f"Tiempo total: {metricas['metadata']['duracion_total_segundos']:.2f} segundos")
    
    if metricas['tokens']['llamadas_llm'] > 0:
        print(f"Llamadas LLM: {metricas['tokens']['llamadas_llm']}")
        print(f"Tokens totales: {metricas['tokens']['total_tokens']:,}")
        print(f"Costo estimado: ${metricas['tokens']['costo_total_usd']:.6f} USD")
    
    print()
    print(f"Revisa el informe completo en: {ruta_reporte_md}")
    print()
    print("="*80)


if __name__ == "__main__":
    main()
