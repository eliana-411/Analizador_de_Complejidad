**FRONTEND: Instalar paquetes**
pip install streamlit


**Correr Frontend**
streamlit run Frontend/ui.py

# 📊 Proyecto: Análisis y Diseño de Algoritmos
## Analizador de Complejidad Computacional

---

## 📖 1. Introducción

Este proyecto busca integrar conocimientos avanzados en **análisis algorítmico**, **técnicas de diseño** y **tecnologías emergentes**, para construir un sistema que, a partir de un algoritmo escrito en pseudocódigo, determine automáticamente su **complejidad computacional**.

El trabajo será desarrollado por parejas de estudiantes y tendrá como eje central la implementación de un **Analizador de Complejidades** asistido por **Modelos de Lenguaje de Gran Escala (LLMs)**.

---

## 🎯 2. Objetivo General

Diseñar e implementar un **sistema inteligente** que analice algoritmos escritos en pseudocódigo, con el fin de determinar su complejidad en notación:
- **O** (peor caso)
- **Ω** (mejor caso)
- **Θ** (caso promedio)
- **Cotas fuertes**

Utilizando técnicas avanzadas de diseño algorítmico e integrando fundamentos teóricos y prácticos de los **Modelos de Lenguaje (LLMs)**.

---

## 📝 3. Descripción del Proyecto

El sistema debe ser capaz de interpretar estructuras algorítmicas como:
- ✅ Ciclos (for, while, repeat-until)
- ✅ Condicionales (if-then-else)
- ✅ Recursiones
- ✅ Llamadas a procedimientos
- ✅ Estructuras de datos (vectores, objetos, grafos, etc.)

### 🔍 Salida Esperada

El sistema debe producir un **análisis detallado** que incluya:
- 📊 Complejidad en notación **O, Ω y Θ**
- 🧮 Razonamientos y cálculos paso a paso
- 🌳 Árboles de recursión (cuando aplique)
- 📐 Relaciones de recurrencia
- 💡 Identificación de técnicas algorítmicas aplicadas:
  - Programación dinámica
  - Algoritmos voraces
  - Divide y vencerás
  - Backtracking
  - Heurísticas

---

## 🤖 Incorporación de LLMs (Obligatorio)

Una parte **obligatoria** del proyecto será la incorporación de **modelos de lenguaje (LLMs)**, cuya función será asistir en:

### Funcionalidades con LLM:

| Funcionalidad | Descripción |
|--------------|-------------|
| 🗣️ **Traducción de lenguaje natural** | El sistema puede aceptar descripciones en lenguaje natural del algoritmo y usar un LLM para traducirlo a pseudocódigo estructurado |
| 🧩 **Análisis estructurado** | Llevar el problema a un análisis estructurado por cada paso en el proceso de razonamiento |
| 🏷️ **Clasificación de patrones** | Clasificación de patrones algorítmicos conocidos (búsqueda, ordenamiento, grafos, etc.) |
| ✅ **Verificación matemática** | Verificación o validación del análisis generado por el sistema mediante representación matemática |
| 📊 **Diagramas de ejecución** | Diagramas de representación de seguimiento de la ejecución del pseudocódigo |
| 📄 **Documentación automática** | Apoyo a la documentación explicativa del análisis realizado |
| ⏱️ **Análisis de coste** | Coste por cada instrucción del análisis (microsegundos y tokens por llamado) |

---

## 📦 4. Entregables

### 📋 Documentación

1. **Informe técnico** con:
   - Análisis del sistema desarrollado
   - Metodología utilizada
   - Técnicas aplicadas
   - Ejemplos resueltos

2. **Análisis del propio Analizador**:
   - Complejidad del algoritmo del Analizador de Funciones de eficiencia
   - Mejor caso, peor caso y caso promedio
   - Notaciones O, Ω y Θ para cada caso

### 💻 Código y Pruebas

3. **Código fuente**:
   - Perfectamente documentado
   - Modularizado
   - Funcional

4. **Conjunto de pruebas**:
   - Mínimo **10 algoritmos** de entrada diferentes
   - Casos de prueba variados (iterativos, recursivos, mixtos)

### 🎥 Recursos Explicativos

5. **Material audiovisual/interactivo**:
   - Video explicativo, O
   - Animación, O
   - Presentación interactiva

---

## 📊 5. Criterios de Evaluación

| Criterio | Ponderación | Descripción |
|----------|-------------|-------------|
| ✅ **Correcto análisis de complejidad (O, Ω, Θ)** | **60%** | Precisión en el cálculo de complejidades y cotas fuertes |
| 📊 **Diagramas de seguimiento del pseudocódigo** | **15%** | Calidad y claridad de las representaciones gráficas |
| 🧠 **Aplicación de técnicas algorítmicas avanzadas** | **15%** | Uso correcto de árboles de recursión, recurrencias, DP, etc. |
| 📄 **Informe técnico y recursos** | **5%** | Calidad de documentación y materiales explicativos |
| 🧪 **Cobertura de pruebas y validación** | **5%** | Cantidad y calidad de casos de prueba |

**Total:** 100%

---

## 🚀 6. Observaciones Finales

El proyecto representa una **oportunidad única** para que los estudiantes:

