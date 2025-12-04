import { createSignal, Show } from 'solid-js';
import { Copy, Check } from 'lucide-solid';

interface CodeBlockProps {
  code: string;
  language: string;
}

/**
 * Code block component with syntax highlighting and copy functionality
 * Uses simple color coding for MVP (full syntax highlighting can be added later)
 */
export default function CodeBlock(props: CodeBlockProps) {
  const [copied, setCopied] = createSignal(false);

  const copyToClipboard = async () => {
    try {
      await navigator.clipboard.writeText(props.code);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy:', err);
    }
  };

  return (
    <div class="relative group">
      {/* Language badge */}
      <div class="absolute top-3 left-3 px-2 py-1 bg-black/40 rounded text-xs text-gray-400">
        {props.language}
      </div>

      {/* Copy button */}
      <button
        onClick={copyToClipboard}
        class="absolute top-3 right-3 p-2 rounded-lg bg-white/5 hover:bg-white/10
               transition-all opacity-0 group-hover:opacity-100"
        aria-label="Copy code"
      >
        <Show when={copied()} fallback={<Copy class="w-4 h-4" />}>
          <Check class="w-4 h-4 text-green-400" />
        </Show>
      </button>

      {/* Code content */}
      <pre class="bg-black/60 rounded-lg p-6 pt-12 overflow-x-auto">
        <code class="text-sm font-mono text-gray-300">
          {props.code}
        </code>
      </pre>
    </div>
  );
}
