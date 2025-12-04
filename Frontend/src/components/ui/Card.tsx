import type { JSX } from 'solid-js';
import { Show } from 'solid-js';

interface CardProps {
  title?: string;
  children: JSX.Element;
  footer?: JSX.Element;
  class?: string;
  hover?: boolean;
}

/**
 * Glass card component with optional header and footer
 * Features hover elevation effect when hover prop is true
 */
export default function Card(props: CardProps) {
  return (
    <div
      class={`glass rounded-lg overflow-hidden elevation-2
              ${props.hover ? 'hover-lift hover:elevation-3 hover:border-gray-400 cursor-pointer' : ''}
              ${props.class || ''}`}
    >
      {/* Header with title */}
      <Show when={props.title}>
        <div class="px-6 py-4 border-b-2 border-gray-300 bg-white/10">
          <h3 class="text-lg font-semibold text-gray-900">{props.title}</h3>
        </div>
      </Show>

      {/* Main content */}
      <div class="p-6">
        {props.children}
      </div>

      {/* Footer */}
      <Show when={props.footer}>
        <div class="px-6 py-4 border-t-2 border-gray-300 bg-white/10">
          {props.footer}
        </div>
      </Show>
    </div>
  );
}
