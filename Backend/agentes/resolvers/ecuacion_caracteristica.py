from .base_resolver import BaseResolver
import re
from sympy import symbols, solve, Poly, simplify, apart

class EcuacionCaracteristica(BaseResolver):
    """
    Método de Ecuaciones Características para resolver recurrencias lineales homogéneas.
    
    Resuelve recurrencias de la forma:
    - T(n) = c₁T(n-1) + c₂T(n-2) + ... + cₖT(n-k)
    - T(n) = c₁T(n-1) + c₂T(n-2) + ... + cₖT(n-k) + f(n)  (no homogénea)
    
    Ejemplos:
    - T(n) = 2T(n-1)                    → Torres de Hanoi
    - T(n) = T(n-1) + T(n-2)            → Fibonacci
    - T(n) = 6T(n-1) - 9T(n-2)          → Raíces repetidas
    - T(n) = 3T(n-1) + 2T(n-2) + 1      → No homogénea
    
    Proceso:
    1. Formar la ecuación característica: rᵏ = c₁rᵏ⁻¹ + c₂rᵏ⁻² + ... + cₖ
    2. Resolver para encontrar las raíces
    3. Construir solución general basada en las raíces
    """
    
    def puede_resolver(self, ecuacion):
        """
        Verifica si la ecuación es una recurrencia lineal que puede resolver.
        
        Este método resuelve:
        - decrementacion_multiple: T(n) = aT(n-1) + f(n)
        - lineal_multiple: T(n) = a₁T(n-1) + a₂T(n-2) + ... + f(n)  (Fibonacci, etc)
        """
        forma = ecuacion.get('forma')
        
        # Puede resolver recurrencias lineales múltiples (Fibonacci, Tribonacci, etc)
        if forma == 'lineal_multiple':
            return True
        
        # También resuelve decrementación múltiple simple
        if forma == 'decrementacion_multiple':
            # Verificar que c = 1 (decrementación de 1 en 1)
            return ecuacion.get('c', 0) == 1
        
        return False
    
    def resolver(self, ecuacion):
        """
        Resuelve la recurrencia usando ecuaciones características.
        
        Para T(n) = aT(n-1) + f(n):
        - Si f(n) = 0 (homogénea): T(n) = c·aⁿ
        - Si f(n) ≠ 0 (no homogénea): usar solución particular
        
        Para T(n) = a₁T(n-1) + a₂T(n-2) + ... + f(n):
        - Resolver ecuación característica: rᵏ = a₁rᵏ⁻¹ + a₂rᵏ⁻² + ...
        - Construir solución basada en las raíces
        """
        forma = ecuacion.get('forma')
        
        if forma == 'lineal_multiple':
            # Fibonacci, Tribonacci, etc
            return self._resolver_lineal_multiple(ecuacion)
        elif forma == 'decrementacion_multiple':
            # Caso simple T(n) = aT(n-1) + f(n)
            pasos = []
            a = ecuacion['a']
            c = ecuacion['c']
            f_n_str = ecuacion['f_n']
            
            pasos.append(f"📝 Ecuación: T(n) = {a}T(n-{c}) + {f_n_str}")
            pasos.append(f"")
            pasos.append(f"🔹 MÉTODO DE ECUACIONES CARACTERÍSTICAS")
            pasos.append(f"   Para recurrencias lineales de la forma T(n) = aT(n-1) + f(n)")
            pasos.append(f"")
            
            # Verificar si es homogénea o no homogénea
            es_homogenea = self._es_homogenea(f_n_str)
            
            if es_homogenea:
                return self._resolver_homogenea(a, c, pasos)
            else:
                return self._resolver_no_homogenea(a, c, f_n_str, pasos)
        
        return self._crear_resultado(
            exito=False,
            explicacion="Forma de ecuación no soportada por Ecuaciones Características"
        )
    
    def _es_homogenea(self, f_n_str):
        """
        Verifica si f(n) = 0 (recurrencia homogénea).
        """
        f_n = f_n_str.strip().lower()
        return f_n == '0'
    
    def _resolver_homogenea(self, a, c, pasos):
        """
        Resuelve T(n) = aT(n-c) (homogénea).
        
        Solución general: T(n) = C · aⁿ/ᶜ
        """
        pasos.append(f"🔹 PASO 1: Identificar tipo de recurrencia")
        pasos.append(f"   Esta es una recurrencia lineal homogénea")
        pasos.append(f"   T(n) = {a}T(n-{c}) + 0")
        pasos.append(f"")
        
        pasos.append(f"🔹 PASO 2: Formar ecuación característica")
        pasos.append(f"   Asumimos T(n) = rⁿ")
        pasos.append(f"   Sustituyendo: rⁿ = {a}·r⁽ⁿ⁻{c}⁾")
        pasos.append(f"   Dividiendo por r⁽ⁿ⁻{c}⁾: r^{c} = {a}")
        pasos.append(f"   Ecuación característica: r = {a}^(1/{c})")
        pasos.append(f"")
        
        if c == 1:
            raiz = a
            pasos.append(f"🔹 PASO 3: Resolver ecuación característica")
            pasos.append(f"   r = {a}")
            pasos.append(f"")
            
            pasos.append(f"🔹 PASO 4: Construir solución general")
            pasos.append(f"   Como r = {a}, la solución es:")
            pasos.append(f"   T(n) = C · {a}ⁿ")
            pasos.append(f"")
            pasos.append(f"   donde C es una constante determinada por condiciones iniciales")
            pasos.append(f"   (generalmente T(0) o T(1))")
            pasos.append(f"")
            
            if a == 2:
                pasos.append(f"   💡 Ejemplo famoso: Torres de Hanoi con T(0) = 0")
                pasos.append(f"      T(n) = (2ⁿ - 1) cuando T(0) = 0")
                pasos.append(f"")
            
            # Solución simplificada asumiendo C como constante
            solucion = f"C·{a}ⁿ" if a != 1 else "C"
        else:
            raiz = a ** (1/c)
            pasos.append(f"🔹 PASO 3: Resolver ecuación característica")
            pasos.append(f"   r = {a}^(1/{c}) ≈ {raiz:.4f}")
            pasos.append(f"")
            
            pasos.append(f"🔹 PASO 4: Construir solución general")
            pasos.append(f"   T(n) = C · ({raiz:.4f})ⁿ")
            pasos.append(f"")
            
            solucion = f"C·{raiz:.4f}ⁿ"
        
        explicacion = self._construir_explicacion_homogenea(a, c, solucion)
        
        return self._crear_resultado(
            exito=True,
            solucion=solucion,
            pasos=pasos,
            explicacion=explicacion,
            detalles={
                'tipo': 'homogenea',
                'raiz': a if c == 1 else raiz,
                'a': a,
                'c': c
            }
        )
    
    def _resolver_no_homogenea(self, a, c, f_n_str, pasos):
        """
        Resuelve T(n) = aT(n-c) + f(n) (no homogénea).
        
        Solución = Solución homogénea + Solución particular
        """
        pasos.append(f"🔹 PASO 1: Identificar tipo de recurrencia")
        pasos.append(f"   Esta es una recurrencia lineal NO homogénea")
        pasos.append(f"   T(n) = {a}T(n-{c}) + {f_n_str}")
        pasos.append(f"")
        
        pasos.append(f"🔹 PASO 2: Resolver parte homogénea")
        pasos.append(f"   Primero resolvemos T(n) = {a}T(n-{c})")
        
        # Solución homogénea
        if c == 1:
            pasos.append(f"   Ecuación característica: r = {a}")
            pasos.append(f"   Solución homogénea: Tₕ(n) = C·{a}ⁿ")
        else:
            raiz = a ** (1/c)
            pasos.append(f"   Ecuación característica: r = {a}^(1/{c}) ≈ {raiz:.4f}")
            pasos.append(f"   Solución homogénea: Tₕ(n) = C·{raiz:.4f}ⁿ")
        pasos.append(f"")
        
        # Intentar encontrar solución particular
        pasos.append(f"🔹 PASO 3: Encontrar solución particular")
        pasos.append(f"   Necesitamos Tₚ(n) que satisfaga T(n) = {a}T(n-{c}) + {f_n_str}")
        pasos.append(f"")
        
        forma_fn = self._analizar_funcion(f_n_str)
        solucion_particular = self._encontrar_solucion_particular(a, c, forma_fn, pasos)
        
        if not solucion_particular:
            pasos.append(f"   ⚠️  No se pudo determinar solución particular automáticamente")
            pasos.append(f"   Se requiere análisis manual o uso de otro método")
            pasos.append(f"")
            
            return self._crear_resultado(
                exito=False,
                explicacion="No se pudo encontrar solución particular para esta recurrencia no homogénea",
                pasos=pasos
            )
        
        pasos.append(f"🔹 PASO 4: Solución general")
        pasos.append(f"   T(n) = Tₕ(n) + Tₚ(n)")
        
        # Formatear la solución con signos correctos
        if c == 1:
            if solucion_particular.startswith('-') or solucion_particular.startswith('('):
                solucion = f"C·{a}ⁿ - {solucion_particular.replace('-', '').replace('(', '').replace(')', '')}"
                pasos.append(f"   T(n) = C·{a}ⁿ - {solucion_particular.replace('-', '').replace('(', '').replace(')', '')}")
            else:
                solucion = f"C·{a}ⁿ + {solucion_particular}"
                pasos.append(f"   T(n) = C·{a}ⁿ + {solucion_particular}")
        else:
            raiz = a ** (1/c)
            if solucion_particular.startswith('-') or solucion_particular.startswith('('):
                solucion = f"C·{raiz:.4f}ⁿ - {solucion_particular.replace('-', '').replace('(', '').replace(')', '')}"
                pasos.append(f"   T(n) = C·{raiz:.4f}ⁿ - {solucion_particular.replace('-', '').replace('(', '').replace(')', '')}")
            else:
                solucion = f"C·{raiz:.4f}ⁿ + {solucion_particular}"
                pasos.append(f"   T(n) = C·{raiz:.4f}ⁿ + {solucion_particular}")
        
        pasos.append(f"")
        pasos.append(f"   donde C se determina con condiciones iniciales")
        pasos.append(f"")
        
        explicacion = self._construir_explicacion_no_homogenea(a, c, f_n_str, solucion)
        
        return self._crear_resultado(
            exito=True,
            solucion=solucion,
            pasos=pasos,
            explicacion=explicacion,
            detalles={
                'tipo': 'no_homogenea',
                'solucion_homogenea': f"C·{a}ⁿ" if c == 1 else f"C·{a**(1/c):.4f}ⁿ",
                'solucion_particular': solucion_particular,
                'a': a,
                'c': c,
                'f_n': f_n_str
            }
        )
    
    def _analizar_funcion(self, f_n_str):
        """
        Analiza f(n) para determinar la forma de solución particular.
        """
        f_n = f_n_str.lower().replace(' ', '')
        
        # Constante
        if f_n.isdigit():
            return {
                'tipo': 'constante',
                'valor': int(f_n)
            }
        
        if f_n == '1':
            return {
                'tipo': 'constante',
                'valor': 1
            }
        
        # Polinomial
        if 'n' in f_n and '**' not in f_n and '^' not in f_n:
            return {
                'tipo': 'lineal'
            }
        
        return {
            'tipo': 'desconocido',
            'expr': f_n_str
        }
    
    def _encontrar_solucion_particular(self, a, c, forma_fn, pasos):
        """
        Encuentra la solución particular según f(n).
        
        Casos comunes:
        - f(n) = constante k, a ≠ 1 → Tₚ(n) = k/(a-1)
        - f(n) = constante k, a = 1 → Tₚ(n) = kn
        - f(n) = n → requiere método más complejo
        """
        tipo = forma_fn['tipo']
        
        if tipo == 'constante':
            k = forma_fn['valor']
            
            if a == 1:
                # Caso especial: T(n) = T(n-1) + k
                pasos.append(f"   f(n) = {k} (constante)")
                pasos.append(f"   Como a = 1, probamos Tₚ(n) = An")
                pasos.append(f"   Sustituyendo: An = A(n-1) + {k}")
                pasos.append(f"   An = An - A + {k}")
                pasos.append(f"   A = {k}")
                pasos.append(f"   Solución particular: Tₚ(n) = {k}n")
                pasos.append(f"")
                
                return f"{k}n"
            else:
                # Caso general: T(n) = aT(n-1) + k
                pasos.append(f"   f(n) = {k} (constante)")
                pasos.append(f"   Probamos Tₚ(n) = A (constante)")
                pasos.append(f"   Sustituyendo: A = {a}·A + {k}")
                pasos.append(f"   A - {a}A = {k}")
                pasos.append(f"   A({1-a}) = {k}")
                pasos.append(f"   A = {k}/{1-a} = {k/(1-a):.4f}")
                
                # Formatear la solución particular
                valor_particular = k/(1-a)
                if valor_particular >= 0:
                    pasos.append(f"   Solución particular: Tₚ(n) = {valor_particular:.4f}")
                else:
                    pasos.append(f"   Solución particular: Tₚ(n) = {valor_particular:.4f}")
                pasos.append(f"")
                
                # Retornar con el signo correcto
                if abs(valor_particular - round(valor_particular)) < 0.0001:
                    valor_particular = round(valor_particular)
                    return f"{int(valor_particular)}" if valor_particular >= 0 else f"({int(valor_particular)})"
                else:
                    return f"{valor_particular:.4f}"
        
        elif tipo == 'lineal':
            pasos.append(f"   f(n) es lineal (requiere método más avanzado)")
            pasos.append(f"   Se recomienda usar Método de Sumas o Iteración")
            return None
        
        else:
            pasos.append(f"   f(n) tiene forma desconocida: {forma_fn.get('expr', 'N/A')}")
            return None
    
    def _construir_explicacion_homogenea(self, a, c, solucion):
        """
        Construye explicación para recurrencia homogénea.
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║              ECUACIONES CARACTERÍSTICAS                      ║
║                 (Recurrencia Homogénea)                      ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {a}T(n-{c})

ESTRATEGIA:
  1. Asumir T(n) = rⁿ
  2. Formar ecuación característica
  3. Resolver para r
  4. Construir solución general

SOLUCIÓN GENERAL: T(n) = {solucion}

Donde C es determinada por las condiciones iniciales.

Este método es especialmente útil para recurrencias exponenciales
como Torres de Hanoi, Fibonacci, y otras secuencias recursivas.
"""
    
    def _resolver_lineal_multiple(self, ecuacion):
        """
        Resuelve recurrencias lineales con múltiples términos recursivos.
        
        Forma general: T(n) = a₁T(n-1) + a₂T(n-2) + ... + aₖT(n-k) + f(n)
        
        Proceso:
        1. Formar ecuación característica: rᵏ - a₁rᵏ⁻¹ - a₂rᵏ⁻² - ... - aₖ = 0
        2. Resolver para encontrar raíces usando sympy
        3. Construir solución basada en las raíces
        """
        pasos = []
        terminos = ecuacion['terminos']  # [(coef, offset), ...]
        f_n_str = ecuacion['f_n']
        
        # Extraer información
        max_offset = max(offset for _, offset in terminos)
        
        # Crear descripción de la ecuación
        desc_terminos = []
        for coef, offset in terminos:
            if coef == 1:
                desc_terminos.append(f"T(n-{offset})")
            elif coef == -1:
                desc_terminos.append(f"- T(n-{offset})")
            else:
                desc_terminos.append(f"{coef}T(n-{offset})")
        
        ecuacion_str = " + ".join(desc_terminos).replace("+ -", "- ")
        if f_n_str != '0':
            ecuacion_str += f" + {f_n_str}"
        
        pasos.append(f"📝 Ecuación: T(n) = {ecuacion_str}")
        pasos.append(f"")
        pasos.append(f"🔹 MÉTODO DE ECUACIONES CARACTERÍSTICAS")
        pasos.append(f"   Para recurrencias lineales con múltiples términos recursivos")
        pasos.append(f"")
        
        # Verificar si es homogénea
        es_homogenea = self._es_homogenea(f_n_str)
        
        if not es_homogenea:
            pasos.append(f"⚠️  Esta recurrencia es NO homogénea (tiene f(n) = {f_n_str})")
            pasos.append(f"   Por ahora, solo resolvemos la parte homogénea.")
            pasos.append(f"")
        
        # PASO 1: Formar ecuación característica
        pasos.append(f"🔹 PASO 1: Formar ecuación característica")
        pasos.append(f"   Asumimos T(n) = rⁿ")
        pasos.append(f"")
        
        # Construir ecuación característica como polinomio
        # Para T(n) = a₁T(n-1) + a₂T(n-2) + ... se convierte en:
        # rⁿ = a₁r^(n-1) + a₂r^(n-2) + ...
        # Dividiendo por r^(n-k): r^k = a₁r^(k-1) + a₂r^(k-2) + ...
        # Reordenando: r^k - a₁r^(k-1) - a₂r^(k-2) - ... = 0
        
        # Crear diccionario de coeficientes por offset
        coef_dict = {offset: coef for coef, offset in terminos}
        
        # Construir descripción de la ecuación característica
        ec_terminos = [f"r^{max_offset}"]
        for i in range(1, max_offset + 1):
            coef = coef_dict.get(i, 0)
            if coef != 0:
                exp = max_offset - i
                if exp == 0:
                    if coef > 0:
                        ec_terminos.append(f"- {coef}")
                    else:
                        ec_terminos.append(f"+ {abs(coef)}")
                elif exp == 1:
                    if coef > 0:
                        ec_terminos.append(f"- {coef}r")
                    else:
                        ec_terminos.append(f"+ {abs(coef)}r")
                else:
                    if coef > 0:
                        ec_terminos.append(f"- {coef}r^{exp}")
                    else:
                        ec_terminos.append(f"+ {abs(coef)}r^{exp}")
        
        ec_str = " ".join(ec_terminos) + " = 0"
        pasos.append(f"   Ecuación característica: {ec_str}")
        pasos.append(f"")
        
        # PASO 2: Resolver con sympy
        pasos.append(f"🔹 PASO 2: Resolver ecuación característica")
        
        try:
            r = symbols('r')
            
            # Construir polinomio: r^k - a₁r^(k-1) - a₂r^(k-2) - ...
            poly_expr = r**max_offset
            for i in range(1, max_offset + 1):
                coef = coef_dict.get(i, 0)
                if coef != 0:
                    poly_expr -= coef * r**(max_offset - i)
            
            # Resolver
            raices = solve(poly_expr, r)
            
            pasos.append(f"   Resolviendo usando métodos numéricos...")
            pasos.append(f"   Raíces encontradas: {len(raices)}")
            pasos.append(f"")
            
            # Mostrar raíces
            for i, raiz in enumerate(raices, 1):
                # Evaluar numéricamente
                raiz_num = complex(raiz.evalf())
                if abs(raiz_num.imag) < 1e-10:
                    # Raíz real
                    pasos.append(f"   r_{i} = {raiz_num.real:.6f}")
                else:
                    # Raíz compleja
                    pasos.append(f"   r_{i} = {raiz_num.real:.6f} + {raiz_num.imag:.6f}i")
            pasos.append(f"")
            
            # PASO 3: Construir solución
            pasos.append(f"🔹 PASO 3: Construir solución general")
            
            # Verificar raíces repetidas
            raices_unicas = list(set([complex(r.evalf()) for r in raices]))
            
            if len(raices_unicas) == len(raices):
                # Todas las raíces son distintas
                pasos.append(f"   Todas las raíces son distintas")
                pasos.append(f"   Solución: T(n) = C₁·r₁ⁿ + C₂·r₂ⁿ + ... + Cₖ·rₖⁿ")
                pasos.append(f"")
                
                # Construir solución
                sol_terminos = []
                for i, raiz in enumerate(raices, 1):
                    raiz_num = complex(raiz.evalf())
                    if abs(raiz_num.imag) < 1e-10:
                        # Raíz real
                        val = raiz_num.real
                        if abs(val - round(val)) < 1e-6:
                            sol_terminos.append(f"C_{i}·{int(round(val))}ⁿ")
                        else:
                            sol_terminos.append(f"C_{i}·({val:.4f})ⁿ")
                    else:
                        # Raíz compleja - forma polar
                        modulo = abs(raiz_num)
                        sol_terminos.append(f"C_{i}·({modulo:.4f})ⁿ·e^(iθ_{i}n)")
                
                solucion = " + ".join(sol_terminos)
                
            else:
                # Hay raíces repetidas
                pasos.append(f"   ⚠️  Hay raíces repetidas (multiplicidad > 1)")
                pasos.append(f"   La solución incluye términos de la forma: (C₁ + C₂n + ... + Cₘnᵐ⁻¹)·rⁿ")
                pasos.append(f"")
                
                solucion = "Solución con raíces repetidas (requiere análisis de multiplicidad)"
            
            pasos.append(f"   T(n) = {solucion}")
            pasos.append(f"")
            pasos.append(f"   Donde C₁, C₂, ... son constantes determinadas por condiciones iniciales")
            pasos.append(f"")
            
            explicacion = self._construir_explicacion_lineal_multiple(ecuacion_str, ec_str, raices, solucion)
            
            return self._crear_resultado(
                exito=True,
                solucion=solucion,
                pasos=pasos,
                explicacion=explicacion,
                detalles={
                    'tipo': 'lineal_multiple',
                    'orden': max_offset,
                    'raices': [complex(r.evalf()) for r in raices],
                    'ecuacion_caracteristica': str(poly_expr)
                }
            )
            
        except Exception as e:
            pasos.append(f"   ❌ Error al resolver: {str(e)}")
            pasos.append(f"")
            
            return self._crear_resultado(
                exito=False,
                explicacion=f"No se pudo resolver la ecuación característica: {str(e)}",
                pasos=pasos
            )
    
    def _construir_explicacion_lineal_multiple(self, ecuacion_str, ec_str, raices, solucion):
        """
        Construye explicación para recurrencia lineal múltiple.
        """
        raices_desc = []
        for i, raiz in enumerate(raices, 1):
            raiz_num = complex(raiz.evalf())
            if abs(raiz_num.imag) < 1e-10:
                raices_desc.append(f"  r_{i} ≈ {raiz_num.real:.6f}")
            else:
                raices_desc.append(f"  r_{i} ≈ {raiz_num.real:.6f} + {raiz_num.imag:.6f}i")
        
        return f"""
╔══════════════════════════════════════════════════════════════╗
║              ECUACIONES CARACTERÍSTICAS                      ║
║            (Recurrencia Lineal Múltiple)                     ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {ecuacion_str}

ESTRATEGIA:
  1. Asumir T(n) = rⁿ
  2. Formar ecuación característica
  3. Resolver para encontrar raíces
  4. Construir solución general

ECUACIÓN CARACTERÍSTICA: {ec_str}

RAÍCES:
{chr(10).join(raices_desc)}

SOLUCIÓN GENERAL: T(n) = {solucion}

Las constantes C₁, C₂, ... se determinan usando las condiciones
iniciales T(0), T(1), ..., T(k-1).
"""
    
    def _construir_explicacion_homogenea(self, a, c, solucion):
        """
        Construye explicación para recurrencia homogénea.
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║              ECUACIONES CARACTERÍSTICAS                      ║
║                 (Recurrencia Homogénea)                      ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {a}T(n-{c})

ESTRATEGIA:
  1. Asumir T(n) = rⁿ
  2. Formar ecuación característica
  3. Resolver para r
  4. Construir solución general

SOLUCIÓN GENERAL: T(n) = {solucion}

Donde C es determinada por las condiciones iniciales.

Este método es especialmente útil para recurrencias exponenciales.
"""
    
    def _construir_explicacion_no_homogenea(self, a, c, f_n_str, solucion):
        """
        Construye explicación para recurrencia no homogénea.
        """
        return f"""
╔══════════════════════════════════════════════════════════════╗
║              ECUACIONES CARACTERÍSTICAS                      ║
║              (Recurrencia No Homogénea)                      ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = {a}T(n-{c}) + {f_n_str}

ESTRATEGIA:
  1. Resolver parte homogénea T(n) = {a}T(n-{c})
  2. Encontrar solución particular para f(n) = {f_n_str}
  3. Combinar: T(n) = Tₕ(n) + Tₚ(n)

SOLUCIÓN GENERAL: T(n) = {solucion}

Donde C es determinada por las condiciones iniciales.

La solución particular depende de la forma de f(n).
"""
