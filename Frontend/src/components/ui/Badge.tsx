import type { JSX } from 'solid-js';
import type { BadgeVariant } from '../../types';

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
        return 'bg-green-100 text-green-700 border-2 border-green-300';
      case 'warning':
        return 'bg-yellow-100 text-yellow-700 border-2 border-yellow-300';
      case 'danger':
        return 'bg-red-100 text-red-700 border-2 border-red-300';
      case 'info':
        return 'bg-blue-100 text-blue-700 border-2 border-blue-300';
      default:
        return '';
    }
  };

  return (
    <span
      class={`inline-flex items-center px-3 py-1 rounded-full
              text-xs font-medium
              ${variantClasses()} ${props.class || ''}`}
    >
      {props.children}
    </span>
  );
}
