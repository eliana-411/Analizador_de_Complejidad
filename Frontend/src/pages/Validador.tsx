import { createSignal } from 'solid-js';
import { H1 } from '../components/ui/Typography';
import Button from '../components/ui/Button';
import Textarea from '../components/ui/Textarea';
import StatusIndicator from '../components/ui/StatusIndicator';
import ToggleButtonGroup from '../components/ui/ToggleButtonGroup';
import ContentContainer from '../components/layout/ContentContainer';
import { mockPseudocode, mockValidation } from '../mock-data/validador';

/**
 * Validador page - Pseudocode validation interface
 * Shows validation status with static indicators and text input
 */
export default function Validador() {
  const [macroalgorith, setMacroalgorith] = createSignal(mockPseudocode);
  const [visualization, setVisualization] = createSignal(false);
  const [algorithmType, setAlgorithmType] = createSignal('iterativo');

  const handleAnalyze = () => {
    console.log('Analyzing pseudocode...', {
      pseudocode: macroalgorith(),
      visualization: visualization(),
      algorithmType: algorithmType()
    });
  };

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        {/* Header */}
        <H1 class="text-center">Analizador de complejidad de un algoritmo</H1>

        {/* Status Indicators Row */}
        <div class="flex justify-center gap-12">
          <StatusIndicator label="léxica" status={mockValidation.lexica} />
          <StatusIndicator label="sintaxis" status={mockValidation.sintaxis} />
          <StatusIndicator label="estructuras" status={mockValidation.estructuras} />
        </div>

        {/* Toggle Buttons Row */}
        <div class="flex justify-center gap-4">
          <ToggleButtonGroup
            options={[
              { value: 'false', label: 'Visualiza tu pseudocódigo' },
              { value: 'true', label: 'Ocultar visualización' }
            ]}
            value={String(visualization())}
            onChange={(val) => setVisualization(val === 'true')}
            color="blue"
          />
          <ToggleButtonGroup
            options={[
              { value: 'iterativo', label: 'iterativo' },
              { value: 'recursivo', label: 'recursivo' }
            ]}
            value={algorithmType()}
            onChange={setAlgorithmType}
            color="orange"
          />
        </div>

        {/* Main Content: Textarea + Analyze Button */}
        <div class="grid grid-cols-1 lg:grid-cols-12 gap-6">
          {/* Textarea - takes up most space */}
          <div class="lg:col-span-9">
            <Textarea
              placeholder="IN(pseudocodigo)"
              value={macroalgorith()}
              onChange={setMacroalgorith}
              rows={16}
            />
          </div>

          {/* Analyze Button - vertical on the right */}
          <div class="lg:col-span-3 flex items-stretch">
            <Button
              variant="warning"
              onClick={handleAnalyze}
              class="w-full h-full flex items-center justify-center text-xl font-bold"
            >
              <span class="writing-mode-vertical-rl rotate-180 py-8">
                ANALYZE
              </span>
            </Button>
          </div>
        </div>
      </div>
    </ContentContainer>
  );
}
