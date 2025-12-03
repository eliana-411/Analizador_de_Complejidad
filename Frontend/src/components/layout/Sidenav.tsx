import { Home, CheckCircle, Activity, Pi, BarChart3 } from 'lucide-solid';
import { For } from 'solid-js';
import { A, useLocation } from '@solidjs/router';

interface NavItem {
  path: string;
  label: string;
  icon: any;
}

const navItems: NavItem[] = [
  { path: '/', label: 'Inicio', icon: Home },
  { path: '/validador', label: 'Validador', icon: CheckCircle },
  { path: '/analizador', label: 'Analizador', icon: Activity },
  { path: '/notaciones', label: 'Notaciones', icon: Pi },
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
      <div class="bg-white/20 backdrop-blur-xl rounded-full p-4 flex flex-col items-center space-y-6 border-2 border-gray-300 elevation-2">
        {/* Navigation links - icon only */}
        <For each={navItems}>
          {(item) => (
            <A
              href={item.path}
              class={`p-3 rounded-full transition-all duration-200 group relative
                      ${isActive(item.path)
                        ? 'bg-purple-500/20 text-purple-600 border-2 border-purple-300'
                        : 'text-gray-600 hover:bg-white/25 hover:text-gray-900 border-2 border-transparent hover:border-gray-300'
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
