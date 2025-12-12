import { createSignal, onMount, Show } from 'solid-js';
import { useSearchParams, useNavigate } from '@solidjs/router';
import { H1, H2 } from '../components/ui/Typography';
import Table, { type Column } from '../components/ui/Table';
import ContentContainer from '../components/layout/ContentContainer';
// import { analyzeCode } from '../api/analyzer';
import type { LineCost } from '../types';
import { useAnalysis } from '../contexts/AnalysisContext';

interface ScenarioRow {
  id: string;
  condition: string;
  state: string;
  cost_T: string;
  probability_P: string;
  lineCosts: LineCost[];
}

/**
 * Analyzer page - Tabla Omega
 * Muestra los escenarios de complejidad con desglose línea por línea
 */
export default function Analyzer() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { analysisResult } = useAnalysis();

  const [expandedRows, setExpandedRows] = createSignal<Set<number>>(new Set());
  const [scenarios, setScenarios] = createSignal<ScenarioRow[]>([]);
  const [isLoading, setIsLoading] = createSignal(true);
  const [error, setError] = createSignal<string | null>(null);
  const [algorithmName, setAlgorithmName] = createSignal('Algoritmo');

  onMount(async () => {
    // LEER DESDE CONTEXTO GLOBAL (no llamar backend)
    const resultado = analysisResult();

    if (!resultado) {
      setError('No hay datos de análisis. Por favor, analiza el pseudocódigo primero en la página de Validación.');
      setIsLoading(false);
      return;
    }

    try {
      console.log('Leyendo resultado desde contexto:', resultado);

      if (resultado.costos_por_linea) {
        const omega = resultado.costos_por_linea;
        setAlgorithmName(omega.algorithm_name || 'Algoritmo');

        // Convertir scenarios
        const scenariosData: ScenarioRow[] = (omega.scenarios || []).map((s: any) => {
          let lineCosts: LineCost[] = [];

          // Buscar análisis línea por línea
          if (omega.metadata?.llm_analysis && s.semantic_id) {
            const caseData = omega.metadata.llm_analysis[s.semantic_id];
            if (caseData?.line_by_line_analysis) {
              lineCosts = caseData.line_by_line_analysis;
            }
          }

          // Si no hay line_by_line_analysis, usar datos de ejemplo
          if (lineCosts.length === 0) {
            console.warn(`No hay análisis línea por línea para ${s.id}, usando datos de ejemplo`);
            lineCosts = [
              { line_number: 1, code: '...', C_op: 1, Freq: '1', Total: '1' }
            ];
          }

          return {
            id: s.id || 'S_unknown',
            condition: s.condition || 'Sin condición',
            state: s.state || 'UNKNOWN',
            cost_T: s.cost_T || '?',
            probability_P: s.probability_P || '?',
            lineCosts
          };
        });

        setScenarios(scenariosData);
      } else {
        setError('No se generó la tabla Omega');
      }

    } catch (err: any) {
      console.error('Error procesando resultado:', err);
      setError(err.message || 'Error al procesar datos');
    } finally {
      setIsLoading(false);
    }
  });

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
    { key: 'id', header: 'ID', width: 'w-32' },
    { key: 'condition', header: 'Condición', width: 'w-48' },
    { key: 'state', header: 'Estado', width: 'w-32' },
    { key: 'cost_T', header: 'T(S)', width: 'w-24' },
    { key: 'probability_P', header: 'P(S)', width: 'w-24' },
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
      <Show when={item.lineCosts.length > 0}>
        <div>
          <h3 class="text-lg font-semibold text-gray-900 mb-3">Costeo por línea</h3>
          <Table
            data={item.lineCosts}
            columns={lineCostColumns}
            class="text-sm"
          />
        </div>

        <div class="bg-purple-50/50 border-2 border-purple-300 rounded-lg p-4">
          <p class="text-sm font-semibold text-gray-900">
            Costo total: <span class="text-purple-600 font-mono">{item.cost_T}</span>
          </p>
        </div>
      </Show>

      <Show when={item.lineCosts.length === 0}>
        <p class="text-sm text-gray-600 italic">
          No hay desglose de costos para este escenario
        </p>
      </Show>
    </div>
  );

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        <H1 class="text-center">Tabla Omega (Ω) - {algorithmName()}</H1>

        <Show when={isLoading()}>
          <div class="text-center py-12">
            <p class="text-lg text-gray-600">Analizando pseudocódigo...</p>
          </div>
        </Show>

        <Show when={error()}>
          <div class="bg-red-50 border-2 border-red-300 rounded-lg p-6">
            <p class="text-red-700 font-semibold">Error:</p>
            <p class="text-red-600">{error()}</p>
          </div>
        </Show>

        <Show when={!isLoading() && !error()}>
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            <div class="lg:col-span-8">
              <H2 gradient class="mb-6">Escenarios Identificados</H2>

              <Show when={scenarios().length > 0}>
                <Table
                  data={scenarios()}
                  columns={scenarioColumns}
                  expandable={true}
                  expandedRows={expandedRows()}
                  onRowClick={toggleRow}
                  expandedContent={renderExpandedContent}
                />
              </Show>

              <Show when={scenarios().length === 0}>
                <div class="bg-gray-50 border-2 border-gray-300 rounded-lg p-8 text-center">
                  <p class="text-gray-700">
                    No se encontraron escenarios. El análisis puede estar incompleto.
                  </p>
                </div>
              </Show>
            </div>

            <div class="lg:col-span-4">
              <div class="bg-yellow-50/80 border-2 border-yellow-300 rounded-lg p-6 elevation-2 sticky top-4">
                <h3 class="text-lg font-semibold text-gray-900 mb-4">Notas</h3>
                <div class="space-y-3 text-sm text-gray-700">
                  <p class="font-medium">
                    Haz clic en cada escenario para ver el desglose detallado de costos por línea.
                  </p>
                  <div class="pt-3 border-t border-yellow-300">
                    <p class="font-semibold mb-2">Total de escenarios: {scenarios().length}</p>
                    <p class="text-xs">
                      Cada escenario representa un camino de ejecución posible del algoritmo.
                    </p>
                  </div>
                  <div class="pt-3 border-t border-yellow-300">
                    <p class="font-semibold mb-1">Leyenda</p>
                    <ul class="text-xs space-y-1">
                      <li><strong>T(S):</strong> Función de costo</li>
                      <li><strong>P(S):</strong> Probabilidad</li>
                      <li><strong>C_op:</strong> Operaciones</li>
                      <li><strong>Freq:</strong> Frecuencia</li>
                    </ul>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Button */}
          <Show when={!isLoading() && !error() && scenarios().length > 0}>
            <div class="flex justify-end mt-8">
              <button
                onClick={() => navigate(`/notaciones?pseudocodigo=${encodeURIComponent((searchParams.pseudocodigo as string) || '')}`)}
                class="flex items-center gap-2 px-6 py-3 rounded-lg font-semibold text-white transition-all duration-200 shadow-md hover:shadow-lg"
                style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);"
              >
                <span>Siguiente: Ver Notaciones Asintóticas</span>
                <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
                </svg>
              </button>
            </div>
          </Show>
        </Show>
      </div>
    </ContentContainer>
  );
}
