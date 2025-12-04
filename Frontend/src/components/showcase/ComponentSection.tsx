import type { JSX } from 'solid-js';
import { H3, Body } from '../ui/Typography';

interface ComponentSectionProps {
  title: string;
  description?: string;
  children: JSX.Element;
}

/**
 * Wrapper for component demos in the showcase page
 * Provides title, description, and glass demo area
 */
export default function ComponentSection(props: ComponentSectionProps) {
  return (
    <section class="mb-12 animate-fade-in-up">
      {/* Header */}
      <div class="mb-6">
        <H3>{props.title}</H3>
        {props.description && (
          <Body class="mt-2">{props.description}</Body>
        )}
      </div>

      {/* Demo area with glass background */}
      <div class="glass-panel">
        <div class="space-y-4">
          {props.children}
        </div>
      </div>
    </section>
  );
}
