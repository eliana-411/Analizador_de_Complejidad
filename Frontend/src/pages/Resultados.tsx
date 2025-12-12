import { createSignal, createEffect, Show } from 'solid-js';
import { useSearchParams } from '@solidjs/router';
import { H1, H2 } from '../components/ui/Typography';
import ContentContainer from '../components/layout/ContentContainer';
import { useAnalysis } from '../contexts/AnalysisContext';

/**
 * Resultados page - Algorithm analysis results dashboard
 * Shows classification, recurrence solution, and complete analysis
 */
export default function Resultados() {
  const [searchParams] = useSearchParams();
  const { analysisResult, isLoading: contextLoading } = useAnalysis();
  
  // Señales para los datos del análisis
  const [algorithmName, setAlgorithmName] = createSignal('Algoritmo');
  const [classification, setClassification] = createSignal<any>(null);
  const [recurrence, setRecurrence] = createSignal<any>(null);
  const [timeComplexity, setTimeComplexity] = createSignal<any>(null);
  const [error, setError] = createSignal<string | null>(null);

  // Procesar los datos del contexto cuando cambien
  createEffect(() => {
    const resultado = analysisResult();
    
    if (!resultado) {
      const pseudocodigo = searchParams.pseudocodigo;
      if (!pseudocodigo) {
        setError('No hay análisis disponible. Por favor, analiza un algoritmo primero.');
      }
      return;
    }

    try {
      console.log('Procesando resultado del análisis:', resultado);

      // Extraer nombre del algoritmo desde complejidades
      if (resultado.complejidades?.algorithm_name) {
        setAlgorithmName(resultado.complejidades.algorithm_name);
      }

      // Clasificación del algoritmo (si existe)
      if (resultado.clasificacion) {
        setClassification({
          type: resultado.clasificacion.categoria_principal || 'No especificado',
          category: resultado.clasificacion.top_predicciones?.[0]?.categoria || 'No especificada',
          complexity: resultado.clasificacion.confianza 
            ? `${(resultado.clasificacion.confianza * 100).toFixed(1)}% confianza`
            : 'No especificada'
        });
      }

      // Recurrencia - extraer del caso promedio
      if (resultado.complejidades?.pasos_resolucion?.caso_promedio) {
        const casoProm = resultado.complejidades.pasos_resolucion.caso_promedio;
        setRecurrence({
          formula: casoProm.ecuacion || 'No disponible',
          result: casoProm.solucion || 'No disponible',
          steps: casoProm.pasos || []
        });
      }

      // Complejidades temporales desde complejidades.complejidades (nivel correcto)
      if (resultado.complejidades?.complejidades) {
        setTimeComplexity({
          best: resultado.complejidades.complejidades.mejor_caso || 'No disponible',
          average: resultado.complejidades.complejidades.caso_promedio || 'No disponible',
          worst: resultado.complejidades.complejidades.peor_caso || 'No disponible'
        });
      }

    } catch (err: any) {
      console.error('Error al procesar análisis:', err);
      setError(err.message || 'Error al procesar el análisis');
    }
  });

  const isLoading = () => contextLoading() || (!analysisResult() && !error());

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        {/* Header */}
        <H1 class="text-center">Análisis de Complejidad - {algorithmName()}</H1>

        {/* Loading State */}
        <Show when={isLoading()}>
          <div class="text-center py-12">
            <p class="text-lg text-gray-600">Cargando resultados...</p>
          </div>
        </Show>

        {/* Error State */}
        <Show when={error()}>
          <div class="bg-red-50 border-2 border-red-300 rounded-lg p-6">
            <p class="text-red-700 font-semibold">Error:</p>
            <p class="text-red-600">{error()}</p>
          </div>
        </Show>

        {/* Main Content */}
        <Show when={!isLoading() && !error()}>
          {/* Dashboard Layout: Sidebar + Main Content */}
          <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
            {/* Sidebar - Left Side */}
            <div class="lg:col-span-4 space-y-6">
              {/* Classification Card */}
              <Show when={classification()}>
                <div class="glass rounded-lg overflow-hidden elevation-2">
                  {/* Card Header - Red/Pink Gradient */}
                  <div class="bg-gradient-to-br from-red-400 to-pink-500 p-4">
                    <h3 class="text-lg font-bold text-white">Clasificación del algoritmo</h3>
                  </div>

                  {/* Card Content */}
                  <div class="p-6 space-y-4">
                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Tipo Principal</p>
                      <p class="text-base font-medium text-gray-900">{classification()?.type}</p>
                    </div>

                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Categoría Detectada</p>
                      <p class="text-base font-medium text-gray-900">{classification()?.category}</p>
                    </div>

                    <div>
                      <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Confianza</p>
                      <p class="text-base font-medium text-gray-900">{classification()?.complexity}</p>
                    </div>
                  </div>
                </div>
              </Show>

              {/* Recurrence Card - mostrar todos los casos */}
              <Show when={analysisResult()?.complejidades?.pasos_resolucion}>
                <div class="rounded-lg overflow-hidden border border-neutral-700 bg-[#232834] shadow-lg">
                  <div class="px-6 py-4 border-b border-neutral-700">
                    <h3 class="text-lg font-bold text-green-400 tracking-wide">Ecuaciones de Recurrencia</h3>
                  </div>
                  <div class="p-6 space-y-8 max-h-[32rem] overflow-y-auto">
                    {/* Mejor caso */}
                    <Show when={analysisResult()?.complejidades?.pasos_resolucion?.mejor_caso}>
                      <div>
                        <p class="text-xs font-semibold text-green-400 uppercase tracking-wide mb-2">Mejor caso</p>
                        <div class="mb-2">
                          <span class="text-xs text-gray-400">Fórmula</span>
                          <pre class="bg-[#1a1d23] border border-green-900/40 rounded px-3 py-2 mt-1 text-green-300 font-mono text-sm whitespace-pre-wrap break-words">{analysisResult()?.complejidades?.pasos_resolucion?.mejor_caso?.ecuacion || 'No disponible'}</pre>
                        </div>
                        <div class="mb-2">
                          <span class="text-xs text-gray-400">Solución</span>
                          <pre class="bg-[#1a1d23] border border-green-900/40 rounded px-3 py-2 mt-1 text-green-200 font-mono text-base font-bold whitespace-pre-wrap break-words">{analysisResult()?.complejidades?.pasos_resolucion?.mejor_caso?.solucion || 'No disponible'}</pre>
                        </div>
                        <Show when={analysisResult()?.complejidades?.pasos_resolucion?.mejor_caso?.pasos?.length > 0}>
                          <div class="mt-2">
                            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Pasos de Resolución</p>
                            <ol class="space-y-2 text-sm text-gray-300">
                              {analysisResult()?.complejidades?.pasos_resolucion?.mejor_caso?.pasos.map((step: string, index: number) => (
                                <li class="flex">
                                  <span class="text-green-400 font-semibold mr-2 flex-shrink-0">{index + 1}.</span>
                                  <span class="break-words font-mono">{step}</span>
                                </li>
                              ))}
                            </ol>
                          </div>
                        </Show>
                      </div>
                    </Show>
                    {/* Caso promedio */}
                    <Show when={analysisResult()?.complejidades?.pasos_resolucion?.caso_promedio}>
                      <div>
                        <p class="text-xs font-semibold text-yellow-400 uppercase tracking-wide mb-2">Caso promedio</p>
                        <div class="mb-2">
                          <span class="text-xs text-gray-400">Fórmula</span>
                          <pre class="bg-[#1a1d23] border border-yellow-900/40 rounded px-3 py-2 mt-1 text-yellow-300 font-mono text-sm whitespace-pre-wrap break-words">{analysisResult()?.complejidades?.pasos_resolucion?.caso_promedio?.ecuacion || 'No disponible'}</pre>
                        </div>
                        <div class="mb-2">
                          <span class="text-xs text-gray-400">Solución</span>
                          <pre class="bg-[#1a1d23] border border-yellow-900/40 rounded px-3 py-2 mt-1 text-yellow-200 font-mono text-base font-bold whitespace-pre-wrap break-words">{analysisResult()?.complejidades?.pasos_resolucion?.caso_promedio?.solucion || 'No disponible'}</pre>
                        </div>
                        <Show when={analysisResult()?.complejidades?.pasos_resolucion?.caso_promedio?.pasos?.length > 0}>
                          <div class="mt-2">
                            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Pasos de Resolución</p>
                            <ol class="space-y-2 text-sm text-gray-300">
                              {analysisResult()?.complejidades?.pasos_resolucion?.caso_promedio?.pasos.map((step: string, index: number) => (
                                <li class="flex">
                                  <span class="text-yellow-400 font-semibold mr-2 flex-shrink-0">{index + 1}.</span>
                                  <span class="break-words font-mono">{step}</span>
                                </li>
                              ))}
                            </ol>
                          </div>
                        </Show>
                      </div>
                    </Show>
                    {/* Peor caso */}
                    <Show when={analysisResult()?.complejidades?.pasos_resolucion?.peor_caso}>
                      <div>
                        <p class="text-xs font-semibold text-red-400 uppercase tracking-wide mb-2">Peor caso</p>
                        <div class="mb-2">
                          <span class="text-xs text-gray-400">Fórmula</span>
                          <pre class="bg-[#1a1d23] border border-red-900/40 rounded px-3 py-2 mt-1 text-red-300 font-mono text-sm whitespace-pre-wrap break-words">{analysisResult()?.complejidades?.pasos_resolucion?.peor_caso?.ecuacion || 'No disponible'}</pre>
                        </div>
                        <div class="mb-2">
                          <span class="text-xs text-gray-400">Solución</span>
                          <pre class="bg-[#1a1d23] border border-red-900/40 rounded px-3 py-2 mt-1 text-red-200 font-mono text-base font-bold whitespace-pre-wrap break-words">{analysisResult()?.complejidades?.pasos_resolucion?.peor_caso?.solucion || 'No disponible'}</pre>
                        </div>
                        <Show when={analysisResult()?.complejidades?.pasos_resolucion?.peor_caso?.pasos?.length > 0}>
                          <div class="mt-2">
                            <p class="text-xs font-semibold text-gray-400 uppercase tracking-wide mb-2">Pasos de Resolución</p>
                            <ol class="space-y-2 text-sm text-gray-300">
                              {analysisResult()?.complejidades?.pasos_resolucion?.peor_caso?.pasos.map((step: string, index: number) => (
                                <li class="flex">
                                  <span class="text-red-400 font-semibold mr-2 flex-shrink-0">{index + 1}.</span>
                                  <span class="break-words font-mono">{step}</span>
                                </li>
                              ))}
                            </ol>
                          </div>
                        </Show>
                      </div>
                    </Show>
                  </div>
                </div>
              </Show>
            </div>

            {/* Main Content - Right Side */}
            <div class="lg:col-span-8">
              <div class="bg-blue-500/10 backdrop-blur-xl border-2 border-blue-300 rounded-lg p-8 elevation-2">
                <H2 class="mb-6 text-blue-900">Complejidad Temporal</H2>

                <div class="space-y-6">
                  {/* Algorithm Name */}
                  <div>
                    <p class="text-sm font-semibold text-gray-600 mb-2">Algoritmo Analizado</p>
                    <p class="text-2xl font-bold text-gray-900">{algorithmName()}</p>
                  </div>

                  {/* Time Complexity */}
                  <Show when={timeComplexity()}>
                    <div>
                      <p class="text-sm font-semibold text-gray-600 mb-3">Análisis de Complejidad</p>
                      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                        {/* Mejor caso */}
                        <div class="bg-green-50/80 border-2 border-green-300 rounded-lg p-4 text-center">
                          <p class="text-xs font-semibold text-gray-600 mb-1">Mejor caso</p>
                          <code class="text-lg font-mono font-bold text-green-600 break-words block">
                            {timeComplexity()?.best}
                          </code>
                          <Show when={analysisResult()?.complejidades?.pasos_resolucion?.mejor_caso?.metodo}>
                            <div class="mt-2 bg-green-100/60 border border-green-300 rounded p-2 text-xs text-green-900">
                              <span class="font-semibold">Método:</span> {analysisResult()?.complejidades?.pasos_resolucion?.mejor_caso?.metodo}
                            </div>
                          </Show>
                        </div>
                        {/* Caso promedio */}
                        <div class="bg-yellow-50/80 border-2 border-yellow-300 rounded-lg p-4 text-center">
                          <p class="text-xs font-semibold text-gray-600 mb-1">Caso promedio</p>
                          <code class="text-lg font-mono font-bold text-yellow-600 break-words block">
                            {timeComplexity()?.average}
                          </code>
                          <Show when={analysisResult()?.complejidades?.pasos_resolucion?.caso_promedio?.metodo}>
                            <div class="mt-2 bg-yellow-100/60 border border-yellow-300 rounded p-2 text-xs text-yellow-900">
                              <span class="font-semibold">Método:</span> {analysisResult()?.complejidades?.pasos_resolucion?.caso_promedio?.metodo}
                            </div>
                          </Show>
                        </div>
                        {/* Peor caso */}
                        <div class="bg-red-50/80 border-2 border-red-300 rounded-lg p-4 text-center">
                          <p class="text-xs font-semibold text-gray-600 mb-1">Peor caso</p>
                          <code class="text-lg font-mono font-bold text-red-600 break-words block">
                            {timeComplexity()?.worst}
                          </code>
                          <Show when={analysisResult()?.complejidades?.pasos_resolucion?.peor_caso?.metodo}>
                            <div class="mt-2 bg-red-100/60 border border-red-300 rounded p-2 text-xs text-red-900">
                              <span class="font-semibold">Método:</span> {analysisResult()?.complejidades?.pasos_resolucion?.peor_caso?.metodo}
                            </div>
                          </Show>
                        </div>
                      </div>
                    </div>
                  </Show>

                  {/* Observación sobre complejidades */}
                  <Show when={analysisResult()?.complejidades?.observacion}>
                    <div class="bg-purple-50/50 border-2 border-purple-300 rounded-lg p-6">
                      <p class="text-sm font-semibold text-gray-900 mb-2">Observación</p>
                      <p class="text-sm text-gray-700 leading-relaxed">
                        {analysisResult()?.complejidades?.observacion}
                      </p>
                    </div>
                  </Show>
                </div>
              </div>
            </div>
          </div>
        </Show>
      </div>
    </ContentContainer>
  );
}