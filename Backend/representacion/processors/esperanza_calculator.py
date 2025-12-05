"""
Calculador de Esperanza Matemática E[T].

Calcula el valor esperado de T(n) para algoritmos iterativos con múltiples
escenarios probabilísticos.

Fórmula: E[T] = Σ T(S) · P(S) para todos los escenarios S en Ω
"""

import sympy as sp
from typing import List, Tuple
from core.analizador.models.omega_table import ScenarioEntry


def calculate_expected_value(scenarios: List[ScenarioEntry]) -> Tuple[str, str]:
    """
    Calcula la Esperanza Matemática E[T] para un conjunto de escenarios.
    
    Aplica la fórmula:
        E[T] = Σ T(S) · P(S) para todo S en Ω
    
    Donde:
    - T(S) = costo del escenario S
    - P(S) = probabilidad del escenario S
    - Ω = espacio de todos los escenarios posibles
    
    Args:
        scenarios: Lista de escenarios con cost_T y probability_P
    
    Returns:
        Tuple[str, str]: (ecuacion_simplificada, derivacion_completa)
            - ecuacion_simplificada: Resultado final de E[T]
            - derivacion_completa: Pasos detallados del cálculo
    
    Examples:
        >>> scenarios = [
        ...     ScenarioEntry(id="S_1", cost_T="6", probability_P="1/n", ...),
        ...     ScenarioEntry(id="S_k", cost_T="4*k + 2", probability_P="1/n", ...),
        ...     ScenarioEntry(id="S_n", cost_T="4*n + 2", probability_P="1/n", ...)
        ... ]
        >>> ecuacion, derivacion = calculate_expected_value(scenarios)
        >>> # ecuacion: "2*n + 4" (simplificado)
    """
    if not scenarios:
        return "0", "No hay escenarios para calcular E[T]"
    
    # Si solo hay un escenario, E[T] = T(S) * P(S)
    if len(scenarios) == 1:
        scenario = scenarios[0]
        derivacion = f"E[T] = {scenario.cost_T} · {scenario.probability_P}"
        
        # Si P = 1, E[T] = T
        if scenario.probability_P == "1":
            return scenario.cost_T, derivacion
        
        # Calcular producto
        try:
            result = _calcular_producto_simple(scenario.cost_T, scenario.probability_P)
            derivacion += f"\nE[T] = {result}"
            return result, derivacion
        except:
            return scenario.cost_T, derivacion
    
    # Múltiples escenarios: sumar todos
    return _calcular_esperanza_multiple(scenarios)


