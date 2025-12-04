import { createSignal } from 'solid-js';
import { H1, H2 } from '../components/ui/Typography';
import Table, { type Column } from '../components/ui/Table';
import ContentContainer from '../components/layout/ContentContainer';
import { mockBounds } from '../mock-data/bounds';
import type { BoundAnalysis } from '../types';

/**
 * Notaciones page - Asymptotic bounds analysis
 * Shows upper, average, and lower bounds with expandable details
 */
export default function Notaciones() {
  const [expandedRows, setExpandedRows] = createSignal<Set<number>>(new Set());

  const toggleRow = (_item: BoundAnalysis, index: number) => {
    const newSet = new Set(expandedRows());
    if (newSet.has(index)) {
      newSet.delete(index);
    } else {
      newSet.add(index);
    }
    setExpandedRows(newSet);
  };

  const boundsColumns: Column<BoundAnalysis>[] = [
    { key: 'cota', header: 'Cota', width: 'w-40' },
    { key: 'escenario', header: 'Escenario', width: 'w-48' },
    { key: 'valor', header: 'Valor', width: 'w-40' },
    { key: 'notacion', header: 'Notación', width: 'w-32' },
  ];

  const renderExpandedContent = (item: BoundAnalysis) => (
    <div class="space-y-4">
      {/* Analysis text */}
      <div class="bg-gray-50/80 border-l-4 border-purple-500 rounded-lg p-4">
        <h4 class="text-sm font-semibold text-gray-900 mb-2">Análisis</h4>
        <p class="text-sm text-gray-700 leading-relaxed">{item.expanded.analysis}</p>
      </div>

      {/* Mathematical formula */}
      <div class="bg-gray-900/95 backdrop-blur-xl border-2 border-gray-700 rounded-lg p-4">
        <h4 class="text-xs font-semibold text-green-400 mb-3 uppercase tracking-wide">Fórmula matemática</h4>
        <code class="font-mono text-sm text-green-300 leading-relaxed block whitespace-pre-wrap">
          {item.expanded.formula}
        </code>
      </div>
    </div>
  );

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        {/* Header */}
        <H1 class="text-center">Cotas Asintóticas</H1>

        {/* Grid Layout: Table + Math Panel */}
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Bounds Table - Left Side */}
          <div class="lg:col-span-7">
            <H2 gradient class="mb-6">Análisis de complejidad</H2>
            <Table
              data={mockBounds}
              columns={boundsColumns}
              expandable={true}
              expandedRows={expandedRows()}
              onRowClick={toggleRow}
              expandedContent={renderExpandedContent}
            />
          </div>

          {/* Math Panel - Right Side */}
          <div class="lg:col-span-5">
            <div class="bg-gray-900/95 backdrop-blur-xl border-2 border-gray-700 rounded-lg p-6 elevation-3 sticky top-4">
              <h3 class="text-lg font-semibold text-green-400 mb-4 uppercase tracking-wide">
                Representación matemática
              </h3>

              <div class="space-y-6 font-mono text-xs text-green-300 leading-relaxed">
                {/* Upper Bound - O notation */}
                <div class="space-y-2">
                  <p class="text-green-400 font-bold text-sm">Cota Superior - O(n)</p>
                  <div class="bg-black/40 rounded p-3 border border-green-900/50">
                    <p>∃ c, n₀ &gt; 0 tal que:</p>
                    <p class="mt-1">T(n) ≤ c·g(n) ∀ n ≥ n₀</p>
                  </div>
                  <p class="text-gray-400 text-xs italic">Peor caso: recorrido completo del array</p>
                </div>

                {/* Average Bound - Θ notation */}
                <div class="space-y-2">
                  <p class="text-green-400 font-bold text-sm">Cota Promedio - Θ(n)</p>
                  <div class="bg-black/40 rounded p-3 border border-green-900/50">
                    <p>∃ c₁, c₂, n₀ &gt; 0 tal que:</p>
                    <p class="mt-1">c₁·g(n) ≤ T(n) ≤ c₂·g(n)</p>
                    <p class="mt-1">∀ n ≥ n₀</p>
                  </div>
                  <p class="text-gray-400 text-xs italic">Caso promedio: elemento en posición n/2</p>
                </div>

                {/* Lower Bound - Ω notation */}
                <div class="space-y-2">
                  <p class="text-green-400 font-bold text-sm">Cota Inferior - Ω(1)</p>
                  <div class="bg-black/40 rounded p-3 border border-green-900/50">
                    <p>∃ c, n₀ &gt; 0 tal que:</p>
                    <p class="mt-1">T(n) ≥ c·g(n) ∀ n ≥ n₀</p>
                  </div>
                  <p class="text-gray-400 text-xs italic">Mejor caso: elemento en primera posición</p>
                </div>

                {/* Summary */}
                <div class="pt-4 border-t border-green-900/50">
                  <p class="text-green-400 font-semibold mb-2">Notación asintótica</p>
                  <ul class="space-y-1 text-gray-300">
                    <li>• O(g) - límite superior (≤)</li>
                    <li>• Ω(g) - límite inferior (≥)</li>
                    <li>• Θ(g) - límite ajustado (=)</li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ContentContainer>
  );
}
