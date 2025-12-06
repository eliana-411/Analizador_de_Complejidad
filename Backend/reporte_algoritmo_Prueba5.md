# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 05/12/2025 10:46:57  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ⚠️ Corregido automáticamente |
| **Tipo de Algoritmo** | None |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0[Algoritmo Prueba5 (n)]
    N1[for i <- 0 to n do]
    N2[print (i)]
    N3[if (i mod 2) = 0 then]
    N4[print ("Par")]
    N0 --> N1
    N1 --> N2
    N2 --> N3
    N3 --> N4
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis
### 2.1 Clasificación de Estructura Algorítmica (ML)
🤖 **Categoría principal:** GREEDY
📊 **Confianza:** 36.5%

**Otras posibilidades:**
- iterativo (22.5%)
- busqueda (15.0%)

> 💡 Esta clasificación es automática y puede ayudar a entender el tipo de algoritmo.

### 2.2 Detección de Entrada
🔍 **Tipo detectado:** Pseudocódigo
➡️ Se procedió directamente a validación

### 2.3 Validación de Sintaxis
❌ **Resultado:** Se encontraron 0 errores

**Errores por capa:**

**1_LEXICA:**
- Línea 8: Carácter inválido '"' en: print ("Par")
- Línea 8: Carácter inválido '"' en: print ("Par")

### 2.4 Corrección Automática
🔧 **Resultado:** Pseudocódigo corregido exitosamente
📚 **Ejemplos usados:** 01-busqueda-lineal, 02-busqueda-binaria, 04-merge-sort
⚠️ **Re-validación:** Aún quedan 0 errores

## 5. Pseudocódigo Final
```
Prueba5(int n)
begin
    int i

    for i 🡨 0 to n do
    begin
        print(i)
        if (i mod 2) = 0 then
        begin
            print('Par')
        end
    end
end
```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

**Errores encontrados:**
- Pseudocódigo inválido: 0 errores

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 13.08 segundos

### 💰 Consumo de Tokens y Costos

| Métrica | Valor |
|---------|-------|
| Llamadas LLM | 1 |
| Tokens entrada | 1,441 |
| Tokens salida | 218 |
| **Total tokens** | **1,659** |
| **Costo total** | **$0.007593 USD** |

#### Detalle por Modelo

| Modelo | Llamadas | Tokens | Costo USD |
|--------|----------|--------|-----------|
| claude-sonnet-4-5-20250929 | 1 | 1,659 | $0.007593 |
