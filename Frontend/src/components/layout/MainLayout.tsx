import type { JSX } from 'solid-js';
import Sidenav from './Sidenav';
import TopNav from './TopNav';
import videoBackground from '../../assets/cobija.webm';

interface MainLayoutProps {
  children: JSX.Element;
}

/**
 * Main layout component with video background and glassomorphic UI
 * Features animated video background with overlay for better glass effect visibility
 */
export default function MainLayout(props: MainLayoutProps) {
  return (
    <div class="min-h-screen relative overflow-hidden">
      {/* Video background */}
      <video
        autoplay
        loop
        muted
        playsinline
        class="fixed inset-0 w-full h-full object-cover z-0"
      >
        <source src={videoBackground} type="video/webm" />
      </video>

      {/* Dark overlay for better glass effect visibility */}
      <div class="fixed inset-0 bg-black/40 z-0" />

      {/* Main content with glass effect */}
      <div class="relative z-10 flex min-h-screen">
        {/* Sidebar */}
        <Sidenav />

        {/* Main content area */}
        <div class="flex-1 flex flex-col min-h-screen">
          {/* Top navigation */}
          <TopNav />

          {/* Page content */}
          <main class="flex-1 p-6">
            {props.children}
          </main>
        </div>
      </div>
    </div>
  );
}
