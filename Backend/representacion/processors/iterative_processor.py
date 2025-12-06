"""
Procesador de Algoritmos Iterativos.

Maneja la generación de ecuaciones para algoritmos iterativos,
diferenciando mejor caso, caso promedio y peor caso.
"""

from typing import Dict, List
from core.analizador.models.omega_table import OmegaTable, ScenarioEntry
from representacion.utils.cost_comparator import complejidad_numerica
from representacion.utils.equation_formatter import simplificar_con_constantes
from representacion.processors.esperanza_calculator import calculate_expected_value


def process_iterative(omega_table: OmegaTable, llm_analysis: Dict = None) -> Dict:
    """
    Procesa un algoritmo iterativo para generar sus ecuaciones.
    
    Estrategia:
    1. Identificar mejor caso (mínimo cost_T)
    2. Identificar peor caso (máximo cost_T)
    3. Calcular caso promedio (E[T] si hay múltiples escenarios)
    4. Simplificar usando constantes (K, C) en lugar de T(n)
    5. Si llm_analysis está presente, usar insights para mejorar simplificación
    
    Args:
        omega_table: Tabla Omega con escenarios del algoritmo iterativo
        llm_analysis: Análisis opcional del LLM con términos dominantes y sugerencias
    
    Returns:
        Dict con:
            - mejor_caso: str (ecuación simplificada)
            - caso_promedio: str
            - peor_caso: str
            - ecuaciones_iguales: bool
            - tipo_analisis: str
            - derivacion_caso_promedio: str (opcional)
            - pasos_generacion: List[str]
    """
    scenarios = omega_table.scenarios
    pasos = []
    
    # Agregar información de análisis LLM si está disponible
    if llm_analysis:
        pasos.append("📊 Usando análisis LLM para guiar simplificación")
        pasos.append("")
    pasos.append("📊 Algoritmo ITERATIVO detectado")
    pasos.append(f"   Total de escenarios: {len(scenarios)}")
    
    # CASO 1: Un solo escenario (ecuación única para todos los casos)
    if len(scenarios) == 1:
        pasos.append("   ► Un solo escenario: ecuación única para todos los casos")
        
        scenario = scenarios[0]
        cost = scenario.cost_T
        ecuacion_simplificada = simplificar_con_constantes(cost, es_caso_promedio=False, tipo_caso='mejor')
        
        pasos.append(f"   ► Costo: {cost}")
        pasos.append(f"   ► Simplificado: {ecuacion_simplificada}")
        
        return {
            'mejor_caso': ecuacion_simplificada,
            'caso_promedio': ecuacion_simplificada,
            'peor_caso': ecuacion_simplificada,
            'ecuaciones_iguales': True,
            'tipo_analisis': 'iterativo_casos',
            'pasos_generacion': pasos
        }
    
    # CASO 2: Múltiples escenarios
    pasos.append(f"   ► Múltiples escenarios detectados")
    pasos.append("")
    
    # Si hay más de 3 escenarios, usar procesador especializado
    if len(scenarios) > 3:
        pasos.append("   ► Más de 3 escenarios: usando procesador multi-escenario")
        return process_multiple_scenarios(omega_table, llm_analysis)
    
    # Encontrar mejor caso (mínimo costo)
    pasos.append("🔍 Identificando MEJOR CASO (Ω - lower bound):")
    mejor_scenario = min(scenarios, key=lambda s: complejidad_numerica(s.cost_T))
    mejor_caso_raw = mejor_scenario.cost_T
    
    # Usar sugerencia del LLM si está disponible
    if llm_analysis and 'mejor_caso' in llm_analysis:
        llm_suggestion = llm_analysis['mejor_caso'].get('ecuacion_sugerida')
        if llm_suggestion:
            mejor_caso = llm_suggestion
            pasos.append(f"   ► Escenario: {mejor_scenario.id}")
            pasos.append(f"   ► Condición: {mejor_scenario.condition}")
            pasos.append(f"   ► Costo: {mejor_caso_raw}")
            pasos.append(f"   ► 🤖 LLM sugiere: {mejor_caso}")
            pasos.append(f"      └─ {llm_analysis['mejor_caso'].get('explicacion', '')}")
        else:
            mejor_caso = simplificar_con_constantes(mejor_caso_raw, es_caso_promedio=False, tipo_caso='mejor')
            pasos.append(f"   ► Escenario: {mejor_scenario.id}")
            pasos.append(f"   ► Condición: {mejor_scenario.condition}")
            pasos.append(f"   ► Costo: {mejor_caso_raw}")
            pasos.append(f"   ► Simplificado: {mejor_caso}")
    else:
        mejor_caso = simplificar_con_constantes(mejor_caso_raw, es_caso_promedio=False, tipo_caso='mejor')
        pasos.append(f"   ► Escenario: {mejor_scenario.id}")
        pasos.append(f"   ► Condición: {mejor_scenario.condition}")
        pasos.append(f"   ► Costo: {mejor_caso_raw}")
        pasos.append(f"   ► Simplificado: {mejor_caso}")
    pasos.append("")
    
    # Encontrar peor caso (máximo costo)
    pasos.append("🔍 Identificando PEOR CASO (O - upper bound):")
    peor_scenario = max(scenarios, key=lambda s: complejidad_numerica(s.cost_T))
    peor_caso_raw = peor_scenario.cost_T
    
    # Usar sugerencia del LLM si está disponible
    if llm_analysis and 'peor_caso' in llm_analysis:
        llm_suggestion = llm_analysis['peor_caso'].get('ecuacion_sugerida')
        if llm_suggestion:
            peor_caso = llm_suggestion
            pasos.append(f"   ► Escenario: {peor_scenario.id}")
            pasos.append(f"   ► Condición: {peor_scenario.condition}")
            pasos.append(f"   ► Costo: {peor_caso_raw}")
            pasos.append(f"   ► 🤖 LLM sugiere: {peor_caso}")
            pasos.append(f"      └─ {llm_analysis['peor_caso'].get('explicacion', '')}")
        else:
            # Peor caso no es caso promedio, no usar flag
            peor_caso = simplificar_con_constantes(peor_caso_raw, es_caso_promedio=False, tipo_caso='peor')
            pasos.append(f"   ► Escenario: {peor_scenario.id}")
            pasos.append(f"   ► Condición: {peor_scenario.condition}")
            pasos.append(f"   ► Costo: {peor_caso_raw}")
            pasos.append(f"   ► Simplificado: {peor_caso}")
    else:
        # Peor caso no es caso promedio, no usar flag
        peor_caso = simplificar_con_constantes(peor_caso_raw, es_caso_promedio=False, tipo_caso='peor')
        pasos.append(f"   ► Escenario: {peor_scenario.id}")
        pasos.append(f"   ► Condición: {peor_scenario.condition}")
        pasos.append(f"   ► Costo: {peor_caso_raw}")
        pasos.append(f"   ► Simplificado: {peor_caso}")
    pasos.append("")
    
    # Calcular caso promedio (Esperanza Matemática o escenario intermedio)
    pasos.append("📊 Calculando CASO PROMEDIO (Θ - expected value):")
    
    # Verificar si todos los escenarios tienen probabilidad 1 (son casos independientes, no probabilísticos)
    todas_prob_uno = all(s.probability_P == "1" for s in scenarios)
    
    if todas_prob_uno and len(scenarios) == 3:
        # Caso especial: 3 escenarios con P=1 representan mejor, promedio y peor directamente
        pasos.append("   ► Escenarios representan casos directos (mejor, promedio, peor)")
        
        # Tomar el escenario intermedio (el que no es ni el mejor ni el peor)
        escenarios_intermedios = [s for s in scenarios if s != mejor_scenario and s != peor_scenario]
        
        if escenarios_intermedios:
            scenario_promedio = escenarios_intermedios[0]
            caso_promedio_raw = scenario_promedio.cost_T
            
            pasos.append(f"   ► Escenario: {scenario_promedio.id}")
            pasos.append(f"   ► Condición: {scenario_promedio.condition}")
            pasos.append(f"   ► Costo: {caso_promedio_raw}")
            
            # Usar sugerencia del LLM si está disponible
            if llm_analysis and 'caso_promedio' in llm_analysis:
                llm_suggestion = llm_analysis['caso_promedio'].get('ecuacion_sugerida')
                if llm_suggestion:
                    caso_promedio = llm_suggestion
                    pasos.append(f"   ► 🤖 LLM sugiere: {caso_promedio}")
                    pasos.append(f"      └─ {llm_analysis['caso_promedio'].get('explicacion', '')}")
                else:
                    # Detectar si tiene n/2 en el costo
                    es_caso_promedio = '/2' in caso_promedio_raw or '0.5' in caso_promedio_raw
                    caso_promedio = simplificar_con_constantes(caso_promedio_raw, es_caso_promedio=es_caso_promedio, tipo_caso='promedio')
                    pasos.append(f"   ► Simplificado: {caso_promedio}")
            else:
                # Detectar si tiene n/2 en el costo
                es_caso_promedio = '/2' in caso_promedio_raw or '0.5' in caso_promedio_raw
                caso_promedio = simplificar_con_constantes(caso_promedio_raw, es_caso_promedio=es_caso_promedio, tipo_caso='promedio')
                pasos.append(f"   ► Simplificado: {caso_promedio}")
            
            derivacion = f"Caso promedio tomado directamente del escenario {scenario_promedio.id}"
        else:
            # Fallback: calcular esperanza
            caso_promedio_raw, derivacion = calculate_expected_value(scenarios)
            es_caso_promedio = '/2' in caso_promedio_raw or '0.5' in caso_promedio_raw
            caso_promedio = simplificar_con_constantes(caso_promedio_raw, es_caso_promedio=es_caso_promedio, tipo_caso='promedio')
            pasos.append(f"   ► E[T] calculado: {caso_promedio_raw}")
            pasos.append(f"   ► Simplificado: {caso_promedio}")
    else:
        # Calcular esperanza matemática normalmente
        pasos.append("   E[T] = Σ T(S) · P(S)")
        
        caso_promedio_raw, derivacion = calculate_expected_value(scenarios)
        
        # Usar sugerencia del LLM si está disponible
        if llm_analysis and 'caso_promedio' in llm_analysis:
            llm_suggestion = llm_analysis['caso_promedio'].get('ecuacion_sugerida')
            if llm_suggestion:
                caso_promedio = llm_suggestion
                pasos.append(f"   ► E[T] calculado: {caso_promedio_raw}")
                pasos.append(f"   ► 🤖 LLM sugiere: {caso_promedio}")
                pasos.append(f"      └─ {llm_analysis['caso_promedio'].get('explicacion', '')}")
            else:
                # Detectar si es caso promedio (n/2) para usar formato correcto
                es_caso_promedio = '/2' in caso_promedio_raw or '0.5' in caso_promedio_raw
                caso_promedio = simplificar_con_constantes(caso_promedio_raw, es_caso_promedio=es_caso_promedio, tipo_caso='promedio')
                pasos.append(f"   ► E[T] calculado: {caso_promedio_raw}")
                pasos.append(f"   ► Simplificado: {caso_promedio}")
        else:
            # Detectar si es caso promedio (n/2) para usar formato correcto
            es_caso_promedio = '/2' in caso_promedio_raw or '0.5' in caso_promedio_raw
            caso_promedio = simplificar_con_constantes(caso_promedio_raw, es_caso_promedio=es_caso_promedio, tipo_caso='promedio')
            pasos.append(f"   ► E[T] calculado: {caso_promedio_raw}")
            pasos.append(f"   ► Simplificado: {caso_promedio}")
    pasos.append("")
    
    # Verificar si las 3 son iguales
    ecuaciones_iguales = (mejor_caso == caso_promedio == peor_caso)
    
    if ecuaciones_iguales:
        pasos.append("⚠️ Las 3 ecuaciones son idénticas (complejidad constante en todos los casos)")
    else:
        pasos.append("✅ Ecuaciones diferenciadas por caso")
    
    return {
        'mejor_caso': mejor_caso,
        'caso_promedio': caso_promedio,
        'peor_caso': peor_caso,
        'ecuaciones_iguales': ecuaciones_iguales,
        'tipo_analisis': 'iterativo_casos',
        'derivacion_caso_promedio': derivacion,
        'pasos_generacion': pasos
    }