def _calcular_esperanza_multiple(scenarios: List[ScenarioEntry]) -> Tuple[str, str]:
    """
    Calcula E[T] para múltiples escenarios usando SymPy.
    
    Maneja casos como:
    - Sumatorias con variable k
    - Múltiples grupos de probabilidad
    - Simplificación algebraica
    """
    # Símbolos
    n = sp.Symbol('n', positive=True, integer=True)
    k = sp.Symbol('k', positive=True, integer=True)
    q = sp.Symbol('q', real=True, positive=True)
    
    derivacion_pasos = []
    derivacion_pasos.append("📊 CÁLCULO DE ESPERANZA MATEMÁTICA")
    derivacion_pasos.append("")
    derivacion_pasos.append("E[T] = Σ T(S) · P(S) para todo S ∈ Ω")
    derivacion_pasos.append("")
    
    # Agrupar escenarios por tipo
    escenarios_exito = []
    escenarios_fallo = []
    
    for scenario in scenarios:
        if 'fallo' in scenario.state.lower() or 'fail' in scenario.state.lower():
            escenarios_fallo.append(scenario)
        else:
            escenarios_exito.append(scenario)
    
    suma_total = 0
    
    # Procesar escenarios de éxito
    if escenarios_exito:
        derivacion_pasos.append("▸ Casos de ÉXITO:")
        
        for scenario in escenarios_exito:
            try:
                T_S = _parsear_expresion(scenario.cost_T, n, k)
                P_S = _parsear_expresion(scenario.probability_P, n, k, q)
                
                termino = T_S * P_S
                suma_total += termino
                
                derivacion_pasos.append(f"  + ({scenario.cost_T}) · ({scenario.probability_P})")
                
            except Exception as e:
                derivacion_pasos.append(f"  ! Error parseando {scenario.id}: {str(e)}")
    
    # Procesar escenarios de fallo
    if escenarios_fallo:
        derivacion_pasos.append("")
        derivacion_pasos.append("▸ Casos de FALLO:")
        
        for scenario in escenarios_fallo:
            try:
                T_S = _parsear_expresion(scenario.cost_T, n, k)
                P_S = _parsear_expresion(scenario.probability_P, n, k, q)
                
                termino = T_S * P_S
                suma_total += termino
                
                derivacion_pasos.append(f"  + ({scenario.cost_T}) · ({scenario.probability_P})")
                
            except Exception as e:
                derivacion_pasos.append(f"  ! Error parseando {scenario.id}: {str(e)}")
    
    derivacion_pasos.append("")
    derivacion_pasos.append(f"= {suma_total}")
    
    # Simplificar
    try:
        simplificado = sp.simplify(suma_total)
        derivacion_pasos.append("")
        derivacion_pasos.append("📐 Simplificando:")
        derivacion_pasos.append(f"E[T] = {simplificado}")
        
        # Convertir a string limpio
        resultado_str = str(simplificado)
        
        # Asumir q=1 si aparece (elemento siempre existe)
        if 'q' in resultado_str:
            simplificado_q1 = simplificado.subs(q, 1)
            derivacion_pasos.append("")
            derivacion_pasos.append("Asumiendo q=1 (elemento siempre presente):")
            derivacion_pasos.append(f"E[T] = {simplificado_q1}")
            resultado_str = str(simplificado_q1)
        
        return resultado_str, "\n".join(derivacion_pasos)
        
    except Exception as e:
        derivacion_pasos.append(f"\n⚠️ Error en simplificación: {str(e)}")
        return str(suma_total), "\n".join(derivacion_pasos)


def _parsear_expresion(expr_str: str, n, k, q=None):
    """
    Parsea una expresión string a SymPy.
    
    Maneja:
    - Operadores: +, -, *, /, ^, **
    - Variables: n, k, q
    - Fracciones: 1/n, k/n, etc.
    """
    expr_str = expr_str.strip().replace(' ', '')
    
    # Normalizar operadores
    expr_str = expr_str.replace('^', '**')
    
    # Casos especiales comunes
    if expr_str == '1':
        return sp.Integer(1)
    if expr_str == '0':
        return sp.Integer(0)
    
    # Parsear con SymPy
    try:
        # Crear diccionario de variables locales
        local_vars = {'n': n, 'k': k}
        if q is not None:
            local_vars['q'] = q
        
        expr = sp.sympify(expr_str, locals=local_vars)
        return expr
        
    except Exception as e:
        raise ValueError(f"No se pudo parsear '{expr_str}': {str(e)}")


def _calcular_producto_simple(cost: str, prob: str) -> str:
    """
    Calcula el producto simple T * P para un solo escenario.
    """
    n = sp.Symbol('n', positive=True, integer=True)
    
    try:
        T = _parsear_expresion(cost, n, None)
        P = _parsear_expresion(prob, n, None)
        
        resultado = sp.simplify(T * P)
        return str(resultado)
        
    except:
        return f"({cost}) * ({prob})"


def inferir_sumatoria_k(scenarios: List[ScenarioEntry]) -> bool:
    """
    Detecta si los escenarios requieren una sumatoria sobre k.
    
    Returns:
        bool: True si hay variable k en los costos
    """
    for scenario in scenarios:
        if 'k' in scenario.cost_T.lower():
            return True
    return False
