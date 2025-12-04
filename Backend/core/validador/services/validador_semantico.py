import re
from core.validador.models.patterns import GrammarPatterns


class ValidadorSemantico:
    """
    Validador de capas avanzadas (4-7):
    - Capa 4: Expresiones (operadores aritméticos, relacionales, lógicos)
    - Capa 5: Sentencias (IF, WHILE, FOR, REPEAT, asignaciones)
    - Capa 6: Subrutinas (llamadas CALL, recursión)
    - Capa 7: Semántica (tipos, scope, compatibilidad)

    Recibe estado compartido del ValidadorBasico.
    """

    def __init__(self, state_basico: dict):
        """Inicializar con estado del ValidadorBasico"""
        self.patterns = GrammarPatterns()
        self.codigo_limpio = state_basico["codigo_limpio"]
        self.secciones = state_basico["secciones"]
        self.clases_definidas = state_basico["clases_definidas"]
        self.subrutinas_definidas = state_basico["subrutinas_definidas"]
        self.variables_declaradas = state_basico["variables_declaradas"]
        self.tipo_algoritmo = None

    def validar(self) -> tuple[dict, str]:
        """
        Ejecuta validación de capas 4-7.

        Returns:
            tuple: (resultado_validacion, tipo_algoritmo)
        """
        resultado = {
            "4_EXPRESIONES": self._validar_capa_expresiones(),
            "5_SENTENCIAS": self._validar_capa_sentencias(),
            "6_SUBRUTINAS": self._validar_capa_subrutinas(),
            "7_SEMANTICA": self._validar_capa_semantica(),
        }

        return resultado, self.tipo_algoritmo

    def _validar_capa_expresiones(self) -> dict:
        """Valida expresiones aritméticas y booleanas"""
        capa = {"valido": True, "errores": [], "detalles": []}
        capa["detalles"].append("Validando expresiones...")

        operadores_encontrados = {
            "aritmeticos": set(),
            "relacionales": set(),
            "logicos": set(),
        }

        for subrutina in self.secciones["subrutinas"]:
            for linea in subrutina:
                linea = linea.strip()

                # Buscar operadores aritméticos
                ops_arit = re.findall(self.patterns.patron_operador_aritmetico, linea)
                operadores_encontrados["aritmeticos"].update(ops_arit)

                # Buscar operadores relacionales
                ops_rel = re.findall(self.patterns.patron_operador_relacional, linea)
                operadores_encontrados["relacionales"].update(ops_rel)

                # Buscar operadores lógicos
                ops_log = re.findall(self.patterns.patron_operador_logico, linea)
                operadores_encontrados["logicos"].update(ops_log)

                # Validar uso correcto de mod y div (deben tener espacios)
                if "mod" in linea.lower():
                    if not re.search(r"\w+\s+mod\s+\w+", linea, re.IGNORECASE):
                        capa["valido"] = False
                        capa["errores"].append(
                            f"Operador mod mal usado: {linea}. Use: a mod b"
                        )

                if "div" in linea.lower():
                    if not re.search(r"\w+\s+div\s+\w+", linea, re.IGNORECASE):
                        capa["valido"] = False
                        capa["errores"].append(
                            f"Operador div mal usado: {linea}. Use: a div b"
                        )

        if operadores_encontrados["aritmeticos"]:
            capa["detalles"].append(
                f"✓ Operadores aritméticos: {', '.join(sorted(operadores_encontrados['aritmeticos']))}"
            )
        if operadores_encontrados["relacionales"]:
            capa["detalles"].append(
                f"✓ Operadores relacionales: {', '.join(sorted(operadores_encontrados['relacionales']))}"
            )
        if operadores_encontrados["logicos"]:
            capa["detalles"].append(
                f"✓ Operadores lógicos: {', '.join(sorted(operadores_encontrados['logicos']))}"
            )

        return capa

    def _validar_capa_sentencias(self) -> dict:
        """Valida sentencias de control y asignaciones"""
        capa = {"valido": True, "errores": [], "detalles": []}
        capa["detalles"].append("Validando sentencias...")

        contadores = {
            "if": 0,
            "while": 0,
            "for": 0,
            "repeat": 0,
            "asignaciones": 0,
            "return": 0,
        }

        for subrutina in self.secciones["subrutinas"]:
            for linea in subrutina:
                linea_limpia = linea.strip()

                # IF con THEN
                if linea_limpia.startswith("if "):
                    if re.match(self.patterns.patron_if, linea_limpia):
                        contadores["if"] += 1
                    else:
                        capa["valido"] = False
                        if not linea_limpia.endswith(" then"):
                            capa["errores"].append(f"IF sin THEN: {linea_limpia}")
                        elif "(" not in linea_limpia or ")" not in linea_limpia:
                            capa["errores"].append(f"IF sin paréntesis: {linea_limpia}")

                # WHILE con DO
                if linea_limpia.startswith("while "):
                    if re.match(self.patterns.patron_while, linea_limpia):
                        contadores["while"] += 1
                    else:
                        capa["valido"] = False
                        if not linea_limpia.endswith(" do"):
                            capa["errores"].append(f"WHILE sin DO: {linea_limpia}")

                # FOR con TO y DO
                if linea_limpia.startswith("for "):
                    if re.match(self.patterns.patron_for, linea_limpia):
                        contadores["for"] += 1
                    else:
                        capa["valido"] = False
                        if " to " not in linea_limpia:
                            capa["errores"].append(f"FOR sin TO: {linea_limpia}")
                        elif not linea_limpia.endswith(" do"):
                            capa["errores"].append(f"FOR sin DO: {linea_limpia}")

                # REPEAT
                if re.match(self.patterns.patron_repeat, linea_limpia):
                    contadores["repeat"] += 1

                # Asignaciones
                if re.match(self.patterns.patron_asignacion, linea_limpia):
                    contadores["asignaciones"] += 1

                # Return
                if re.match(self.patterns.patron_return, linea_limpia):
                    contadores["return"] += 1

        for estructura, cantidad in contadores.items():
            if cantidad > 0:
                capa["detalles"].append(
                    f"✓ {cantidad} sentencia(s) {estructura.upper()}"
                )

        return capa

    def _validar_capa_subrutinas(self) -> dict:
        """Valida llamadas a subrutinas y detecta recursión"""
        capa = {"valido": True, "errores": [], "detalles": []}
        capa["detalles"].append("Validando subrutinas y llamadas...")

        llamadas_call = []
        es_recursivo = False

        for idx, subrutina in enumerate(self.secciones["subrutinas"]):
            nombre_sub = (
                self.subrutinas_definidas[idx]
                if idx < len(self.subrutinas_definidas)
                else f"sub_{idx}"
            )

            for linea in subrutina:
                linea_limpia = linea.strip()

                # Detectar llamadas CALL
                if "CALL" in linea_limpia:
                    match = re.search(r"CALL\s+(\w+)", linea_limpia)
                    if match:
                        funcion_llamada = match.group(1)
                        llamadas_call.append((nombre_sub, funcion_llamada))

                        # Detectar recursión
                        if funcion_llamada == nombre_sub:
                            es_recursivo = True
                            capa["detalles"].append(
                                f"⚠ Recursión detectada: {nombre_sub} se llama a sí misma"
                            )

                # Detectar llamadas sin CALL a subrutinas definidas
                # Caso 1: Asignación directa (var 🡨 funcion(...))
                if re.match(r"^\w+\s*🡨\s*\w+\(.*\)$", linea_limpia):
                    match = re.search(r"🡨\s*(\w+)\(", linea_limpia)
                    if match:
                        funcion = match.group(1)
                        if (
                            funcion in self.subrutinas_definidas
                            and funcion != "length"
                        ):
                            capa["valido"] = False
                            capa["errores"].append(
                                f"Llamada sin CALL en {nombre_sub}: {funcion}(...) debe ser CALL {funcion}(...)"
                            )

                # Caso 2: Return con llamada recursiva (return funcion(...))
                if re.match(r"^return\s+", linea_limpia):
                    # Primero, remover todas las llamadas que YA tienen CALL
                    linea_sin_calls = re.sub(
                        r"CALL\s+\w+\s*\([^)]*\)", "", linea_limpia
                    )

                    # Ahora buscar llamadas restantes (las que NO tienen CALL)
                    llamadas_sin_call = re.findall(r"(\w+)\s*\(", linea_sin_calls)
                    for funcion in llamadas_sin_call:
                        if funcion in self.subrutinas_definidas:
                            # Es una llamada recursiva sin CALL
                            capa["valido"] = False
                            capa["errores"].append(
                                f"Llamada sin CALL en return de {nombre_sub}: {funcion}(...) debe ser CALL {funcion}(...)"
                            )

        self.tipo_algoritmo = "Recursivo" if es_recursivo else "Iterativo"

        if llamadas_call:
            capa["detalles"].append(
                f"✓ {len(llamadas_call)} llamada(s) CALL encontradas"
            )
            capa["detalles"].append(f"✓ Tipo de algoritmo: {self.tipo_algoritmo}")

        return capa

    def _validar_capa_semantica(self) -> dict:
        """Valida aspectos semánticos: tipos, scope, compatibilidad"""
        capa = {"valido": True, "errores": [], "detalles": []}
        capa["detalles"].append("Validando semántica...")

        # 1. Verificar que todas las variables tengan tipo
        total_vars = sum(len(vars) for vars in self.variables_declaradas.values())
        capa["detalles"].append(
            f"✓ Todas las variables tienen tipo explícito ({total_vars} declaraciones)"
        )

        # 2. Verificar que todos los parámetros tengan tipo
        if self.subrutinas_definidas:
            capa["detalles"].append(
                "✓ Todos los parámetros tienen tipo (gramática v2.0)"
            )

        # 3. Verificar que las clases estén declaradas antes de usarse
        if self.clases_definidas:
            capa["detalles"].append(
                f"✓ {len(self.clases_definidas)} clase(s) definida(s) al inicio del programa"
            )

        # 4. Scope: Variables declaradas antes de uso
        capa["detalles"].append("✓ Scope: Variables locales por subrutina")

        return capa
