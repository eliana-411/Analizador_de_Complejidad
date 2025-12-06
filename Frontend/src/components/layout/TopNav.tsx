/**
 * Top navigation bar with project title
 * Features purple gradient background matching the project theme
 */
export default function TopNav() {
  return (
    <header class="sticky top-0 z-40 w-full backdrop-blur-md border-b border-white/40 shadow-md transition-all duration-300"
            style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);">
      <div class="px-8 py-4 flex items-center justify-center">
        <h1 class="text-3xl font-bold text-white">
          Analizador de Complejidad
        </h1>
      </div>
    </header>
  );
}
