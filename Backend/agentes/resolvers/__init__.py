"""
Módulo de métodos de resolución de recurrencias.

Métodos disponibles:
- TeoremaMAestro: Para T(n) = aT(n/b) + f(n) [división uniforme estándar]
- MetodoSumas: Para T(n) = T(n-1) + f(n) [decrementación simple]
- MetodoIteracion: Para expansión y simplificación directa
- EcuacionCaracteristica: Para T(n) = a₁T(n-1) + a₂T(n-2) + ... [lineales múltiples]
- ArbolRecursion: Para T(n) = T(n/a) + T(n/b) + f(n) [división asimétrica/múltiple]
- AnalizadorDirecto: Para expresiones directas sin recurrencia [T(n) = K + n*C]
"""

from .base_resolver import BaseResolver
from .teorema_maestro import TeoremaMAestro
from .metodo_sumas import MetodoSumas
from .metodo_iteracion import MetodoIteracion
from .ecuacion_caracteristica import EcuacionCaracteristica
from .arbol_recursion import ArbolRecursion
from .analizador_directo import AnalizadorDirecto

__all__ = [
    'BaseResolver',
    'TeoremaMAestro',
    'MetodoSumas',
    'MetodoIteracion',
    'EcuacionCaracteristica',
    'ArbolRecursion',
    'AnalizadorDirecto',
]
