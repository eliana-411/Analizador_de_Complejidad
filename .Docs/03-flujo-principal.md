# 3. FLUJO PRINCIPAL DE PROCESAMIENTO

### 3.1 Diagrama de Flujo de Datos

```mermaid
flowchart TB
    Start([Input: Pseudocódigo]) --> Validate[Validación y Corrección]
    Validate --> Check{¿Es Válido?}
    Check -->|No| Error([Error: Pseudocódigo Inválido])
    Check -->|Sí| Classify[Clasificación]
    Error --> Validate
    Classify --> Type{Tipo}
    Type -->|Iterativo| AnalyzeIter[Análisis Iterativo]
    Type -->|Recursivo| AnalyzeRec[Análisis Recursivo]
    AnalyzeIter --> Cost[Costeo de Escenarios]
    AnalyzeRec --> Cost
    Cost --> Math[Representación Matemática]
    Math --> Solve[Resolución de Series]
    Solve --> Asymptotic[Notación Asintótica]
    Asymptotic --> Report[Reporte con Justificación]
    Report --> End([Output: Mejor, Peor, Promedio + Justificación])
    style Start fill:#e1f5e1
    style End fill:#e1f5e1
    style Error fill:#ffe1e1
    style Check fill:#fff4e1
    style Type fill:#fff4e1
```

### 3.2 Descripción de Cada Fase

| Fase | Input | Output | Propósito |
|------|-------|--------|-----------|
| **Validación** | Pseudocódigo raw | Pseudocódigo validado/corregido + flag iterativo/recursivo | Asegurar que el código cumple la gramática |
| **Clasificación** | Pseudocódigo validado | Tipo (iterativo/recursivo) + metadata | Determinar estrategia de análisis |
| **Análisis** | Pseudocódigo + tipo | Costeo de instrucciones | Calcular costo computacional |
| **Costeo Escenarios** | Análisis | Costos mejor/peor/promedio | Diferenciar casos |
| **Representación Matemática** | Costos | Ecuaciones/series matemáticas | Formalizar el análisis |
| **Resolución** | Ecuaciones/series | Soluciones cerradas | Resolver matemáticamente |
| **Notación Asintótica** | Soluciones | O, Ω, Θ con cotas | Expresar complejidad |
| **Reporte** | Todo lo anterior | Documento justificado | Comunicar resultados |