- 🔬 Integren conocimientos de **análisis de algoritmos**
- 🤖 Exploren **nuevas tecnologías** basadas en inteligencia artificial
- 💡 Desarrollen un producto **robusto y técnicamente sólido**
- 🎨 Usen **creatividad** en el aprovechamiento de herramientas LLM para análisis algorítmico

### 🎓 Expectativas:

- Sistema funcional y completo
- Análisis riguroso y matemáticamente correcto
- Documentación clara y profesional
- Innovación en el uso de LLMs

---

## 💡 Propuesta de Uso Técnico de LLMs

### Opciones de Integración (Gemini/ChatGPT/Anthropic o similares):

#### 1. 🔍 **Asistencia en Parsing**
Usar un LLM (vía API o manualmente) para sugerir la estructura lógica del algoritmo.

**Ejemplo de flujo:**
```
Pseudocódigo → LLM → Estructura AST → Análisis de complejidad
```

#### 2. ⚖️ **Comparación de Resultados**
El sistema del estudiante produce una complejidad, y un LLM también la calcula independientemente, para:
- Ver concordancia entre ambos análisis
- Analizar divergencias
- Validar resultados

**Ejemplo:**
```
Sistema → O(n²)
LLM → O(n²)
✅ Concordancia verificada
```

#### 3. 🎓 **Generación de Dataset de Entrenamiento**
Entrenar un pequeño modelo de clasificación de estructuras algorítmicas, usando ejemplos generados por GPT.

**Proceso sugerido:**
```
1. LLM genera ejemplos de algoritmos con complejidad conocida
2. Se etiquetan por patrón (búsqueda, ordenamiento, recursión, etc.)
3. Se entrena modelo clasificador
4. Se usa para pre-clasificar nuevos algoritmos
```

### ⭐ Crédito Adicional

> **Nota:** Las propuestas anteriores **no son obligatorias**, pero podrían dar **crédito adicional** si se implementan de forma efectiva.

---

## 🛠️ Tecnologías Sugeridas

### Backend
- Python (análisis de AST, complejidad)
- APIs de LLM (OpenAI, Anthropic, Google)

### Frontend (opcional)
- Web interface para input de pseudocódigo
- Visualización de diagramas de ejecución

### Herramientas de Análisis
- Parsers (PLY, ANTLR, o custom)
- Generación de AST
- Análisis simbólico

---

## 📚 Recursos Adicionales

### Documentación del Proyecto
- [Gramática Formal](Backend/data/gramatica.md) - Especificación completa del pseudocódigo
- [Elementos Léxicos](Backend/data/gramatica/1-lexica.md) - Tokens y operadores
- [Validación](Backend/data/gramatica/8-validacion.md) - Criterios de corrección

### Referencias Teóricas Recomendadas
- "Introduction to Algorithms" (CLRS)
- "The Art of Computer Programming" (Knuth)
- "Algorithm Design" (Kleinberg & Tardos)

---

## 👥 Equipo de Desarrollo

- **Modalidad:** Parejas de estudiantes
- **Curso:** Análisis y Diseño de Algoritmos
- **Semestre:** 10

---

## 📞 Contacto y Soporte

Para dudas sobre el proyecto:
1. Consultar la documentación técnica en `Backend/data/gramatica/`
2. Revisar ejemplos de algoritmos de prueba
3. Contactar al docente del curso

---

## 📅 Cronograma (Sugerido)

| Fase | Actividad | Tiempo Estimado |
|------|-----------|-----------------|
| 1️⃣ | Diseño de gramática y parser | 2 semanas |
| 2️⃣ | Implementación del analizador de complejidad | 3 semanas |
| 3️⃣ | Integración con LLM | 2 semanas |
| 4️⃣ | Generación de diagramas y documentación | 1 semana |
| 5️⃣ | Pruebas y validación | 1 semana |
| 6️⃣ | Informe final y presentación | 1 semana |

**Total:** ~10 semanas

---

## ✅ Checklist de Entrega

Antes de entregar, verificar que se cumple con:

- [ ] Código fuente documentado y modularizado
- [ ] Informe técnico completo
- [ ] Análisis de complejidad del propio analizador
- [ ] Mínimo 10 casos de prueba funcionando
- [ ] Diagramas de seguimiento implementados
- [ ] Material audiovisual/presentación
- [ ] Integración funcional con LLM
- [ ] README actualizado con instrucciones de uso

---

## 📜 Licencia

Este proyecto es parte de un trabajo académico para el curso de **Análisis y Diseño de Algoritmos**.

---

**Universidad:** [Nombre de la Universidad]
**Facultad:** Ingeniería
**Programa:** Ingeniería de Sistemas / Ciencias de la Computación
**Año:** 2025

---

> **"El análisis de algoritmos es el arte de medir la eficiencia antes de que el código corra."**

---

## 🔗 Enlaces Útiles

- [Especificación de Gramática Completa](Backend/data/gramatica.md)
- [Guía de Validación](Backend/data/gramatica/8-validacion.md)
- [Ejemplos de Algoritmos](Backend/data/ejemplos/)

---

**Última actualización:** Enero 2025
**Versión:** 1.0
