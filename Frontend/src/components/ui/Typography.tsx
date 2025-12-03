import type { JSX } from 'solid-js';

interface TypographyProps {
  gradient?: boolean;
  children: JSX.Element | string;
  class?: string;
}

/**
 * Typography components with optional gradient text effect
 * Supports h1, h2, h3, and body variants
 */
export function H1(props: Omit<TypographyProps, 'variant'>) {
  return (
    <h1
      class={`text-5xl font-bold mb-4 ${props.gradient ? 'gradient-text' : 'text-white'} ${props.class || ''}`}
    >
      {props.children}
    </h1>
  );
}

export function H2(props: Omit<TypographyProps, 'variant'>) {
  return (
    <h2
      class={`text-4xl font-semibold mb-3 ${props.gradient ? 'gradient-text' : 'text-white'} ${props.class || ''}`}
    >
      {props.children}
    </h2>
  );
}

export function H3(props: Omit<TypographyProps, 'variant'>) {
  return (
    <h3
      class={`text-2xl font-medium mb-2 ${props.gradient ? 'gradient-text' : 'text-white'} ${props.class || ''}`}
    >
      {props.children}
    </h3>
  );
}

export function Body(props: Omit<TypographyProps, 'variant'>) {
  return (
    <p
      class={`text-base ${props.gradient ? 'gradient-text' : 'text-gray-300'} ${props.class || ''}`}
    >
      {props.children}
    </p>
  );
}
