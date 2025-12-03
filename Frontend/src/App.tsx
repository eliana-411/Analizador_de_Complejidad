import { Router, Route } from '@solidjs/router'
import { lazy } from 'solid-js'
import MainLayout from './components/layout/MainLayout'

// Lazy load pages for better performance
const Home = lazy(() => import('./pages/Home'))
const Validador = lazy(() => import('./pages/Validador'))
const Analyzer = lazy(() => import('./pages/Analyzer'))
const Notaciones = lazy(() => import('./pages/Notaciones'))
const Results = lazy(() => import('./pages/Results'))

function App() {
  return (
    <Router>
      <Route path="/" component={MainLayout}>
        <Route path="/" component={Home} />
        <Route path="/validador" component={Validador} />
        <Route path="/analizador" component={Analyzer} />
        <Route path="/notaciones" component={Notaciones} />
        <Route path="/resultados" component={Results} />
        <Route path="/resultados/:id" component={Results} />
      </Route>
    </Router>
  )
}

export default App
