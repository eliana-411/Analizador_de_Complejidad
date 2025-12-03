import { Show, type Component } from 'solid-js';

interface ToastProps {
  type: 'success' | 'error' | 'info';
  title: string;
  message?: string;
  details?: string[];
  suggestions?: string[];
  onClose?: () => void;
}

const Toast: Component<ToastProps> = (props) => {
  const bgColors = {
    success: 'bg-green-50 border-green-200',
    error: 'bg-red-50 border-red-200',
    info: 'bg-blue-50 border-blue-200',
  };

  const textColors = {
    success: 'text-green-800',
    error: 'text-red-800',
    info: 'text-blue-800',
  };

  const iconColors = {
    success: 'text-green-600',
    error: 'text-red-600',
    info: 'text-blue-600',
  };

  const icons = {
    success: '✓',
    error: '✕',
    info: 'ℹ',
  };

  return (
    <div
      class={`fixed top-4 right-4 max-w-md w-full shadow-xl rounded-lg border-2 ${bgColors[props.type]}
              transform transition-all duration-300 animate-slide-in-right z-50`}
    >
      <div class="p-4">
        {/* Header */}
        <div class="flex items-start justify-between">
          <div class="flex items-start gap-3">
            <span class={`text-2xl font-bold ${iconColors[props.type]}`}>
              {icons[props.type]}
            </span>
            <div class="flex-1">
              <h3 class={`font-bold text-lg ${textColors[props.type]}`}>
                {props.title}
              </h3>
              <Show when={props.message}>
                <p class={`text-sm mt-1 ${textColors[props.type]} opacity-90`}>
                  {props.message}
                </p>
              </Show>
            </div>
          </div>

          <Show when={props.onClose}>
            <button
              onClick={props.onClose}
              class={`${textColors[props.type]} hover:opacity-70 transition-opacity ml-2`}
              aria-label="Close"
            >
              <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path
                  fill-rule="evenodd"
                  d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                  clip-rule="evenodd"
                />
              </svg>
            </button>
          </Show>
        </div>

        {/* Details */}
        <Show when={props.details && props.details.length > 0}>
          <div class="mt-3 space-y-1">
            {props.details!.map((detail) => (
              <p class={`text-xs ${textColors[props.type]} opacity-80`}>
                • {detail}
              </p>
            ))}
          </div>
        </Show>

        {/* Suggestions */}
        <Show when={props.suggestions && props.suggestions.length > 0}>
          <div class="mt-3 pt-3 border-t border-current/10">
            <p class={`text-xs font-semibold ${textColors[props.type]} mb-2`}>
              💡 Sugerencias:
            </p>
            <div class="space-y-1 max-h-32 overflow-y-auto">
              {props.suggestions!.slice(0, 3).map((sug) => (
                <p class={`text-xs ${textColors[props.type]} opacity-80`}>
                  • {sug}
                </p>
              ))}
              <Show when={props.suggestions!.length > 3}>
                <p class={`text-xs ${textColors[props.type]} opacity-60 italic`}>
                  ... y {props.suggestions!.length - 3} más
                </p>
              </Show>
            </div>
          </div>
        </Show>
      </div>
    </div>
  );
};

export default Toast;
