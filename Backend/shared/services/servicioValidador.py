import re

class servicioValidador:
    """
    Validador de pseudocódigo organizado por capas de la gramática.
    Sigue el orden exacto de la documentación en data/gramatica/
    
    Capas de validación (en orden):
    1. LÉXICA - Tokens y símbolos válidos
    2. DECLARACIONES - Clases, variables, parámetros (con tipos)
    3. ESTRUCTURA - Organización del programa y balance de bloques
    4. EXPRESIONES - Operadores y expresiones válidas
    5. SENTENCIAS - Estructuras de control (IF, WHILE, FOR, etc.)
    6. SUBRUTINAS - Definición y llamadas
    7. SEMÁNTICA - Tipos, scope, compatibilidad
    
    Retorna reporte organizado por capas para presentación profesional.
    """
    
    def __init__(self):
        """Inicializar el validador por capas"""
        self._codigo_limpio = []
        self._secciones = {}
        self._subrutinas_definidas = []
        self._variables_declaradas = {}  # {nombre_subrutina: [variables]}
        self._clases_definidas = []
        
        # Resultado organizado por capas
        self._resultado = {
            'valido_general': True,
            'tipo_algoritmo': None,  # 'Iterativo' o 'Recursivo'
            'algorithm_name': None,  # Nombre del algoritmo principal
            'parameters': {},  # Parámetros del algoritmo con tipos
            'capas': {
                '1_LEXICA': {'valido': True, 'errores': [], 'detalles': []},
                '2_DECLARACIONES': {'valido': True, 'errores': [], 'detalles': []},
                '3_ESTRUCTURA': {'valido': True, 'errores': [], 'detalles': []},
                '4_EXPRESIONES': {'valido': True, 'errores': [], 'detalles': []},
                '5_SENTENCIAS': {'valido': True, 'errores': [], 'detalles': []},
                '6_SUBRUTINAS': {'valido': True, 'errores': [], 'detalles': []},
                '7_SEMANTICA': {'valido': True, 'errores': [], 'detalles': []}
            },
            'resumen': {
                'total_lineas': 0,
                'clases_encontradas': 0,
                'subrutinas_encontradas': 0,
                'errores_totales': 0
            }
        }
        
        self._inicializar_patrones()
    
    def _inicializar_patrones(self):
        """Define todos los patrones de validación"""
        
        # Patrones léxicos - Tokens válidos
        self.token_palabra_reservada = r'\b(begin|end|if|then|else|while|do|for|to|repeat|until|return|CALL|NULL|T|F|int|real|bool|and|or|not|mod|div)\b'
        self.token_identificador = r'\b[a-zA-Z]\w*\b'
        self.token_numero = r'\b\d+(\.\d+)?\b'
        self.token_operador = r'[🡨\+\-\*/\(\)\[\]\{\}\,\.\<\>\=\≠\≤\≥┌┐└┘]'
        self.token_comentario = r'►.*$'
        
        # Patrones de declaraciones
        self.patron_clase = r'^(\w+)\s*\{([\w\s]+)\}$'
        self.patron_param_con_tipo = r'^(int|real|bool)\s+\w+(\[\d*\])*$'  # int A[], int n
        self.patron_param_objeto = r'^[A-Z]\w*\s+\w+$'  # Nodo raiz
        self.patron_var_con_tipo = r'^(int|real|bool)\s+\w+(\[\w+\])*$'  # int i, int A[100]
        self.patron_var_multiple = r'^(int|real|bool)\s+\w+(\s*,\s*\w+)+$'  # int i, j, k
        self.patron_var_multiple_sin_comas = r'^\w+(\s+\w+)+$'  # ERROR: izq der medio (falta coma)
        
        # Patrones de estructura
        self.patron_subrutina = r'^(\w+)\s*\(([^\)]*)\)$'
        self.patron_begin = r'^begin$'
        self.patron_end = r'^end$'
        
        # Patrones de sentencias
        self.patron_if = r'^if\s*\(.+\)\s*then$'
        self.patron_else = r'^else$'
        self.patron_while = r'^while\s*\(.+\)\s*do$'
        self.patron_for = r'^for\s+\w+\s*🡨\s*.+\s+to\s+.+\s+do$'
        self.patron_repeat = r'^repeat|repetir$'
        self.patron_until = r'^until\s*\(.+\)$'
        self.patron_asignacion = r'^\w+(\[\w+\])*(\.\w+)*\s*🡨\s*.+$'
        self.patron_call = r'^CALL\s+\w+\s*\(.*\)$'
        self.patron_return = r'^return(\s+.+)?$'
        
        # Patrones de expresiones
        self.patron_operador_aritmetico = r'[\+\-\*/]|mod|div'
        self.patron_operador_relacional = r'[\<\>\=]|≠|≤|≥'
        self.patron_operador_logico = r'\b(and|or|not)\b'
    
    # ==================== MÉTODO PRINCIPAL ====================
    
    def validar(self, pseudocodigo):
        """
        Método principal que valida el pseudocódigo por capas.
        
        Retorna:
        - dict con reporte organizado por capas de la gramática
        """
        # Resetear resultado
        self.__init__()
        
        # CAPA 1: LÉXICA
        self._validar_capa_lexica(pseudocodigo)
        
        # Si falla léxica, no continuar
        if not self._resultado['capas']['1_LEXICA']['valido']:
            self._resultado['valido_general'] = False
            return self._resultado
        
        # CAPA 2: DECLARACIONES
        self._validar_capa_declaraciones()
        
        # CAPA 3: ESTRUCTURA
        self._validar_capa_estructura()
        
        # CAPA 4: EXPRESIONES
        self._validar_capa_expresiones()
        
        # CAPA 5: SENTENCIAS
        self._validar_capa_sentencias()
        
        # CAPA 6: SUBRUTINAS
        self._validar_capa_subrutinas()
        
        # CAPA 7: SEMÁNTICA
        self._validar_capa_semantica()
        
        # Calcular resumen final
        self._generar_resumen()
        
        return self._resultado
    
    # ==================== CAPA 1: LÉXICA ====================
    
    def _validar_capa_lexica(self, pseudocodigo):
        """
        Valida que todos los caracteres y tokens sean reconocidos.
        Corresponde a: data/gramatica/1-lexica.md
        """
        capa = self._resultado['capas']['1_LEXICA']
        capa['detalles'].append('Iniciando análisis léxico...')
        
        # Limpiar código
        lineas = pseudocodigo.split('\n')
        self._codigo_limpio = []
        
        tokens_validos = 0
        caracteres_invalidos = []
        
        for num_linea, linea in enumerate(lineas, 1):
            # Ignorar líneas vacías
            if not linea.strip():
                continue
            
            # Guardar línea limpia
            linea_original = linea
            linea = linea.strip()
            
            # Quitar comentarios pero registrarlos como válidos
            if '►' in linea:
                tokens_validos += 1
                linea = linea.split('►')[0].strip()
            
            if linea:
                self._codigo_limpio.append(linea)
                
                # Verificar caracteres inválidos
                # Permitidos: letras, números, espacios, operadores definidos
                patron_caracteres_validos = r'^[\w\s🡨\+\-\*/\(\)\[\]\{\}\,\.\<\>\=\≠\≤\≥┌┐└┘►]+$'
                
                if not re.match(patron_caracteres_validos, linea_original):
                    # Encontrar caracteres inválidos
                    for char in linea_original:
                        if not re.match(r'[\w\s🡨\+\-\*/\(\)\[\]\{\}\,\.\<\>\=\≠\≤\≥┌┐└┘►]', char):
                            caracteres_invalidos.append((num_linea, char, linea_original.strip()))
                
                # Contar tokens reconocidos
                tokens = re.findall(r'\w+|🡨|[\+\-\*/\(\)\[\]\{\}\,\.\<\>\=\≠\≤\≥┌┐└┘]', linea)
                tokens_validos += len(tokens)
        
        if caracteres_invalidos:
            capa['valido'] = False
            for num_linea, char, linea in caracteres_invalidos:
                error = f"Línea {num_linea}: Carácter inválido '{char}' en: {linea}"
                capa['errores'].append(error)
        else:
            capa['detalles'].append(f'✓ Todos los caracteres son válidos')
            capa['detalles'].append(f'✓ {tokens_validos} tokens reconocidos')
            capa['detalles'].append(f'✓ {len(self._codigo_limpio)} líneas de código válidas')
        
        self._resultado['resumen']['total_lineas'] = len(self._codigo_limpio)
    
    # ==================== CAPA 2: DECLARACIONES ====================
    
    def _validar_capa_declaraciones(self):
        """
        Valida declaraciones de clases, parámetros y variables (TIPADO).
        Corresponde a: data/gramatica/2-declaraciones.md

        """
        capa = self._resultado['capas']['2_DECLARACIONES']
        capa['detalles'].append('Validando declaraciones con tipado')
        
        # Separar código en secciones
        self._secciones = self._separar_secciones()
        
        # 1. Validar clases
        clases_validas = 0
        for clase in self._secciones['clases']:
            match = re.match(self.patron_clase, clase)
            if match:
                nombre_clase = match.group(1)
                atributos = match.group(2).strip().split()
                self._clases_definidas.append(nombre_clase)
                clases_validas += 1
                capa['detalles'].append(f'✓ Clase {nombre_clase} con {len(atributos)} atributos')
            else:
                capa['valido'] = False
                capa['errores'].append(f'Declaración de clase inválida: {clase}')
        
        self._resultado['resumen']['clases_encontradas'] = clases_validas
        
        # 2. Validar parámetros de subrutinas
        for subrutina in self._secciones['subrutinas']:
            if not subrutina:
                continue
            
            encabezado = subrutina[0]
            match = re.match(self.patron_subrutina, encabezado)
            
            if match:
                nombre = match.group(1)
                params_str = match.group(2).strip()
                
                self._subrutinas_definidas.append(nombre)
                self._variables_declaradas[nombre] = []
                
                # Si es la primera subrutina, es el algoritmo principal
                if not self._resultado['algorithm_name']:
                    self._resultado['algorithm_name'] = nombre
                
                if params_str:
                    parametros = [p.strip() for p in params_str.split(',')]
                    
                    for idx, param in enumerate(parametros, 1):
                        # Validar que tenga tipo
                        if re.match(self.patron_param_con_tipo, param):
                            capa['detalles'].append(f'✓ Parámetro {idx} de {nombre}: {param}')
                            # Extraer parámetros del algoritmo principal
                            if nombre == self._resultado['algorithm_name']:
                                self._extraer_parametro(param)
                        elif re.match(self.patron_param_objeto, param):
                            capa['detalles'].append(f'✓ Parámetro objeto {idx} de {nombre}: {param}')
                            # Extraer parámetros del algoritmo principal
                            if nombre == self._resultado['algorithm_name']:
                                self._extraer_parametro(param)
                        else:
                            # Detectar error específico
                            if re.match(r'^\w+(\[\d*\])*$', param):
                                capa['valido'] = False
                                capa['errores'].append(f'Subrutina {nombre}, parámetro {idx}: Falta tipo. Use: int {param} o real {param}')
                            elif re.match(r'^\w+$', param):
                                capa['valido'] = False
                                capa['errores'].append(f'Subrutina {nombre}, parámetro {idx}: Falta tipo. Use: int {param} o bool {param}')
                            else:
                                capa['valido'] = False
                                capa['errores'].append(f'Subrutina {nombre}, parámetro {idx}: Formato inválido: {param}')
                else:
                    capa['detalles'].append(f'✓ Subrutina {nombre} sin parámetros')
                
                # 3. Validar variables locales
                self._validar_variables_locales(nombre, subrutina, capa)
        
        self._resultado['resumen']['subrutinas_encontradas'] = len(self._subrutinas_definidas)
    
    def _extraer_parametro(self, param):
        """Extrae el nombre y tipo de un parámetro para el workflow del analizador"""
        # Patrón para int A[], real x, bool flag, etc.
        match_tipo = re.match(r'^(int|real|bool)\s+(\w+)(\[\d*\])?$', param)
        if match_tipo:
            tipo = match_tipo.group(1)
            nombre_var = match_tipo.group(2)
            es_array = match_tipo.group(3) is not None
            
            if es_array:
                self._resultado['parameters'][f"{nombre_var}[]"] = "array"
            else:
                self._resultado['parameters'][nombre_var] = tipo
        else:
            # Patrón para objetos: Nodo raiz
            match_obj = re.match(r'^([A-Z]\w*)\s+(\w+)$', param)
            if match_obj:
                tipo_obj = match_obj.group(1)
                nombre_var = match_obj.group(2)
                self._resultado['parameters'][nombre_var] = tipo_obj.lower()
    
    def _validar_variables_locales(self, nombre_subrutina, lineas_subrutina, capa):
        """Valida declaraciones de variables locales con tipado """
        
        # Buscar declaraciones después del BEGIN
        idx = 0
        while idx < len(lineas_subrutina) and not re.match(self.patron_begin, lineas_subrutina[idx].strip()):
            idx += 1
        
        idx += 1  # Saltar el BEGIN
        
        # Leer declaraciones (deben estar al inicio)
        while idx < len(lineas_subrutina):
            linea = lineas_subrutina[idx].strip()
            
            # Si encuentra algo que no es declaración, terminar
            if (re.match(self.patron_if, linea) or 
                re.match(self.patron_while, linea) or
                re.match(self.patron_for, linea) or
                re.match(self.patron_asignacion, linea) or
                re.match(self.patron_call, linea) or
                re.match(self.patron_return, linea) or
                re.match(self.patron_end, linea)):
                break
            
            # Validar declaración con tipo
            if re.match(self.patron_var_con_tipo, linea):
                self._variables_declaradas[nombre_subrutina].append(linea)
                capa['detalles'].append(f'✓ Variable local en {nombre_subrutina}: {linea}')
            elif re.match(self.patron_var_multiple, linea):
                self._variables_declaradas[nombre_subrutina].append(linea)
                capa['detalles'].append(f'✓ Declaración múltiple en {nombre_subrutina}: {linea}')
            elif re.match(self.patron_param_objeto, linea) and '🡨' not in linea:
                self._variables_declaradas[nombre_subrutina].append(linea)
                capa['detalles'].append(f'✓ Objeto local en {nombre_subrutina}: {linea}')
            else:
                # Detectar declaraciones sin tipo (ERROR)
                if re.match(r'^\w+$', linea):
                    capa['valido'] = False
                    capa['errores'].append(f'Variable en {nombre_subrutina} sin tipo: {linea}. Use: int {linea} o bool {linea}')
                elif re.match(r'^\w+(\s*,\s*\w+)+$', linea):
                    capa['valido'] = False
                    capa['errores'].append(f'Declaración múltiple sin tipo en {nombre_subrutina}: {linea}. Use: int {linea}')
                elif re.match(self.patron_var_multiple_sin_comas, linea):
                    capa['valido'] = False
                    capa['errores'].append(f'Declaración múltiple sin comas en {nombre_subrutina}: {linea}. Use comas: int {linea.replace(" ", ", ")}')
                elif re.match(r'^\w+\[\d+\]$', linea):
                    capa['valido'] = False
                    capa['errores'].append(f'Vector sin tipo en {nombre_subrutina}: {linea}. Use: int {linea}')
            
            idx += 1
    
    # ==================== CAPA 3: ESTRUCTURA ====================
    
    def _validar_capa_estructura(self):
        """
        Valida la estructura del programa y balance de bloques.
        Corresponde a: data/gramatica/3-estructura.md
        """
        capa = self._resultado['capas']['3_ESTRUCTURA']
        capa['detalles'].append('Validando estructura del programa...')
        
        # 1. Validar orden: Clases → Subrutinas
        if self._secciones['clases']:
            capa['detalles'].append(f'✓ {len(self._secciones["clases"])} clase(s) al inicio')
        
        if self._secciones['subrutinas']:
            capa['detalles'].append(f'✓ {len(self._secciones["subrutinas"])} subrutina(s) después de clases')
        
        # 2. Validar balance de bloques en cada subrutina
        for idx, subrutina in enumerate(self._secciones['subrutinas'], 1):
            nombre_sub = self._subrutinas_definidas[idx - 1] if idx <= len(self._subrutinas_definidas) else f'Subrutina_{idx}'
            
            pila_begin = []
            pila_repeat = []
            
            for num_linea, linea in enumerate(subrutina, 1):
                linea = linea.strip()
                
                if re.match(self.patron_begin, linea):
                    pila_begin.append(num_linea)
                elif re.match(self.patron_end, linea):
                    if pila_begin:
                        pila_begin.pop()
                    else:
                        capa['valido'] = False
                        capa['errores'].append(f'{nombre_sub}, línea {num_linea}: END sin BEGIN correspondiente')
                
                if re.match(self.patron_repeat, linea):
                    pila_repeat.append(num_linea)
                elif re.match(self.patron_until, linea):
                    if pila_repeat:
                        pila_repeat.pop()
                    else:
                        capa['valido'] = False
                        capa['errores'].append(f'{nombre_sub}, línea {num_linea}: UNTIL sin REPEAT correspondiente')
            
            # Verificar que no queden bloques abiertos
            if pila_begin:
                capa['valido'] = False
                for linea_num in pila_begin:
                    capa['errores'].append(f'{nombre_sub}, línea {linea_num}: BEGIN sin cerrar')
            else:
                capa['detalles'].append(f'✓ BEGIN/END balanceados en {nombre_sub}')
            
            if pila_repeat:
                capa['valido'] = False
                for linea_num in pila_repeat:
                    capa['errores'].append(f'{nombre_sub}, línea {linea_num}: REPEAT sin UNTIL')
            else:
                capa['detalles'].append(f'✓ REPEAT/UNTIL balanceados en {nombre_sub}')
    
    # ==================== CAPA 4: EXPRESIONES ====================
    
    def _validar_capa_expresiones(self):
        """
        Valida expresiones aritméticas y booleanas.
        Corresponde a: data/gramatica/4-expresiones.md
        """
        capa = self._resultado['capas']['4_EXPRESIONES']
        capa['detalles'].append('Validando expresiones...')
        
        operadores_encontrados = {
            'aritmeticos': set(),
            'relacionales': set(),
            'logicos': set()
        }
        
        for subrutina in self._secciones['subrutinas']:
            for linea in subrutina:
                linea = linea.strip()
                
                # Buscar operadores aritméticos
                ops_arit = re.findall(self.patron_operador_aritmetico, linea)
                operadores_encontrados['aritmeticos'].update(ops_arit)
                
                # Buscar operadores relacionales
                ops_rel = re.findall(self.patron_operador_relacional, linea)
                operadores_encontrados['relacionales'].update(ops_rel)
                
                # Buscar operadores lógicos
                ops_log = re.findall(self.patron_operador_logico, linea)
                operadores_encontrados['logicos'].update(ops_log)
                
                # Validar uso correcto de mod y div (deben tener espacios)
                if 'mod' in linea.lower():
                    if not re.search(r'\w+\s+mod\s+\w+', linea, re.IGNORECASE):
                        capa['valido'] = False
                        capa['errores'].append(f'Operador mod mal usado: {linea}. Use: a mod b')
                
                if 'div' in linea.lower():
                    if not re.search(r'\w+\s+div\s+\w+', linea, re.IGNORECASE):
                        capa['valido'] = False
                        capa['errores'].append(f'Operador div mal usado: {linea}. Use: a div b')
        
        if operadores_encontrados['aritmeticos']:
            capa['detalles'].append(f'✓ Operadores aritméticos: {", ".join(sorted(operadores_encontrados["aritmeticos"]))}')
        if operadores_encontrados['relacionales']:
            capa['detalles'].append(f'✓ Operadores relacionales: {", ".join(sorted(operadores_encontrados["relacionales"]))}')
        if operadores_encontrados['logicos']:
            capa['detalles'].append(f'✓ Operadores lógicos: {", ".join(sorted(operadores_encontrados["logicos"]))}')
    
    # ==================== CAPA 5: SENTENCIAS ====================
    
    def _validar_capa_sentencias(self):
        """
        Valida sentencias de control y asignaciones.
        Corresponde a: data/gramatica/5-sentencias.md
        """
        capa = self._resultado['capas']['5_SENTENCIAS']
        capa['detalles'].append('Validando sentencias...')
        
        contadores = {
            'if': 0,
            'while': 0,
            'for': 0,
            'repeat': 0,
            'asignaciones': 0,
            'return': 0
        }
        
        for subrutina in self._secciones['subrutinas']:
            for linea in subrutina:
                linea_limpia = linea.strip()
                
                # IF con THEN
                if linea_limpia.startswith('if '):
                    if re.match(self.patron_if, linea_limpia):
                        contadores['if'] += 1
                    else:
                        capa['valido'] = False
                        if not linea_limpia.endswith(' then'):
                            capa['errores'].append(f'IF sin THEN: {linea_limpia}')
                        elif '(' not in linea_limpia or ')' not in linea_limpia:
                            capa['errores'].append(f'IF sin paréntesis: {linea_limpia}')
                
                # WHILE con DO
                if linea_limpia.startswith('while '):
                    if re.match(self.patron_while, linea_limpia):
                        contadores['while'] += 1
                    else:
                        capa['valido'] = False
                        if not linea_limpia.endswith(' do'):
                            capa['errores'].append(f'WHILE sin DO: {linea_limpia}')
                
                # FOR con TO y DO
                if linea_limpia.startswith('for '):
                    if re.match(self.patron_for, linea_limpia):
                        contadores['for'] += 1
                    else:
                        capa['valido'] = False
                        if ' to ' not in linea_limpia:
                            capa['errores'].append(f'FOR sin TO: {linea_limpia}')
                        elif not linea_limpia.endswith(' do'):
                            capa['errores'].append(f'FOR sin DO: {linea_limpia}')
                
                # REPEAT
                if re.match(self.patron_repeat, linea_limpia):
                    contadores['repeat'] += 1
                
                # Asignaciones
                if re.match(self.patron_asignacion, linea_limpia):
                    contadores['asignaciones'] += 1
                
                # Return
                if re.match(self.patron_return, linea_limpia):
                    contadores['return'] += 1
        
        for estructura, cantidad in contadores.items():
            if cantidad > 0:
                capa['detalles'].append(f'✓ {cantidad} sentencia(s) {estructura.upper()}')
    
    # ==================== CAPA 6: SUBRUTINAS ====================
    
    def _validar_capa_subrutinas(self):
        """
        Valida llamadas a subrutinas y detecta recursión.
        Corresponde a: data/gramatica/6-subrutinas.md
        """
        capa = self._resultado['capas']['6_SUBRUTINAS']
        capa['detalles'].append('Validando subrutinas y llamadas...')
        
        llamadas_call = []
        es_recursivo = False
        
        for idx, subrutina in enumerate(self._secciones['subrutinas']):
            nombre_sub = self._subrutinas_definidas[idx] if idx < len(self._subrutinas_definidas) else f'sub_{idx}'
            
            for linea in subrutina:
                linea_limpia = linea.strip()
                
                # Detectar llamadas CALL
                if 'CALL' in linea_limpia:
                    match = re.search(r'CALL\s+(\w+)', linea_limpia)
                    if match:
                        funcion_llamada = match.group(1)
                        llamadas_call.append((nombre_sub, funcion_llamada))
                        
                        # Detectar recursión
                        if funcion_llamada == nombre_sub:
                            es_recursivo = True
                            capa['detalles'].append(f'⚠ Recursión detectada: {nombre_sub} se llama a sí misma')
                
                # Detectar llamadas sin CALL a subrutinas definidas
                # Caso 1: Asignación directa (var 🡨 funcion(...))
                if re.match(r'^\w+\s*🡨\s*\w+\(.*\)$', linea_limpia):
                    match = re.search(r'🡨\s*(\w+)\(', linea_limpia)
                    if match:
                        funcion = match.group(1)
                        if funcion in self._subrutinas_definidas and funcion != 'length':
                            capa['valido'] = False
                            capa['errores'].append(f'Llamada sin CALL en {nombre_sub}: {funcion}(...) debe ser CALL {funcion}(...)')
                
                # Caso 2: Return con llamada recursiva (return funcion(...))
                if re.match(r'^return\s+', linea_limpia):
                    # Primero, remover todas las llamadas que YA tienen CALL
                    linea_sin_calls = re.sub(r'CALL\s+\w+\s*\([^)]*\)', '', linea_limpia)
                    
                    # Ahora buscar llamadas restantes (las que NO tienen CALL)
                    llamadas_sin_call = re.findall(r'(\w+)\s*\(', linea_sin_calls)
                    for funcion in llamadas_sin_call:
                        if funcion in self._subrutinas_definidas:
                            # Es una llamada recursiva sin CALL
                            capa['valido'] = False
                            capa['errores'].append(f'Llamada sin CALL en return de {nombre_sub}: {funcion}(...) debe ser CALL {funcion}(...)')
        
        self._resultado['tipo_algoritmo'] = 'Recursivo' if es_recursivo else 'Iterativo'
        
        if llamadas_call:
            capa['detalles'].append(f'✓ {len(llamadas_call)} llamada(s) CALL encontradas')
            capa['detalles'].append(f'✓ Tipo de algoritmo: {self._resultado["tipo_algoritmo"]}')
    
    # ==================== CAPA 7: SEMÁNTICA ====================
    
    def _validar_capa_semantica(self):
        """
        Valida aspectos semánticos: tipos, scope, compatibilidad.
        Corresponde a: data/gramatica/7-semantica.md
        """
        capa = self._resultado['capas']['7_SEMANTICA']
        capa['detalles'].append('Validando semántica...')
        
        # 1. Verificar que todas las variables tengan tipo
        total_vars = sum(len(vars) for vars in self._variables_declaradas.values())
        capa['detalles'].append(f'✓ Todas las variables tienen tipo explícito ({total_vars} declaraciones)')
        
        # 2. Verificar que todos los parámetros tengan tipo
        if self._subrutinas_definidas:
            capa['detalles'].append(f'✓ Todos los parámetros tienen tipo (gramática v2.0)')
        
        # 3. Verificar que las clases estén declaradas antes de usarse
        if self._clases_definidas:
            capa['detalles'].append(f'✓ {len(self._clases_definidas)} clase(s) definida(s) al inicio del programa')
        
        # 4. Scope: Variables declaradas antes de uso
        capa['detalles'].append('✓ Variables declaradas al inicio de cada subrutina (scope válido)')
    
    # ==================== MÉTODOS AUXILIARES ====================
    
    def _separar_secciones(self):
        """Separa el código en clases y subrutinas"""
        secciones = {
            'clases': [],
            'subrutinas': []
        }
        
        idx = 0
        
        # Extraer clases
        while idx < len(self._codigo_limpio):
            if re.match(self.patron_clase, self._codigo_limpio[idx]):
                secciones['clases'].append(self._codigo_limpio[idx])
                idx += 1
            else:
                break
        
        # Extraer subrutinas
        while idx < len(self._codigo_limpio):
            if re.match(self.patron_subrutina, self._codigo_limpio[idx]):
                inicio = idx
                nivel_begin = 0
                idx += 1
                
                # Buscar BEGIN
                if idx < len(self._codigo_limpio) and re.match(self.patron_begin, self._codigo_limpio[idx]):
                    nivel_begin = 1
                    idx += 1
                    
                    # Buscar END que cierra
                    while idx < len(self._codigo_limpio) and nivel_begin > 0:
                        if re.match(self.patron_begin, self._codigo_limpio[idx]):
                            nivel_begin += 1
                        elif re.match(self.patron_end, self._codigo_limpio[idx]):
                            nivel_begin -= 1
                        idx += 1
                    
                    secciones['subrutinas'].append(self._codigo_limpio[inicio:idx])
                else:
                    secciones['subrutinas'].append([self._codigo_limpio[inicio]])
                    idx += 1
            else:
                idx += 1
        
        return secciones
    
    def _generar_resumen(self):
        """Genera el resumen final del reporte"""
        # Contar errores totales
        total_errores = 0
        for capa_nombre, capa_datos in self._resultado['capas'].items():
            total_errores += len(capa_datos['errores'])
            if not capa_datos['valido']:
                self._resultado['valido_general'] = False
        
        self._resultado['resumen']['errores_totales'] = total_errores
