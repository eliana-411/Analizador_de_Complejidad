import { createSignal } from 'solid-js';
import { useNavigate } from '@solidjs/router';
import { H1 } from '../components/ui/Typography';
import Button from '../components/ui/Button';
import Textarea from '../components/ui/Textarea';
import StatusIndicator from '../components/ui/StatusIndicator';
import ContentContainer from '../components/layout/ContentContainer';
import ClassificationPanel from '../components/ui/ClassificationPanel';
import ErrorModal from '../components/ui/ErrorModal';
import CorrectionFeedback from '../components/ui/CorrectionFeedback';
import { mockPseudocode } from '../mock-data/validador';
import { validatePseudocode, type ValidationResponse } from '../api/validator';
import { analyzeCode, type AnalisisResponse } from '../api/analyzer';
import type { ValidationStatus } from '../types';
import { useAnalysis } from '../contexts/AnalysisContext';

/**
 * Validador page - Pseudocode validation interface
 * Shows validation status with static indicators and text input
 */
export default function Validador() {
  const navigate = useNavigate();
  const { setAnalysisResult, setIsLoading: setGlobalLoading } = useAnalysis();

  const [macroalgorith, setMacroalgorith] = createSignal(mockPseudocode);
  const [validationResult, setValidationResult] = createSignal<ValidationResponse | null>(null);
  const [analysisResult, setLocalAnalysisResult] = createSignal<AnalisisResponse | null>(null);
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
    setGlobalLoading(true);
    try {
      console.log('Analyzing pseudocode...');

      // Call analysis endpoint to get validation + correction data
      const resultado = await analyzeCode({
        entrada: macroalgorith(),
        tipo_entrada: 'auto',
        auto_corregir: true
      });

      console.log('Resultado de análisis:', resultado);

      // Guardar en CONTEXTO GLOBAL (memoria compartida)
      setAnalysisResult(resultado);

      // También guardar localmente para mostrar UI
      setLocalAnalysisResult(resultado);

      // Extract validation data for UI (from validacion or validacion_inicial)
      const validacionData = resultado.validacion;
      if (validacionData) {
        // Map analysis validation to ValidationResponse format
        const mappedValidation: ValidationResponse = {
          valido_general: validacionData.valido_general || false,
          tipo_algoritmo: validacionData.tipo_algoritmo || null,
          capas: validacionData.capas || {},
          resumen: validacionData.resumen || {
            total_lineas: 0,
            clases_encontradas: 0,
            subrutinas_encontradas: 0,
            errores_totales: 0
          },
          clasificacion: resultado.clasificacion || null,
          sugerencias: []
        };
        setValidationResult(mappedValidation);
      }

      // No redirigir automáticamente - el usuario navegará con el botón de flecha

    } catch (error) {
      console.error('Error al analizar:', error);
      // TODO: Mostrar error al usuario con un toast/notification
    } finally {
      setIsAnalyzing(false);
      setGlobalLoading(false);
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

            {/* Correction Feedback - below ANALIZAR button */}
            <CorrectionFeedback
              correccion={analysisResult()?.correccion}
              validacionInicial={analysisResult()?.validacion_inicial}
            />
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

        {/* Navigation Button */}
        <Show when={validationResult()?.valido_general && analysisResult()}>
          <div class="flex justify-end mt-8">
            <button
              onClick={() => {
                // Ya no pasamos pseudocódigo por URL - el contexto tiene TODO
                navigate('/analizador');
              }}
              class="flex items-center gap-2 px-6 py-3 rounded-lg font-semibold text-white transition-all duration-200 shadow-md hover:shadow-lg"
              style="background: linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%);"
            >
              <span>Siguiente: Ver Tabla Omega</span>
              <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
              </svg>
            </button>
          </div>
        </Show>
      </div>
    </ContentContainer>
  );
}
