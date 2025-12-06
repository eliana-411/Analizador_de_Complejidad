"""
Test simple para verificar qué retorna el ServicioCorrector
"""
import json
from shared.services.servicioValidador import servicioValidador
from shared.services.servicioCorrector import ServicioCorrector

# Pseudocódigo con error de comillas dobles
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

print("=" * 80)
print("TEST DE CORRECCIÓN")
print("=" * 80)

# 1. Validar
validador = servicioValidador()
validacion = validador.validar(pseudocodigo_con_error)

print(f"\n[1] VALIDACIÓN INICIAL:")
print(f"    Válido: {validacion['valido_general']}")
print(f"    Errores totales: {validacion['resumen']['errores_totales']}")

# 2. Corregir
corrector = ServicioCorrector()
resultado_correccion = corrector.corregir(pseudocodigo_con_error, validacion)

print(f"\n[2] CORRECCIÓN:")
print(f"    Corregido: {resultado_correccion.get('corregido', False)}")

# Mostrar estructura completa del resultado de corrección
print(f"\n[3] ESTRUCTURA COMPLETA DE CORRECCIÓN:")
with open("test_correccion_output.json", "w", encoding="utf-8") as f:
    json.dump(resultado_correccion, f, indent=2, ensure_ascii=False, default=str)
print("    -> Guardado en test_correccion_output.json")

# Mostrar keys principales
print(f"\n[4] KEYS EN RESULTADO DE CORRECCIÓN:")
for key in resultado_correccion.keys():
    print(f"    - {key}: {type(resultado_correccion[key]).__name__}")

print("\n" + "=" * 80)
