"""
Test para verificar que ArbolRecursion genera diagramas Mermaid
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from agentes.resolvers.arbol_recursion import ArbolRecursion

def test_diagrama_arbol():
    """
    Test que verifica la generación del diagrama Mermaid
    para una recurrencia asimétrica típica
    """
    print("=" * 70)
    print("TEST: Diagrama de Árbol de Recursión")
    print("=" * 70)
    
    # Ecuación asimétrica típica: T(n) = T(n/3) + T(2n/3) + n
    ecuacion = {
        'forma': 'divide_conquista',
        'es_asimetrico': True,
        'terminos_recursivos': [
            {'divisor': 3, 'coeficiente': 1},
            {'divisor': 3, 'coeficiente': 2}  # 2n/3 se representa así
        ],
        'f_n': 'n'
    }
    
    resolver = ArbolRecursion()
    
    # Verificar que puede resolver
    puede = resolver.puede_resolver(ecuacion)
    print(f"\n✓ ¿Puede resolver? {puede}")
    assert puede, "ArbolRecursion debería poder resolver esta ecuación"
    
    # Resolver
    resultado = resolver.resolver(ecuacion)
    print(f"\n✓ ¿Éxito? {resultado['exito']}")
    print(f"✓ Solución: {resultado['solucion']}")
    print(f"✓ Método: {resultado.get('metodo_usado', 'Árbol de Recursión')}")
    
    # Verificar que tiene diagrama
    assert 'diagrama_mermaid' in resultado, "Resultado debe incluir diagrama_mermaid"
    diagrama = resultado['diagrama_mermaid']
    
    print(f"\n✓ Diagrama generado: {len(diagrama)} caracteres")
    print(f"✓ Comienza con ```mermaid: {diagrama.startswith('```mermaid')}")
    print(f"✓ Termina con ```: {diagrama.endswith('```')}")
    
    # Mostrar pasos
    print("\n" + "=" * 70)
    print("PASOS DE RESOLUCIÓN:")
    print("=" * 70)
    for i, paso in enumerate(resultado['pasos'], 1):
        print(f"{i}. {paso}")
    
    # Mostrar diagrama
    print("\n" + "=" * 70)
    print("DIAGRAMA MERMAID:")
    print("=" * 70)
    print(diagrama)
    
    # Exportar a archivo para visualización
    output_file = "diagrama_arbol.md"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("# Diagrama de Árbol de Recursión\n\n")
        f.write(f"## Ecuación: T(n) = T(n/3) + T(2n/3) + n\n\n")
        f.write("## Solución paso a paso\n\n")
        for paso in resultado['pasos']:
            f.write(f"- {paso}\n")
        f.write(f"\n**Solución:** {resultado['solucion']}\n\n")
        f.write("## Visualización del Árbol\n\n")
        f.write(diagrama)
        f.write("\n\n")
        f.write("## Explicación\n\n")
        f.write(resultado['explicacion'])
    
    print(f"\n✓ Diagrama exportado a: {output_file}")
    print("\n" + "=" * 70)
    print("✅ TEST COMPLETADO CON ÉXITO")
    print("=" * 70)

if __name__ == "__main__":
    test_diagrama_arbol()
