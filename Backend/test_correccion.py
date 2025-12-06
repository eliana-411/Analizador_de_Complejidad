"""
Test rápido para verificar que el flujo retorna datos de corrección
"""
import json
from tests.flujo_analisis import FlujoAnalisis

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

print("="*60)
print("PRUEBA DE CORRECCIÓN AUTOMÁTICA")
print("="*60)

flujo = FlujoAnalisis(modo_verbose=True)
resultado = flujo.analizar(
    entrada=pseudocodigo_con_error,
    tipo_entrada="pseudocodigo",
    auto_corregir=True
)

print("\n" + "="*60)
print("RESULTADO DEL ANÁLISIS")
print("="*60)

print(f"\nExito: {resultado['exito']}")
print(f"Fase actual: {resultado['fase_actual']}")

print(f"\nValidacion inicial existe: {resultado.get('validacion_inicial') is not None}")
if resultado.get('validacion_inicial'):
    print(f"  - Errores totales: {resultado['validacion_inicial'].get('resumen', {}).get('errores_totales', 0)}")

print(f"\nCorreccion existe: {resultado.get('correccion') is not None}")
if resultado.get('correccion'):
    print(f"  - Corregido: {resultado['correccion'].get('corregido')}")
    print(f"  - Tiene explicacion: {resultado['correccion'].get('explicacion') is not None}")
    print(f"  - Ejemplos usados: {len(resultado['correccion'].get('ejemplos_usados', []))} ejemplos")

print(f"\nValidacion final existe: {resultado.get('validacion') is not None}")
if resultado.get('validacion'):
    print(f"  - Valido general: {resultado['validacion'].get('valido_general')}")

# Guardar resultado completo en JSON para inspección
with open('test_correccion_resultado.json', 'w', encoding='utf-8') as f:
    # Convertir resultado a formato serializable
    resultado_serializable = {
        'exito': resultado['exito'],
        'fase_actual': resultado['fase_actual'],
        'validacion_inicial': resultado.get('validacion_inicial'),
        'correccion': resultado.get('correccion'),
        'validacion': resultado.get('validacion'),
    }
    json.dump(resultado_serializable, f, indent=2, ensure_ascii=False)

print("\nResultado guardado en: test_correccion_resultado.json")
