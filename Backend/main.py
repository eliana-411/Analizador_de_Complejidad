from services.lectorArchivos import LectorArchivos
from agentes.agenteValidador import AgenteValidador

def main():
    print("=" * 60)
    print("    ANALIZADOR DE COMPLEJIDAD - Validador de Pseudocódigo")
    print("=" * 60)
    print()
    
    # Pide la ruta del archivo
    # ruta = input("Ingresa la ruta del archivo .txt: ")
    ruta = "C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/incorrectos/01-busqueda-lineal.txt"  # Ruta fija para pruebas rápidas
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/01-busqueda-lineal.txt --> Iterativo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/02-busqueda-binaria.txt --> Iterativo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/03-bubble-sort.txt --> Iterativo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/04-merge-sort.txt --> Recursivo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/05-quick-sort.txt --> Recursivo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/06-fibonacci-recursivo.txt --> Recursivo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/07-factorial-recursivo.txt --> Recursivo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/08-torres-hanoi.txt --> Recursivo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/09-bst-insert.txt --> Recursivo
    # C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/10-matrix-multiplication.txt --> Iterativo

    print(f"📂 Leyendo archivo: {ruta}")
    print()
    
    # 1. Leer el archivo con LectorArchivos
    lector = LectorArchivos(ruta)
    
    if not lector.leer_archivo():
        print("\n✗ No se pudo leer el archivo")
        return
    
    print("✓ Archivo leído correctamente")
    print()
    
    # 2. Obtener el contenido completo
    pseudocodigo = lector.obtener_contenido_completo()
    
    print("--- PSEUDOCÓDIGO ORIGINAL ---")
    print(pseudocodigo)
    print()
    
    # 3. Validar con el AgenteValidador
    print("🤖 Validando con AgenteValidador...")
    print()
    
    agente = AgenteValidador()
    resultado = agente.validar_algoritmo_completo(pseudocodigo)
    
    # 4. Mostrar resultados
    print("=" * 60)
    print("    REPORTE DE VALIDACIÓN")
    print("=" * 60)
    print()
    
    print(f"✓ Válido:        {'SÍ' if resultado['is_valid'] else 'NO'}")
    print(f"✓ Tipo:          {'Iterativo' if resultado['is_iterative'] else 'Recursivo'}")
    print(f"✓ Errores:       {len(resultado['errors'])}")
    print()
    
    if resultado['errors']:
        print("--- ERRORES ENCONTRADOS ---")
        for error in resultado['errors']:
            num_linea, texto, valido, mensaje = error
            print(f"  Línea {num_linea}: {mensaje}")
            if texto:
                print(f"    → {texto}")
        print()
    
    print("--- REPORTE DETALLADO ---")
    for reporte in resultado['report']:
        num_linea, texto, valido, mensaje = reporte
        simbolo = "✓" if valido else "✗"
        print(f"  {simbolo} Línea {num_linea}: {mensaje}")
    
    print()
    print("=" * 60)

if __name__ == "__main__":
    main()
