"""
TEST FASE 1: GENERACIÓN DE TABLA OMEGA
=======================================

Este script prueba ÚNICAMENTE el Agente de Análisis de Costos (Fase 1).

Entrada: Pseudocódigo
Salida: Tabla Omega completa

Uso:
    python test_fase1_tabla_omega.py
    
    O edita la variable PSEUDOCODIGO_INPUT para probar otro algoritmo.
"""

import json
import sys
from pathlib import Path
from datetime import datetime

# Configurar path
backend_path = Path(__file__).parent
sys.path.insert(0, str(backend_path))

from core.analizador.agents.workflow import get_workflow
from core.analizador.models.scenario_state import ScenarioState


# ============================================================================
# CONFIGURACIÓN: PEGA AQUÍ TU PSEUDOCÓDIGO
# ============================================================================

PSEUDOCODIGO_INPUT = """
    fibonacci(int n)
begin
    if (n ≤ 1) then
    begin
        return n
    end
    else
    begin
        return CALL fibonacci(n - 1) + CALL fibonacci(n - 2)
    end
end
"""

# ============================================================================


def print_separator(char: str = "=", width: int = 80):
    """Imprime separador"""
    print(char * width)


def detectar_metadata_algoritmo(pseudocodigo: str) -> tuple:
    """
    Detecta automáticamente metadata del algoritmo desde el pseudocódigo.
    
    Returns:
        tuple: (algorithm_name, is_iterative)
    """
    lineas = pseudocodigo.strip().split('\n')
    
    # Detectar nombre del algoritmo (primera línea con paréntesis)
    algorithm_name = "algoritmo"
    for linea in lineas:
        linea_limpia = linea.strip()
        if '(' in linea_limpia and ')' in linea_limpia:
            # Extraer nombre antes del paréntesis
            algorithm_name = linea_limpia.split('(')[0].strip()
            break
    
    # Detectar si es iterativo o recursivo
    pseudocodigo_lower = pseudocodigo.lower()
    
    # Buscar palabras clave de loops (iterativo)
    tiene_loops = any(keyword in pseudocodigo_lower for keyword in 
                     ['for ', 'while ', 'repeat ', 'do '])
    
    # Buscar llamadas recursivas (función se llama a sí misma)
    tiene_recursion = f'call {algorithm_name.lower()}(' in pseudocodigo_lower
    
    # Si tiene recursión, es recursivo; si solo tiene loops, es iterativo
    # Si no tiene ninguno, asumir iterativo por defecto
    is_iterative = tiene_loops and not tiene_recursion
    
    return algorithm_name, is_iterative


