"""
Formateador de Ecuaciones.

Provee funciones para simplificar y formatear ecuaciones matemáticas
para el Agente Resolver.
"""

import re
import sympy as sp
from typing import Tuple


def simplificar_con_constantes(cost_str: str, es_caso_promedio: bool = False, tipo_caso: str = 'mejor') -> str:
    """
    Simplifica una expresión de costo usando constantes simbólicas.
    
    Maneja todos los tipos de complejidad algorítmica:
    - Constante: K1 (mejor), K2 (promedio), K3 (peor)
    - Logarítmica: log(n)*C, log2(n)*C, (log(n)/2)*C
    - Lineal: n*C, (n/2)*C
    - Linealítmica: n*log(n)*C
    - Cuadrática: n**2*C
    - Cúbica: n**3*C
    - Exponencial: 2**n*C, n**n*C
    - Raíz: sqrt(n)*C
    - Factorial: n!*C
    
    Args:
        cost_str: Expresión de costo
        es_caso_promedio: Si True, preserva fracciones como n/2
        tipo_caso: 'mejor', 'promedio', o 'peor' para determinar K1, K2, K3
    
    Returns:
        str: Expresión simplificada con constantes
    """
    # Normalizar entrada
    cost_str = cost_str.strip().replace(' ', '')
    
    # Caso especial: constante numérica pura
    try:
        float(cost_str)
        # Retornar K apropiado según el tipo de caso
        if tipo_caso == 'mejor':
            return "K1"
        elif tipo_caso == 'promedio':
            return "K2"
        else:  # peor
            return "K3"
    except:
        pass
    
    # Parsear con SymPy
    try:
        n = sp.Symbol('n', positive=True, integer=True)
        k = sp.Symbol('k', positive=True, integer=True)
        S = sp.Symbol('S', positive=True)  # Símbolo para sumatorias
        
        # Preparar expresión para SymPy
        expr_str = _preparar_expresion(cost_str)
        
        # Reemplazar k por n si existe
        if 'k' in expr_str and 'k' != expr_str:
            expr_str = expr_str.replace('k', 'n')
        
        # Parsear
        expr = sp.sympify(expr_str, locals={'n': n, 'k': k, 'S': S})
        expr_expanded = sp.expand(expr)
        
    except Exception as e:
        return _simplificar_basico(cost_str)
    
    # Analizar componentes de la expresión
    componentes = _analizar_expresion(expr_expanded, n, cost_str)
    
    # Construir resultado
    return _construir_resultado(componentes, cost_str, es_caso_promedio, tipo_caso)


def _preparar_expresion(expr_str: str) -> str:
    """
    Prepara una expresión para ser parseada por SymPy.
    
    Convierte notaciones comunes a formato SymPy:
    - log2(n) → log(n)/log(2)
    - log10(n) → log(n)/log(10)
    - ln(n) → log(n)
    - sqrt(n) → n**(1/2)
    - n! → factorial(n)
    - ^ → **
    - Σ(i=1 to n) f(i) → S (símbolo temporal para análisis)
    """
    # Operadores
    expr_str = expr_str.replace('^', '**')
    
    # Sumatorias - detectar múltiples formas y reemplazar por símbolo S
    # Σ(i=1 to n), sum(i=1 to n), sum(1,n), Σ i=1..n, etc.
    sumatoria_patterns = [
        r'Σ\s*\(?\s*i\s*=\s*1\s*(?:to|hasta|a|\.\.)\.?\s*n\s*\)?',
        r'sum\s*\(\s*(?:i\s*=\s*)?1\s*,\s*n\s*\)',
        r'sum\s*\(\s*i\s*,\s*1\s*,\s*n\s*\)',
        r'Σ\s*\(\s*1\s*,\s*n\s*\)',
        r'suma\(1,n\)',
    ]
    
    for pattern in sumatoria_patterns:
        # Reemplazar por S (símbolo que SymPy puede parsear)
        expr_str = re.sub(pattern, 'S', expr_str, flags=re.IGNORECASE)
    
    # Logaritmos - usar división para evitar problemas de SymPy
    expr_str = re.sub(r'log2\(([^)]+)\)', r'(log(\1)/log(2))', expr_str)
    expr_str = re.sub(r'log10\(([^)]+)\)', r'(log(\1)/log(10))', expr_str)
    expr_str = re.sub(r'ln\(([^)]+)\)', r'log(\1)', expr_str)
    
    # Raíz cuadrada
    expr_str = re.sub(r'sqrt\(([^)]+)\)', r'(\1)**(1/2)', expr_str)
    
    # Factorial
    expr_str = re.sub(r'(\w+)!', r'factorial(\1)', expr_str)
    
    return expr_str


