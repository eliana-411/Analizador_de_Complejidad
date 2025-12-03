import { JSX, Show } from 'solid-js';

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
      class={`glass rounded-lg overflow-hidden
              ${props.hover ? 'hover-lift glass-hover cursor-pointer' : ''}
              ${props.class || ''}`}
    >
      {/* Header with title */}
      <Show when={props.title}>
        <div class="px-6 py-4 border-b border-white/10">
          <h3 class="text-lg font-semibold text-white">{props.title}</h3>
        </div>
      </Show>

      {/* Main content */}
      <div class="p-6">
        {props.children}
      </div>

      {/* Footer */}
      <Show when={props.footer}>
        <div class="px-6 py-4 border-t border-white/10 bg-white/5">
          {props.footer}
        </div>
      </Show>
    </div>
  );
}
