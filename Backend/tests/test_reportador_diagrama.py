"""
Test para verificar que el reportador incluye diagramas del resolver
SIN llamar a la API (usando datos mockeados)
"""
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agentes.agenteReportador import AgenteReportador

def test_diagrama_en_reporte():
    """
    Verifica que el reportador incluya los diagramas del resolver
    """
    print("=" * 70)
    print("TEST: Reportador incluye diagramas del resolver")
    print("=" * 70)
    
    # Datos mockeados simulando resultado del flujo con diagrama
    resultado_flujo_mock = {
        'exito': True,
        'fase_actual': 'resolucion_completada',
        'pseudocodigo_original': 'funcion buscar(A, x) {...}',
        'pseudocodigo_validado': 'funcion buscar(A, x) {...}',
        'validacion': {'exito': True},
        'complejidades': {
            'ecuaciones': {
                'peor_caso': 'T(n) = T(n/3) + T(2n/3) + n'
            },
            'pasos_resolucion': {
                'peor_caso': {
                    'ecuacion': 'T(n) = T(n/3) + T(2n/3) + n',
                    'metodo': 'Árbol de Recursión',
                    'pasos': [
                        'Paso 1: Construir árbol',
                        'Paso 2: Calcular niveles',
                        'Paso 3: Sumar costos'
                    ],
                    'solucion': 'O(n log n)',
                    'explicacion': 'Se usa árbol porque es asimétrico',
                    'diagrama_mermaid': '```mermaid\ngraph TD\n    N0["T(n)"]\n    N0_h0["T(n/3)"]\n    N0 --> N0_h0\n```'
                }
            },
            'complejidades': {
                'peor_caso': 'O(n log n)'
            },
            'metodo_usado': 'Árbol de Recursión'
        }
    }
    
    # Crear reportador
    reportador = AgenteReportador()
    
    print("\n1. Generando reporte completo...")
    reporte_completo = reportador.generar_reporte_completo(resultado_flujo_mock)
    
    print("✓ Reporte generado")
    
    # Verificar que el markdown incluya el diagrama
    markdown = reporte_completo['markdown']
    
    print("\n2. Verificando que el diagrama esté en el Markdown...")
    if '```mermaid' in markdown and 'graph TD' in markdown:
        print("✓ Diagrama Mermaid encontrado en el reporte")
    else:
        print("✗ NO se encontró diagrama Mermaid en el reporte")
        print("\nBuscando 'mermaid' en el texto...")
        if 'mermaid' in markdown.lower():
            print(f"  Encontrado 'mermaid' en posición: {markdown.lower().find('mermaid')}")
        else:
            print("  'mermaid' NO aparece en el markdown")
    
    # Verificar sección de visualización
    if '**Visualización:**' in markdown:
        print("✓ Sección de visualización encontrada")
    else:
        print("✗ NO se encontró sección de visualización")
    
    # Verificar diagramas extraídos
    print("\n3. Verificando diagramas extraídos...")
    diagramas = reporte_completo.get('diagramas', {})
    print(f"✓ Total de diagramas: {len(diagramas)}")
    for key, valor in diagramas.items():
        if valor and '```mermaid' in str(valor):
            print(f"  ✓ {key}: Contiene código Mermaid")
        else:
            print(f"  - {key}: {type(valor).__name__}")
    
    # Exportar a archivo para inspección
    output_file = "reporte_con_diagrama.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(markdown)
    
    print(f"\n✓ Reporte exportado a: {output_file}")
    
    # Mostrar fragmento con el diagrama
    print("\n4. Fragmento del reporte con diagrama:")
    print("=" * 70)
    lineas = markdown.split('\n')
    en_seccion_viz = False
    contador = 0
    for i, linea in enumerate(lineas):
        if '**Visualización:**' in linea:
            en_seccion_viz = True
            # Mostrar 20 líneas desde aquí
            for j in range(i, min(i+25, len(lineas))):
                print(lineas[j])
            break
    
    if not en_seccion_viz:
        print("(No se encontró sección de visualización)")
        # Mostrar parte de resolución de recurrencia
        for i, linea in enumerate(lineas):
            if '## 4. Resolución' in linea:
                for j in range(i, min(i+30, len(lineas))):
                    print(lineas[j])
                break
    
    print("=" * 70)
    print("\n✅ TEST COMPLETADO")
    print(f"Abre {output_file} con VS Code y presiona Ctrl+Shift+V")

if __name__ == "__main__":
    test_diagrama_en_reporte()