def _analizar_expresion(expr, n, original_str: str) -> dict:
    """
    Analiza una expresión SymPy y extrae sus componentes.
    
    Returns:
        dict con claves:
        - constante: término constante
        - n_lineal: coeficiente de n
        - n_cuadratico: coeficiente de n²
        - n_cubico: coeficiente de n³
        - logaritmico: coeficiente de log(n)
        - nlogn: coeficiente de n*log(n)
        - exponencial: si tiene términos exponenciales
        - raiz: si tiene términos con raíz
        - expresiones_especiales: lista de expresiones entre paréntesis en original
    """
    componentes = {
        'constante': 0,
        'n_lineal': 0,
        'n_cuadratico': 0,
        'n_cubico': 0,
        'logaritmico': 0,
        'nlogn': 0,
        'n2logn': 0,
        'exponencial': None,
        'raiz': False,
        'factorial': False,
        'sumatoria': False,
        'expresiones_especiales': []
    }
    
    # Símbolo S para sumatorias
    S = sp.Symbol('S', positive=True)
    
    # Detectar si hay sumatorias (símbolo S) y guardar coeficiente
    if expr.has(S):
        try:
            # Intentar extraer el coeficiente de S
            coef_S = expr.coeff(S, 1)
            if coef_S and coef_S != 0:
                componentes['sumatoria'] = coef_S
            else:
                componentes['sumatoria'] = True
        except:
            componentes['sumatoria'] = True
        
        # Sustituir S por 0 para analizar el resto de la expresión
        expr = expr.subs(S, 0)
    
    # Término constante (n=0)
    try:
        componentes['constante'] = expr.subs(n, 0)
    except:
        pass
    
    # Coeficientes de potencias de n
    try:
        componentes['n_lineal'] = expr.coeff(n, 1)
    except:
        pass
    
    try:
        componentes['n_cuadratico'] = expr.coeff(n, 2)
    except:
        pass
    
    try:
        componentes['n_cubico'] = expr.coeff(n, 3)
    except:
        pass
    
    # Analizar todos los términos de la expresión
    for term in sp.Add.make_args(expr):
        # Términos logarítmicos y combinaciones
        if term.has(sp.log):
            # Verificar si tiene n fuera del logaritmo (n*log(n))
            # Sustituir temporalmente log(n) por un símbolo para verificar
            L = sp.Symbol('L')
            term_sin_log = term.subs(sp.log(n), L)
            
            # Si después de reemplazar log(n) todavía tiene n, es n*log(n)
            if term_sin_log.has(n):
                # Es n*log(n) o n²*log(n)
                # Verificar si es n*log(n)
                try:
                    temp = term / (n * sp.log(n) / sp.log(2))
                    if temp.is_number or temp.is_symbol or not temp.has(n):
                        if componentes['nlogn'] == 0:
                            componentes['nlogn'] = temp
                        else:
                            componentes['nlogn'] += temp
                        continue
                except:
                    pass
                
                try:
                    temp = term / (n * sp.log(n))
                    if temp.is_number or temp.is_symbol or not temp.has(n):
                        if componentes['nlogn'] == 0:
                            componentes['nlogn'] = temp
                        else:
                            componentes['nlogn'] += temp
                        continue
                except:
                    pass
                
                # Verificar si es n²*log(n)
                try:
                    temp = term / (n**2 * sp.log(n) / sp.log(2))
                    if temp.is_number or temp.is_symbol or not temp.has(n):
                        if componentes['n2logn'] == 0:
                            componentes['n2logn'] = temp
                        else:
                            componentes['n2logn'] += temp
                        continue
                except:
                    pass
                
                try:
                    temp = term / (n**2 * sp.log(n))
                    if temp.is_number or temp.is_symbol or not temp.has(n):
                        if componentes['n2logn'] == 0:
                            componentes['n2logn'] = temp
                        else:
                            componentes['n2logn'] += temp
                        continue
                except:
                    pass
            else:
                # Es solo log(n)*coef
                try:
                    coef = term / (sp.log(n) / sp.log(2))
                    # Aceptar números o símbolos (como c6, c7, etc)
                    if coef.is_number or coef.is_symbol or not coef.has(sp.log):
                        if componentes['logaritmico'] == 0:
                            componentes['logaritmico'] = coef
                        else:
                            componentes['logaritmico'] += coef
                        continue
                except:
                    pass
                
                try:
                    coef = term / sp.log(n)
                    # Aceptar números o símbolos (como c6, c7, etc)
                    if coef.is_number or coef.is_symbol or not coef.has(sp.log):
                        if componentes['logaritmico'] == 0:
                            componentes['logaritmico'] = coef
                        else:
                            componentes['logaritmico'] += coef
                        continue
                except:
                    pass
        
        # Raíz cuadrada (SymPy convierte sqrt(n) a n**(1/2))
        if term.has(sp.Pow):
            for factor in sp.Mul.make_args(term):
                if isinstance(factor, sp.Pow):
                    base, exp = factor.as_base_exp()
                    if base == n and exp == sp.Rational(1, 2):
                        # Es sqrt(n)*coef
                        try:
                            coef = term / sp.sqrt(n)
                            if coef.is_number or coef.is_symbol or not coef.has(n):
                                if componentes['raiz'] == 0:
                                    componentes['raiz'] = coef
                                else:
                                    componentes['raiz'] += coef
                                break
                        except:
                            pass
        
        # Exponencial (2^n, e^n, n^n)
        if term.has(sp.exp):
            componentes['exponencial'] = True
        elif term.has(sp.Pow):
            for factor in sp.Mul.make_args(term):
                if isinstance(factor, sp.Pow):
                    base, exp_val = factor.as_base_exp()
                    # Verificar que no sea sqrt (que también es Pow pero con exp=1/2)
                    if exp_val.has(n) and exp_val != sp.Rational(1, 2):
                        componentes['exponencial'] = str(factor)
        
        # Factorial
        if term.has(sp.factorial):
            componentes['factorial'] = True
    
    # Detectar expresiones especiales entre paréntesis en el string original
    matches = re.findall(r'\(([^)]*(?:n|log)[^)]*)\)', original_str)
    componentes['expresiones_especiales'] = matches
    
    return componentes


