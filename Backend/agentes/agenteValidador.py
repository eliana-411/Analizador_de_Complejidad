# agenteValidador.py
import re

class AgenteValidador:
    """
    Agente especializado en validar pseudocódigo completo según la gramática definida.
    
    Responsabilidades:
    - Validar que el pseudocódigo cumpla con la gramática formal
    - Identificar si el algoritmo es iterativo o recursivo
    - Corregir errores cuando sea posible
    - Proveer reportes detallados de validación
    
    Reglas de parámetros según el documento:
    - Arreglos: nombre[] o nombre[n] o nombre[n]..[m] (SIN tipo)
    - Objetos: Clase nombre (CON nombre de clase)
    - Simples: nombre (SIN tipo)
    
    EXTENSIÓN: Sentencia return
    - return valor (retorna un valor)
    - return (retorna sin valor, termina ejecución)
    
    Nota sobre cadenas y grafos:
    - Cadenas: Se representan como arreglos de char
    - Grafos: Se representan como objetos con atributos (Nodo {valor adyacentes})
    """
    
    def __init__(self):
        """Inicializar el validador"""
        self._parametros_actuales = []  # Para guardar parámetros de la subrutina actual
        self._nombre_subrutina_actual = ""  # Para detectar recursividad
        self._pila_bloques = []  # Para validar balance de bloques
        self._subrutinas_definidas = []  # Lista de nombres de subrutinas en el archivo
    
    # ==================== PATRONES DE VALIDACIÓN ====================
    
    # Patrones para estructuras de control (ESTRICTOS)
    patron_for = r'^for\s+\w+\s*🡨\s*.+\s+to\s+.+\s+do$'  # Requiere: for var 🡨 inicio to fin do
    patron_while = r'^while\s*\(.+\)\s*do$'  # Requiere: while (condicion) do
    patron_repeat = r'^repeat|repetir$'
    patron_if = r'^if\s*\(.+\)\s*then$'  # Requiere: if (condicion) then
    patron_else = r'^else$'
    patron_until = r'^until\s*\(.+\)$'  # Requiere: until (condicion)
    
    # Patrones para bloques
    patron_begin = r'^begin$'
    patron_end = r'^end$'
    
    # Patrón para return (NUEVO)
    patron_return = r'^return(\s+.+)?$'
    
    # Patrones para expresiones y operadores
    patron_condicion = r'[\w\s\.\[\]\(\)\<\>\=\≠\≤\≥]+(and|or|not)?[\w\s\.\[\]\(\)\<\>\=\≠\≤\≥]*'
    patron_accion = r'^[\w\s\<\-🡨\+\*/\(\)\[\]\.\=\≠\≤\≥\<\>\{\}\,┌┐└┘]+$'
    patron_asignacion = r'^\w+\s*🡨\s*.+$'
    
    # Patrones para elementos especiales
    patron_comentario = r'^►.*$'
    patron_null = r'\bNULL\b'
    patron_boolean = r'\b(T|F)\b'
    patron_length = r'length\s*\(\s*\w+\s*\)'
    
    # Patrones para estructuras de datos
    patron_rango_arreglo = r'\w+\[\d+\.\.\w+\]'  # A[1..j]
    patron_acceso_arreglo = r'\w+\[\w+\]'  # A[i]
    patron_acceso_objeto = r'\w+\.\w+'  # objeto.campo
    
    # Patrones para subrutinas
    patron_call = r'^CALL\s+\w+\s*\(.+\)$'
    patron_call_sin_params = r'^CALL\s+\w+\s*\(\s*\)$'  # CALL sin parámetros
    patron_subrutina = r'^\w+\s*\([^\)]*\)$'  # nombre_subrutina(params)
    patron_llamada_sin_call = r'^\w+\s*\(.+\)$'  # Detecta llamadas SIN CALL (ERROR)
    
    # Patrones para declaraciones
    patron_declaracion_clase = r'^\w+\s*\{[\w\s]+\}$'  # Casa {area color propietario}
    patron_declaracion_vector = r'^\w+\[\d+\]$'  # nombreVector[tamaño]
    
    # Patrones para PARÁMETROS (según documento: SIN tipos excepto objetos)
    patron_param_arreglo = r'^\w+\[\d*\](\[\d*\])*$'  # A[], A[n], A[5][10]
    patron_param_arreglo_rango = r'^\w+\[\w*\]\.\.\[\w*\]$|^\w+\[\d+\.\.\w+\]$'  # A[n]..[m] o A[1..n]
    patron_param_objeto = r'^[A-Z]\w*\s+\w+$'  # Clase nombre_objeto (Clase empieza con mayúscula)
    patron_param_simple = r'^\w+$'  # Solo nombre (SIN tipo)
    
    # Patrones para DECLARACIONES LOCALES (con o sin tipo)
    patron_declaracion_variable_con_tipo = r'^(int|real|bool)\s+\w+$'  # int i, bool encontrado  
    patron_declaracion_multiple = r'^(int|real|bool)\s+\w+(\s*,\s*\w+)+$'  # int izq, der, medio
    patron_declaracion_multiple_sin_tipo = r'^\w+(\s*,\s*\w+)+$'  # izq, der, medio
    patron_declaracion_vector_con_tipo = r'^(int|real|bool)\s+\w+(\[\w+\])+$'  # int matriz[n][m]
    patron_declaracion_objeto_valida = r'^[A-Z]\w*\s+\w+$'  # Persona p (Clase empieza con mayúscula)
    patron_solo_identificador = r'^\w+$'  # Solo nombre sin tipo (VÁLIDO según lineamientos)
    
    # Patrón para detectar tipos inválidos en parámetros
    patron_tipo_invalido_en_parametro = r'^(int|real|bool|char|string)\s+.+$'
    
    # ==================== MÉTODO PRINCIPAL ====================
    
    def validar_algoritmo_completo(self, pseudocodigo):
        """
        Método principal que valida un pseudocódigo completo.
        
        Entrada:
        - pseudocodigo: string con el algoritmo completo (puede incluir clases)
        
        Salida:
        - dict con:
            - is_valid: bool
            - is_iterative: bool (True si solo ciclos, False si tiene recursión)
            - errors: lista de errores
            - corrected_code: pseudocódigo corregido (si aplica)
            - report: reporte detallado de validación
        """
        resultado = {
            'is_valid': True,
            'is_iterative': None,
            'errors': [],
            'corrected_code': pseudocodigo,
            'report': []
        }
        
        # 1. Limpiar y preparar el código
        lineas = self._limpiar_codigo(pseudocodigo)
        
        # 2. Separar en secciones: clases, subrutinas, algoritmo principal
        secciones = self._separar_secciones(lineas)
        
        # 3. Validar clases (si existen)
        if secciones['clases']:
            for clase in secciones['clases']:
                reporte_clase = self._validar_declaracion_clase(clase)
                resultado['report'].extend(reporte_clase)
                if not all(r[2] for r in reporte_clase):  # Si hay errores
                    resultado['is_valid'] = False
        
        # 4. Extraer nombres de subrutinas definidas (para validar llamadas)
        self._subrutinas_definidas = []
        if secciones['subrutinas']:
            for subrutina_lineas in secciones['subrutinas']:
                if subrutina_lineas:
                    # Extraer nombre del encabezado
                    match = re.match(r'^(\w+)\s*\(', subrutina_lineas[0].strip())
                    if match:
                        self._subrutinas_definidas.append(match.group(1))
        
        # 5. Validar cada subrutina con numeración global
        if secciones['subrutinas']:
            linea_global = len(secciones['clases']) + 1  # Empezar después de las clases
            
            for subrutina_lineas in secciones['subrutinas']:
                # Validar balance de bloques para esta subrutina
                es_balanceado, errores_balance = self.validar_balance_bloques(subrutina_lineas)
                
                if not es_balanceado:
                    # Agregar errores de balance al reporte con líneas ajustadas
                    for num_linea, texto, mensaje in errores_balance:
                        resultado['report'].append((num_linea + linea_global - 1, texto, False, f'Error de estructura: {mensaje}'))
                    resultado['is_valid'] = False
                
                # Validar sintaxis detallada
                reporte_subrutina = self.validar_subrutina(subrutina_lineas, linea_inicio=linea_global)
                resultado['report'].extend(reporte_subrutina)
                if not all(r[2] for r in reporte_subrutina):
                    resultado['is_valid'] = False
                
                # Avanzar el contador global
                linea_global += len(subrutina_lineas)
        
        # 6. Detectar si es iterativo o recursivo
        resultado['is_iterative'] = self._detectar_tipo_algoritmo(lineas)
        
        # 7. Extraer errores del reporte
        resultado['errors'] = [r for r in resultado['report'] if not r[2]]
        
        return resultado
    
    # ==================== MÉTODOS AUXILIARES DE PROCESAMIENTO ====================
    
    def _limpiar_codigo(self, pseudocodigo):
        """
        Limpia el código: elimina líneas vacías, normaliza espacios, separa en líneas.
        """
        lineas = pseudocodigo.split('\n')
        lineas_limpias = []
        
        for linea in lineas:
            # Ignorar comentarios completos
            if re.match(self.patron_comentario, linea.strip()):
                continue
            
            # Remover comentarios al final de línea
            if '►' in linea:
                linea = linea.split('►')[0]
            
            # Ignorar líneas vacías
            linea = linea.strip()
            if linea:
                lineas_limpias.append(linea)
        
        return lineas_limpias
    
    def _separar_secciones(self, lineas):
        """
        Separa el pseudocódigo en: clases y múltiples subrutinas.
        
        Retorna dict con:
        - clases: lista de líneas de declaraciones de clases
        - subrutinas: lista de subrutinas, cada una con sus líneas
        """
        secciones = {
            'clases': [],
            'subrutinas': []  # Cambiado de 'subrutina' a 'subrutinas' (lista)
        }
        
        idx = 0
        
        # 1. Extraer clases (antes de cualquier subrutina)
        while idx < len(lineas):
            if re.match(self.patron_declaracion_clase, lineas[idx]):
                secciones['clases'].append(lineas[idx])
                idx += 1
            else:
                break
        
        # 2. Extraer múltiples subrutinas
        while idx < len(lineas):
            # Detectar inicio de subrutina (nombre seguido de paréntesis)
            if re.match(self.patron_subrutina, lineas[idx].strip()):
                inicio_subrutina = idx
                
                # Buscar el END que cierra esta subrutina
                # Contamos BEGIN/END para encontrar el cierre correcto
                nivel_begin = 0
                idx += 1  # Saltar el encabezado
                
                # Debe haber un BEGIN después del encabezado
                if idx < len(lineas) and re.match(self.patron_begin, lineas[idx].strip()):
                    nivel_begin = 1
                    idx += 1
                    
                    # Buscar hasta encontrar el END que balancea el BEGIN inicial
                    while idx < len(lineas) and nivel_begin > 0:
                        if re.match(self.patron_begin, lineas[idx].strip()):
                            nivel_begin += 1
                        elif re.match(self.patron_end, lineas[idx].strip()):
                            nivel_begin -= 1
                        idx += 1
                    
                    # Extraer la subrutina completa
                    subrutina_completa = lineas[inicio_subrutina:idx]
                    secciones['subrutinas'].append(subrutina_completa)
                else:
                    # Error: no hay BEGIN después del encabezado
                    # Incluimos solo el encabezado como subrutina incompleta
                    secciones['subrutinas'].append([lineas[inicio_subrutina]])
                    idx += 1
            else:
                # Línea que no es inicio de subrutina, saltarla
                idx += 1
        
        return secciones
    
    def _detectar_tipo_algoritmo(self, lineas):
        """
        Detecta si el algoritmo es iterativo o recursivo.
        
        Retorna:
        - True: si es iterativo (solo tiene ciclos)
        - False: si es recursivo (tiene llamadas recursivas)
        """
        # Buscar llamadas CALL en cualquier parte de la línea
        for linea in lineas:
            # Patrón más flexible: busca CALL seguido de nombre y paréntesis
            # No importa si está al inicio o en medio de una expresión
            matches = re.finditer(r'CALL\s+(\w+)\s*\(', linea)
            
            for match in matches:
                nombre_llamado = match.group(1)
                # Verificar si es una llamada recursiva
                if nombre_llamado == self._nombre_subrutina_actual:
                    return False  # Es recursivo
        
        # Si no hay llamadas recursivas, es iterativo
        return True
    
    def _validar_declaracion_clase(self, linea):
        """
        Valida una declaración de clase.
        Formato: NombreClase {atributo1 atributo2 ...}
        Ejemplo: Nodo {valor izquierdo derecho}
        
        Retorna: lista de tuplas (num_linea, texto, es_valido, mensaje)
        """
        linea = linea.strip()
        
        if re.match(self.patron_declaracion_clase, linea):
            # Extraer nombre de clase y atributos
            match = re.match(r'^(\w+)\s*\{([\w\s]+)\}$', linea)
            if match:
                nombre_clase = match.group(1)
                atributos = match.group(2).strip().split()
                return [(1, linea, True, f'Declaración de clase válida: {nombre_clase} con {len(atributos)} atributos')]
            else:
                return [(1, linea, False, 'Formato de clase inválido')]
        else:
            return [(1, linea, False, 'Declaración de clase inválida')]
    
    def validar_declaracion_local(self, linea):
        """
        Valida declaraciones locales dentro de subrutinas.
        """
        linea = linea.strip()
        
        # PRIMERO: Detectar declaraciones múltiples MAL FORMADAS
        # Si hay múltiples palabras sin comas y sin operadores, es un error
        palabras = linea.split()
        if len(palabras) > 1 and ',' not in linea and '🡨' not in linea:
            # Verificar si parece ser una declaración múltiple sin comas
            # Excepto cuando es una declaración con tipo o de objeto
            if not re.match(r'^(int|real|bool)\s+', linea) and not re.match(self.patron_declaracion_objeto_valida, linea):
                return (False, 'Declaración múltiple requiere comas entre variables', 'declaracion_invalida')
        
        # Verificar si es declaración múltiple con tipo (int izq, der, medio)
        if re.match(self.patron_declaracion_multiple, linea):
            return (True, 'Declaración múltiple válida', 'declaracion')
        
        # Verificar si es declaración múltiple sin tipo (izq, der, medio)
        if re.match(self.patron_declaracion_multiple_sin_tipo, linea):
            return (True, 'Declaración múltiple válida', 'declaracion')
        
        # Verificar si es declaración de variable simple con tipo
        if re.match(self.patron_declaracion_variable_con_tipo, linea):
            return (True, 'Declaración de variable válida', 'declaracion')
        
        # Verificar si es declaración de vector con tipo
        if re.match(self.patron_declaracion_vector_con_tipo, linea):
            return (True, 'Declaración de vector válida', 'declaracion')
        
        # Verificar si es declaración de vector sin tipo (nombreVector[tamaño])
        if re.match(self.patron_declaracion_vector, linea):
            return (True, 'Declaración de vector válida', 'declaracion')
        
        # Verificar si es declaración de objeto (válida)
        if re.match(self.patron_declaracion_objeto_valida, linea):
            # Verificar que no sea una asignación disfrazada
            if '🡨' not in linea:
                return (True, 'Declaración de objeto válida', 'declaracion')
        
        # Verificar si es variable simple SIN tipo (VÁLIDO según lineamientos)
        if re.match(self.patron_solo_identificador, linea):
            return (True, 'Declaración de variable válida', 'declaracion')
        
        return (None, None, 'no_es_declaracion')
    
    # ==================== VALIDACIÓN DE PARÁMETROS ====================
    
    def validar_parametros_subrutina(self, encabezado):
        """
        Valida los parámetros de una subrutina según las reglas del proyecto.
        
        REGLAS DEL DOCUMENTO:
        - Arreglos: nombre[] o nombre[n]..[m] (SIN tipo)
        - Objetos: Clase nombre (CON nombre de clase)
        - Simples: nombre (SIN tipo)
        
        Entrada:
        - encabezado: string del encabezado de la subrutina (ej: "busqueda(A[], x, n)")
        
        Salida:
        - (bool, str, list): (es_valido, mensaje, lista_parametros)
        """
        # Extraer nombre de subrutina y parámetros
        match = re.match(r'^(\w+)\s*\(([^\)]*)\)$', encabezado.strip())
        
        if not match:
            return (False, "Formato de encabezado inválido", [])
        
        nombre_subrutina = match.group(1)
        params_str = match.group(2).strip()
        
        # Guardar nombre de subrutina para detectar recursividad
        self._nombre_subrutina_actual = nombre_subrutina
        
        # Si no hay parámetros
        if not params_str:
            return (True, f"Subrutina '{nombre_subrutina}' sin parámetros (válido)", [])
        
        # Separar parámetros por comas
        parametros = [p.strip() for p in params_str.split(',')]
        parametros_validados = []
        errores = []
        
        for idx, param in enumerate(parametros, 1):
            tipo_param, mensaje_error = self._clasificar_parametro(param)
            
            if tipo_param == 'invalido':
                errores.append(f"Parámetro {idx} '{param}': {mensaje_error}")
            else:
                parametros_validados.append({
                    'nombre': param,
                    'tipo': tipo_param,
                    'posicion': idx
                })
        
        if errores:
            return (False, "; ".join(errores), parametros_validados)
        
        return (True, f"Subrutina '{nombre_subrutina}' con {len(parametros)} parámetros válidos", parametros_validados)
    
    def _clasificar_parametro(self, param):
        """
        Clasifica un parámetro según su tipo usando las reglas del documento.
        
        REGLAS:
        - Arreglos: A[], A[n], A[n]..[m] (SIN tipo de dato)
        - Objetos: Clase nombre (CON nombre de clase que empieza con mayúscula)
        - Simples: nombre (SIN tipo de dato)
        
        Retorna: (tipo, mensaje_error)
        - tipo: 'arreglo', 'objeto', 'simple', o 'invalido'
        - mensaje_error: descripción del error si es inválido
        """
        param = param.strip()
        
        # DETECTAR ERROR: tipo de dato en parámetro simple o arreglo
        if re.match(self.patron_tipo_invalido_en_parametro, param):
            # Verificar si tiene corchetes (intento de arreglo con tipo)
            if '[' in param:
                return ('invalido', 'Los arreglos NO deben llevar tipo de dato. Use: A[] o A[n]')
            else:
                return ('invalido', 'Los parámetros simples NO deben llevar tipo de dato. Use solo: nombre')
        
        # Verificar si es un arreglo con rango (A[n]..[m] o A[1..n])
        if re.match(self.patron_param_arreglo_rango, param):
            return ('arreglo', None)
        
        # Verificar si es un arreglo simple (A[], A[n], A[5][10])
        if re.match(self.patron_param_arreglo, param):
            return ('arreglo', None)
        
        # Verificar si es un objeto (Clase nombre)
        if re.match(self.patron_param_objeto, param):
            return ('objeto', None)
        
        # Verificar si es un parámetro simple (solo identificador)
        if re.match(self.patron_param_simple, param):
            return ('simple', None)
        
        # Si no coincide con ningún patrón válido
        return ('invalido', 'Formato de parámetro no reconocido')
    
    # ==================== VALIDACIÓN DE ESTRUCTURA DE BLOQUES ====================
    
    def validar_balance_bloques(self, lineas):
        """
        Valida que todos los bloques estén correctamente balanceados.
        
        REGLAS DE LA GRAMÁTICA:
        - BEGIN siempre requiere END
        - IF-THEN y IF-THEN-ELSE NO requieren END propio (se cierran con los END de sus bloques internos)
        - WHILE-DO requiere BEGIN-END internos
        - FOR-DO requiere BEGIN-END internos
        - REPEAT-UNTIL NO requiere BEGIN-END (las acciones van directo)
        
        Retorna: (bool, list) - (es_valido, lista_errores)
        """
        pila = []  # Pila de bloques abiertos: [(tipo, linea_num)]
        errores = []
        
        for idx, linea in enumerate(lineas, start=1):
            linea_limpia = linea.strip()
            
            # Detectar apertura de bloques que SOLO requieren seguimiento (no cierres explícitos)
            if re.match(self.patron_if, linea_limpia):
                # IF no va a la pila porque no requiere END propio
                pass
            
            elif re.match(self.patron_while, linea_limpia):
                # WHILE tampoco requiere END propio, solo sus BEGIN internos
                pass
            
            elif re.match(self.patron_for, linea_limpia):
                # FOR tampoco requiere END propio, solo sus BEGIN internos
                pass
            
            elif re.match(self.patron_repeat, linea_limpia):
                # REPEAT sí requiere UNTIL para cerrarse
                pila.append(('REPEAT', idx))
            
            elif re.match(self.patron_begin, linea_limpia):
                # BEGIN siempre requiere END
                pila.append(('BEGIN', idx))
            
            # Detectar ELSE
            elif re.match(self.patron_else, linea_limpia):
                # ELSE es válido, no necesita validación especial de pila
                # porque es parte del IF que no requiere cierre
                pass
            
            # Detectar cierre de bloques
            elif re.match(self.patron_end, linea_limpia):
                if not pila:
                    errores.append((idx, linea, 'END sin BEGIN correspondiente'))
                else:
                    tipo_cerrado, linea_apertura = pila.pop()
                    # El END debe cerrar un BEGIN
                    if tipo_cerrado != 'BEGIN':
                        errores.append((idx, linea, f'END encontrado pero se esperaba cierre de {tipo_cerrado} (línea {linea_apertura})'))
            
            elif re.match(self.patron_until, linea_limpia):
                # UNTIL debe cerrar un REPEAT
                if not pila:
                    errores.append((idx, linea, 'UNTIL sin REPEAT correspondiente'))
                else:
                    # Buscamos el REPEAT en la pila
                    encontrado = False
                    temp_pila = []
                    
                    while pila:
                        tipo, linea_num = pila.pop()
                        if tipo == 'REPEAT':
                            encontrado = True
                            # Restauramos lo que sacamos (si había BEGIN sin cerrar dentro del REPEAT)
                            while temp_pila:
                                pila.append(temp_pila.pop())
                            break
                        else:
                            temp_pila.append((tipo, linea_num))
                    
                    if not encontrado:
                        # Restauramos todo y reportamos error
                        while temp_pila:
                            pila.append(temp_pila.pop())
                        errores.append((idx, linea, 'UNTIL sin REPEAT correspondiente'))
        
        # Verificar que no queden bloques sin cerrar
        for tipo, linea_num in pila:
            if tipo == 'BEGIN':
                errores.append((len(lineas) + 1, '', f'BEGIN sin cerrar (abierto en línea {linea_num})'))
            elif tipo == 'REPEAT':
                errores.append((len(lineas) + 1, '', f'REPEAT sin UNTIL (abierto en línea {linea_num})'))
        
        return (len(errores) == 0, errores)
    
    # ==================== VALIDADORES DE BLOQUES ====================
    
    def validar_asignacion_unica(self, linea):
        """
        Valida que en una línea solo haya una asignación (un solo símbolo 🡨).
        """
        count = linea.count('🡨')
        return count <= 1

    def validar_operadores_matematicos(self, linea):
        """
        Valida que 'mod' y 'div' estén usados como operadores (con espacios alrededor).
        """
        linea = linea.strip()
        
        patron_mod_valido = r'\b\w+\s+mod\s+\w+\b'
        patron_div_valido = r'\b\w+\s+div\s+\w+\b'
        patron_mod_invalido = r'\w*mod\w+|\w+mod\w*'
        patron_div_invalido = r'\w*div\w+|\w+div\w*'
        
        if 'mod' in linea.lower():
            if re.search(patron_mod_invalido, linea, re.IGNORECASE) and not re.search(patron_mod_valido, linea, re.IGNORECASE):
                return (False, "'mod' debe usarse como operador: a mod b")
        
        if 'div' in linea.lower():
            if re.search(patron_div_invalido, linea, re.IGNORECASE) and not re.search(patron_div_valido, linea, re.IGNORECASE):
                return (False, "'div' debe usarse como operador: a div b")
        
        return (True, 'Operadores matemáticos válidos')
    
    def validar_return(self, linea):
        """
        Valida una sentencia return.
        
        Formatos válidos:
        - return valor
        - return expresion
        - return CALL funcion(params)
        - return (sin valor)
        """
        linea = linea.strip()
        
        if re.match(self.patron_return, linea):
            return (True, 'Sentencia return válida')
        
        return (False, 'Sentencia return inválida')

    def validar_declaracion_local(self, linea):
        """
        Valida declaraciones locales dentro de subrutinas.
        
        Según lineamientos del proyecto:
        - Variables simples: con o sin tipo (i, int i, bool encontrado) ✓
        - Declaración múltiple: int izq, der, medio o izq, der, medio ✓
        - Vectores locales: nombreVector[tamaño] ✓
        - Objetos: Clase nombre_objeto ✓
        """
        linea = linea.strip()
        
        # Verificar si es declaración múltiple con tipo (int izq, der, medio)
        if re.match(self.patron_declaracion_multiple, linea):
            return (True, 'Declaración múltiple válida', 'declaracion')
        
        # Verificar si es declaración múltiple sin tipo (izq, der, medio)
        if re.match(self.patron_declaracion_multiple_sin_tipo, linea):
            return (True, 'Declaración múltiple válida', 'declaracion')
        
        # Verificar si es declaración de variable simple con tipo
        if re.match(self.patron_declaracion_variable_con_tipo, linea):
            return (True, 'Declaración de variable válida', 'declaracion')
        
        # Verificar si es declaración de vector con tipo
        if re.match(self.patron_declaracion_vector_con_tipo, linea):
            return (True, 'Declaración de vector válida', 'declaracion')
        
        # Verificar si es declaración de vector sin tipo (nombreVector[tamaño])
        if re.match(self.patron_declaracion_vector, linea):
            return (True, 'Declaración de vector válida', 'declaracion')
        
        # Verificar si es declaración de objeto (válida)
        if re.match(self.patron_declaracion_objeto_valida, linea):
            # Verificar que no sea una asignación disfrazada
            if '🡨' not in linea:
                return (True, 'Declaración de objeto válida', 'declaracion')
        
        # Verificar si es variable simple SIN tipo (VÁLIDO según lineamientos)
        if re.match(self.patron_solo_identificador, linea):
            return (True, 'Declaración de variable válida', 'declaracion')
        
        return (None, None, 'no_es_declaracion')  # No es declaración, puede ser otra cosa

    def validar_declaracion_vector(self, linea):
        """
        Valida declaración de vector: nombreVector[tamaño] o matriz[n][m]
        """
        linea = linea.strip()
        patron_1d = r'^\w+\[\d+\]$'
        patron_multi = r'^\w+(\[\d+\])+$'
        
        if re.match(patron_1d, linea) or re.match(patron_multi, linea):
            return (True, 'Declaración de vector válida')
        return (False, 'Declaración de vector inválida')

    def validar_call(self, linea):
        """
        Valida llamada a subrutina: CALL nombre_subrutina(param1, param2, ...)
        """
        linea = linea.strip()
        if re.match(self.patron_call, linea) or re.match(self.patron_call_sin_params, linea):
            return (True, 'Llamada CALL válida')
        return (False, 'Llamada CALL inválida')

    def validar_llamada_subrutina(self, linea):
        """
        Valida que las llamadas a subrutinas usen CALL.
        
        Detecta patrones como:
        - funcion(a, b) ✗ (falta CALL si funcion está definida en el archivo)
        - CALL funcion(a, b) ✓
        - length(A) ✓ (función built-in)
        
        Retorna: (bool, str)
        """
        linea = linea.strip()
        
        # Si tiene CALL, está bien
        if linea.startswith('CALL '):
            return (True, 'Llamada con CALL correcta')
        
        # Funciones built-in que NO requieren CALL
        funciones_builtin = ['length']
        
        # Si parece una llamada a función (nombre seguido de paréntesis con contenido)
        # pero NO empieza con CALL
        if re.match(self.patron_llamada_sin_call, linea):
            # Extraer nombre de la función
            match = re.match(r'^(\w+)\s*\(', linea)
            if match:
                nombre_funcion = match.group(1)
                
                # Si es función built-in, está bien
                if nombre_funcion in funciones_builtin:
                    return (True, f'Llamada a función built-in: {nombre_funcion}')
                
                # Si está definida en el archivo, requiere CALL
                if nombre_funcion in self._subrutinas_definidas:
                    return (False, f'Llamada a subrutina sin CALL: debe ser "CALL {nombre_funcion}(...)"')
                
                # Si no está definida, asumimos que es externa o válida
                # (podría ser una función de librería o error de otro tipo)
                return (True, f'Llamada a función externa o built-in: {nombre_funcion}')
        
        return (True, 'No es una llamada a subrutina')

    def validar_for(self, lineas):
        """
        Valida un bloque FOR completo.
        Formato: for variable 🡨 valorInicial to limite do
        """
        reportes = []
        if len(lineas) < 3:
            reportes.append((1, '', False, 'El bloque FOR es demasiado corto'))
            return reportes
        
        # Encabezado FOR - Validación estricta
        encabezado = lineas[0].strip()
        if re.match(self.patron_for, encabezado):
            reportes.append((1, lineas[0], True, 'Encabezado FOR válido'))
        else:
            # Diagnóstico de error específico
            error_msg = 'Encabezado FOR inválido. '
            if not encabezado.startswith('for '):
                error_msg += 'Debe empezar con "for"'
            elif '🡨' not in encabezado:
                error_msg += 'Falta símbolo de asignación 🡨'
            elif ' to ' not in encabezado:
                error_msg += 'Falta palabra clave "to"'
            elif not encabezado.endswith(' do'):
                error_msg += 'Debe terminar con "do"'
            else:
                error_msg += 'Formato: for variable 🡨 valorInicial to limite do'
            reportes.append((1, lineas[0], False, error_msg))
        
        # BEGIN
        if re.match(self.patron_begin, lineas[1].strip()):
            reportes.append((2, lineas[1], True, 'BEGIN válido'))
        else:
            reportes.append((2, lineas[1], False, 'Se esperaba BEGIN'))
        
        # END
        if re.match(self.patron_end, lineas[-1].strip()):
            reportes.append((len(lineas), lineas[-1], True, 'END válido'))
        else:
            reportes.append((len(lineas), lineas[-1], False, 'Se esperaba END'))
        
        return reportes

    def validar_while(self, lineas):
        """
        Valida un bloque WHILE completo.
        Formato: while (condicion) do
        """
        reportes = []
        if len(lineas) < 3:
            reportes.append((1, '', False, 'El bloque WHILE es demasiado corto'))
            return reportes
        
        # Encabezado WHILE - Validación estricta
        encabezado = lineas[0].strip()
        if re.match(self.patron_while, encabezado):
            reportes.append((1, lineas[0], True, 'Encabezado WHILE válido'))
        else:
            # Diagnóstico de error específico
            error_msg = 'Encabezado WHILE inválido. '
            if not encabezado.startswith('while '):
                error_msg += 'Debe empezar con "while"'
            elif '(' not in encabezado or ')' not in encabezado:
                error_msg += 'La condición debe estar entre paréntesis'
            elif not encabezado.endswith(' do'):
                error_msg += 'Debe terminar con "do"'
            else:
                error_msg += 'Formato: while (condicion) do'
            reportes.append((1, lineas[0], False, error_msg))
        
        # BEGIN
        if re.match(self.patron_begin, lineas[1].strip()):
            reportes.append((2, lineas[1], True, 'BEGIN válido'))
        else:
            reportes.append((2, lineas[1], False, 'Se esperaba BEGIN'))
        
        # Validación de acciones internas
        for idx, linea in enumerate(lineas[2:-1], start=3):
            if not self.validar_asignacion_unica(linea):
                reportes.append((idx, linea, False, 'Asignación múltiple no permitida'))
            else:
                valido_op, mensaje_op = self.validar_operadores_matematicos(linea)
                if not valido_op:
                    reportes.append((idx, linea, False, mensaje_op))
                elif re.match(self.patron_accion, linea.strip()):
                    reportes.append((idx, linea, True, 'Acción válida'))
                else:
                    reportes.append((idx, linea, False, 'Acción inválida'))
        
        # END
        if re.match(self.patron_end, lineas[-1].strip()):
            reportes.append((len(lineas), lineas[-1], True, 'END válido'))
        else:
            reportes.append((len(lineas), lineas[-1], False, 'Se esperaba END'))
        
        return reportes

    def validar_repeat(self, lineas):
        """
        Valida un bloque REPEAT completo.
        """
        reportes = []
        if len(lineas) < 3:
            reportes.append((1, '', False, 'El bloque REPEAT es demasiado corto'))
            return reportes
        
        # REPEAT
        if re.match(self.patron_repeat, lineas[0].strip()):
            reportes.append((1, lineas[0], True, 'REPEAT válido'))
        else:
            reportes.append((1, lineas[0], False, 'Falta o sintaxis incorrecta en REPEAT'))
        
        # Acciones
        for idx, linea in enumerate(lineas[1:-1], start=2):
            if not self.validar_asignacion_unica(linea):
                reportes.append((idx, linea, False, 'Asignación múltiple no permitida'))
            else:
                valido_op, mensaje_op = self.validar_operadores_matematicos(linea)
                if not valido_op:
                    reportes.append((idx, linea, False, mensaje_op))
                elif re.match(self.patron_accion, linea.strip()):
                    reportes.append((idx, linea, True, 'Acción válida'))
                else:
                    reportes.append((idx, linea, False, 'Acción inválida'))
        
        # UNTIL
        if re.match(self.patron_until, lineas[-1].strip()):
            reportes.append((len(lineas), lineas[-1], True, 'UNTIL válido'))
        else:
            reportes.append((len(lineas), lineas[-1], False, 'Falta o sintaxis incorrecta en UNTIL'))
        
        return reportes

    def validar_if(self, lineas):
        """
        Valida un bloque IF-ELSE completo.
        Formato: if (condicion) then
        """
        reportes = []
        if len(lineas) < 4:
            reportes.append((1, '', False, 'El bloque IF es demasiado corto'))
            return reportes
        
        # Encabezado IF - Validación estricta
        encabezado = lineas[0].strip()
        if re.match(self.patron_if, encabezado):
            reportes.append((1, lineas[0], True, 'IF válido'))
        else:
            # Diagnóstico de error específico
            error_msg = 'Encabezado IF inválido. '
            if not encabezado.startswith('if '):
                error_msg += 'Debe empezar con "if"'
            elif '(' not in encabezado or ')' not in encabezado:
                error_msg += 'La condición debe estar entre paréntesis'
            elif not encabezado.endswith(' then'):
                error_msg += 'Debe terminar con "then"'
            else:
                error_msg += 'Formato: if (condicion) then'
            reportes.append((1, lineas[0], False, error_msg))

        # BEGIN del IF
        if re.match(self.patron_begin, lineas[1].strip()):
            reportes.append((2, lineas[1], True, 'BEGIN válido'))
        else:
            reportes.append((2, lineas[1], False, 'Se esperaba BEGIN'))

        # Acciones bloque IF
        idx = 2
        while idx < len(lineas) and not re.match(self.patron_end, lineas[idx].strip()):
            if not self.validar_asignacion_unica(lineas[idx]):
                reportes.append((idx+1, lineas[idx], False, 'Asignación múltiple no permitida'))
            else:
                valido_op, mensaje_op = self.validar_operadores_matematicos(lineas[idx])
                if not valido_op:
                    reportes.append((idx+1, lineas[idx], False, mensaje_op))
                elif re.match(self.patron_accion, lineas[idx].strip()):
                    reportes.append((idx+1, lineas[idx], True, 'Acción válida'))
                else:
                    reportes.append((idx+1, lineas[idx], False, 'Acción inválida'))
            idx += 1
        
        # END del IF
        if idx < len(lineas) and re.match(self.patron_end, lineas[idx].strip()):
            reportes.append((idx+1, lineas[idx], True, 'END válido'))
            idx += 1
        else:
            reportes.append((idx+1, '', False, 'Se esperaba END'))

        # Verificar si hay ELSE
        if idx < len(lineas) and re.match(self.patron_else, lineas[idx].strip()):
            reportes.append((idx+1, lineas[idx], True, 'ELSE válido'))
            idx += 1
            
            # BEGIN del ELSE
            if re.match(self.patron_begin, lineas[idx].strip()):
                reportes.append((idx+1, lineas[idx], True, 'BEGIN válido'))
            else:
                reportes.append((idx+1, lineas[idx], False, 'Se esperaba BEGIN'))
            idx += 1
            
            # Acciones bloque ELSE
            while idx < len(lineas) and not re.match(self.patron_end, lineas[idx].strip()):
                if not self.validar_asignacion_unica(lineas[idx]):
                    reportes.append((idx+1, lineas[idx], False, 'Asignación múltiple no permitida'))
                else:
                    valido_op, mensaje_op = self.validar_operadores_matematicos(lineas[idx])
                    if not valido_op:
                        reportes.append((idx+1, lineas[idx], False, mensaje_op))
                    elif re.match(self.patron_accion, lineas[idx].strip()):
                        reportes.append((idx+1, lineas[idx], True, 'Acción válida'))
                    else:
                        reportes.append((idx+1, lineas[idx], False, 'Acción inválida'))
                idx += 1
            
            # END del ELSE
            if idx < len(lineas) and re.match(self.patron_end, lineas[idx].strip()):
                reportes.append((idx+1, lineas[idx], True, 'END válido'))
            else:
                reportes.append((idx+1, '', False, 'Se esperaba END'))

        return reportes

    def validar_subrutina(self, lineas, linea_inicio=1):
        """
        Valida una subrutina completa: nombre(params) begin ... end
        
        Parámetros:
        - lineas: lista de líneas de la subrutina
        - linea_inicio: número de línea global donde empieza esta subrutina en el archivo original
        """
        reportes = []
        if len(lineas) < 3:
            reportes.append((linea_inicio, '', False, 'El bloque de subrutina es demasiado corto'))
            return reportes
        
        # ===== VALIDACIÓN MEJORADA DEL ENCABEZADO =====
        encabezado = lineas[0].strip()
        es_valido, mensaje, parametros = self.validar_parametros_subrutina(encabezado)
        
        if es_valido:
            reportes.append((linea_inicio, lineas[0], True, f'Encabezado de subrutina válido: {mensaje}'))
            self._parametros_actuales = parametros
        else:
            reportes.append((linea_inicio, lineas[0], False, f'Encabezado de subrutina inválido: {mensaje}'))
            self._parametros_actuales = []
        
        # BEGIN
        if re.match(self.patron_begin, lineas[1].strip()):
            reportes.append((linea_inicio + 1, lineas[1], True, 'BEGIN válido'))
        else:
            reportes.append((linea_inicio + 1, lineas[1], False, 'Se esperaba BEGIN'))
        
        # ===== VALIDACIÓN DE ACCIONES INTERNAS =====
        en_seccion_declaraciones = True
        
        for idx, linea in enumerate(lineas[2:-1], start=linea_inicio + 2):
            linea_limpia = linea.strip()
            
            # ===== PRIMERO: Detectar estructuras de control y palabras clave =====
            # Estas NO son declaraciones y terminan la sección de declaraciones
            
            # Estructuras de control - VALIDACIÓN ESTRICTA
            
            # IF: debe tener formato "if (condicion) then"
            if linea_limpia.startswith('if '):
                en_seccion_declaraciones = False
                if re.match(self.patron_if, linea_limpia):
                    reportes.append((idx, linea, True, 'IF válido'))
                else:
                    # Diagnosticar error específico
                    error_msg = 'IF inválido. '
                    if '(' not in linea_limpia or ')' not in linea_limpia:
                        error_msg += 'La condición debe estar entre paréntesis'
                    elif not linea_limpia.endswith(' then'):
                        error_msg += 'Debe terminar con "then"'
                    else:
                        error_msg += 'Formato: if (condicion) then'
                    reportes.append((idx, linea, False, error_msg))
                continue
            
            if re.match(self.patron_else, linea_limpia):
                en_seccion_declaraciones = False
                reportes.append((idx, linea, True, 'ELSE válido'))
                continue
            
            # WHILE: debe tener formato "while (condicion) do"
            if linea_limpia.startswith('while '):
                en_seccion_declaraciones = False
                if re.match(self.patron_while, linea_limpia):
                    reportes.append((idx, linea, True, 'WHILE válido'))
                else:
                    # Diagnosticar error específico
                    error_msg = 'WHILE inválido. '
                    if '(' not in linea_limpia or ')' not in linea_limpia:
                        error_msg += 'La condición debe estar entre paréntesis'
                    elif not linea_limpia.endswith(' do'):
                        error_msg += 'Debe terminar con "do"'
                    else:
                        error_msg += 'Formato: while (condicion) do'
                    reportes.append((idx, linea, False, error_msg))
                continue
            
            # FOR: debe tener formato "for variable 🡨 valorInicial to limite do"
            if linea_limpia.startswith('for '):
                en_seccion_declaraciones = False
                if re.match(self.patron_for, linea_limpia):
                    reportes.append((idx, linea, True, 'FOR válido'))
                else:
                    # Diagnosticar error específico
                    error_msg = 'FOR inválido. '
                    if '🡨' not in linea_limpia:
                        error_msg += 'Falta símbolo de asignación 🡨'
                    elif ' to ' not in linea_limpia:
                        error_msg += 'Falta palabra clave "to"'
                    elif not linea_limpia.endswith(' do'):
                        error_msg += 'Debe terminar con "do"'
                    else:
                        error_msg += 'Formato: for variable 🡨 valorInicial to limite do'
                    reportes.append((idx, linea, False, error_msg))
                continue
            
            if re.match(self.patron_repeat, linea_limpia):
                en_seccion_declaraciones = False
                reportes.append((idx, linea, True, 'REPEAT válido'))
                continue
            
            if re.match(self.patron_until, linea_limpia):
                en_seccion_declaraciones = False
                reportes.append((idx, linea, True, 'UNTIL válido'))
                continue
            
            # BEGIN y END internos
            if re.match(self.patron_begin, linea_limpia):
                en_seccion_declaraciones = False
                reportes.append((idx, linea, True, 'BEGIN válido'))
                continue
            
            if re.match(self.patron_end, linea_limpia):
                en_seccion_declaraciones = False
                reportes.append((idx, linea, True, 'END válido'))
                continue
            
            # Return
            if re.match(self.patron_return, linea_limpia):
                en_seccion_declaraciones = False
                valido_ret, mensaje_ret = self.validar_return(linea_limpia)
                if valido_ret:
                    reportes.append((idx, linea, True, mensaje_ret))
                else:
                    reportes.append((idx, linea, False, mensaje_ret))
                continue
            
            # CALL
            if re.match(self.patron_call, linea_limpia) or re.match(self.patron_call_sin_params, linea_limpia):
                en_seccion_declaraciones = False
                valido_call, mensaje_call = self.validar_call(linea_limpia)
                if valido_call:
                    reportes.append((idx, linea, True, mensaje_call))
                else:
                    reportes.append((idx, linea, False, mensaje_call))
                continue
            
            # Asignaciones (terminan sección de declaraciones)
            if '🡨' in linea_limpia:
                en_seccion_declaraciones = False
                if not self.validar_asignacion_unica(linea):
                    reportes.append((idx, linea, False, 'Asignación múltiple no permitida'))
                else:
                    # PRIMERO: Verificar si hay llamada a subrutina sin CALL en el lado derecho
                    # Ejemplo: pivote 🡨 particionar(A[], izq, der)
                    lado_derecho = linea_limpia.split('🡨', 1)[1].strip() if '🡨' in linea_limpia else ''
                    
                    if lado_derecho:
                        valido_llamada, mensaje_llamada = self.validar_llamada_subrutina(lado_derecho)
                        if not valido_llamada:
                            reportes.append((idx, linea, False, mensaje_llamada))
                            continue
                    
                    # SEGUNDO: Validar operadores matemáticos
                    valido_op, mensaje_op = self.validar_operadores_matematicos(linea)
                    if not valido_op:
                        reportes.append((idx, linea, False, mensaje_op))
                    elif re.match(self.patron_accion, linea_limpia):
                        reportes.append((idx, linea, True, 'Acción válida'))
                    else:
                        reportes.append((idx, linea, False, 'Acción inválida'))
                continue
            
            # ===== VALIDAR: Llamadas a subrutinas sin CALL =====
            valido_llamada, mensaje_llamada = self.validar_llamada_subrutina(linea_limpia)
            if not valido_llamada:
                en_seccion_declaraciones = False
                reportes.append((idx, linea, False, mensaje_llamada))
                continue
            
            # ===== AHORA SÍ: Validar declaraciones =====
            es_valida, mensaje, tipo = self.validar_declaracion_local(linea_limpia)
            
            if tipo == 'declaracion':
                if en_seccion_declaraciones:
                    reportes.append((idx, linea, True, mensaje))
                else:
                    reportes.append((idx, linea, False, 'Declaración fuera de lugar. Las declaraciones deben estar al inicio después del begin'))
            elif tipo == 'declaracion_invalida':
                reportes.append((idx, linea, False, mensaje))
            else:
                # No es declaración reconocida, validar como acción general
                en_seccion_declaraciones = False
                valido_op, mensaje_op = self.validar_operadores_matematicos(linea)
                if not valido_op:
                    reportes.append((idx, linea, False, mensaje_op))
                elif re.match(self.patron_accion, linea_limpia):
                    reportes.append((idx, linea, True, 'Acción válida'))
                else:
                    reportes.append((idx, linea, False, 'Acción inválida'))
        
        # END final
        if re.match(self.patron_end, lineas[-1].strip()):
            reportes.append((linea_inicio + len(lineas) - 1, lineas[-1], True, 'END válido'))
        else:
            reportes.append((linea_inicio + len(lineas) - 1, lineas[-1], False, 'Se esperaba END'))
        
        return reportes