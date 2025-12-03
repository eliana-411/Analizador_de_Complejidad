from .base_resolver import BaseResolver
import math
import re

class ArbolRecursion(BaseResolver):
    """
    Método del Árbol de Recursión para resolver recurrencias.
    
    Visualiza la estructura de llamadas recursivas y calcula el costo total
    sumando el trabajo en cada nivel del árbol.
    
    ESPECIALMENTE ÚTIL PARA:
    - División asimétrica: T(n) = T(n/3) + T(2n/3) + n
    - Múltiples divisiones diferentes: T(n) = T(n/2) + T(n/4) + T(n/8) + n
    - Casos donde el Teorema Maestro NO aplica (diferentes divisores)
    - Recurrencias con caminos de diferente profundidad
    
    NO usar para:
    - División estándar T(n) = aT(n/b) + f(n) → mejor usar Teorema Maestro
    - Decrementación simple T(n) = T(n-1) + f(n) → mejor usar Método de Sumas
    - Lineales múltiples T(n) = aT(n-1) + bT(n-2) → mejor usar Ecuaciones Características
    
    Proceso:
    1. Construir el árbol de recursión nivel por nivel
    2. Calcular el costo en cada nivel (considerando caminos diferentes)
    3. Determinar altura del árbol (camino más largo)
    4. Sumar el costo de todos los niveles
    """
    
    def puede_resolver(self, ecuacion):
        """
        El árbol de recursión es útil principalmente para casos especiales:
        - División asimétrica (diferentes divisores)
        - Múltiples términos recursivos con divisiones distintas
        
        Para casos estándar, otros métodos son más directos.
        """
        forma = ecuacion.get('forma')
        
        # Solo resolver si realmente tiene sentido usar árbol
        if forma == 'divide_conquista':
            # Verificar si es asimétrico o múltiple
            if ecuacion.get('es_asimetrico') or ecuacion.get('terminos_multiples'):
                return True
            # Para casos simétricos estándar, dejar que otros métodos lo resuelvan
            return False
        
        # Decrementación mejor con método de sumas
        return False
    
    def resolver(self, ecuacion):
        """
        Resuelve usando el método del árbol de recursión.
        Solo se activa para casos donde realmente es necesario.
        """
        forma = ecuacion.get('forma')
        
        if forma == 'divide_conquista':
            # Detectar si es asimétrico o tiene múltiples términos
            if ecuacion.get('es_asimetrico'):
                return self._resolver_asimetrico(ecuacion)
            elif ecuacion.get('terminos_multiples'):
                return self._resolver_multiples_terminos(ecuacion)
            else:
                return self._resolver_divide_conquista(ecuacion)
        
        return self._crear_resultado(
            exito=False,
            explicacion="Esta forma se resuelve mejor con otro método"
        )
    
    def _resolver_asimetrico(self, ecuacion):
        """
        Resuelve recurrencias con división asimétrica.
        Ejemplo: T(n) = T(n/3) + T(2n/3) + n
        
        Este tipo NO puede ser resuelto por Teorema Maestro estándar
        porque tiene diferentes divisores (n/3 y 2n/3).
        """
        pasos = []
        terminos = ecuacion.get('terminos_recursivos', [])
        f_n_str = ecuacion.get('f_n', '0')
        
        pasos.append(f"📝 Ecuación: T(n) = " + " + ".join([f"T(n/{t['divisor']})" for t in terminos]) + f" + {f_n_str}")
        pasos.append(f"")
        pasos.append(f"🔹 MÉTODO DEL ÁRBOL DE RECURSIÓN (División Asimétrica)")
        pasos.append(f"   ⚠️  Esta ecuación NO puede resolverse con Teorema Maestro")
        pasos.append(f"   porque tiene divisores diferentes: {', '.join([str(t['divisor']) for t in terminos])}")
        pasos.append(f"")
        
        # PASO 1: Construir niveles del árbol
        pasos.append(f"🔹 PASO 1: Construir el árbol de recursión")
        pasos.append(f"")
        pasos.append(f"   Nivel 0 (raíz):")
        pasos.append(f"      T(n)")
        pasos.append(f"      Costo: {f_n_str}")
        pasos.append(f"")
        
        pasos.append(f"   Nivel 1:")
        for t in terminos:
            pasos.append(f"      T(n/{t['divisor']})")
        pasos.append(f"      Costo por nodo: {f_n_str} evaluado en cada tamaño")
        
        # Calcular suma del nivel 1
        suma_nivel1 = self._calcular_suma_nivel_asimetrico(terminos, f_n_str, 1)
        pasos.append(f"      Suma nivel 1: {suma_nivel1}")
        pasos.append(f"")
        
        pasos.append(f"   Nivel 2:")
        pasos.append(f"      Cada T(n/{terminos[0]['divisor']}) genera {len(terminos)} llamadas")
        pasos.append(f"      Total: {len(terminos)}² = {len(terminos)**2} nodos")
        suma_nivel2 = self._calcular_suma_nivel_asimetrico(terminos, f_n_str, 2)
        pasos.append(f"      Suma nivel 2: {suma_nivel2}")
        pasos.append(f"")
        
        # PASO 2: Determinar altura (camino más largo)
        pasos.append(f"🔹 PASO 2: Determinar altura del árbol")
        divisor_min = min(t['divisor'] for t in terminos)
        divisor_max = max(t['divisor'] for t in terminos)
        pasos.append(f"   Camino más corto: divisor = {divisor_max} → altura ≈ log_{divisor_max}(n)")
        pasos.append(f"   Camino más largo: divisor = {divisor_min} → altura ≈ log_{divisor_min}(n)")
        pasos.append(f"")
        pasos.append(f"   La altura del árbol está determinada por el camino más largo:")
        pasos.append(f"   h = log_{divisor_min}(n)")
        pasos.append(f"")
        
        # PASO 3: Analizar suma de niveles
        pasos.append(f"🔹 PASO 3: Sumar costo de todos los niveles")
        pasos.append(f"")
        
        forma_fn = self._analizar_funcion_simple(f_n_str)
        
        if forma_fn['tipo'] == 'lineal':
            pasos.append(f"   Para f(n) = n:")
            pasos.append(f"   Nivel 0: n")
            pasos.append(f"   Nivel 1: n/{terminos[0]['divisor']} + n/{terminos[1]['divisor']} + ... = n")
            pasos.append(f"   Nivel 2: suma también ≈ n")
            pasos.append(f"   ...")
            pasos.append(f"")
            pasos.append(f"   🔑 Observación: cada nivel suma aproximadamente n")
            pasos.append(f"   Total niveles: log_{divisor_min}(n)")
            pasos.append(f"")
            pasos.append(f"   T(n) = n × log_{divisor_min}(n)")
            
            solucion = f"c·n·log(n)"
            
        elif forma_fn['tipo'] == 'constante':
            c = forma_fn.get('valor', 1)
            num_terminos = len(terminos)
            pasos.append(f"   Para f(n) = {c}:")
            pasos.append(f"   Nivel 0: {c}")
            pasos.append(f"   Nivel 1: {num_terminos} × {c} = {num_terminos * c}")
            pasos.append(f"   Nivel 2: {num_terminos}² × {c} = {num_terminos**2 * c}")
            pasos.append(f"   ...")
            pasos.append(f"   Nivel k: {num_terminos}ᵏ × {c}")
            pasos.append(f"")
            pasos.append(f"   Suma geométrica con razón {num_terminos}")
            
            if num_terminos > 1:
                log_val = math.log(num_terminos) / math.log(divisor_min)
                pasos.append(f"   T(n) ≈ c·n^{log_val:.4f}")
                solucion = f"c·n^{log_val:.4f}"
            else:
                pasos.append(f"   T(n) = c·log(n)")
                solucion = "c·log(n)"
        else:
            pasos.append(f"   f(n) = {f_n_str}")
            pasos.append(f"   Análisis requiere cálculo detallado caso por caso")
            solucion = "Requiere análisis adicional"
        
        pasos.append(f"")
        pasos.append(f"✅ SOLUCIÓN: T(n) = {solucion}")
        
        explicacion = f"""
╔══════════════════════════════════════════════════════════════╗
║           ÁRBOL DE RECURSIÓN - DIVISIÓN ASIMÉTRICA           ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = """ + " + ".join([f"T(n/{t['divisor']})" for t in terminos]) + f" + {f_n_str}" + """

⚠️  NOTA IMPORTANTE:
Este tipo de recurrencia NO puede resolverse con el Teorema Maestro
porque tiene diferentes divisores en los términos recursivos.

El Árbol de Recursión es el método ideal para este caso.

SOLUCIÓN: T(n) = """ + solucion + """

El árbol de recursión muestra que aunque las ramas tienen diferentes
profundidades, el costo por nivel se mantiene balanceado.
"""
        
        return self._crear_resultado(
            exito=True,
            solucion=solucion,
            pasos=pasos,
            explicacion=explicacion
        )
    
    def _resolver_multiples_terminos(self, ecuacion):
        """
        Resuelve recurrencias con múltiples términos recursivos con divisiones diferentes.
        Ejemplo: T(n) = T(n/2) + T(n/4) + T(n/8) + n
        """
        pasos = []
        terminos = ecuacion.get('terminos_recursivos', [])
        f_n_str = ecuacion.get('f_n', '0')
        
        pasos.append(f"📝 Ecuación: T(n) = " + " + ".join([f"T(n/{t['divisor']})" for t in terminos]) + f" + {f_n_str}")
        pasos.append(f"")
        pasos.append(f"🔹 MÉTODO DEL ÁRBOL DE RECURSIÓN (Múltiples Divisiones)")
        pasos.append(f"   Esta ecuación tiene {len(terminos)} términos recursivos con divisores diferentes")
        pasos.append(f"")
        
        pasos.append(f"🔹 PASO 1: Identificar estructura")
        for i, t in enumerate(terminos):
            pasos.append(f"   Término {i+1}: T(n/{t['divisor']})")
        pasos.append(f"   Trabajo no recursivo: {f_n_str}")
        pasos.append(f"")
        
        # Determinar profundidades de cada camino
        divisor_min = min(t['divisor'] for t in terminos)
        divisor_max = max(t['divisor'] for t in terminos)
        
        pasos.append(f"🔹 PASO 2: Analizar profundidades")
        pasos.append(f"   Camino más profundo: divisor {divisor_min} → log_{divisor_min}(n) niveles")
        pasos.append(f"   Camino más corto: divisor {divisor_max} → log_{divisor_max}(n) niveles")
        pasos.append(f"")
        pasos.append(f"   ⚠️  El árbol es irregular: diferentes ramas tienen diferentes alturas")
        pasos.append(f"")
        
        pasos.append(f"🔹 PASO 3: Sumar costo por nivel")
        forma_fn = self._analizar_funcion_simple(f_n_str)
        
        if forma_fn['tipo'] == 'lineal':
            pasos.append(f"   Para f(n) = n, el costo dominante viene del trabajo no recursivo")
            pasos.append(f"   en los primeros niveles del árbol.")
            pasos.append(f"")
            pasos.append(f"   T(n) ≈ c·n")
            solucion = "c·n"
        else:
            pasos.append(f"   Análisis detallado requiere sumar costo nivel por nivel")
            pasos.append(f"   considerando que no todos los nodos llegan a todos los niveles")
            solucion = "Requiere análisis adicional"
        
        pasos.append(f"")
        pasos.append(f"✅ SOLUCIÓN: T(n) = {solucion}")
        
        explicacion = f"""
╔══════════════════════════════════════════════════════════════╗
║        ÁRBOL DE RECURSIÓN - MÚLTIPLES DIVISIONES             ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = """ + " + ".join([f"T(n/{t['divisor']})" for t in terminos]) + f" + {f_n_str}" + """

Este tipo de recurrencia requiere análisis con árbol porque:
- Tiene múltiples términos con divisores diferentes
- Las ramas del árbol tienen profundidades diferentes
- El costo no se distribuye uniformemente

SOLUCIÓN: T(n) = """ + solucion + """
"""
        
        return self._crear_resultado(
            exito=True,
            solucion=solucion,
            pasos=pasos,
            explicacion=explicacion
        )
    
    def _calcular_suma_nivel_asimetrico(self, terminos, f_n_str, nivel):
        """
        Calcula la suma del costo en un nivel del árbol asimétrico.
        """
        forma_fn = self._analizar_funcion_simple(f_n_str)
        
        if forma_fn['tipo'] == 'lineal':
            # Para f(n) = n, suma de n/d1 + n/d2 + ...
            suma_fracciones = sum(1/t['divisor']**nivel for t in terminos)
            if abs(suma_fracciones - 1) < 0.1:
                return "≈ n"
            else:
                return f"{suma_fracciones:.3f}·n"
        elif forma_fn['tipo'] == 'constante':
            c = forma_fn.get('valor', 1)
            num_nodos = len(terminos) ** nivel
            return f"{num_nodos * c}"
        else:
            return "suma compleja"
    
    def _resolver_divide_conquista(self, ecuacion):
        """
        Resuelve T(n) = aT(n/b) + f(n) usando árbol de recursión.
        
        NOTA: Este método solo debería activarse como fallback o para verificación.
        Para casos estándar, el Teorema Maestro es más directo.
        
        Construcción del árbol:
        - Raíz: costo f(n)
        - Nivel 1: a nodos, cada uno con costo f(n/b)
        - Nivel 2: a² nodos, cada uno con costo f(n/b²)
        - ...
        - Nivel k: aᵏ nodos, cada uno con costo f(n/bᵏ)
        """
        pasos = []
        a = ecuacion['a']
        b = ecuacion['b']
        f_n_str = ecuacion['f_n']
        
        pasos.append(f"📝 Ecuación: T(n) = {a}T(n/{b}) + {f_n_str}")
        pasos.append(f"")
        pasos.append(f"🔹 MÉTODO DEL ÁRBOL DE RECURSIÓN")
        pasos.append(f"   💡 Para este tipo estándar, el Teorema Maestro es más directo")
        pasos.append(f"   Aquí mostramos el análisis visual del árbol")
        pasos.append(f"")
        
        # PASO 1: Construir el árbol
        pasos.append(f"🔹 PASO 1: Construir el árbol de recursión")
        pasos.append(f"")
        pasos.append(f"   Nivel 0 (raíz):")
        pasos.append(f"      T(n)")
        pasos.append(f"      Costo: {f_n_str}")
        pasos.append(f"      Nodos: 1")
        pasos.append(f"")
        
        pasos.append(f"   Nivel 1:")
        pasos.append(f"      {a} llamadas a T(n/{b})")
        if a == 1:
            pasos.append(f"      T(n/{b})")
        elif a == 2:
            pasos.append(f"      T(n/{b})  T(n/{b})")
        elif a <= 4:
            pasos.append(f"      " + "  ".join([f"T(n/{b})"] * a))
        else:
            pasos.append(f"      {a} × T(n/{b})")
        pasos.append(f"      Costo por nodo: f(n/{b})")
        pasos.append(f"      Costo total nivel: {a} × f(n/{b})")
        pasos.append(f"      Nodos: {a}")
        pasos.append(f"")
        
        pasos.append(f"   Nivel 2:")
        pasos.append(f"      {a}² = {a**2} llamadas a T(n/{b}²)")
        pasos.append(f"      Costo por nodo: f(n/{b}²)")
        pasos.append(f"      Costo total nivel: {a**2} × f(n/{b}²)")
        pasos.append(f"      Nodos: {a**2}")
        pasos.append(f"")
        
        pasos.append(f"   Nivel k (general):")
        pasos.append(f"      Llamadas: {a}ᵏ × T(n/{b}ᵏ)")
        pasos.append(f"      Costo por nodo: f(n/{b}ᵏ)")
        pasos.append(f"      Costo total nivel: {a}ᵏ × f(n/{b}ᵏ)")
        pasos.append(f"      Nodos: {a}ᵏ")
        pasos.append(f"")
        
        # PASO 2: Determinar altura del árbol
        pasos.append(f"🔹 PASO 2: Determinar altura del árbol")
        pasos.append(f"   El árbol se detiene cuando llegamos al caso base")
        pasos.append(f"   n/{b}ᵏ = 1  →  n = {b}ᵏ  →  k = log_{b}(n)")
        pasos.append(f"")
        pasos.append(f"   Altura del árbol: h = log_{b}(n)")
        pasos.append(f"")
        
        # PASO 3: Analizar f(n)
        pasos.append(f"🔹 PASO 3: Analizar el costo por nivel")
        forma_fn = self._analizar_funcion_simple(f_n_str)
        
        if forma_fn['tipo'] == 'constante':
            c = forma_fn.get('valor', 1)
            pasos.append(f"   f(n) = {c} (constante)")
            pasos.append(f"")
            pasos.append(f"   Nivel 0: 1 × {c} = {c}")
            pasos.append(f"   Nivel 1: {a} × {c} = {a*c}")
            pasos.append(f"   Nivel 2: {a**2} × {c} = {a**2 * c}")
            pasos.append(f"   ...")
            pasos.append(f"   Nivel k: {a}ᵏ × {c}")
            pasos.append(f"")
            
        elif forma_fn['tipo'] == 'lineal':
            pasos.append(f"   f(n) = n (lineal)")
            pasos.append(f"")
            pasos.append(f"   Nivel 0: 1 × n = n")
            pasos.append(f"   Nivel 1: {a} × (n/{b}) = {a}/{b} × n")
            pasos.append(f"   Nivel 2: {a**2} × (n/{b}²) = {a**2}/{b**2} × n")
            pasos.append(f"   ...")
            pasos.append(f"   Nivel k: {a}ᵏ × (n/{b}ᵏ) = ({a}/{b})ᵏ × n")
            pasos.append(f"")
            
        else:
            pasos.append(f"   f(n) = {f_n_str}")
            pasos.append(f"   Nivel k: {a}ᵏ × f(n/{b}ᵏ)")
            pasos.append(f"")
        
        # PASO 4: Sumar todos los niveles
        pasos.append(f"🔹 PASO 4: Sumar el costo de todos los niveles")
        pasos.append(f"")
        pasos.append(f"   T(n) = Σ (costo nivel i) para i=0 hasta log_{b}(n)")
        pasos.append(f"")
        
        # Determinar la suma según el tipo de función
        solucion = self._calcular_suma_arbol(a, b, forma_fn, pasos)
        
        if not solucion:
            return self._crear_resultado(
                exito=False,
                explicacion="No se pudo calcular la suma del árbol automáticamente",
                pasos=pasos
            )
        
        explicacion = self._construir_explicacion(a, b, f_n_str, solucion)
        
        return self._crear_resultado(
            exito=True,
            solucion=solucion,
            pasos=pasos,
            explicacion=explicacion,
            detalles={
                'a': a,
                'b': b,
                'f_n': f_n_str,
                'altura': f"log_{b}(n)",
                'tipo_fn': forma_fn['tipo']
            }
        )
    
    def _analizar_funcion_simple(self, f_n_str):
        """Análisis simple de f(n)"""
        f_n = f_n_str.lower().replace(' ', '')
        
        if f_n.isdigit():
            return {'tipo': 'constante', 'valor': int(f_n)}
        elif f_n == '1':
            return {'tipo': 'constante', 'valor': 1}
        elif f_n == 'n':
            return {'tipo': 'lineal'}
        elif 'n**2' in f_n or 'n^2' in f_n:
            return {'tipo': 'cuadratico'}
        elif 'log' in f_n:
            return {'tipo': 'logaritmico'}
        else:
            return {'tipo': 'otro', 'expr': f_n_str}
    
    def _calcular_suma_arbol(self, a, b, forma_fn, pasos):
        """
        Calcula la suma del costo de todos los niveles del árbol.
        """
        tipo = forma_fn['tipo']
        
        if tipo == 'constante':
            c = forma_fn.get('valor', 1)
            # Suma: c + ac + a²c + ... + aᵏc donde k = log_b(n)
            # Si a = 1: suma = c × log_b(n)
            # Si a > 1: suma geométrica = c × (aᵏ⁺¹ - 1)/(a - 1)
            
            if a == 1:
                pasos.append(f"   Suma: {c} × (1 + 1 + ... + 1) = {c} × log_{b}(n)")
                pasos.append(f"")
                pasos.append(f"   T(n) = {c}·log_{b}(n) + caso_base")
                return f"{c}·log_{b}(n) + c'"
            else:
                pasos.append(f"   Suma geométrica: {c} × (1 + {a} + {a}² + ... + {a}^log_{b}(n))")
                pasos.append(f"   = {c} × ({a}^(log_{b}(n)+1) - 1)/({a} - 1)")
                pasos.append(f"")
                pasos.append(f"   Nota: {a}^log_{b}(n) = n^log_{b}({a})")
                log_ba = math.log(a) / math.log(b)
                pasos.append(f"         log_{b}({a}) ≈ {log_ba:.4f}")
                pasos.append(f"")
                pasos.append(f"   T(n) ≈ c·n^{log_ba:.4f}")
                return f"c·n^{log_ba:.4f}"
                
        elif tipo == 'lineal':
            # Suma: n × (1 + a/b + (a/b)² + ... + (a/b)ᵏ)
            ratio = a / b
            
            if abs(ratio - 1) < 0.01:
                # a/b ≈ 1: suma aritmética
                pasos.append(f"   Como {a}/{b} ≈ 1, tenemos:")
                pasos.append(f"   Suma: n × (log_{b}(n) términos)")
                pasos.append(f"")
                pasos.append(f"   T(n) = n·log_{b}(n) + términos_menores")
                return f"n·log_{b}(n) + c"
            elif ratio < 1:
                # Serie convergente
                pasos.append(f"   Como {a}/{b} < 1, la serie converge:")
                pasos.append(f"   Suma ≈ n × (constante)")
                pasos.append(f"")
                pasos.append(f"   T(n) = c·n")
                return "c·n"
            else:
                # ratio > 1: término dominante es el último
                pasos.append(f"   Como {a}/{b} > 1, domina el último término:")
                log_ba = math.log(a) / math.log(b)
                pasos.append(f"   T(n) ≈ n^{log_ba:.4f}")
                return f"n^{log_ba:.4f}"
        
        elif tipo == 'cuadratico':
            pasos.append(f"   f(n) = n²")
            pasos.append(f"   Análisis de suma de niveles requiere cálculo más detallado")
            return None
        
        else:
            pasos.append(f"   f(n) = {forma_fn.get('expr', 'desconocido')}")
            pasos.append(f"   Suma requiere análisis caso por caso")
            return None
    
    def _construir_explicacion(self, a, b, f_n_str, solucion):
        """
        Construye explicación del método.
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║                  ÁRBOL DE RECURSIÓN                          ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {a}T(n/{b}) + {f_n_str}

💡 NOTA: Para casos estándar como este, el Teorema Maestro es más directo.
   El árbol de recursión es ideal para divisiones asimétricas.

ESTRATEGIA:
  1. Construir árbol de llamadas recursivas
  2. Calcular costo en cada nivel
  3. Determinar altura del árbol (log_{b}(n))
  4. Sumar costo de todos los niveles

ESTRUCTURA DEL ÁRBOL:
  • Nivel 0: 1 nodo con costo {f_n_str}
  • Nivel 1: {a} nodos con costo f(n/{b}) cada uno
  • Nivel 2: {a}² nodos con costo f(n/{b}²) cada uno
  • ...
  • Nivel k: {a}ᵏ nodos con costo f(n/{b}ᵏ) cada uno

ALTURA: log_{b}(n) niveles

SOLUCIÓN: T(n) = {solucion}

El árbol de recursión visualiza la estructura de llamadas
y verifica resultados de otros métodos.
"""
