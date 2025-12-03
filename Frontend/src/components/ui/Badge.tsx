import type { JSX } from 'solid-js';
import { BadgeVariant } from '../../types';

interface BadgeProps {
  children: string | JSX.Element;
  variant: BadgeVariant;
  class?: string;
}

/**
 * Badge component for status indicators and labels
 * Color variants: success (green), warning (yellow), danger (red), info (blue)
 */
export default function Badge(props: BadgeProps) {
  const variantClasses = () => {
    switch (props.variant) {
      case 'success':
        return 'bg-green-500/20 text-green-400 border-green-500/30';
      case 'warning':
        return 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30';
      case 'danger':
        return 'bg-red-500/20 text-red-400 border-red-500/30';
      case 'info':
        return 'bg-blue-500/20 text-blue-400 border-blue-500/30';
      default:
        return '';
    }
  };

  return (
    <span
      class={`inline-flex items-center px-3 py-1 rounded-full
              text-xs font-medium border backdrop-blur-sm
              ${variantClasses()} ${props.class || ''}`}
    >
      {props.children}
    </span>
  );
}
