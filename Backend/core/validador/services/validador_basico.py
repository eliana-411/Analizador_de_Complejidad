import re
from core.validador.models.patterns import GrammarPatterns


class ValidadorBasico:
    """
    Validador de capas fundamentales (1-3):
    - Capa 1: Léxica (tokens y caracteres válidos)
    - Capa 2: Declaraciones (clases, parámetros, variables con tipos)
    - Capa 3: Estructura (balance de bloques y organización)

    Procesa pseudocódigo y retorna estado compartido para ValidadorSemantico.
    """

    def __init__(self):
        self.patterns = GrammarPatterns()
        self.codigo_limpio = []
        self.secciones = {}
        self.clases_definidas = []
        self.subrutinas_definidas = []
        self.variables_declaradas = {}

    def validar(self, pseudocodigo: str) -> tuple[dict, dict]:
        """
        Ejecuta validación de capas 1-3.

        Returns:
            tuple: (resultado_validacion, state_compartido)
        """
        resultado = {
            "1_LEXICA": self._validar_capa_lexica(pseudocodigo),
            "2_DECLARACIONES": self._validar_capa_declaraciones(),
            "3_ESTRUCTURA": self._validar_capa_estructura(),
        }

        state = self.get_state()
        return resultado, state

    def get_state(self) -> dict:
        """Estado compartido para ValidadorSemantico"""
        return {
            "codigo_limpio": self.codigo_limpio,
            "secciones": self.secciones,
            "clases_definidas": self.clases_definidas,
            "subrutinas_definidas": self.subrutinas_definidas,
            "variables_declaradas": self.variables_declaradas,
        }

    def _validar_capa_lexica(self, pseudocodigo: str) -> dict:
        """Valida que todos los caracteres y tokens sean reconocidos"""
        capa = {"valido": True, "errores": [], "detalles": []}
        capa["detalles"].append("Iniciando análisis léxico...")

        lineas = pseudocodigo.split("\n")
        self.codigo_limpio = []

        tokens_validos = 0
        caracteres_invalidos = []

        for num_linea, linea in enumerate(lineas, 1):
            if not linea.strip():
                continue

            linea_original = linea
            linea = linea.strip()

            # Quitar comentarios
            if "►" in linea:
                tokens_validos += 1
                linea = linea.split("►")[0].strip()

            if linea:
                self.codigo_limpio.append(linea)

                # Verificar caracteres inválidos
                patron_caracteres_validos = (
                    r"^[\w\s🡨\+\-\*/\(\)\[\]\{\}\,\.\<\>\=\≠\≤\≥┌┐└┘►]+$"
                )

                if not re.match(patron_caracteres_validos, linea_original):
                    for char in linea_original:
                        if not re.match(
                            r"[\w\s🡨\+\-\*/\(\)\[\]\{\}\,\.\<\>\=\≠\≤\≥┌┐└┘►]", char
                        ):
                            caracteres_invalidos.append(
                                (num_linea, char, linea_original.strip())
                            )

                # Contar tokens reconocidos
                tokens = re.findall(
                    r"\w+|🡨|[\+\-\*/\(\)\[\]\{\}\,\.\<\>\=\≠\≤\≥┌┐└┘]", linea
                )
                tokens_validos += len(tokens)

        if caracteres_invalidos:
            capa["valido"] = False
            for num_linea, char, linea in caracteres_invalidos:
                error = f"Línea {num_linea}: Carácter inválido '{char}' en: {linea}"
                capa["errores"].append(error)
        else:
            capa["detalles"].append("✓ Todos los caracteres son válidos")
            capa["detalles"].append(f"✓ {tokens_validos} tokens reconocidos")
            capa["detalles"].append(
                f"✓ {len(self.codigo_limpio)} líneas de código válidas"
            )

        return capa

    def _validar_capa_declaraciones(self) -> dict:
        """Valida declaraciones de clases, parámetros y variables (TIPADO)"""
        capa = {"valido": True, "errores": [], "detalles": []}
        capa["detalles"].append("Validando declaraciones con tipado")

        # Separar código en secciones
        self.secciones = self._separar_secciones()

        # 1. Validar clases
        clases_validas = 0
        for clase in self.secciones["clases"]:
            match = re.match(self.patterns.patron_clase, clase)
            if match:
                nombre_clase = match.group(1)
                atributos = match.group(2).strip().split()
                self.clases_definidas.append(nombre_clase)
                clases_validas += 1
                capa["detalles"].append(
                    f"✓ Clase {nombre_clase} con {len(atributos)} atributos"
                )
            else:
                capa["valido"] = False
                capa["errores"].append(f"Declaración de clase inválida: {clase}")

        # 2. Validar parámetros de subrutinas
        for subrutina in self.secciones["subrutinas"]:
            if not subrutina:
                continue

            encabezado = subrutina[0]
            match = re.match(self.patterns.patron_subrutina, encabezado)

            if match:
                nombre = match.group(1)
                params_str = match.group(2).strip()

                self.subrutinas_definidas.append(nombre)
                self.variables_declaradas[nombre] = []

                if params_str:
                    parametros = [p.strip() for p in params_str.split(",")]

                    for idx, param in enumerate(parametros, 1):
                        # Validar que tenga tipo
                        if re.match(self.patterns.patron_param_con_tipo, param):
                            capa["detalles"].append(
                                f"✓ Parámetro {idx} de {nombre}: {param}"
                            )
                        elif re.match(self.patterns.patron_param_objeto, param):
                            capa["detalles"].append(
                                f"✓ Parámetro objeto {idx} de {nombre}: {param}"
                            )
                        else:
                            # Detectar error específico
                            if re.match(r"^\w+(\[\d*\])*$", param):
                                capa["valido"] = False
                                capa["errores"].append(
                                    f"Subrutina {nombre}, parámetro {idx}: Falta tipo. Use: int {param} o real {param}"
                                )
                            elif re.match(r"^\w+$", param):
                                capa["valido"] = False
                                capa["errores"].append(
                                    f"Subrutina {nombre}, parámetro {idx}: Falta tipo. Use: int {param} o bool {param}"
                                )
                            else:
                                capa["valido"] = False
                                capa["errores"].append(
                                    f"Subrutina {nombre}, parámetro {idx}: Formato inválido: {param}"
                                )
                else:
                    capa["detalles"].append(f"✓ Subrutina {nombre} sin parámetros")

                # 3. Validar variables locales
                self._validar_variables_locales(nombre, subrutina, capa)

        return capa

    def _validar_variables_locales(
        self, nombre_subrutina: str, lineas_subrutina: list, capa: dict
    ):
        """Valida declaraciones de variables locales con tipado"""

        # Buscar declaraciones después del BEGIN
        idx = 0
        while idx < len(lineas_subrutina) and not re.match(
            self.patterns.patron_begin, lineas_subrutina[idx].strip()
        ):
            idx += 1

        idx += 1  # Saltar el BEGIN

        # Leer declaraciones (deben estar al inicio)
        while idx < len(lineas_subrutina):
            linea = lineas_subrutina[idx].strip()

            # Si encuentra algo que no es declaración, terminar
            if (
                re.match(self.patterns.patron_if, linea)
                or re.match(self.patterns.patron_while, linea)
                or re.match(self.patterns.patron_for, linea)
                or re.match(self.patterns.patron_asignacion, linea)
                or re.match(self.patterns.patron_call, linea)
                or re.match(self.patterns.patron_return, linea)
                or re.match(self.patterns.patron_end, linea)
            ):
                break

            # Validar declaración con tipo
            if re.match(self.patterns.patron_var_con_tipo, linea):
                self.variables_declaradas[nombre_subrutina].append(linea)
                capa["detalles"].append(
                    f"✓ Variable local en {nombre_subrutina}: {linea}"
                )
            elif re.match(self.patterns.patron_var_multiple, linea):
                self.variables_declaradas[nombre_subrutina].append(linea)
                capa["detalles"].append(
                    f"✓ Declaración múltiple en {nombre_subrutina}: {linea}"
                )
            elif re.match(self.patterns.patron_param_objeto, linea) and "🡨" not in linea:
                self.variables_declaradas[nombre_subrutina].append(linea)
                capa["detalles"].append(
                    f"✓ Objeto local en {nombre_subrutina}: {linea}"
                )
            else:
                # Detectar declaraciones sin tipo (ERROR)
                if re.match(r"^\w+$", linea):
                    capa["valido"] = False
                    capa["errores"].append(
                        f"Variable en {nombre_subrutina} sin tipo: {linea}. Use: int {linea} o bool {linea}"
                    )
                elif re.match(r"^\w+(\s*,\s*\w+)+$", linea):
                    capa["valido"] = False
                    capa["errores"].append(
                        f"Declaración múltiple sin tipo en {nombre_subrutina}: {linea}. Use: int {linea}"
                    )
                elif re.match(self.patterns.patron_var_multiple_sin_comas, linea):
                    capa["valido"] = False
                    capa["errores"].append(
                        f"Declaración múltiple sin comas en {nombre_subrutina}: {linea}. Use comas: int {linea.replace(' ', ', ')}"
                    )
                elif re.match(r"^\w+\[\d+\]$", linea):
                    capa["valido"] = False
                    capa["errores"].append(
                        f"Vector sin tipo en {nombre_subrutina}: {linea}. Use: int {linea}"
                    )

            idx += 1

    def _validar_capa_estructura(self) -> dict:
        """Valida la estructura del programa y balance de bloques"""
        capa = {"valido": True, "errores": [], "detalles": []}
        capa["detalles"].append("Validando estructura del programa...")

        # 1. Validar orden: Clases → Subrutinas
        if self.secciones["clases"]:
            capa["detalles"].append(
                f"✓ {len(self.secciones['clases'])} clase(s) al inicio"
            )

        if self.secciones["subrutinas"]:
            capa["detalles"].append(
                f"✓ {len(self.secciones['subrutinas'])} subrutina(s) después de clases"
            )

        # 2. Validar balance de bloques en cada subrutina
        for idx, subrutina in enumerate(self.secciones["subrutinas"], 1):
            nombre_sub = (
                self.subrutinas_definidas[idx - 1]
                if idx <= len(self.subrutinas_definidas)
                else f"Subrutina_{idx}"
            )

            pila_begin = []
            pila_repeat = []

            for num_linea, linea in enumerate(subrutina, 1):
                linea = linea.strip()

                if re.match(self.patterns.patron_begin, linea):
                    pila_begin.append(num_linea)
                elif re.match(self.patterns.patron_end, linea):
                    if pila_begin:
                        pila_begin.pop()
                    else:
                        capa["valido"] = False
                        capa["errores"].append(
                            f"{nombre_sub}, línea {num_linea}: END sin BEGIN correspondiente"
                        )

                if re.match(self.patterns.patron_repeat, linea):
                    pila_repeat.append(num_linea)
                elif re.match(self.patterns.patron_until, linea):
                    if pila_repeat:
                        pila_repeat.pop()
                    else:
                        capa["valido"] = False
                        capa["errores"].append(
                            f"{nombre_sub}, línea {num_linea}: UNTIL sin REPEAT correspondiente"
                        )

            # Verificar que no queden bloques abiertos
            if pila_begin:
                capa["valido"] = False
                for linea_num in pila_begin:
                    capa["errores"].append(
                        f"{nombre_sub}, línea {linea_num}: BEGIN sin cerrar"
                    )
            else:
                capa["detalles"].append(f"✓ BEGIN/END balanceados en {nombre_sub}")

            if pila_repeat:
                capa["valido"] = False
                for linea_num in pila_repeat:
                    capa["errores"].append(
                        f"{nombre_sub}, línea {linea_num}: REPEAT sin UNTIL"
                    )
            else:
                capa["detalles"].append(f"✓ REPEAT/UNTIL balanceados en {nombre_sub}")

        return capa

    def _separar_secciones(self) -> dict:
        """Separa el código en clases y subrutinas"""
        secciones = {"clases": [], "subrutinas": []}

        idx = 0

        # Extraer clases
        while idx < len(self.codigo_limpio):
            if re.match(self.patterns.patron_clase, self.codigo_limpio[idx]):
                secciones["clases"].append(self.codigo_limpio[idx])
                idx += 1
            else:
                break

        # Extraer subrutinas
        while idx < len(self.codigo_limpio):
            if re.match(self.patterns.patron_subrutina, self.codigo_limpio[idx]):
                inicio = idx
                nivel_begin = 0
                idx += 1

                # Buscar BEGIN
                if idx < len(self.codigo_limpio) and re.match(
                    self.patterns.patron_begin, self.codigo_limpio[idx]
                ):
                    nivel_begin = 1
                    idx += 1

                    # Buscar END que cierra
                    while idx < len(self.codigo_limpio) and nivel_begin > 0:
                        if re.match(self.patterns.patron_begin, self.codigo_limpio[idx]):
                            nivel_begin += 1
                        elif re.match(self.patterns.patron_end, self.codigo_limpio[idx]):
                            nivel_begin -= 1
                        idx += 1

                    secciones["subrutinas"].append(self.codigo_limpio[inicio:idx])
                else:
                    secciones["subrutinas"].append([self.codigo_limpio[inicio]])
                    idx += 1
            else:
                idx += 1

        return secciones