def _construir_resultado(componentes: dict, original_str: str, es_caso_promedio: bool, tipo_caso: str = 'mejor') -> str:
    """
    Construye la representación simplificada final.
    Mantiene la estructura simbólica K + (n/2)*C para casos promedio.
    """
    partes = []
    
    # Constante (K1, K2, K3 según el caso)
    tiene_constante = componentes['constante'] != 0
    
    # Determinar qué símbolo K usar basado en tipo_caso
    if tipo_caso == 'mejor':
        simbolo_k = "K1"
    elif tipo_caso == 'promedio':
        simbolo_k = "K2"
    else:  # peor
        simbolo_k = "K3"
    
    # Verificar si hay términos dependientes de n
    tiene_terminos_n = any([
        componentes['n_lineal'] != 0,
        componentes['n_cuadratico'] != 0,
        componentes['n_cubico'] != 0,
        componentes['logaritmico'] != 0,
        componentes['nlogn'] != 0,
        componentes['n2logn'] != 0,
        componentes['exponencial'],
        componentes['raiz'],
        componentes['factorial'],
        componentes['sumatoria']
    ])
    
    # Si solo hay constante, retornar K apropiado
    if tiene_constante and not tiene_terminos_n:
        return simbolo_k
    
    # Si hay constante y términos de n, agregar K
    if tiene_constante:
        partes.append(simbolo_k)
    
    # Logarítmico
    if componentes['logaritmico'] != 0:
        if '(log2(n)/2)' in original_str or 'log2(n)/2' in original_str:
            partes.append("(log2(n)/2)*C")
        elif '(log(n)/2)' in original_str or 'log(n)/2' in original_str:
            partes.append("(log(n)/2)*C")
        elif 'log2' in original_str:
            partes.append("log2(n)*C")
        elif 'log10' in original_str:
            partes.append("log10(n)*C")
        elif 'ln' in original_str:
            partes.append("ln(n)*C")
        else:
            partes.append("log(n)*C")
    
    # Raíz
    if componentes['raiz'] != 0:
        partes.append("sqrt(n)*C")
    
    # Lineal - AQUÍ está la clave para casos promedio
    if componentes['n_lineal'] != 0:
        # Buscar expresiones especiales con n
        expr_n = [e for e in componentes['expresiones_especiales'] if 'n' in e and 'log' not in e]
        if expr_n:
            partes.append(f"({expr_n[0]})*C")
        else:
            # Intentar convertir a float solo si es un número
            try:
                coef_val = float(componentes['n_lineal']) if componentes['n_lineal'] != 0 else 0
                if abs(coef_val - 0.5) < 0.01 or (es_caso_promedio and '/2' in original_str):
                    partes.append("(n/2)*C")
                elif abs(coef_val - 0.25) < 0.01:
                    partes.append("(n/4)*C")
                elif abs(coef_val - 0.75) < 0.01:
                    partes.append("(3*n/4)*C")
                elif abs(coef_val - 1.5) < 0.01:
                    partes.append("(3*n/2)*C")
                else:
                    partes.append("n*C")
            except (TypeError, AttributeError):
                # Si no se puede convertir a float, es una expresión simbólica
                partes.append("n*C")
    
    # n*log(n)
    if componentes['nlogn'] != 0:
        if 'log2' in original_str:
            partes.append("n*log2(n)*C")
        else:
            partes.append("n*log(n)*C")
    
    # Cuadrático
    if componentes['n_cuadratico'] != 0:
        partes.append("n**2*C")
    
    # n²*log(n)
    if componentes['n2logn'] != 0:
        partes.append("n**2*log(n)*C")
    
    # Cúbico
    if componentes['n_cubico'] != 0:
        partes.append("n**3*C")
    
    # Sumatoria
    if componentes['sumatoria']:
        partes.append("Σ(i=1 to n)*C")
    
    # Exponencial
    if componentes['exponencial']:
        exp_str = str(componentes['exponencial'])
        # Convertir formato SymPy a formato legible
        if '2**n' in exp_str or '2^n' in original_str:
            partes.append("2^n")
        elif 'exp(n)' in exp_str:
            partes.append("e^n")
        elif 'n**n' in exp_str:
            partes.append("n^n")
        else:
            # Formatear cualquier otro exponencial
            exp_formatted = exp_str.replace('**', '^')
            partes.append(exp_formatted)
    
    # Factorial
    if componentes['factorial']:
        partes.append("n!*C")
    
    # Si no hay partes, retornar constante apropiada
    if not partes:
        return simbolo_k
    
    return " + ".join(partes)


