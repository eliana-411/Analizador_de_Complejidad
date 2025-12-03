import { createSignal, Show } from 'solid-js';
import { InputType } from '../../types';

interface InputProps {
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  type?: InputType;
  error?: string;
  class?: string;
}

/**
 * Glass input field with floating label animation
 * Features gradient border on focus and error states
 */
export default function Input(props: InputProps) {
  const [isFocused, setIsFocused] = createSignal(false);

  const hasValue = () => props.value.length > 0;
  const labelFloating = () => isFocused() || hasValue();

  return (
    <div class={`relative ${props.class || ''}`}>
      <input
        type={props.type || 'text'}
        value={props.value}
        onInput={(e) => props.onChange(e.currentTarget.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={props.placeholder}
        class={`w-full px-4 py-3 rounded-lg
                bg-white/90 border-2 transition-all duration-200
                text-gray-900 placeholder-transparent
                focus:outline-none focus:bg-white elevation-1
                ${props.error
                  ? 'border-red-500 focus:border-red-600'
                  : isFocused()
                  ? 'border-purple-500 elevation-2'
                  : 'border-gray-300'
                }
                ${props.label ? 'pt-6 pb-2' : ''}`}
      />

      {/* Floating label */}
      <Show when={props.label}>
        <label
          class={`absolute left-4 transition-all duration-200 pointer-events-none
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
