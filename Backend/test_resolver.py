# Backend/test_resolver.py

from agentes.agenteResolver import AgenteResolver

def probar_con_detalles():
    """
    Prueba exhaustiva de todos los métodos implementados.
    """
    resolver = AgenteResolver()
    
    print("╔" + "═" * 68 + "╗")
    print("║" + " PRUEBAS DEL AGENTE RESOLVER - COMPLETO".center(68) + "║")
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
        {
            'nombre': 'T(n/2) duplicados (Normalización + Teorema Maestro)',
            'ecuacion': 'T(n) = T(n/2) + T(n/2) + n',
            'esperado': 'Θ(n log n)',
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
        {
            'nombre': 'Decrementación paso 2 (Método de Sumas)',
            'ecuacion': 'T(n) = T(n-2) + n',
            'esperado': 'O(n²)',
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
        {
            'nombre': 'T(n-1) triplicados (Normalización + Ecuación Característica)',
            'ecuacion': 'T(n) = T(n-1) + T(n-1) + T(n-1)',
            'esperado': 'C·3ⁿ',
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
        },
        
        # ═══════════════════════════════════════════════════════════
        # ANALIZADOR DIRECTO - Expresiones iterativas
        # ═══════════════════════════════════════════════════════════
        {
            'nombre': 'Constante (Analizador Directo)',
            'ecuacion': 'T(n) = 1',
            'esperado': 'O(1)',
            'metodo': 'AnalizadorDirecto'
        },
        {
            'nombre': 'Lineal directa (Analizador Directo)',
            'ecuacion': 'T(n) = K + n*C',
            'esperado': 'O(n)',
            'metodo': 'AnalizadorDirecto'
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

def probar_analizador_directo():
    """
    Prueba del AnalizadorDirecto para expresiones directas.
    """
    print("╔" + "═" * 68 + "╗")
    print("║" + " PRUEBAS DEL ANALIZADOR DIRECTO".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    resolver = AgenteResolver()
    
    casos_directos = [
        ('T(n) = 1', '1'),
        ('T(n) = K1', '1'),
        ('T(n) = n', 'n'),
        ('T(n) = K + n*C', 'n'),
        ('T(n) = K2 + (n/2)*C', 'n'),
        ('T(n) = n**2', 'n²'),
        ('T(n) = n*log(n)', 'n·log(n)'),
    ]
    
    exitosos = 0
    fallidos = 0
    
    for ecuacion, esperado in casos_directos:
        print(f"{'─' * 70}")
        print(f"📝 {ecuacion}")
        print(f"🎯 Esperado: {esperado}")
        
        resultado = resolver.resolver_ecuacion(ecuacion)
        
        if resultado['exito']:
            print(f"✅ {resultado['metodo_usado']}: {resultado['solucion']}")
            exitosos += 1
        else:
            print(f"❌ FALLÓ: {resultado['explicacion'][:100]}")
            fallidos += 1
        print()
    
    print("═" * 70)
    print(f"Resultados: ✅ {exitosos} exitosos | ❌ {fallidos} fallidos")
    print("═" * 70)

def probar_resolver_casos():
    """
    Prueba del método resolver_casos() para analizar mejor/promedio/peor caso.
    """
    print("╔" + "═" * 68 + "╗")
    print("║" + " PRUEBAS DE RESOLVER_CASOS (3 casos)".center(68) + "║")
    print("╚" + "═" * 68 + "╝")
    print()
    
    resolver = AgenteResolver()
    
    # TEST 1: Casos iguales (MergeSort)
    print("─" * 70)
    print("TEST 1: MergeSort (casos iguales)")
    print("─" * 70)
    
    casos1 = {
        'mejor_caso': 'T(n) = 2T(n/2) + n',
        'caso_promedio': 'T(n) = 2T(n/2) + n',
        'peor_caso': 'T(n) = 2T(n/2) + n'
    }
    
    resultado1 = resolver.resolver_casos(casos1)
    
    print(f"\n📊 Complejidades:")
    print(f"   Mejor:    {resultado1['complejidades'].get('mejor_caso', 'N/A')}")
    print(f"   Promedio: {resultado1['complejidades'].get('caso_promedio', 'N/A')}")
    print(f"   Peor:     {resultado1['complejidades'].get('peor_caso', 'N/A')}")
    print(f"\n{resultado1['observacion']}")
    print()
    
    # TEST 2: Casos diferentes (QuickSort)
    print("\n" + "─" * 70)
    print("TEST 2: QuickSort (casos diferentes)")
    print("─" * 70)
    
    casos2 = {
        'mejor_caso': 'T(n) = 2T(n/2) + n',
        'caso_promedio': 'T(n) = 2T(n/2) + n',
        'peor_caso': 'T(n) = T(n-1) + n'
    }
    
    resultado2 = resolver.resolver_casos(casos2)
    
    print(f"\n📊 Complejidades:")
    print(f"   Mejor:    {resultado2['complejidades'].get('mejor_caso', 'N/A')}")
    print(f"   Promedio: {resultado2['complejidades'].get('caso_promedio', 'N/A')}")
    print(f"   Peor:     {resultado2['complejidades'].get('peor_caso', 'N/A')}")
    print(f"\n{resultado2['observacion']}")
    print()
    
    # TEST 3: Búsqueda Lineal (expresiones directas)
    print("\n" + "─" * 70)
    print("TEST 3: Búsqueda Lineal (expresiones directas)")
    print("─" * 70)
    
    casos3 = {
        'mejor_caso': 'T(n) = 1',
        'caso_promedio': 'T(n) = n/2',
        'peor_caso': 'T(n) = n'
    }
    
    resultado3 = resolver.resolver_casos(casos3)
    
    print(f"\n📊 Complejidades:")
    print(f"   Mejor:    {resultado3['complejidades'].get('mejor_caso', 'N/A')}")
    print(f"   Promedio: {resultado3['complejidades'].get('caso_promedio', 'N/A')}")
    print(f"   Peor:     {resultado3['complejidades'].get('peor_caso', 'N/A')}")
    print(f"\n{resultado3['observacion']}")
    
    print("\n" + "═" * 70)
    print("TESTS COMPLETADOS")
    print("═" * 70)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # Modo: probar ecuación específica
        ecuacion = ' '.join(sys.argv[1:])
        probar_caso_individual(ecuacion)
    else:
        # Modo: probar todos los casos
        probar_con_detalles()
        
        # Probar AnalizadorDirecto
        print("\n\n")
        probar_analizador_directo()
        
        # Probar resolver_casos (mejor, promedio, peor)
        print("\n\n")
        probar_resolver_casos()