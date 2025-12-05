"""
Procesadores para el Agente de Representación Matemática.

Exporta procesadores especializados para algoritmos iterativos y recursivos.
"""

from .esperanza_calculator import calculate_expected_value
from .iterative_processor import process_iterative
from .recursive_processor import process_recursive

__all__ = [
    "calculate_expected_value",
    "process_iterative",
    "process_recursive",
]
