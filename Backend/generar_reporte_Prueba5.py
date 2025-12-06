"""
Generar reporte del Algoritmo Prueba5 en formato Markdown
"""

import sys
import os

# Agregar Backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.flujo_analisis import FlujoAnalisis
from agentes.agenteReportador import AgenteReportador

# Pseudocódigo del algoritmo Prueba5
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

def main():
    print("Generando reporte del Algoritmo Prueba5...")

    try:
        # Crear flujo con verbose desactivado
        flujo = FlujoAnalisis(modo_verbose=False)

        # Ejecutar análisis completo
        resultado = flujo.analizar(
            entrada=pseudocodigo,
            tipo_entrada="pseudocodigo",
            auto_corregir=True
        )

        # Generar reporte con AgenteReportador
        reportador = AgenteReportador()
        reporte_completo = reportador.generar_reporte_completo(resultado)

        # Guardar reporte en archivo
        nombre_archivo = "reporte_algoritmo_Prueba5.md"

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(reporte_completo.get('markdown', ''))

        print("OK - Reporte generado exitosamente:", nombre_archivo)
        print("OK - Exito del analisis:", resultado['exito'])
        print("OK - Fase:", resultado['fase_actual'])

        # Mostrar resumen
        if resultado.get('clasificacion'):
            clasif = resultado['clasificacion']
            print(f"OK - Clasificacion ML: {clasif['categoria_principal']} ({clasif['confianza']*100:.1f}%)")

        if resultado.get('validacion'):
            val = resultado['validacion']
            print(f"OK - Validacion: {'Valido' if val['valido_general'] else 'Con errores'}")
            if val['resumen']['errores_totales'] > 0:
                print(f"  - Errores encontrados: {val['resumen']['errores_totales']}")

        if resultado.get('complejidades'):
            comp = resultado['complejidades'].get('complejidades', {})
            if comp:
                print("\nCOMPLEJIDADES:")
                print(f"  - Mejor caso: {comp.get('mejor_caso', 'N/A')}")
                print(f"  - Caso promedio: {comp.get('caso_promedio', 'N/A')}")
                print(f"  - Peor caso: {comp.get('peor_caso', 'N/A')}")

        print(f"\nArchivo guardado en: {os.path.abspath(nombre_archivo)}")

        return True

    except Exception as e:
        print(f"ERROR - Error generando reporte: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
