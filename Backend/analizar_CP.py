"""
Análisis del Algoritmo CP - Contador de Pares
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
    print("=" * 80)
    print("ANALISIS DEL ALGORITMO CP (Contador de Pares)")
    print("=" * 80)
    print()

    print("PSEUDOCODIGO A ANALIZAR:")
    print("-" * 80)
    print(pseudocodigo)
    print("-" * 80)
    print()

    try:
        # Crear flujo con verbose desactivado para limpieza
        flujo = FlujoAnalisis(modo_verbose=False)

        print("EJECUTANDO ANALISIS COMPLETO...")
        print()

        # Ejecutar análisis completo
        resultado = flujo.analizar(
            entrada=pseudocodigo,
            tipo_entrada="pseudocodigo",
            auto_corregir=True
        )

        print("\n" + "=" * 80)
        print("RESULTADOS DEL ANALISIS")
        print("=" * 80)
        print()

        # Mostrar resultados clave
        print(f"Exito: {resultado['exito']}")
        print(f"Fase actual: {resultado['fase_actual']}")
        print()

        # Validación
        if resultado.get('validacion'):
            val = resultado['validacion']
            print("VALIDACION:")
            print(f"  - Valido: {val['valido_general']}")
            print(f"  - Tipo: {val.get('tipo_algoritmo', 'N/A')}")
            print(f"  - Errores: {val['resumen']['errores_totales']}")

            if val['resumen']['errores_totales'] > 0:
                print("\n  Errores encontrados:")
                for capa, datos in val['capas'].items():
                    if datos['errores']:
                        print(f"\n  {capa}:")
                        for error in datos['errores']:
                            print(f"    - {error}")
            print()

        # Clasificación ML
        if resultado.get('clasificacion'):
            clasif = resultado['clasificacion']
            print("CLASIFICACION ML:")
            print(f"  - Categoria: {clasif['categoria_principal']}")
            print(f"  - Confianza: {clasif['confianza']*100:.1f}%")
            if clasif.get('top_predicciones'):
                print("  - Top 3:")
                for pred in clasif['top_predicciones'][:3]:
                    print(f"    {pred['categoria']}: {pred['probabilidad']*100:.1f}%")
            print()

        # Tabla Omega
        if resultado.get('omega_table'):
            print("TABLA OMEGA:")
            omega = resultado['omega_table']
            print(f"  - Escenarios: {len(omega.scenarios)}")
            print(f"  - Variables de control: {omega.control_variables}")
            print()

        # Ecuaciones
        if resultado.get('ecuaciones'):
            print("ECUACIONES GENERADAS:")
            ecuaciones = resultado['ecuaciones']
            print(f"  - Mejor caso: {ecuaciones.get('mejor_caso', 'N/A')}")
            print(f"  - Caso promedio: {ecuaciones.get('caso_promedio', 'N/A')}")
            print(f"  - Peor caso: {ecuaciones.get('peor_caso', 'N/A')}")
            print()

        # Complejidades
        if resultado.get('complejidades'):
            print("COMPLEJIDADES RESUELTAS:")
            comp = resultado['complejidades'].get('complejidades', {})
            print(f"  - Mejor caso (Omega): {comp.get('mejor_caso', 'N/A')}")
            print(f"  - Caso promedio (Theta): {comp.get('caso_promedio', 'N/A')}")
            print(f"  - Peor caso (O): {comp.get('peor_caso', 'N/A')}")

            metodo = resultado['complejidades'].get('metodo_usado')
            if metodo:
                print(f"  - Metodo usado: {metodo}")
            print()

        # Flowchart
        if resultado.get('flowchart'):
            print("FLOWCHART GENERADO:")
            print("-" * 80)
            print(resultado['flowchart'])
            print("-" * 80)
            print()

        # Generar reporte completo
        print("\n" + "=" * 80)
        print("GENERANDO REPORTE COMPLETO...")
        print("=" * 80)
        print()

        reportador = AgenteReportador()
        reporte_completo = reportador.generar_reporte_completo(resultado)

        if reporte_completo.get('markdown'):
            print("REPORTE EN MARKDOWN:")
            print("=" * 80)
            print(reporte_completo['markdown'])
            print("=" * 80)
            print()

        # Errores
        if resultado.get('errores'):
            print("ERRORES ENCONTRADOS:")
            for error in resultado['errores']:
                print(f"  - {error}")
            print()

        print("=" * 80)
        print("ANALISIS COMPLETADO")
        print("=" * 80)

        return resultado

    except Exception as e:
        print(f"\nERROR EN ANALISIS: {str(e)}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    resultado = main()

    # Código de salida
    if resultado and resultado['exito']:
        sys.exit(0)
    else:
        sys.exit(1)
