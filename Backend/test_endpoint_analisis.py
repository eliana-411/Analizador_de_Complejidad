"""
Test del endpoint /analisis/analizar para verificar respuesta completa
"""
import requests
import json

url = "http://localhost:8000/analisis/analizar"

pseudocodigo_con_error = """Algoritmo Prueba5 (n)
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

payload = {
    "entrada": pseudocodigo_con_error,
    "tipo_entrada": "auto",
    "auto_corregir": True
}

print("="* 80)
print("TEST ENDPOINT /analisis/analizar")
print("="* 80)

try:
    response = requests.post(url, json=payload, timeout=60)

    print(f"\n[STATUS]: {response.status_code}")

    if response.status_code == 200:
        data = response.json()

        print(f"\n[KEYS EN RESPUESTA]:")
        for key in data.keys():
            print(f"  - {key}: {type(data[key]).__name__}")

        print(f"\n[VALIDACION_INICIAL]:")
        if data.get('validacion_inicial'):
            print(f"  Existe: True")
            print(f"  Válido general: {data['validacion_inicial'].get('valido_general')}")
            print(f"  Errores totales: {data['validacion_inicial'].get('resumen', {}).get('errores_totales')}")
        else:
            print(f"  Existe: False")

        print(f"\n[CORRECCION]:")
        if data.get('correccion'):
            print(f"  Existe: True")
            print(f"  Corregido: {data['correccion'].get('corregido')}")
            print(f"  Explicación: {data['correccion'].get('explicacion', '')[:100]}...")
            print(f"  Ejemplos usados: {data['correccion'].get('ejemplos_usados')}")
        else:
            print(f"  Existe: False")

        # Guardar respuesta completa
        with open("test_endpoint_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        print(f"\n[OK] Respuesta completa guardada en: test_endpoint_response.json")

    else:
        print(f"\n[ERROR]: {response.text}")

except Exception as e:
    print(f"\n[ERROR]: {e}")

print("\n" + "="* 80)
