"""
Test del DetectorTipoEntrada
=============================
Prueba la detección automática de lenguaje natural vs pseudocódigo
"""

import sys
from pathlib import Path

# Agregar Backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.services.detectorTipoEntrada import DetectorTipoEntrada


def test_detector():
    casos = [
        # Lenguaje Natural
        {
            "nombre": "LN: Descripción paso a paso",
            "entrada": """
Iniciar una variable llamada suma en 0.
Recorrer cada elemento de la lista, uno por uno.
En cada paso, agregar el valor del elemento actual a la variable suma.
            """,
            "esperado": "lenguaje_natural"
        },
        {
            "nombre": "LN: Descripción simple",
            "entrada": "Buscar un elemento en un arreglo de forma secuencial",
            "esperado": "lenguaje_natural"
        },
        
        # Pseudocódigo
        {
            "nombre": "Pseudocódigo: Completo",
            "entrada": """
busquedaLineal(int A[], int n, int x)
begin
    int i
    bool encontrado
    
    encontrado 🡨 F
    i 🡨 1
    
    while (i ≤ n and not encontrado) do
    begin
        if (A[i] = x) then
        begin
            encontrado 🡨 T
        end
        i 🡨 i + 1
    end
    
    return encontrado
end
            """,
            "esperado": "pseudocodigo"
        },
        {
            "nombre": "Pseudocódigo: Con error",
            "entrada": """
busquedaLineal(int A[], int n, int x)
begin
    i
    encontrado 🡨 F
    return encontrado
end
            """,
            "esperado": "pseudocodigo"
        }
    ]
    
    print("="*80)
    print("TEST: DetectorTipoEntrada")
    print("="*80)
    
    aciertos = 0
    total = len(casos)
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{i}. {caso['nombre']}")
        print("-"*40)
        
        tipo_detectado = DetectorTipoEntrada.detectar(caso['entrada'])
        detalles = DetectorTipoEntrada.obtener_confianza(caso['entrada'])
        
        es_correcto = tipo_detectado == caso['esperado']
        aciertos += 1 if es_correcto else 0
        
        print(f"{'✅' if es_correcto else '❌'} Detectado: {tipo_detectado} (esperado: {caso['esperado']})")
        print(f"   Score: {detalles['score']}")
    
    print(f"\n{'='*80}")
    print(f"RESULTADO: {aciertos}/{total} ({aciertos*100//total}%)")
    print("="*80)
    
    return aciertos == total


if __name__ == "__main__":
    exito = test_detector()
    exit(0 if exito else 1)
