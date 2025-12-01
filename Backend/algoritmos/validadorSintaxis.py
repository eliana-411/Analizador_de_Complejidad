import re

class ValidadorSintaxis:
    patron_for = r'^for\s+\w+\s*(<-|🡨)\s*\w+\s+to\s+\w+\s+do$'
    patron_condicion = r'[\w\s\.\[\]\(\)\<\>\=\≠\≤\≥]+(and|or|not)?[\w\s\.\[\]\(\)\<\>\=\≠\≤\≥]*'
    patron_while = r'^while\s*\(.+\)\s*do$'
    patron_repeat = r'^repeat|repetir$'
    patron_if = r'^if\s*\(.+\)\s*then$'
    patron_else = r'^else$'
    patron_begin = r'^begin$'
    patron_end = r'^end$'
    patron_accion = r'^[\w\s\<\-🡨\+\*/\(\)\[\]\.\=\≠\≤\≥\<\>\{\}\,┌┐└┘]+$'
    patron_until = r'^until\s*\(.+\)$'
    patron_comentario = r'^►.*$'
    patron_asignacion = r'^\w+\s*🡨\s*.+$'
    patron_null = r'\bNULL\b'
    patron_boolean = r'\b(T|F)\b'  # T=true, F=false
    patron_length = r'length\s*\(\s*\w+\s*\)'
    patron_rango_arreglo = r'\w+\[\d+\.\.\w+\]'  # A[1..j]
    patron_acceso_arreglo = r'\w+\[\w+\]'  # A[i]
    patron_acceso_objeto = r'\w+\.\w+'  # objeto.campo
    patron_call = r'^CALL\s+\w+\s*\(.+\)$'
    patron_declaracion_vector = r'^\w+\[\d+\]$'  # nombreVector[tamaño]
    patron_subrutina = r'^\w+\s*\([^\)]*\)$'  # nombre_subrutina(params)
    patron_param_arreglo = r'\w+\[\d*\](\[\d*\])*'  # A[], A[n], A[5][10]
    patron_param_arreglo_rango = r'\w+\[\w*\]\.\.\[\w*\]|\w+\[\d*\.\.\w*\]'  # A[n]..[m] o A[1..n]
    patron_param_objeto = r'Clase\s+\w+'  # Clase nombre_objeto

    def validar_asignacion_unica(self, linea):
        """
        Valida que en una línea solo haya una asignación (un solo símbolo 🡨).
        Retorna True si es válida (0 o 1 asignaciones), False si hay múltiples.
        """
        # Contar cuántas veces aparece el símbolo de asignación
        count = linea.count('🡨')
        return count <= 1

    def validar_operadores_matematicos(self, linea):
        """
        Valida que 'mod' y 'div' estén usados como operadores (con espacios alrededor)
        y no como parte de nombres de variables.
        Retorna (True, mensaje) si es válido, (False, mensaje) si es inválido.
        """
        linea = linea.strip()
        
        # Buscar 'mod' y 'div' como palabras completas (con límites de palabra)
        # Ejemplos válidos: "a mod b", "x div y"
        # Ejemplos inválidos: "modulo", "dividir", "amod"
        
        patron_mod_valido = r'\b\w+\s+mod\s+\w+\b'
        patron_div_valido = r'\b\w+\s+div\s+\w+\b'
        
        # Buscar uso incorrecto (mod o div como parte de una palabra)
        patron_mod_invalido = r'\w*mod\w+|\w+mod\w*'
        patron_div_invalido = r'\w*div\w+|\w+div\w*'
        
        # Si contiene 'mod' o 'div', validar su uso
        if 'mod' in linea.lower():
            if re.search(patron_mod_invalido, linea, re.IGNORECASE) and not re.search(patron_mod_valido, linea, re.IGNORECASE):
                return (False, "'mod' debe usarse como operador: a mod b")
        
        if 'div' in linea.lower():
            if re.search(patron_div_invalido, linea, re.IGNORECASE) and not re.search(patron_div_valido, linea, re.IGNORECASE):
                return (False, "'div' debe usarse como operador: a div b")
        
        return (True, 'Operadores matemáticos válidos')

    def validar_declaracion_vector(self, linea):
        """
        Valida que una declaración de vector tenga el formato: nombreVector[tamaño]
        También acepta vectores multidimensionales: matriz[n][m]
        Retorna (True, mensaje) si es válida, (False, mensaje) si no lo es.
        """
        linea = linea.strip()
        # Patrón para vector de una dimensión: nombre[tamaño]
        patron_1d = r'^\w+\[\d+\]$'
        # Patrón para vector multidimensional: nombre[n][m]... o nombre[n]..[m]
        patron_multi = r'^\w+(\[\d+\])+$'
        
        if re.match(patron_1d, linea) or re.match(patron_multi, linea):
            return (True, 'Declaración de vector válida')
        return (False, 'Declaración de vector inválida')

   

    def validar_call(self, linea):
        """
        Valida que una llamada a subrutina tenga el formato: CALL nombre_subrutina(param1, param2, ...)
        Retorna (True, mensaje) si es válida, (False, mensaje) si no lo es.
        """
        linea = linea.strip()
        if re.match(self.patron_call, linea):
            return (True, 'Llamada CALL válida')
        return (False, 'Llamada CALL inválida')

    def validar_for(self, lineas): 
        """
        Recibe una lista de líneas y valida el ciclo FOR paso a paso.
        """
        reportes = []
        if len(lineas) < 3:
            reportes.append((1, '', False, 'El bloque es demasiado corto'))
            return reportes
        # 1 - Encabezado FOR
        if re.match(self.patron_for, lineas[0].strip()):
            reportes.append((1, lineas[0], True, 'Encabezado FOR válido'))
        else:
            reportes.append((1, lineas[0], False, 'Encabezado FOR inválido'))
        # 2 - BEGIN
        if re.match(self.patron_begin, lineas[1].strip()):
            reportes.append((2, lineas[1], True, 'BEGIN válido'))
        else:
            reportes.append((2, lineas[1], False, 'Se esperaba BEGIN'))
        # N - END
        if re.match(self.patron_end, lineas[-1].strip()):
            reportes.append((len(lineas), lineas[-1], True, 'END válido'))
        else:
            reportes.append((len(lineas), lineas[-1], False, 'Se esperaba END'))
        return reportes

    def validar_subrutina(self, lineas):
        """
        Valida una subrutina con el formato:
        nombre_subrutina(param1, param2, A[1..n], Clase objeto)
            begin
                ...
            end
        """
        reportes = []
        if len(lineas) < 3:
            reportes.append((1, '', False, 'El bloque de subrutina es demasiado corto'))
            return reportes
        
        # 1 - Encabezado de subrutina: nombre(parametros)
        # Acepta parámetros como: simples, arreglos A[], A[n], A[1..n], A[][], objetos: Clase nombre
        patron_encabezado = r'^\w+\s*\([^\)]*\)$'
        if re.match(patron_encabezado, lineas[0].strip()):
            reportes.append((1, lineas[0], True, 'Encabezado de subrutina válido'))
        else:
            reportes.append((1, lineas[0], False, 'Encabezado de subrutina inválido'))
        
        # 2 - BEGIN
        if re.match(self.patron_begin, lineas[1].strip()):
            reportes.append((2, lineas[1], True, 'BEGIN válido'))
        else:
            reportes.append((2, lineas[1], False, 'Se esperaba BEGIN'))
        
        # Validación de acciones internas (similar a otros bloques)
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
        
        # N - END
        if re.match(self.patron_end, lineas[-1].strip()):
            reportes.append((len(lineas), lineas[-1], True, 'END válido'))
        else:
            reportes.append((len(lineas), lineas[-1], False, 'Se esperaba END'))
        
        return reportes

    # validar_while: Valida la sintaxis de un bloque WHILE
    def validar_while(self, lineas):
        reportes = []
        if len(lineas) < 3:
            reportes.append((1, '', False, 'El bloque es demasiado corto'))
            return reportes
        # 1 - Encabezado WHILE
        if re.match(self.patron_while, lineas[0].strip()):
            reportes.append((1, lineas[0], True, 'Encabezado WHILE válido'))
        else:
            reportes.append((1, lineas[0], False, 'Encabezado WHILE inválido'))
        # 2 - BEGIN
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
        # N - END
        if re.match(self.patron_end, lineas[-1].strip()):
            reportes.append((len(lineas), lineas[-1], True, 'END válido'))
        else:
            reportes.append((len(lineas), lineas[-1], False, 'Se esperaba END'))
        return reportes

    # validar_repeat: Valida la sintaxis de un bloque REPEAT
    def validar_repeat(self, lineas):
        reportes = []
        if len(lineas) < 3:
            reportes.append((1, '', False, 'El bloque es demasiado corto'))
            return reportes
        # repeat
        if re.match(self.patron_repeat, lineas[0].strip()):
            reportes.append((1, lineas[0], True, 'REPEAT válido'))
        else:
            reportes.append((1, lineas[0], False, 'Falta o sintaxis incorrecta en REPEAT'))
        # acciones
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
        # until (...)
        if re.match(self.patron_until, lineas[-1].strip()):
            reportes.append((len(lineas), lineas[-1], True, 'UNTIL válido'))
        else:
            reportes.append((len(lineas), lineas[-1], False, 'Falta o sintaxis incorrecta en UNTIL'))
        return reportes
    

    # Valdar_if: Valida la sintaxis de un bloque IF-ELSE
    def validar_if(self, lineas):
        reportes = []
        if len(lineas) < 4:
            reportes.append((1, '', False, 'El bloque es demasiado corto'))
            return reportes
        # Encabezado IF
        if re.match(self.patron_if, lineas[0].strip()):
            reportes.append((1, lineas[0], True, 'IF válido'))
        else:
            reportes.append((1, lineas[0], False, 'Encabezado IF inválido'))

        # BEGIN/END del bloque IF
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
        # END
        if idx < len(lineas) and re.match(self.patron_end, lineas[idx].strip()):
            reportes.append((idx+1, lineas[idx], True, 'END válido'))
            idx += 1
        else:
            reportes.append((idx+1, '', False, 'Se esperaba END'))

        # Verificar si hay ELSE
        if idx < len(lineas) and re.match(self.patron_else, lineas[idx].strip()):
            reportes.append((idx+1, lineas[idx], True, 'ELSE válido'))
            idx += 1
            # BEGIN/END del bloque ELSE
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
            # END (ELSE)
            if idx < len(lineas) and re.match(self.patron_end, lineas[idx].strip()):
                reportes.append((idx+1, lineas[idx], True, 'END válido'))
            else:
                reportes.append((idx+1, '', False, 'Se esperaba END'))

        return reportes


#! Falta definir:
#! Estructura para cadenas
#! Estructura para grafos
