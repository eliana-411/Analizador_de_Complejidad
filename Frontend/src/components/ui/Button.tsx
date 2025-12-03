import type { JSX } from 'solid-js';
import type { ButtonVariant } from '../../types';

interface ButtonProps {
  variant?: ButtonVariant;
  children: JSX.Element | string;
  onClick?: () => void;
  disabled?: boolean;
  class?: string;
  type?: 'button' | 'submit' | 'reset';
}

/**
 * Button component with 4 style variants
 * - primary: Gradient background with hover lift
 * - secondary: Glass background with gradient border
 * - ghost: Transparent with hover glass effect
 * - danger: Red gradient for destructive actions
 */
export default function Button(props: ButtonProps) {
  const variant = () => props.variant || 'primary';

  const baseClasses = 'px-6 py-3 rounded-lg font-medium transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed';

  const variantClasses = () => {
    switch (variant()) {
      case 'primary':
        return 'gradient-primary text-white elevation-2 hover:elevation-3 hover:-translate-y-0.5';
      case 'secondary':
        return 'bg-white/15 border-2 border-gray-300 hover:border-purple-500 text-gray-900 elevation-1 hover:elevation-2 hover:bg-white/20';
      case 'ghost':
        return 'bg-transparent text-gray-700 hover:bg-white/15 hover:text-gray-900 border border-transparent hover:border-gray-300';
      case 'danger':
        return 'gradient-danger text-white elevation-2 hover:elevation-3 hover:-translate-y-0.5';
      default:
        return '';
    }
  };

  return (
    <button
      type={props.type || 'button'}
      class={`${baseClasses} ${variantClasses()} ${props.class || ''}`}
      onClick={props.onClick}
      disabled={props.disabled}
    >
      {props.children}
    </button>
  );
}