def _simplificar_basico(cost_str: str) -> str:
    """
    Simplificación básica sin SymPy (fallback).
    
    Args:
        cost_str: Expresión de costo
    
    Returns:
        str: Expresión simplificada
    """
    cost = cost_str.lower().replace(' ', '')
    
    # Detectar patrón común: coef*n + const
    match = re.match(r'(\d+)\*n\+(\d+)', cost)
    if match:
        return "K + n*C"
    
    # Detectar solo n
    if cost == 'n':
        return "n*C"
    
    # Detectar n**2 o n²
    if 'n**2' in cost or 'n²' in cost or 'n^2' in cost:
        if '+' in cost:
            return "K + n*C + n**2*C1"
        return "n**2*C1"
    
    # Si solo es número, es constante
    try:
        float(cost)
        return "K1"
    except:
        pass
    
    # Fallback: retornar original
    return cost_str


def format_for_resolver(equation: str, is_iterative: bool = True) -> str:
    """
    Formatea una ecuación para que sea compatible con el Agente Resolver.
    
    - Para iterativos: Mantiene formato simplificado sin "T(n) ="
    - Para recursivos: Agrega "T(n) = " si no lo tiene
    
    Args:
        equation: Ecuación a formatear
        is_iterative: True si es iterativo, False si recursivo
    
    Returns:
        str: Ecuación formateada
    
    Examples:
        >>> format_for_resolver("K + n*C", is_iterative=True)
        'K + n*C'
        >>> format_for_resolver("T(n-1) + 1", is_iterative=False)
        'T(n) = T(n-1) + 1'
        >>> format_for_resolver("T(n) = T(n-1) + 1", is_iterative=False)
        'T(n) = T(n-1) + 1'
    """
    equation = equation.strip()
    
    if is_iterative:
        # Para iterativos, remover "T(n) =" si existe
        if equation.startswith("T(n)"):
            equation = re.sub(r'^T\(n\)\s*=\s*', '', equation)
        return equation
    else:
        # Para recursivos, agregar "T(n) =" si no lo tiene
        if not equation.startswith("T(n)"):
            equation = f"T(n) = {equation}"
        return equation


