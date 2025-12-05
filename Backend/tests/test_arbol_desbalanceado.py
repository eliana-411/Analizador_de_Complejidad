"""
Test para árbol de recursión DESBALANCEADO
T(n) = T(n/3) + T(2n/3) + n
"""
import sys
import os

# Configurar encoding UTF-8 para Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agentes.resolvers.arbol_recursion import ArbolRecursion

def test_arbol_desbalanceado():
    """
    Test con ecuación verdaderamente asimétrica/desbalanceada:
    T(n) = T(n/3) + T(2n/3) + n
    
    Esto simula QuickSort con particiones desbalanceadas.
    """
    print("=" * 70)
    print("TEST: Árbol de Recursión DESBALANCEADO")
    print("Ecuación: T(n) = T(n/3) + T(2n/3) + n")
    print("=" * 70)
    
    # Ecuación asimétrica: T(n) = T(n/3) + T(2n/3) + n
    # 2n/3 se representa como: coeficiente=2, divisor=3
    ecuacion = {
        'forma': 'divide_conquista',
        'es_asimetrico': True,
        'terminos_recursivos': [
            {'divisor': 3, 'coeficiente': 1},      # T(n/3)
            {'divisor': 3, 'coeficiente': 2}       # T(2n/3)
        ],
        'f_n': 'n'
    }
    
    resolver = ArbolRecursion()
    
    # Verificar que puede resolver
    puede = resolver.puede_resolver(ecuacion)
    print(f"\n✓ ¿Puede resolver? {puede}")
    
    if not puede:
        print("❌ ArbolRecursion no acepta esta ecuación")
        print("Intentando con terminos_multiples...")
        ecuacion['terminos_multiples'] = True
        puede = resolver.puede_resolver(ecuacion)
        print(f"✓ ¿Puede resolver ahora? {puede}")
    
    # Resolver
    resultado = resolver.resolver(ecuacion)
    print(f"\n✓ ¿Éxito? {resultado['exito']}")
    print(f"✓ Solución: {resultado['solucion']}")
    print(f"✓ Método: {resultado.get('metodo_usado', 'Árbol de Recursión')}")
    
    # Verificar diagrama
    if 'diagrama_mermaid' in resultado:
        diagrama = resultado['diagrama_mermaid']
        print(f"\n✓ Diagrama generado: {len(diagrama)} caracteres")
    else:
        print("\n❌ No se generó diagrama")
        diagrama = None
    
    # Mostrar pasos
    print("\n" + "=" * 70)
    print("PASOS DE RESOLUCIÓN:")
    print("=" * 70)
    for i, paso in enumerate(resultado['pasos'][:20], 1):  # Primeros 20 pasos
        print(paso)
    if len(resultado['pasos']) > 20:
        print(f"... ({len(resultado['pasos']) - 20} pasos más)")
    
    # Exportar a archivo
    output_file = "arbol_desbalanceado.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Árbol de Recursión DESBALANCEADO\n\n")
        f.write("## Ecuación: T(n) = T(n/3) + T(2n/3) + n\n\n")
        f.write("Este es el caso típico de **QuickSort con partición desbalanceada**.\n\n")
        f.write(f"**Solución:** {resultado['solucion']}\n\n")
        
        f.write("---\n\n")
        f.write("## Resolución Paso a Paso\n\n")
        for paso in resultado['pasos']:
            f.write(f"{paso}\n\n")
        
        if diagrama:
            f.write("---\n\n")
            f.write("## Visualización del Árbol\n\n")
            f.write(diagrama)
            f.write("\n\n")
            f.write("### Interpretación del Diagrama\n\n")
            f.write("- **Nodo morado oscuro**: Raíz T(n) con costo n\n")
            f.write("- **Nodos morados medios**: Nivel 1\n")
            f.write("  - Rama izquierda: T(n/3) - más profunda\n")
            f.write("  - Rama derecha: T(2n/3) - menos profunda\n")
            f.write("- **Nodos morados claros**: Nivel 2 con 4 nodos\n")
            f.write("- **Caja amarilla**: Observación clave sobre suma de niveles\n\n")
        
        f.write("---\n\n")
        f.write("## Explicación Teórica\n\n")
        f.write(resultado['explicacion'])
    
    print(f"\n✓ Reporte exportado a: {output_file}")
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETADO")
    print("=" * 70)
    print(f"\nAbre el archivo con: code {output_file}")
    print("Y presiona Ctrl+Shift+V para ver el preview con el diagrama renderizado")

if __name__ == "__main__":
    test_arbol_desbalanceado()
