import re
from .resolvers.teorema_maestro import TeoremaMAestro
from .resolvers.metodo_sumas import MetodoSumas
from .resolvers.metodo_iteracion import MetodoIteracion
from .resolvers.ecuacion_caracteristica import EcuacionCaracteristica
from .resolvers.arbol_recursion import ArbolRecursion
from .resolvers.analizador_directo import AnalizadorDirecto
from .normalizador import NormalizadorEcuaciones

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
            ArbolRecursion(),  
            AnalizadorDirecto(),  
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
            - ecuacion_normalizada: str (si se aplicaron transformaciones)
            - transformaciones: list (transformaciones aplicadas)
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
            'ecuacion_normalizada': None,
            'transformaciones': [],
            'ecuacion_parseada': None,
            'metodo_usado': None,
            'solucion': None,
            'pasos': [],
            'explicacion': '',
            'intentos': []
        }
        
        # NUEVO: Normalizar ecuación antes de parsear
        normalizacion = NormalizadorEcuaciones.normalizar(ecuacion_str)
        ecuacion_a_parsear = normalizacion['ecuacion_normalizada']
        
        if normalizacion['transformaciones']:
            resultado['ecuacion_normalizada'] = ecuacion_a_parsear
            resultado['transformaciones'] = normalizacion['transformaciones']
            print(f"  >> Normalizaciones aplicadas:")
            for trans in normalizacion['transformaciones']:
                print(f"     - {trans}")
        
        # Paso 1: Parsear la ecuación (ahora la normalizada)
        ecuacion_parseada = self._parsear_ecuacion(ecuacion_a_parsear)
        # Siempre debería retornar algo (al menos expresion_directa)
        if ecuacion_parseada is None:
            ecuacion_parseada = {'forma': 'expresion_directa', 'ecuacion_original': ecuacion_a_parsear}
        resultado['ecuacion_parseada'] = ecuacion_parseada
        
        # Paso 2: Intentar resolver con cada método
        for metodo in self.metodos:
            nombre_metodo = metodo.__class__.__name__
            resultado['intentos'].append(nombre_metodo)
            
            # Verificar si el método puede resolver esta ecuación
            if metodo.puede_resolver(ecuacion_parseada):
                print(f"  >> Intentando con {nombre_metodo}...")
                
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

        # Intentar parsear como sumatoria tipo QuickSort: T(n) = (a/n)*SUM(k=0 to n-1)T(k) + f(n) o con ∑
        resultado = self._parsear_sumatoria_todos(ecuacion)
        if resultado:
            return resultado

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

        # Si no es ninguna recurrencia conocida, asumir expresión directa
        # Para el AnalizadorDirecto
        return {
            'forma': 'expresion_directa',
            'ecuacion_original': ecuacion_str
        }

    def _parsear_sumatoria_todos(self, ecuacion):
        """
        Detecta ecuaciones del tipo T(n) = (a/n)*SUM(k=0 to n-1)T(k) + f(n) o con ∑
        Retorna dict con forma 'sumatoria_todos' si matchea.
        """
        # Permitir SUM o ∑, y a puede ser numérico o simbólico
        # Ejemplo: T(n)=(2/n)*SUM(k=0ton-1)T(k)+c*n
        patron = r'T\(n\)=\(?([a-zA-Z0-9]+)\/n\)?\*?(SUM|∑)\(k=0to(n-1|n−1)\)T\(k\)\+(.+)'  # n−1 unicode
        match = re.match(patron, ecuacion, re.IGNORECASE)
        if match:
            a = match.group(1)
            sum_word = match.group(2)
            f_n = match.group(4)
            f_n = f_n.replace('^', '**')
            return {
                'forma': 'sumatoria_todos',
                'a': a,
                'f_n': f_n,
                'ecuacion_limpia': f"T(n) = ({a}/n)*{sum_word}(k=0 to n-1)T(k) + {f_n}"
            }
        # Variante: permitir espacios y variantes de suma
        patron2 = r'T\(n\)=\(?([a-zA-Z0-9]+)\/n\)?\*?(SUM|∑)\(k=0to(n-1|n−1)\)T\(k\)[\+ ](.+)'  # con espacio antes de +
        match2 = re.match(patron2, ecuacion, re.IGNORECASE)
        if match2:
            a = match2.group(1)
            sum_word = match2.group(2)
            f_n = match2.group(4)
            f_n = f_n.replace('^', '**')
            return {
                'forma': 'sumatoria_todos',
                'a': a,
                'f_n': f_n,
                'ecuacion_limpia': f"T(n) = ({a}/n)*{sum_word}(k=0 to n-1)T(k) + {f_n}"
            }
        return None
        
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
        
        # Si no es ninguna recurrencia conocida, asumir expresión directa
        # Para el AnalizadorDirecto
        return {
            'forma': 'expresion_directa',
            'ecuacion_original': ecuacion_str
        }
    
    def _parsear_division_multiple(self, ecuacion):
        """
        Parsea ecuaciones con múltiples términos de división (asimétricas o múltiples).
        
        Ejemplos:
        - T(n) = T(n/3) + T(2n/3) + n      → asimétrico (diferentes divisores)
        - T(n) = T(n/2) + T(n/4) + T(n/8) + n  → múltiples divisiones
        - T(n) = 2T(n/3) + T(n/2) + n      → combinación
        
        # Permitir espacios opcionales alrededor del asterisco: 2*T(n/2), 2 * T(n/2), etc.
        patron = r'(\d+)\s*\*\s*T\((\d*)n/(\d+)\)|(\d*)T\((\d*)n/(\d+)\)'
        - Todos los términos T(numerador*n/divisor)
        matches = []
        for m in re.finditer(patron, ecuacion, re.IGNORECASE):
            if m.group(1) is not None:
                # Caso con asterisco y posibles espacios: 2 * T(n/2)
                coef = m.group(1)
                num = m.group(2)
                div = m.group(3)
            else:
                # Caso sin asterisco: 2T(n/2)
                coef = m.group(4)
                num = m.group(5)
                div = m.group(6)
            matches.append((coef, num, div))
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
        # Patrón 1: Con 'a' explícito y posible asterisco y espacios → T(n)=a*T(n/b)+f(n) o T(n)=a * T(n/b)+f(n)
        patron1 = r'T\(n\)=(\d+)\s*\*\s*T\(n/(\d+)\)\+(.*)'
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
                'ecuacion_limpia': f"T(n) = {a}*T(n/{b}) + {f_n}"
            }
        # Patrón 2: Con 'a' explícito sin asterisco → T(n)=aT(n/b)+f(n)
        patron2 = r'T\(n\)=(\d+)T\(n/(\d+)\)\+(.*)'
        match = re.match(patron2, ecuacion, re.IGNORECASE)
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
        # Patrón 3: Sin 'a' explícito (a=1 implícito) → T(n)=T(n/b)+f(n)
        patron3 = r'T\(n\)=T\(n/(\d+)\)\+(.*)'
        match = re.match(patron3, ecuacion, re.IGNORECASE)
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
        Ahora acepta: 2T(n-1), 2*T(n-1), 2.T(n-1), 2 * T(n-1), 2 . T(n-1), etc.
        """
        # Quitar espacios para facilitar el parseo
        ecuacion_sin_espacios = ecuacion.replace(' ', '')
        # Patron mejorado: acepta *, . o nada entre el coef y T
        patron = r'T\(n\)\s*=\s*(\d+)\s*[\*\.]?\s*T\(n-(\d+)\)\s*\+\s*(.*)'
        match = re.match(patron, ecuacion_sin_espacios, re.IGNORECASE)
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
    
    def resolver_casos(self, casos):
        """
        Resuelve ecuaciones para los 3 casos: mejor, promedio y peor.
        
        Parámetros:
        - casos: dict con las claves:
            - 'mejor_caso': str con la ecuación del mejor caso
            - 'caso_promedio': str con la ecuación del caso promedio
            - 'peor_caso': str con la ecuación del peor caso
        
        Retorna:
        - dict con:
            - 'mejor_caso': dict con resultado del mejor caso
            - 'caso_promedio': dict con resultado del caso promedio
            - 'peor_caso': dict con resultado del peor caso
            - 'complejidades': dict con las complejidades con notación aplicada
            - 'son_iguales': bool indicando si las 3 complejidades son iguales
            - 'observacion': str con observación sobre los resultados
        """
        resultados = {
            'mejor_caso': None,
            'caso_promedio': None,
            'peor_caso': None,
            'complejidades': {},
            'son_iguales': False,
            'observacion': ''
        }
        
        # Resolver cada caso
        print("\n🔍 Resolviendo mejor caso...")
        resultado_mejor = self.resolver_ecuacion(casos['mejor_caso'])
        resultados['mejor_caso'] = resultado_mejor
        
        print("\n🔍 Resolviendo caso promedio...")
        resultado_promedio = self.resolver_ecuacion(casos['caso_promedio'])
        resultados['caso_promedio'] = resultado_promedio
        
        print("\n🔍 Resolviendo peor caso...")
        resultado_peor = self.resolver_ecuacion(casos['peor_caso'])
        resultados['peor_caso'] = resultado_peor
        
        # Aplicar notaciones asintóticas
        if resultado_mejor['exito']:
            self._detalles_ultimo_resultado = resultado_mejor.get('detalles', {})
            resultados['complejidades']['mejor_caso'] = self._aplicar_notacion(
                resultado_mejor['solucion'],
                'mejor_caso',
                resultado_mejor['metodo_usado']
            )

        if resultado_promedio['exito']:
            self._detalles_ultimo_resultado = resultado_promedio.get('detalles', {})
            resultados['complejidades']['caso_promedio'] = self._aplicar_notacion(
                resultado_promedio['solucion'],
                'caso_promedio',
                resultado_promedio['metodo_usado']
            )

        if resultado_peor['exito']:
            self._detalles_ultimo_resultado = resultado_peor.get('detalles', {})
            resultados['complejidades']['peor_caso'] = self._aplicar_notacion(
                resultado_peor['solucion'],
                'peor_caso',
                resultado_peor['metodo_usado']
            )
        
        # Verificar si las complejidades son iguales
        if len(resultados['complejidades']) == 3:
            son_iguales = self._complejidades_iguales(resultados['complejidades'])
            resultados['son_iguales'] = son_iguales
            
            if son_iguales:
                # Usar Θ para todos si son iguales
                complejidad_base = self._extraer_complejidad_base(
                    resultados['complejidades']['caso_promedio']
                )
                resultados['observacion'] = f"⚠️ Complejidad constante: Θ({complejidad_base}) en todos los casos"
                
                # Actualizar todas con Θ
                resultados['complejidades']['mejor_caso'] = f"Θ({complejidad_base})"
                resultados['complejidades']['caso_promedio'] = f"Θ({complejidad_base})"
                resultados['complejidades']['peor_caso'] = f"Θ({complejidad_base})"
            else:
                # Si son diferentes, forzar la aplicación de notaciones específicas
                resultados['observacion'] = ">> Complejidad variable según la entrada"
                
                # Reaplica notaciones con forzar_cambio=True para casos diferentes
                if resultado_mejor['exito']:
                    resultados['complejidades']['mejor_caso'] = self._aplicar_notacion(
                        resultado_mejor['solucion'],
                        'mejor_caso',
                        resultado_mejor['metodo_usado'],
                        forzar_cambio=True
                    )
                
                if resultado_promedio['exito']:
                    resultados['complejidades']['caso_promedio'] = self._aplicar_notacion(
                        resultado_promedio['solucion'],
                        'caso_promedio',
                        resultado_promedio['metodo_usado'],
                        forzar_cambio=True
                    )
                
                if resultado_peor['exito']:
                    resultados['complejidades']['peor_caso'] = self._aplicar_notacion(
                        resultado_peor['solucion'],
                        'peor_caso',
                        resultado_peor['metodo_usado'],
                        forzar_cambio=True
                    )
        
        return resultados
    
    def _aplicar_notacion(self, solucion, caso_tipo, metodo_usado, forzar_cambio=False):
        """
        Aplica la notación asintótica según el tipo de caso.
        
        Excepción: TeoremaMAestro retorna con Θ, se mantiene a menos que forzar_cambio=True
        
        Parámetros:
        - solucion: str con la solución (ej: "n log n", "n²")
        - caso_tipo: 'mejor_caso', 'caso_promedio' o 'peor_caso'
        - metodo_usado: nombre del método que resolvió
        - forzar_cambio: bool, si True cambia incluso las que tienen Θ del Teorema Maestro
        
        Retorna:
        - str con la notación aplicada
        """
        # Teorema Maestro ya incluye Θ, mantener si no se fuerza cambio
        if metodo_usado == 'TeoremaMAestro' and not forzar_cambio:
            return solucion  # Ya tiene Θ incluida

        # Si el método es EcuacionCaracteristica y hay detalles con raiz_dominante, usar ese término para la notación
        # Se asume que self tiene acceso a los detalles del último resultado (por diseño actual)
        detalles = getattr(self, '_detalles_ultimo_resultado', None)
        if metodo_usado == 'EcuacionCaracteristica' and detalles and 'raiz_dominante' in detalles:
            raiz_dom = detalles['raiz_dominante']
            # Formatear raíz dominante
            def format_raiz(r):
                try:
                    # Si es complejo
                    if isinstance(r, complex):
                        real = round(r.real, 4)
                        imag = round(r.imag, 4)
                        if imag == 0:
                            return f"{real}"
                        elif real == 0:
                            return f"{imag}j"
                        else:
                            signo = '+' if imag > 0 else '-'
                            return f"{real}{signo}{abs(imag)}j"
                    else:
                        # Si es float/int
                        return f"{round(float(r), 4)}"
                except Exception:
                    return str(r)

            raiz_dom_str = format_raiz(raiz_dom)
            exponente_n = detalles.get('exponente_n', 0)
            if exponente_n and exponente_n > 0:
                complejidad_base = f"n^{exponente_n} * {raiz_dom_str}^n"
            else:
                complejidad_base = f"{raiz_dom_str}^n"
        else:
            # Extraer la complejidad base (sin notación previa)
            complejidad_base = self._extraer_complejidad_base(solucion)

        # Aplicar notación según caso
        if caso_tipo == 'mejor_caso':
            return f"Ω({complejidad_base})"
        elif caso_tipo == 'caso_promedio':
            return f"Θ({complejidad_base})"
        elif caso_tipo == 'peor_caso':
            return f"O({complejidad_base})"

        return solucion
    
    def _extraer_complejidad_base(self, solucion):
        """
        Extrae la complejidad sin notación asintótica.
        
        Ejemplos:
        - "Θ(n log n)" → "n log n"
        - "O(n²)" → "n²"
        - "n log n" → "n log n"
        """
        import re
        # Buscar patrón Θ(...), O(...), Ω(...)
        match = re.search(r'[ΘOΩ]\((.+)\)', solucion)
        if match:
            return match.group(1)
        return solucion
    
    def _complejidades_iguales(self, complejidades):
        """
        Verifica si las 3 complejidades son iguales (ignorando la notación).
        
        Parámetros:
        - complejidades: dict con 'mejor_caso', 'caso_promedio', 'peor_caso'
        
        Retorna:
        - bool
        """
        if len(complejidades) != 3:
            return False
        
        # Extraer bases sin notación
        mejor = self._extraer_complejidad_base(complejidades['mejor_caso'])
        promedio = self._extraer_complejidad_base(complejidades['caso_promedio'])
        peor = self._extraer_complejidad_base(complejidades['peor_caso'])
        
        # Normalizar espacios
        mejor = mejor.replace(' ', '')
        promedio = promedio.replace(' ', '')
        peor = peor.replace(' ', '')
        
        return mejor == promedio == peor