def identificar_mejor_caso(scenarios: List[ScenarioEntry]) -> ScenarioEntry:
    """
    Identifica el escenario con menor costo (mejor caso).
    
    Args:
        scenarios: Lista de escenarios
    
    Returns:
        ScenarioEntry con el menor costo
    """
    return min(scenarios, key=lambda s: complejidad_numerica(s.cost_T))


def identificar_peor_caso(scenarios: List[ScenarioEntry]) -> ScenarioEntry:
    """
    Identifica el escenario con mayor costo (peor caso).
    
    Args:
        scenarios: Lista de escenarios
    
    Returns:
        ScenarioEntry con el mayor costo
    """
    return max(scenarios, key=lambda s: complejidad_numerica(s.cost_T))


def son_ecuaciones_iguales(mejor: str, promedio: str, peor: str) -> bool:
    """
    Verifica si las tres ecuaciones son iguales.
    
    Args:
        mejor: Ecuación del mejor caso
        promedio: Ecuación del caso promedio
        peor: Ecuación del peor caso
    
    Returns:
        bool: True si las 3 son idénticas
    """
    # Normalizar espacios
    mejor = mejor.replace(' ', '')
    promedio = promedio.replace(' ', '')
    peor = peor.replace(' ', '')
    
    return mejor == promedio == peor


