import { Code } from 'lucide-solid';
import { H1, Body } from '../components/ui/Typography';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import ContentContainer from '../components/layout/ContentContainer';

/**
 * Analyzer page placeholder
 * Future: Monaco editor for pseudocode input and analysis trigger
 */
export default function Analyzer() {
  return (
    <ContentContainer>
      <div class="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <div class="glass rounded-full p-8 mb-8 animate-float">
          <Code class="w-16 h-16 text-purple-400" />
        </div>

        <H1 gradient class="mb-4">Code Analyzer</H1>
        <Body class="text-lg mb-8 max-w-2xl">
          This page will feature a powerful code editor where you can input
          pseudocode algorithms for complexity analysis. The analyzer will
          generate detailed Omega tables and complexity bounds.
        </Body>

        <Card class="max-w-xl">
          <div class="space-y-4">
            <H1 class="text-2xl">Coming Soon</H1>
            <Body>Features in development:</Body>
            <ul class="text-left space-y-2 text-gray-700">
              <li>• Monaco code editor with syntax highlighting</li>
              <li>• Real-time pseudocode validation</li>
              <li>• Algorithm type detection (iterative/recursive)</li>
              <li>• Loop and control flow analysis</li>
              <li>• One-click complexity analysis</li>
            </ul>
            <div class="pt-4">
              <Button variant="primary" onClick={() => window.location.href = '/'}>
                Back to Home
              </Button>
            </div>
          </div>
        </Card>
      </div>
    </ContentContainer>
  );
}
