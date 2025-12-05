import { Show, For, onMount, onCleanup } from 'solid-js';
import { X, AlertCircle } from 'lucide-solid';

interface ErrorModalProps {
  isOpen: boolean;
  onClose: () => void;
  layerName: string;
  errors: string[];
}

const LAYER_LABELS: Record<string, string> = {
  '1_LEXICA': 'LÉXICA',
  '2_DECLARACIONES': 'DECLARACIONES',
  '3_ESTRUCTURA': 'ESTRUCTURA',
  '4_EXPRESIONES': 'EXPRESIONES',
  '5_SENTENCIAS': 'SENTENCIAS',
  '6_SUBRUTINAS': 'SUBRUTINAS',
  '7_SEMANTICA': 'SEMÁNTICA',
};

export default function ErrorModal(props: ErrorModalProps) {
  const getLayerLabel = () => {
    return LAYER_LABELS[props.layerName] || props.layerName;
  };

  // Close modal on ESC key
  onMount(() => {
    const handleEscape = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && props.isOpen) {
        props.onClose();
      }
    };

    document.addEventListener('keydown', handleEscape);

    onCleanup(() => {
      document.removeEventListener('keydown', handleEscape);
    });
  });

  return (
    <Show when={props.isOpen}>
      {/* Backdrop */}
      <div
        class="fixed inset-0 bg-black/50 z-50 flex items-start justify-center pt-20 px-4 animate-fade-in"
        onClick={props.onClose}
      >
        {/* Modal Panel */}
        <div
          class="glass-panel w-full max-w-2xl bg-white/95 backdrop-blur-xl rounded-lg shadow-2xl animate-fade-in-up"
          onClick={(e) => e.stopPropagation()}
        >
          {/* Header */}
          <div class="flex items-center justify-between p-6 border-b border-gray-200">
            <div class="flex items-center gap-3">
              <div class="p-2 bg-red-100 rounded-lg">
                <AlertCircle class="w-6 h-6 text-red-600" />
              </div>
              <div>
                <h2 class="text-xl font-bold text-gray-900">
                  Errores de {getLayerLabel()}
                </h2>
                <p class="text-sm text-gray-600">
                  Se encontraron {props.errors.length} error{props.errors.length !== 1 ? 'es' : ''}
                </p>
              </div>
            </div>
            <button
              onClick={props.onClose}
              class="p-2 rounded-lg hover:bg-gray-100 transition-colors"
              title="Cerrar"
            >
              <X class="w-5 h-5 text-gray-500" />
            </button>
          </div>

          {/* Error List */}
          <div class="p-6 max-h-96 overflow-y-auto">
            <div class="space-y-3">
              <For each={props.errors}>
                {(error, index) => (
                  <div class="flex items-start gap-3 p-4 bg-red-50 border border-red-200 rounded-lg hover:border-red-400 transition-colors">
                    <div class="flex-shrink-0 w-6 h-6 bg-red-200 rounded-full flex items-center justify-center">
                      <span class="text-xs font-bold text-red-700">{index() + 1}</span>
                    </div>
                    <div class="flex-1">
                      <p class="text-sm text-gray-800 leading-relaxed">{error}</p>
                    </div>
                  </div>
                )}
              </For>
            </div>
          </div>

          {/* Footer */}
          <div class="flex justify-end gap-3 p-6 border-t border-gray-200 bg-gray-50/50">
            <button
              onClick={props.onClose}
              class="px-6 py-2 bg-gray-200 hover:bg-gray-300 text-gray-800 font-medium rounded-lg transition-colors"
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </Show>
  );
}
