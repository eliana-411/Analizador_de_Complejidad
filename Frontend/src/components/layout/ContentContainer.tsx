import type { JSX } from 'solid-js';

interface ContentContainerProps {
  children: JSX.Element;
}

/**
 * Glass panel container for page content
 * Provides consistent padding, border, and glass effect
 */
export default function ContentContainer(props: ContentContainerProps) {
  return (
    <div class="glass-panel animate-fade-in-up">
      {props.children}
    </div>
  );
}
