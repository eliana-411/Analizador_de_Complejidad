import { createSignal, createEffect, Show } from 'solid-js';
import { useSearchParams, useNavigate } from '@solidjs/router';
import { H1, H2 } from '../components/ui/Typography';
import Table, { type Column } from '../components/ui/Table';
import ContentContainer from '../components/layout/ContentContainer';
import { useAnalysis } from '../contexts/AnalysisContext';
import type { BoundAnalysis } from '../types';

/**
 * Notaciones page - Cotas asintóticas
 * Muestra Ω, Θ, O con análisis matemático
 */
export default function Notaciones() {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { analysisResult, isLoading: contextLoading } = useAnalysis();
  const [expandedRows, setExpandedRows] = createSignal<Set<number>>(new Set());
  const [bounds, setBounds] = createSignal<BoundAnalysis[]>([]);
  const [error, setError] = createSignal<string | null>(null);
  const [algorithmName, setAlgorithmName] = createSignal('Algoritmo');
  const [derivacion, setDerivacion] = createSignal('');
  const [ecuacionesMat, setEcuacionesMat] = createSignal<any>(null);

  // Efecto para procesar los datos del contexto cuando cambien
  createEffect(() => {
    const resultado = analysisResult();
    
    if (!resultado) {
      // Si no hay resultado en el contexto, mostrar mensaje
      const pseudocodigo = searchParams.pseudocodigo;
      if (!pseudocodigo) {
        setError('No hay análisis disponible. Por favor, analiza un algoritmo primero.');
      }
      return;
    }

    try {
      console.log('Procesando resultado del análisis:', resultado);

      if (resultado.complejidades) {
        const comp = resultado.complejidades;

        setAlgorithmName(comp.algorithm_name || 'Algoritmo');
        setDerivacion(comp.derivacion_caso_promedio || '');
        
        // Guardar ecuaciones matemáticas si existen
        if (comp.ecuaciones_matematicas) {
          console.log('Ecuaciones matemáticas recibidas:', JSON.stringify(comp.ecuaciones_matematicas, null, 2));
          setEcuacionesMat(comp.ecuaciones_matematicas);
        }

        // Crear bounds desde las complejidades
        const boundsData: BoundAnalysis[] = [];

        // Mejor caso (Ω)
        if (comp.mejor_caso) {
          const ecuacionMejor = (typeof comp.ecuaciones_matematicas?.mejor_caso === 'string' 
            ? comp.ecuaciones_matematicas.mejor_caso 
            : undefined);
          boundsData.push({
            cota: 'Cota Inferior (Ω)',
            escenario: 'Mejor caso posible',
            ecuacion: ecuacionMejor,
            expanded: {
              analysis: 'Representa el límite inferior del tiempo de ejecución. El algoritmo nunca ejecutará más rápido que esta cota.',
              formula: `∃ c, n₀ > 0 tal que:\nT(n) ≥ c·g(n) ∀ n ≥ n₀\n\nDonde g(n) = ${comp.mejor_caso}`
            }
          });
        }

        // Caso promedio (Θ)
        if (comp.caso_promedio) {
          const ecuacionPromedio = (typeof comp.ecuaciones_matematicas?.caso_promedio === 'string' 
            ? comp.ecuaciones_matematicas.caso_promedio 
            : undefined);
          boundsData.push({
            cota: 'Cota Ajustada (Θ)',
            escenario: 'Caso promedio',
            ecuacion: ecuacionPromedio,
            expanded: {
              analysis: 'Representa el comportamiento típico del algoritmo. Acota tanto superior como inferiormente.',
              formula: `∃ c₁, c₂, n₀ > 0 tal que:\nc₁·g(n) ≤ T(n) ≤ c₂·g(n)\n∀ n ≥ n₀\n\nDonde g(n) = ${comp.caso_promedio}`
            }
          });
        }

        // Peor caso (O)
        if (comp.peor_caso) {
          const ecuacionPeor = (typeof comp.ecuaciones_matematicas?.peor_caso === 'string' 
            ? comp.ecuaciones_matematicas.peor_caso 
            : undefined);
          boundsData.push({
            cota: 'Cota Superior (O)',
            escenario: 'Peor caso posible',
            ecuacion: ecuacionPeor,
            expanded: {
              analysis: 'Representa el límite superior del tiempo de ejecución. El algoritmo nunca tomará más tiempo que esta cota.',
              formula: `∃ c, n₀ > 0 tal que:\nT(n) ≤ c·g(n) ∀ n ≥ n₀\n\nDonde g(n) = ${comp.peor_caso}`
            }
          });
        }

        setBounds(boundsData);
      } else {
        setError('No se generaron las complejidades');
      }

    } catch (err: any) {
      console.error('Error:', err);
      setError(err.message || 'Error al procesar análisis');
    }
  });

  // Determinar si está cargando
  const isLoading = () => contextLoading() || (!analysisResult() && !error());

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
    { key: 'cota', header: 'Cota', width: 'w-1/2' },
    { key: 'escenario', header: 'Escenario', width: 'w-1/2' },
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
        
        {/* Ecuación del agente matemático */}
        <Show when={item.ecuacion}>
          <div class="mt-4 pt-4 border-t border-gray-700">
            <h4 class="text-xs font-semibold text-yellow-400 mb-2 uppercase tracking-wide">Ecuación generada por agente matemático</h4>
            <code class="font-mono text-sm text-yellow-300 leading-relaxed block whitespace-pre-wrap">
              {item.ecuacion}
            </code>
          </div>
        </Show>
      </div>
    </div>
  );

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        <H1 class="text-center">Representación Matematica - {algorithmName()}</H1>

        <Show when={isLoading()}>
          <div class="text-center py-12">
            <p class="text-lg text-gray-600">Analizando complejidad...</p>
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
            {/* Bounds Table */}
            <div class="lg:col-span-7">
              <H2 gradient class="mb-6">Análisis de complejidad</H2>

              <Show when={bounds().length > 0}>
                <Table
                  data={bounds()}
                  columns={boundsColumns}
                  expandable={true}
                  expandedRows={expandedRows()}
                  onRowClick={toggleRow}
                  expandedContent={renderExpandedContent}
                />
              </Show>

              <Show when={bounds().length === 0}>
                <div class="bg-gray-50 border-2 border-gray-300 rounded-lg p-8 text-center">
                  <p class="text-gray-700">
                    No se generaron cotas asintóticas
                  </p>
                </div>
              </Show>
            </div>

            {/* Math Panel */}
            <div class="lg:col-span-5">
              <div class="bg-gray-900/95 backdrop-blur-xl border-2 border-gray-700 rounded-lg p-6 elevation-3 sticky top-4">
                <h3 class="text-lg font-semibold text-green-400 mb-4 uppercase tracking-wide">
                  Representación matemática
                </h3>

                <div class="space-y-6 font-mono text-xs text-green-300 leading-relaxed">
                  <Show when={bounds().length > 0}>
                    {/* Mostrar cada cota */}
                    <Show when={bounds().find(b => b.cota.includes('Superior'))}>
                      {(bound) => (
                        <div class="space-y-2">
                          <p class="text-green-400 font-bold text-sm">Cota Superior </p>
                          <div class="bg-black/40 rounded p-3 border border-green-900/50">
                            <p>∃ c, n₀ &gt; 0 tal que:</p>
                            <p class="mt-1">T(n) ≤ c·g(n) ∀ n ≥ n₀</p>
                            <Show when={ecuacionesMat()?.peor_caso}>
                              <p class="mt-2 text-yellow-300">Ecuación: {ecuacionesMat()?.peor_caso}</p>
                            </Show>
                          </div>
                          <p class="text-gray-400 text-xs italic">{bound().escenario}</p>
                        </div>
                      )}
                    </Show>

                    <Show when={bounds().find(b => b.cota.includes('Ajustada'))}>
                      {(bound) => (
                        <div class="space-y-2">
                          <p class="text-green-400 font-bold text-sm">Cota Ajustada</p>
                          <div class="bg-black/40 rounded p-3 border border-green-900/50">
                            <p>∃ c₁, c₂, n₀ &gt; 0 tal que:</p>
                            <p class="mt-1">c₁·g(n) ≤ T(n) ≤ c₂·g(n)</p>
                            <p class="mt-1">∀ n ≥ n₀</p>
                            <Show when={ecuacionesMat()?.caso_promedio}>
                              <p class="mt-2 text-yellow-300">Ecuación: {ecuacionesMat()?.caso_promedio}</p>
                            </Show>
                          </div>
                          <p class="text-gray-400 text-xs italic">{bound().escenario}</p>
                        </div>
                      )}
                    </Show>

                    <Show when={bounds().find(b => b.cota.includes('Inferior'))}>
                      {(bound) => (
                        <div class="space-y-2">
                          <p class="text-green-400 font-bold text-sm">Cota Inferior</p>
                          <div class="bg-black/40 rounded p-3 border border-green-900/50">
                            <p>∃ c, n₀ &gt; 0 tal que:</p>
                            <p class="mt-1">T(n) ≥ c·g(n) ∀ n ≥ n₀</p>
                            <Show when={ecuacionesMat()?.mejor_caso}>
                              <p class="mt-2 text-yellow-300">Ecuación: {ecuacionesMat()?.mejor_caso}</p>
                            </Show>
                          </div>
                          <p class="text-gray-400 text-xs italic">{bound().escenario}</p>
                        </div>
                      )}
                    </Show>
                  </Show>

                  {/* Summary */}
                  <div class="pt-4 border-t border-green-900/50">
                    <p class="text-green-400 font-semibold mb-2">Notación asintótica</p>
                    <ul class="space-y-1 text-gray-300">
                      <li>• O(g) - límite superior (≤)</li>
                      <li>• Ω(g) - límite inferior (≥)</li>
                      <li>• Θ(g) - límite ajustado (=)</li>
                    </ul>
                  </div>

                  {/* Derivación del caso promedio */}
                  <Show when={derivacion()}>
                    <div class="pt-4 border-t border-green-900/50">
                      <p class="text-green-400 font-semibold mb-2">Derivación caso promedio</p>
                      <div class="bg-black/40 rounded p-3 border border-green-900/50">
                        <p class="text-xs whitespace-pre-wrap">{derivacion()}</p>
                      </div>
                    </div>
                  </Show>
                </div>
              </div>
            </div>
          </div>

          {/* Navigation Button */}
          <Show when={!isLoading() && !error() && bounds().length > 0}>
            <div class="flex justify-end mt-8">
              <button
                onClick={() => navigate(`/resultados?pseudocodigo=${encodeURIComponent((searchParams.pseudocodigo as string) || '')}`)}
                class="flex items-center gap-2 px-6 py-3 rounded-lg font-semibold text-white transition-all duration-200 shadow-md hover:shadow-lg"
                style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);"
              >
                <span>Siguiente: Ver Reporte Final</span>
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
