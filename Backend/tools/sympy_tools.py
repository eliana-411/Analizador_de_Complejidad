"""
SymPy Tools - Herramientas para Manipulacion Matematica
========================================================

Proposito:
    Proporcionar funciones utilitarias para trabajar con expresiones matematicas
    usando SymPy. Estas tools son usadas principalmente por el Agente de
    Representacion Matematica para convertir descripciones textuales de costos
    en ecuaciones formales.

Funcionalidades:
    1. sympy_expression_builder: Valida y convierte expresiones a SymPy
    2. series_generator: Genera representaciones de series matematicas

Uso:
    from tools.sympy_tools import sympy_expression_builder, series_generator

    result = sympy_expression_builder("n**2 + 2*n + 1")
    if result["is_valid"]:
        print(result["sympy_expr"])
"""

from sympy import symbols, sympify, simplify, Sum, summation, SympifyError
from typing import Dict, Any, Optional


def sympy_expression_builder(expression: str) -> Dict[str, Any]:
    n = symbols('n', positive=True, integer=True)
    T = symbols('T', cls=type)

    try:
        expr = sympify(expression, locals={'n': n, 'T': T})
        simplified = simplify(expr)

        return {
            "is_valid": True,
            "sympy_expr": str(expr),
            "simplified": str(simplified),
            "latex": None,
            "error": None
        }
    except (SympifyError, Exception) as e:
        return {
            "is_valid": False,
            "sympy_expr": None,
            "simplified": None,
            "latex": None,
            "error": str(e)
        }


def series_generator(pattern: str, start: int, end: str, variable: str = "i") -> Dict[str, Any]:
    try:
        n = symbols('n', positive=True, integer=True)
        i = symbols(variable, integer=True)

        pattern_expr = sympify(pattern, locals={'i': i, 'n': n})

        end_symbol = sympify(end, locals={'n': n})

        series = Sum(pattern_expr, (i, start, end_symbol))

        try:
            closed_form = summation(pattern_expr, (i, start, end_symbol))
            closed_form_str = str(simplify(closed_form))
        except:
            closed_form_str = None

        return {
            "is_valid": True,
            "series_notation": str(series),
            "closed_form": closed_form_str,
            "pattern": str(pattern_expr),
            "error": None
        }
    except Exception as e:
        return {
            "is_valid": False,
            "series_notation": None,
            "closed_form": None,
            "pattern": None,
            "error": str(e)
        }


def validate_equation_syntax(equation: str) -> Dict[str, Any]:
    n = symbols('n', positive=True, integer=True)

    common_replacements = {
        '^': '**',
        '×': '*',
        '÷': '/',
        '²': '**2',
        '³': '**3',
    }

    cleaned = equation
    for old, new in common_replacements.items():
        cleaned = cleaned.replace(old, new)

    result = sympy_expression_builder(cleaned)

    if result["is_valid"]:
        result["original_equation"] = equation
        result["cleaned_equation"] = cleaned

    return result