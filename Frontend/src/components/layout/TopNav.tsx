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
    <nav class="glass border-b border-white/10 px-6 py-4 animate-fade-in-down">
      <div class="flex items-center justify-between">
        {/* Breadcrumbs */}
        <div class="flex items-center space-x-2 text-sm">
          <span class="text-gray-400">Home</span>
          <span class="text-gray-600">/</span>
          <span class="text-white font-medium">Dashboard</span>
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
              class="bg-white/5 border border-white/10 rounded-lg px-4 py-2 pl-10
                     text-sm text-white placeholder-gray-500
                     focus:outline-none focus:border-white/20 focus:bg-white/10
                     transition-all duration-200 w-64"
            />
            <Search class="absolute left-3 top-1/2 -translate-y-1/2 w-4 h-4 text-gray-500" />
          </form>

          {/* User avatar */}
          <button class="glass-hover rounded-full p-2 transition-all">
            <User class="w-5 h-5 text-gray-300" />
          </button>
        </div>
      </div>
    </nav>
  );
}
