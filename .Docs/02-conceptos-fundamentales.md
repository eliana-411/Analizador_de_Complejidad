# 2. CONCEPTOS FUNDAMENTALES

### 2.1 Definiciones

#### 🤖 Agente
**¿Qué es?**
Un LLM equipado con tools que busca cumplir un objetivo específico.

**Características:**
- **NO** tiene pasos procedurales en sus instrucciones
- **SÍ** tiene un objetivo claro
- **SÍ** tiene acceso a tools que simplifican su razonamiento
- Toma decisiones basándose en el contexto y su capacidad de razonamiento

**Ejemplo:**
*Agente Validador* tiene como objetivo validar el pseudocódigo según la gramática. No tiene instrucciones de "primero haz X, luego Y", sino "valida este código y corrígelo si es necesario".

---

#### 🔄 Workflow
**¿Qué es?**
Orquestador determinista que guía a los agentes por una secuencia de pasos.

**Características:**
- Define la secuencia de ejecución
- Maneja decisiones condicionales (branching)
- Pasa estado entre agentes
- **ES** determinista (mismo input → mismo flujo)

**Ejemplo:**
*Workflow de Análisis* define: Validar → Clasificar → Analizar → Resolver → Reportar

---

#### 🛠️ Tool
**¿Qué es?**
Función o librería que simplifica el trabajo del agente.

**Características:**
- Tiene input y output bien definidos
- Resuelve un problema específico
- Reduce la carga cognitiva del agente
- Puede ser una librería externa (SymPy, Lark) o función custom

**Ejemplo:**
*Lark Parser* es una tool que convierte pseudocódigo en AST, liberando al agente de hacer parsing manual.

---

#### 📊 Estado
**¿Qué es?**
Información compartida entre todos los pasos del workflow.

**Características:**
- Tipado con Pydantic/TypedDict
- Mutable (se actualiza en cada paso)
- Persiste en memoria durante ejecución
- Opcionalmente se guarda en SQLite
