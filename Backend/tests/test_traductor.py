"""
Test del ServicioTraductor
===========================
Prueba la traducción de lenguaje natural a pseudocódigo
"""

import sys
from pathlib import Path

# Agregar Backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.services.servicioTraductor import ServicioTraductor


def test_traductor():
    casos = [
        "Buscar un elemento en un arreglo de forma secuencial",
        "Ordenar un arreglo usando el método de burbuja",
        "Calcular el factorial de un número de forma recursiva"
    ]
    
    print("="*80)
    print("TEST: ServicioTraductor")
    print("="*80)
    
    traductor = ServicioTraductor()
    exitos = 0
    
    for i, descripcion in enumerate(casos, 1):
        print(f"\n{i}. {descripcion}")
        print("-"*80)
        
        try:
            resultado = traductor.traducir(descripcion)
            
            print(f"✅ Tipo: {resultado['tipo_detectado']}")
            print(f"📚 Ejemplos: {len(resultado['ejemplos_usados'])}")
            print(f"\nPseudocódigo (primeras 5 líneas):")
            lineas = resultado['pseudocodigo'].strip().split('\n')[:5]
            for linea in lineas:
                print(f"   {linea}")
            if len(resultado['pseudocodigo'].strip().split('\n')) > 5:
                print("   ...")
            
            exitos += 1
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print(f"\n{'='*80}")
    print(f"RESULTADO: {exitos}/{len(casos)} traducciones exitosas")
    print("="*80)
    
    return exitos == len(casos)


if __name__ == "__main__":
    exito = test_traductor()
    exit(0 if exito else 1)
