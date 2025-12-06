# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 05/12/2025 10:39:35  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ⚠️ Corregido automáticamente |
| **Tipo de Algoritmo** | Iterativo |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0[Algoritmo CP (int A[n])]
    N1[contador <- 0]
    N2[for i <- 1 to n do]
    N3[Si el numero del arreglo es par, incrementar un contador en 1]
    N0 --> N1
    N1 --> N2
    N2 --> N3
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis
### 2.1 Clasificación de Estructura Algorítmica (ML)
🤖 **Categoría principal:** ITERATIVO
📊 **Confianza:** 37.4%

**Otras posibilidades:**
- ordenamiento (25.5%)
- busqueda (14.2%)

> 💡 Esta clasificación es automática y puede ayudar a entender el tipo de algoritmo.

### 2.2 Detección de Entrada
🔍 **Tipo detectado:** Pseudocódigo
➡️ Se procedió directamente a validación

### 2.3 Validación de Sintaxis
❌ **Resultado:** Se encontraron 1 errores

**Errores por capa:**

**2_DECLARACIONES:**
- Subrutina print, parámetro 1: Falta tipo. Use: int contador o real contador

### 2.4 Corrección Automática
🔧 **Resultado:** Pseudocódigo corregido exitosamente
📚 **Ejemplos usados:** 01-busqueda-lineal, 02-busqueda-binaria, 12-insertion-sort
⚠️ **Re-validación:** Aún quedan 1 errores

## 5. Pseudocódigo Final
```
CP(int A[], int n)
begin
    int i, contador
    
    contador 🡨 0
    
    for i 🡨 1 to n do
    begin
        if (A[i] mod 2 = 0) then
        begin
            contador 🡨 contador + 1
        end
    end
    
    CALL print(contador)
end
```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

**Errores encontrados:**
- Pseudocódigo inválido: 1 errores

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 8.72 segundos

### 💰 Consumo de Tokens y Costos

| Métrica | Valor |
|---------|-------|
| Llamadas LLM | 1 |
| Tokens entrada | 1,015 |
| Tokens salida | 271 |
| **Total tokens** | **1,286** |
| **Costo total** | **$0.007110 USD** |

#### Detalle por Modelo

| Modelo | Llamadas | Tokens | Costo USD |
|--------|----------|--------|-----------|
| claude-sonnet-4-5-20250929 | 1 | 1,286 | $0.007110 |
