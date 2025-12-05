import { createSignal, Show } from 'solid-js';
import { Paperclip, Loader2 } from 'lucide-solid';

export interface TextareaProps {
  label?: string;
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
  rows?: number;
  error?: string;
  class?: string;
  disabled?: boolean;
  onFileUpload?: (content: string, filename: string) => void;
}

/**
 * Large textarea component with glass styling
 * Ideal for code or pseudocode input with monospace font
 */
export default function Textarea(props: TextareaProps) {
  const [isFocused, setIsFocused] = createSignal(false);
  const [isUploadingFile, setIsUploadingFile] = createSignal(false);
  const [uploadError, setUploadError] = createSignal<string | null>(null);
  let fileInputRef: HTMLInputElement | undefined;

  const hasValue = () => props.value.length > 0;
  const labelFloating = () => isFocused() || hasValue();

  const handleFileSelect = async (event: Event) => {
    const input = event.target as HTMLInputElement;
    const file = input.files?.[0];

    if (!file) return;

    // Validate file type
    if (!file.name.endsWith('.txt')) {
      setUploadError('Solo se permiten archivos .txt');
      setTimeout(() => setUploadError(null), 3000);
      return;
    }

    setIsUploadingFile(true);
    setUploadError(null);

    try {
      const reader = new FileReader();

      reader.onload = (e) => {
        const content = e.target?.result as string;
        if (props.onFileUpload) {
          props.onFileUpload(content, file.name);
        }
        setIsUploadingFile(false);
        // Reset input so same file can be uploaded again
        if (fileInputRef) fileInputRef.value = '';
      };

      reader.onerror = () => {
        setUploadError('Error al leer el archivo');
        setIsUploadingFile(false);
        setTimeout(() => setUploadError(null), 3000);
      };

      reader.readAsText(file);
    } catch (err) {
      setUploadError('Error al procesar el archivo');
      setIsUploadingFile(false);
      setTimeout(() => setUploadError(null), 3000);
    }
  };

  const triggerFileInput = () => {
    fileInputRef?.click();
  };

  return (
    <div class={`relative ${props.class || ''}`}>
      <textarea
        value={props.value}
        onInput={(e) => props.onChange(e.currentTarget.value)}
        onFocus={() => setIsFocused(true)}
        onBlur={() => setIsFocused(false)}
        placeholder={props.placeholder}
        rows={props.rows || 12}
        disabled={props.disabled}
        class={`w-full px-4 py-3 rounded-lg font-mono text-sm leading-relaxed
                bg-white/90 border-2 transition-all duration-200
                text-gray-900 placeholder-gray-400 resize-none
                focus:outline-none focus:bg-white backdrop-blur-xl
                disabled:opacity-50 disabled:cursor-not-allowed
                ${props.error
                  ? 'border-red-500 focus:border-red-600'
                  : isFocused()
                  ? 'border-purple-500 elevation-2'
                  : 'border-gray-300'
                }
                ${props.label ? 'pt-6' : ''}`}
      />

      {/* Floating label */}
      <Show when={props.label}>
        <label
          class={`absolute left-4 transition-all duration-200 pointer-events-none font-sans
                  ${labelFloating()
                    ? 'top-2 text-xs text-purple-600 font-medium'
                    : 'top-3.5 text-base text-gray-500'
                  }`}
        >
          {props.label}
        </label>
      </Show>

      {/* Error message */}
      <Show when={props.error}>
        <p class="mt-1 text-sm text-red-400">{props.error}</p>
      </Show>

      {/* File Upload Button - Floating in top-right corner */}
      <Show when={props.onFileUpload}>
        <input
          ref={fileInputRef}
          type="file"
          accept=".txt"
          onChange={handleFileSelect}
          class="hidden"
          aria-label="Cargar archivo de pseudocódigo"
        />

        <button
          type="button"
          onClick={triggerFileInput}
          disabled={isUploadingFile() || props.disabled}
          class="absolute top-3 right-3 p-2 rounded-lg glass
                 bg-white/80 hover:bg-white/95 border border-gray-300
                 transition-all duration-200 hover:elevation-2
                 disabled:opacity-50 disabled:cursor-not-allowed
                 group"
          title="Cargar archivo .txt"
        >
          <Show
            when={!isUploadingFile()}
            fallback={<Loader2 class="w-5 h-5 text-purple-600 animate-spin" />}
          >
            <Paperclip class="w-5 h-5 text-gray-600 group-hover:text-purple-600 transition-colors" />
          </Show>
        </button>

        {/* Upload error message */}
        <Show when={uploadError()}>
          <div class="absolute top-14 right-3 px-3 py-2 bg-red-100 border border-red-400 rounded-lg text-sm text-red-700 animate-fade-in">
            {uploadError()}
          </div>
        </Show>
      </Show>
    </div>
  );
}
