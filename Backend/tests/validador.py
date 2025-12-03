from shared.services.lectorArchivos import LectorArchivos
from core.validador.services.orchestrator import ValidationOrchestrator

def main():
    print("=" * 80)
    print("  🎓 ANALIZADOR DE COMPLEJIDAD - Validador por Capas de la Gramática")
    print("=" * 80)
    print()
    
    # ==================== CONFIGURACIÓN ====================
    print("📋 Selecciona el archivo a validar:")
    print()
    print("  ✅ CORRECTOS (Iterativos):")
    print("    1. Búsqueda Lineal")
    print("    2. Búsqueda Binaria")
    print("    3. Bubble Sort")
    print("   10. Multiplicación de Matrices")
    print()
    print("  ✅ CORRECTOS (Recursivos):")
    print("    4. Merge Sort")
    print("    5. Quick Sort")
    print("    6. Fibonacci Recursivo")
    print("    7. Factorial Recursivo")
    print("    8. Torres de Hanoi")
    print("    9. BST Insert")
    print()
    print("  ❌ INCORRECTOS (con errores):")
    print("   11. Búsqueda Lineal (errores)")
    print("   12. Búsqueda Binaria (errores)")
    print("   13. Bubble Sort (errores)")
    print("   14. Merge Sort (errores)")
    print("   15. Quick Sort (errores)")
    print("   16. Fibonacci (errores)")
    print("   17. Factorial (errores)")
    print("   18. Torres de Hanoi (errores)")
    print("   19. BST Insert (errores)")
    print("   20. Multiplicación de Matrices (errores)")
    print()
    print("  📝 PERSONALIZADO:")
    print("    0. Ingresar ruta manualmente")
    print()
    
    opcion = input("Selecciona [0-20] ").strip()
    
    # Mapeo de opciones
    base_path = "C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/"
    archivos = {
        "1": "correctos/01-busqueda-lineal.txt",
        "2": "correctos/02-busqueda-binaria.txt",
        "3": "correctos/03-bubble-sort.txt",
        "4": "correctos/04-merge-sort.txt",
        "5": "correctos/05-quick-sort.txt",
        "6": "correctos/06-fibonacci-recursivo.txt",
        "7": "correctos/07-factorial-recursivo.txt",
        "8": "correctos/08-torres-hanoi.txt",
        "9": "correctos/09-bst-insert.txt",
        "10": "correctos/10-matrix-multiplication.txt",
        "11": "incorrectos/01-busqueda-lineal.txt",
        "12": "incorrectos/02-busqueda-binaria.txt",
        "13": "incorrectos/03-bubble-sort.txt",
        "14": "incorrectos/04-merge-sort.txt",
        "15": "incorrectos/05-quick-sort.txt",
        "16": "incorrectos/06-fibonacci-recursivo.txt",
        "17": "incorrectos/07-factorial-recursivo.txt",
        "18": "incorrectos/08-torres-hanoi.txt",
        "19": "incorrectos/09-bst-insert.txt",
        "20": "incorrectos/10-matrix-multiplication.txt",
    }
    
    if opcion == "0":
        ruta = input("\n📂 Ingresa la ruta completa del archivo: ").strip()
    else:
        if not opcion:
            opcion = "6"
        ruta = base_path + archivos.get(opcion)
    
    print()
    print(f"📂 Archivo: {ruta.split('/')[-1]}")
    print("─" * 80)
    print()
    
    # ==================== LECTURA ====================
    lector = LectorArchivos(ruta)
    
    if not lector.leer_archivo():
        print("\n✗ No se pudo leer el archivo")
        return
    
    pseudocodigo = lector.obtener_contenido_completo()
    
    print("📄 PSEUDOCÓDIGO:")
    print("─" * 80)
    print(pseudocodigo)
    print("─" * 80)
    print()
    
    # ==================== VALIDADOR POR CAPAS ====================
    print("=" * 80)
    print("  🎓 VALIDACIÓN ORGANIZADA POR CAPAS DE LA GRAMÁTICA")
    print("=" * 80)
    print()

    orchestrator = ValidationOrchestrator()
    resultado_obj = orchestrator.validar(pseudocodigo, return_suggestions=True)
    resultado = resultado_obj.model_dump()  # Convertir Pydantic model a dict
    
    print(f"✓ Válido General:  {'SÍ ✅' if resultado['valido_general'] else 'NO ❌'}")
    print(f"✓ Tipo Algoritmo:  {resultado['tipo_algoritmo']}")
    print(f"✓ Total Errores:   {resultado['resumen']['errores_totales']}")
    print()
    
    # Mostrar resumen
    print("📊 RESUMEN:")
    print(f"  • Líneas totales:         {resultado['resumen']['total_lineas']}")
    print(f"  • Clases encontradas:     {resultado['resumen']['clases_encontradas']}")
    print(f"  • Subrutinas encontradas: {resultado['resumen']['subrutinas_encontradas']}")
    print()
    
    # Mostrar cada capa
    print("🔍 VALIDACIÓN POR CAPAS:")
    print()
    for capa_nombre, capa_datos in resultado['capas'].items():
        nombre_limpio = capa_nombre.replace('_', ' ').title()
        estado = "✅" if capa_datos['valido'] else "❌"
        
        print(f"{nombre_limpio}: {estado}")
        
        # Mostrar detalles positivos (máximo 5)
        if capa_datos['detalles'][:5]:
            for detalle in capa_datos['detalles'][:5]:
                print(f"  {detalle}")
            if len(capa_datos['detalles']) > 5:
                print(f"  ... y {len(capa_datos['detalles']) - 5} detalles más")
        
        # Mostrar errores (todos)
        if capa_datos['errores']:
            print(f"\n  ❌ ERRORES EN {nombre_limpio}:")
            for error in capa_datos['errores']:
                print(f"     • {error}")
        
        print()
    
    print("=" * 80)
    print("  📋 RESULTADO FINAL")
    print("=" * 80)
    print()
    
    if resultado['valido_general']:
        print("  ✅ ¡PSEUDOCÓDIGO VÁLIDO!")
        print(f"  ✅ Tipo: {resultado['tipo_algoritmo']}")
        print("  ✅ Cumple con todas las capas de la gramática")
    else:
        print("  ❌ PSEUDOCÓDIGO INVÁLIDO")
        print(f"  ❌ Se encontraron {resultado['resumen']['errores_totales']} errores")
        print("  ❌ Revisa los errores por capa arriba indicados")

        # Mostrar sugerencias si existen
        if resultado.get('sugerencias'):
            print()
            print("💡 SUGERENCIAS DE CORRECCIÓN:")
            for sugerencia in resultado['sugerencias']:
                print(f"  • {sugerencia}")

    print()
    print("=" * 80)

if __name__ == "__main__":
    main()
