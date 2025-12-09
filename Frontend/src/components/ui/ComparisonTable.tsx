import { createSignal, Show, For } from 'solid-js';
import type { ValidacionComplejidadesResult } from '../../api/analyzer';
import Card from './Card';
import Badge from './Badge';
import { Body } from './Typography';
import { CheckCircle, XCircle, AlertTriangle, Brain, Code } from 'lucide-solid';

interface ComparisonTableProps {
  validacion: ValidacionComplejidadesResult;
}

/**
 * Comparison Table Component
 * Displays a comparison between System and LLM complexity analysis
 */
export default function ComparisonTable(props: ComparisonTableProps) {
  const [showDetails, setShowDetails] = createSignal(false);

  const getStatusIcon = (sistema: string, llm: string) => {
    if (sistema === llm) {
      return <CheckCircle class="w-5 h-5 text-green-500" />;
    }
    // Verificar si son equivalentes (ej: O(n) vs Θ(n))
    const sistemaClean = sistema.replace(/[OΘΩ]/g, '').trim();
    const llmClean = llm.replace(/[OΘΩ]/g, '').trim();
    if (sistemaClean === llmClean) {
      return <AlertTriangle class="w-5 h-5 text-yellow-500" />;
    }
    return <XCircle class="w-5 h-5 text-red-500" />;
  };

  const getStatusText = (sistema: string, llm: string) => {
    if (sistema === llm) return 'Igual';
    const sistemaClean = sistema.replace(/[OΘΩ]/g, '').trim();
    const llmClean = llm.replace(/[OΘΩ]/g, '').trim();
    if (sistemaClean === llmClean) return 'Equivalente';
    return 'Diferente';
  };

  const getConfidenceBadge = () => {
    const confianza = props.validacion.confianza;
    if (confianza >= 0.9) return 'success';
    if (confianza >= 0.7) return 'warning';
    return 'danger';
  };

  return (
    <Card title="🔍 Validación con LLM: Comparación Sistema vs IA">
      <div class="space-y-6">
        {/* Header con estado general */}
        <div class="flex items-center justify-between p-4 rounded-lg bg-gradient-to-r from-purple-50 to-indigo-50 border border-purple-200">
          <div class="flex items-center gap-4">
            <Show
              when={props.validacion.concordancia}
              fallback={
                <div class="flex items-center gap-2">
                  <XCircle class="w-6 h-6 text-red-500" />
                  <div>
                    <Body class="font-semibold text-red-700">Divergencia Detectada</Body>
                    <Body class="text-sm text-red-600">El sistema y el LLM difieren en el análisis</Body>
                  </div>
                </div>
              }
            >
              <div class="flex items-center gap-2">
                <CheckCircle class="w-6 h-6 text-green-500" />
                <div>
                  <Body class="font-semibold text-green-700">Concordancia Verificada</Body>
                  <Body class="text-sm text-green-600">El análisis es consistente</Body>
                </div>
              </div>
            </Show>
          </div>
          <div class="text-right">
            <Body class="text-sm text-gray-600 mb-1">Nivel de Confianza</Body>
            <Badge variant={getConfidenceBadge()} class="text-lg px-4 py-1">
              {(props.validacion.confianza * 100).toFixed(0)}%
            </Badge>
          </div>
        </div>

        {/* Tabla comparativa */}
        <div class="overflow-x-auto">
          <table class="w-full border-collapse">
            <thead>
              <tr class="bg-gray-100 border-b-2 border-gray-300">
                <th class="text-left p-3 font-semibold text-gray-700">Caso de Análisis</th>
                <th class="text-left p-3 font-semibold text-gray-700">
                  <div class="flex items-center gap-2">
                    <Code class="w-4 h-4" />
                    Sistema
                  </div>
                </th>
                <th class="text-left p-3 font-semibold text-gray-700">
                  <div class="flex items-center gap-2">
                    <Brain class="w-4 h-4" />
                    LLM (IA)
                  </div>
                </th>
                <th class="text-center p-3 font-semibold text-gray-700">Estado</th>
              </tr>
            </thead>
            <tbody>
              {/* Mejor Caso */}
              <tr class="border-b border-gray-200 hover:bg-green-50 transition-colors">
                <td class="p-3">
                  <Body class="font-semibold text-gray-700">Mejor Caso (Ω)</Body>
                  <Body class="text-xs text-gray-500">Mínimas operaciones</Body>
                </td>
                <td class="p-3">
                  <Badge variant="success" class="text-base px-3 py-1">
                    {props.validacion.complejidades_sistema.mejor_caso || 'N/A'}
                  </Badge>
                </td>
                <td class="p-3">
                  <Badge variant="success" class="text-base px-3 py-1">
                    {props.validacion.complejidades_llm.mejor_caso || 'N/A'}
                  </Badge>
                </td>
                <td class="p-3 text-center">
                  <div class="flex items-center justify-center gap-2">
                    {getStatusIcon(
                      props.validacion.complejidades_sistema.mejor_caso || '',
                      props.validacion.complejidades_llm.mejor_caso || ''
                    )}
                    <Body class="text-sm">
                      {getStatusText(
                        props.validacion.complejidades_sistema.mejor_caso || '',
                        props.validacion.complejidades_llm.mejor_caso || ''
                      )}
                    </Body>
                  </div>
                </td>
              </tr>

              {/* Caso Promedio */}
              <tr class="border-b border-gray-200 hover:bg-yellow-50 transition-colors">
                <td class="p-3">
                  <Body class="font-semibold text-gray-700">Caso Promedio (Θ)</Body>
                  <Body class="text-xs text-gray-500">Comportamiento típico</Body>
                </td>
                <td class="p-3">
                  <Badge variant="warning" class="text-base px-3 py-1">
                    {props.validacion.complejidades_sistema.caso_promedio || 'N/A'}
                  </Badge>
                </td>
                <td class="p-3">
                  <Badge variant="warning" class="text-base px-3 py-1">
                    {props.validacion.complejidades_llm.caso_promedio || 'N/A'}
                  </Badge>
                </td>
                <td class="p-3 text-center">
                  <div class="flex items-center justify-center gap-2">
                    {getStatusIcon(
                      props.validacion.complejidades_sistema.caso_promedio || '',
                      props.validacion.complejidades_llm.caso_promedio || ''
                    )}
                    <Body class="text-sm">
                      {getStatusText(
                        props.validacion.complejidades_sistema.caso_promedio || '',
                        props.validacion.complejidades_llm.caso_promedio || ''
                      )}
                    </Body>
                  </div>
                </td>
              </tr>

              {/* Peor Caso */}
              <tr class="border-b border-gray-200 hover:bg-red-50 transition-colors">
                <td class="p-3">
                  <Body class="font-semibold text-gray-700">Peor Caso (O)</Body>
                  <Body class="text-xs text-gray-500">Máximas operaciones</Body>
                </td>
                <td class="p-3">
                  <Badge variant="danger" class="text-base px-3 py-1">
                    {props.validacion.complejidades_sistema.peor_caso || 'N/A'}
                  </Badge>
                </td>
                <td class="p-3">
                  <Badge variant="danger" class="text-base px-3 py-1">
                    {props.validacion.complejidades_llm.peor_caso || 'N/A'}
                  </Badge>
                </td>
                <td class="p-3 text-center">
                  <div class="flex items-center justify-center gap-2">
                    {getStatusIcon(
                      props.validacion.complejidades_sistema.peor_caso || '',
                      props.validacion.complejidades_llm.peor_caso || ''
                    )}
                    <Body class="text-sm">
                      {getStatusText(
                        props.validacion.complejidades_sistema.peor_caso || '',
                        props.validacion.complejidades_llm.peor_caso || ''
                      )}
                    </Body>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>

        {/* Recomendación */}
        <div class="p-4 rounded-lg bg-blue-50 border border-blue-200">
          <Body class="font-semibold text-blue-900 mb-2">💡 Recomendación del Sistema:</Body>
          <Body class="text-blue-800">{props.validacion.recomendacion}</Body>
        </div>

        {/* Divergencias (si existen) */}
        <Show when={props.validacion.analisis_divergencias && props.validacion.analisis_divergencias.length > 0}>
          <div class="mt-4">
            <button
              class="w-full flex items-center justify-between p-3 bg-yellow-50 border border-yellow-200 rounded-lg hover:bg-yellow-100 transition-colors"
              onClick={() => setShowDetails(!showDetails())}
            >
              <div class="flex items-center gap-2">
                <AlertTriangle class="w-5 h-5 text-yellow-600" />
                <Body class="font-semibold text-yellow-900">
                  Ver Detalles de Divergencias ({props.validacion.analisis_divergencias.length})
                </Body>
              </div>
              <span class="text-yellow-600 text-xl">{showDetails() ? '▲' : '▼'}</span>
            </button>

            <Show when={showDetails()}>
              <div class="mt-2 space-y-2">
                <For each={props.validacion.analisis_divergencias}>
                  {(divergencia) => (
                    <div class="p-3 bg-white border border-yellow-200 rounded-lg">
                      <div class="flex items-center justify-between mb-2">
                        <Body class="font-semibold capitalize">
                          {divergencia.caso.replace(/_/g, ' ')}
                        </Body>
                        <Badge variant={divergencia.severidad === 'alta' ? 'danger' : 'warning'}>
                          {divergencia.severidad}
                        </Badge>
                      </div>
                      <div class="grid grid-cols-2 gap-2 text-sm">
                        <div>
                          <Body class="text-gray-600">Sistema:</Body>
                          <Body class="font-mono">{divergencia.sistema}</Body>
                        </div>
                        <div>
                          <Body class="text-gray-600">LLM:</Body>
                          <Body class="font-mono">{divergencia.llm}</Body>
                        </div>
                      </div>
                      <Body class="text-xs text-gray-500 mt-2">
                        Tipo: {divergencia.tipo.replace(/_/g, ' ')}
                      </Body>
                    </div>
                  )}
                </For>
              </div>
            </Show>
          </div>
        </Show>

        {/* Explicación */}
        <div class="p-4 bg-gray-50 rounded-lg border border-gray-200">
          <Body class="text-sm text-gray-600">
            <strong>¿Qué significa esto?</strong> El sistema analiza el pseudocódigo usando métodos formales 
            de conteo de operaciones, mientras que el LLM (IA) realiza un análisis independiente basado en 
            su entrenamiento. La concordancia entre ambos métodos aumenta la confianza en el resultado.
          </Body>
        </div>
      </div>
    </Card>
  );
}
