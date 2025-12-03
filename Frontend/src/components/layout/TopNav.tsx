import { Search, User } from 'lucide-solid';
import { createSignal } from 'solid-js';

/**
 * Top navigation bar with breadcrumbs, search, and user avatar
 * Features glass morphism effect and search functionality
 */
export default function TopNav() {
  const [searchQuery, setSearchQuery] = createSignal('');

  const handleSearch = (e: Event) => {
    e.preventDefault();
    // TODO: Implement search functionality
    console.log('Search:', searchQuery());
  };

  return (
    <nav class="bg-white/20 backdrop-blur-xl border-2 border-gray-300 rounded-2xl mx-4 mt-4 px-8 py-4 elevation-2 animate-fade-in-down">
      <div class="flex items-center justify-between">
        {/* Breadcrumbs */}
        <div class="flex items-center space-x-2 text-sm">
          <span class="text-gray-600">Inicio</span>
          <span class="text-gray-400">/</span>
          <span class="text-gray-900 font-medium">Dashboard</span>
        </div>

        {/* Right side: Search + Avatar */}
        <div class="flex items-center space-x-4">
          {/* Search bar */}
          <form onSubmit={handleSearch} class="relative">
            <input
              type="text"
              value={searchQuery()}
              onInput={(e) => setSearchQuery(e.currentTarget.value)}
              placeholder="Search..."
              class="bg-white/90 border-2 border-gray-300 rounded-lg px-4 py-2 pl-10
                     text-sm text-gray-900 placeholder-gray-500
                     focus:outline-none focus:border-purple-500 focus:bg-white focus:elevation-1
                     transition-all duration-200 w-64"
            />
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          </form>

          {/* User avatar */}
          <button class="bg-white/20 hover:bg-white/25 border border-gray-300 rounded-full p-2 transition-all elevation-1">
            <User class="w-5 h-5 text-gray-600" />
          </button>
        </div>
      </div>
    </nav>
  );
}
