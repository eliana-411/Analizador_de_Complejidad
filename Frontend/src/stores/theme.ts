import { createSignal } from 'solid-js';

// Theme state management using SolidJS signals
// Currently only dark mode is supported, but can be extended for light mode

export const [isDarkMode, setIsDarkMode] = createSignal(true);

export function toggleTheme() {
  setIsDarkMode(!isDarkMode());
}
