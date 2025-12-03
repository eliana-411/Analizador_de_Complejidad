import { Home, Code, BarChart3, ChevronLeft, ChevronRight } from 'lucide-solid';
import { createSignal, For } from 'solid-js';
import { A, useLocation } from '@solidjs/router';

interface NavItem {
  path: string;
  label: string;
  icon: any;
}

const navItems: NavItem[] = [
  { path: '/', label: 'Home', icon: Home },
  { path: '/analyzer', label: 'Analyzer', icon: Code },
  { path: '/results/example', label: 'Results', icon: BarChart3 },
];

/**
 * Collapsible sidebar navigation with glassomorphic effect
 * Features active state highlighting and smooth transitions
 */
export default function Sidenav() {
  const [isCollapsed, setIsCollapsed] = createSignal(false);
  const location = useLocation();

  const toggleCollapse = () => setIsCollapsed(!isCollapsed());

  const isActive = (path: string) => {
    if (path === '/') {
      return location.pathname === '/';
    }
    return location.pathname.startsWith(path);
  };

  return (
    <aside
      class={`glass border-r border-white/10 h-screen sticky top-0
              transition-all duration-300 animate-slide-in-left
              ${isCollapsed() ? 'w-20' : 'w-64'}`}
    >
      <div class="flex flex-col h-full p-4">
        {/* Logo section */}
        <div class="flex items-center justify-between mb-8">
          <div class={`transition-all duration-300 ${isCollapsed() ? 'opacity-0 w-0' : 'opacity-100'}`}>
            <h1 class="text-xl font-bold gradient-text">
              Complexity
            </h1>
            <p class="text-xs text-gray-400">Analyzer</p>
          </div>
          <button
            onClick={toggleCollapse}
            class="glass-hover p-2 rounded-lg transition-all hover:bg-white/10"
            aria-label={isCollapsed() ? 'Expand sidebar' : 'Collapse sidebar'}
          >
            {isCollapsed() ? (
              <ChevronRight class="w-5 h-5" />
            ) : (
              <ChevronLeft class="w-5 h-5" />
            )}
          </button>
        </div>

        {/* Navigation links */}
        <nav class="flex-1 space-y-2">
          <For each={navItems}>
            {(item) => (
              <A
                href={item.path}
                class={`flex items-center space-x-3 px-4 py-3 rounded-lg
                        transition-all duration-200 group relative overflow-hidden
                        ${isActive(item.path)
                          ? 'bg-white/10 text-white'
                          : 'text-gray-400 hover:bg-white/5 hover:text-white'
                        }`}
              >
                {/* Active indicator */}
                {isActive(item.path) && (
                  <div class="absolute left-0 top-0 h-full w-1 gradient-primary rounded-r" />
                )}

                {/* Icon */}
                <item.icon class={`w-5 h-5 transition-transform group-hover:scale-110 ${isCollapsed() ? '' : 'ml-2'}`} />

                {/* Label */}
                <span
                  class={`font-medium transition-all duration-300
                          ${isCollapsed() ? 'opacity-0 w-0' : 'opacity-100'}`}
                >
                  {item.label}
                </span>
              </A>
            )}
          </For>
        </nav>

        {/* Footer / version */}
        <div class={`text-xs text-gray-600 transition-all duration-300
                     ${isCollapsed() ? 'opacity-0' : 'opacity-100'}`}>
          v1.0.0 MVP
        </div>
      </div>
    </aside>
  );
}
