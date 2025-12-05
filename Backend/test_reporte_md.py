"""
Script de prueba para generar reporte .md con árboles de recursión
"""

from tests.flujo_analisis import FlujoAnalisis
from pathlib import Path


def main():
    """Ejecuta análisis y genera reporte en .md"""
    
    # Ejemplo de pseudocódigo recursivo (Fibonacci)
    pseudocodigo = """
fibonacci(n)
begin
    if (n <= 1) then
        return n
    end
    return fibonacci(n-1) + fibonacci(n-2)
end
"""
    
    print("="*80)
    print("GENERANDO REPORTE DE ANÁLISIS CON ÁRBOLES DE RECURSIÓN")
    print("="*80)
    print()
    
    # Crear flujo de análisis
    flujo = FlujoAnalisis(modo_verbose=True)
    
    # Analizar pseudocódigo
    print("\n🔍 Analizando pseudocódigo...")
    resultado = flujo.analizar(
        entrada=pseudocodigo,
        tipo_entrada="pseudocodigo",
        auto_corregir=True
    )
    
    # Verificar resultados
    print("\n" + "="*80)
    print("RESULTADOS DEL ANÁLISIS")
    print("="*80)
    
    if resultado['exito']:
        print("✅ Análisis completado exitosamente")
        print(f"📁 Reporte guardado en: {resultado.get('ruta_reporte_guardado', 'N/A')}")
        
        # Mostrar complejidades
        if resultado.get('complejidades'):
            comp = resultado['complejidades'].get('complejidades', {})
            print("\n📊 COMPLEJIDADES CALCULADAS:")
            print(f"   • Mejor caso:    {comp.get('mejor_caso', 'N/A')}")
            print(f"   • Caso promedio: {comp.get('caso_promedio', 'N/A')}")
            print(f"   • Peor caso:     {comp.get('peor_caso', 'N/A')}")
        
        # Mostrar fragmento del reporte
        if resultado.get('reporte_markdown'):
            print("\n📝 FRAGMENTO DEL REPORTE:")
            print("-"*80)
            lineas = resultado['reporte_markdown'].split('\n')[:20]
            print('\n'.join(lineas))
            print("-"*80)
            print(f"... ({len(resultado['reporte_markdown'].split(chr(10)))} líneas en total)")
    else:
        print("❌ Análisis falló")
        if resultado.get('errores'):
            print("\n🔴 ERRORES:")
            for error in resultado['errores']:
                print(f"   • {error}")
    
    print("\n" + "="*80)


if __name__ == "__main__":
    main()
