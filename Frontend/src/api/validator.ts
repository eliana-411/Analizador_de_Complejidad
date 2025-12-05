export interface ValidationRequest {
  pseudocodigo: string;
  return_suggestions?: boolean;
}

export interface LayerResult {
  valido: boolean;
  errores: string[];
  detalles: string[];
}

export interface ClasificacionPrediccion {
  categoria: string;
  probabilidad: number;
}

export interface ClasificacionResult {
  categoria_principal: string;
  confianza: number;
  top_predicciones: ClasificacionPrediccion[];
}

export interface ValidationResponse {
  valido_general: boolean;
  tipo_algoritmo?: string | null;
  capas: Record<string, LayerResult>;
  resumen: {
    total_lineas: number;
    clases_encontradas: number;
    subrutinas_encontradas: number;
    errores_totales: number;
  };
  clasificacion?: ClasificacionResult | null;
  sugerencias?: string[];
}


const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export async function validatePseudocode(
  request: ValidationRequest
): Promise<ValidationResponse> {
  const response = await fetch(`${API_BASE_URL}/validador/validar`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(request),
  });

  if (!response.ok) {
    const error = await response.json().catch(() => ({ detail: response.statusText }));
    throw new Error(error.detail || `Validation failed: ${response.statusText}`);
  }

  return response.json();
}
