from .base_resolver import BaseResolver
import math
import re

class TeoremaMAestro(BaseResolver):
    """
    Implementa el Teorema Maestro para resolver recurrencias de la forma:
    T(n) = aT(n/b) + f(n)
    
    Casos:
    1. Si f(n) = O(n^c) donde c < log_b(a) → T(n) = Θ(n^log_b(a))
    2. Si f(n) = Θ(n^c log^k n) donde c = log_b(a) → T(n) = Θ(n^c log^(k+1) n)
    3. Si f(n) = Ω(n^c) donde c > log_b(a) y cumple regularidad → T(n) = Θ(f(n))
    """
    
    def puede_resolver(self, ecuacion):
        """
        Verifica si la ecuación tiene la forma T(n) = aT(n/b) + f(n)
        """
        if ecuacion.get('forma') == 'divide_conquista':
            # Verificar que a >= 1 y b > 1
            a = ecuacion.get('a', 0)
            b = ecuacion.get('b', 0)
            return a >= 1 and b > 1
        return False
    
    def resolver(self, ecuacion):
        """
        Resuelve usando el Teorema Maestro.
        
        Parámetros:
        - ecuacion: dict con 'a', 'b', 'f_n'
        """
        pasos = []
        
        # Extraer parámetros
        a = ecuacion['a']
        b = ecuacion['b']
        f_n_str = ecuacion['f_n']
        
        pasos.append(f"📝 Ecuación: T(n) = {a}T(n/{b}) + {f_n_str}")
        pasos.append(f"")
        pasos.append(f"🔹 PASO 1: Identificar parámetros")
        pasos.append(f"   a = {a} (número de subproblemas)")
        pasos.append(f"   b = {b} (factor de división)")
        pasos.append(f"   f(n) = {f_n_str} (trabajo extra)")
        
        # Calcular exponente crítico
        c = math.log(a) / math.log(b)
        pasos.append(f"")
        pasos.append(f"🔹 PASO 2: Calcular exponente crítico")
        pasos.append(f"   c = log_b(a) = log_{b}({a}) = {c:.4f}")
        
        # Analizar f(n)
        pasos.append(f"")
        pasos.append(f"🔹 PASO 3: Analizar f(n)")
        forma_fn = self._analizar_funcion(f_n_str)
        pasos.append(f"   f(n) = {f_n_str}")
        pasos.append(f"   Forma: {forma_fn['descripcion']}")
        
        # Determinar caso
        pasos.append(f"")
        pasos.append(f"🔹 PASO 4: Determinar caso del Teorema Maestro")
        
        caso_resultado = self._determinar_caso(a, b, c, forma_fn, pasos)
        
        if not caso_resultado:
            return self._crear_resultado(
                exito=False,
                explicacion="El Teorema Maestro no aplica para esta ecuación",
                pasos=pasos
            )
        
        # Construir explicación final
        explicacion = self._construir_explicacion(caso_resultado, a, b, c, f_n_str)
        
        return self._crear_resultado(
            exito=True,
            solucion=caso_resultado['solucion'],
            pasos=pasos,
            explicacion=explicacion,
            detalles={
                'caso': caso_resultado['numero'],
                'exponente_critico': c,
                'a': a,
                'b': b,
                'f_n': f_n_str
            }
        )
    
    def _analizar_funcion(self, f_n_str):
        """
        Analiza la función f(n) para determinar su forma.
        
        Retorna dict con:
        - tipo: 'constante', 'polinomial', 'polinomial_log', 'exponencial'
        - exponente: float (para polinomiales)
        - k_log: int (exponente de logaritmo)
        - descripcion: str
        """
        f_n = f_n_str.lower().replace(' ', '')
        
        # Constante
        if f_n.isdigit() or f_n == '1':
            return {
                'tipo': 'constante',
                'exponente': 0,
                'k_log': 0,
                'descripcion': 'constante (c)'
            }
        
        # n^k (polinomial)
        if 'log' not in f_n:
            if f_n == 'n':
                return {
                    'tipo': 'polinomial',
                    'exponente': 1,
                    'k_log': 0,
                    'descripcion': 'lineal (n)'
                }
            
            # n**2, n^2, etc.
            match = re.search(r'n\*\*(\d+\.?\d*)', f_n)
            if not match:
                match = re.search(r'n\^(\d+\.?\d*)', f_n)
            
            if match:
                exp = float(match.group(1))
                return {
                    'tipo': 'polinomial',
                    'exponente': exp,
                    'k_log': 0,
                    'descripcion': f'polinomial (n^{exp})'
                }
        
        # n^k * log^m(n)
        else:
            # n * log(n)
            if 'n*log(n)' in f_n or 'nlog(n)' in f_n or 'n*logn' in f_n:
                return {
                    'tipo': 'polinomial_log',
                    'exponente': 1,
                    'k_log': 1,
                    'descripcion': 'n·log(n)'
                }
            
            # log(n)
            if f_n == 'log(n)' or f_n == 'logn':
                return {
                    'tipo': 'polinomial_log',
                    'exponente': 0,
                    'k_log': 1,
                    'descripcion': 'logarítmica (log n)'
                }
            
            # n^2 * log(n)
            match = re.search(r'n\*?\*?(\d+).*log', f_n)
            if match:
                exp = float(match.group(1))
                return {
                    'tipo': 'polinomial_log',
                    'exponente': exp,
                    'k_log': 1,
                    'descripcion': f'n^{exp}·log(n)'
                }
        
        # Por defecto, asumir lineal
        return {
            'tipo': 'desconocido',
            'exponente': 1,
            'k_log': 0,
            'descripcion': f_n_str
        }
    
    def _determinar_caso(self, a, b, c, forma_fn, pasos):
        """
        Determina cuál de los 3 casos del Teorema Maestro aplica.
        """
        exp = forma_fn['exponente']
        k_log = forma_fn['k_log']
        
        epsilon = 0.001  # Tolerancia para comparaciones
        
        pasos.append(f"   Comparando exponentes:")
        pasos.append(f"   - Exponente de f(n): {exp}")
        pasos.append(f"   - Exponente crítico c: {c:.4f}")
        pasos.append(f"")
        
        # CASO ESPECIAL: a = 1 (un solo subproblema)
        if a == 1:
            pasos.append(f"   ⚠️  Caso especial: a = 1 (un solo subproblema)")
            pasos.append(f"   Con un solo subproblema, hay log_{b}(n) niveles")
            pasos.append(f"   y cada nivel hace trabajo f(n)")
            pasos.append(f"")
            
            if forma_fn['tipo'] == 'constante':
                pasos.append(f"   Como f(n) = {forma_fn['descripcion']} es constante:")
                pasos.append(f"   Trabajo total = f(n) · log_{b}(n)")
                pasos.append(f"   T(n) = Θ(log n)")
                pasos.append(f"")
                
                return {
                    'numero': 'especial_log',
                    'solucion': 'log(n)'
                }
            else:
                pasos.append(f"   Como f(n) = {forma_fn['descripcion']}:")
                pasos.append(f"   Cada nivel hace O(f(n)) y hay log_{b}(n) niveles")
                pasos.append(f"   T(n) = Θ(f(n) · log n)")
                pasos.append(f"")
                
                # Construir solución
                if forma_fn['tipo'] == 'lineal':
                    sol_str = "n log n"
                elif forma_fn['tipo'] == 'cuadratico':
                    sol_str = "n² log n"
                elif forma_fn['tipo'] == 'cubico':
                    sol_str = "n³ log n"
                else:
                    sol_str = f"n^{exp} log n"
                
                return {
                    'numero': 'especial_fn_log',
                    'solucion': sol_str
                }
        
        # CASO 1: f(n) = O(n^(c-ε))
        if exp < c - epsilon and k_log == 0:
            pasos.append(f"   ✓ {exp} < {c:.4f}")
            pasos.append(f"   → CASO 1: f(n) es polinomialmente menor que n^{c:.4f}")
            pasos.append(f"")
            pasos.append(f"🔹 PASO 5: Aplicar Caso 1")
            pasos.append(f"   T(n) = Θ(n^log_b(a))")
            pasos.append(f"   T(n) = Θ(n^{c:.4f})")
            
            # Simplificar si c es entero
            if abs(c - round(c)) < epsilon:
                c_int = int(round(c))
                solucion_str = f"n^{c_int}" if c_int > 1 else "n"
            else:
                solucion_str = f"n^{c:.4f}"
            
            return {
                'numero': 1,
                'solucion': solucion_str
            }
        
        # CASO 2: f(n) = Θ(n^c * log^k n)
        elif abs(exp - c) < epsilon:
            pasos.append(f"   ✓ {exp} ≈ {c:.4f}")
            pasos.append(f"   → CASO 2: f(n) = Θ(n^{c:.4f} · log^{k_log}(n))")
            pasos.append(f"")
            pasos.append(f"🔹 PASO 5: Aplicar Caso 2")
            pasos.append(f"   T(n) = Θ(n^c · log^(k+1)(n))")
            
            # Simplificar notación
            if abs(c - round(c)) < epsilon:
                c_int = int(round(c))
                base = f"n^{c_int}" if c_int > 1 else "n"
            else:
                base = f"n^{c:.4f}"
            
            if k_log == 0:
                solucion_str = f"{base} log n"
            else:
                solucion_str = f"{base} log^{k_log + 1} n"
            
            pasos.append(f"   T(n) = Θ({solucion_str})")
            
            return {
                'numero': 2,
                'solucion': solucion_str,
                'k': k_log
            }
        
        # CASO 3: f(n) = Ω(n^(c+ε))
        elif exp > c + epsilon and k_log == 0:
            pasos.append(f"   ✓ {exp} > {c:.4f}")
            pasos.append(f"   → CASO 3: f(n) es polinomialmente mayor que n^{c:.4f}")
            pasos.append(f"")
            
            # Verificar condición de regularidad
            regular = self._verificar_regularidad(a, b, exp)
            
            if regular:
                pasos.append(f"   ✓ Condición de regularidad: a·f(n/b) ≤ c·f(n) para c < 1")
                pasos.append(f"     {a} · (n/{b})^{exp} ≤ c · n^{exp}")
                pasos.append(f"     {a}/{b**exp:.4f} ≤ c < 1 ✓")
                pasos.append(f"")
                pasos.append(f"🔹 PASO 5: Aplicar Caso 3")
                pasos.append(f"   T(n) = Θ(f(n))")
                
                # Formatear f(n)
                if exp == 1:
                    fn_str = "n"
                elif abs(exp - round(exp)) < epsilon:
                    fn_str = f"n^{int(round(exp))}"
                else:
                    fn_str = f"n^{exp}"
                
                pasos.append(f"   T(n) = Θ({fn_str})")
                
                return {
                    'numero': 3,
                    'solucion': fn_str
                }
            else:
                pasos.append(f"   ✗ NO cumple condición de regularidad")
                pasos.append(f"     {a}/{b**exp:.4f} ≥ 1")
                return None
        
        else:
            pasos.append(f"   ✗ No se puede determinar el caso")
            pasos.append(f"     (posiblemente f(n) tiene forma no estándar)")
            return None
    
    def _verificar_regularidad(self, a, b, exp):
        """
        Verifica la condición de regularidad del Caso 3:
        a · f(n/b) ≤ c · f(n) para alguna constante c < 1
        
        Para f(n) = n^exp, esto se simplifica a: a/b^exp < 1
        """
        return (a / (b ** exp)) < 1
    
    def _construir_explicacion(self, caso_resultado, a, b, c, f_n_str):
        """
        Construye una explicación detallada del resultado.
        """
        caso_num = caso_resultado['numero']
        solucion = caso_resultado['solucion']
        
        explicaciones = {
            1: f"""
╔══════════════════════════════════════════════════════════════╗
║                    TEOREMA MAESTRO - CASO 1                  ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {a}T(n/{b}) + {f_n_str}

Exponente crítico: c = log_{b}({a}) = {c:.4f}

CASO 1 APLICA porque:
  f(n) es polinomialmente MENOR que n^{c:.4f}
  
  Esto significa que el trabajo en las llamadas recursivas
  DOMINA sobre el trabajo adicional f(n).

SOLUCIÓN: {solucion}

El costo está dominado por el número de nodos en el árbol
de recursión, que crece como n^{c:.4f}.
""",
            2: f"""
╔══════════════════════════════════════════════════════════════╗
║                    TEOREMA MAESTRO - CASO 2                  ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {a}T(n/{b}) + {f_n_str}

Exponente crítico: c = log_{b}({a}) = {c:.4f}

CASO 2 APLICA porque:
  f(n) tiene el MISMO orden que n^{c:.4f}
  
  El trabajo en cada nivel del árbol de recursión es
  aproximadamente igual, y hay log(n) niveles.

SOLUCIÓN: {solucion}

El factor logarítmico adicional viene de sumar el trabajo
de todos los niveles del árbol de recursión.
""",
            3: f"""
╔══════════════════════════════════════════════════════════════╗
║                    TEOREMA MAESTRO - CASO 3                  ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {a}T(n/{b}) + {f_n_str}

Exponente crítico: c = log_{b}({a}) = {c:.4f}

CASO 3 APLICA porque:
  f(n) es polinomialmente MAYOR que n^{c:.4f}
  Y cumple la condición de regularidad
  
  El trabajo adicional f(n) DOMINA sobre el trabajo
  en las llamadas recursivas.

SOLUCIÓN: {solucion}

El costo está dominado por el trabajo en la raíz del
árbol de recursión.
"""
        }
        
        return explicaciones.get(caso_num, f"Solución: {solucion}")