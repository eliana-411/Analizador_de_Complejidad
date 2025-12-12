/* @refresh reload */
import { render } from 'solid-js/web';
import './styles/globals.css';
import App from './App';
import { AnalysisProvider } from './contexts/AnalysisContext';

const root = document.getElementById('root');

if (!root) {
  throw new Error('Root element not found');
}

render(() => (
  <AnalysisProvider>
    <App />
  </AnalysisProvider>
), root);
