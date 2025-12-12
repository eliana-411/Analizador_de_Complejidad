#!/usr/bin/env python3
"""
Prueba manual del AgenteResolver con 3 ecuaciones
=================================================

Script para probar las 3 ecuaciones de recurrencia (mejor, promedio, peor caso).

Uso:
    python test_resolver_simple.py "T(n)=1" "T(n)=n*log(n)" "T(n)=n^2"
"""

import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from agentes.agenteResolver import AgenteResolver

def probar_ecuaciones(mejor_caso, caso_promedio, peor_caso):
    """
    Prueba las 3 ecuaciones de recurrencia usando resolver_casos().
    El resolver ya muestra todos los prints internos del proceso.
    """
    casos = {
        'mejor_caso': mejor_caso,
        'caso_promedio': caso_promedio,
        'peor_caso': peor_caso
    }

    resolver = AgenteResolver()

    print("\n" + "="*120)
    print("🎯 RESOLUCIÓN COMPLETA CON APLICACIÓN DE NOTACIONES")
    print("="*120)
    print(f"📝 Mejor caso: {mejor_caso}")
    print(f"📊 Caso promedio: {caso_promedio}")
    print(f"📈 Peor caso: {peor_caso}")
    print()

    try:
        # El resolver_casos() ya muestra TODOS los prints internos del proceso completo
        resultados = resolver.resolver_casos(casos)

        # Mostrar información DETALLADA de cada caso
        for caso_tipo in ['mejor_caso', 'caso_promedio', 'peor_caso']:
            if caso_tipo in resultados:
                resultado = resultados[caso_tipo]
                nombre_display = {
                    'mejor_caso': 'MEJOR CASO',
                    'caso_promedio': 'CASO PROMEDIO',
                    'peor_caso': 'PEOR CASO'
                }[caso_tipo]

                print(f"\n{'='*100}")
                print(f"🏷️  {nombre_display}: {casos[caso_tipo]}")
                print(f"{'='*100}")

                print(f"📊 RESULTADO:")
                print(f"   ✅ Éxito: {resultado['exito']}")
                print(f"   🛠️  Método usado: {resultado.get('metodo_usado', 'Ninguno')}")
                print(f"   🔢 Solución cruda: {resultado.get('solucion', 'N/A')}")

                if resultado.get('ecuacion_parseada'):
                    print(f"\n🔍 PARSEO:")
                    parsed = resultado['ecuacion_parseada']
                    print(f"   📋 Forma: {parsed.get('forma', 'N/A')}")
                    for key, value in parsed.items():
                        if key != 'forma':
                            print(f"   {key}: {value}")

                if resultado.get('transformaciones'):
                    print(f"\n🔄 TRANSFORMACIONES:")
                    for trans in resultado['transformaciones']:
                        print(f"   - {trans}")

                if resultado.get('intentos'):
                    print(f"\n🎯 MÉTODOS INTENTADOS: {resultado['intentos']}")

                if resultado.get('pasos') and resultado['exito']:
                    print(f"\n📝 PASOS DE RESOLUCIÓN:")
                    for i, paso in enumerate(resultado['pasos'], 1):
                        print(f"   {i}. {paso}")

                if resultado.get('explicacion'):
                    print(f"\n💡 EXPLICACIÓN: {resultado['explicacion']}")

                if not resultado['exito']:
                    print(f"\n❌ FALLÓ:")
                    if resultado.get('ecuacion_parseada'):
                        forma = resultado['ecuacion_parseada'].get('forma', 'desconocida')
                        print(f"   Forma detectada: {forma}")
                    else:
                        print("   No se pudo parsear la ecuación")

        # Mostrar resumen final con notaciones aplicadas
        print("\n" + "="*80)
        print("📊 RESUMEN FINAL:")
        print("="*80)

        if 'complejidades' in resultados:
            print("\n🎨 COMPLEJIDADES CON NOTACIÓN APLICADA:")
            for caso, notacion in resultados['complejidades'].items():
                nombre_display = {
                    'mejor_caso': 'Ω (Mejor caso)',
                    'caso_promedio': 'Θ (Caso promedio)',
                    'peor_caso': 'O (Peor caso)'
                }[caso]
                print(f"   {nombre_display}: {notacion}")

            print("🔍 ANÁLISIS:")
            print(f"   📏 Son iguales: {resultados.get('son_iguales', False)}")
            if resultados.get('observacion'):
                print(f"   💡 Observación: {resultados['observacion']}")

            # Explicar la lógica aplicada
            print("🧠 LÓGICA DE NOTACIONES:")
            if resultados.get('son_iguales'):
                print("   → Las complejidades son iguales → Se usa Θ para todos los casos")
            else:
                print("   → Las complejidades son diferentes → Se aplican notaciones específicas:")
                print("     • Mejor caso → Ω (Omega)")
                print("     • Caso promedio → Θ (Theta)")
                print("     • Peor caso → O (Big O)")
                if any('TeoremaMAestro' in str(resultados.get(caso, {}).get('metodo_usado', '')) for caso in ['mejor_caso', 'caso_promedio', 'peor_caso']):
                    print("   → Teorema Maestro mantiene su Θ original (excepto si se fuerza cambio)")

        else:
            print("❌ No se pudieron calcular las complejidades")

    except Exception as e:
        print(f"\n💥 ERROR: {e}")
        import traceback
        traceback.print_exc()

