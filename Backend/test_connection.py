"""
Script para probar la conexión con la API de Claude.

Uso:
    python test_connection.py

Antes de ejecutar:
    1. Asegúrate de haber instalado las dependencias: pip install -r requirements.txt
    2. Configura tu ANTHROPIC_API_KEY en el archivo .env
"""

from services.llm_service import LLMService


def main():
    print("=" * 60)
    print("PRUEBA DE CONEXIÓN CON LA API DE CLAUDE")
    print("=" * 60)
    print()

    print("Probando conexión con la API de Anthropic...")
    print()

    result = LLMService.test_connection()

    if result["status"] == "success":
        print("✓ CONEXIÓN EXITOSA")
        print(f"  Modelo: {result['model']}")
        print(f"  Respuesta de Claude: {result['response']}")
        print()
        print("La API está configurada correctamente y lista para usar.")
    else:
        print("✗ ERROR EN LA CONEXIÓN")
        print(f"  Tipo: {result.get('type', 'unknown')}")
        print(f"  Mensaje: {result['message']}")
        print()

        if result.get("type") == "configuration_error":
            print("SOLUCIÓN:")
            print("  1. Abre el archivo .env")
            print("  2. Reemplaza 'tu_api_key_aqui' con tu API key de Anthropic")
            print("  3. Guarda el archivo y vuelve a ejecutar este script")
        else:
            print("POSIBLES CAUSAS:")
            print("  - Verifica que la API key sea válida")
            print("  - Asegúrate de tener conexión a internet")
            print("  - Revisa que hayas instalado las dependencias correctamente")

    print()
    print("=" * 60)


if __name__ == "__main__":
    main()