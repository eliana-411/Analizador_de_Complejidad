import { Home, Code, BarChart3 } from 'lucide-solid';
import { For } from 'solid-js';
import { A, useLocation } from '@solidjs/router';

interface NavItem {
  path: string;
  label: string;
  icon: any;
}

const navItems: NavItem[] = [
  { path: '/', label: 'Inicio', icon: Home },
  { path: '/validador', label: 'Validador', icon: Code },
  { path: '/analizador', label: 'Analizador', icon: Code },
  { path: '/notaciones', label: 'Notaciones', icon: Code },
  { path: '/resultados', label: 'Resultados', icon: BarChart3 },
];

/**
 * Floating icon-only sidebar navigation with glassomorphic effect
 * Rounded pill design matching reference image
 */
export default function Sidenav() {
  const location = useLocation();

  const isActive = (path: string) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <aside class="fixed left-4 top-1/2 -translate-y-1/2 z-20 animate-slide-in-left">
      <div class="bg-white/10 backdrop-blur-xl rounded-full p-4 flex flex-col items-center space-y-6 border border-white/20">
        {/* Navigation links - icon only */}
        <For each={navItems}>
          {(item) => (
            <A
              href={item.path}
              class={`p-3 rounded-full transition-all duration-200 group relative
                      ${isActive(item.path)
                        ? 'bg-purple-500/30 text-purple-300'
                        : 'text-white/70 hover:bg-white/20 hover:text-white'
                      }`}
              title={item.label}
            >
              <item.icon class="w-6 h-6 transition-transform group-hover:scale-110" />
            </A>
          )}
        </For>
      </div>
    </aside>
  );
}
