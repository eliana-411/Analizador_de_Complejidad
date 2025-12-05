"""
Test del Flujo Completo de An√°lisis de Complejidad

Prueba la integraci√≥n completa:
1. Validaci√≥n ‚Üí extrae metadatos
2. Workflow ‚Üí genera Tabla Omega
3. Agente Matem√°ticas ‚Üí genera Ecuaciones
4. Resolver ‚Üí genera Complejidades
"""

import sys
import os

# Agregar Backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.flujo_analisis import FlujoAnalisis

# Pseudoc√≥digo de prueba: B√∫squeda Lineal Simple
pseudocodigo_test = """busquedaLineal(int A[], int n, int x)
begin
    int i
    i Ì±® 1
    while (i <= n) do
    begin
        if (A[i] = x) then
        begin
            return i
        end
        i Ì±® i + 1
    end
    return -1
end"""

def main():
    print("=" * 80)
    print("TEST DE FLUJO COMPLETO DE AN√ÅLISIS")
    print("=" * 80)
    print()
    
    # Crear flujo con verbose activado
    flujo = FlujoAnalisis(modo_verbose=True)
    
    print("Ì≥ù PSEUDOC√ìDIGO A ANALIZAR:")
    print("-" * 80)
    print(pseudocodigo_test)
    print("-" * 80)
    print()
    
    try:
        # Ejecutar an√°lisis completo
        print("Ì∫Ä INICIANDO AN√ÅLISIS COMPLETO...")
        print()
        
        resultado = flujo.analizar(
            entrada=pseudocodigo_test,
            tipo_entrada="pseudocodigo",
            auto_corregir=True
        )
        
        print("\n" + "=" * 80)
        print("Ì≥ä RESULTADOS DEL AN√ÅLISIS")
        print("=" * 80)
        print()
        
        # Mostrar resultados clave
        print(f"‚úÖ √âxito: {resultado['exito']}")
        print(f"Ì≥ç Fase actual: {resultado['fase_actual']}")
        print()
        
        # Validaci√≥n
        if resultado.get('validacion'):
            val = resultado['validacion']
            print("Ì¥ç VALIDACI√ìN:")
            print(f"   - V√°lido: {val['valido_general']}")
            print(f"   - Tipo: {val.get('tipo_algoritmo', 'N/A')}")
            print(f"   - Algoritmo: {val.get('algorithm_name', 'N/A')}")
            print(f"   - Par√°metros: {val.get('parameters', {})}")
            print(f"   - Errores: {val['resumen']['errores_totales']}")
            print()
        
        # Tabla Omega
        if resultado.get('omega_table'):
            print("Ì≥ã TABLA OMEGA:")
            omega = resultado['omega_table']
            print(f"   - Escenarios: {len(omega.scenarios)}")
            print(f"   - Variables de control: {omega.control_variables}")
            print()
        
        # Ecuaciones
        if resultado.get('ecuaciones'):
            print("Ì¥¢ ECUACIONES GENERADAS:")
            ecuaciones = resultado['ecuaciones']
            print(f"   - Mejor caso: {ecuaciones.get('mejor_caso', 'N/A')}")
            print(f"   - Caso promedio: {ecuaciones.get('caso_promedio', 'N/A')}")
            print(f"   - Peor caso: {ecuaciones.get('peor_caso', 'N/A')}")
            print()
        
        # Complejidades
        if resultado.get('complejidades'):
            print("ÌæØ COMPLEJIDADES RESUELTAS:")
            comp = resultado['complejidades'].get('complejidades', {})
            print(f"   - Mejor caso: {comp.get('mejor_caso', 'N/A')}")
            print(f"   - Caso promedio: {comp.get('caso_promedio', 'N/A')}")
            print(f"   - Peor caso: {comp.get('peor_caso', 'N/A')}")
            print()
        
        # Errores
        if resultado.get('errores'):
            print("‚ùå ERRORES:")
            for error in resultado['errores']:
                print(f"   - {error}")
            print()
        
        print("=" * 80)
        print("‚úÖ TEST COMPLETADO")
        print("=" * 80)
        
        return resultado
        
    except Exception as e:
        print(f"\n‚ùå ERROR EN TEST: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    resultado = main()
    
    # C√≥digo de salida
    if resultado and resultado['exito']:
        sys.exit(0)
    else:
        sys.exit(1)
