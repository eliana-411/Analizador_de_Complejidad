import { createSignal, Show } from 'solid-js';
import { H1 } from '../components/ui/Typography';
import Button from '../components/ui/Button';
import Textarea from '../components/ui/Textarea';
import StatusIndicator, { type ValidationStatus } from '../components/ui/StatusIndicator';
import ToggleButtonGroup from '../components/ui/ToggleButtonGroup';
import ContentContainer from '../components/layout/ContentContainer';
import Toast from '../components/ui/Toast';
import { mockPseudocode } from '../mock-data/validador';
import { validatePseudocode, correctPseudocode, type ValidationResponse, type CorrectionResponse } from '../api/validator';

/**
 * Validador page - Pseudocode validation interface
 * Shows validation status with dynamic indicators and text input
 */
export default function Validador() {
  const [macroalgorith, setMacroalgorith] = createSignal(mockPseudocode);
  const [visualization, setVisualization] = createSignal(false);
  const [algorithmType, setAlgorithmType] = createSignal('iterativo');

  // Validation state
  const [validationResult, setValidationResult] = createSignal<ValidationResponse | null>(null);
  const [isValidating, setIsValidating] = createSignal(false);
  const [errorMessage, setErrorMessage] = createSignal<string | null>(null);
  const [showToast, setShowToast] = createSignal(false);

  // Correction state
  const [correctedCode, setCorrectedCode] = createSignal<string | null>(null);
  const [isCorrecting, setIsCorrecting] = createSignal(false);
  const [correctionExplanation, setCorrectionExplanation] = createSignal<string | null>(null);

  // Helper function para obtener el status de una capa
  const getLayerStatus = (layerKey: string): ValidationStatus => {
    const result = validationResult();
    if (!result) return 'pending';

    const layer = result.capas[layerKey];
    if (!layer) return 'pending';

    return layer.valido ? 'valid' : 'invalid';
  };

  const handleAnalyze = async () => {
    setIsValidating(true);
    setErrorMessage(null);
    setValidationResult(null);
    setShowToast(false);
    setCorrectedCode(null);
    setCorrectionExplanation(null);

    try {
      console.log('Analyzing pseudocode...');

      const resultado = await validatePseudocode({
        pseudocodigo: macroalgorith(),
        return_suggestions: true
      });

      console.log('Resultado de validación:', resultado);

      // Guardar resultado
      setValidationResult(resultado);

      // Actualizar tipo de algoritmo si se detectó
      if (resultado.tipo_algoritmo) {
        setAlgorithmType(resultado.tipo_algoritmo.toLowerCase());
      }

      // Mostrar toast
      setShowToast(true);

      // Auto-cerrar toast después de 8 segundos
      setTimeout(() => setShowToast(false), 8000);

    } catch (error) {
      console.error('Error al validar:', error);
      setErrorMessage(error instanceof Error ? error.message : 'Error desconocido al validar');
      setShowToast(true);

      // Auto-cerrar toast de error después de 5 segundos
      setTimeout(() => setShowToast(false), 5000);
    } finally {
      setIsValidating(false);
    }
  };

  const handleCorrect = async () => {
    const result = validationResult();
    if (!result || result.valido_general) return;

    setIsCorrecting(true);
    setErrorMessage(null);
    setShowToast(false);

    try {
      console.log('Correcting pseudocode...');

      const correccion = await correctPseudocode({
        pseudocodigo: macroalgorith(),
        resultado_validacion: result
      });

      console.log('Resultado de corrección:', correccion);

      if (correccion.corregido) {
        setCorrectedCode(correccion.pseudocodigo);
        setCorrectionExplanation(correccion.explicacion);

        // Mostrar toast de éxito
        setShowToast(true);
        setTimeout(() => setShowToast(false), 8000);
      }
    } catch (error) {
      console.error('Error al corregir:', error);
      setErrorMessage(error instanceof Error ? error.message : 'Error desconocido al corregir');
      setShowToast(true);

      // Auto-cerrar toast de error después de 5 segundos
      setTimeout(() => setShowToast(false), 5000);
    } finally {
      setIsCorrecting(false);
    }
  };

  const applyCorrection = () => {
    const code = correctedCode();
    if (code) {
      setMacroalgorith(code);
      setCorrectedCode(null);
      setCorrectionExplanation(null);
    }
  };

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        {/* Header */}
        <H1 class="text-center">Analizador de complejidad de un algoritmo</H1>

        {/* Status Indicators Row */}
        <div class="flex flex-wrap justify-center gap-8 py-4">
          <StatusIndicator label="Léxica" status={getLayerStatus('1_LEXICA')} />
          <StatusIndicator label="Declaraciones" status={getLayerStatus('2_DECLARACIONES')} />
          <StatusIndicator label="Estructuras" status={getLayerStatus('3_ESTRUCTURA')} />
          <StatusIndicator label="Expresiones" status={getLayerStatus('4_EXPRESIONES')} />
          <StatusIndicator label="Sentencias" status={getLayerStatus('5_SENTENCIAS')} />
          <StatusIndicator label="Subrutinas" status={getLayerStatus('6_SUBRUTINAS')} />
          <StatusIndicator label="Semántica" status={getLayerStatus('7_SEMANTICA')} />
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
          <div class="flex justify-end gap-4">
            <Show when={validationResult() && !validationResult()!.valido_general}>
              <Button
                variant="primary"
                onClick={handleCorrect}
                disabled={isCorrecting() || isValidating()}
                class="px-8 py-4 text-lg font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
              >
                {isCorrecting() ? 'CORRIGIENDO...' : '🤖 CORREGIR AUTOMÁTICAMENTE'}
              </Button>
            </Show>
            <Button
              variant="warning"
              onClick={handleAnalyze}
              disabled={isValidating()}
              class="px-12 py-4 text-lg font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {isValidating() ? 'ANALIZANDO...' : 'ANALIZAR CÓDIGO'}
            </Button>
          </div>
        </div>

        {/* Corrected Code Display */}
        <Show when={correctedCode()}>
          <div class="mt-6 p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-2 border-blue-300 rounded-lg shadow-lg animate-fade-in-up">
            <h4 class="font-bold text-blue-900 text-xl mb-4 flex items-center gap-2">
              <span>✨</span> Código Corregido
            </h4>

            <pre class="text-sm font-mono bg-white p-4 rounded-lg overflow-x-auto border border-blue-200 shadow-inner mb-4 whitespace-pre-wrap">
              {correctedCode()}
            </pre>

            <Show when={correctionExplanation()}>
              <div class="mb-4 p-4 bg-blue-100 rounded-lg border border-blue-200">
                <h5 class="font-semibold text-blue-900 mb-2">Explicación:</h5>
                <p class="text-sm text-blue-800 whitespace-pre-wrap">{correctionExplanation()}</p>
              </div>
            </Show>

            <div class="flex justify-end gap-3">
              <Button
                variant="secondary"
                onClick={() => {
                  setCorrectedCode(null);
                  setCorrectionExplanation(null);
                }}
                class="px-6 py-2"
              >
                Descartar
              </Button>
              <Button
                variant="primary"
                onClick={applyCorrection}
                class="px-6 py-2 font-bold"
              >
                ✓ Aplicar Corrección
              </Button>
            </div>
          </div>
        </Show>

        {/* Toast Notifications */}
        <Show when={showToast()}>
          {/* Success/Error Toast */}
          <Show when={validationResult()} fallback={
            <Show when={errorMessage()}>
              <Toast
                type="error"
                title="Error de conexión"
                message={errorMessage()!}
                onClose={() => setShowToast(false)}
              />
            </Show>
          }>
            {(result) => (
              <Toast
                type={result().valido_general ? 'success' : 'error'}
                title={result().valido_general ? 'Código válido' : 'Código inválido'}
                message={result().tipo_algoritmo ? `Algoritmo ${result().tipo_algoritmo}` : undefined}
                details={[
                  `${result().resumen.total_lineas} líneas analizadas`,
                  `${result().resumen.errores_totales} error${result().resumen.errores_totales !== 1 ? 'es' : ''} encontrado${result().resumen.errores_totales !== 1 ? 's' : ''}`
                ]}
                suggestions={result().sugerencias}
                onClose={() => setShowToast(false)}
              />
            )}
          </Show>
        </Show>
      </div>
    </ContentContainer>
  );
}
