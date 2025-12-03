import { createSignal, Show } from 'solid-js';

export interface TextareaProps {
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  rows?: number;
  error?: string;
  class?: string;
  disabled?: boolean;
}

/**
 * Large textarea component with glass styling
 * Ideal for code or pseudocode input with monospace font
 */
export default function Textarea(props: TextareaProps) {
  const [isFocused, setIsFocused] = createSignal(false);

  const hasValue = () => props.value.length > 0;
  const labelFloating = () => isFocused() || hasValue();

  return (
    <div class={`relative ${props.class || ''}`}>
      <textarea
        value={props.value}
        onInput={(e) => props.onChange(e.currentTarget.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={props.placeholder}
        rows={props.rows || 12}
        disabled={props.disabled}
        class={`w-full px-4 py-3 rounded-lg font-mono text-sm leading-relaxed
                bg-white/90 border-2 transition-all duration-200
                text-gray-900 placeholder-gray-400 resize-none
                focus:outline-none focus:bg-white backdrop-blur-xl
                disabled:opacity-50 disabled:cursor-not-allowed
                ${props.error
                  ? 'border-red-500 focus:border-red-600'
                  : isFocused()
                  ? 'border-purple-500 elevation-2'
                  : 'border-gray-300'
                }
                ${props.label ? 'pt-6' : ''}`}
      />

      {/* Floating label */}
      <Show when={props.label}>
        <label
          class={`absolute left-4 transition-all duration-200 pointer-events-none font-sans
                  ${labelFloating()
                    ? 'top-2 text-xs text-purple-600 font-medium'
                    : 'top-3.5 text-base text-gray-500'
                  }`}
        >
          {props.label}
        </label>
      </Show>

      {/* Error message */}
      <Show when={props.error}>
        <p class="mt-1 text-sm text-red-400">{props.error}</p>
      </Show>
    </div>
  );
}
