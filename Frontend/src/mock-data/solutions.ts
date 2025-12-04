import type { AlgorithmClassification, RecurrenceSolution, AlgorithmSolution } from '../types';

export const mockClassification: AlgorithmClassification = {
  type: 'Búsqueda Iterativa',
  category: 'Algoritmo de búsqueda',
  complexity: 'Lineal'
};

export const mockRecurrence: RecurrenceSolution = {
  formula: 'T(n) = T(n-1) + O(1)',
  result: 'T(n) = O(n)',
  steps: [
    '1. Identificar la relación de recurrencia: T(n) = T(n-1) + c',
    '2. Expandir la recurrencia: T(n) = T(n-2) + 2c = T(n-3) + 3c = ... = T(1) + (n-1)c',
    '3. Caso base: T(1) = c',
    '4. Resultado: T(n) = c + (n-1)c = nc = O(n)'
  ]
};

export const mockSolution: AlgorithmSolution = {
  algorithm: 'Búsqueda Lineal (Linear Search)',
  timeComplexity: {
    best: 'O(1)',
    average: 'Θ(n)',
    worst: 'O(n)'
  },
  spaceComplexity: 'O(1)',
  characteristics: [
    'Algoritmo simple e intuitivo',
    'No requiere que los datos estén ordenados',
    'Examina cada elemento secuencialmente',
    'Ineficiente para grandes volúmenes de datos',
    'Complejidad espacial constante (in-place)',
    'Tiempo de ejecución proporcional al tamaño de entrada'
  ],
  optimizations: [
    'Usar búsqueda binaria si los datos están ordenados (O(log n))',
    'Implementar early termination en casos especiales',
    'Considerar estructuras de datos indexadas (hash table) para búsquedas frecuentes',
    'Ordenar los datos previamente si se realizarán múltiples búsquedas'
  ]
};
