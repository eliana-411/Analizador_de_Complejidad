# 📊 Reporte de Análisis de Complejidad

**Fecha de generación:** 11/12/2025 21:26:56  
**Sistema:** Analizador de Complejidad v1.0

---

## 1. Resumen Ejecutivo

| Aspecto | Valor |
|---------|-------|
| **Estado** | ❌ Con errores |
| **Tipo de Algoritmo** | Recursivo |
| **Mejor Caso** | N/A |
| **Caso Promedio** | Θ(C_1·(-0.6180)ⁿ + C_2·(1.6180)ⁿ) |
| **Peor Caso** | N/A |

## 2. Diagrama de Flujo (Flowchart)

Representación visual del flujo de ejecución del algoritmo:

```mermaid
flowchart TD
    N0([Inicio: fibonacci])
    N1{n ≤ 1?}
    N2[/Retornar n/]
    N3[Continuar]
    N4[else]
    N5[/Retornar CALL fibonacci(n - 1) + CALL fibonacci(n - 2)/]
    N6([Fin: fibonacci])
    N0 --> N1
    N1 -->|Sí| N2
    N2 --> N3
    N1 -->|No| N3
    N3 --> N4
    N4 --> N5
    N5 --> N6
```

**Leyenda:**
- `([...])`: Nodos de inicio/fin
- `[...]`: Procesos y asignaciones
- `{...?}`: Decisiones (condiciones)
- `[/... /]`: Retorno de función

## 2. Proceso de Análisis

### 2.1 Detección de Entrada
🔍 **Tipo detectado:** Pseudocódigo
➡️ Se procedió directamente a validación

### 2.2 Validación de Sintaxis
✅ **Resultado:** Pseudocódigo válido
- 0 errores encontrados

## 4. Análisis de Costos
### 4.1 Tabla de Costos por Línea
| Línea | Código | C_op | Frecuencia | Total |
|-------|--------|------|------------|-------|
| ... | ... | ... | ... | ... |

*⚠️ Sección pendiente de implementación*

## 5. Resolución de Ecuaciones de Recurrencia

### 5.1 Método Utilizado: None

### 5.2 Ecuaciones Analizadas

**Mejor Caso:**
```
T(1) = c
```

**Caso Promedio:**
```
T(n) = T(n-1) + T(n-2) + c
```

**Peor Caso:**
```
T(1) = c
```

### 5.3 Paso a Paso de la Resolución

#### Caso Promedio

**Ecuación:** `T(n) = T(n-1) + T(n-2) + c`
**Método:** EcuacionCaracteristica

**Pasos:**
1. 📝 Ecuación: T(n) = T(n-1) + T(n-2) + c
2. 
3. 🔹 MÉTODO DE ECUACIONES CARACTERÍSTICAS
4.    Para recurrencias lineales con múltiples términos recursivos
5. 
6. ⚠️  Esta recurrencia es NO homogénea (tiene f(n) = c)
7.    Por ahora, solo resolvemos la parte homogénea.
8. 
9. 🔹 PASO 1: Formar ecuación característica
10.    Asumimos T(n) = rⁿ
11. 
12.    Ecuación característica: r^2 - 1r - 1 = 0
13. 
14. 🔹 PASO 2: Resolver ecuación característica
15.    Resolviendo usando métodos numéricos...
16.    Raíces encontradas: 2
17. 
18.    r_1 = -0.618034
19.    r_2 = 1.618034
20. 
21. 🔹 PASO 3: Construir solución general
22.    Todas las raíces son distintas
23.    Solución: T(n) = C₁·r₁ⁿ + C₂·r₂ⁿ + ... + Cₖ·rₖⁿ
24. 
25.    T(n) = C_1·(-0.6180)ⁿ + C_2·(1.6180)ⁿ
26. 
27.    Donde C₁, C₂, ... son constantes determinadas por condiciones iniciales
28. 

**Explicación:** 
╔══════════════════════════════════════════════════════════════╗
║              ECUACIONES CARACTERÍSTICAS                      ║
║            (Recurrencia Lineal Múltiple)                     ║
╚══════════════════════════════════════════════════════════════╝

Ecuación: T(n) = T(n-1) + T(n-2) + c

ESTRATEGIA:
  1. Asumir T(n) = rⁿ
  2. Formar ecuación característica
  3. Resolver para encontrar raíces
  4. Construir solución general

ECUACIÓN CARACTERÍSTICA: r^2 - 1r - 1 = 0

RAÍCES:
  r_1 ≈ -0.618034
  r_2 ≈ 1.618034

SOLUCIÓN GENERAL: T(n) = C_1·(-0.6180)ⁿ + C_2·(1.6180)ⁿ

Las constantes C₁, C₂, ... se determinan usando las condiciones
iniciales T(0), T(1), ..., T(k-1).


**Solución:** `C_1·(-0.6180)ⁿ + C_2·(1.6180)ⁿ`


### 4.4 Complejidades Finales

| Caso | Notación Ω (mejor) | Notación Θ (promedio) | Notación O (peor) |
|------|-------------------|---------------------|-------------------|
| Resultado | N/A | Θ(C_1·(-0.6180)ⁿ + C_2·(1.6180)ⁿ) | N/A |

## 5. Pseudocódigo Final
```
fibonacci(int n)
begin
    if (n ≤ 1) then
    begin
        return n
    end
    else
    begin
        return CALL fibonacci(n - 1) + CALL fibonacci(n - 2)
    end
end
```

## 6. Conclusiones
⚠️ El análisis se completó con advertencias.

## 📊 Métricas de Ejecución

### ⏱️ Tiempo de Ejecución

| Fase | Llamadas | Total (s) | Promedio (s) |
|------|----------|-----------|--------------|

**Duración total:** 422.47 segundos
