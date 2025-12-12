// Shared TypeScript types for the application

export type ButtonVariant = 'primary' | 'secondary' | 'ghost' | 'danger' | 'blue' | 'orange' | 'warning';

export type BadgeVariant = 'success' | 'warning' | 'danger' | 'info';

export type TypographyVariant = 'h1' | 'h2' | 'h3' | 'body';

export type InputType = 'text' | 'number' | 'email' | 'password';

export type ValidationStatus = 'valid' | 'invalid' | 'pending';

export interface ComponentSectionProps {
  title: string;
  description?: string;
  children: any;
}

export interface CodeBlockProps {
  code: string;
  language: string;
}

// Future: API types for backend integration
export interface AnalyzeRequest {
  pseudocode: string;
}

export interface LineCost {
  line_number: number;
  code: string;
  C_op: number;
  Freq: string;
  Total: string;
}

export interface ScenarioEntry {
  id: string;
  condition: string;
  state: string;
  cost_T: string;
  probability_P: string;
  justification_subtable: LineCost[];
}

export interface OmegaTable {
  scenarios: ScenarioEntry[];
  complexity_O?: string;
  complexity_Omega?: string;
  complexity_Theta?: string;
}

// Additional types for mocked UI

export interface ScenarioRow {
  id: string;
  s0: string;
  A0: string;
  exito: string;
  k: string;
  lineCosts: LineCost[];
  justification: string;
  cost: string;
}

export interface BoundAnalysis {
  cota: string;
  escenario: string;
  ecuacion?: string;
  expanded: {
    analysis: string;
    formula: string;
  };
}

export interface AlgorithmClassification {
  type: string;
  category: string;
  complexity: string;
}

export interface RecurrenceSolution {
  formula: string;
  result: string;
  steps: string[];
}

export interface AlgorithmSolution {
  algorithm: string;
  timeComplexity: {
    best: string;
    average: string;
    worst: string;
  };
  spaceComplexity: string;
  characteristics: string[];
  optimizations: string[];
}