def main():
    """
    Función principal.
    """
    # Aquí puedes cambiar las ecuaciones directamente
    mejor_caso =    "T(n)= 2*T(n/2) + c*n"           
    caso_promedio = "T(n)= (2/n)*SUM(k=0 to n-1)T(k) + c*n"            
    peor_caso =     "T(n)= T(n-1) + c*n"           

    print(f"Probando ecuaciones:")
    print(f"  Mejor caso: {mejor_caso}")
    print(f"  Caso promedio: {caso_promedio}")
    print(f"  Peor caso: {peor_caso}")
    print()

    probar_ecuaciones(mejor_caso, caso_promedio, peor_caso)

if __name__ == "__main__":
    main()

# Ecuaciones de ejemplo para probar:

#? Búsqueda Lineal
#TODO   Mejor Caso (Ω): K1
#**     Caso Promedio (Θ): K2 + (n/2)*C
#!      Peor Caso (O): K3 + n*C

#? Búsqueda Binaria
#TODO   Mejor Caso (Ω):      K1
#**     Caso Promedio (Θ):   K2 + (log2(n)/2)*C
#!      Peor Caso (O):       K3 + log2(n)*C

#? bubbleSort
#TODO   Mejor Caso (Ω):      K1 + n*C
#**     Caso Promedio (Θ):   K2 + (n^2/2)*C
#!      Peor Caso (O):       K3 + (n^2/2)*C

#? Fibinacci
#TODO   Mejor Caso (Ω):      T(n) = T(n-1) + T(n-2) + c
#**     Caso Promedio (Θ):   T(n) = T(n-1) + T(n-2) + c
#!      Peor Caso (O):       T(n) = T(n-1) + T(n-2) + c
# 	base_cases:
#       - T(0): c
#       - T(1): c

#? Factorial
#TODO   Mejor Caso (Ω):      T(n) = T(n-1) + c
#**     Caso Promedio (Θ):   T(n) = T(n-1) + c
#!      Peor Caso (O):       T(n) = T(n-1) + c
#       base_cases:
#       - T(0): c
#       - T(1): c

#? MergeSort
#TODO   Mejor Caso (Ω):      T(n) = 2*T(n/2) + c*n
#**     Caso Promedio (Θ):   T(n) = 2*T(n/2) + c*n
#!      Peor Caso (O):       T(n) = 2*T(n/2) + c*n
#       Caso Base:         T(1) = c

#? Quicksort
#TODO   Mejor Caso (Ω):      T(n) = 2*T(n/2) + c*n
#**     Caso Promedio (Θ):   T(n) = (2/n)*SUM(k=0 to n-1)T(k) + c*n
#!      Peor Caso (O):       T(n) = T(n-1) + c*n
#       Caso Base:           T(n) = T(n-1) + c·n
#                            T(1) = c

#? Torre de Hanoi
#TODO   Mejor Caso (Ω):      T(n) = 2*T(n-1) + c
#**     Caso Promedio (Θ):   T(n) = 2*T(n- 1) +c
#!      Peor Caso (O):       T(n) = 2*T(n-1) + c

