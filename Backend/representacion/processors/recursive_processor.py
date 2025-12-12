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
    
    # Casos base deshabilitados (ya no se generan)
    casos_base = None
    
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
        'casos_base': casos_base,
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
    
    # PASO 1: Separar casos base de escenarios recursivos
    pasos.append("🔍 Separando casos base de escenarios recursivos...")
    
    casos_base_scenarios = []
    escenarios_recursivos = []
    
    for scenario in scenarios:
        condicion_lower = scenario.condition.lower()
        costo_lower = scenario.cost_T.lower()
        
        # Un escenario es caso base si:
        # 1. No tiene llamadas recursivas en el costo (no contiene T(...)
        # 2. O la condición indica valores pequeños (n=0, n=1, n≤1)
        es_caso_base = (
            ('t(n' not in costo_lower and 't(' not in costo_lower) or
            'n = 0' in condicion_lower or 'n == 0' in condicion_lower or 'n=0' in condicion_lower or
            'n = 1' in condicion_lower or 'n == 1' in condicion_lower or 'n=1' in condicion_lower or
            'n ≤ 1' in condicion_lower or 'n <= 1' in condicion_lower or 'n<=1' in condicion_lower or
            'caso base' in condicion_lower or 'base case' in condicion_lower
        )
        
        if es_caso_base:
            casos_base_scenarios.append(scenario)
            pasos.append(f"   ► Caso base detectado: {scenario.id}")
        else:
            escenarios_recursivos.append(scenario)
            pasos.append(f"   ► Escenario recursivo: {scenario.id}")
    
    pasos.append("")
    pasos.append(f"📊 Total: {len(casos_base_scenarios)} casos base, {len(escenarios_recursivos)} escenarios recursivos")
    pasos.append("")
    
    # Si no hay escenarios recursivos, error
    if not escenarios_recursivos:
        pasos.append("⚠️ ERROR: No se encontraron escenarios recursivos")
        return {
            'mejor_caso': 'T(n) = c',
            'caso_promedio': 'T(n) = c',
            'peor_caso': 'T(n) = c',
            'ecuaciones_iguales': True,
            'casos_base': extraer_casos_base(omega_table, pasos),
            'tipo_analisis': 'recursivo_uniforme',
            'pasos_generacion': pasos
        }
    
    # PASO 2: Revisar si el LLM tiene sugerencias para casos diferenciados
    tiene_llm_diferenciado = False
    if llm_analysis:
        mejor_llm = llm_analysis.get('mejor_caso', {}).get('ecuacion_sugerida')
        peor_llm = llm_analysis.get('peor_caso', {}).get('ecuacion_sugerida')
        
        # Validar que las sugerencias del LLM sean ecuaciones recursivas, no casos base
        mejor_es_recursivo = mejor_llm and ('T(n' in mejor_llm or 'T (n' in mejor_llm) and mejor_llm != 'T(1) = c' and mejor_llm != 'T(0) = c'
        peor_es_recursivo = peor_llm and ('T(n' in peor_llm or 'T (n' in peor_llm) and peor_llm != 'T(1) = c' and peor_llm != 'T(0) = c'
        
        # Solo marcar como diferenciado si AMBOS son recursivos Y son DIFERENTES
        if mejor_es_recursivo and peor_es_recursivo and mejor_llm != peor_llm:
            tiene_llm_diferenciado = True
            pasos.append("🤖 LLM detectó ecuaciones diferentes para mejor y peor caso")
            pasos.append(f"   ► Mejor: {mejor_llm}")
            pasos.append(f"   ► Peor: {peor_llm}")
            pasos.append("")
        elif mejor_llm and peor_llm and not mejor_es_recursivo:
            pasos.append(f"⚠️  LLM sugiere caso base para mejor caso, ignorando sugerencias")
            pasos.append("")
    
    # PASO 3: Filtrar escenarios "fallback" (heurísticos poco confiables)
    escenarios_confiables = []
    escenarios_fallback = []
    
    for scenario in escenarios_recursivos:
        if 'fallback' in scenario.id.lower() or 'fallback' in scenario.condition.lower():
            escenarios_fallback.append(scenario)
            pasos.append(f"⚠️  Escenario fallback detectado: {scenario.id}")
        else:
            escenarios_confiables.append(scenario)
    
    # Si el LLM tiene sugerencias diferenciadas, NO usar análisis uniforme
    if tiene_llm_diferenciado:
        pasos.append("✓ Usando análisis diferenciado guiado por LLM")
        pasos.append("")
        # Asegurar que tengamos escenarios para trabajar
        if not escenarios_confiables:
            escenarios_confiables = escenarios_recursivos
    elif not escenarios_confiables:
        # Si no hay LLM diferenciado y todos son fallback, usarlos
        escenarios_confiables = escenarios_recursivos
        pasos.append("⚠️  Solo hay escenarios fallback, se usarán con precaución")
    
    pasos.append("")
    
    # PASO 4: Ordenar escenarios confiables por complejidad
    scenarios_ordenados = sorted(escenarios_confiables, key=lambda s: complejidad_numerica(s.cost_T))
    
    # PASO 5: Verificar si todos los escenarios recursivos tienen la misma ecuación
    # PERO: Si el LLM sugiere ecuaciones diferentes, NO usar caso uniforme
    if tiene_llm_diferenciado:
        pasos.append("✓ LLM indica ecuaciones diferentes por caso")
        pasos.append("  → Saltando verificación de uniformidad")
        pasos.append("")
        # Forzar análisis diferenciado
        ecuaciones_recursivas = ['diferente_mejor', 'diferente_peor']
    else:
        ecuaciones_recursivas = []
        for scenario in scenarios_ordenados:
            ecuacion = construir_recurrencia(
                metadata.get('recursion_info', {}).get('num_calls', 1),
                metadata.get('recursion_info', {}).get('call_pattern', ['n-1']),
                scenario.cost_T
            )
            ecuaciones_recursivas.append(ecuacion)
    
    # Si todas las ecuaciones son iguales Y no hay LLM diferenciado, usar caso uniforme
    if len(set(ecuaciones_recursivas)) == 1 and not tiene_llm_diferenciado:
        pasos.append("✓ Todos los escenarios recursivos tienen la misma ecuación")
        pasos.append("  → Usando análisis uniforme (sin diferenciar casos)")
        pasos.append("")
        
        ecuacion_unica = ecuaciones_recursivas[0]
        # Casos base deshabilitados (ya no se generan)
        casos_base = None
        
        pasos.append("")
        pasos.append(f"📐 Ecuación de recurrencia: {ecuacion_unica}")
        pasos.append("ℹ️ Mejor caso = Caso promedio = Peor caso")
        
        return {
            'mejor_caso': ecuacion_unica,
            'caso_promedio': ecuacion_unica,
            'peor_caso': ecuacion_unica,
            'ecuaciones_iguales': True,
            'casos_base': None,
            'tipo_analisis': 'recursivo_uniforme',
            'pasos_generacion': pasos
        }
    
    # PASO 6: Si las ecuaciones son diferentes, generar por caso
    pasos.append("✓ Escenarios recursivos con ecuaciones diferentes")
    pasos.append("  → Generando ecuaciones diferenciadas por caso")
    pasos.append("")
    
    # Si el LLM tiene sugerencias diferenciadas, usarlas directamente
    if tiene_llm_diferenciado:
        pasos.append("🤖 Usando sugerencias del LLM para casos diferenciados")
        pasos.append("")
        
        # MEJOR CASO desde LLM
        pasos.append("🔍 MEJOR CASO (Ω):")
        mejor_caso = llm_analysis['mejor_caso'].get('ecuacion_sugerida')
        pasos.append(f"   ► 🤖 LLM: {mejor_caso}")
        pasos.append("")
        
        # PEOR CASO desde LLM
        pasos.append("🔍 PEOR CASO (O):")
        peor_caso = llm_analysis['peor_caso'].get('ecuacion_sugerida')
        pasos.append(f"   ► 🤖 LLM: {peor_caso}")
        pasos.append("")
        
        # CASO PROMEDIO desde LLM o interpolación
        pasos.append("📊 CASO PROMEDIO (Θ):")
        if llm_analysis.get('caso_promedio', {}).get('ecuacion_sugerida'):
            caso_promedio = llm_analysis['caso_promedio']['ecuacion_sugerida']
            pasos.append(f"   ► 🤖 LLM: {caso_promedio}")
        else:
            # Si no hay caso promedio del LLM, usar el mejor caso (típicamente)
            caso_promedio = mejor_caso
            pasos.append(f"   ► Usando mejor caso: {caso_promedio}")
        pasos.append("")
        
    else:
        # Análisis tradicional basado en escenarios ordenados
        # MEJOR CASO (del conjunto recursivo)
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
        
        # CASO PROMEDIO (de los escenarios recursivos)
        pasos.append("📊 CASO PROMEDIO (Θ):")
        
        # Si solo hay escenarios fallback y mejor==peor corregidos por LLM, usar el mismo
        if len(escenarios_fallback) == len(escenarios_recursivos) and mejor_caso == peor_caso:
            caso_promedio = mejor_caso
            pasos.append(f"   ► Usando ecuación de mejor/peor caso (todos escenarios fallback)")
        else:
            # Seleccionar escenario intermedio
            if len(scenarios_ordenados) >= 3:
                promedio_scenario = scenarios_ordenados[len(scenarios_ordenados) // 2]
            else:
                promedio_scenario = mejor_scenario
            
            pasos.append(f"   ► Escenario: {promedio_scenario.id}")
            caso_promedio = construir_recurrencia(num_calls_mejor, pattern_mejor, promedio_scenario.cost_T)
            
            # Aplicar sugerencia LLM si existe
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
    
    # Casos base deshabilitados (ya no se generan)
    casos_base = None
    
    # Verificar si las ecuaciones son iguales
    son_iguales = (mejor_caso == caso_promedio == peor_caso)
    
    if son_iguales:
        pasos.append("")
        pasos.append("ℹ️ Las 3 ecuaciones recursivas son idénticas")
        pasos.append("   (Algoritmo determinista sin variación por entrada)")
    
    return {
        'mejor_caso': mejor_caso,
        'caso_promedio': caso_promedio,
        'peor_caso': peor_caso,
        'ecuaciones_iguales': son_iguales,
        'casos_base': None,
        'tipo_analisis': 'recursivo_diferenciado',
        'pasos_generacion': pasos
    }


def construir_recurrencia(num_calls: int, call_pattern: list, cost_T: str) -> str:
    """
    Construye la relación de recurrencia a partir de parámetros.
    
    Estrategia:
    1. Si cost_T ya tiene formato de recurrencia (T(n) = ...), extraerlo y simplificarlo
    2. Si no, construir desde num_calls y call_pattern
    
    Maneja casos especiales:
    - Fibonacci: T(n) = T(n-1) + T(n-2) + c
    - Hanoi: T(n) = 2T(n-1) + c
    - Divide y conquista: T(n) = aT(n/b) + f(n)
    
    Args:
        num_calls: Número de llamadas recursivas
        call_pattern: Patrón de transformación
        cost_T: Costo original del escenario (puede contener la recurrencia completa)
    
    Returns:
        str: Recurrencia construida
    """
    cost_T_clean = cost_T.strip()
    
    # ESTRATEGIA 1: Si cost_T ya tiene formato T(n) = ..., extraerlo y simplificarlo
    if cost_T_clean.startswith('T(n)'):
        # Ya es una ecuación de recurrencia, simplificar constantes
        ecuacion = cost_T_clean
        
        # Simplificar constantes numéricas a 'c'
        # T(n) = T(n-1) + T(n-2) + 4 → T(n) = T(n-1) + T(n-2) + c
        import re
        # Reemplazar números al final (después de +/-) por 'c'
        ecuacion = re.sub(r'\+\s*\d+\s*$', '+ c', ecuacion)
        ecuacion = re.sub(r'-\s*\d+\s*$', '- c', ecuacion)
        
        # Si no hay constante al final pero hay llamadas recursivas, agregar + c
        if 'T(n' in ecuacion and not ecuacion.endswith('c') and not any(ecuacion.endswith(x) for x in [')', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']):
            if '+' in ecuacion or '-' in ecuacion:
                pass  # Ya tiene operaciones
            else:
                ecuacion += ' + c'
        
        return ecuacion
    
    # ESTRATEGIA 2: Construir desde parámetros
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


def extraer_casos_base(omega_table: OmegaTable, pasos: list) -> list:
    """
    Extrae los casos base de un algoritmo recursivo.
    
    Los casos base son escenarios donde:
    - No hay llamadas recursivas (costo constante)
    - La condición indica valores pequeños de n (n=0, n=1, n≤1, etc.)
    - El tipo_caso es 'best_case' o similar
    
    Args:
        omega_table: Tabla Omega con escenarios
        pasos: Lista para agregar pasos de generación
    
    Returns:
        List[str]: Lista de casos base (ej: ['T(0) = c', 'T(1) = c'])
    """
    casos_base = []
    scenarios = omega_table.scenarios
    
    pasos.append("🔍 Extrayendo casos base...")
    
    for scenario in scenarios:
        # Detectar casos base por condición
        condicion_lower = scenario.condition.lower()
        costo_lower = scenario.cost_T.lower()
        
        # Verificar primero si NO tiene llamadas recursivas (es constante)
        tiene_recursion = 't(n' in costo_lower or 't(' in costo_lower
        
        # Patrones que indican caso base
        es_caso_base = False
        valores_n = []
        
        # Detectar valores específicos o rangos
        if 'n = 0' in condicion_lower or 'n == 0' in condicion_lower or 'n=0' in condicion_lower:
            valores_n.append(0)
        if 'n = 1' in condicion_lower or 'n == 1' in condicion_lower or 'n=1' in condicion_lower:
            valores_n.append(1)
        if 'n ≤ 1' in condicion_lower or 'n <= 1' in condicion_lower or 'n<=1' in condicion_lower:
            valores_n = [0, 1]
        
        # Si menciona "0 o 1", "0 or 1", etc.
        if ('0' in condicion_lower and '1' in condicion_lower and 
            ('o' in condicion_lower or 'or' in condicion_lower)):
            valores_n = [0, 1]
        
        # Si es best_case Y no tiene recursión, es caso base
        if (scenario.semantic_id == 'best_case' or 'best' in scenario.id.lower()) and not tiene_recursion:
            es_caso_base = True
            # Si no detectó valores específicos, inferir de la condición
            if not valores_n:
                if '0' in condicion_lower and '1' in condicion_lower:
                    valores_n = [0, 1]
                elif '0' in condicion_lower:
                    valores_n = [0]
                elif '1' in condicion_lower:
                    valores_n = [1]
                else:
                    valores_n = ['base']
        
        # También detectar si explícitamente dice "caso base"
        if 'caso base' in condicion_lower or 'base case' in condicion_lower:
            es_caso_base = True
            if not valores_n:
                valores_n = [0, 1]  # Asumimos ambos por defecto
        
        # Si encontró valores Y no tiene recursión, es caso base
        if valores_n and not tiene_recursion:
            es_caso_base = True
        
        if es_caso_base:
            # Construir ecuaciones para cada valor
            for val in valores_n:
                if val in [0, 1]:
                    caso_base_eq = f"T({val}) = c"
                else:
                    caso_base_eq = f"T(base) = c"
                
                if caso_base_eq not in casos_base:  # Evitar duplicados
                    casos_base.append(caso_base_eq)
                    pasos.append(f"   ► Encontrado: {caso_base_eq}")
    
    if not casos_base:
        pasos.append("   ⚠️ No se encontraron casos base explícitos")
        pasos.append("   ► Infiriendo caso base genérico: T(0) = c")
        casos_base.append("T(0) = c")
    
    pasos.append("")
    return casos_base
