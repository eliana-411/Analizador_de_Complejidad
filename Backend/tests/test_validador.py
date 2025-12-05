"""
Test del ServicioValidador
===========================
Prueba la validación de pseudocódigo
"""

import sys
from pathlib import Path

# Agregar Backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.services.servicioValidador import servicioValidador
def test_validador():
    casos = [
        {
            "nombre": "Pseudocódigo válido",
            "codigo": """
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
            "debe_ser_valido": True
        },
        {
            "nombre": "Pseudocódigo con error (sin tipo)",
            "codigo": """
busquedaLineal(int A[], int n, int x)
begin
    i
    encontrado 🡨 F
    return encontrado
end
            """,
            "debe_ser_valido": False
        }
    ]
    
    print("="*80)
    print("TEST: ServicioValidador")
    print("="*80)
    
    validador = servicioValidador()
    aciertos = 0
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{i}. {caso['nombre']}")
        print("-"*80)
        
        resultado = validador.validar(caso['codigo'])
        
        es_correcto = resultado['valido_general'] == caso['debe_ser_valido']
        aciertos += 1 if es_correcto else 0
        
        print(f"{'✅' if es_correcto else '❌'} Válido: {resultado['valido_general']} (esperado: {caso['debe_ser_valido']})")
        print(f"   Errores: {resultado['resumen']['errores_totales']}")
        
        if resultado['resumen']['errores_totales'] > 0:
            for capa, datos in resultado['capas'].items():
                if datos['errores']:
                    print(f"   {capa}: {datos['errores'][0]}")
    
    print(f"\n{'='*80}")
    print(f"RESULTADO: {aciertos}/{len(casos)} validaciones correctas")
    print("="*80)
    
    return aciertos == len(casos)


if __name__ == "__main__":
    exito = test_validador()
    exit(0 if exito else 1)
