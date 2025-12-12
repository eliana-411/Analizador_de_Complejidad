import { createContext, useContext, createSignal, type ParentProps } from 'solid-js';
import type { AnalisisResponse } from '../api/analyzer';

/**
 * Context para compartir el resultado del análisis entre todas las páginas
 * Evita múltiples llamadas al backend cuando el usuario navega entre páginas
 */

interface AnalysisContextType {
    analysisResult: () => AnalisisResponse | null;
    setAnalysisResult: (result: AnalisisResponse | null) => void;
    isLoading: () => boolean;
    setIsLoading: (loading: boolean) => void;
    clearAnalysis: () => void;
}

const AnalysisContext = createContext<AnalysisContextType>();

/**
 * Provider que envuelve la aplicación y proporciona estado global
 */
export const AnalysisProvider = (props: ParentProps) => {
    const [analysisResult, setAnalysisResult] = createSignal<AnalisisResponse | null>(null);
    const [isLoading, setIsLoading] = createSignal(false);

    const clearAnalysis = () => {
        setAnalysisResult(null);
        setIsLoading(false);
    };

    const value: AnalysisContextType = {
        analysisResult,
        setAnalysisResult,
        isLoading,
        setIsLoading,
        clearAnalysis
    };

    return (
        <AnalysisContext.Provider value={value}>
            {props.children}
        </AnalysisContext.Provider>
    );
};

/**
 * Hook para acceder al contexto de análisis desde cualquier componente
 */
export function useAnalysis() {
    const context = useContext(AnalysisContext);
    if (!context) {
        throw new Error('useAnalysis debe ser usado dentro de AnalysisProvider');
    }
    return context;
}
