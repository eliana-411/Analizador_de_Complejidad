import { createMemo, splitProps, JSX } from 'solid-js';

interface MarkdownRendererProps {
  content: string;
  class?: string;
}

/**
 * Simple Markdown renderer for displaying analysis reports
 * Handles basic Markdown formatting without external dependencies
 */
export default function MarkdownRenderer(props: MarkdownRendererProps) {
  const [local, others] = splitProps(props, ['content', 'class']);

  const processMarkdown = createMemo(() => {
    let html = local.content;

    // Headers
    html = html.replace(/^# (.*?)$/gm, '<h1 class="text-3xl font-bold mb-4 mt-6 text-gray-900">$1</h1>');
    html = html.replace(/^## (.*?)$/gm, '<h2 class="text-2xl font-bold mb-3 mt-5 text-gray-800">$1</h2>');
    html = html.replace(/^### (.*?)$/gm, '<h3 class="text-xl font-semibold mb-2 mt-4 text-gray-700">$1</h3>');
    html = html.replace(/^#### (.*?)$/gm, '<h4 class="text-lg font-semibold mb-2 mt-3 text-gray-700">$1</h4>');

    // Bold
    html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="font-bold text-gray-900">$1</strong>');

    // Italic
    html = html.replace(/\*(.*?)\*/g, '<em class="italic">$1</em>');

    // Code blocks with Mermaid detection
    html = html.replace(/```mermaid\n([\s\S]*?)```/g, (match, code) => {
      return `<div class="mermaid-diagram my-4 p-4 bg-gray-50 border border-gray-200 rounded-lg overflow-x-auto"><pre class="text-sm">${code.trim()}</pre></div>`;
    });

    html = html.replace(/```(\w*)\n([\s\S]*?)```/g, (match, lang, code) => {
      return `<pre class="my-4 p-4 bg-gray-900 text-gray-100 rounded-lg overflow-x-auto"><code class="text-sm font-mono">${code.trim()}</code></pre>`;
    });

    // Inline code
    html = html.replace(/`([^`]+)`/g, '<code class="px-2 py-1 bg-purple-100 text-purple-800 rounded text-sm font-mono">$1</code>');

    // Tables
    html = html.replace(/\n(\|.+\|)\n(\|[-:\s|]+\|)\n((?:\|.+\|\n?)*)/g, (match, header, separator, rows) => {
      const headerCells = header.split('|').filter((cell: string) => cell.trim()).map((cell: string) =>
        `<th class="px-4 py-3 bg-purple-100 text-left text-sm font-semibold text-gray-700 border-b-2 border-purple-200">${cell.trim()}</th>`
      ).join('');

      const rowsHtml = rows.trim().split('\n').map((row: string) => {
        const cells = row.split('|').filter((cell: string) => cell.trim()).map((cell: string) =>
          `<td class="px-4 py-3 text-sm border-b border-gray-200">${cell.trim()}</td>`
        ).join('');
        return `<tr class="hover:bg-gray-50">${cells}</tr>`;
      }).join('');

      return `<div class="my-4 overflow-x-auto"><table class="min-w-full divide-y divide-gray-200 border border-gray-200 rounded-lg"><thead><tr>${headerCells}</tr></thead><tbody class="bg-white">${rowsHtml}</tbody></table></div>`;
    });

    // Horizontal rules
    html = html.replace(/^---$/gm, '<hr class="my-6 border-t-2 border-gray-300" />');

    // Lists - unordered
    html = html.replace(/^\- (.*?)$/gm, '<li class="ml-6 mb-1 text-gray-700">$1</li>');
    html = html.replace(/(<li class="ml-6.*?<\/li>\n?)+/g, '<ul class="list-disc my-3">$&</ul>');

    // Lists - ordered
    html = html.replace(/^\d+\. (.*?)$/gm, '<li class="ml-6 mb-1 text-gray-700">$1</li>');

    // Blockquotes
    html = html.replace(/^> (.*?)$/gm, '<blockquote class="border-l-4 border-purple-400 pl-4 py-2 my-3 bg-purple-50 text-gray-700 italic">$1</blockquote>');

    // Line breaks
    html = html.replace(/\n\n/g, '<br class="my-2" />');

    return html;
  });

  return (
    <div
      class={`markdown-content prose prose-sm max-w-none ${local.class || ''}`}
      innerHTML={processMarkdown()}
      {...others}
    />
  );
}
