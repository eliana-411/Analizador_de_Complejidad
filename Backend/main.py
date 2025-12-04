from shared.services.servicioTraductor import ServicioTraductor
from shared.services.servicioValidador import servicioValidador
from shared.services.servicioCorrector import ServicioCorrector

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
    
    validador = servicioValidador()
    resultado_validacion = validador.validar(resultado['pseudocodigo'])
    
    print(f"✓ Válido General:  {'SÍ ✅' if resultado_validacion['valido_general'] else 'NO ❌'}")
    print(f"✓ Tipo Algoritmo:  {resultado_validacion['tipo_algoritmo']}")
    print(f"✓ Total Errores:   {resultado_validacion['resumen']['errores_totales']}")
    print()
    
    if resultado_validacion['valido_general']:
        print("  ✅ ¡PSEUDOCÓDIGO VÁLIDO!")
        print(f"  ✅ Tipo: {resultado_validacion['tipo_algoritmo']}")
        print("  ✅ Cumple con todas las capas de la gramática v2.0")
    else:
        print("  ❌ PSEUDOCÓDIGO INVÁLIDO")
        print(f"  ❌ Se encontraron {resultado_validacion['resumen']['errores_totales']} errores")
        print()
        
        # ==================== CORRECCIÓN AUTOMÁTICA CON RAG ====================
        print("=" * 80)
        print("  🤖 CORRECCIÓN AUTOMÁTICA CON RAG")
        print("=" * 80)
        print()
        
        respuesta = input("¿Deseas que el sistema corrija automáticamente los errores? (s/n): ").strip().lower()
        
        if respuesta == 's':
            print("\n🔍 Analizando errores y buscando ejemplos similares...")
            print()
            
            corrector = ServicioCorrector()
            
            # Mostrar estadísticas de la base de conocimiento
            stats = corrector.obtener_estadisticas_base()
            print(f"📚 Base de conocimiento: {stats['total_ejemplos']} ejemplos")
            print(f"   • Iterativos: {stats['iterativos']}")
            print(f"   • Recursivos: {stats['recursivos']}")
            print()
            
            # Corregir usando RAG
            print("⚙️ Generando corrección con IA...")
            resultado_correccion = corrector.corregir(resultado['pseudocodigo'], resultado_validacion)
            
            print()
            print("=" * 80)
            print("  ✨ RESULTADO DE LA CORRECCIÓN")
            print("=" * 80)
            print()
            
            if resultado_correccion['corregido']:
                print("  ✅ Corrección exitosa")
                print()
                print(f"  📖 Ejemplos usados como referencia:")
                for ejemplo in resultado_correccion['ejemplos_usados']:
                    print(f"     • {ejemplo}")
                print()
                
                print("  📝 EXPLICACIÓN:")
                print("  " + "─" * 76)
                # Mostrar solo la parte de correcciones, no todo el pseudocódigo
                explicacion_lineas = resultado_correccion['explicacion'].split('\n')
                for linea in explicacion_lineas[:15]:  # Primeras 15 líneas
                    print(f"  {linea}")
                print()
                
                print("  💻 PSEUDOCÓDIGO CORREGIDO:")
                print("  " + "─" * 76)
                print(resultado_correccion['pseudocodigo'])
                print("  " + "─" * 76)
                print()
                
                # Preguntar si quiere validar la corrección
                validar_correccion = input("¿Validar pseudocódigo corregido? (s/n): ").strip().lower()
                
                if validar_correccion == 's':
                    print("\n🔍 Validando pseudocódigo corregido...\n")
                    
                    validador2 = servicioValidador()
                    resultado2 = validador2.validar(resultado_correccion['pseudocodigo'])
                    
                    if resultado2['valido_general']:
                        print("  🎉 ¡PSEUDOCÓDIGO CORREGIDO ES VÁLIDO!")
                        print(f"  ✅ Tipo: {resultado2['tipo_algoritmo']}")
                        print("  ✅ Sin errores")
                    else:
                        print("  ⚠️ El pseudocódigo corregido aún tiene errores:")
                        print(f"  ❌ {resultado2['resumen']['errores_totales']} errores restantes")
                        print("  💡 Puede requerir ajustes manuales adicionales")
            else:
                print("  ❌ No se pudo corregir automáticamente")
                print(f"  📝 Razón: {resultado_correccion['explicacion']}")
        else:
            print("\n  💡 Puedes revisar y corregir los errores manualmente")
    
    print()
    print("=" * 80)
    print("  🏁 FIN DEL PROCESO")
    print("=" * 80)

if __name__ == "__main__":
    main()
