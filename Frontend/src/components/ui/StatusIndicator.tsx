import { Check, X, Clock } from 'lucide-solid';

export type ValidationStatus = 'valid' | 'invalid' | 'pending';

export interface StatusIndicatorProps {
  label: string;
  status: ValidationStatus;
  class?: string;
}

/**
 * Circular status indicator with icon and label
 * Shows validation state with color-coded badges
 */
export default function StatusIndicator(props: StatusIndicatorProps) {
  const getStatusClasses = () => {
    switch (props.status) {
      case 'valid':
        return 'bg-green-500/20 border-green-400 text-green-600';
      case 'invalid':
        return 'bg-red-500/20 border-red-400 text-red-600';
      case 'pending':
        return 'bg-gray-400/20 border-gray-400 text-gray-600';
      default:
        return '';
    }
  };

  const getIcon = () => {
    switch (props.status) {
      case 'valid':
        return <Check class="w-6 h-6" />;
      case 'invalid':
        return <X class="w-6 h-6" />;
      case 'pending':
        return <Clock class="w-6 h-6" />;
      default:
        return null;
    }
  };

  return (
    <div class={`flex flex-col items-center gap-2 ${props.class || ''}`}>
      {/* Circle badge */}
      <div
        class={`w-12 h-12 rounded-full border-2 flex items-center justify-center
                transition-all duration-300 ${getStatusClasses()}`}
        role="status"
        aria-label={`${props.label}: ${props.status}`}
      >
        {getIcon()}
      </div>

      {/* Label */}
      <span class="text-sm font-medium text-gray-700">{props.label}</span>
    </div>
  );
}
