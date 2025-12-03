import { createSignal } from 'solid-js';
import { H1, H2 } from '../components/ui/Typography';
import Table, { type Column } from '../components/ui/Table';
import ContentContainer from '../components/layout/ContentContainer';
import { mockScenarios } from '../mock-data/scenarios';
import type { ScenarioRow, LineCost } from '../types';

/**
 * Analyzer page - Scenario analysis with expandable cost breakdown
 * Shows complexity scenarios with line-by-line cost details
 */
export default function Analyzer() {
  const [expandedRows, setExpandedRows] = createSignal<Set<number>>(new Set());

  const toggleRow = (_item: ScenarioRow, index: number) => {
    const newSet = new Set(expandedRows());
    if (newSet.has(index)) {
      newSet.delete(index);
    } else {
      newSet.add(index);
    }
    setExpandedRows(newSet);
  };

  const scenarioColumns: Column<ScenarioRow>[] = [
    { key: 's0', header: 's0', width: 'w-32' },
    { key: 'A0', header: 'A[0]', width: 'w-40' },
    { key: 'exito', header: 'exito', width: 'w-24' },
    { key: 'k', header: 'k', width: 'w-20' },
  ];

  const lineCostColumns: Column<LineCost>[] = [
    { key: 'line_number', header: 'Línea', width: 'w-20' },
    { key: 'code', header: 'Código', render: (item) => <code class="font-mono text-xs">{item.code}</code> },
    { key: 'C_op', header: 'C_op', width: 'w-20' },
    { key: 'Freq', header: 'Freq', width: 'w-28' },
    { key: 'Total', header: 'Total', width: 'w-28' },
  ];

  const renderExpandedContent = (item: ScenarioRow) => (
    <div class="space-y-4">
      <div>
        <h3 class="text-lg font-semibold text-gray-900 mb-3">Costeo por línea</h3>
        <Table
          data={item.lineCosts}
          columns={lineCostColumns}
          class="text-sm"
        />
      </div>

      {/* Total cost */}
      <div class="bg-purple-50/50 border-2 border-purple-300 rounded-lg p-4">
        <p class="text-sm font-semibold text-gray-900">
          Costo total: <span class="text-purple-600 font-mono">{item.cost}</span>
        </p>
      </div>
    </div>
  );

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        {/* Header */}
        <H1 class="text-center">Analizador de complejidad de un algoritmo</H1>

        {/* Grid Layout: Table + Notes Panel */}
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Scenarios Table - Left Side */}
          <div class="lg:col-span-8">
            <H2 gradient class="mb-6">Escenarios</H2>
            <Table
              data={mockScenarios}
              columns={scenarioColumns}
              expandable={true}
              expandedRows={expandedRows()}
              onRowClick={toggleRow}
              expandedContent={renderExpandedContent}
            />
          </div>

          {/* Notes Panel - Right Side */}
          <div class="lg:col-span-4">
            <div class="bg-yellow-50/80 border-2 border-yellow-300 rounded-lg p-6 elevation-2 sticky top-4">
              <h3 class="text-lg font-semibold text-gray-900 mb-4">Notas</h3>
              <div class="space-y-3 text-sm text-gray-700">
                <p class="font-medium">
                  Haz clic en cada escenario para ver el desglose detallado de costos por línea.
                </p>
                <div class="pt-3 border-t border-yellow-300">
                  <p class="font-semibold mb-2">Escenarios analizados:</p>
                  <ul class="list-disc list-inside space-y-1">
                    <li>Mejor caso (x ∈ A, primera posición)</li>
                    <li>Peor caso (x ∉ A, recorrido completo)</li>
                    <li>Caso promedio (x en posición aleatoria)</li>
                  </ul>
                </div>
                <div class="pt-3 border-t border-yellow-300">
                  <p class="font-semibold mb-1">Justificación</p>
                  <p class="text-xs italic">
                    Selecciona un escenario para ver la justificación matemática de la complejidad.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </ContentContainer>
  );
}
