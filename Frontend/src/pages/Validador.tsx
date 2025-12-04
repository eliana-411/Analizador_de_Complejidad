import { createSignal } from 'solid-js';
import { H1 } from '../components/ui/Typography';
import Button from '../components/ui/Button';
import Textarea from '../components/ui/Textarea';
import StatusIndicator from '../components/ui/StatusIndicator';
import ToggleButtonGroup from '../components/ui/ToggleButtonGroup';
import ContentContainer from '../components/layout/ContentContainer';
import { mockPseudocode, mockValidation } from '../mock-data/validador';
import { validatePseudocode } from '../api/validator';

/**
 * Validador page - Pseudocode validation interface
 * Shows validation status with static indicators and text input
 */
export default function Validador() {
  const [macroalgorith, setMacroalgorith] = createSignal(mockPseudocode);
  const [visualization, setVisualization] = createSignal(false);
  const [algorithmType, setAlgorithmType] = createSignal('iterativo');

  const handleAnalyze = async () => {
    try {
      console.log('Analyzing pseudocode...');

      const resultado = await validatePseudocode({
        pseudocodigo: macroalgorith(),
        return_suggestions: true
      });

      console.log('Resultado de validación:', resultado);

      // TODO: Actualizar estado de los StatusIndicators con resultado.capas
      // TODO: Mostrar sugerencias al usuario si hay errores

    } catch (error) {
      console.error('Error al validar:', error);
      // TODO: Mostrar error al usuario
    }
  };

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        {/* Header */}
        <H1 class="text-center">Analizador de complejidad de un algoritmo</H1>

        {/* Status Indicators Row */}
        <div class="flex flex-wrap justify-center gap-8 py-4">
          <StatusIndicator label="Léxica" status={mockValidation.lexica} />
          <StatusIndicator label="Declaraciones" status="pending" />
          <StatusIndicator label="Estructuras" status={mockValidation.estructuras} />
          <StatusIndicator label="Expresiones" status="pending" />
          <StatusIndicator label="Sentencias" status="pending" />
          <StatusIndicator label="Sintaxis" status={mockValidation.sintaxis} />
          <StatusIndicator label="Semántica" status="pending" />
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
        <div class="flex flex-col gap-6">
          {/* Textarea - takes up full width */}
          <div class="w-full">
            <Textarea
              placeholder="IN(pseudocodigo)"
              value={macroalgorith()}
              onChange={setMacroalgorith}
              rows={16}
              class="font-mono text-sm"
            />
          </div>

          {/* Analyze Button - below textarea */}
          <div class="flex justify-end">
            <Button
              variant="warning"
              onClick={handleAnalyze}
              class="px-12 py-4 text-lg font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
            >
              ANALIZAR CÓDIGO
            </Button>
          </div>
        </div>
      </div>
    </ContentContainer>
  );
}