def normalizar_notacion(expr: str) -> str:
    """
    Normaliza la notación matemática para SymPy.
    
    Convierte:
    - ^ → **
    - ² → **2
    - ³ → **3
    
    Args:
        expr: Expresión matemática
    
    Returns:
        str: Expresión normalizada
    """
    expr = expr.replace('^', '**')
    expr = expr.replace('²', '**2')
    expr = expr.replace('³', '**3')
    return expr


def detectar_orden_complejidad(cost_str: str) -> Tuple[str, int]:
    """
    Detecta el orden de complejidad de una expresión.
    
    Args:
        cost_str: Expresión de costo
    
    Returns:
        Tuple[str, int]: (nombre_orden, nivel_numerico)
            - nombre_orden: "constante", "logaritmica", "lineal", "cuadratica", etc.
            - nivel_numerico: Valor numérico para comparación
    
    Examples:
        >>> detectar_orden_complejidad("6")
        ('constante', 1)
        >>> detectar_orden_complejidad("n")
        ('lineal', 3)
        >>> detectar_orden_complejidad("n**2")
        ('cuadratica', 5)
    """
    cost = cost_str.lower().replace(' ', '')
    
    if 'n!' in cost:
        return ("factorial", 8)
    elif '2**n' in cost or 'exp' in cost:
        return ("exponencial", 7)
    elif 'n**3' in cost or 'n³' in cost:
        return ("cubica", 6)
    elif 'n**2' in cost or 'n²' in cost:
        return ("cuadratica", 5)
    elif 'n*log' in cost or 'nlog' in cost:
        return ("lineal_logaritmica", 4)
    elif 'n' in cost:
        return ("lineal", 3)
    elif 'log' in cost:
        return ("logaritmica", 2)
    else:
        return ("constante", 1)


def simplificar_ecuacion_compleja(cost_str: str, es_caso_promedio: bool = False, tipo_caso: str = 'mejor') -> str:
    """
    Sistema de fallback robusto para ecuaciones muy complejas.
    
    Este método se invoca cuando simplificar_con_constantes() falla
    o cuando la ecuación tiene patrones muy complejos.
    
    Estrategia:
    1. Intentar simplificación normal
    2. Si falla, usar análisis heurístico
    3. Si falla, preservar ecuación original con ajustes mínimos
    
    Args:
        cost_str: Expresión de costo
        es_caso_promedio: Si True, preserva fracciones
        tipo_caso: 'mejor', 'promedio', 'peor'
    
    Returns:
        str: Ecuación simplificada o preservada
    """
    try:
        # Intento 1: Simplificación normal
        return simplificar_con_constantes(cost_str, es_caso_promedio, tipo_caso)
    except Exception as e:
        pass
    
    # Intento 2: Análisis heurístico
    try:
        return _simplificar_heuristico(cost_str, es_caso_promedio, tipo_caso)
    except:
        pass
    
    # Intento 3: Preservar con ajustes mínimos
    return _preservar_ecuacion(cost_str, tipo_caso)


