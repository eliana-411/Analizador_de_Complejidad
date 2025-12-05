"""
Line Cost Calculator - Calcula el costo T(S) para cada escenario

Implementa la fórmula: T(S) = Σ (C_op × Freq) para cada línea del pseudocódigo.

- C_op: Costo invariante (operaciones elementales)
- Freq: Multiplicador de frecuencia (cuántas veces se ejecuta la línea)
"""

import re
import sympy as sp
from typing import List, Dict, Tuple, Optional
from core.analizador.models.omega_table import LineCost
from core.analizador.models.scenario_state import LoopInfo
from core.analizador.models.recursion_info import RecursionInfo


class LineCostCalculator:
    """
    Calcula el costo computacional T(S) de un escenario específico
    mediante análisis línea por línea.
    """

    def __init__(self):
        # Símbolos matemáticos para expresiones simbólicas
        self.n = sp.Symbol('n')
        self.k = sp.Symbol('k')
        self.p = sp.Symbol('p')  # Para casos como QuickSort (pivote)

    def calculate_scenario_cost(
        self,
        lines: List[str],
        scenario: Dict,
        loops: List[LoopInfo],
        recursion_info: Optional[RecursionInfo] = None
    ) -> Tuple[str, List[LineCost]]:
        """
        Calcula T(S) para un escenario específico.

        Para algoritmos iterativos: retorna fórmula cerrada (ej: "2*n + 2")
        Para algoritmos recursivos: retorna relación de recurrencia (ej: "T(n) = T(n-1) + 2")

        Args:
            lines: Líneas del pseudocódigo
            scenario: Dict con info del escenario (id, condition, early_exit, iteration_value)
            loops: Información de todos los loops del algoritmo
            recursion_info: Información de recursión (si es recursivo)

        Returns:
            (formula_total, list_of_line_costs)
        """
        # CASO RECURSIVO
        if recursion_info:
            return self._calculate_recursive_cost(lines, scenario, recursion_info)

        # CASO ITERATIVO (lógica existente)
        total = 0
        line_costs = []

        for line_num, line in enumerate(lines):
            # Contar operaciones elementales (C_op)
            c_op = self._count_operations(line)

            # Determinar frecuencia de ejecución (Freq)
            freq = self._get_frequency(line_num, scenario, loops, lines)

            # Calcular costo de esta línea
            cost = c_op * freq
            total += cost

            # Agregar a la lista de costos
            line_costs.append(LineCost(
                line_number=line_num + 1,  # 1-indexed para display
                code=line.strip(),
                C_op=c_op,
                Freq=str(freq),
                Total=str(sp.simplify(cost))
            ))

        # Simplificar expresión total
        simplified = sp.simplify(total)
        return str(simplified), line_costs

    def _count_operations(self, line: str) -> int:
        """
        Cuenta las operaciones elementales en una línea.

        Operaciones consideradas:
        - Asignaciones (←, 🡨): 1 op
        - Operaciones aritméticas (+, -, *, /): 1 op cada una
        - Comparaciones (<, >, =, ≤, ≥, ≠): 1 op
        - Accesos a array (A[i]): 1 op

        Args:
            line: Línea de pseudocódigo

        Returns:
            Número total de operaciones
        """
        line_clean = line.strip()

        # Ignorar líneas estructurales (no tienen operaciones)
        if not line_clean or line_clean in ['begin', 'end']:
            return 0

        # Ignorar declaraciones de variables
        if line_clean.startswith('int ') or line_clean.startswith('bool ') or line_clean.startswith('real '):
            return 0

        # IMPORTANTE: Los encabezados de loops SÍ tienen costo
        # FOR: tiene comparación (i <= n) que se ejecuta n+1 veces
        # WHILE: tiene evaluación de condición
        # Por eso NO los ignoramos aquí, los contamos según su operación

        # Contar operaciones en encabezados de loops
        if line_clean.startswith('for '):
            # for i = 1 to n → tiene comparación implícita
            return 1  # Comparación i <= n

        if line_clean.startswith('while '):
            # while (condicion) → evaluar la condición
            # Contar operaciones en la condición
            match = re.search(r'while\s*\((.+?)\)', line_clean)
            if match:
                condition = match.group(1)
                # Contar comparaciones y operaciones lógicas en la condición
                ops_in_condition = 0
                ops_in_condition += len(re.findall(r'(==|!=|<=|>=|<|>)', condition))
                ops_in_condition += len(re.findall(r'(and|or|not)', condition))
                return max(ops_in_condition, 1)  # Al menos 1 op
            return 1  # Default si no se puede parsear

        # Contar operaciones en IF
        if line_clean.startswith('if '):
            # if (condicion) then → evaluar la condición
            match = re.search(r'if\s*\((.+?)\)\s*then', line_clean)
            if match:
                condition = match.group(1)
                # Contar comparaciones y operaciones lógicas en la condición
                ops_in_condition = 0
                ops_in_condition += len(re.findall(r'(==|!=|<=|>=|<|>)', condition))
                ops_in_condition += len(re.findall(r'(and|or|not)', condition))
                return max(ops_in_condition, 1)  # Al menos 1 op si hay condición
            return 1  # Default si no se puede parsear

        # Ignorar otros headers (else, then, repeat, until)
        if any(line_clean.startswith(kw) for kw in ['else', 'then', 'repeat', 'until ']):
            return 0

        ops = 0

        # Asignaciones (←, 🡨, =, :=)
        # Solo contar como asignación si no es parte de una comparación
        if '←' in line_clean or '🡨' in line_clean:
            ops += 1
        elif '=' in line_clean:
            # Verificar que no sea comparación (==, !=, <=, >=)
            if not any(op in line_clean for op in ['==', '!=', '<=', '>=']):
                ops += 1

        # Operaciones aritméticas
        ops += len(re.findall(r'[\+\-\*/]', line_clean))

        # Comparaciones (evitar contar = en asignaciones)
        # Buscar: ==, !=, <, >, <=, >=
        comparison_pattern = r'(==|!=|<=|>=|<|>)'
        ops += len(re.findall(comparison_pattern, line_clean))

        # Accesos a array
        ops += len(re.findall(r'\w+\[\w+\]', line_clean))

        # Llamadas a funciones (CALL)
        if 'CALL' in line_clean:
            ops += 1  # Costo base de la llamada

        # return
        if line_clean.startswith('return'):
            ops += 1

        return max(ops, 0)

    def _get_frequency(
        self,
        line_num: int,
        scenario: Dict,
        loops: List[LoopInfo],
        lines: List[str]
    ) -> sp.Expr:
        """
        Determina cuántas veces se ejecuta una línea en el escenario dado.

        Estrategia:
        1. Si línea está fuera de loops → Freq = 1
        2. Si línea es ENCABEZADO de loop → Freq = iteraciones + 1 (lógica de ejecución real)
        3. Si línea está DENTRO de loop(s) → Freq = producto de iteraciones de loops contenedores
        4. Si escenario tiene salida temprana → aplicar modificador de iteraciones

        IMPORTANTE: Sigue la lógica real de ejecución:
        - El encabezado del loop (for/while) se evalúa n+1 veces
        - El cuerpo del loop se ejecuta n veces

        Args:
            line_num: Número de línea (0-indexed)
            scenario: Info del escenario (incluye iteration_value, early_exit)
            loops: Todos los loops del algoritmo
            lines: Todas las líneas (para contexto)

        Returns:
            Expresión simbólica de la frecuencia
        """
        # Por defecto, líneas fuera de loops se ejecutan 1 vez
        freq = sp.Integer(1)

        # Obtener la línea actual para verificar si es encabezado de loop
        current_line = lines[line_num].strip().lower() if line_num < len(lines) else ""

        # Verificar si esta línea ES un encabezado de loop
        is_loop_header = (
            current_line.startswith('for ') or
            current_line.startswith('while ') or
            current_line.startswith('repeat')
        )

        # Encontrar loops que contienen esta línea
        # IMPORTANTE: Los loops están indexados desde 0, igual que las líneas
        containing_loops = []
        loop_owner = None  # El loop cuyo encabezado es esta línea

        for loop in loops:
            # Si esta línea ES el encabezado del loop
            if loop.start_line == line_num and is_loop_header:
                loop_owner = loop
            # Si esta línea está DENTRO del rango del loop (pero no es el encabezado)
            elif loop.start_line < line_num <= loop.end_line:
                containing_loops.append(loop)

        # CASO 1: Esta línea es el ENCABEZADO de un loop
        if loop_owner:
            # El encabezado se evalúa (n + 1) veces
            try:
                loop_iterations = sp.sympify(loop_owner.iterations)
            except:
                loop_iterations = self.n

            # Aplicar modificador si hay salida temprana
            if scenario.get('early_exit'):
                iteration_val = scenario.get('iteration_value', 'n')
                try:
                    loop_iterations = sp.sympify(iteration_val)
                except:
                    loop_iterations = self.k

            # Encabezado se evalúa una vez más que el cuerpo
            freq = loop_iterations + 1

        # CASO 2: Esta línea está DENTRO de loop(s)
        elif containing_loops:
            # Multiplicar iteraciones de todos los loops contenedores
            for loop in containing_loops:
                # Convertir string de iteraciones a expresión simbólica
                try:
                    loop_iterations = sp.sympify(loop.iterations)
                except:
                    loop_iterations = self.n

                # Aplicar modificador si hay salida temprana
                if scenario.get('early_exit'):
                    iteration_val = scenario.get('iteration_value', 'n')
                    try:
                        loop_iterations = sp.sympify(iteration_val)
                    except:
                        loop_iterations = self.k

                freq *= loop_iterations

        # Verificar si la línea está en un bloque condicional que NO se ejecuta en este escenario
        if self._is_in_unexecuted_branch(line_num, scenario, lines):
            freq = sp.Integer(0)

        return freq

    def _is_in_unexecuted_branch(
        self,
        line_num: int,
        scenario: Dict,
        lines: List[str]
    ) -> bool:
        """
        Determina si una línea está en un bloque IF que NO se ejecuta en este escenario.

        Por ejemplo, en búsqueda lineal con escenario "no encontrado",
        la línea "encontrado ← T" NO se ejecuta.

        Args:
            line_num: Número de línea
            scenario: Info del escenario
            lines: Todas las líneas

        Returns:
            True si la línea no se ejecuta en este escenario
        """
        # MVP: Simplificado
        # Versión completa requeriría parsing completo del IF/THEN/ELSE

        # Heurística simple: si el escenario indica "FALLO" y la línea
        # está cerca de un "then" que modifica variables de éxito, no se ejecuta
        line = lines[line_num].strip().lower()

        scenario_state = scenario.get('state', '').upper()

        # Si estado es FALLO y línea asigna True a variable "encontrado/success"
        if 'FALLO' in scenario_state or 'FAILURE' in scenario_state:
            if ('🡨' in line or '←' in line) and ('t' == line[-1].lower() or 'true' in line.lower()):
                return True

        return False

    def _calculate_recursive_cost(
        self,
        lines: List[str],
        scenario: Dict,
        recursion_info: RecursionInfo
    ) -> Tuple[str, List[LineCost]]:
        """
        Calcula la relación de recurrencia para un algoritmo recursivo
        y genera tabla de costos línea por línea COMPLETA.

        Para recursivos, la tabla muestra:
        - TODAS las líneas del algoritmo
        - Las llamadas recursivas tienen costo "T(pattern)" en lugar de numérico
        - El costo total es una relación de recurrencia

        Ejemplos de output:
        - Factorial: "T(n) = T(n-1) + 2"
        - Binary search: "T(n) = T(n/2) + 3"
        - Merge sort: "T(n) = 2*T(n/2) + n"

        Args:
            lines: Líneas del pseudocódigo
            scenario: Info del escenario
            recursion_info: Estructura de recursión

        Returns:
            (recurrence_relation, line_costs)
        """
        line_costs = []
        non_recursive_cost = 0
        recursive_cost_term = ""  # T(n-1), T(n/2), etc.

        # Obtener patrón de recursión
        num_calls = recursion_info.num_calls
        patterns = recursion_info.call_pattern if recursion_info.call_pattern else ["n-1"]

        # Ajustar patrón según escenario (balanced vs skewed)
        recursion_pattern = scenario.get("recursion_pattern", "standard")
        if recursion_pattern == "skewed" and "divide" in recursion_info.recurrence_type:
            # Peor caso: división desbalanceada
            patterns = ["n-1"]
            num_calls = 1

        # Formatear término recursivo
        # Si todos los patrones son iguales: num_calls*T(pattern)
        # Si son diferentes: T(pattern1) + T(pattern2) + ...
        if len(set(patterns)) == 1:
            # Todos los patrones son iguales
            pattern = patterns[0]
            if num_calls == 1:
                recursive_cost_term = f"T({pattern})"
            else:
                recursive_cost_term = f"{num_calls}*T({pattern})"
        else:
            # Patrones diferentes (ej: fibonacci con T(n-1) + T(n-2))
            recursive_cost_term = " + ".join([f"T({p})" for p in patterns])

        # 1. Generar tabla COMPLETA línea por línea
        for line_num, line in enumerate(lines):
            c_op = self._count_operations(line)

            # Determinar si es una llamada recursiva
            is_recursive = self._is_recursive_call(line)

            if is_recursive:
                # Llamada recursiva: contar operaciones NO recursivas + mostrar T(pattern)
                # Ejemplo: "return n * CALL factorial(n-1)" tiene 2 ops (return + *) + T(n-1)

                # Contar operaciones excluyendo la llamada CALL
                line_without_call = line.replace("CALL", "").replace("call", "")
                non_recursive_ops = self._count_operations(line_without_call)

                # Total = ops_no_recursivas + T(pattern)
                if non_recursive_ops > 0:
                    total = f"{non_recursive_ops} + {recursive_cost_term}"
                else:
                    total = recursive_cost_term

                line_costs.append(LineCost(
                    line_number=line_num + 1,
                    code=line.strip(),
                    C_op=non_recursive_ops,
                    Freq="1",
                    Total=total
                ))

                # Acumular costo no recursivo
                non_recursive_cost += non_recursive_ops
            else:
                # Línea normal: mostrar su costo
                freq = "1"  # En recursivos simples, cada línea se ejecuta 1 vez por llamada
                total = str(c_op) if c_op > 0 else "0"

                line_costs.append(LineCost(
                    line_number=line_num + 1,
                    code=line.strip(),
                    C_op=c_op,
                    Freq=freq,
                    Total=total
                ))

                # Acumular costo no recursivo
                non_recursive_cost += c_op

        # 2. Construir relación de recurrencia
        # Usar recursive_cost_term que ya tiene el formato correcto
        if non_recursive_cost > 0:
            recurrence = f"T(n) = {recursive_cost_term} + {non_recursive_cost}"
        else:
            recurrence = f"T(n) = {recursive_cost_term}"

        # Simplificación: eliminar " + 0" si el costo no recursivo es 0
        recurrence = recurrence.replace(" + 0", "").strip()

        return recurrence, line_costs

    def _is_recursive_call(self, line: str) -> bool:
        """
        Determina si una línea contiene una llamada recursiva.

        Args:
            line: Línea de código

        Returns:
            True si la línea contiene CALL
        """
        line_clean = line.strip()
        return "CALL" in line_clean or "call" in line_clean.lower()
