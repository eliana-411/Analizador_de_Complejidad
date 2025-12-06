import requests
import json

# Código sin errores
pseudocodigo = """BusquedaLineal(int A[], int n, int x)
begin
    int i
    bool encontrado

    encontrado 🡨 false
    i 🡨 1

    while (i <= n) and (not encontrado) do
    begin
        if (A[i] = x) then
        begin
            encontrado 🡨 true
        end
        i 🡨 i + 1
    end

    if encontrado then
    begin
        return i
    end
    else
    begin
        return -1
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

print("Llamando al endpoint /analisis/analizar con código sin errores...")
print("="*60)

try:
    response = requests.post(url, json=data, timeout=120)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        resultado = response.json()

        print("\nRESULTADO:")
        print(f"- exito: {resultado.get('exito')}")
        print(f"- fase_actual: {resultado.get('fase_actual')}")

        print(f"\n- validacion: valido={resultado.get('validacion', {}).get('valido_general')}")
        print(f"  Errores: {resultado.get('validacion', {}).get('resumen', {}).get('errores_totales', 0)}")

        print(f"\n- costos_por_linea existe: {resultado.get('costos_por_linea') is not None}")
        if resultado.get('costos_por_linea'):
            omega = resultado['costos_por_linea']
            print(f"  Scenarios: {len(omega.get('scenarios', []))}")

        print(f"\n- complejidades existe: {resultado.get('complejidades') is not None}")
        if resultado.get('complejidades'):
            comp = resultado['complejidades']
            print(f"  Mejor caso: {comp.get('mejor_caso')}")
            print(f"  Caso promedio: {comp.get('caso_promedio')}")
            print(f"  Peor caso: {comp.get('peor_caso')}")

        # Guardar respuesta completa
        with open('test_simple_response.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        print("\nRespuesta guardada en: test_simple_response.json")

    else:
        print(f"ERROR: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"ERROR: {e}")
