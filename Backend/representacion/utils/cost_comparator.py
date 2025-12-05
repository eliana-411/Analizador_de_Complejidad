"""
Comparador de Complejidades.

Provee heurísticas para comparar costos sin evaluación numérica directa.
Usado para identificar mejor y peor caso en algoritmos iterativos.
"""

import re


def complejidad_numerica(cost_str: str) -> float:
    """
    Heurística para comparar costos basada en orden de complejidad asintótica.
    
    Retorna un valor numérico aproximado que representa el orden de magnitud
    de la complejidad para n grande. Esto permite comparar costos sin
    evaluarlos numéricamente.
    
    Jerarquía de complejidades (menor a mayor):
    1. Constante: O(1)
    2. Logarítmica: O(log n)
    3. Lineal: O(n)
    4. Lineal-logarítmica: O(n log n)
    5. Cuadrática: O(n²)
    6. Cúbica: O(n³)
    7. Exponencial: O(2^n)
    8. Factorial: O(n!)
    
    Args:
        cost_str: Expresión de costo como string (ej: "4*n + 2", "n**2", "log(n)")
    
    Returns:
        float: Valor numérico aproximado del orden de complejidad
    
    Examples:
        >>> complejidad_numerica("6")
        6.0
        >>> complejidad_numerica("4*n + 2")
        400.0
        >>> complejidad_numerica("n**2")
        10000.0
        >>> complejidad_numerica("2*n + 3")
        200.0
    """
    # Normalizar: minúsculas, sin espacios
    cost = cost_str.lower().replace(' ', '')
    
    # Orden 8: Factorial O(n!)
    if 'n!' in cost or 'factorial' in cost:
        return 1e10
    
    # Orden 7: Exponencial O(2^n)
    if '2**n' in cost or '2^n' in cost or 'exp' in cost:
        return 1e8
    
    # Orden 6: Cúbico O(n³)
    if 'n**3' in cost or 'n³' in cost or 'n^3' in cost:
        return 1e6
    
    # Orden 5: Cuadrático O(n²)
    if 'n**2' in cost or 'n²' in cost or 'n^2' in cost:
        return 1e4
    
    # Orden 4: Lineal-logarítmico O(n log n)
    if ('n*log' in cost or 'nlog' in cost or 
        'n*ln' in cost or 'nln' in cost):
        return 1e3
    
    # Orden 3: Lineal O(n)
    if 'n' in cost:
        # Extraer coeficiente si es explícito (ej: "4*n" → 4)
        match = re.search(r'(\d+)\*n', cost)
        if match:
            coef = int(match.group(1))
            return coef * 100
        
        # Detectar fracciones como n/2
        if 'n/2' in cost or '0.5*n' in cost:
            return 50  # Menor que n completo
        
        return 100  # Lineal genérico
    
    # Orden 2: Logarítmico O(log n)
    if 'log' in cost or 'ln' in cost:
        return 10
    
    # Orden 1: Constante O(1)
    # Intentar parsear como número
    try:
        # Remover operadores para obtener la magnitud aproximada
        # Ej: "4 + 2" → evaluar como constante
        if '+' in cost or '-' in cost:
            # Es suma/resta de constantes
            return float(eval(cost.replace('k', '1')))  # Reemplazar variables por 1
        return float(cost)
    except:
        # Si no se puede parsear, asumir constante pequeña
        return 1.0


def es_constante(cost_str: str) -> bool:
    """
    Verifica si una expresión de costo es constante (no depende de n).
    
    Args:
        cost_str: Expresión de costo como string
    
    Returns:
        bool: True si es constante (O(1)), False en caso contrario
    
    Examples:
        >>> es_constante("6")
        True
        >>> es_constante("4*n + 2")
        False
        >>> es_constante("log(n)")
        False
    """
    cost = cost_str.lower().replace(' ', '')
    
    # Si contiene 'n' o 'log', no es constante
    if 'n' in cost or 'log' in cost:
        return False
    
    # Si se puede evaluar como número, es constante
    try:
        float(cost)
        return True
    except:
        return False


def es_lineal(cost_str: str) -> bool:
    """
    Verifica si una expresión de costo es lineal O(n).
    
    Args:
        cost_str: Expresión de costo como string
    
    Returns:
        bool: True si es lineal, False en caso contrario
    
    Examples:
        >>> es_lineal("4*n + 2")
        True
        >>> es_lineal("n**2")
        False
        >>> es_lineal("n")
        True
    """
    cost = cost_str.lower().replace(' ', '')
    
    # Tiene n pero no n^2, n^3, n*log, etc.
    if 'n' in cost:
        if ('n**2' in cost or 'n²' in cost or 'n^2' in cost or
            'n**3' in cost or 'n³' in cost or 'n^3' in cost or
            'log' in cost):
            return False
        return True
    
    return False
