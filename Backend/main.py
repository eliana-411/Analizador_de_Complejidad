from services.servicioTraductor import ServicioTraductor
from services.servicioValidador import servicioValidador

def main():
    print("=" * 80)
    print("  🎓 ANALIZADOR DE COMPLEJIDAD - Traductor de Lenguaje Natural")
    print("=" * 80)
    print()
    
    print("📝 Describe el algoritmo que deseas crear en lenguaje natural")
    print()
    print("💡 Ejemplos:")
    print("   • 'Buscar un elemento en un arreglo recorriendo uno por uno'")
    print("   • 'Ordenar números intercambiando adyacentes si están desordenados'")
    print("   • 'Calcular factorial de un número multiplicándolo recursivamente'")
    print("   • 'Contar cuántos números pares hay en un arreglo'")
    print()
    print("─" * 80)
    
    # Obtener descripción del usuario
    print("\n✏️  Escribe tu descripción (presiona ENTER dos veces para terminar):")
    print("─" * 80)
    
    lineas = []
    while True:
        linea = input()
        if linea == "" and lineas:  # ENTER vacío y ya hay algo escrito
            break
        if linea:
            lineas.append(linea)
    
    descripcion = " ".join(lineas).strip()
    
    if not descripcion:
        print("\n❌ No se ingresó ninguna descripción")
        return
    
    print()
    print("=" * 80)
    print("  🤖 TRADUCCIÓN CON RAG")
    print("=" * 80)
    print()
    
    # Inicializar traductor
    print("📚 Cargando base de conocimiento...")
    traductor = ServicioTraductor()
    
    # Mostrar estadísticas
    stats = traductor.obtener_estadisticas_base()
    print(f"✅ {stats['total_ejemplos']} ejemplos cargados")
    print(f"   • Iterativos: {stats['iterativos']}")
    print(f"   • Recursivos: {stats['recursivos']}")
    print()
    
    # Traducir
    print("⚙️  Analizando descripción y generando pseudocódigo...")
    print()
    
    resultado = traductor.traducir(descripcion)
    
    print("=" * 80)
    print("  ✨ RESULTADO DE LA TRADUCCIÓN")
    print("=" * 80)
    print()
    
    if not resultado['traducido']:
        print("❌ No se pudo traducir")
        print(f"📝 Razón: {resultado['explicacion']}")
        return
    
    print("✅ Traducción exitosa")
    print()
    
    if resultado['ejemplos_usados']:
        print("📖 Ejemplos usados como referencia:")
        for ejemplo in resultado['ejemplos_usados']:
            print(f"   • {ejemplo}")
        print()
    
    print(f"🏷️  Tipo detectado: {resultado['tipo_detectado']}")
    print()
    
    print("💻 PSEUDOCÓDIGO GENERADO:")
    print("─" * 80)
    print(resultado['pseudocodigo'])
    print("─" * 80)
    print()
    
    # Preguntar si quiere validar
    print("=" * 80)
    print("  🔍 VALIDACIÓN")
    print("=" * 80)
    print()
    
    validar = input("¿Validar el pseudocódigo generado? (s/n): ").strip().lower()
    
    if validar == 's':
        print()
        print("🔍 Validando pseudocódigo...\n")
        
        validador = servicioValidador()
        resultado_validacion = validador.validar(resultado['pseudocodigo'])
        
        print("=" * 80)
        print("  📊 RESULTADO VALIDACIÓN")
        print("=" * 80)
        print()
        
        print(f"✓ Válido:         {'SÍ ✅' if resultado_validacion['valido_general'] else 'NO ❌'}")
        print(f"✓ Tipo:           {resultado_validacion['tipo_algoritmo']}")
        print(f"✓ Total Errores:  {resultado_validacion['resumen']['errores_totales']}")
        print()
        
        # Mostrar resumen
        print("📊 RESUMEN:")
        print(f"  • Líneas totales:         {resultado_validacion['resumen']['total_lineas']}")
        print(f"  • Clases encontradas:     {resultado_validacion['resumen']['clases_encontradas']}")
        print(f"  • Subrutinas encontradas: {resultado_validacion['resumen']['subrutinas_encontradas']}")
        print()
        
        if not resultado_validacion['valido_general']:
            print("🔍 ERRORES ENCONTRADOS:")
            print()
            
            for capa_nombre, capa_datos in resultado_validacion['capas'].items():
                if capa_datos['errores']:
                    nombre_limpio = capa_nombre.replace('_', ' ').title()
                    print(f"❌ {nombre_limpio}:")
                    for error in capa_datos['errores']:
                        print(f"   • {error}")
                    print()
        else:
            print("🎉 ¡EL PSEUDOCÓDIGO GENERADO ES VÁLIDO!")
            print("✅ Cumple con todas las capas de la gramática")
    
    print()
    print("=" * 80)
    print("  🏁 FIN DEL PROCESO")
    print("=" * 80)

if __name__ == "__main__":
    main()
