"""
Loop Counter Tool

Herramienta que analiza ciclos (for, while, repeat) en pseudocódigo
y determina el número de iteraciones y tipo de complejidad.
"""

import re
from typing import Dict, List, Optional


class LoopCounter:
    """
    Analiza ciclos en pseudocódigo y determina su complejidad.

    Soporta:
    - Ciclos FOR con sintaxis: for <var> <- <inicio> to <fin> do
    - Ciclos WHILE con sintaxis: while (<condicion>) do
    - Ciclos REPEAT con sintaxis: repeat ... until (<condicion>)
    """

    # Patrones de expresiones regulares para identificar ciclos
    # Acepta: <-, 🡨, ←, :=, y =
    PATRON_FOR = r'for\s+(\w+)\s*(<-|🡨|←|:=|=)\s*(.+?)\s+to\s+(.+?)\s+do'
    PATRON_WHILE = r'while\s*\((.+?)\)\s*do'
    PATRON_REPEAT = r'repeat|repetir'
    PATRON_UNTIL = r'until\s*\((.+?)\)'

    # Patrones para detectar modificaciones de variables
    # Acepta: <-, 🡨, ←, :=, y =
    PATRON_INCREMENTO_LINEAL = r'(\w+)\s*(<-|🡨|←|:=|=)\s*\1\s*\+\s*(\d+)'  # i = i + 1
    PATRON_DECREMENTO_LINEAL = r'(\w+)\s*(<-|🡨|←|:=|=)\s*\1\s*-\s*(\d+)'  # i = i - 1
    PATRON_MULTIPLICACION = r'(\w+)\s*(<-|🡨|←|:=|=)\s*\1\s*\*\s*(\d+)'    # i = i * 2
    PATRON_DIVISION = r'(\w+)\s*(<-|🡨|←|:=|=)\s*\1\s*/\s*(\d+)'           # i = i / 2

    def __init__(self):
        """Inicializa el contador de ciclos."""
        pass

    def analizar_for(self, linea_for: str) -> Dict:
        """
        Analiza un ciclo FOR y determina sus iteraciones.

        Args:
            linea_for: Línea con la declaración del FOR
                       Ejemplo: "for i <- 1 to n do"

        Returns:
            Dict con la información del ciclo:
            {
                "variable": str,          # Variable de control (ej: "i")
                "inicio": str,            # Valor inicial (ej: "1")
                "fin": str,               # Valor final (ej: "n")
                "iteraciones": str,       # Expresión de iteraciones (ej: "n")
                "tipo": str,              # Tipo de complejidad (ej: "lineal")
                "complejidad": str,       # Notación Big-O (ej: "O(n)")
                "valido": bool            # Si se pudo analizar correctamente
            }

        Ejemplos:
            >>> analizar_for("for i <- 1 to n do")
            {"variable": "i", "inicio": "1", "fin": "n",
             "iteraciones": "n", "tipo": "lineal", "complejidad": "O(n)"}

            >>> analizar_for("for i <- 1 to n-1 do")
            {"variable": "i", "inicio": "1", "fin": "n-1",
             "iteraciones": "n-1", "tipo": "lineal", "complejidad": "O(n)"}
        """
        linea_limpia = linea_for.strip()

        # Intentar hacer match con el patrón FOR
        match = re.search(self.PATRON_FOR, linea_limpia, re.IGNORECASE)

        if not match:
            return {
                "valido": False,
                "error": "No se pudo parsear el ciclo FOR"
            }

        variable = match.group(1)      # Ej: "i"
        inicio = match.group(3).strip() # Ej: "1"
        fin = match.group(4).strip()    # Ej: "n"

        # Calcular número de iteraciones simbólicamente
        iteraciones = self._calcular_iteraciones_for(inicio, fin)

        # Determinar tipo de complejidad
        tipo, complejidad = self._clasificar_complejidad(iteraciones)

        return {
            "valido": True,
            "variable": variable,
            "inicio": inicio,
            "fin": fin,
            "iteraciones": iteraciones,
            "tipo": tipo,
            "complejidad": complejidad
        }

    def analizar_while(self, linea_while: str, cuerpo: List[str]) -> Dict:
        """
        Analiza un ciclo WHILE.

        Args:
            linea_while: Línea con la declaración del WHILE
                        Ejemplo: "while (i <= n) do"
            cuerpo: Lista de líneas dentro del ciclo

        Returns:
            Dict con información del ciclo similar a analizar_for()

        Estrategia:
        1. Extraer la condición del while
        2. Identificar la variable de control de la condición
        3. Buscar en el cuerpo cómo se modifica esa variable
        4. Estimar iteraciones según el tipo de modificación
        """
        linea_limpia = linea_while.strip()

        # Extraer condición
        match = re.search(self.PATRON_WHILE, linea_limpia, re.IGNORECASE)

        if not match:
            return {
                "valido": False,
                "error": "No se pudo parsear el ciclo WHILE"
            }

        condicion = match.group(1).strip()

        # Intentar identificar variable de control de la condición
        variable_control = self._extraer_variable_condicion(condicion)

        if not variable_control:
            return {
                "valido": False,
                "error": "No se pudo identificar variable de control"
            }

        # Analizar el cuerpo para ver cómo se modifica la variable
        tipo_modificacion = self._analizar_modificacion_variable(variable_control, cuerpo)

        # Estimar iteraciones según el tipo de modificación
        iteraciones, tipo, complejidad = self._estimar_iteraciones_while(
            condicion,
            tipo_modificacion
        )

        return {
            "valido": True,
            "condicion": condicion,
            "variable_control": variable_control,
            "tipo_modificacion": tipo_modificacion,
            "iteraciones": iteraciones,
            "tipo": tipo,
            "complejidad": complejidad
        }

    def analizar_repeat(self, cuerpo: List[str], linea_until: str) -> Dict:
        """
        Analiza un ciclo REPEAT-UNTIL.

        Args:
            cuerpo: Lista de líneas dentro del repeat
            linea_until: Línea con la condición until
                        Ejemplo: "until (i > n)"

        Returns:
            Dict con información del ciclo similar a analizar_while()

        Nota: REPEAT se ejecuta al menos una vez (diferencia con WHILE)
        """
        linea_limpia = linea_until.strip()

        # Extraer condición del until
        match = re.search(self.PATRON_UNTIL, linea_limpia, re.IGNORECASE)

        if not match:
            return {
                "valido": False,
                "error": "No se pudo parsear la condición UNTIL"
            }

        condicion = match.group(1).strip()

        # Identificar variable de control
        variable_control = self._extraer_variable_condicion(condicion)

        if not variable_control:
            return {
                "valido": False,
                "error": "No se pudo identificar variable de control"
            }

        # Analizar modificación de variable
        tipo_modificacion = self._analizar_modificacion_variable(variable_control, cuerpo)

        # Estimar iteraciones (similar a while)
        iteraciones, tipo, complejidad = self._estimar_iteraciones_while(
            condicion,
            tipo_modificacion
        )

        return {
            "valido": True,
            "tipo_ciclo": "repeat-until",
            "condicion": condicion,
            "variable_control": variable_control,
            "tipo_modificacion": tipo_modificacion,
            "iteraciones": iteraciones,
            "tipo": tipo,
            "complejidad": complejidad,
            "nota": "Se ejecuta al menos una vez"
        }

    def detectar_anidamiento(self, bloques: List[Dict]) -> Dict:
        """
        Detecta ciclos anidados y calcula la complejidad combinada.

        Args:
            bloques: Lista de diccionarios con información de ciclos
                     Cada bloque debe tener "nivel" y "complejidad"

        Returns:
            Dict con información del anidamiento:
            {
                "nivel_anidamiento": int,
                "complejidad_combinada": str,
                "detalle": str
            }

        Ejemplo:
            bloques = [
                {"nivel": 1, "iteraciones": "n", "complejidad": "O(n)"},
                {"nivel": 2, "iteraciones": "n", "complejidad": "O(n)"}
            ]
            → {"nivel_anidamiento": 2, "complejidad_combinada": "O(n²)"}
        """
        if not bloques:
            return {
                "nivel_anidamiento": 0,
                "complejidad_combinada": "O(1)"
            }

        # Encontrar el nivel máximo de anidamiento
        nivel_max = max(bloque.get("nivel", 1) for bloque in bloques)

        # Agrupar ciclos por nivel
        ciclos_por_nivel = {}
        for bloque in bloques:
            nivel = bloque.get("nivel", 1)
            if nivel not in ciclos_por_nivel:
                ciclos_por_nivel[nivel] = []
            ciclos_por_nivel[nivel].append(bloque)

        # Calcular complejidad combinada
        complejidad_combinada = self._combinar_complejidades_anidadas(ciclos_por_nivel)

        return {
            "nivel_anidamiento": nivel_max,
            "complejidad_combinada": complejidad_combinada,
            "ciclos_por_nivel": ciclos_por_nivel
        }

    # ==================== MÉTODOS AUXILIARES PRIVADOS ====================

    def _calcular_iteraciones_for(self, inicio: str, fin: str) -> str:
        """
        Calcula el número de iteraciones de un FOR de forma simbólica.

        Args:
            inicio: Valor inicial (ej: "1", "0")
            fin: Valor final (ej: "n", "n-1", "n/2")

        Returns:
            Expresión simbólica de iteraciones

        Ejemplos:
            (1, n) → "n"
            (0, n-1) → "n"
            (1, n/2) → "n/2"
        """
        # Casos simples
        if inicio == "1" and fin == "n":
            return "n"

        if inicio == "0" and fin == "n-1":
            return "n"

        if inicio == "1" and fin == "n-1":
            return "n-1"

        # Casos con divisiones
        if "/" in fin:
            return fin  # Retornar como está: "n/2", "n/3", etc.

        # Caso general: retornar el fin (simplificación)
        return fin

    def _clasificar_complejidad(self, iteraciones: str) -> tuple:
        """
        Clasifica el tipo de complejidad según las iteraciones.

        Args:
            iteraciones: Expresión de iteraciones (ej: "n", "n/2", "log n")

        Returns:
            Tupla (tipo, complejidad_big_o)

        Ejemplos:
            "n" → ("lineal", "O(n)")
            "n/2" → ("lineal", "O(n)")
            "log n" → ("logaritmico", "O(log n)")
        """
        iteraciones_lower = iteraciones.lower()

        # Casos logarítmicos
        if "log" in iteraciones_lower:
            return ("logaritmico", "O(log n)")

        # Casos lineales (incluyendo n/2, n-1, etc.)
        if "n" in iteraciones_lower and "^" not in iteraciones_lower and "*" not in iteraciones_lower:
            return ("lineal", "O(n)")

        # Casos cuadráticos
        if "n^2" in iteraciones_lower or "n²" in iteraciones_lower:
            return ("cuadratico", "O(n²)")

        # Casos constantes
        if iteraciones.isdigit():
            return ("constante", "O(1)")

        # Caso por defecto
        return ("desconocido", f"O({iteraciones})")

    def _extraer_variable_condicion(self, condicion: str) -> Optional[str]:
        """
        Extrae la variable principal de una condición.

        Args:
            condicion: Expresión booleana (ej: "i <= n", "i < n and i > 0")

        Returns:
            Nombre de la variable de control o None si no se encuentra

        Ejemplos:
            "i <= n" → "i"
            "j < n" → "j"
            "i <= n and not encontrado" → "i"
        """
        # Buscar patrones comunes: variable comparada con algo
        # Patrones: var <= expr, var < expr, var >= expr, var > expr, var = expr
        patron = r'(\w+)\s*(<|<=|>|>=|=|≤|≥)\s*'
        match = re.search(patron, condicion)

        if match:
            return match.group(1)

        # Si no se encuentra, intentar extraer la primera palabra
        palabras = re.findall(r'\w+', condicion)
        if palabras:
            return palabras[0]

        return None

    def _analizar_modificacion_variable(self, variable: str, cuerpo: List[str]) -> Dict:
        """
        Analiza cómo se modifica una variable en el cuerpo de un ciclo.

        Args:
            variable: Nombre de la variable a analizar
            cuerpo: Líneas de código dentro del ciclo

        Returns:
            Dict con información de la modificación:
            {
                "tipo": "incremento_lineal" | "decremento_lineal" |
                        "multiplicacion" | "division" | "desconocido",
                "factor": int o None
            }
        """
        cuerpo_completo = "\n".join(cuerpo)

        # Buscar incremento lineal: i <- i + k
        match = re.search(self.PATRON_INCREMENTO_LINEAL, cuerpo_completo)
        if match and match.group(1) == variable:
            factor = int(match.group(3))
            return {"tipo": "incremento_lineal", "factor": factor}

        # Buscar decremento lineal: i <- i - k
        match = re.search(self.PATRON_DECREMENTO_LINEAL, cuerpo_completo)
        if match and match.group(1) == variable:
            factor = int(match.group(3))
            return {"tipo": "decremento_lineal", "factor": factor}

        # Buscar multiplicación: i <- i * k
        match = re.search(self.PATRON_MULTIPLICACION, cuerpo_completo)
        if match and match.group(1) == variable:
            factor = int(match.group(3))
            return {"tipo": "multiplicacion", "factor": factor}

        # Buscar división: i <- i / k
        match = re.search(self.PATRON_DIVISION, cuerpo_completo)
        if match and match.group(1) == variable:
            factor = int(match.group(3))
            return {"tipo": "division", "factor": factor}

        return {"tipo": "desconocido", "factor": None}

    def _estimar_iteraciones_while(self, condicion: str, tipo_modificacion: Dict) -> tuple:
        """
        Estima las iteraciones de un WHILE según el tipo de modificación.

        Args:
            condicion: Condición del while
            tipo_modificacion: Dict con info de cómo se modifica la variable

        Returns:
            Tupla (iteraciones, tipo, complejidad)
        """
        tipo = tipo_modificacion.get("tipo", "desconocido")

        if tipo == "incremento_lineal":
            return ("n", "lineal", "O(n)")

        if tipo == "decremento_lineal":
            return ("n", "lineal", "O(n)")

        if tipo == "multiplicacion":
            factor = tipo_modificacion.get("factor", 2)
            return (f"log_{factor}(n)", "logaritmico", "O(log n)")

        if tipo == "division":
            factor = tipo_modificacion.get("factor", 2)
            return (f"log_{factor}(n)", "logaritmico", "O(log n)")

        # Caso desconocido: asumir lineal
        return ("n", "desconocido", "O(n)")

    def _combinar_complejidades_anidadas(self, ciclos_por_nivel: Dict) -> str:
        """
        Combina las complejidades de ciclos anidados.

        Regla: Multiplicar las complejidades de cada nivel.

        Ejemplos:
            Nivel 1: O(n), Nivel 2: O(n) → O(n²)
            Nivel 1: O(n), Nivel 2: O(log n) → O(n log n)
        """
        if not ciclos_por_nivel:
            return "O(1)"

        # Contar cuántos niveles de O(n) hay
        niveles_lineales = 0
        tiene_logaritmico = False

        for nivel, ciclos in ciclos_por_nivel.items():
            for ciclo in ciclos:
                complejidad = ciclo.get("complejidad", "O(1)")
                if complejidad == "O(n)":
                    niveles_lineales += 1
                elif complejidad == "O(log n)":
                    tiene_logaritmico = True

        # Construir complejidad combinada
        if niveles_lineales == 0:
            return "O(1)"
        elif niveles_lineales == 1:
            if tiene_logaritmico:
                return "O(n log n)"
            return "O(n)"
        elif niveles_lineales == 2:
            return "O(n²)"
        elif niveles_lineales == 3:
            return "O(n³)"
        else:
            return f"O(n^{niveles_lineales})"
