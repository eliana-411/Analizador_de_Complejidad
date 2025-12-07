"""
Test de Comparación Sistema vs LLM
Demuestra la funcionalidad de validación cruzada
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agentes.agenteValidadorComplejidades import AgenteValidadorComplejidades

# Pseudocódigo de prueba: Búsqueda Lineal
pseudocodigo_busqueda_lineal = """busquedaLineal(int A[], int n, int x)
begin
    int i
    i <- 1
    while (i <= n) do
    begin
        if (A[i] = x) then
        begin
            return i
        end
        i <- i + 1
    end
    return -1
end"""

# Complejidades calculadas por el sistema
complejidades_sistema = {
    'mejor_caso': 'O(1)',
    'caso_promedio': 'O(n)',
    'peor_caso': 'O(n)'
}

def main():
    print("=" * 80)
    print("TEST DE COMPARACIÓN SISTEMA vs LLM")
    print("=" * 80)
    print()
    
    print("📝 PSEUDOCÓDIGO:")
    print("-" * 80)
    print(pseudocodigo_busqueda_lineal)
    print("-" * 80)
    print()
    
    print("🖥️  COMPLEJIDADES DEL SISTEMA:")
    print(f"   Mejor caso:    {complejidades_sistema['mejor_caso']}")
    print(f"   Caso promedio: {complejidades_sistema['caso_promedio']}")
    print(f"   Peor caso:     {complejidades_sistema['peor_caso']}")
    print()
    
    print("🔄 Iniciando validación con LLM...")
    print()
    
    # Crear validador y ejecutar comparación
    validador = AgenteValidadorComplejidades(use_llm=True)
    
    resultado = validador.validar_complejidades(
        pseudocodigo=pseudocodigo_busqueda_lineal,
        complejidades_sistema=complejidades_sistema,
        algorithm_name="busquedaLineal"
    )
    
    print()
    print("=" * 80)
    print("RESUMEN DE VALIDACIÓN")
    print("=" * 80)
    print(f"✓ Concordancia: {'SÍ ✅' if resultado['concordancia'] else 'NO ❌'}")
    print(f"✓ Confianza: {resultado['confianza']:.0%}")
    print(f"✓ Recomendación: {resultado['recomendacion']}")
    print()
    
    if resultado['analisis_divergencias']:
        print("⚠️  DIVERGENCIAS DETECTADAS:")
        for div in resultado['analisis_divergencias']:
            print(f"   • {div['caso']}: {div['tipo']} (severidad: {div['severidad']})")
    else:
        print("✅ No se detectaron divergencias")
    
    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
