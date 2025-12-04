import type { ScenarioRow } from '../types';

export const mockScenarios: ScenarioRow[] = [
  {
    id: 's0-best',
    s0: 'x ∈ A',
    A0: 'A[0] = x',
    exito: 'true',
    k: '1',
    lineCosts: [
      { line_number: 1, code: 'n ← length(A)', C_op: 1, Freq: '1', Total: '1' },
      { line_number: 2, code: 'FOR i ← 0 TO n-1', C_op: 1, Freq: '1', Total: '1' },
      { line_number: 3, code: 'IF A[i] = x', C_op: 1, Freq: '1', Total: '1' },
      { line_number: 4, code: 'RETURN i', C_op: 1, Freq: '1', Total: '1' },
    ],
    justification: 'Mejor caso: El elemento se encuentra en la primera posición del array, por lo que solo se realiza una comparación.',
    cost: 'Θ(1)'
  },
  {
    id: 's1-worst',
    s0: 'x ∉ A',
    A0: 'N/A',
    exito: 'false',
    k: 'n',
    lineCosts: [
      { line_number: 1, code: 'n ← length(A)', C_op: 1, Freq: '1', Total: '1' },
      { line_number: 2, code: 'FOR i ← 0 TO n-1', C_op: 1, Freq: 'n+1', Total: 'n+1' },
      { line_number: 3, code: 'IF A[i] = x', C_op: 1, Freq: 'n', Total: 'n' },
      { line_number: 5, code: 'RETURN -1', C_op: 1, Freq: '1', Total: '1' },
    ],
    justification: 'Peor caso: El elemento no existe en el array, por lo que se recorren todos los n elementos sin encontrar coincidencia.',
    cost: 'Θ(n)'
  },
  {
    id: 's2-average',
    s0: 'x ∈ A',
    A0: 'A[k] = x, k aleatorio',
    exito: 'true',
    k: '(n+1)/2',
    lineCosts: [
      { line_number: 1, code: 'n ← length(A)', C_op: 1, Freq: '1', Total: '1' },
      { line_number: 2, code: 'FOR i ← 0 TO n-1', C_op: 1, Freq: '(n+1)/2+1', Total: '(n+1)/2+1' },
      { line_number: 3, code: 'IF A[i] = x', C_op: 1, Freq: '(n+1)/2', Total: '(n+1)/2' },
      { line_number: 4, code: 'RETURN i', C_op: 1, Freq: '1', Total: '1' },
    ],
    justification: 'Caso promedio: El elemento se encuentra en una posición aleatoria, en promedio se recorren n/2 elementos antes de encontrarlo.',
    cost: 'Θ(n)'
  }
];
