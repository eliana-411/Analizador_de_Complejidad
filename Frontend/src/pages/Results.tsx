import { BarChart3 } from 'lucide-solid';
import { H1, Body } from '../components/ui/Typography';
import Card from '../components/ui/Card';
import Button from '../components/ui/Button';
import Badge from '../components/ui/Badge';
import ContentContainer from '../components/layout/ContentContainer';

/**
 * Results page placeholder
 * Future: Display Omega tables, complexity analysis, and visualizations
 */
export default function Results() {
  return (
    <ContentContainer>
      <div class="flex flex-col items-center justify-center min-h-[60vh] text-center">
        <div class="glass rounded-full p-8 mb-8 animate-float">
          <BarChart3 class="w-16 h-16 text-pink-400" />
        </div>

        <H1 gradient class="mb-4">Analysis Results</H1>
        <Body class="text-lg mb-8 max-w-2xl">
          This page will display comprehensive complexity analysis results,
          including Omega tables, scenario breakdowns, and interactive visualizations
          of algorithm performance.
        </Body>

        <Card class="max-w-xl">
          <div class="space-y-4">
            <H1 class="text-2xl">Coming Soon</H1>
            <Body>Results features in development:</Body>
            <ul class="text-left space-y-2 text-gray-700">
              <li>• Complete Omega (Ω) table display</li>
              <li>• Line-by-line cost breakdown</li>
              <li>• Scenario taxonomy with probabilities</li>
              <li>• Big-O, Omega, and Theta notation</li>
              <li>• Interactive complexity charts</li>
              <li>• Export results (JSON, Markdown, PDF)</li>
            </ul>

            <div class="flex gap-2 justify-center pt-4">
              <Badge variant="success">O(1)</Badge>
              <Badge variant="warning">O(n)</Badge>
              <Badge variant="danger">O(n²)</Badge>
            </div>

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
