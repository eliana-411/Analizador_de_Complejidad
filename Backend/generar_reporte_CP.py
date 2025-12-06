"""
Generar reporte del Algoritmo CP en formato Markdown
"""

import sys
import os

# Agregar Backend al path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tests.flujo_analisis import FlujoAnalisis
from agentes.agenteReportador import AgenteReportador

# Pseudocódigo del algoritmo CP
pseudocodigo = """Algoritmo CP (int A[n])
begin
  contador <- 0
  for i <- 1 to n do
     Si el numero del arreglo es par, incrementar un contador en 1
  end
  print(contador)
end
"""

def main():
    print("Generando reporte del Algoritmo CP...")

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
        nombre_archivo = "reporte_algoritmo_CP.md"

        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            f.write(reporte_completo.get('markdown', ''))

        print(f"✓ Reporte generado exitosamente: {nombre_archivo}")
        print(f"✓ Exito del analisis: {resultado['exito']}")
        print(f"✓ Fase: {resultado['fase_actual']}")

        # Mostrar resumen
        if resultado.get('clasificacion'):
            clasif = resultado['clasificacion']
            print(f"✓ Clasificacion ML: {clasif['categoria_principal']} ({clasif['confianza']*100:.1f}%)")

        if resultado.get('validacion'):
            val = resultado['validacion']
            print(f"✓ Validacion: {'Valido' if val['valido_general'] else 'Con errores'}")
            if val['resumen']['errores_totales'] > 0:
                print(f"  - Errores encontrados: {val['resumen']['errores_totales']}")

        print(f"\nArchivo guardado en: {os.path.abspath(nombre_archivo)}")

        return True

    except Exception as e:
        print(f"✗ Error generando reporte: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    exito = main()
    sys.exit(0 if exito else 1)
