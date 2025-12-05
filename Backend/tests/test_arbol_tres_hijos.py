"""
Test para árbol de recursión con 3 HIJOS
T(n) = T(n/4) + T(n/4) + T(n/2) + n
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

def test_arbol_tres_hijos():
    """
    Test con ecuación que genera 3 hijos por nodo:
    T(n) = T(n/4) + T(n/4) + T(n/2) + n
    
    Esto simula un algoritmo que divide el problema en 3 partes:
    - Dos partes pequeñas: n/4 cada una
    - Una parte grande: n/2
    """
    print("=" * 70)
    print("TEST: Árbol de Recursión con 3 HIJOS")
    print("Ecuación: T(n) = T(n/4) + T(n/4) + T(n/2) + n")
    print("=" * 70)
    
    # Ecuación con 3 términos recursivos
    ecuacion = {
        'forma': 'divide_conquista',
        'terminos_multiples': True,
        'terminos_recursivos': [
            {'divisor': 4, 'coeficiente': 1},      # T(n/4)
            {'divisor': 4, 'coeficiente': 1},      # T(n/4)
            {'divisor': 2, 'coeficiente': 1}       # T(n/2)
        ],
        'f_n': 'n'
    }
    
    resolver = ArbolRecursion()
    
    # Verificar que puede resolver
    puede = resolver.puede_resolver(ecuacion)
    print(f"\n✓ ¿Puede resolver? {puede}")
    
    if not puede:
        print("❌ ArbolRecursion no acepta esta ecuación")
        print("Intentando con es_asimetrico...")
        ecuacion['es_asimetrico'] = True
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
    
    # Mostrar pasos (primeros 25)
    print("\n" + "=" * 70)
    print("PASOS DE RESOLUCIÓN (primeros 25):")
    print("=" * 70)
    for i, paso in enumerate(resultado['pasos'][:25], 1):
        print(paso)
    if len(resultado['pasos']) > 25:
        print(f"... ({len(resultado['pasos']) - 25} pasos más)")
    
    # Exportar a archivo
    output_file = "arbol_tres_hijos.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Árbol de Recursión con 3 HIJOS\n\n")
        f.write("## Ecuación: T(n) = T(n/4) + T(n/4) + T(n/2) + n\n\n")
        f.write("Este algoritmo divide el problema en **3 partes**:\n")
        f.write("- Dos subproblemas pequeños: T(n/4) cada uno\n")
        f.write("- Un subproblema grande: T(n/2)\n\n")
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
            f.write("- **Cada nodo tiene 3 hijos** (no 2 como en los ejemplos anteriores)\n")
            f.write("- **Rama izquierda**: T(n/4) - más profunda (divisor menor)\n")
            f.write("- **Rama central**: T(n/4) - misma profundidad que izquierda\n")
            f.write("- **Rama derecha**: T(n/2) - menos profunda (divisor mayor)\n")
            f.write("- **Nodos con `...`**: Ramas que terminan antes\n\n")
        
        f.write("---\n\n")
        f.write("## Explicación Teórica\n\n")
        f.write(resultado['explicacion'])
    
    print(f"\n✓ Reporte exportado a: {output_file}")
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETADO")
    print("=" * 70)
    print(f"\nAbre el archivo con: code {output_file}")
    print("Y presiona Ctrl+Shift+V para ver el árbol con 3 hijos por nodo")

if __name__ == "__main__":
    test_arbol_tres_hijos()
