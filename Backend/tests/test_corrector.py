"""
Test del ServicioCorrector
===========================
Prueba la corrección automática de pseudocódigo con errores
"""

import sys
from pathlib import Path

# Agregar Backend al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from shared.services.servicioCorrector import ServicioCorrector
from shared.services.servicioValidador import servicioValidador


def test_corrector():
    codigo_con_error = """
busquedaLineal(int A[], int n, int x)
begin
    i
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
    """
    
    print("="*80)
    print("TEST: ServicioCorrector")
    print("="*80)
    
    # 1. Validar
    print("\n1. VALIDANDO...")
    print("-"*80)
    validador = servicioValidador()
    validacion = validador.validar(codigo_con_error)
    
    print(f"Válido: {validacion['valido_general']}")
    print(f"Errores: {validacion['resumen']['errores_totales']}")
    
    if validacion['resumen']['errores_totales'] > 0:
        for capa, datos in validacion['capas'].items():
            if datos['errores']:
                print(f"  • {datos['errores'][0]}")
    
    # 2. Corregir
    print("\n2. CORRIGIENDO...")
    print("-"*80)
    corrector = ServicioCorrector()
    
    try:
        resultado = corrector.corregir(codigo_con_error, validacion)
        
        if resultado['corregido']:
            print(f"✅ Corregido exitosamente")
            print(f"📚 Ejemplos usados: {resultado['ejemplos_usados']}")
            
            # 3. Re-validar
            print("\n3. RE-VALIDANDO...")
            print("-"*80)
            validacion_nueva = validador.validar(resultado['pseudocodigo'])
            print(f"{'✅' if validacion_nueva['valido_general'] else '❌'} Válido: {validacion_nueva['valido_general']}")
            print(f"Errores restantes: {validacion_nueva['resumen']['errores_totales']}")
            
            exito = validacion_nueva['valido_general']
        else:
            print(f"❌ No se pudo corregir")
            print(f"Razón: {resultado['explicacion']}")
            exito = False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        exito = False
    
    print(f"\n{'='*80}")
    print(f"RESULTADO: {'✅ EXITOSO' if exito else '❌ FALLÓ'}")
    print("="*80)
    
    return exito


if __name__ == "__main__":
    exito = test_corrector()
    exit(0 if exito else 1)
