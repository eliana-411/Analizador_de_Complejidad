"""
Test del flujo completo con algoritmo ITERATIVO
Prueba la nueva funcionalidad de prompts específicos para iterativos
con constantes simbólicas (c1, c2, c3) y probabilidades resueltas
"""

import asyncio
import json
from pathlib import Path
from core.analizador.agents.workflow import get_workflow
from core.analizador.models.scenario_state import ScenarioState


# ============================================================================
# ALGORITMO DE PRUEBA: BÚSQUEDA LINEAL (Iterativo Simple)
# ============================================================================

CODIGO_BUSQUEDA_LINEAL = """maximoArray(int arr[], int n)
begin
    max 🡨 arr[0]
    for i 🡨 1 to n-1 do
    begin
        if (arr[i] > max) then
        begin
            max 🡨 arr[i]
        end
    end
    return max
end
"""


# ============================================================================
# ESTADO INICIAL: Simula lo que llega al workflow
# ============================================================================

def crear_estado_inicial() -> ScenarioState:
    """
    Crea el estado inicial que entraría al workflow.
    Simula un estado mínimo después del parsing.
    """
    
    # Crear estado inicial simplificado
    estado = ScenarioState(
        pseudocode=CODIGO_BUSQUEDA_LINEAL,
        algorithm_name="busqueda_lineal",
        is_iterative=True,  # ← CLAVE: Marca como iterativo
        parameters={"arr": "array", "objetivo": "int"},
        lines=CODIGO_BUSQUEDA_LINEAL.split('\n'),
        raw_scenarios=[],
        errors=[]
    )
    
    return estado


# ============================================================================
# EJECUTAR PRUEBA
# ============================================================================

