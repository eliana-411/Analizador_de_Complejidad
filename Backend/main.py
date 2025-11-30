from Backend.lectorArchivos import LectorArchivos

def main():
    print("=== Analizador de Complejidad ===\n")
    
    # Pide la ruta del archivo
    # ruta = input("Ingresa la ruta del archivo .txt: ")
    ruta = "Backend/algoritmos/prueba.txt"  # Ruta fija para pruebas rápidas
    
    # Crea el lector
    lector = LectorArchivos(ruta)
    
    # Lee el archivo
    if lector.leer_archivo():
        print("\nArchivo leído correctamente\n")
        print("--- Contenido del archivo ---\n")
        
        # Obtiene todas las líneas
        lineas = lector.obtener_lineas()
        
        # Muestra cada línea con su número
        for linea in lineas:
            print(f"{linea['num_linea']}: {linea['texto']}")
        
        print(f"\nTotal de líneas: {len(lineas)}")
    else:
        print("\n✗ No se pudo leer el archivo")

if __name__ == "__main__":
    main()
