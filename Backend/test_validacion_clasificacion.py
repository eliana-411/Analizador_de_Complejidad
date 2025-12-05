"""
Script de Prueba: Validación + Clasificación ML

Prueba el endpoint de validación que ahora incluye:
1. Validación por 7 capas
2. Clasificación ML del algoritmo

Uso:
    python test_validacion_clasificacion.py
"""

import requests
import json


def test_validacion_clasificacion():
    """Prueba el endpoint de validación con clasificación ML"""

    # URL del endpoint
    url = "http://localhost:8000/validador/validar"

    # Pseudocódigo de prueba: Búsqueda Lineal
    pseudocodigo = """busquedaLineal(int A[], int n, int x)
begin
    int i
    bool encontrado

    encontrado <- F
    i <- 1

    while (i <= n and not encontrado) do
    begin
        if (A[i] = x) then
        begin
            encontrado <- T
        end
        i <- i + 1
    end

    return encontrado
end"""

    # Request
    payload = {
        "pseudocodigo": pseudocodigo,
        "return_suggestions": True
    }

    print("=" * 80)
    print("TEST: Validación + Clasificación ML")
    print("=" * 80)
    print()
    print("Endpoint:", url)
    print("Pseudocódigo:", pseudocodigo[:50] + "...")
    print()

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()

        resultado = response.json()

        print("[OK] Respuesta recibida")
        print()

        # Mostrar validación
        print("=" * 80)
        print("1. VALIDACIÓN")
        print("=" * 80)
        print()
        print(f"Válido General: {'SI' if resultado['valido_general'] else 'NO'}")
        print(f"Tipo Algoritmo: {resultado['tipo_algoritmo']}")
        print()

        print("Capas de Validación:")
        print("-" * 80)
        for capa_nombre, capa_datos in resultado['capas'].items():
            status = "[OK]" if capa_datos['valido'] else "[ERROR]"
            print(f"{status} {capa_nombre}")

            if not capa_datos['valido'] and capa_datos['errores']:
                for error in capa_datos['errores']:
                    print(f"      - {error}")
        print()

        # Mostrar clasificación
        print("=" * 80)
        print("2. CLASIFICACIÓN ML")
        print("=" * 80)
        print()

        if resultado.get('clasificacion'):
            clasificacion = resultado['clasificacion']
            print(f"Categoría Principal: {clasificacion['categoria_principal']}")
            print(f"Confianza: {clasificacion['confianza']*100:.2f}%")
            print()
            print("Top 3 Predicciones:")
            for i, pred in enumerate(clasificacion['top_predicciones'], 1):
                print(f"  {i}. {pred['categoria']:30} {pred['probabilidad']*100:6.2f}%")
        else:
            print("[WARN] No se pudo ejecutar la clasificación ML")
            print("       (modelo no encontrado o error)")

        print()

        # Mostrar resumen
        print("=" * 80)
        print("3. RESUMEN")
        print("=" * 80)
        print()
        resumen = resultado['resumen']
        print(f"Total Líneas: {resumen['total_lineas']}")
        print(f"Clases Encontradas: {resumen['clases_encontradas']}")
        print(f"Subrutinas Encontradas: {resumen['subrutinas_encontradas']}")
        print(f"Errores Totales: {resumen['errores_totales']}")
        print()

        # Mostrar JSON completo (para debugging)
        print("=" * 80)
        print("4. JSON COMPLETO")
        print("=" * 80)
        print()
        print(json.dumps(resultado, indent=2, ensure_ascii=False))
        print()

        print("=" * 80)
        print("TEST COMPLETADO")
        print("=" * 80)

    except requests.exceptions.ConnectionError:
        print("[ERROR] No se pudo conectar al servidor")
        print("        Asegúrate de que el servidor esté corriendo:")
        print("        cd Backend && python app.py")
    except requests.exceptions.HTTPError as e:
        print(f"[ERROR] Error HTTP: {e}")
        if hasattr(e.response, 'json'):
            print(json.dumps(e.response.json(), indent=2, ensure_ascii=False))
    except Exception as e:
        print(f"[ERROR] Error inesperado: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    test_validacion_clasificacion()
