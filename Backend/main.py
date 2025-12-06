"""
MAIN - Ejecución Completa del Analizador de Complejidad
========================================================

Ejecuta el flujo completo mostrando TODOS los pasos, sin omitir nada.
Configurado para máxima verbosidad y detalle completo.

Uso:
    python main.py
    python main.py <archivo.txt>
"""

import sys
import logging
from pathlib import Path

from flujo_analisis import FlujoAnalisis


def configurar_logging_completo():
    """Configura logging para mostrar TODO sin filtros"""
    # Configurar logging root
    logging.basicConfig(
        level=logging.DEBUG,  # Nivel más bajo = TODO
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Asegurar que TODOS los loggers muestren TODO
    loggers = [
        'MathAgent',
        'LLMEquationGenerator',
        'BasicEquationGenerator',
        'WorkflowLogger',
        'AnalizadorLogger',
        'ResolverLogger'
    ]
    
    for logger_name in loggers:
        logger = logging.getLogger(logger_name)
        logger.setLevel(logging.DEBUG)
        logger.propagate = True


def mostrar_seccion(titulo: str, caracter: str = "=", ancho: int = 100):
    """Muestra una sección visualmente destacada"""
    print("\n" + caracter * ancho)
    print(f"{titulo:^{ancho}}")
    print(caracter * ancho + "\n")


def mostrar_resultado_completo(resultado: dict, mostrar_todo: bool = True):
    """
    Muestra TODOS los resultados del análisis sin omitir nada.
    
    Args:
        resultado: Dict del flujo completo
        mostrar_todo: Si True (default), muestra absolutamente todo
    """
    
    mostrar_seccion("📊 RESULTADOS FINALES DEL ANÁLISIS", "=", 100)
    
    # ==================== ESTADO GENERAL ====================
    print("🎯 ESTADO GENERAL")
    print("-" * 100)
    print(f"✓ Éxito: {resultado.get('exito', False)}")
    print(f"✓ Fase final: {resultado.get('fase_actual', 'N/A')}")
    print(f"✓ Errores: {len(resultado.get('errores', []))}")
    
    # ==================== PSEUDOCÓDIGO ====================
    mostrar_seccion("📝 PSEUDOCÓDIGO ANALIZADO", "-", 100)
    
    print("ORIGINAL:")
    print("─" * 100)
    print(resultado.get('pseudocodigo_original', 'N/A'))
    print("─" * 100)
    
    if resultado.get('pseudocodigo_validado') != resultado.get('pseudocodigo_original'):
        print("\nVALIDADO/CORREGIDO:")
        print("─" * 100)
        print(resultado.get('pseudocodigo_validado', 'N/A'))
        print("─" * 100)
    
    # ==================== CLASIFICACIÓN ====================
    if resultado.get('clasificacion'):
        mostrar_seccion("🔍 CLASIFICACIÓN ML", "-", 100)
        clasificacion = resultado['clasificacion']
        
        print(f"Categoría principal: {clasificacion.get('categoria_principal', 'N/A')}")
        print(f"Confianza: {clasificacion.get('confianza', 0):.2%}")
        
        print("\nTop predicciones:")
        for i, pred in enumerate(clasificacion.get('top_predicciones', []), 1):
            print(f"  {i}. {pred['categoria']}: {pred['probabilidad']:.2%}")
    
    # ==================== VALIDACIÓN ====================
    if resultado.get('validacion'):
        mostrar_seccion("✅ VALIDACIÓN SINTÁCTICA", "-", 100)
        validacion = resultado['validacion']
        
        print(f"Válido: {validacion.get('valido_general', False)}")
        print(f"Tipo de algoritmo: {validacion.get('tipo_algoritmo', 'N/A')}")
        print(f"Nombre del algoritmo: {validacion.get('algorithm_name', 'N/A')}")
        print(f"Parámetros: {validacion.get('parameters', {})}")
        
        print("\nRESUMEN DE CAPAS:")
        resumen = validacion.get('resumen', {})
        print(f"  • Errores totales: {resumen.get('errores_totales', 0)}")
        print(f"  • Capas validadas: {resumen.get('capas_validadas', 0)}")
        print(f"  • Capas con errores: {resumen.get('capas_con_errores', 0)}")
        
        # TODOS los detalles de cada capa
        print("\nDETALLE POR CAPA:")
        for capa_nombre, capa_datos in validacion.get('capas', {}).items():
            print(f"\n  📌 {capa_nombre}:")
            print(f"     Válida: {capa_datos.get('valido', False)}")
            print(f"     Errores: {len(capa_datos.get('errores', []))}")
            
            if capa_datos.get('errores'):
                print("     Detalles:")
                for error in capa_datos['errores']:
                    print(f"       ❌ {error}")
            
            if capa_datos.get('advertencias'):
                print("     Advertencias:")
                for adv in capa_datos['advertencias']:
                    print(f"       ⚠  {adv}")
    
    # ==================== CORRECCIÓN ====================
    if resultado.get('correccion'):
        mostrar_seccion("🔧 CORRECCIÓN AUTOMÁTICA", "-", 100)
        correccion = resultado['correccion']
        
        print(f"Corregido: {correccion.get('corregido', False)}")
        
        if correccion.get('explicacion'):
            print(f"\nExplicación:")
            print(f"  {correccion['explicacion']}")
        
        if correccion.get('cambios'):
            print("\nCambios realizados:")
            for cambio in correccion['cambios']:
                print(f"  • {cambio}")
    
    # ==================== FLOWCHART ====================
    if resultado.get('flowchart'):
        mostrar_seccion("📊 FLOWCHART (Mermaid)", "-", 100)
        print(resultado['flowchart'])
    
    # ==================== TABLA OMEGA ====================
    if resultado.get('omega_table'):
        mostrar_seccion("📋 TABLA OMEGA - ANÁLISIS DE COSTOS", "-", 100)
        omega = resultado['omega_table']
        
        # Variables de control
        if hasattr(omega, 'control_variables'):
            print(f"Variables de control: {', '.join(omega.control_variables)}")
        
        # Metadata
        if hasattr(omega, 'metadata'):
            print(f"\nMetadata:")
            for key, value in omega.metadata.items():
                print(f"  • {key}: {value}")
        
        # Escenarios
        print(f"\nESCENARIOS ANALIZADOS:")
        print("-" * 100)
        
        if hasattr(omega, 'scenarios'):
            for i, scenario in enumerate(omega.scenarios, 1):
                print(f"\n🔹 Escenario {i}:")
                print(f"   ID: {scenario.id}")
                print(f"   Condición: {scenario.condition}")
                print(f"   Estado: {scenario.state}")
                print(f"   Costo T(S): {scenario.cost_T}")
                print(f"   Probabilidad P(S): {scenario.probability_P}")
                
                if hasattr(scenario, 'line_costs') and scenario.line_costs:
                    print(f"\n   Costos por línea:")
                    for line_cost in scenario.line_costs:
                        print(f"     • Línea {line_cost.get('line', '?')}: {line_cost.get('cost', '?')} (freq: {line_cost.get('frequency', '?')})")
    
    # ==================== ECUACIONES ====================
    if resultado.get('ecuaciones'):
        mostrar_seccion("🔢 ECUACIONES DE RECURRENCIA", "-", 100)
        ecuaciones = resultado['ecuaciones']
        
        print(f"Mejor caso:    {ecuaciones.get('mejor_caso', 'N/A')}")
        print(f"Caso promedio: {ecuaciones.get('caso_promedio', 'N/A')}")
        print(f"Peor caso:     {ecuaciones.get('peor_caso', 'N/A')}")
        
        # Detalles adicionales si existen
        if resultado.get('ecuaciones_detalle'):
            detalle = resultado['ecuaciones_detalle']
            
            if detalle.get('reasoning'):
                print(f"\nRazonamiento:")
                print(f"  {detalle['reasoning']}")
            
            if detalle.get('assumptions'):
                print(f"\nAsunciones:")
                for assumption in detalle['assumptions']:
                    print(f"  • {assumption}")
    
    # ==================== COMPLEJIDADES ====================
    if resultado.get('complejidades'):
        mostrar_seccion("🎯 COMPLEJIDADES CALCULADAS", "-", 100)
        complejidades = resultado['complejidades']
        
        # Complejidades finales
        comp = complejidades.get('complejidades', {})
        print("NOTACIONES ASINTÓTICAS:")
        print("-" * 100)
        print(f"✓ Mejor caso (Ω):    {comp.get('mejor_caso', 'N/A')}")
        print(f"✓ Caso promedio (Θ): {comp.get('caso_promedio', 'N/A')}")
        print(f"✓ Peor caso (O):     {comp.get('peor_caso', 'N/A')}")
        
        print(f"\nMétodo usado: {complejidades.get('metodo_usado', 'N/A')}")
        
        if complejidades.get('observacion'):
            print(f"\nObservación: {complejidades['observacion']}")
        
        # PASOS DETALLADOS de resolución
        if complejidades.get('pasos_resolucion'):
            print("\n" + "=" * 100)
            print("PASOS DE RESOLUCIÓN DETALLADOS:")
            print("=" * 100)
            
            for caso, detalle in complejidades['pasos_resolucion'].items():
                print(f"\n📌 {caso.replace('_', ' ').upper()}:")
                print("-" * 100)
                
                print(f"Ecuación: {detalle.get('ecuacion', 'N/A')}")
                print(f"Método: {detalle.get('metodo', 'N/A')}")
                print(f"Solución: {detalle.get('solucion', 'N/A')}")
                
                if detalle.get('explicacion'):
                    print(f"\nExplicación:")
                    print(f"  {detalle['explicacion']}")
                
                if detalle.get('pasos'):
                    print(f"\nPasos:")
                    for i, paso in enumerate(detalle['pasos'], 1):
                        print(f"  {i}. {paso}")
                
                if detalle.get('diagrama_mermaid'):
                    print(f"\nDiagrama:")
                    print(detalle['diagrama_mermaid'])
    
    # ==================== VALIDACIÓN DE COMPLEJIDADES ====================
    if resultado.get('validacion_complejidades'):
        mostrar_seccion("🔍 VALIDACIÓN CON LLM", "-", 100)
        validacion_llm = resultado['validacion_complejidades']
        
        print(f"Concordancia: {'✅ SÍ' if validacion_llm.get('concordancia') else '❌ NO'}")
        print(f"Confianza: {validacion_llm.get('confianza', 0):.0%}")
        
        print("\nCOMPARACIÓN SISTEMA vs LLM:")
        print("-" * 100)
        print(f"{'Caso':<20} {'Sistema':<25} {'LLM':<25} {'Estado'}")
        print("-" * 100)
        
        sistema = validacion_llm.get('complejidades_sistema', {})
        llm = validacion_llm.get('complejidades_llm', {})
        
        for caso in ['mejor_caso', 'caso_promedio', 'peor_caso']:
            nombre = caso.replace('_', ' ').title()
            val_sistema = sistema.get(caso, 'N/A')
            val_llm = llm.get(caso, 'N/A')
            estado = "✅" if val_sistema == val_llm else "⚠"
            
            print(f"{nombre:<20} {val_sistema:<25} {val_llm:<25} {estado}")
        
        if validacion_llm.get('analisis_divergencias'):
            print("\nDIVERGENCIAS DETECTADAS:")
            print("-" * 100)
            for div in validacion_llm['analisis_divergencias']:
                print(f"  • {div['caso']}:")
                print(f"    - Sistema: {div['sistema']}")
                print(f"    - LLM: {div['llm']}")
                print(f"    - Tipo: {div['tipo']}")
                print(f"    - Severidad: {div['severidad']}")
        
        print(f"\nRecomendación: {validacion_llm.get('recomendacion', 'N/A')}")
        
        if validacion_llm.get('complejidades_llm', {}).get('justificacion'):
            print(f"\nJustificación del LLM:")
            print(f"  {validacion_llm['complejidades_llm']['justificacion']}")
    
    # ==================== ERRORES ====================
    if resultado.get('errores'):
        mostrar_seccion("❌ ERRORES ENCONTRADOS", "-", 100)
        for i, error in enumerate(resultado['errores'], 1):
            print(f"{i}. {error}")
    
    # ==================== RESUMEN FINAL ====================
    mostrar_seccion("📊 RESUMEN EJECUTIVO", "=", 100)
    
    print(f"✓ Análisis: {'EXITOSO ✅' if resultado.get('exito') else 'CON ERRORES ❌'}")
    
    if resultado.get('validacion'):
        print(f"✓ Algoritmo: {resultado['validacion'].get('algorithm_name', 'N/A')}")
        print(f"✓ Tipo: {resultado['validacion'].get('tipo_algoritmo', 'N/A')}")
    
    if resultado.get('complejidades'):
        comp = resultado['complejidades']['complejidades']
        print(f"✓ Complejidad final: {comp.get('peor_caso', 'N/A')}")
    
    if resultado.get('validacion_complejidades'):
        conc = resultado['validacion_complejidades']['concordancia']
        print(f"✓ Validación LLM: {'Concordante ✅' if conc else 'Divergente ⚠'}")
    
    print("\n" + "=" * 100 + "\n")


def main():
    """Función principal"""
    
    # Banner
    print("\n" + "=" * 100)
    print("🚀 ANALIZADOR DE COMPLEJIDAD ALGORÍTMICA - EJECUCIÓN COMPLETA".center(100))
    print("=" * 100 + "\n")
    
    # Configurar logging completo
    print("📋 Configurando logging completo (nivel DEBUG)...")
    configurar_logging_completo()
    print("✅ Logging configurado\n")
    
    # Determinar archivo a analizar
    if len(sys.argv) > 1:
        archivo = sys.argv[1]
    else:
        # Archivo por defecto
        archivo = "data/pseudocodigos/correctos/08-torres-hanoi.txt"
    
    archivo_path = Path(archivo)
    
    if not archivo_path.exists():
        print(f"❌ Error: Archivo no encontrado: {archivo}")
        print(f"\nUso: python main.py [archivo.txt]")
        print(f"Ejemplo: python main.py data/pseudocodigos/correctos/02-busqueda-binaria.txt")
        return 1
    
    print(f"📄 Archivo a analizar: {archivo}")
    print(f"📏 Tamaño: {archivo_path.stat().st_size} bytes")
    print()
    
    # Inicializar flujo
    mostrar_seccion("🔧 INICIALIZANDO SISTEMA", "=", 100)
    print("Cargando componentes...")
    
    flujo = FlujoAnalisis(modo_verbose=True)  # Verbose = True para TODO
    
    print("\n✅ Sistema inicializado correctamente")
    
    # Ejecutar análisis completo
    mostrar_seccion("⚙  EJECUTANDO ANÁLISIS COMPLETO", "=", 100)
    print("MOSTRANDO TODOS LOS PASOS SIN OMITIR NADA...\n")
    print("=" * 100 + "\n")
    
    try:
        resultado = flujo.analizar_desde_archivo(
            str(archivo_path),
            auto_corregir=True
        )
        
        # Mostrar TODOS los resultados
        mostrar_resultado_completo(resultado, mostrar_todo=True)
        
        # Estado de salida
        return 0 if resultado.get('exito') else 1
        
    except Exception as e:
        mostrar_seccion("❌ ERROR CRÍTICO", "=", 100)
        print(f"Tipo: {type(e)._name_}")
        print(f"Mensaje: {str(e)}")
        
        import traceback
        print("\nTraceback completo:")
        print("-" * 100)
        traceback.print_exc()
        print("-" * 100)
        
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)