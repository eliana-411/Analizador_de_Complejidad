import { createSignal } from 'solid-js';
import { useNavigate } from '@solidjs/router';
import { H1 } from '../components/ui/Typography';
import Button from '../components/ui/Button';
import Textarea from '../components/ui/Textarea';
import StatusIndicator from '../components/ui/StatusIndicator';
import ContentContainer from '../components/layout/ContentContainer';
import ClassificationPanel from '../components/ui/ClassificationPanel';
import ErrorModal from '../components/ui/ErrorModal';
import { mockPseudocode } from '../mock-data/validador';
import { validatePseudocode, type ValidationResponse } from '../api/validator';
import type { ValidationStatus } from '../types';

/**
 * Validador page - Pseudocode validation interface
 * Shows validation status with static indicators and text input
 */
export default function Validador() {
  const navigate = useNavigate();

  const [macroalgorith, setMacroalgorith] = createSignal(mockPseudocode);
  const [validationResult, setValidationResult] = createSignal<ValidationResponse | null>(null);
  const [isAnalyzing, setIsAnalyzing] = createSignal(false);
  const [errorModal, setErrorModal] = createSignal<{
    isOpen: boolean;
    layer: string;
    errors: string[];
  }>({
    isOpen: false,
    layer: '',
    errors: []
  });

  const getLayerStatus = (layerKey: string): ValidationStatus => {
    const result = validationResult();
    if (!result) return 'pending';
    const layer = result.capas[layerKey];
    return layer?.valido ? 'valid' : 'invalid';
  };

  const handleStatusClick = (layerKey: string) => {
    const result = validationResult();
    if (!result) return;

    const layer = result.capas[layerKey];
    if (!layer.valido && layer.errores.length > 0) {
      setErrorModal({
        isOpen: true,
        layer: layerKey,
        errors: layer.errores
      });
    }
  };

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    try {
      console.log('Analyzing pseudocode...');

      const resultado = await validatePseudocode({
        pseudocodigo: macroalgorith(),
        return_suggestions: true
      });

      console.log('Resultado de validación:', resultado);
      setValidationResult(resultado);

      // Si la validación es exitosa, navegar a Results
      if (resultado.valido_general) {
        console.log('Validación exitosa, navegando a Results...');
        navigate(`/results?pseudocodigo=${encodeURIComponent(macroalgorith())}`);
      }

    } catch (error) {
      console.error('Error al validar:', error);
      // TODO: Mostrar error al usuario con un toast/notification
    } finally {
      setIsAnalyzing(false);
    }
  };

  return (
    <ContentContainer>
      <div class="space-y-8 animate-fade-in-up">
        {/* Header */}
        <H1 class="text-center">Analizador de complejidad de un algoritmo</H1>

        {/* Status Indicators Row - Clickable */}
        <div class="flex flex-wrap justify-center gap-8 py-4">
          <div onClick={() => handleStatusClick('1_LEXICA')} class="cursor-pointer">
            <StatusIndicator label="Léxica" status={getLayerStatus('1_LEXICA')} />
          </div>
          <div onClick={() => handleStatusClick('2_DECLARACIONES')} class="cursor-pointer">
            <StatusIndicator label="Declaraciones" status={getLayerStatus('2_DECLARACIONES')} />
          </div>
          <div onClick={() => handleStatusClick('3_ESTRUCTURA')} class="cursor-pointer">
            <StatusIndicator label="Estructura" status={getLayerStatus('3_ESTRUCTURA')} />
          </div>
          <div onClick={() => handleStatusClick('4_EXPRESIONES')} class="cursor-pointer">
            <StatusIndicator label="Expresiones" status={getLayerStatus('4_EXPRESIONES')} />
          </div>
          <div onClick={() => handleStatusClick('5_SENTENCIAS')} class="cursor-pointer">
            <StatusIndicator label="Sentencias" status={getLayerStatus('5_SENTENCIAS')} />
          </div>
          <div onClick={() => handleStatusClick('6_SUBRUTINAS')} class="cursor-pointer">
            <StatusIndicator label="Subrutinas" status={getLayerStatus('6_SUBRUTINAS')} />
          </div>
          <div onClick={() => handleStatusClick('7_SEMANTICA')} class="cursor-pointer">
            <StatusIndicator label="Semántica" status={getLayerStatus('7_SEMANTICA')} />
          </div>
        </div>

        {/* Main Content: Two-Column Layout */}
        <div class="grid grid-cols-12 gap-6">
          {/* Left Column: Textarea (60%) */}
          <div class="col-span-7">
            <Textarea
              placeholder="IN(pseudocodigo)"
              value={macroalgorith()}
              onChange={setMacroalgorith}
              onFileUpload={(content, filename) => {
                setMacroalgorith(content);
                console.log(`Archivo cargado: ${filename}`);
                // Analizar automáticamente después de cargar el archivo
                setTimeout(() => handleAnalyze(), 100);
              }}
              rows={20}
              class="font-mono text-sm"
            />

            {/* Analyze Button - below textarea */}
            <div class="flex justify-end mt-4">
              <Button
                variant="warning"
                onClick={handleAnalyze}
                disabled={isAnalyzing()}
                class="px-12 py-4 text-lg font-bold shadow-lg hover:shadow-xl transform hover:-translate-y-0.5 transition-all duration-200"
              >
                {isAnalyzing() ? 'ANALIZANDO...' : 'ANALIZAR CÓDIGO'}
              </Button>
            </div>
          </div>

          {/* Right Column: Classification Panel (40%) */}
          <div class="col-span-5">
            <ClassificationPanel
              classification={validationResult()?.clasificacion}
              isLoading={isAnalyzing()}
            />
          </div>
        </div>

        {/* Error Modal */}
        <ErrorModal
          isOpen={errorModal().isOpen}
          onClose={() => setErrorModal({ isOpen: false, layer: '', errors: [] })}
          layerName={errorModal().layer}
          errors={errorModal().errors}
        />
      </div>
    </ContentContainer>
  );
}
