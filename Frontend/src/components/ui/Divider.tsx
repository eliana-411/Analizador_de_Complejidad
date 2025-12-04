interface DividerProps {
  vertical?: boolean;
  class?: string;
}

/**
 * Gradient divider for visual separation
 * Supports horizontal (default) and vertical orientations
 */
export default function Divider(props: DividerProps) {
  if (props.vertical) {
    return (
      <div class={`w-px h-full bg-gradient-to-b from-transparent via-purple-400/70 to-transparent ${props.class || ''}`} />
    );
  }

  return (
    <div class={`h-px w-full my-4 bg-gradient-to-r from-transparent via-purple-400/70 to-transparent ${props.class || ''}`} />
  );
}
