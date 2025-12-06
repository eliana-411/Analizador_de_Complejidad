import { Show } from 'solid-js';
import type { CorreccionResult } from '../../api/analyzer';

interface CorrectionFeedbackProps {
  correccion: CorreccionResult | null | undefined;
  validacionInicial?: Record<string, any> | null;
}

/**
 * CorrectionFeedback component - versión simplificada
 * Muestra feedback de corrección automática
 */
export default function CorrectionFeedback(props: CorrectionFeedbackProps) {
  const hasCorrection = () => props.correccion?.corregido === true;
  const totalErrores = () => props.validacionInicial?.resumen?.errores_totales || 0;

  return (
    <Show when={hasCorrection()}>
      <div class="mt-4 animate-fade-in-up">
        {/* Panel simple de corrección */}
        <div class="bg-green-50 border-2 border-green-300 rounded-lg p-4 shadow-md">
          {/* Título */}
          <h3 class="text-base font-bold text-green-900 mb-2">
            ✓ Código corregido automáticamente
          </h3>

          {/* Mensaje de errores corregidos */}
          <Show when={totalErrores() > 0}>
            <p class="text-sm text-green-700 mb-3">
              Se encontraron y corrigieron {totalErrores()} error{totalErrores() !== 1 ? 'es' : ''}
            </p>
          </Show>

          {/* Explicación de cambios */}
          <Show when={props.correccion?.explicacion}>
            <div class="p-3 bg-white rounded border border-green-200">
              <p class="text-xs font-semibold text-gray-700 mb-1">
                Qué se corrigió:
              </p>
              <div class="text-xs text-gray-600 whitespace-pre-line">
                {props.correccion!.explicacion}
              </div>
            </div>
          </Show>

          {/* Ejemplos usados (si existen) */}
          <Show when={props.correccion?.ejemplos_usados && props.correccion.ejemplos_usados.length > 0}>
            <div class="mt-3">
              <p class="text-xs text-green-800 mb-1">
                Ejemplos usados: {props.correccion!.ejemplos_usados.join(', ')}
              </p>
            </div>
          </Show>
        </div>
      </div>
    </Show>
  );
}