def main():
    """Ejecuta prueba de Fase 1: Generación de Tabla Omega"""
    
    print_separator("=")
    print("TEST FASE 1: GENERACIÓN DE TABLA OMEGA".center(80))
    print_separator("=")
    print(f"Fecha: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    
    # ========================================================================
    # PASO 1: CARGAR PSEUDOCÓDIGO
    # ========================================================================
    print("📄 PASO 1: Cargando pseudocódigo...")
    print("-" * 80)
    
    # Usar el pseudocódigo directamente desde la variable
    pseudocodigo = PSEUDOCODIGO_INPUT.strip()
    print("✅ Pseudocódigo cargado desde variable PSEUDOCODIGO_INPUT")
    
    print("\nPseudocódigo a analizar:")
    print("-" * 80)
    print(pseudocodigo)
    print("-" * 80)
    print(f"Total: {len(pseudocodigo.splitlines())} líneas\n")
    
    # ========================================================================
    # PASO 1.5: DETECTAR METADATA DEL ALGORITMO
    # ========================================================================
    print("🔍 Detectando metadata del algoritmo...")
    print("-" * 80)
    
    algorithm_name, is_iterative = detectar_metadata_algoritmo(pseudocodigo)
    
    print(f"✅ Nombre detectado: {algorithm_name}")
    print(f"✅ Tipo detectado: {'Iterativo' if is_iterative else 'Recursivo'}")
    print()
    
    # ========================================================================
    # PASO 2: EJECUTAR WORKFLOW (FASE 1)
    # ========================================================================
    print("🔄 PASO 2: Ejecutando Workflow de Análisis de Costos...")
    print("-" * 80)
    print(f"Algoritmo: {algorithm_name}")
    print(f"Tipo: {'Iterativo' if is_iterative else 'Recursivo'}")
    print()
    
    print("Este workflow ejecuta:")
    print("  1️⃣  parse_lines_node → Extrae líneas")
    print("  2️⃣  llm_analyze_best_case_node → Analiza MEJOR caso")
    print("  3️⃣  llm_analyze_worst_case_node → Analiza PEOR caso")
    print("  4️⃣  llm_analyze_average_case_node → Analiza CASO PROMEDIO")
    print("  5️⃣  build_omega_table_node → Construye Tabla Omega")
    print()
    print_separator("=")
    print("⏳ EJECUTANDO WORKFLOW...")
    print_separator("=")
    print()
    
    try:
        # Crear estado inicial con metadata detectada
        estado_inicial = ScenarioState(
            pseudocode=pseudocodigo,
            algorithm_name=algorithm_name,
            is_iterative=is_iterative
        )
        
        # Obtener workflow y ejecutar
        workflow = get_workflow()
        resultado = workflow.invoke(estado_inicial)
        
        # Extraer tabla omega
        tabla_omega = resultado.get("omega_table")
        
        if not tabla_omega:
            print("❌ ERROR: No se generó la Tabla Omega")
            return
        
        print()
        print_separator("=")
        print("✅ WORKFLOW COMPLETADO EXITOSAMENTE")
        print_separator("=")
        print()
        
    except Exception as e:
        print(f"\n❌ ERROR durante la ejecución del workflow:")
        print(f"   {e}\n")
        import traceback
        traceback.print_exc()
        return
    
    # ========================================================================
    # PASO 3: MOSTRAR TABLA OMEGA
    # ========================================================================
    print("📊 PASO 3: Tabla Omega Generada")
    print_separator("=")
    
    print("\n🔍 INFORMACIÓN GENERAL:")
    print("-" * 80)
    print(f"  Tipo objeto: {type(tabla_omega)}")
    print(f"  Algoritmo: {getattr(tabla_omega, 'algorithm_name', 'N/A')}")
    
    # Obtener tipo de algoritmo desde metadata
    tipo_algoritmo = "N/A"
    if hasattr(tabla_omega, 'metadata') and tabla_omega.metadata:
        tipo_algoritmo = tabla_omega.metadata.get('algorithm_type', 'N/A')
        if tipo_algoritmo == "iterative":
            tipo_algoritmo = "Iterativo"
        elif tipo_algoritmo == "recursive":
            tipo_algoritmo = "Recursivo"
    
    print(f"  Tipo: {tipo_algoritmo}")
    
    # Verificar si tiene escenarios
    if hasattr(tabla_omega, 'scenarios'):
        escenarios = tabla_omega.scenarios
        print(f"  Número de escenarios: {len(escenarios)}")
    else:
        escenarios = []
        print(f"  Número de escenarios: 0 (no tiene atributo 'scenarios')")
    
    print()
    
    # Intentar convertir a diccionario
    tabla_dict = None
    if hasattr(tabla_omega, 'to_dict'):
        try:
            tabla_dict = tabla_omega.to_dict()
        except Exception as e:
            print(f"⚠️  Error al convertir con to_dict(): {e}")
    
    if hasattr(tabla_omega, 'model_dump'):
        try:
            tabla_dict = tabla_omega.model_dump()
        except Exception as e:
            print(f"⚠️  Error al convertir con model_dump(): {e}")
    
    if hasattr(tabla_omega, 'dict'):
        try:
            tabla_dict = tabla_omega.dict()
        except Exception as e:
            print(f"⚠️  Error al convertir con dict(): {e}")
    
    # Si aún no se pudo, mostrar los atributos directamente
    if not tabla_dict:
        print("⚠️  No se pudo convertir a diccionario, mostrando atributos:")
        print("-" * 80)
        
        # Mostrar todos los atributos del objeto
        for attr in dir(tabla_omega):
            if not attr.startswith('_'):
                try:
                    valor = getattr(tabla_omega, attr)
                    if not callable(valor):
                        print(f"\n{attr}:")
                        if isinstance(valor, list) and len(valor) > 0:
                            print(f"  [{len(valor)} elementos]")
                            for i, item in enumerate(valor[:3], 1):  # Mostrar primeros 3
                                print(f"  {i}. {item}")
                            if len(valor) > 3:
                                print(f"  ... y {len(valor) - 3} más")
                        else:
                            print(f"  {valor}")
                except Exception as e:
                    print(f"  Error al obtener {attr}: {e}")
    
    print()
    
    # Mostrar escenarios detalladamente
    if escenarios:
        print("\n📋 ESCENARIOS DETALLADOS:")
        print_separator("=")
        
        for i, escenario in enumerate(escenarios, 1):
            print(f"\n🔹 ESCENARIO {i}")
            print("-" * 80)
            
            # Obtener atributos del escenario
            for attr in ['id_escenario', 'nombre_escenario', 'tipo_caso', 'entrada_que_causa_caso',
                        'costo_total', 'probabilidad', 'recurrencia']:
                if hasattr(escenario, attr):
                    valor = getattr(escenario, attr)
                    print(f"  {attr}: {valor}")
            
            # Mostrar análisis de líneas si existe
            if hasattr(escenario, 'analisis_lineas'):
                lineas = getattr(escenario, 'analisis_lineas')
                if lineas:
                    print(f"\n  Análisis por línea: ({len(lineas)} líneas)")
                    for j, linea in enumerate(lineas[:5], 1):  # Mostrar primeras 5
                        if hasattr(linea, 'numero_linea') and hasattr(linea, 'costo'):
                            print(f"    Línea {getattr(linea, 'numero_linea')}: "
                                  f"costo={getattr(linea, 'costo')}, "
                                  f"frecuencia={getattr(linea, 'frecuencia', 'N/A')}")
                    if len(lineas) > 5:
                        print(f"    ... y {len(lineas) - 5} líneas más")
        
        print()
        print_separator("=")
    
    # Intentar mostrar como JSON si se pudo convertir
    if tabla_dict:
        print("\n📋 TABLA OMEGA COMPLETA (JSON):")
        print_separator("=")
        print(json.dumps(tabla_dict, indent=2, ensure_ascii=False))
        print_separator("=")
        
        # Guardar en archivo JSON para Fase 2
        results_dir = backend_path / "resultados_pruebas"
        results_dir.mkdir(exist_ok=True)
        
        #timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        nombre_algoritmo_safe = algorithm_name.replace(" ", "_").lower()
        json_filename = f"fase1_tabla_{nombre_algoritmo_safe}.json"
        json_path = results_dir / json_filename
        
        # Guardar el resultado completo del workflow tal cual viene del analizador
        # El resultado (ScenarioState) ya tiene toda la estructura correcta
        if hasattr(resultado, 'model_dump'):
            output_data = resultado.model_dump()
        elif hasattr(resultado, 'dict'):
            output_data = resultado.dict()
        else:
            # Fallback: convertir manualmente
            output_data = {
                "pseudocode": resultado.pseudocode if hasattr(resultado, 'pseudocode') else pseudocodigo,
                "algorithm_name": resultado.algorithm_name if hasattr(resultado, 'algorithm_name') else algorithm_name,
                "is_iterative": resultado.is_iterative if hasattr(resultado, 'is_iterative') else is_iterative,
                "parameters": resultado.parameters if hasattr(resultado, 'parameters') else {},
                "lines": resultado.lines if hasattr(resultado, 'lines') else [],
                "loops": resultado.loops if hasattr(resultado, 'loops') else [],
                "recursive_calls": resultado.recursive_calls if hasattr(resultado, 'recursive_calls') else [],
                "is_recursive": resultado.is_recursive if hasattr(resultado, 'is_recursive') else False,
                "control_variables": resultado.control_variables if hasattr(resultado, 'control_variables') else [],
                "raw_scenarios": [
                    s.model_dump() if hasattr(s, 'model_dump') else s.dict() if hasattr(s, 'dict') else s
                    for s in (resultado.raw_scenarios if hasattr(resultado, 'raw_scenarios') else [])
                ],
                "llm_analysis": resultado.llm_analysis if hasattr(resultado, 'llm_analysis') else {},
                "omega_table": tabla_dict,
                "errors": resultado.errors if hasattr(resultado, 'errors') else [],
                "warnings": resultado.warnings if hasattr(resultado, 'warnings') else []
            }
        
        with open(json_path, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 JSON guardado en: {json_path.name}")
    
    print()
    
    # ========================================================================
    # PASO 4: RESUMEN
    # ========================================================================
    print_separator("=")
    print("🎉 RESUMEN DE LA PRUEBA")
    print_separator("=")
    
    escenarios = getattr(tabla_omega, 'scenarios', [])
    algorithm_name = getattr(tabla_omega, 'algorithm_name', 'N/A')
    
    # Obtener tipo de algoritmo desde metadata
    tipo_algoritmo = "N/A"
    if hasattr(tabla_omega, 'metadata') and tabla_omega.metadata:
        tipo_algoritmo = tabla_omega.metadata.get('algorithm_type', 'N/A')
        if tipo_algoritmo == "iterative":
            tipo_algoritmo = "Iterativo"
        elif tipo_algoritmo == "recursive":
            tipo_algoritmo = "Recursivo"
    
    print(f"✅ Tabla Omega generada correctamente")
    print(f"✅ Algoritmo detectado: {algorithm_name}")
    print(f"✅ Tipo detectado: {tipo_algoritmo}")
    print(f"✅ Escenarios analizados: {len(escenarios)}")
    
    if escenarios:
        print("\nEscenarios detectados:")
        for i, escenario in enumerate(escenarios, 1):
            nombre = getattr(escenario, 'case_type', 'N/A')
            entrada = getattr(escenario, 'input_causing_case', 'N/A')
            print(f"  {i}. {nombre}: {entrada}")
    
    print()
    print_separator("=")
    print("PRUEBA COMPLETADA EXITOSAMENTE".center(80))
    print_separator("=")
    print()
    
    print("💡 SIGUIENTE PASO:")
    print("   Ejecuta: python test_fase2_ecuaciones.py")
    print("   (automáticamente cargará el JSON más reciente)")
    print()


if __name__ == "__main__":
    main()
