# Backend/test_resolver_v2.py

from agentes.agenteResolver import AgenteResolver

def probar_con_detalles():
    """
    Prueba exhaustiva de los 3 métodos implementados.
    """
    resolver = AgenteResolver()
    
    print("╔" + "═" * 68 + "╗")
    print("║" + " PRUEBAS DEL AGENTE RESOLVER - FASE 1".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    casos = [
        # ═══════════════════════════════════════════════════════════
        # TEOREMA MAESTRO - División uniforme estándar
        # ═══════════════════════════════════════════════════════════
        {
            'nombre': 'MergeSort (Teorema Maestro - Caso 2)',
            'ecuacion': 'T(n) = 2T(n/2) + n',
            'esperado': 'Θ(n log n)',
            'metodo': 'TeoremaMAestro'
        },
        {
            'nombre': 'Búsqueda Binaria (Teorema Maestro - Caso 2)',
            'ecuacion': 'T(n) = T(n/2) + 1',
            'esperado': 'Θ(log n)',
            'metodo': 'TeoremaMAestro'
        },
        
        # ═══════════════════════════════════════════════════════════
        # MÉTODO DE SUMAS - Decrementación simple
        # ═══════════════════════════════════════════════════════════
        {
            'nombre': 'Selection Sort (Método de Sumas)',
            'ecuacion': 'T(n) = T(n-1) + n',
            'esperado': 'n(n+1)/2 + c',
            'metodo': 'MetodoSumas'
        },
        {
            'nombre': 'Contador Simple (Método de Sumas)',
            'ecuacion': 'T(n) = T(n-1) + 1',
            'esperado': 'n + c',
            'metodo': 'MetodoSumas'
        },
        
        # ═══════════════════════════════════════════════════════════
        # MÉTODO DE ITERACIÓN - Expansión y simplificación
        # ═══════════════════════════════════════════════════════════
        {
            'nombre': 'Potencias (Método de Iteración)',
            'ecuacion': 'T(n) = T(n-1) + 2**n',
            'esperado': '2^(n+1) - 2 + c',
            'metodo': 'MetodoIteracion'
        },
        
        # ═══════════════════════════════════════════════════════════
        # ECUACIONES CARACTERÍSTICAS - Lineales múltiples
        # ═══════════════════════════════════════════════════════════
        {
            'nombre': 'Torres de Hanoi (Ecuación Característica)',
            'ecuacion': 'T(n) = 2T(n-1) + 1',
            'esperado': 'C·2ⁿ - 1',
            'metodo': 'EcuacionCaracteristica'
        },
        {
            'nombre': 'Fibonacci (Ecuación Característica)',
            'ecuacion': 'T(n) = T(n-1) + T(n-2)',
            'esperado': 'C₁·φⁿ + C₂·ψⁿ',
            'metodo': 'EcuacionCaracteristica'
        },
        
        # ═══════════════════════════════════════════════════════════
        # ÁRBOL DE RECURSIÓN - División asimétrica
        # ═══════════════════════════════════════════════════════════
        {
            'nombre': 'División Asimétrica 1/3 y 2/3 (Árbol de Recursión)',
            'ecuacion': 'T(n) = T(n/3) + T(2n/3) + n',
            'esperado': 'c·n·log(n)',
            'metodo': 'ArbolRecursion'
        },
        {
            'nombre': 'Múltiples Divisiones Diferentes (Árbol de Recursión)',
            'ecuacion': 'T(n) = T(n/2) + T(n/4) + T(n/8) + n',
            'esperado': 'c·n',
            'metodo': 'ArbolRecursion'
        }
    ]
    
    resultados = {
        'exitosos': 0,
        'fallidos': 0,
        'omitidos': 0,
        'detalles': []
    }
    
    for i, caso in enumerate(casos, 1):
        print(f"\n{'━' * 70}")
        print(f"CASO {i}: {caso['nombre']}")
        print(f"{'━' * 70}")
        print(f"📝 Ecuación: {caso['ecuacion']}")
        print(f"🎯 Esperado: {caso['esperado']}")
        print(f"🔧 Método: {caso['metodo']}")
        print()
        
        try:
            resultado = resolver.resolver_ecuacion(caso['ecuacion'])
            
            if resultado['exito']:
                print(f"✅ ÉXITO")
                print(f"   Método usado: {resultado['metodo_usado']}")
                print(f"   Solución: {resultado['solucion']}")
                
                # Verificar si usó el método esperado
                if resultado['metodo_usado'] == caso['metodo']:
                    print(f"   ✓ Método correcto")
                else:
                    print(f"   ⚠️  Método diferente al esperado")
                
                # Mostrar TODOS los pasos del proceso
                print(f"\n   📋 Proceso completo ({len(resultado['pasos'])} pasos):")
                print(f"   {'-' * 66}")
                for j, paso in enumerate(resultado['pasos'], 1):
                    if paso.strip():
                        print(f"   {j:2d}. {paso}")
                print(f"   {'-' * 66}")
                
                resultados['exitosos'] += 1
                resultados['detalles'].append({
                    'caso': caso['nombre'],
                    'status': 'OK',
                    'metodo': resultado['metodo_usado']
                })
                
            else:
                print(f"❌ FALLÓ")
                print(f"   Razón: {resultado['explicacion'][:200]}...")
                
                resultados['fallidos'] += 1
                resultados['detalles'].append({
                    'caso': caso['nombre'],
                    'status': 'FAIL',
                    'razon': resultado['explicacion']
                })
        
        except Exception as e:
            print(f"💥 ERROR INESPERADO")
            print(f"   {type(e).__name__}: {str(e)}")
            
            resultados['fallidos'] += 1
            resultados['detalles'].append({
                'caso': caso['nombre'],
                'status': 'ERROR',
                'error': str(e)
            })
    
    # Resumen final
    print("\n" + "╔" + "═" * 68 + "╗")
    print("║" + " RESUMEN DE PRUEBAS".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print(f"Total de casos: {len(casos)}")
    print(f"✅ Exitosos: {resultados['exitosos']}")
    print(f"❌ Fallidos: {resultados['fallidos']}")
    print(f"⏭️  Omitidos: {resultados['omitidos']}")
    casos_ejecutados = len(casos) - resultados['omitidos']
    if casos_ejecutados > 0:
        print(f"📊 Tasa de éxito: {(resultados['exitosos']/casos_ejecutados*100):.1f}%")
    print()
    
    # Métodos cubiertos
    metodos_usados = {}
    for detalle in resultados['detalles']:
        if detalle['status'] == 'OK':
            metodo = detalle['metodo']
            metodos_usados[metodo] = metodos_usados.get(metodo, 0) + 1
    
    if metodos_usados:
        print("Métodos probados:")
        for metodo, count in metodos_usados.items():
            print(f"  ✓ {metodo}: {count} caso(s)")
        print()
    
    # Detalles de fallos
    if resultados['fallidos'] > 0:
        print("Casos fallidos:")
        for detalle in resultados['detalles']:
            if detalle['status'] != 'OK' and detalle['status'] != 'SKIPPED':
                print(f"  • {detalle['caso']}: {detalle.get('razon', detalle.get('error', 'Unknown'))[:80]}")
    
    # Casos omitidos
    if resultados['omitidos'] > 0:
        print("\nCasos omitidos (requieren implementación futura):")
        for detalle in resultados['detalles']:
            if detalle['status'] == 'SKIPPED':
                print(f"  ⏭️  {detalle['caso']}")
    
    print("\n" + "═" * 70)
    
    return resultados

def probar_caso_individual(ecuacion):
    """
    Prueba detallada de un solo caso.
    Útil para debugging.
    """
    resolver = AgenteResolver()
    
    print("╔" + "═" * 68 + "╗")
    print("║" + " PRUEBA INDIVIDUAL".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    print(f"Ecuación: {ecuacion}")
    print()
    
    resultado = resolver.resolver_ecuacion(ecuacion)
    
    if resultado['exito']:
        print("✅ RESUELTO CON ÉXITO\n")
        print(f"Método: {resultado['metodo_usado']}")
        print(f"Solución: {resultado['solucion']}\n")
        
        print("=" * 70)
        print("PASOS DE RESOLUCIÓN:")
        print("=" * 70)
        for paso in resultado['pasos']:
            print(paso)
        
        print("\n" + "=" * 70)
        print("EXPLICACIÓN:")
        print("=" * 70)
        print(resultado['explicacion'])
    else:
        print("❌ NO SE PUDO RESOLVER\n")
        print(resultado['explicacion'])
    
    return resultado

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Modo: probar ecuación específica
        ecuacion = ' '.join(sys.argv[1:])
        probar_caso_individual(ecuacion)
    else:
        # Modo: probar todos los casos
        probar_con_detalles()