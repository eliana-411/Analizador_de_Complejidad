"""
Test rápido del endpoint analizar-con-reporte
"""
import requests
import json

# Pseudocódigo de prueba
pseudocodigo = """busquedaLineal(int A[], int n, int x)
begin
    int i
    i <- 1
    while (i <= n) do
    begin
        if (A[i] = x) then
        begin
            return i
        end
        i <- i + 1
    end
    return -1
end"""

url = "http://localhost:8000/analisis/analizar-con-reporte"

data = {
    "entrada": pseudocodigo,
    "tipo_entrada": "auto",
    "auto_corregir": True
}

print("Enviando petición...")
response = requests.post(url, json=data)

if response.status_code == 200:
    resultado = response.json()
    print("\n✅ Respuesta exitosa!")
    print(f"\nCampos presentes:")
    for key in resultado.keys():
        valor = resultado[key]
        if isinstance(valor, str) and len(valor) > 100:
            print(f"  - {key}: (string de {len(valor)} caracteres)")
        elif isinstance(valor, dict):
            print(f"  - {key}: (dict con {len(valor)} claves)")
        elif isinstance(valor, list):
            print(f"  - {key}: (list con {len(valor)} elementos)")
        else:
            print(f"  - {key}: {valor}")
    
    # Verificar campos importantes
    print(f"\n📊 Reporte markdown presente: {bool(resultado.get('reporte_markdown'))}")
    print(f"🔍 Validación complejidades presente: {bool(resultado.get('validacion_complejidades'))}")
    
    if resultado.get('validacion_complejidades'):
        val = resultado['validacion_complejidades']
        print(f"\n✓ Concordancia: {val.get('concordancia')}")
        print(f"✓ Confianza: {val.get('confianza'):.0%}")
        
    if resultado.get('reporte_markdown'):
        reporte = resultado['reporte_markdown']
        print(f"\n📄 Primeras 200 caracteres del reporte:")
        print(reporte[:200])
else:
    print(f"\n❌ Error: {response.status_code}")
    print(response.text)
