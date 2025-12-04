import { For } from 'solid-js';

export interface ToggleOption {
  value: string;
  label: string;
}

export interface ToggleButtonGroupProps {
  options: ToggleOption[];
  value: string;
  onChange: (value: string) => void;
  color?: 'blue' | 'orange' | 'purple';
  class?: string;
}

/**
 * Segmented control for toggling between options
 * Smooth transition with color variants
 */
export default function ToggleButtonGroup(props: ToggleButtonGroupProps) {
  const getActiveClasses = () => {
    switch (props.color || 'blue') {
      case 'blue':
        return 'bg-blue-500 text-white';
      case 'orange':
        return 'bg-orange-500 text-white';
      case 'purple':
        return 'bg-purple-500 text-white';
      default:
        return 'bg-blue-500 text-white';
    }
  };

  return (
    <div
      class={`glass rounded-lg p-1 flex gap-1 ${props.class || ''}`}
      role="group"
      aria-label="Toggle options"
    >
      <For each={props.options}>
        {(option) => (
          <button
            onClick={() => props.onChange(option.value)}
            class={`px-4 py-2 rounded-md text-sm font-medium transition-all duration-200
                    ${props.value === option.value
                      ? `${getActiveClasses()} elevation-1`
                      : 'text-gray-600 hover:bg-white/10'
                    }`}
            role="radio"
            aria-checked={props.value === option.value}
          >
            {option.label}
          </button>
        )}
      </For>
    </div>
  );
}
