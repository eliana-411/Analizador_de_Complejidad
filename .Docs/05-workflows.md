# 5. WORKFLOWS

## 5.1 Workflow Principal: Análisis Completo

**Propósito:** Orquestar todo el proceso desde input hasta output final.

**Pasos:**
1. Recibir pseudocódigo
2. Ejecutar Agente Validador
3. Si no válido → terminar con error
4. Si válido → continuar
5. Ejecutar Agente Analizador de Complejidad
6. Ejecutar Agente de Representación Matemática
7. Ejecutar Agente Resolver
8. Ejecutar Agente de Notación Asintótica
9. Ejecutar Agente Reportador
10. Retornar reporte final

**Decisiones (branching):**
- Después de validación: ¿Es válido? Sí/No
- Durante análisis: ¿Es iterativo o recursivo?

**Criterio de Terminado:**
- [ ] Todos los agentes completaron exitosamente
- [ ] El reporte final está generado
- [ ] No hay errores pendientes

---

## 5.2 Workflow de Validación y Corrección

**Propósito:** Asegurar que el pseudocódigo es válido antes de analizar.

**Pasos:**
1. Parsear pseudocódigo con Lark (si necesario)
2. Validar contra gramática
3. Si hay errores → intentar corrección (decisión pendiente)
4. Clasificar como iterativo/recursivo
5. Retornar resultado

**Decisiones:**
- ¿Intentar corrección automática o solo reportar?

**Criterio de Terminado:**
- [ ] Pseudocódigo validado o errores documentados
- [ ] Clasificación iterativo/recursivo completada

---

## 5.3 Workflow de Análisis de Complejidad

**Propósito:** Costear el algoritmo en los 3 escenarios.

**Pasos:**
1. Recibir pseudocódigo validado + clasificación
2. Si iterativo → analizar ciclos
3. Si recursivo → identificar relación de recurrencia
4. Diferenciar escenarios (mejor/peor/promedio)
5. Costear cada escenario
6. Retornar costos

**Decisiones:**
- Branch: iterativo vs recursivo
- ¿Qué condiciones definen cada escenario?

**Criterio de Terminado:**
- [ ] Costos identificados para los 3 escenarios
- [ ] Justificación clara de cada costo

---

## 5.4 Workflow de Resolución Matemática

**Propósito:** Convertir costos en ecuaciones y resolverlas.

**Pasos:**
1. Convertir costos a ecuaciones formales
2. Representar como series (si aplica)
3. Resolver con técnicas apropiadas
4. Aplicar notación asintótica
5. Retornar soluciones

**Decisiones:**
- ¿Qué técnica usar? (divide-venceras, teorema-maestro, etc.)
- Un agente debe actuar como router para decidir que metodología o técnica utilizar.

**Criterio de Terminado:**
- [ ] Ecuaciones resueltas
- [ ] Notación asintótica aplicada
- [ ] Cotas fuertes identificadas

---

## 5.5 Workflow de Reporte Final

**Propósito:** Generar documentación del análisis.

**Pasos:**
1. Recopilar toda la información del estado
2. Estructurar reporte
3. Generar diagramas (si aplican)
4. Formatear en LaTeX/Markdown
5. Retornar reporte

**Criterio de Terminado:**
- [ ] Reporte completo generado
- [ ] Todos los diagramas incluidos
- [ ] Formato correcto
