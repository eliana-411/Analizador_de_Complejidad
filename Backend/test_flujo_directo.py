"""
Test directo del FlujoAnalisis para ver qué keys retorna
"""
from tests.flujo_analisis import FlujoAnalisis
import json

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

print("="* 80)
print("TEST DIRECTO FLUJO ANALISIS")
print("="* 80)

flujo = FlujoAnalisis(modo_verbose=False)
resultado = flujo.analizar(
    entrada=pseudocodigo_con_error,
    tipo_entrada="auto",
    auto_corregir=True
)

print(f"\n[KEYS EN RESULTADO]:")
for key in resultado.keys():
    value_type = type(resultado[key]).__name__
    is_none = resultado[key] is None
    print(f"  - {key}: {value_type} {'(None)' if is_none else ''}")

print(f"\n[VALIDACION_INICIAL]:")
if 'validacion_inicial' in resultado:
    print(f"  Existe en dict: True")
    print(f"  Valor es None: {resultado['validacion_inicial'] is None}")
    if resultado['validacion_inicial']:
        print(f"  Errores totales: {resultado['validacion_inicial'].get('resumen', {}).get('errores_totales')}")
else:
    print(f"  Existe en dict: False")

print(f"\n[CORRECCION]:")
if 'correccion' in resultado:
    print(f"  Existe en dict: True")
    print(f"  Valor es None: {resultado['correccion'] is None}")
    if resultado['correccion']:
        print(f"  Corregido: {resultado['correccion'].get('corregido')}")
        print(f"  Keys: {list(resultado['correccion'].keys())}")
else:
    print(f"  Existe en dict: False")

# Guardar
with open("test_flujo_resultado.json", "w", encoding="utf-8") as f:
    json.dump(resultado, f, indent=2, ensure_ascii=False, default=str)
print(f"\n[OK] Resultado completo guardado en: test_flujo_resultado.json")

print("\n" + "="* 80)
