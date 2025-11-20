# validadorSintaxis.py
import re

class ValidadorSintaxis:
    # Patrón para sintaxis FOR (incluye 🡨 y <-)
    patron_for = r'^for\s+\w+\s*(<-|🡨)\s*\w+\s+to\s+\w+\s+do$'
    patron_while = r'^while\s*\(.+\)\s*do$'
    patron_repeat = r'^repetir$'
    patron_if = r'^if\s*\(.+\)\s*then$'
    patron_else = r'^else$'
    patron_begin = r'^begin$'
    patron_end = r'^end$'
    patron_accion = r'^[\w\s\<\-\+\*/\(\)\[\]]+$'
    patron_until = r'^until\s*\(.+\)$'
    patron_comentario = r'^►.*$'
    patron_asignacion = r'^\w+\s*🡨\s*.+$'

    # validar_for: Valida la sintaxis de un bloque FOR
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
            if re.match(self.patron_accion, linea.strip()):
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
            if re.match(self.patron_accion, linea.strip()):
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
        idx = 3
        while idx < len(lineas) and not re.match(self.patron_end, lineas[idx].strip()):
            if re.match(self.patron_accion, lineas[idx].strip()):
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
                if re.match(self.patron_accion, lineas[idx].strip()):
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




# Ejemplo simple
if __name__ == "__main__":
    #? Ejemplo con el for
    # pseudocodigo = [
    #     "for i 🡨 1 to x do",
    #     "begin",
    #     "x <- x + i",
    #     "a <- 5",
    #     "end"
    # ]
    # validador = ValidadorSintaxis()
    # resultado = validador.validar_while(pseudocodigo)
    # for idx, linea, valido, mensaje in resultado:
    #     print(f"{'✔' if valido else '✘'} Línea {idx}: {mensaje} - '{linea}'")

    #? Ejemplo con el while
    # pseudocodigo_while = [
    #     "while (x < 10)",
    #     "begin",
    #     "x <- x + 1",
    #     "end"
    # ]
    # validador = ValidadorSintaxis()
    # resultado = validador.validar_while(pseudocodigo_while)
    # for idx, linea, valido, mensaje in resultado:
    #     print(f"{'✔' if valido else '✘'} Línea {idx}: {mensaje} - '{linea}'")

    #? Ejemplo con el repeat
    # pseudocodigo_repeat = [
    #     "repetir",
    #     "x <- x - 1",
    #     "y <- y + x",
    #     "until (x == 0)"
    # ]
    # validador = ValidadorSintaxis()
    # resultado = validador.validar_repeat(pseudocodigo_repeat)
    # for idx, linea, valido, mensaje in resultado:
    #     print(f"{'✔' if valido else '✘'} Línea {idx}: {mensaje} - '{linea}'")

    #? Ejemplo con el if-else 
    pseudocodigo_if = [
    "if (x > 0) then",
    "begin",
    "y <- x",
    "end",
    "else",
    "begin",
    "y <- 0",
    "end"
    ]
    validador = ValidadorSintaxis()
    resultado = validador.validar_if(pseudocodigo_if)
    for idx, linea, valido, mensaje in resultado:
        print(f"{'✔' if valido else '✘'} Línea {idx}: {mensaje} - '{linea}'")
