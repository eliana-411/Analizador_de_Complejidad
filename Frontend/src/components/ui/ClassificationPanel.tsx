import { Show, For } from 'solid-js';
import Card from './Card';
import Badge from './Badge';
import { H3, Body } from './Typography';
import { Brain, TrendingUp } from 'lucide-solid';
import type { ClasificacionResult } from '../../api/validator';

interface ClassificationPanelProps {
  classification: ClasificacionResult | null | undefined;
  isLoading?: boolean;
  class?: string;
}

export default function ClassificationPanel(props: ClassificationPanelProps) {
  const formatPercentage = (value: number) => {
    return `${(value * 100).toFixed(1)}%`;
  };

  const getConfidenceColor = (confidence: number): 'success' | 'warning' | 'danger' => {
    if (confidence >= 0.7) return 'success';
    if (confidence >= 0.4) return 'warning';
    return 'danger';
  };

  const getConfidenceBarColor = (confidence: number): string => {
    if (confidence >= 0.7) return 'bg-gradient-to-r from-green-500 to-emerald-500';
    if (confidence >= 0.4) return 'bg-gradient-to-r from-yellow-500 to-orange-500';
    return 'bg-gradient-to-r from-red-500 to-pink-500';
  };

  return (
    <div class={`${props.class || ''}`}>
      <Card title="Clasificación ML" class="h-full">
        <Show
          when={!props.isLoading && props.classification}
          fallback={
            <div class="flex flex-col items-center justify-center py-12 text-gray-400">
              <Brain class="w-16 h-16 mb-4 opacity-30" />
              <Body class="text-center">
                {props.isLoading
                  ? 'Analizando algoritmo...'
                  : 'Analiza un pseudocódigo para ver la clasificación'}
              </Body>
            </div>
          }
        >
          {(classification) => (
            <div class="space-y-6">
              {/* Main Category */}
              <div class="p-4 rounded-lg bg-gradient-to-br from-purple-50 to-blue-50 border-2 border-purple-200">
                <div class="flex items-start justify-between mb-2">
                  <H3 class="text-lg">Categoría Principal</H3>
                  <Badge variant={getConfidenceColor(classification.confianza || 0)}>
                    {formatPercentage(classification.confianza || 0)}
                  </Badge>
                </div>
                <p class="text-2xl font-bold text-purple-700 capitalize">
                  {classification.categoria_principal?.replace(/_/g, ' ') || 'Desconocido'}
                </p>
              </div>

              {/* Confidence Bar */}
              <div>
                <div class="flex justify-between text-sm mb-2">
                  <span class="text-gray-600 font-medium">Nivel de confianza</span>
                  <span class="text-gray-900 font-bold">
                    {formatPercentage(classification.confianza || 0)}
                  </span>
                </div>
                <div class="w-full h-3 bg-gray-200 rounded-full overflow-hidden">
                  <div
                    class={`h-full ${getConfidenceBarColor(
                      classification.confianza || 0
                    )} transition-all duration-500 ease-out`}
                    style={{ width: formatPercentage(classification.confianza || 0) }}
                  />
                </div>
              </div>

              {/* Top Predictions */}
              <div>
                <div class="flex items-center gap-2 mb-3">
                  <TrendingUp class="w-5 h-5 text-gray-600" />
                  <h4 class="text-sm font-semibold text-gray-700">Top 3 Predicciones</h4>
                </div>
                <div class="space-y-2">
                  <For each={classification.top_predicciones || []}>
                    {(pred, index) => (
                      <div class="glass p-3 rounded-lg border border-gray-200 hover:border-purple-300 transition-colors">
                        <div class="flex items-center justify-between mb-1">
                          <span class="text-sm font-medium text-gray-700 capitalize">
                            #{index() + 1} {pred.categoria?.replace(/_/g, ' ') || 'Desconocido'}
                          </span>
                          <Badge variant="info">{formatPercentage(pred.probabilidad || 0)}</Badge>
                        </div>
                        <div class="w-full h-1.5 bg-gray-200 rounded-full overflow-hidden">
                          <div
                            class="h-full bg-blue-400 transition-all duration-300"
                            style={{ width: formatPercentage(pred.probabilidad || 0) }}
                          />
                        </div>
                      </div>
                    )}
                  </For>
                </div>
              </div>
            </div>
          )}
        </Show>
      </Card>
    </div>
  );
}
