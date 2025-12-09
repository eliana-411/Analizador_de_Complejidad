"""
Script para ejecutar análisis de complejidad en todos los pseudocódigos correctos.
Genera un reporte consolidado con los resultados.
"""

import json
from pathlib import Path
from datetime import datetime
from flujo_analisis import FlujoAnalisis

def ejecutar_analisis_completo():
    """Ejecuta análisis en todos los pseudocódigos y genera reporte."""
    
    # Carpeta con pseudocódigos correctos
    carpeta_pseudocodigos = Path('data/pseudocodigos/correctos')
    
    # Obtener todos los archivos .txt
    archivos = sorted(carpeta_pseudocodigos.glob('*.txt'))
    
    print("="*80)
    print("ANÁLISIS DE COMPLEJIDAD - TODOS LOS PSEUDOCÓDIGOS")
    print("="*80)
    print(f"\nTotal de archivos a analizar: {len(archivos)}\n")
    
    resultados_todos = []
    flujo = FlujoAnalisis(modo_verbose=False)
    
    for i, archivo in enumerate(archivos, 1):
        nombre_archivo = archivo.name
        print(f"\n[{i}/{len(archivos)}] Analizando: {nombre_archivo}")
        print("-" * 60)
        
        try:
            # Leer pseudocódigo
            with open(archivo, 'r', encoding='utf-8') as f:
                codigo = f.read()
            
            # Ejecutar análisis
            resultado = flujo.analizar(
                entrada=codigo,
                tipo_entrada='pseudocodigo',
                auto_corregir=True
            )
            
            # Extraer información relevante
            info = {
                'archivo': nombre_archivo,
                'exito': resultado.get('exito', False),
                'fase_actual': resultado.get('fase_actual', 'N/A'),
                'complejidades': {},
                'concordancia': None,
                'errores': resultado.get('errores', [])
            }
            
            # Complejidades del sistema
            if 'complejidades' in resultado and 'complejidades' in resultado['complejidades']:
                comp = resultado['complejidades']['complejidades']
                info['complejidades']['sistema'] = {
                    'mejor_caso': comp.get('mejor_caso', 'N/A'),
                    'caso_promedio': comp.get('caso_promedio', 'N/A'),
                    'peor_caso': comp.get('peor_caso', 'N/A')
                }
            
            # Complejidades del LLM y concordancia
            if 'validacion_complejidades' in resultado:
                val = resultado['validacion_complejidades']
                info['complejidades']['llm'] = {
                    'mejor_caso': val['complejidades_llm'].get('mejor_caso', 'N/A'),
                    'caso_promedio': val['complejidades_llm'].get('caso_promedio', 'N/A'),
                    'peor_caso': val['complejidades_llm'].get('peor_caso', 'N/A')
                }
                info['concordancia'] = val.get('concordancia', False)
                info['confianza'] = val.get('confianza', 0)
            
            resultados_todos.append(info)
            
            # Imprimir resumen
            print(f"  ✅ Éxito: {info['exito']}")
            if info['complejidades'].get('sistema'):
                comp_sys = info['complejidades']['sistema']
                print(f"  📊 Complejidades:")
                print(f"     Mejor caso:    {comp_sys['mejor_caso']}")
                print(f"     Caso promedio: {comp_sys['caso_promedio']}")
                print(f"     Peor caso:     {comp_sys['peor_caso']}")
            
            if info['concordancia'] is not None:
                estado = "✅ SÍ" if info['concordancia'] else "❌ NO"
                print(f"  🔍 Concordancia con LLM: {estado} ({info['confianza']}%)")
            
            if info['errores']:
                print(f"  ⚠️  Errores: {len(info['errores'])}")
        
        except Exception as e:
            print(f"  ❌ ERROR: {str(e)}")
            resultados_todos.append({
                'archivo': nombre_archivo,
                'exito': False,
                'error': str(e)
            })
    
    # Generar reporte consolidado
    print("\n" + "="*80)
    print("RESUMEN GENERAL")
    print("="*80)
    
    exitosos = sum(1 for r in resultados_todos if r.get('exito', False))
    con_concordancia = sum(1 for r in resultados_todos if r.get('concordancia', False))
    
    print(f"\nTotal analizados: {len(resultados_todos)}")
    print(f"Exitosos: {exitosos}/{len(resultados_todos)}")
    print(f"Con concordancia LLM: {con_concordancia}/{len(resultados_todos)}")
    
    # Guardar resultados en JSON
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    archivo_resultados = Path(f'resultados_analisis_todos_{timestamp}.json')
    
    with open(archivo_resultados, 'w', encoding='utf-8') as f:
        json.dump(resultados_todos, f, indent=2, ensure_ascii=False)
    
    print(f"\n📄 Resultados guardados en: {archivo_resultados}")
    
    # Tabla resumen
    print("\n" + "="*80)
    print("TABLA DE COMPLEJIDADES")
    print("="*80)
    print(f"{'Archivo':<30} {'Mejor Caso':<15} {'Caso Prom.':<15} {'Peor Caso':<15} {'Concordancia':<12}")
    print("-" * 95)
    
    for res in resultados_todos:
        if res.get('exito') and res['complejidades'].get('sistema'):
            comp = res['complejidades']['sistema']
            conc = "✅ SÍ" if res.get('concordancia') else "❌ NO" if res.get('concordancia') is not None else "N/A"
            
            # Truncar nombre si es muy largo
            nombre = res['archivo'][:28] if len(res['archivo']) > 28 else res['archivo']
            
            print(f"{nombre:<30} {comp['mejor_caso']:<15} {comp['caso_promedio']:<15} {comp['peor_caso']:<15} {conc:<12}")
    
    print("="*80)

if __name__ == "__main__":
    ejecutar_analisis_completo()
