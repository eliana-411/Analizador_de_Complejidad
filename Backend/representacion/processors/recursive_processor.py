"""
Procesador de Algoritmos Recursivos.

Maneja la generación de relaciones de recurrencia para algoritmos recursivos.
"""

from typing import Dict, Optional
from core.analizador.models.omega_table import OmegaTable
from core.analizador.models.recursion_info import RecursionInfo


def process_recursive(omega_table: OmegaTable, llm_analysis: Dict = None) -> Dict:
    """
    Procesa un algoritmo recursivo para generar su relación de recurrencia.
    
    Estrategia:
    - Generar relación de recurrencia desde RecursionInfo
    - Detectar casos especiales (Fibonacci, múltiple recursión)
    - Diferenciar mejor/promedio/peor si hay variantes
    - Formato: "T(n) = aT(n/b) + f(n)" o "T(n) = T(n-1) + T(n-2) + c"
    - Si llm_analysis está presente, usar insights para mejorar generación
    
    Args:
        omega_table: Tabla Omega con metadata de recursión
        llm_analysis: Análisis opcional del LLM con términos dominantes y sugerencias
    
    Returns:
        Dict con:
            - mejor_caso: str
            - caso_promedio: str
            - peor_caso: str
            - ecuaciones_iguales: bool
            - tipo_analisis: str
            - pasos_generacion: List[str]
    """
    metadata = omega_table.metadata
    scenarios = omega_table.scenarios
    pasos = []
    
    pasos.append("🔄 Algoritmo RECURSIVO detectado")
    
    # Agregar información de análisis LLM si está disponible
    if llm_analysis:
        pasos.append("📊 Usando análisis LLM para guiar generación de recurrencia")
        pasos.append("")
    
    # Verificar si hay múltiples escenarios (implica casos diferenciados)
    tiene_multiples_casos = len(scenarios) > 1
    
    if tiene_multiples_casos:
        pasos.append(f"   ► {len(scenarios)} escenarios detectados")
        pasos.append("   ► Generando ecuaciones diferenciadas por caso")
        pasos.append("")
        
        # Procesar cada caso individualmente
        return procesar_recursivo_multiples_casos(omega_table, llm_analysis, pasos)
    
    # Caso único: misma ecuación para todos los casos
    pasos.append("   ► Caso único: misma recurrencia para mejor/promedio/peor")
    
    # Intentar obtener RecursionInfo del metadata
    recursion_info = metadata.get('recursion_info')
    
    if recursion_info:
        pasos.append("   ► RecursionInfo encontrado")
        ecuacion = generar_recurrencia_desde_info(recursion_info, pasos)
    else:
        pasos.append("   ⚠️ No hay RecursionInfo en metadata")
        pasos.append("   ► Infiriendo recurrencia de escenarios...")
        ecuacion = inferir_recurrencia_de_scenarios(scenarios, pasos)
    
    # Usar sugerencia del LLM si está disponible
    if llm_analysis and 'mejor_caso' in llm_analysis:
        llm_sugerencia = llm_analysis['mejor_caso'].get('ecuacion_sugerida')
        if llm_sugerencia:
            pasos.append("")
            pasos.append(f"🤖 LLM sugiere: {llm_sugerencia}")
            ecuacion = llm_sugerencia
    
    pasos.append("")
    pasos.append(f"📐 Relación de recurrencia generada:")
    pasos.append(f"   {ecuacion}")
    pasos.append("")
    pasos.append("ℹ️ Para este algoritmo recursivo:")
    pasos.append("   Mejor caso = Caso promedio = Peor caso")
    
    # Para recursivos típicos, las 3 son iguales
    return {
        'mejor_caso': ecuacion,
        'caso_promedio': ecuacion,
        'peor_caso': ecuacion,
        'ecuaciones_iguales': True,
        'tipo_analisis': 'recursivo_uniforme',
        'pasos_generacion': pasos
    }


