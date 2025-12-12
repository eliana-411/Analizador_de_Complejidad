/**
 * API client for complexity analysis endpoints
 */

export interface AnalisisRequest {
  entrada: string;
  tipo_entrada?: 'pseudocodigo' | 'lenguaje_natural' | 'auto';
  auto_corregir?: boolean;
}

export interface CorreccionResult {
  corregido: boolean;
  pseudocodigo?: string;
  explicacion?: string;
  razon?: string;
  ejemplos_usados?: string[];
  cambios?: Array<{
    linea: number;
    antes: string;
    despues: string;
    razon: string;
  }>;
}

export interface ValidacionComplejidadesResult {
  algorithm_name: string;
  complejidades_sistema: {
    mejor_caso?: string;
    caso_promedio?: string;
    peor_caso?: string;
  };
  complejidades_llm: {
    mejor_caso?: string;
    caso_promedio?: string;
    peor_caso?: string;
  };
  concordancia: boolean;
  analisis_divergencias: Array<{
    caso: string;
    sistema: string;
    llm: string;
    tipo: string;
    severidad: string;
  }>;
  confianza: number;
  recomendacion: string;
}

export interface AnalisisResponse {
  exito: boolean;
  fase_actual: string | null;
  pseudocodigo_original: string | null;
  pseudocodigo_validado: string | null;
  validacion: Record<string, any> | null;
  validacion_inicial?: Record<string, any> | null;
  correccion?: CorreccionResult | null;
  costos_por_linea: Record<string, any> | null;
  ecuaciones: Record<string, any> | null;
  complejidades: ComplejidadesResult | null;
  errores: string[];
  clasificacion?: ClasificacionResult | null;
  flowchart?: string | null;
  reporte_markdown?: string | null;
  diagramas?: Record<string, string> | null;
  validacion_complejidades?: ValidacionComplejidadesResult | null;
}

export interface ComplejidadesResult {
  algorithm_name?: string;
  mejor_caso?: string;
  caso_promedio?: string;
  peor_caso?: string;
  derivacion_caso_promedio?: string;
  metodo_usado?: string;
  ecuaciones?: Record<string, string>;
  ecuaciones_matematicas?: {
    mejor_caso?: string;
    peor_caso?: string;
    caso_promedio?: string;
    ecuaciones_iguales?: boolean;
    casos_base?: string[];
  };
  pasos_resolucion?: Record<string, any>;
  observacion?: string;
}

export interface ClasificacionResult {
  categoria_principal: string;
  confianza: number;
  top_predicciones: Array<{
    categoria: string;
    probabilidad: number;
  }>;
}

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

/**
 * Analiza pseudocódigo sin generar reporte
 */
export async function analyzeCode(
  request: AnalisisRequest
): Promise<AnalisisResponse> {
  const response = await fetch(`${API_BASE_URL}/analisis/analizar`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `Analysis failed: ${response.statusText}`);
  }

  return response.json();
}

/**
 * Analiza pseudocódigo Y genera reporte completo en Markdown
 */
export async function analyzeCodeWithReport(
  request: AnalisisRequest
): Promise<AnalisisResponse> {
  const response = await fetch(`${API_BASE_URL}/analisis/analizar-con-reporte`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `Analysis with report failed: ${response.statusText}`);
  }

  return response.json();
}
