import type { BoundAnalysis } from '../types';

export const mockBounds: BoundAnalysis[] = [
  {
    cota: 'Superior (O)',
    escenario: 'Peor caso',
    valor: 'x ∉ A',
    notacion: 'O(n)',
    expanded: {
      analysis: 'Se recorren todos los n elementos del array sin encontrar el elemento buscado.',
      formula: 'T(n) = c₁ + c₂(n+1) + c₃n = c₁ + c₂n + c₂ + c₃n = (c₂ + c₃)n + (c₁ + c₂) = O(n)'
    }
  },
  {
    cota: 'Promedio (Θ)',
    escenario: 'Caso promedio',
    valor: 'x ∈ A, posición aleatoria',
    notacion: 'Θ(n)',
    expanded: {
      analysis: 'En promedio, el elemento se encuentra en la mitad del array, requiriendo aproximadamente n/2 comparaciones.',
      formula: 'Tₐᵥₘ(n) = Σ P(i) × Cost(i) = (1/n) × Σ i = (1/n) × n(n+1)/2 = (n+1)/2 = Θ(n)'
    }
  },
  {
    cota: 'Inferior (Ω)',
    escenario: 'Mejor caso',
    valor: 'A[0] = x',
    notacion: 'Ω(1)',
    expanded: {
      analysis: 'El elemento se encuentra en la primera posición, realizando solo una comparación.',
      formula: 'T(n) = c₁ + c₂ + c₃ + c₄ = Ω(1)'
    }
  }
];