def _simplificar_heuristico(cost_str: str, es_caso_promedio: bool, tipo_caso: str) -> str:
    """
    Simplificación heurística para ecuaciones complejas.
    
    Usa patrones regex y análisis de términos para identificar
    la complejidad sin parsing completo con SymPy.
    """
    import re
    
    # Normalizar
    expr = cost_str.strip().replace(' ', '')
    
    # Determinar K basado en tipo_caso
    K = 'K1' if tipo_caso == 'mejor' else ('K2' if tipo_caso == 'promedio' else 'K3')
    
    # Detectar términos dominantes por orden de prioridad
    terminos = []
    
    # Factorial
    if re.search(r'\bn!', expr):
        terminos.append('n!*C')
    
    # Exponencial
    if re.search(r'2\*\*n|e\*\*n|exp\(n\)', expr):
        terminos.append('2**n*C')
    
    # Cúbico
    if re.search(r'n\*\*3|n³|n\*n\*n', expr):
        terminos.append('n**3*C')
    
    # Cuadrático
    if re.search(r'n\*\*2|n²|n\*n|\(n\*\(n-1\)\)/2', expr):
        terminos.append('n**2*C')
    
    # Lineal-logarítmico
    if re.search(r'n\*log|nlog', expr, re.IGNORECASE):
        terminos.append('n*log(n)*C')
    
    # Lineal (incluyendo fracciones)
    if re.search(r'\bn\b|\bn/\d+|\d\*n', expr):
        # Preservar fracciones en caso promedio
        if es_caso_promedio and re.search(r'n/2', expr):
            terminos.append('(n/2)*C')
        elif es_caso_promedio and re.search(r'n/4', expr):
            terminos.append('(n/4)*C')
        else:
            terminos.append('n*C')
    
    # Logarítmico
    if re.search(r'log\d?\(n\)', expr, re.IGNORECASE):
        if re.search(r'log2?\(n\)/2', expr):
            terminos.append('(log(n)/2)*C')
        else:
            terminos.append('log(n)*C')
    
    # Construir resultado
    if not terminos:
        # Solo constantes
        return K
    
    # Tomar término dominante (el primero por orden de prioridad)
    termino_dominante = terminos[0]
    
    # Construir ecuación
    return f"{K} + {termino_dominante}"


def _preservar_ecuacion(cost_str: str, tipo_caso: str) -> str:
    """
    Preserva la ecuación original con ajustes mínimos.
    
    Solo reemplaza constantes numéricas explícitas por K.
    """
    import re
    
    K = 'K1' if tipo_caso == 'mejor' else ('K2' if tipo_caso == 'promedio' else 'K3')
    
    # Reemplazar constantes numéricas por c (coeficientes)
    # Mantener n y sus exponentes intactos
    expr = cost_str
    
    # Reemplazar números que no están como parte de n/2, n**2, etc.
    # Primero, proteger patrones importantes
    protegidos = []
    
    # Proteger n/número, n**número, log2, log10
    for match in re.finditer(r'(n/\d+|n\*\*\d+|log\d+|2\*\*n)', expr):
        placeholder = f"__PROT{len(protegidos)}__"
        protegidos.append(match.group())
        expr = expr.replace(match.group(), placeholder, 1)
    
    # Ahora reemplazar constantes numéricas aisladas
    expr = re.sub(r'\b\d+\b', 'c', expr)
    
    # Restaurar protegidos
    for i, prot in enumerate(protegidos):
        expr = expr.replace(f"__PROT{i}__", prot)
    
    # Si la ecuación tiene términos, agregar K al inicio
    if '+' in expr or '-' in expr:
        return f"{K} + {expr}"
    else:
        # Solo un término
        if any(var in expr for var in ['n', 'log', 'T(']):
            return f"{K} + {expr}"
        else:
            return K