def procesar_recursivo_multiples_casos(omega_table: OmegaTable, llm_analysis: Dict, pasos: list) -> Dict:
    """
    Procesa algoritmos recursivos con múltiples casos diferenciados.
    
    Ejemplo: QuickSort (mejor caso: O(n log n), peor caso: O(n²))
    
    Args:
        omega_table: Tabla Omega
        llm_analysis: Análisis LLM (opcional)
        pasos: Lista de pasos
    
    Returns:
        Dict con ecuaciones por caso
    """
    from representacion.utils.cost_comparator import complejidad_numerica
    
    scenarios = omega_table.scenarios
    metadata = omega_table.metadata
    
    # Ordenar escenarios por complejidad
    scenarios_ordenados = sorted(scenarios, key=lambda s: complejidad_numerica(s.cost_T))
    
    # MEJOR CASO
    mejor_scenario = scenarios_ordenados[0]
    pasos.append("🔍 MEJOR CASO (Ω):")
    pasos.append(f"   ► Escenario: {mejor_scenario.id}")
    pasos.append(f"   ► Condición: {mejor_scenario.condition}")
    
    # Generar recurrencia para mejor caso
    recursion_info_mejor = metadata.get('recursion_info', {})
    if isinstance(recursion_info_mejor, dict):
        num_calls_mejor = recursion_info_mejor.get('num_calls_mejor', recursion_info_mejor.get('num_calls', 1))
        pattern_mejor = recursion_info_mejor.get('call_pattern_mejor', recursion_info_mejor.get('call_pattern', ['n-1']))
    else:
        num_calls_mejor = recursion_info_mejor.num_calls
        pattern_mejor = recursion_info_mejor.call_pattern
    
    mejor_caso = construir_recurrencia(num_calls_mejor, pattern_mejor, mejor_scenario.cost_T)
    
    if llm_analysis and 'mejor_caso' in llm_analysis:
        llm_sug = llm_analysis['mejor_caso'].get('ecuacion_sugerida')
        if llm_sug:
            mejor_caso = llm_sug
            pasos.append(f"   ► 🤖 LLM sugiere: {mejor_caso}")
        else:
            pasos.append(f"   ► Recurrencia: {mejor_caso}")
    else:
        pasos.append(f"   ► Recurrencia: {mejor_caso}")
    pasos.append("")
    
    # PEOR CASO
    peor_scenario = scenarios_ordenados[-1]
    pasos.append("🔍 PEOR CASO (O):")
    pasos.append(f"   ► Escenario: {peor_scenario.id}")
    pasos.append(f"   ► Condición: {peor_scenario.condition}")
    
    # Generar recurrencia para peor caso
    if isinstance(recursion_info_mejor, dict):
        num_calls_peor = recursion_info_mejor.get('num_calls_peor', num_calls_mejor)
        pattern_peor = recursion_info_mejor.get('call_pattern_peor', pattern_mejor)
    else:
        num_calls_peor = num_calls_mejor
        pattern_peor = pattern_mejor
    
    peor_caso = construir_recurrencia(num_calls_peor, pattern_peor, peor_scenario.cost_T)
    
    if llm_analysis and 'peor_caso' in llm_analysis:
        llm_sug = llm_analysis['peor_caso'].get('ecuacion_sugerida')
        if llm_sug:
            peor_caso = llm_sug
            pasos.append(f"   ► 🤖 LLM sugiere: {peor_caso}")
        else:
            pasos.append(f"   ► Recurrencia: {peor_caso}")
    else:
        pasos.append(f"   ► Recurrencia: {peor_caso}")
    pasos.append("")
    
    # CASO PROMEDIO
    if len(scenarios) >= 3:
        promedio_scenario = scenarios_ordenados[len(scenarios) // 2]
    else:
        promedio_scenario = mejor_scenario
    
    pasos.append("📊 CASO PROMEDIO (Θ):")
    pasos.append(f"   ► Escenario: {promedio_scenario.id}")
    
    caso_promedio = construir_recurrencia(num_calls_mejor, pattern_mejor, promedio_scenario.cost_T)
    
    if llm_analysis and 'caso_promedio' in llm_analysis:
        llm_sug = llm_analysis['caso_promedio'].get('ecuacion_sugerida')
        if llm_sug:
            caso_promedio = llm_sug
            pasos.append(f"   ► 🤖 LLM sugiere: {caso_promedio}")
        else:
            pasos.append(f"   ► Recurrencia: {caso_promedio}")
    else:
        pasos.append(f"   ► Recurrencia: {caso_promedio}")
    pasos.append("")
    
    return {
        'mejor_caso': mejor_caso,
        'caso_promedio': caso_promedio,
        'peor_caso': peor_caso,
        'ecuaciones_iguales': (mejor_caso == caso_promedio == peor_caso),
        'tipo_analisis': 'recursivo_diferenciado',
        'pasos_generacion': pasos
    }


def construir_recurrencia(num_calls: int, call_pattern: list, cost_T: str) -> str:
    """
    Construye la relación de recurrencia a partir de parámetros.
    
    Maneja casos especiales:
    - Fibonacci: T(n) = T(n-1) + T(n-2) + c
    - Hanoi: T(n) = 2T(n-1) + c
    - Divide y conquista: T(n) = aT(n/b) + f(n)
    
    Args:
        num_calls: Número de llamadas recursivas
        call_pattern: Patrón de transformación
        cost_T: Costo original (para inferir f(n))
    
    Returns:
        str: Recurrencia construida
    """
    # CASO ESPECIAL: Fibonacci (T(n-1) + T(n-2))
    if num_calls == 2 and len(call_pattern) == 2:
        if 'n-1' in call_pattern and 'n-2' in call_pattern:
            return "T(n) = T(n-1) + T(n-2) + c"
    
    # CASO: Múltiples llamadas con mismo patrón
    if len(set(call_pattern)) == 1:
        termino = f"{num_calls}T({call_pattern[0]})" if num_calls > 1 else f"T({call_pattern[0]})"
    else:
        # Llamadas diferentes (ej: T(n/3) + T(2n/3))
        terminos = [f"T({p})" for p in call_pattern]
        termino = " + ".join(terminos)
    
    # Inferir f(n) del cost_T
    cost_lower = cost_T.lower()
    if 'n**2' in cost_lower or 'n²' in cost_lower:
        f_n = "c*n**2"
    elif 'n*' in cost_lower or '*n' in cost_lower:
        f_n = "c*n"
    elif 'log' in cost_lower:
        f_n = "c*log(n)"
    else:
        f_n = "c"
    
    return f"T(n) = {termino} + {f_n}"



def generar_recurrencia_desde_info(recursion_info, pasos: list) -> str:
    """
    Genera string de relación de recurrencia desde RecursionInfo.
    
    Formatos soportados:
    - T(n) = T(n-c) + f(n)      (decrementación)
    - T(n) = aT(n/b) + f(n)     (divide y conquista)
    - T(n) = T(...) + T(...) + f(n)  (múltiples llamadas)
    
    Args:
        recursion_info: Dict o RecursionInfo con información de la estructura recursiva
        pasos: Lista para agregar pasos de generación
    
    Returns:
        str: Relación de recurrencia
    
    Examples:
        >>> info = {'num_calls': 1, 'call_pattern': ['n-1'], ...}
        >>> generar_recurrencia_desde_info(info, [])
        'T(n) = T(n-1) + c'
        
        >>> info = {'num_calls': 2, 'call_pattern': ['n/2', 'n/2'], ...}
        >>> generar_recurrencia_desde_info(info, [])
        'T(n) = 2T(n/2) + f(n)'
    """
    # Manejar tanto dict como objeto RecursionInfo
    if isinstance(recursion_info, dict):
        num_calls = recursion_info.get('num_calls', 1)
        call_pattern = recursion_info.get('call_pattern', ['n-1'])
        recurrence_type = recursion_info.get('recurrence_type', 'subtract')
    else:
        num_calls = recursion_info.num_calls
        call_pattern = recursion_info.call_pattern
        recurrence_type = recursion_info.recurrence_type
    
    pasos.append(f"   ► Número de llamadas recursivas: {num_calls}")
    pasos.append(f"   ► Patrón de transformación: {call_pattern}")
    pasos.append(f"   ► Tipo de recurrencia: {recurrence_type}")
    
    # Construir términos recursivos
    if num_calls == 1:
        # Una sola llamada: T(n-1), T(n/2), etc.
        termino_recursivo = f"T({call_pattern[0]})"
        pasos.append(f"   ► Término recursivo: {termino_recursivo}")
        
    elif len(set(call_pattern)) == 1:
        # Múltiples llamadas con mismo patrón: aT(n/b)
        termino_recursivo = f"{num_calls}T({call_pattern[0]})"
        pasos.append(f"   ► Término recursivo: {termino_recursivo}")
        
    else:
        # Llamadas con patrones diferentes: T(n/3) + T(2n/3)
        terminos = [f"T({p})" for p in call_pattern]
        termino_recursivo = " + ".join(terminos)
        pasos.append(f"   ► Términos recursivos: {termino_recursivo}")
    
    # Determinar f(n) - trabajo no recursivo
    # Por ahora, usar placeholders comunes
    if recurrence_type == "divide":
        f_n = "n"  # Típico para divide y conquista
    elif recurrence_type == "subtract":
        f_n = "c"  # Típico para decrementación (constante)
    else:
        f_n = "f(n)"  # Genérico
    
    pasos.append(f"   ► Trabajo no recursivo: {f_n}")
    
    # Construir ecuación completa
    ecuacion = f"T(n) = {termino_recursivo} + {f_n}"
    
    return ecuacion


def inferir_recurrencia_de_scenarios(scenarios, pasos: list) -> str:
    """
    Intenta inferir la relación de recurrencia analizando los escenarios.
    
    Busca patrones en los costos para deducir la forma de la recurrencia.
    Este es un fallback cuando no hay RecursionInfo disponible.
    
    Args:
        scenarios: Lista de escenarios
        pasos: Lista para agregar pasos
    
    Returns:
        str: Relación de recurrencia inferida
    """
    pasos.append("   ► Analizando escenarios para inferir patrón...")
    
    # Buscar términos recursivos en los costos
    for scenario in scenarios:
        cost = scenario.cost_T.lower()
        
        # Detectar decrementación: T(n-1), T(n-2), etc.
        if 't(n-' in cost:
            pasos.append(f"   ► Patrón detectado: Decrementación")
            return "T(n) = T(n-1) + c"
        
        # Detectar divide y conquista: T(n/2), etc.
        if 't(n/' in cost:
            # Contar cuántos T(...) hay
            num_terms = cost.count('t(n/')
            if num_terms == 1:
                pasos.append(f"   ► Patrón detectado: Divide y conquista simple")
                return "T(n) = T(n/2) + f(n)"
            else:
                pasos.append(f"   ► Patrón detectado: Divide y conquista múltiple")
                return "T(n) = 2T(n/2) + f(n)"
    
    # Fallback: recurrencia genérica
    pasos.append("   ⚠️ No se pudo inferir patrón específico")
    pasos.append("   ► Usando forma genérica")
    return "T(n) = T(n-1) + f(n)"


def es_divide_y_conquista(call_pattern: list) -> bool:
    """
    Verifica si el patrón corresponde a divide y conquista.
    
    Args:
        call_pattern: Lista de transformaciones (ej: ["n/2", "n/2"])
    
    Returns:
        bool: True si es divide y conquista (divisiones)
    """
    for pattern in call_pattern:
        if '/' in pattern or 'log' in pattern.lower():
            return True
    return False


def es_decrementacion(call_pattern: list) -> bool:
    """
    Verifica si el patrón corresponde a decrementación.
    
    Args:
        call_pattern: Lista de transformaciones (ej: ["n-1"])
    
    Returns:
        bool: True si es decrementación (restas)
    """
    for pattern in call_pattern:
        if '-' in pattern and '/' not in pattern:
            return True
    return False
