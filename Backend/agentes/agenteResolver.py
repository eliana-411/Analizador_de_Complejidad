import re
from .resolvers.teorema_maestro import TeoremaMAestro
from .resolvers.metodo_sumas import MetodoSumas
from .resolvers.metodo_iteracion import MetodoIteracion
from .resolvers.ecuacion_caracteristica import EcuacionCaracteristica
from .resolvers.arbol_recursion import ArbolRecursion

class AgenteResolver:
    """
    Agente especializado en resolver ecuaciones de recurrencia.
    
    Responsabilidades:
    - Parsear ecuaciones de recurrencia en formato string
    - Determinar qué método de resolución aplicar
    - Coordinar la resolución usando el método apropiado
    - Retornar resultados en formato unificado
    """
    
    def __init__(self):
        """Inicializar el resolver con todos los métodos disponibles"""
        self.metodos = [
            TeoremaMAestro(),
            MetodoSumas(),
            EcuacionCaracteristica(),
            MetodoIteracion(),
            ArbolRecursion(),  # Para divisiones asimétricas y múltiples términos
            
            # Aquí se agregarán más métodos después:
            # AkraBazzi(),
        ]
    
    def resolver_ecuacion(self, ecuacion_str):
        """
        Resuelve una ecuación de recurrencia.
        
        Parámetros:
        - ecuacion_str: string con la ecuación, ej: "T(n) = 2T(n/2) + n"
        
        Retorna:
        - dict con:
            - exito: bool
            - ecuacion_original: str
            - ecuacion_parseada: dict
            - metodo_usado: str
            - solucion: str
            - pasos: list
            - explicacion: str
            - intentos: list (métodos que se intentaron)
        """
        resultado = {
            'exito': False,
            'ecuacion_original': ecuacion_str,
            'ecuacion_parseada': None,
            'metodo_usado': None,
            'solucion': None,
            'pasos': [],
            'explicacion': '',
            'intentos': []
        }
        
        # Paso 1: Parsear la ecuación
        ecuacion_parseada = self._parsear_ecuacion(ecuacion_str)
        
        if not ecuacion_parseada:
            resultado['explicacion'] = (
                f"❌ No se pudo parsear la ecuación: '{ecuacion_str}'\n\n"
                f"Formatos soportados:\n"
                f"  • T(n) = aT(n/b) + f(n)  (Divide y Conquista)\n"
                f"  • T(n) = T(n-c) + f(n)   (Decrementación)\n"
                f"  • T(n) = aT(n-c) + f(n)  (Decrementación múltiple)"
            )
            return resultado
        
        resultado['ecuacion_parseada'] = ecuacion_parseada
        
        # Paso 2: Intentar resolver con cada método
        for metodo in self.metodos:
            nombre_metodo = metodo.__class__.__name__
            resultado['intentos'].append(nombre_metodo)
            
            # Verificar si el método puede resolver esta ecuación
            if metodo.puede_resolver(ecuacion_parseada):
                print(f"  ✓ Intentando con {nombre_metodo}...")
                
                # Intentar resolver
                res_metodo = metodo.resolver(ecuacion_parseada)
                
                if res_metodo['exito']:
                    # ¡Éxito!
                    resultado['exito'] = True
                    resultado['metodo_usado'] = nombre_metodo
                    resultado['solucion'] = res_metodo['solucion']
                    resultado['pasos'] = res_metodo['pasos']
                    resultado['explicacion'] = res_metodo['explicacion']
                    resultado['detalles'] = res_metodo.get('detalles', {})
                    
                    return resultado
        
        # Si llegamos aquí, ningún método pudo resolver
        resultado['explicacion'] = (
            f"❌ No se pudo resolver la ecuación con los métodos disponibles.\n\n"
            f"Métodos intentados: {', '.join(resultado['intentos'])}\n\n"
            f"Ecuación parseada como: {ecuacion_parseada['forma']}\n"
            f"Parámetros: {ecuacion_parseada}"
        )
        
        return resultado
    
    def _parsear_ecuacion(self, ecuacion_str):
        """
        Parsea una ecuación de recurrencia desde string.
        
        Formatos soportados:
        1. T(n) = aT(n/b) + f(n)                    → divide_conquista
        2. T(n) = T(n-c) + f(n)                     → decrementacion
        3. T(n) = aT(n-c) + f(n)                    → decrementacion_multiple
        4. T(n) = a₁T(n-1) + a₂T(n-2) + ... + f(n)  → lineal_multiple (Fibonacci, etc)
        5. T(n) = T(n/a) + T(n/b) + ... + f(n)      → divide_conquista asimétrico
        
        Retorna:
        - dict con forma y parámetros, o None si no se pudo parsear
        """
        # Limpiar espacios
        ecuacion = ecuacion_str.replace(' ', '')
        
        # Intentar parsear como Lineal Múltiple PRIMERO (más compleja)
        # Ej: T(n) = T(n-1) + T(n-2)
        resultado = self._parsear_lineal_multiple(ecuacion)
        if resultado:
            return resultado
        
        # Intentar parsear como División Asimétrica o Múltiple ANTES del estándar
        # Ej: T(n) = T(n/3) + T(2n/3) + n  o  T(n) = T(n/2) + T(n/4) + n
        resultado = self._parsear_division_multiple(ecuacion)
        if resultado:
            return resultado
        
        # Intentar parsear como Divide y Conquista estándar: T(n) = aT(n/b) + f(n)
        resultado = self._parsear_divide_conquista(ecuacion)
        if resultado:
            return resultado
        
        # Intentar parsear como Decrementación: T(n) = T(n-c) + f(n)
        resultado = self._parsear_decrementacion(ecuacion)
        if resultado:
            return resultado
        
        # Intentar parsear como Decrementación Múltiple: T(n) = aT(n-c) + f(n)
        resultado = self._parsear_decrementacion_multiple(ecuacion)
        if resultado:
            return resultado
        
        return None
    
    def _parsear_division_multiple(self, ecuacion):
        """
        Parsea ecuaciones con múltiples términos de división (asimétricas o múltiples).
        
        Ejemplos:
        - T(n) = T(n/3) + T(2n/3) + n      → asimétrico (diferentes divisores)
        - T(n) = T(n/2) + T(n/4) + T(n/8) + n  → múltiples divisiones
        - T(n) = 2T(n/3) + T(n/2) + n      → combinación
        
        Detecta:
        - Todos los términos T(numerador*n/divisor)
        - Si hay 2+ términos con divisores diferentes → división múltiple
        """
        # Buscar todos los términos del tipo T(n/divisor) o T(coef*n/divisor)
        # Patrones: T(n/3), T(2n/3), 2T(n/4), etc.
        patron = r'(\d*)T\((\d*)n/(\d+)\)'
        matches = re.findall(patron, ecuacion, re.IGNORECASE)
        
        if len(matches) < 2:
            # Si hay menos de 2 términos, no es división múltiple
            return None
        
        # Extraer términos recursivos
        terminos_recursivos = []
        for coef_str, num_str, div_str in matches:
            coef = int(coef_str) if coef_str else 1
            numerador = int(num_str) if num_str else 1
            divisor = int(div_str)
            
            terminos_recursivos.append({
                'coeficiente': coef,
                'numerador': numerador,
                'divisor': divisor
            })
        
        # Eliminar todos los términos recursivos para obtener f(n)
        ecuacion_sin_t = ecuacion
        for match in re.finditer(patron, ecuacion, re.IGNORECASE):
            ecuacion_sin_t = ecuacion_sin_t.replace(match.group(0), '', 1)
        
        # Limpiar la parte restante
        # Remover T(n)= del inicio
        ecuacion_sin_t = re.sub(r'T\(n\)=', '', ecuacion_sin_t, flags=re.IGNORECASE)
        ecuacion_sin_t = ecuacion_sin_t.strip()
        ecuacion_sin_t = ecuacion_sin_t.lstrip('+').strip()
        
        f_n = ecuacion_sin_t if ecuacion_sin_t else '0'
        f_n = f_n.replace('^', '**')
        
        # Determinar si es asimétrico (diferentes divisores) o solo múltiples términos
        divisores = [t['divisor'] for t in terminos_recursivos]
        divisores_unicos = set(divisores)
        
        # Verificar si hay diferentes numeradores también
        tiene_diferentes_divisores = len(divisores_unicos) > 1
        tiene_diferentes_numeradores = len(set(t['numerador'] for t in terminos_recursivos)) > 1
        
        es_asimetrico = tiene_diferentes_divisores or tiene_diferentes_numeradores
        
        # Construir ecuación limpia
        terminos_str = []
        for t in terminos_recursivos:
            if t['coeficiente'] == 1:
                if t['numerador'] == 1:
                    terminos_str.append(f"T(n/{t['divisor']})")
                else:
                    terminos_str.append(f"T({t['numerador']}n/{t['divisor']})")
            else:
                if t['numerador'] == 1:
                    terminos_str.append(f"{t['coeficiente']}T(n/{t['divisor']})")
                else:
                    terminos_str.append(f"{t['coeficiente']}T({t['numerador']}n/{t['divisor']})")
        
        ecuacion_limpia = "T(n) = " + " + ".join(terminos_str)
        if f_n != '0':
            ecuacion_limpia += f" + {f_n}"
        
        return {
            'forma': 'divide_conquista',
            'terminos_recursivos': terminos_recursivos,
            'f_n': f_n,
            'ecuacion_limpia': ecuacion_limpia,
            'es_asimetrico': es_asimetrico,
            'terminos_multiples': len(terminos_recursivos) > 1
        }
    
    def _parsear_lineal_multiple(self, ecuacion):
        """
        Parsea ecuaciones lineales con múltiples términos recursivos.
        
        Formatos:
        - T(n) = T(n-1) + T(n-2)                    → Fibonacci
        - T(n) = T(n-1) + T(n-2) + 1                → Fibonacci con término constante
        - T(n) = 2T(n-1) + 3T(n-2)                  → Con coeficientes
        - T(n) = T(n-1) + T(n-2) + T(n-3)           → Tribonacci
        - T(n) = 6T(n-1) - 9T(n-2)                  → Con resta
        
        Retorna dict con:
        - forma: 'lineal_multiple'
        - terminos: lista de (coeficiente, offset) ej: [(1, 1), (1, 2)]
        - f_n: término no recursivo (puede ser '0')
        """
        # Remover T(n)= del inicio
        if not ecuacion.upper().startswith('T(N)='):
            return None
        
        lado_derecho = ecuacion[5:]  # Quitar 'T(n)='
        
        # Buscar todos los términos T(n-k) con sus coeficientes
        # Patrón mejorado que captura el signo y coeficiente
        patron_terminos = r'([+\-]?\d*)T\(n-(\d+)\)'
        terminos = []
        
        matches = list(re.finditer(patron_terminos, lado_derecho, re.IGNORECASE))
        
        if len(matches) < 2:
            # Necesita al menos 2 términos recursivos para ser "múltiple"
            return None
        
        # Extraer cada match completo para removerlo después
        terminos_str = []
        for match in matches:
            coef_str = match.group(1).strip()
            offset = int(match.group(2))
            
            # Determinar el coeficiente
            if coef_str == '' or coef_str == '+':
                coeficiente = 1
            elif coef_str == '-':
                coeficiente = -1
            else:
                coeficiente = int(coef_str)
            
            terminos.append((coeficiente, offset))
            terminos_str.append(match.group(0))
        
        # Extraer f(n) - remover todos los T(n-k) y lo que queda es f(n)
        ecuacion_sin_t = lado_derecho
        for term_str in terminos_str:
            ecuacion_sin_t = ecuacion_sin_t.replace(term_str, '', 1)
        
        # Limpiar lo que queda
        ecuacion_sin_t = ecuacion_sin_t.strip()
        ecuacion_sin_t = ecuacion_sin_t.lstrip('+').strip()
        
        # Si empieza con + o -, es f(n)
        f_n = '0'
        if ecuacion_sin_t:
            f_n = ecuacion_sin_t.replace('^', '**')
        
        # Ordenar términos por offset
        terminos.sort(key=lambda x: x[1])
        
        # Crear descripción limpia
        desc_terminos = []
        for i, (coef, offset) in enumerate(terminos):
            if i == 0:
                # Primer término
                if coef == 1:
                    desc_terminos.append(f"T(n-{offset})")
                elif coef == -1:
                    desc_terminos.append(f"-T(n-{offset})")
                else:
                    desc_terminos.append(f"{coef}T(n-{offset})")
            else:
                # Términos subsecuentes
                if coef == 1:
                    desc_terminos.append(f"+ T(n-{offset})")
                elif coef == -1:
                    desc_terminos.append(f"- T(n-{offset})")
                elif coef > 0:
                    desc_terminos.append(f"+ {coef}T(n-{offset})")
                else:
                    desc_terminos.append(f"- {abs(coef)}T(n-{offset})")
        
        ecuacion_limpia = "T(n) = " + " ".join(desc_terminos)
        if f_n != '0':
            ecuacion_limpia += f" + {f_n}"
        
        return {
            'forma': 'lineal_multiple',
            'terminos': terminos,  # [(coef, offset), ...]
            'f_n': f_n,
            'ecuacion_limpia': ecuacion_limpia
        }
    
    def _parsear_divide_conquista(self, ecuacion):
        """
        Parsea ecuaciones de la forma: T(n) = aT(n/b) + f(n)
        
        Ejemplos:
        - T(n)=2T(n/2)+n     → a=2, b=2, f(n)=n
        - T(n)=T(n/2)+1      → a=1, b=2, f(n)=1  (a implícito)
        - T(n)=3T(n/2)+n^2   → a=3, b=2, f(n)=n^2
        """
        # Patrón 1: Con 'a' explícito → T(n)=aT(n/b)+f(n)
        patron1 = r'T\(n\)=(\d+)T\(n/(\d+)\)\+(.*)'
        match = re.match(patron1, ecuacion, re.IGNORECASE)
        
        if match:
            a = int(match.group(1))
            b = int(match.group(2))
            f_n = match.group(3).strip()
            f_n = f_n.replace('^', '**')
            
            return {
                'forma': 'divide_conquista',
                'a': a,
                'b': b,
                'f_n': f_n,
                'ecuacion_limpia': f"T(n) = {a}T(n/{b}) + {f_n}"
            }
        
        # Patrón 2: Sin 'a' explícito (a=1 implícito) → T(n)=T(n/b)+f(n)
        patron2 = r'T\(n\)=T\(n/(\d+)\)\+(.*)'
        match = re.match(patron2, ecuacion, re.IGNORECASE)
        
        if match:
            a = 1  # a implícito
            b = int(match.group(1))
            f_n = match.group(2).strip()
            f_n = f_n.replace('^', '**')
            
            return {
                'forma': 'divide_conquista',
                'a': a,
                'b': b,
                'f_n': f_n,
                'ecuacion_limpia': f"T(n) = T(n/{b}) + {f_n}"
            }
        
        return None
    
    def _parsear_decrementacion(self, ecuacion):
        """
        Parsea ecuaciones de la forma: T(n) = T(n-c) + f(n)
        
        Ejemplos:
        - T(n)=T(n-1)+n
        - T(n)=T(n-1)+1
        - T(n)=T(n-2)+n^2
        """
        patron = r'T\(n\)=T\(n-(\d+)\)\+(.*)'
        match = re.match(patron, ecuacion, re.IGNORECASE)
        
        if match:
            c = int(match.group(1))
            f_n = match.group(2).strip()
            f_n = f_n.replace('^', '**')
            
            return {
                'forma': 'decrementacion',
                'c': c,
                'f_n': f_n,
                'ecuacion_limpia': f"T(n) = T(n-{c}) + {f_n}"
            }
        
        return None
    
    def _parsear_decrementacion_multiple(self, ecuacion):
        """
        Parsea ecuaciones de la forma: T(n) = aT(n-c) + f(n)
        
        Ejemplos:
        - T(n)=2T(n-1)+1    (Torres de Hanoi)
        - T(n)=3T(n-1)+n
        """
        patron = r'T\(n\)=(\d+)T\(n-(\d+)\)\+(.*)'
        match = re.match(patron, ecuacion, re.IGNORECASE)
        
        if match:
            a = int(match.group(1))
            c = int(match.group(2))
            f_n = match.group(3).strip()
            f_n = f_n.replace('^', '**')
            
            return {
                'forma': 'decrementacion_multiple',
                'a': a,
                'c': c,
                'f_n': f_n,
                'ecuacion_limpia': f"T(n) = {a}T(n-{c}) + {f_n}"
            }
        
        return None
    
    def listar_metodos_disponibles(self):
        """
        Lista todos los métodos de resolución disponibles.
        
        Retorna:
        - list de strings con nombres de métodos
        """
        return [metodo.__class__.__name__ for metodo in self.metodos]
    
    def resolver_con_metodo(self, ecuacion_str, nombre_metodo):
        """
        Fuerza el uso de un método específico.
        
        Útil para comparar resultados o cuando se sabe qué método usar.
        
        Parámetros:
        - ecuacion_str: string con la ecuación
        - nombre_metodo: nombre de la clase del método (ej: "TeoremaMAestro")
        
        Retorna:
        - dict con resultado
        """
        ecuacion_parseada = self._parsear_ecuacion(ecuacion_str)
        
        if not ecuacion_parseada:
            return {
                'exito': False,
                'explicacion': f"No se pudo parsear la ecuación: {ecuacion_str}"
            }
        
        for metodo in self.metodos:
            if metodo.__class__.__name__ == nombre_metodo:
                if metodo.puede_resolver(ecuacion_parseada):
                    return metodo.resolver(ecuacion_parseada)
                else:
                    return {
                        'exito': False,
                        'explicacion': f"{nombre_metodo} no puede resolver esta ecuación"
                    }
        
        return {
            'exito': False,
            'explicacion': f"Método '{nombre_metodo}' no encontrado"
        }