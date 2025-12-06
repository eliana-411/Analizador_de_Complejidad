import requests
import json

# Código con error de comillas dobles
pseudocodigo = """Algoritmo Prueba5 (n)
begin
  for i <- 0 to n do
  begin
    print (i)
    if (i mod 2) = 0 then
    begin
      print ("Par")
    end
  end
end
"""

# Llamar al endpoint
url = "http://localhost:8000/analisis/analizar"
data = {
    "entrada": pseudocodigo,
    "tipo_entrada": "auto",
    "auto_corregir": True
}

print("Llamando al endpoint /analisis/analizar...")
print("="*60)

try:
    response = requests.post(url, json=data, timeout=60)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        resultado = response.json()

        print("\nRESULTADO:")
        print(f"- exito: {resultado.get('exito')}")
        print(f"- fase_actual: {resultado.get('fase_actual')}")

        print(f"\n- validacion_inicial existe: {resultado.get('validacion_inicial') is not None}")
        if resultado.get('validacion_inicial'):
            print(f"  Errores: {resultado['validacion_inicial'].get('resumen', {}).get('errores_totales', 0)}")

        print(f"\n- correccion existe: {resultado.get('correccion') is not None}")
        if resultado.get('correccion'):
            print(f"  corregido: {resultado['correccion'].get('corregido')}")
            print(f"  tiene explicacion: {resultado['correccion'].get('explicacion') is not None}")

        # Guardar respuesta completa
        with open('test_endpoint_response.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        print("\nRespuesta guardada en: test_endpoint_response.json")

    else:
        print(f"ERROR: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"ERROR: {e}")
