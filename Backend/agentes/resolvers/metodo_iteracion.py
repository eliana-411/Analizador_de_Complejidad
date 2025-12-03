from .base_resolver import BaseResolver
import re

class MetodoIteracion(BaseResolver):
    """
    Método de Iteración (Unwinding/Expansion) para resolver recurrencias.
    
    Funciona expandiendo la recurrencia k veces hasta encontrar un patrón,
    luego generalizando y sumando.
    
    Puede resolver:
    - T(n) = aT(n/b) + f(n)
    - T(n) = T(n-c) + f(n)
    - T(n) = aT(n-c) + f(n)
    """
    
    def puede_resolver(self, ecuacion):
        """
        El método de iteración funciona para formas estándar, pero no para asimétricas.
        """
        forma = ecuacion.get('forma')
        
        # Rechazar casos asimétricos o con múltiples términos
        if ecuacion.get('es_asimetrico') or ecuacion.get('terminos_multiples'):
            return False
        
        return forma in ['divide_conquista', 'decrementacion', 'decrementacion_multiple']
    
    def resolver(self, ecuacion):
        """
        Resuelve por iteración según la forma.
        """
        forma = ecuacion['forma']
        
        if forma == 'divide_conquista':
            return self._resolver_divide_conquista(ecuacion)
        elif forma == 'decrementacion':
            return self._resolver_decrementacion(ecuacion)
        elif forma == 'decrementacion_multiple':
            return self._resolver_decrementacion_multiple(ecuacion)
        
        return self._crear_resultado(
            exito=False,
            explicacion="Forma de ecuación no soportada por el método de iteración"
        )
    
    def _resolver_divide_conquista(self, ecuacion):
        """
        Resuelve T(n) = aT(n/b) + f(n) por iteración.
        """
        pasos = []
        a = ecuacion['a']
        b = ecuacion['b']
        f_n = ecuacion['f_n']
        
        pasos.append(f"📝 Ecuación: T(n) = {a}T(n/{b}) + {f_n}")
        pasos.append(f"")
        pasos.append(f"🔹 MÉTODO DE ITERACIÓN")
        pasos.append(f"   Expandiremos la recurrencia k veces hasta encontrar el patrón")
        pasos.append(f"")
        
        # Iteración 0
        pasos.append(f"🔹 Iteración 0:")
        pasos.append(f"   T(n) = {a}T(n/{b}) + {f_n}")
        pasos.append(f"")
        
        # Iteración 1
        pasos.append(f"🔹 Iteración 1:")
        pasos.append(f"   Sustituir T(n/{b}) = {a}T(n/{b}²) + f(n/{b})")
        pasos.append(f"   T(n) = {a}[{a}T(n/{b}²) + f(n/{b})] + {f_n}")
        pasos.append(f"   T(n) = {a}²T(n/{b}²) + {a}·f(n/{b}) + {f_n}")
        pasos.append(f"")
        
        # Iteración 2
        pasos.append(f"🔹 Iteración 2:")
        pasos.append(f"   Sustituir T(n/{b}²) = {a}T(n/{b}³) + f(n/{b}²)")
        pasos.append(f"   T(n) = {a}²[{a}T(n/{b}³) + f(n/{b}²)] + {a}·f(n/{b}) + {f_n}")
        pasos.append(f"   T(n) = {a}³T(n/{b}³) + {a}²·f(n/{b}²) + {a}·f(n/{b}) + {f_n}")
        pasos.append(f"")
        
        # Patrón general
        pasos.append(f"🔹 Patrón después de k iteraciones:")
        pasos.append(f"   T(n) = {a}^k · T(n/{b}^k) + Σ({a}^i · f(n/{b}^i)) para i=0 hasta k-1")
        pasos.append(f"")
        
        # Condición de parada
        pasos.append(f"🔹 Condición de parada:")
        pasos.append(f"   Cuando n/{b}^k = 1")
        pasos.append(f"   → k = log_b(n)")
        pasos.append(f"")
        
        # Simplificar
        forma_fn = self._analizar_funcion_simple(f_n)
        pasos.append(f"🔹 Evaluar en k = log_b(n):")
        pasos.append(f"   T(n) = {a}^(log_b(n)) · T(1) + Σ({a}^i · f(n/{b}^i))")
        pasos.append(f"")
        pasos.append(f"   Nota: {a}^(log_b(n)) = n^(log_b({a}))")
        
        # Calcular solución aproximada
        c = self._calcular_log(a, b)
        pasos.append(f"   log_{b}({a}) ≈ {c:.3f}")
        pasos.append(f"")
        
        # Determinar dominancia
        if forma_fn['tipo'] == 'constante':
            pasos.append(f"   Como f(n) = {f_n} es constante:")
            pasos.append(f"   La suma geométrica resulta en un término polinomial")
            pasos.append(f"")
            pasos.append(f"   T(n) = n^(log_{b}({a})) · T(1) + O(n^{c:.3f})")
            pasos.append(f"   Asumiendo T(1) = c (constante):")
            if abs(c - round(c)) < 0.01:
                c_int = int(round(c))
                pasos.append(f"   Fórmula cerrada: T(n) = c·n^{c_int} + término_suma")
                solucion = f"c·n^{c_int} + término_suma" if c_int > 1 else "c·n + término_suma"
            else:
                pasos.append(f"   Fórmula cerrada: T(n) = c·n^{c:.3f} + término_suma")
                solucion = f"c·n^{c:.3f} + término_suma"
        elif forma_fn['tipo'] == 'lineal':
            if abs(c - 1) < 0.01:
                pasos.append(f"   Como f(n) = n y log_{b}({a}) ≈ 1:")
                pasos.append(f"   Suma de niveles: n + n + ... (log n niveles)")
                pasos.append(f"")
                pasos.append(f"   T(n) = n·T(1) + n·log_{b}(n)")
                pasos.append(f"   Asumiendo T(1) = c (constante):")
                pasos.append(f"   Fórmula cerrada: T(n) = c·n + n·log_{b}(n)")
                solucion = f"c·n + n·log_{b}(n)"
            elif c < 1:
                pasos.append(f"   Como f(n) = n domina sobre n^{c:.3f}:")
                pasos.append(f"")
                pasos.append(f"   T(n) ≈ n^{c:.3f}·T(1) + suma(término lineal)")
                pasos.append(f"   Asumiendo T(1) = c (constante):")
                pasos.append(f"   Fórmula cerrada: T(n) ≈ c·n^{c:.3f} + O(n)")
                solucion = f"c·n^{c:.3f} + O(n)"
            else:
                pasos.append(f"   Como n^{c:.3f} domina sobre f(n) = n:")
                pasos.append(f"")
                pasos.append(f"   T(n) ≈ n^{c:.3f}·T(1) + O(n)")
                pasos.append(f"   Asumiendo T(1) = c (constante):")
                pasos.append(f"   Fórmula cerrada: T(n) ≈ c·n^{c:.3f} + término_menor")
                solucion = f"c·n^{c:.3f} + término_menor"
        else:
            if abs(c - round(c)) < 0.01:
                c_int = int(round(c))
                solucion = f"c·n^{c_int}"
            else:
                solucion = f"c·n^{c:.3f}"
        
        explicacion = f"""
╔══════════════════════════════════════════════════════════════╗
║                   MÉTODO DE ITERACIÓN                        ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {a}T(n/{b}) + {f_n}

ESTRATEGIA:
  1. Expandir la recurrencia repetidamente
  2. Identificar el patrón general
  3. Determinar cuántas iteraciones hasta caso base
  4. Evaluar la suma resultante

SOLUCIÓN (Fórmula Cerrada): T(n) = {solucion}

Nota: 'c' representa la condición base T(1), asumida constante.
Para la complejidad asintótica (Θ, O, Ω), otro agente analizará esta fórmula.
"""
        
        return self._crear_resultado(
            exito=True,
            solucion=solucion,
            pasos=pasos,
            explicacion=explicacion
        )
    
    def _resolver_decrementacion(self, ecuacion):
        """
        Resuelve T(n) = T(n-c) + f(n) por iteración.
        """
        pasos = []
        c = ecuacion['c']
        f_n = ecuacion['f_n']
        
        pasos.append(f"📝 Ecuación: T(n) = T(n-{c}) + {f_n}")
        pasos.append(f"")
        pasos.append(f"🔹 MÉTODO DE ITERACIÓN")
        pasos.append(f"")
        
        # Expandir
        pasos.append(f"🔹 Iteración 0:")
        pasos.append(f"   T(n) = T(n-{c}) + f(n)")
        pasos.append(f"")
        
        pasos.append(f"🔹 Iteración 1:")
        pasos.append(f"   T(n) = [T(n-{2*c}) + f(n-{c})] + f(n)")
        pasos.append(f"   T(n) = T(n-{2*c}) + f(n-{c}) + f(n)")
        pasos.append(f"")
        
        pasos.append(f"🔹 Patrón después de k iteraciones:")
        pasos.append(f"   T(n) = T(n-k·{c}) + Σ f(n-i·{c}) para i=0 hasta k-1")
        pasos.append(f"")
        
        pasos.append(f"🔹 Cuando n-k·{c} = 0 → k = n/{c}")
        pasos.append(f"   T(n) = T(0) + Σ f(i) para i=0 hasta n (por pasos de {c})")
        pasos.append(f"")
        
        # Este caso se reduce a método de sumas
        pasos.append(f"   Nota: Este caso se resuelve mejor con el Método de Sumas")
        
        return self._crear_resultado(
            exito=True,
            solucion="Ver Método de Sumas",
            pasos=pasos,
            explicacion="El Método de Iteración muestra que esto se reduce a una suma. Use el Método de Sumas para obtener la solución exacta."
        )
    
    def _resolver_decrementacion_multiple(self, ecuacion):
        """
        Resuelve T(n) = aT(n-c) + f(n) por iteración.
        """
        pasos = []
        a = ecuacion['a']
        c = ecuacion['c']
        f_n = ecuacion['f_n']
        
        pasos.append(f"📝 Ecuación: T(n) = {a}T(n-{c}) + {f_n}")
        pasos.append(f"")
        pasos.append(f"🔹 MÉTODO DE ITERACIÓN")
        pasos.append(f"   (Decrementación con múltiples subproblemas)")
        pasos.append(f"")
        
        # Este caso es más complejo, mejor usar ecuaciones características
        pasos.append(f"   Nota: Este tipo de recurrencia se resuelve mejor")
        pasos.append(f"   usando el método de Ecuaciones Características")
        
        return self._crear_resultado(
            exito=True,
            solucion="Ver Ecuaciones Características",
            pasos=pasos,
            explicacion="Use el método de Ecuaciones Características para resolver esta recurrencia lineal."
        )
    
    def _analizar_funcion_simple(self, f_n_str):
        """Análisis simple de f(n)"""
        f_n = f_n_str.lower().replace(' ', '')
        
        if f_n.isdigit() or f_n == '1':
            return {'tipo': 'constante'}
        elif f_n == 'n':
            return {'tipo': 'lineal'}
        else:
            return {'tipo': 'otro'}
    
    def _calcular_log(self, a, b):
        """Calcula log_b(a)"""
        import math
        return math.log(a) / math.log(b)