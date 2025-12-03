import { H1, H2 } from '../components/ui/Typography';
import ContentContainer from '../components/layout/ContentContainer';
import { mockClassification, mockRecurrence, mockSolution } from '../mock-data/solutions';

/**
 * Resultados page - Algorithm analysis results dashboard
 * Shows classification, recurrence solution, and complete analysis
 */
export default function Resultados() {
  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        {/* Header */}
        <H1 class="text-center">Analizador de complejidad de un algoritmo</H1>

        {/* Dashboard Layout: Sidebar + Main Content */}
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Sidebar - Left Side */}
          <div class="lg:col-span-4 space-y-6">
            {/* Classification Card */}
            <div class="glass rounded-lg overflow-hidden elevation-2">
              {/* Card Header - Red/Pink Gradient */}
              <div class="bg-gradient-to-br from-red-400 to-pink-500 p-4">
                <h3 class="text-lg font-bold text-white">Clasificación del algoritmo</h3>
              </div>

              {/* Card Content */}
              <div class="p-6 space-y-4">
                <div>
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Tipo</p>
                  <p class="text-base font-medium text-gray-900">{mockClassification.type}</p>
                </div>

                <div>
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Categoría</p>
                  <p class="text-base font-medium text-gray-900">{mockClassification.category}</p>
                </div>

                <div>
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-1">Complejidad</p>
                  <p class="text-base font-medium text-gray-900">{mockClassification.complexity}</p>
                </div>
              </div>
            </div>

            {/* Recurrence Card */}
            <div class="glass rounded-lg overflow-hidden elevation-2">
              {/* Card Header - Red/Pink Gradient */}
              <div class="bg-gradient-to-br from-red-400 to-pink-500 p-4">
                <h3 class="text-lg font-bold text-white">Resolver T(n) Recurrente</h3>
              </div>

              {/* Card Content */}
              <div class="p-6 space-y-4">
                <div>
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Fórmula</p>
                  <code class="text-sm font-mono text-purple-600 bg-purple-50/50 px-2 py-1 rounded">
                    {mockRecurrence.formula}
                  </code>
                </div>

                <div>
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Resultado</p>
                  <code class="text-base font-mono font-bold text-green-600 bg-green-50/50 px-2 py-1 rounded">
                    {mockRecurrence.result}
                  </code>
                </div>

                <div>
                  <p class="text-xs font-semibold text-gray-500 uppercase tracking-wide mb-2">Pasos</p>
                  <ol class="space-y-2 text-sm text-gray-700">
                    {mockRecurrence.steps.map((step, index) => (
                      <li class="flex">
                        <span class="text-purple-500 font-semibold mr-2">{index + 1}.</span>
                        <span>{step}</span>
                      </li>
                    ))}
                  </ol>
                </div>
              </div>
            </div>
          </div>

          {/* Main Content - Right Side */}
          <div class="lg:col-span-8">
            <div class="bg-blue-500/10 backdrop-blur-xl border-2 border-blue-300 rounded-lg p-8 elevation-2">
              <H2 class="mb-6 text-blue-900">Solución</H2>

              <div class="space-y-6">
                {/* Algorithm Name */}
                <div>
                  <p class="text-sm font-semibold text-gray-600 mb-2">Algoritmo</p>
                  <p class="text-2xl font-bold text-gray-900">{mockSolution.algorithm}</p>
                </div>

                {/* Time Complexity */}
                <div>
                  <p class="text-sm font-semibold text-gray-600 mb-3">Complejidad Temporal</p>
                  <div class="grid grid-cols-3 gap-4">
                    <div class="bg-green-50/80 border-2 border-green-300 rounded-lg p-4 text-center">
                      <p class="text-xs font-semibold text-gray-600 mb-1">Mejor caso</p>
                      <code class="text-lg font-mono font-bold text-green-600">{mockSolution.timeComplexity.best}</code>
                    </div>
                    <div class="bg-yellow-50/80 border-2 border-yellow-300 rounded-lg p-4 text-center">
                      <p class="text-xs font-semibold text-gray-600 mb-1">Caso promedio</p>
                      <code class="text-lg font-mono font-bold text-yellow-600">{mockSolution.timeComplexity.average}</code>
                    </div>
                    <div class="bg-red-50/80 border-2 border-red-300 rounded-lg p-4 text-center">
                      <p class="text-xs font-semibold text-gray-600 mb-1">Peor caso</p>
                      <code class="text-lg font-mono font-bold text-red-600">{mockSolution.timeComplexity.worst}</code>
                    </div>
                  </div>
                </div>

                {/* Space Complexity */}
                <div>
                  <p class="text-sm font-semibold text-gray-600 mb-2">Complejidad Espacial</p>
                  <code class="text-xl font-mono font-bold text-blue-600 bg-blue-50/50 px-3 py-2 rounded inline-block">
                    {mockSolution.spaceComplexity}
                  </code>
                </div>

                {/* Characteristics */}
                <div>
                  <p class="text-sm font-semibold text-gray-600 mb-3">Características</p>
                  <ul class="space-y-2">
                    {mockSolution.characteristics.map((char) => (
                      <li class="flex items-start">
                        <span class="text-blue-500 mr-2 mt-0.5">•</span>
                        <span class="text-sm text-gray-700 leading-relaxed">{char}</span>
                      </li>
                    ))}
                  </ul>
                </div>

                {/* Optimizations */}
                <div class="bg-purple-50/50 border-2 border-purple-300 rounded-lg p-6">
                  <p class="text-sm font-semibold text-gray-900 mb-3">Optimizaciones posibles</p>
                  <ul class="space-y-2">
                    {mockSolution.optimizations.map((opt) => (
                      <li class="flex items-start">
                        <span class="text-purple-500 mr-2 mt-0.5">✓</span>
                        <span class="text-sm text-gray-700 leading-relaxed">{opt}</span>
                      </li>
                    ))}
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
