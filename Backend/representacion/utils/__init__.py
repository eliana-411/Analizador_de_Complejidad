"""
Utilidades para el Agente de Representación Matemática.

Exporta herramientas para comparación de costos y formateo de ecuaciones.
"""

from .cost_comparator import complejidad_numerica
from .equation_formatter import simplificar_con_constantes, format_for_resolver

__all__ = [
    "complejidad_numerica",
    "simplificar_con_constantes",
    "format_for_resolver",
]
