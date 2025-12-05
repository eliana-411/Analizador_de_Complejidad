"""
Debug del caso 13 - potencia recursiva
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent))

from flujo_analisis import FlujoAnalisis

flujo = FlujoAnalisis(modo_verbose=True)

print("="*80)
print("PROBANDO: 13-potencia-recursiva.txt")
print("="*80)

archivo = "C:/Users/egriv/OneDrive/Documentos/Analizador de Complejidad/Backend/data/pseudocodigos/correctos/13-potencia-recursiva.txt"

resultado = flujo.analizar_desde_archivo(archivo, auto_corregir=True)

print("\n" + "="*80)
print("RESULTADO:")
print("="*80)
print(f"Exito: {resultado['exito']}")
print(f"Errores: {resultado['errores']}")

if resultado.get('validacion'):
    print(f"\nValidacion:")
    print(f"  Valido: {resultado['validacion']['valido_general']}")
    print(f"  Errores totales: {resultado['validacion']['resumen']['errores_totales']}")
    
    if not resultado['validacion']['valido_general']:
        print("\n  Detalles de errores:")
        for capa, datos in resultado['validacion']['capas'].items():
            if datos['errores']:
                print(f"\n  {capa}:")
                for error in datos['errores']:
                    print(f"    - {error}")

print("\n" + "="*80)