def process_multiple_scenarios(omega_table: OmegaTable, llm_analysis: Dict = None) -> Dict:
    """
    Procesa algoritmos con MÁS DE 3 escenarios.
    
    Estrategia para n > 3 escenarios:
    1. Ordenar por complejidad
    2. Mejor caso = mínimo
    3. Peor caso = máximo
    4. Caso promedio = mediana o esperanza matemática si hay probabilidades
    
    Args:
        omega_table: Tabla Omega con múltiples escenarios
        llm_analysis: Análisis del LLM (opcional)
    
    Returns:
        Dict con ecuaciones y pasos de generación
    """
    scenarios = omega_table.scenarios
    pasos = []
    
    pasos.append(f"📊 Algoritmo ITERATIVO con {len(scenarios)} escenarios")
    pasos.append("   ► Estrategia: Análisis de múltiples escenarios")
    pasos.append("")
    
    # Ordenar por complejidad
    scenarios_ordenados = sorted(scenarios, key=lambda s: complejidad_numerica(s.cost_T))
    
    # MEJOR CASO: Mínimo
    mejor_scenario = scenarios_ordenados[0]
    mejor_caso = simplificar_con_constantes(mejor_scenario.cost_T, es_caso_promedio=False, tipo_caso='mejor')
    
    pasos.append("🔍 MEJOR CASO (Ω):")
    pasos.append(f"   ► Escenario: {mejor_scenario.id}")
    pasos.append(f"   ► Costo: {mejor_scenario.cost_T}")
    pasos.append(f"   ► Simplificado: {mejor_caso}")
    pasos.append("")
    
    # PEOR CASO: Máximo
    peor_scenario = scenarios_ordenados[-1]
    peor_caso = simplificar_con_constantes(peor_scenario.cost_T, es_caso_promedio=False, tipo_caso='peor')
    
    pasos.append("🔍 PEOR CASO (O):")
    pasos.append(f"   ► Escenario: {peor_scenario.id}")
    pasos.append(f"   ► Costo: {peor_scenario.cost_T}")
    pasos.append(f"   ► Simplificado: {peor_caso}")
    pasos.append("")
    
    # CASO PROMEDIO: Mediana o esperanza
    pasos.append("📊 CASO PROMEDIO (Θ):")
    
    # Verificar si hay probabilidades reales
    tiene_probabilidades = any(s.probability_P not in ["1", "1.0", ""] for s in scenarios)
    
    if tiene_probabilidades:
        # Calcular esperanza matemática
        pasos.append("   ► Usando esperanza matemática (E[T])")
        caso_promedio, derivacion = calculate_expected_value(omega_table.scenarios)
        pasos.append(f"   ► E[T] = {caso_promedio}")
    else:
        # Usar mediana (escenario del medio)
        idx_medio = len(scenarios_ordenados) // 2
        scenario_medio = scenarios_ordenados[idx_medio]
        
        pasos.append(f"   ► Usando escenario mediano: {scenario_medio.id}")
        pasos.append(f"   ► Costo: {scenario_medio.cost_T}")
        
        es_caso_promedio = '/2' in scenario_medio.cost_T or '0.5' in scenario_medio.cost_T
        caso_promedio = simplificar_con_constantes(
            scenario_medio.cost_T,
            es_caso_promedio=es_caso_promedio,
            tipo_caso='promedio'
        )
        pasos.append(f"   ► Simplificado: {caso_promedio}")
        derivacion = None
    
    pasos.append("")
    
    return {
        'mejor_caso': mejor_caso,
        'caso_promedio': caso_promedio,
        'peor_caso': peor_caso,
        'ecuaciones_iguales': son_ecuaciones_iguales(mejor_caso, caso_promedio, peor_caso),
        'tipo_analisis': 'iterativo_multiple',
        'derivacion_caso_promedio': derivacion or '',
        'pasos_generacion': pasos
    }
