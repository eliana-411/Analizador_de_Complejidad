"""
Line Cost Calculator - Calcula el costo T(S) para cada escenario

Implementa la fórmula: T(S) = Σ (C_op × Freq) para cada línea del pseudocódigo.

- C_op: Costo invariante (operaciones elementales)
- Freq: Multiplicador de frecuencia (cuántas veces se ejecuta la línea)
"""

import re
import sympy as sp
from typing import List, Dict, Tuple
from Backend.mapeo.models.omega_table import LineCost
from Backend.mapeo.models.scenario_state import LoopInfo


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
        loops: List[LoopInfo]
    ) -> Tuple[str, List[LineCost]]:
        """
        Calcula T(S) para un escenario específico.

        Args:
            lines: Líneas del pseudocódigo
            scenario: Dict con info del escenario (id, condition, early_exit, iteration_value)
            loops: Información de todos los loops del algoritmo

        Returns:
            (formula_total, list_of_line_costs)
        """
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

        # Ignorar headers de loops/if (el costo está en el cuerpo)
        if any(line_clean.startswith(kw) for kw in ['for ', 'while ', 'repeat', 'until ', 'if ', 'else', 'then']):
            return 0

        ops = 0

        # Asignaciones
        if '←' in line_clean or '🡨' in line_clean:
            ops += 1

        # Operaciones aritméticas
        ops += len(re.findall(r'[\+\-\*/]', line_clean))

        # Comparaciones (evitar contar =  en asignaciones)
        comparison_pattern = r'(?<![🡨←])\s*([<>=≤≥≠])\s*'
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
        2. Si línea está en loop(s) → Freq = producto de iteraciones de loops contenedores
        3. Si escenario tiene salida temprana → aplicar modificador de iteraciones

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

        # Encontrar loops que contienen esta línea
        containing_loops = [
            loop for loop in loops
            if loop.start_line <= line_num <= loop.end_line
        ]

        # Multiplicar iteraciones de todos los loops contenedores
        for loop in containing_loops:
            loop_iterations = sp.sympify(loop.iterations)

            # Aplicar modificador si hay salida temprana
            if scenario.get('early_exit'):
                # Si hay salida temprana, usar iteration_value del escenario
                iteration_val = scenario.get('iteration_value', 'n')
                loop_iterations = sp.sympify(iteration_value)

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
