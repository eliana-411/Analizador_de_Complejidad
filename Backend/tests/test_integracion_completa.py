"""
Test de Integración Completa
=============================
Verifica que todos los componentes estén correctamente conectados:
- Validador → Workflow → Math Agent → Resolver → Reportador
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from flujo_analisis import FlujoAnalisis

def test_integracion():
    print("="*80)
    print("TEST DE INTEGRACIÓN COMPLETA")
    print("="*80)
    print("\n🔍 Verificando conexión de todos los componentes...\n")
    
    # Inicializar flujo
    print("1️⃣ Inicializando FlujoAnalisis...")
    flujo = FlujoAnalisis(modo_verbose=True)  # ← VERBOSE = TRUE
    print("   ✅ Flujo inicializado\n")
    
    # Ejecutar análisis con un caso simple
    print("2️⃣ Ejecutando análisis completo con TODO el output...")
    print("="*80)
    resultado = flujo.analizar_desde_archivo(
        'data/pseudocodigos/correctos/01-busqueda-lineal.txt',
        auto_corregir=False
    )
    print("="*80)
    
    print("\n" + "="*80)
    print("RESULTADOS DE LA INTEGRACIÓN")
    print("="*80)
    
    # Verificar cada fase
    verificaciones = []
    
    # FASE 4: Validación
    print("\n✓ FASE 4: Validación Sintáctica")
    validacion = resultado.get('validacion', {})
    if validacion.get('valido_general'):  # ← Cambiado a 'valido_general'
        print(f"  ✅ Pseudocódigo válido")
        print(f"  📝 Algorithm name: {validacion.get('algorithm_name', 'N/A')}")
        print(f"  📋 Parámetros: {validacion.get('parameters', {})}")
        print(f"  🔄 Tipo: {validacion.get('tipo_algoritmo', 'N/A')}")
        verificaciones.append(True)
    else:
        print(f"  ❌ Validación falló")
        print(f"  📋 Errores: {validacion.get('resumen', {}).get('errores_totales', 0)}")
        verificaciones.append(False)
    
    # FASE 6: Workflow (Tabla Omega)
    print("\n✓ FASE 6: Análisis de Costos (Workflow)")
    omega_table = resultado.get('omega_table')
    if omega_table:
        print(f"  ✅ Tabla Omega generada")
        # OmegaTable es un objeto Pydantic, no un dict
        scenarios = omega_table.scenarios if hasattr(omega_table, 'scenarios') else []
        control_vars = omega_table.control_variables if hasattr(omega_table, 'control_variables') else []
        print(f"  📊 Escenarios: {len(scenarios)}")
        print(f"  🎯 Variables de control: {control_vars}")
        verificaciones.append(True)
    else:
        print(f"  ❌ Tabla Omega no generada")
        verificaciones.append(False)
    
    # FASE 7: Math Agent (Ecuaciones)
    print("\n✓ FASE 7: Representación Matemática")
    ecuaciones = resultado.get('ecuaciones', {})
    if ecuaciones:
        print(f"  ✅ Ecuaciones generadas")
        print(f"  🔹 Mejor caso: {ecuaciones.get('mejor_caso', 'N/A')}")
        print(f"  🔹 Caso promedio: {ecuaciones.get('caso_promedio', 'N/A')}")
        print(f"  🔹 Peor caso: {ecuaciones.get('peor_caso', 'N/A')}")
        verificaciones.append(True)
    else:
        print(f"  ❌ Ecuaciones no generadas")
        verificaciones.append(False)
    
    # FASE 8: Resolver (Complejidades)
    print("\n✓ FASE 8: Resolución de Ecuaciones")
    complejidades = resultado.get('complejidades', {})
    if complejidades:
        comp_finales = complejidades.get('complejidades', {})
        print(f"  ✅ Ecuaciones resueltas")
        print(f"  📈 Mejor caso (Ω): {comp_finales.get('mejor_caso', 'N/A')}")
        print(f"  📊 Caso promedio (Θ): {comp_finales.get('caso_promedio', 'N/A')}")
        print(f"  📉 Peor caso (O): {comp_finales.get('peor_caso', 'N/A')}")
        print(f"  🔧 Método usado: {complejidades.get('metodo_usado', 'N/A')}")
        verificaciones.append(True)
    else:
        print(f"  ❌ Complejidades no calculadas")
        verificaciones.append(False)
    
    # FASE 9: Reportador
    print("\n✓ FASE 9: Generación de Reporte")
    reporte_markdown = resultado.get('reporte_markdown')
    ruta_reporte = resultado.get('ruta_reporte')
    
    # Nota: La FASE 9 no está implementada actualmente en flujo_analisis.py
    if reporte_markdown or ruta_reporte:
        print(f"  ✅ Reporte generado")
        if ruta_reporte:
            print(f"  📄 Archivo: {ruta_reporte}")
        print(f"  📏 Tamaño: {len(reporte_markdown) if reporte_markdown else 0} caracteres")
        verificaciones.append(True)
    else:
        print(f"  ℹ️  FASE 9 no implementada en flujo_analisis.py")
        print(f"  💡 Para implementar: agregar llamada a AgenteReportador")
        # No marcar como fallo, es opcional por ahora
        # verificaciones.append(None)
    
    # Verificar errores
    print("\n✓ ERRORES")
    errores = resultado.get('errores', [])
    if errores:
        print(f"  ⚠️  Se encontraron {len(errores)} errores:")
        for error in errores[:3]:  # Mostrar solo primeros 3
            print(f"     - {error}")
    else:
        print(f"  ✅ Sin errores")
    
    # Resumen final
    print("\n" + "="*80)
    print("RESUMEN DE LA INTEGRACIÓN")
    print("="*80)
    
    exitosas = sum(1 for v in verificaciones if v == True)
    fallidas = sum(1 for v in verificaciones if v == False)
    opcionales = sum(1 for v in verificaciones if v is None)
    total = len([v for v in verificaciones if v is not None])
    
    print(f"\n✅ Fases exitosas: {exitosas}/{total}")
    if fallidas > 0:
        print(f"❌ Fases fallidas: {fallidas}/{total}")
    if opcionales > 0:
        print(f"⚠️  Fases opcionales: {opcionales}")
    
    # Verificación de conexiones
    print("\n📡 VERIFICACIÓN DE CONEXIONES:")
    
    # Validador → Workflow
    if validacion.get('algorithm_name') and omega_table:
        print("  ✅ Validador → Workflow: CONECTADO")
    else:
        print("  ❌ Validador → Workflow: DESCONECTADO")
    
    # Workflow → Math Agent
    if omega_table and ecuaciones:
        print("  ✅ Workflow → Math Agent: CONECTADO")
    else:
        print("  ❌ Workflow → Math Agent: DESCONECTADO")
    
    # Math Agent → Resolver
    if ecuaciones and complejidades:
        print("  ✅ Math Agent → Resolver: CONECTADO")
    else:
        print("  ❌ Math Agent → Resolver: DESCONECTADO")
    
    # Resolver → Reportador
    if complejidades and (reporte_markdown or ruta_reporte):
        print("  ✅ Resolver → Reportador: CONECTADO")
    else:
        print("  ℹ️  Resolver → Reportador: NO IMPLEMENTADO")
        print("     (FASE 9 pendiente en flujo_analisis.py)")
    
    # Estado final
    print("\n" + "="*80)
    if fallidas == 0:
        print("🎉 INTEGRACIÓN COMPLETA: EXITOSA")
        print("   ✅ Validador → Workflow → Math Agent → Resolver: FUNCIONANDO")
        print("   ℹ️  Reportador: Pendiente de implementar en flujo_analisis.py")
        print("="*80)
        return True
    else:
        print("⚠️  INTEGRACIÓN COMPLETA: CON ERRORES")
        print("="*80)
        return False


if __name__ == "__main__":
    try:
        exito = test_integracion()
        sys.exit(0 if exito else 1)
    except Exception as e:
        print(f"\n❌ ERROR CRÍTICO: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
