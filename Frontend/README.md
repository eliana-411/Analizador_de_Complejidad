# Algorithm Complexity Analyzer - Frontend

Modern SolidJS frontend with glassomorphic design for analyzing algorithm complexity.

## Features

- **Component Showcase**: Living style guide displaying all UI components
- **Glassomorphic Design**: Dark theme with frosted glass effects and backdrop blur
- **Modern Gradients**: Vibrant color transitions (blue → purple → pink)
- **Responsive Layout**: Collapsible sidebar, adaptive design for mobile/tablet/desktop
- **Lucide Icons**: Clean, consistent iconography
- **Type-Safe**: Built with TypeScript for better developer experience

## Tech Stack

- **Framework**: [SolidJS](https://www.solidjs.com/) - Reactive, performant (7KB bundle)
- **Build Tool**: [Vite](https://vitejs.dev/) - Fast dev server and optimized builds
- **Styling**: [Tailwind CSS](https://tailwindcss.com/) - Utility-first CSS with custom glassomorphic utilities
- **Router**: [@solidjs/router](https://github.com/solidjs/solid-router) - Official SolidJS routing
- **Icons**: [Lucide Solid](https://lucide.dev/) - Beautiful, consistent icons
- **TypeScript**: Type safety and better tooling

## Project Structure

```
Frontend/
├── src/
│   ├── components/
│   │   ├── layout/          # MainLayout, Sidenav, TopNav, ContentContainer
│   │   ├── ui/              # Button, Card, Input, Badge, Typography, Divider
│   │   └── showcase/        # ComponentSection, CodeBlock (for demo page)
│   ├── pages/               # Home (showcase), Analyzer, Results
│   ├── styles/              # globals.css (Tailwind + custom CSS)
│   ├── stores/              # Theme state management
│   ├── types.ts             # Shared TypeScript types
│   └── App.tsx              # Router setup
├── public/                  # Static assets
├── index.html               # Entry point
├── vite.config.ts           # Vite configuration
├── tailwind.config.js       # Tailwind configuration
├── postcss.config.js        # PostCSS configuration
└── package.json             # Dependencies and scripts
```

## Getting Started

### Prerequisites

- Node.js 18+ (or compatible version)
- npm or pnpm

### Installation

1. Navigate to the Frontend directory:
```bash
cd Frontend
```

2. Install dependencies:
```bash
npm install
```

### Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

### Build

Create a production build:
```bash
npm run build
```

Preview the production build:
```bash
npm run preview
```

## Component Library

### Layout Components

- **MainLayout**: Root layout with gradient background, sidebar, and top nav
- **Sidenav**: Collapsible navigation sidebar with active state highlighting
- **TopNav**: Top bar with breadcrumbs, search, and user avatar
- **ContentContainer**: Glass panel wrapper for page content

### UI Components

- **Button**: 4 variants (primary, secondary, ghost, danger) with hover animations
- **Card**: Glass card with optional header/footer and hover elevation
- **Input**: Floating label input with focus gradient border
- **Badge**: Status indicators (success/warning/danger/info) for complexity labels
- **Typography**: H1, H2, H3, Body components with optional gradient text
- **Divider**: Horizontal/vertical gradient separator

### Showcase Components

- **ComponentSection**: Demo wrapper with title and description
- **CodeBlock**: Code display with syntax highlighting and copy button

## Design System

### Colors

- **Background**: `#0a0a0f` (dark navy)
- **Glass**: `rgba(15, 15, 25, 0.7)` with backdrop blur
- **Text**: `#f0f0f0` (white), `#a0a0a0` (muted)
- **Gradients**:
  - Primary: `#667eea → #764ba2 → #f093fb` (purple-pink)
  - Background: `#1a1a2e → #16213e → #0f3460` (blue gradient)

### Effects

- **Blur**: 10px (sm), 20px (md), 40px (lg)
- **Shadows**: Multi-level elevation (0-4)
- **Transitions**: 250ms (base), 400ms (slow)

### Typography

- **Font**: Inter (300, 400, 500, 600, 700, 800 weights)
- **Sizes**: H1 (48px), H2 (36px), H3 (24px), Body (16px)

## Pages

### Home (`/`)
Component showcase displaying all UI elements with interactive demos and code examples.

### Analyzer (`/analyzer`)
Placeholder for pseudocode input and analysis trigger (coming soon).

### Results (`/results/:id`)
Placeholder for displaying Omega tables and complexity analysis (coming soon).

## Backend Integration (Future)

The frontend is configured to proxy API requests to the Python backend:

```typescript
// vite.config.ts
server: {
  port: 3000,
  proxy: {
    '/api': {
      target: 'http://localhost:8000',  // Python FastAPI backend
      changeOrigin: true,
    },
  },
}
```

Example API call (future implementation):
```typescript
const response = await fetch('/api/analyze', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ pseudocode: code }),
});
```

## Scripts

- `npm run dev` - Start development server (port 3000)
- `npm run build` - Build for production
- `npm run preview` - Preview production build

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)

## Contributing

This is an academic project. Follow the coding principles in `.claude/CLAUDE.md`:
- Write clean, readable code
- Keep functions short and single-purpose
- Maintain files under 300 LOC
- Comment to explain "why", not "how"
- Stay consistent with existing patterns

## License

Academic project for Algorithm Analysis and Design course.

## Version

v1.0.0 - MVP Release

## Roadmap

### Phase 2 (Post-MVP)
- [ ] Implement Analyzer page with Monaco editor
- [ ] Connect to Python backend API
- [ ] Display real complexity analysis results
- [ ] Add dark/light mode toggle
- [ ] Implement toast notifications
- [ ] Add loading states and skeletons

### Phase 3 (Advanced Features)
- [ ] Interactive complexity visualizations (charts)
- [ ] Algorithm library with pre-loaded examples
- [ ] Export results (JSON, Markdown, PDF)
- [ ] Real-time collaboration features
- [ ] Mobile app version

---

Built with SolidJS, Tailwind CSS, and Lucide Icons | 2024
