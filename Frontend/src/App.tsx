import { Router, Route } from '@solidjs/router';
import { lazy } from 'solid-js';
import MainLayout from './components/layout/MainLayout';
import type { RouteSectionProps } from '@solidjs/router';

// Lazy load pages for better performance
const Home = lazy(() => import('./pages/Home'));
const Analyzer = lazy(() => import('./pages/Analyzer'));
const Results = lazy(() => import('./pages/Results'));

function App() {
  return (
    <Router root={(props: RouteSectionProps) => <MainLayout>{props.children}</MainLayout>}>
      <Route path="/" component={Home} />
      <Route path="/analyzer" component={Analyzer} />
      <Route path="/results/:id" component={Results} />
    </Router>
  );
}

export default App;
