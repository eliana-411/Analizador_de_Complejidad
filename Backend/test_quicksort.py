import requests
import json

# QuickSort - código válido sin errores
pseudocodigo = """quickSort(int A[], int izq, int der)
begin
    int pivote

    if (izq < der) then
    begin
        pivote 🡨 CALL particionar(A[], izq, der)
        CALL quickSort(A[], izq, pivote - 1)
        CALL quickSort(A[], pivote + 1, der)
    end
end

particionar(int A[], int izq, int der)
begin
    int pivote, i, j, temp

    pivote 🡨 A[der]
    i 🡨 izq - 1

    for j 🡨 izq to der - 1 do
    begin
        if (A[j] ≤ pivote) then
        begin
            i 🡨 i + 1
            temp 🡨 A[i]
            A[i] 🡨 A[j]
            A[j] 🡨 temp
        end
    end

    temp 🡨 A[i + 1]
    A[i + 1] 🡨 A[der]
    A[der] 🡨 temp

    return i + 1
end
"""

# Llamar al endpoint
url = "http://localhost:8000/analisis/analizar"
data = {
    "entrada": pseudocodigo,
    "tipo_entrada": "auto",
    "auto_corregir": True
}

print("Probando QuickSort...")
print("="*60)

try:
    response = requests.post(url, json=data, timeout=180)

    print(f"Status Code: {response.status_code}")

    if response.status_code == 200:
        resultado = response.json()

        print("\nRESULTADO:")
        print(f"- exito: {resultado.get('exito')}")
        print(f"- fase_actual: {resultado.get('fase_actual')}")

        print(f"\n- validacion:")
        print(f"  valido_general: {resultado.get('validacion', {}).get('valido_general')}")
        print(f"  errores_totales: {resultado.get('validacion', {}).get('resumen', {}).get('errores_totales', 0)}")

        print(f"\n- costos_por_linea existe: {resultado.get('costos_por_linea') is not None}")
        if resultado.get('costos_por_linea'):
            omega = resultado['costos_por_linea']
            print(f"  Scenarios: {len(omega.get('scenarios', []))}")

        print(f"\n- complejidades existe: {resultado.get('complejidades') is not None}")
        if resultado.get('complejidades'):
            comp = resultado['complejidades']
            print(f"  Algorithm: {comp.get('algorithm_name')}")
            print(f"  Mejor caso: {comp.get('mejor_caso')}")
            print(f"  Caso promedio: {comp.get('caso_promedio')}")
            print(f"  Peor caso: {comp.get('peor_caso')}")

        # Guardar respuesta completa
        with open('test_quicksort_response.json', 'w', encoding='utf-8') as f:
            json.dump(resultado, f, indent=2, ensure_ascii=False)
        print("\nRespuesta guardada en: test_quicksort_response.json")

    else:
        print(f"ERROR: {response.status_code}")
        print(response.text)

except Exception as e:
    print(f"ERROR: {e}")