async def ejecutar_prueba():
    """
    Ejecuta el flujo completo y muestra los resultados
    """
    
    print("=" * 80)
    print("🧪 TEST: FLUJO CON ALGORITMO ITERATIVO")
    print("=" * 80)
    print()
    
    # 1. Crear estado inicial
    print("📋 Paso 1: Creando estado inicial...")
    estado_inicial = crear_estado_inicial()
    print(f"   ✓ Algoritmo: {estado_inicial.algorithm_name}")
    print(f"   ✓ Tipo: {'ITERATIVO' if estado_inicial.is_iterative else 'RECURSIVO'}")
    print(f"   ✓ Líneas: {len(estado_inicial.lines)}")
    print()
    
    # 2. Crear y ejecutar flujo
    print("🔄 Paso 2: Ejecutando workflow...")
    print()
    
    try:
        flujo = get_workflow()
        resultado = await flujo.ainvoke(estado_inicial)
        
        print()
        print("=" * 80)
        print("✅ PRUEBA COMPLETADA - RESULTADOS")
        print("=" * 80)
        print()
        
        # 3. Mostrar análisis LLM de cada caso
        print("📊 ANÁLISIS LLM ALMACENADO:")
        print("-" * 80)
        
        # El resultado es un dict, no ScenarioState
        llm_analysis = resultado.get('llm_analysis', {})
        
        if not llm_analysis:
            print("   ⚠️  No hay análisis LLM (posiblemente por error de créditos)")
            print("   Nota: El flujo intentó usar los prompts nuevos pero falló la llamada a la API")
        
        for caso in ["best_case", "worst_case", "average_case"]:
            if caso in llm_analysis:
                analisis = llm_analysis[caso]
                print(f"\n🔹 {caso.upper().replace('_', ' ')}:")
                
                # Detectar formato
                is_new_format = "input_condition" in analisis
                print(f"   Formato: {'NUEVO (iterativo)' if is_new_format else 'ANTIGUO (recursivo)'}")
                
                if is_new_format:
                    print(f"   • input_condition: {analisis.get('input_condition', 'N/A')[:100]}")
                    print(f"   • T_of_S: {analisis.get('T_of_S', 'N/A')}")
                    print(f"   • P_of_S: {analisis.get('P_of_S', 'N/A')}")
                    
                    # Validar constantes simbólicas
                    line_costs = analisis.get('line_costs', [])
                    if line_costs:
                        print(f"   • Líneas analizadas: {len(line_costs)}")
                        constantes = set()
                        for line in line_costs:
                            c_op = line.get('C_op', '')
                            if c_op.startswith('c') and c_op[1:].isdigit():
                                constantes.add(c_op)
                        print(f"   • Constantes simbólicas encontradas: {', '.join(sorted(constantes))}")
                else:
                    print(f"   • input_description: {analisis.get('input_description', 'N/A')[:100]}")
                    print(f"   • total_cost_T: {analisis.get('total_cost_T', 'N/A')}")
                    print(f"   • probability_P: {analisis.get('probability_P', 'N/A')}")
        
        print()
        print("-" * 80)
        
        # 4. Mostrar escenarios generados
        print()
        print("🎯 ESCENARIOS GENERADOS:")
        print("-" * 80)
        raw_scenarios = resultado.get('raw_scenarios', [])
        for idx, escenario in enumerate(raw_scenarios, 1):
            print(f"\n{idx}. {escenario.get('id', 'N/A')} - {escenario.get('semantic_id', 'N/A')}")
            print(f"   Estado: {escenario.get('state', 'N/A')}")
            print(f"   Condición: {escenario.get('condition', 'N/A')[:80]}")
            print(f"   Costo T(S): {escenario.get('cost_T', 'N/A')}")
            print(f"   Probabilidad P(S): {escenario.get('probability_P', 'N/A')}")
        
        print()
        print("-" * 80)
        
        # 5. Mostrar tabla Omega si existe
        omega_table = resultado.get('omega_table')
        if omega_table:
            print()
            print("📋 TABLA OMEGA GENERADA:")
            print("-" * 80)
            print(f"   Algoritmo: {omega_table.algorithm_name}")
            print(f"   Total de escenarios: {len(omega_table.scenarios)}")
            print(f"   Variables de control: {', '.join(omega_table.control_variables) if omega_table.control_variables else 'N/A'}")
            
            for escenario in omega_table.scenarios:
                print(f"\n   • {escenario.id}")
                print(f"     Condición: {escenario.condition[:60]}")
                print(f"     Estado: {escenario.state}")
                print(f"     T(S): {escenario.cost_T}")
                print(f"     P(S): {escenario.probability_P}")
            
            # Mostrar metadata si existe
            if omega_table.metadata:
                print(f"\n   📊 Metadata disponible: {', '.join(omega_table.metadata.keys())}")
            
            print("-" * 80)
        
        # 6. Verificar errores
        errors = resultado.get('errors', [])
        if errors:
            print()
            print("⚠️  ERRORES ENCONTRADOS:")
            print("-" * 80)
            for error in errors:
                print(f"   • {error}")
        else:
            print()
            print("✅ No se encontraron errores")
        
        print()
        print("=" * 80)
        
        # 7. Guardar resultado completo
        import os
        output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_resultado_iterativo.json")
        with open(output_path, 'w', encoding='utf-8') as f:
            # Convertir OmegaTable a dict para serialización
            resultado_serializable = dict(resultado)
            
            # Convertir omega_table (Pydantic model) a dict
            if 'omega_table' in resultado_serializable and resultado_serializable['omega_table'] is not None:
                resultado_serializable['omega_table'] = resultado_serializable['omega_table'].model_dump()
            
            json.dump(resultado_serializable, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Resultado completo guardado en: {output_path}")
        print()
        
    except Exception as e:
        print()
        print("=" * 80)
        print("❌ ERROR EN LA PRUEBA")
        print("=" * 80)
        print(f"\n{type(e).__name__}: {str(e)}")
        print()
        import traceback
        traceback.print_exc()


# ============================================================================
# FUNCIÓN DE VALIDACIÓN
# ============================================================================

def validar_resultado(resultado: dict) -> dict:
    """
    Valida que el resultado cumpla con las expectativas para un iterativo
    """
    validaciones = {
        "formato_nuevo_detectado": False,
        "constantes_simbolicas_usadas": False,
        "probabilidades_resueltas": False,
        "tres_casos_analizados": False,
        "tabla_omega_generada": False
    }
    
    llm_analysis = resultado.get('llm_analysis', {})
    
    # Verificar formato nuevo en al menos un caso
    for caso in ["best_case", "worst_case", "average_case"]:
        if caso in llm_analysis:
            if "input_condition" in llm_analysis[caso]:
                validaciones["formato_nuevo_detectado"] = True
                break
    
    # Verificar constantes simbólicas
    for caso in ["best_case", "worst_case"]:
        if caso in llm_analysis:
            line_costs = llm_analysis[caso].get('line_costs', [])
            for line in line_costs:
                c_op = line.get('C_op', '')
                if c_op.startswith('c') and c_op[1:].isdigit():
                    validaciones["constantes_simbolicas_usadas"] = True
                    break
    
    # Verificar probabilidades sin 'q'
    for caso in llm_analysis.values():
        prob = caso.get('P_of_S', caso.get('probability_P', ''))
        if 'q' not in str(prob).lower() and prob != '':
            validaciones["probabilidades_resueltas"] = True
            break
    
    # Verificar tres casos analizados
    validaciones["tres_casos_analizados"] = all(
        caso in llm_analysis
        for caso in ["best_case", "worst_case", "average_case"]
    )
    
    # Verificar tabla omega
    if resultado.get('omega_table'):
        validaciones["tabla_omega_generada"] = True
    
    return validaciones


# ============================================================================
# MAIN
# ============================================================================

if __name__ == "__main__":
    asyncio.run(ejecutar_prueba())
