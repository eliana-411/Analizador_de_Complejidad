from .base_resolver import BaseResolver
import re

class MetodoSumas(BaseResolver):
    """
    Método de Sumas para resolver recurrencias de la forma:
    T(n) = T(n-1) + f(n)
    
    Solución: T(n) = T(0) + Σ f(i) para i=1 hasta n
    
    Sumas conocidas:
    - Σ 1 = n
    - Σ i = n(n+1)/2
    - Σ i² = n(n+1)(2n+1)/6
    - Σ i³ = [n(n+1)/2]²
    - Σ 2^i = 2^(n+1) - 1
    - Σ c = c·n (constante)
    """
    
    def puede_resolver(self, ecuacion):
        """
        Ahora permite decrementos de cualquier k: T(n) = T(n-k) + f(n)
        """
        return ecuacion.get('forma') == 'decrementacion' and ecuacion.get('c', 0) >= 1
    
    def resolver(self, ecuacion):
        """
        Resuelve usando el método de sumas para cualquier decremento k.
        T(n) = T(n-k) + f(n)
        T(n) = T(n-2) + f(n) + f(n-2) + ...
        T(n) = T(0) + sumatoria f(i) para i=0 hasta n en pasos de k
        """
        pasos = []
        f_n_str = ecuacion['f_n']
        k = ecuacion.get('c', 1)
        pasos.append(f"📝 Ecuación: T(n) = T(n-{k}) + {f_n_str}")
        pasos.append(f"")
        pasos.append(f"🔹 MÉTODO DE SUMAS")
        pasos.append(f"   Para recurrencias de la forma T(n) = T(n-{k}) + f(n)")
        if k == 1:
            pasos.append(f"   La solución es: T(n) = T(0) + Σ f(i) para i=1 hasta n")
        else:
            pasos.append(f"   La solución es: T(n) = T(0) + Σ f(i) para i=0 hasta n en pasos de {k}")
        pasos.append(f"")
        # Expandir algunos términos para ilustrar
        pasos.append(f"🔹 PASO 1: Expandir la recurrencia")
        if k == 1:
            pasos.append(f"   T(n) = T(n-1) + {f_n_str}")
            pasos.append(f"   T(n) = [T(n-2) + f(n-1)] + {f_n_str}")
            pasos.append(f"   T(n) = T(n-2) + f(n-1) + f(n)")
            pasos.append(f"   T(n) = [T(n-3) + f(n-2)] + f(n-1) + f(n)")
            pasos.append(f"   ...")
            pasos.append(f"   T(n) = T(0) + f(1) + f(2) + ... + f(n)")
        else:
            pasos.append(f"   T(n) = T(n-{k}) + f(n)")
            pasos.append(f"   T(n) = [T(n-2*{k}) + f(n-{k})] + f(n)")
            pasos.append(f"   T(n) = T(n-2*{k}) + f(n-{k}) + f(n)")
            pasos.append(f"   ...")
            pasos.append(f"   T(n) = T(0) + f({k}) + f(2*{k}) + ... + f(n)")
        pasos.append(f"")
        # Identificar la forma de f(n)
        pasos.append(f"🔹 PASO 2: Identificar la suma Σ f(i)")
        forma = self._identificar_forma_funcion(f_n_str)
        pasos.append(f"   f(n) = {f_n_str}")
        pasos.append(f"   Forma: {forma['descripcion']}")
        pasos.append(f"")
        # Resolver la suma
        pasos.append(f"🔹 PASO 3: Calcular la suma")
        resultado_suma = self._resolver_suma_k(forma, pasos, k)
        if not resultado_suma:
            return self._crear_resultado(
                exito=False,
                explicacion=f"No se pudo resolver la suma de {f_n_str}",
                pasos=pasos
            )
        # Construir explicación
        explicacion = self._construir_explicacion(f_n_str, resultado_suma)
        solucion_exacta = resultado_suma['solucion']
        solucion_simplificada = self._simplificar_asintotico(solucion_exacta)

        return self._crear_resultado(
            exito=True,
            solucion=solucion_simplificada,
            pasos=pasos,
            explicacion=explicacion,
            detalles={
                'forma_fn': forma,
                'suma': resultado_suma['suma_expr'],
                'solucion_exacta': solucion_exacta,
                'solucion_simplificada': solucion_simplificada
            }
        )

    def _resolver_suma_k(self, forma, pasos, k):
        """
        Resuelve la suma para decremento k: suma de f(i) para i=0 hasta n en pasos de k.
        Implementado para f(n) constante y f(n) lineal con coeficiente (c*n, k*n, 2*n, etc.) para k=1.
        """
        tipo = forma['tipo']
        # Constante
        if tipo == 'constante':
            c = forma.get('valor', 1)
            pasos.append(f"   Σ {c} para i=0 hasta n en pasos de {k}")
            pasos.append(f"   Hay (n//{k} + 1) términos")
            pasos.append(f"   = {c} · (n//{k} + 1)")
            pasos.append(f"")
            pasos.append(f"   T(n) = T(0) + {c}·(n//{k} + 1)")
            pasos.append(f"   Asumiendo T(0) = c (constante):")
            pasos.append(f"   Fórmula cerrada: T(n) = {c}·(n//{k} + 1) + c")
            pasos.append(f"")
            return {
                'suma_expr': f"{c}(n/{k} + 1)",
                'solucion': f"{c}(n/{k} + 1) + c"
            }
        # Lineal con coeficiente, solo para k=1
        if tipo == 'lineal' and k == 1:
            coef = forma.get('coef', 1)
            pasos.append(f"   Σ {coef}·i para i=1 hasta n")
            pasos.append(f"   = {coef}·n(n+1)/2")
            pasos.append(f"   = ({coef})·(n² + n)/2")
            pasos.append(f"")
            pasos.append(f"   T(n) = T(0) + {coef}·n(n+1)/2")
            pasos.append(f"   Asumiendo T(0) = c (constante):")
            pasos.append(f"   Fórmula cerrada: T(n) = {coef}·n(n+1)/2 + c")
            pasos.append(f"")
            return {
                'suma_expr': f"{coef}n(n+1)/2",
                'solucion': f"{coef}n(n+1)/2 + c"
            }
        pasos.append(f"   ⚠️  Solo se implementa suma cerrada para f(n) constante y decremento k, o f(n) lineal con k=1")
        pasos.append(f"")
        return None
    
    def _identificar_forma_funcion(self, f_n_str):
        """
        Identifica la forma de f(n) para saber qué suma aplicar.
        Extiende para reconocer coeficientes simbólicos o numéricos: c*n, k*n, 2*n, etc.
        """
        f_n = f_n_str.lower().replace(' ', '')
        # Constante numérica
        if f_n.isdigit():
            c = int(f_n)
            return {
                'tipo': 'constante',
                'valor': c,
                'descripcion': f'constante ({c})'
            }
        # Constante simbólica (letra simple, como c, k, etc.)
        if re.fullmatch(r'[a-zA-Z]', f_n):
            return {
                'tipo': 'constante',
                'valor': f_n,
                'descripcion': f'constante simbólica ({f_n})'
            }
        if f_n == '1':
            return {
                'tipo': 'constante',
                'valor': 1,
                'descripcion': 'constante (1)'
            }
        # n (lineal)
        if f_n == 'n':
            return {
                'tipo': 'lineal',
                'coef': 1,
                'exponente': 1,
                'descripcion': 'lineal (n)'
            }
        # c*n, k*n, 2*n, etc. (lineal con coeficiente)
        match_lineal = re.fullmatch(r'([a-zA-Z0-9]+)\*?n', f_n)
        if match_lineal:
            coef = match_lineal.group(1)
            # Si el coeficiente es solo '1', tratar como n
            if coef == '1':
                coef = 1
            return {
                'tipo': 'lineal',
                'coef': coef,
                'exponente': 1,
                'descripcion': f'lineal ({coef}·n)'
            }
        
        # n**2 o n^2
        if 'n**2' in f_n or 'n^2' in f_n:
            return {
                'tipo': 'cuadratico',
                'exponente': 2,
                'descripcion': 'cuadrático (n²)'
            }
        
        # n**3 o n^3
        if 'n**3' in f_n or 'n^3' in f_n:
            return {
                'tipo': 'cubico',
                'exponente': 3,
                'descripcion': 'cúbico (n³)'
            }
        
        # n**k (general)
        match = re.search(r'n\*\*(\d+)', f_n)
        if not match:
            match = re.search(r'n\^(\d+)', f_n)
        
        if match:
            exp = int(match.group(1))
            return {
                'tipo': 'polinomial',
                'exponente': exp,
                'descripcion': f'polinomial (n^{exp})'
            }
        
        # 2**n, 3**n, etc (exponencial)
        match = re.search(r'(\d+)\*\*n', f_n)
        if not match:
            match = re.search(r'(\d+)\^n', f_n)
        
        if match:
            base = int(match.group(1))
            return {
                'tipo': 'exponencial',
                'base': base,
                'descripcion': f'exponencial ({base}^n)'
            }
        
        # log(n)
        if 'log' in f_n:
            return {
                'tipo': 'logaritmico',
                'descripcion': 'logarítmico (log n)'
            }
        
        return {
            'tipo': 'desconocido',
            'descripcion': f_n_str
        }
    
    def _resolver_suma(self, forma, pasos):
        """
        Resuelve la suma según el tipo de función.
        """
        tipo = forma['tipo']
        
        # Σ c = c·n
        if tipo == 'constante':
            c = forma.get('valor', 1)
            pasos.append(f"   Σ {c} para i=1 hasta n")
            pasos.append(f"   = {c} · n")
            if c == 1:
                pasos.append(f"   = n")
            pasos.append(f"")
            pasos.append(f"   T(n) = T(0) + {c}n" if c != 1 else "   T(n) = T(0) + n")
            pasos.append(f"   Asumiendo T(0) = c (constante):")
            pasos.append(f"   Fórmula cerrada: T(n) = {c}n + c" if c != 1 else "   Fórmula cerrada: T(n) = n + c")
            pasos.append(f"")
            
            return {
                'suma_expr': f"{c}n" if c != 1 else "n",
                'solucion': f"{c}n + c" if c != 1 else "n + c"
            }
        
        # Σ i = n(n+1)/2 o Σ coef·i = coef·n(n+1)/2
        elif tipo == 'lineal':
            coef = forma.get('coef', 1)
            pasos.append(f"   Σ {coef}·i para i=1 hasta n" if coef != 1 else "   Σ i para i=1 hasta n")
            pasos.append(f"   = {coef}·n(n+1)/2" if coef != 1 else "   = n(n+1)/2")
            if coef != 1:
                pasos.append(f"   = ({coef})·(n² + n)/2")
            else:
                pasos.append(f"   = (n² + n)/2")
            pasos.append(f"")
            pasos.append(f"   T(n) = T(0) + {coef}·n(n+1)/2" if coef != 1 else "   T(n) = T(0) + n(n+1)/2")
            pasos.append(f"   Asumiendo T(0) = c (constante):")
            pasos.append(f"   Fórmula cerrada: T(n) = {coef}·n(n+1)/2 + c" if coef != 1 else "   Fórmula cerrada: T(n) = n(n+1)/2 + c")
            pasos.append(f"")
            return {
                'suma_expr': f"{coef}n(n+1)/2" if coef != 1 else "n(n+1)/2",
                'solucion': f"{coef}n(n+1)/2 + c" if coef != 1 else "n(n+1)/2 + c"
            }
        
        # Σ i² = n(n+1)(2n+1)/6
        elif tipo == 'cuadratico':
            pasos.append(f"   Σ i² para i=1 hasta n")
            pasos.append(f"   = n(n+1)(2n+1)/6")
            pasos.append(f"   ≈ 2n³/6 = n³/3")
            pasos.append(f"")
            pasos.append(f"   T(n) = T(0) + n(n+1)(2n+1)/6")
            pasos.append(f"   Asumiendo T(0) = c (constante):")
            pasos.append(f"   Fórmula cerrada: T(n) = n(n+1)(2n+1)/6 + c")
            pasos.append(f"")
            
            return {
                'suma_expr': "n(n+1)(2n+1)/6",
                'solucion': "n(n+1)(2n+1)/6 + c"
            }
        
        # Σ i³ = [n(n+1)/2]²
        elif tipo == 'cubico':
            pasos.append(f"   Σ i³ para i=1 hasta n")
            pasos.append(f"   = [n(n+1)/2]²")
            pasos.append(f"   ≈ n⁴/4")
            pasos.append(f"")
            pasos.append(f"   T(n) = T(0) + [n(n+1)/2]²")
            pasos.append(f"   Asumiendo T(0) = c (constante):")
            pasos.append(f"   Fórmula cerrada: T(n) = [n(n+1)/2]² + c")
            pasos.append(f"")
            
            return {
                'suma_expr': "[n(n+1)/2]²",
                'solucion': "[n(n+1)/2]² + c"
            }
        
        # Σ 2^i = 2^(n+1) - 1
        elif tipo == 'exponencial':
            base = forma.get('base', 2)
            pasos.append(f"   Σ {base}^i para i=1 hasta n")
            pasos.append(f"   = {base}^(n+1) - 1")
            pasos.append(f"")
            pasos.append(f"   T(n) = T(0) + {base}^(n+1) - 1")
            pasos.append(f"   Asumiendo T(0) = c (constante):")
            pasos.append(f"   Fórmula cerrada: T(n) = {base}^(n+1) + c - 1")
            pasos.append(f"   Simplificando: T(n) = {base}^(n+1) + c' (donde c' = c-1)")
            pasos.append(f"")
            
            return {
                'suma_expr': f"{base}^(n+1) - 1",
                'solucion': f"{base}^(n+1) + c"
            }
        
        # Σ log(i) ≈ n log(n)
        elif tipo == 'logaritmico':
            pasos.append(f"   Σ log(i) para i=1 hasta n")
            pasos.append(f"   ≈ n·log(n) - n·log(e) + O(log n)")
            pasos.append(f"   ≈ n·log(n)")
            pasos.append(f"")
            pasos.append(f"   T(n) ≈ T(0) + n·log(n)")
            pasos.append(f"   Asumiendo T(0) = c (constante):")
            pasos.append(f"   Fórmula cerrada (aproximada): T(n) ≈ n·log(n) + c")
            pasos.append(f"")
            
            return {
                'suma_expr': "n log n",
                'solucion': "n·log(n) + c"
            }
        
        # No se pudo resolver
        else:
            pasos.append(f"   ⚠️  No se tiene fórmula cerrada para esta suma")
            pasos.append(f"")
            return None
        
    def _simplificar_asintotico(self, expr: str) -> str:
        """
        Simplifica expresiones algebraicas típicas para obtener la notación O grande.
        Extiende para reconocer cuadráticas como n(n+1)/2, c·n(n+1)/2, n^2, etc.
        """
        if not expr:
            return expr

        original = expr
        expr = expr.replace(" ", "").lower()

        # Normalizar formatos raros
        expr = expr.replace("(n/1)", "n")
        expr = expr.replace("n/1", "n")
        expr = expr.replace("/1", "")

        # Cuadrático: n(n+1)/2, c*n(n+1)/2, n^2, n**2, etc.
        cuadratic_patterns = [
            r"n\(n\+1\)/2",           # n(n+1)/2
            r"[a-zA-Z0-9]+n\(n\+1\)/2", # c*n(n+1)/2, 2n(n+1)/2
            r"n\^2",                   # n^2
            r"n\*\*2",                 # n**2
            r"n\(n\+1\)",             # n(n+1)
        ]
        for pat in cuadratic_patterns:
            if re.search(pat, expr):
                return "n^2"

        # Cúbico: n(n+1)(2n+1)/6, n^3, n**3, etc.
        cubic_patterns = [
            r"n\(n\+1\)\(2n\+1\)/6", # n(n+1)(2n+1)/6
            r"n\^3",                    # n^3
            r"n\*\*3",                  # n**3
        ]
        for pat in cubic_patterns:
            if re.search(pat, expr):
                return "n^3"

        # n log n
        if "nlogn" in expr or "n*logn" in expr or "nlog(n)" in expr or "nlog" in expr:
            return "n log n"


        # Lineal: n, c*n, k*n + c, n+1, c(n+1)+c, cn+c, etc.
        lineal_patterns = [
            r"^[a-zA-Z0-9]*n(\+\d+)?$",         # n, cn, 2n, n+1
            r"^[a-zA-Z0-9]*\(n\+1\)(\+\d+)?$", # c(n+1), c(n+1)+c
            r"^[a-zA-Z0-9]*n\+[a-zA-Z0-9]+$",     # cn+c, n+c
            r"^n\+1$",                            # n+1
            r"^[a-zA-Z]+\(n\+1\)\+[a-zA-Z]+$", # c(n+1)+c
        ]
        for pat in lineal_patterns:
            if re.match(pat, expr):
                return "n"

        # Constante
        if expr.isdigit() or re.match(r"^[a-zA-Z]+$", expr):
            return "1"

        # Exponenciales
        if re.search(r"\d+\^n", expr) or re.search(r"\d+\*\*n", expr):
            return "a^n"  # forma genérica

        return expr

    
    def _construir_explicacion(self, f_n_str, resultado_suma):
        """
        Construye explicación detallada.
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                      MÉTODO DE SUMAS                         ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = T(n-1) + {f_n_str}

ESTRATEGIA:
  Expandir la recurrencia hasta llegar a la condición base,
  luego sumar todos los términos.

DESARROLLO:
  T(n) = T(n-1) + f(n)
  T(n) = T(n-2) + f(n-1) + f(n)
  T(n) = T(n-3) + f(n-2) + f(n-1) + f(n)
  ...
  T(n) = T(0) + Σ f(i) para i=1 hasta n

SUMA EVALUADA:
  Σ f(i) = {resultado_suma['suma_expr']}

SOLUCIÓN (Fórmula Cerrada): 
  {resultado_suma['solucion']}

Este resultado representa la solución matemática exacta de la
recurrencia. Para obtener la complejidad asintótica, otro
agente analizará esta fórmula.
"""



