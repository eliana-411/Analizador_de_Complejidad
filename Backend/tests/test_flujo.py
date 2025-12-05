"""
Test del FlujoAnalisis
=======================
Prueba el flujo completo: detección → traducción/validación → corrección → análisis
"""

import sys
from pathlib import Path

# Agregar Backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from Backend.tests.flujo_analisis import FlujoAnalisis


def test_flujo_completo():
    casos = [
        {
            "nombre": "Lenguaje Natural → Pseudocódigo",
            "entrada": "Buscar un elemento en un arreglo de forma secuencial",
            "tipo": "auto"
        },
        {
            "nombre": "Pseudocódigo con error → Corrección",
            "entrada": """
busquedaLineal(int A[], int n, int x)
begin
    i
    encontrado 🡨 F
    i 🡨 1
    return encontrado
end
            """,
            "tipo": "auto"
        }
    ]
    
    print("="*80)
    print("TEST: FlujoAnalisis Completo")
    print("="*80)
    
    flujo = FlujoAnalisis(modo_verbose=False)
    exitos = 0
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{i}. {caso['nombre']}")
        print("="*80)
        
        try:
            resultado = flujo.analizar(
                entrada=caso['entrada'],
                tipo_entrada=caso['tipo'],
                auto_corregir=True
            )
            
            print(f"Éxito: {resultado['exito']}")
            print(f"Fase: {resultado['fase_actual']}")
            
            if resultado['validacion']:
                print(f"Válido: {resultado['validacion']['valido_general']}")
                print(f"Errores: {resultado['validacion']['resumen']['errores_totales']}")
            
            if resultado['complejidades']:
                comp = resultado['complejidades']['complejidades']
                print(f"\nComplejidades:")
                print(f"  Mejor caso: {comp.get('mejor_caso', 'N/A')}")
                print(f"  Peor caso: {comp.get('peor_caso', 'N/A')}")
            
            if resultado['exito'] or resultado['validacion']['valido_general']:
                exitos += 1
                print(f"\n✅ EXITOSO")
            else:
                print(f"\n⚠️ Completado con advertencias")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*80}")
    print(f"RESULTADO: {exitos}/{len(casos)} flujos exitosos")
    print("="*80)
    
    return exitos >= len(casos) // 2  # Al menos 50% exitosos


if __name__ == "__main__":
    exito = test_flujo_completo()
    exit(0 if exito else 1)
