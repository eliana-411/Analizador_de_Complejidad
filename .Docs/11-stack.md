# 11. STACK TECNOLÓGICO

## 11.1 Decisiones Justificadas

| Componente | Tecnología | Justificación | Alternativas Descartadas |
|------------|------------|---------------|--------------------------|
| **Orquestación** | LangGraph | Control determinista, estado tipado, rollback | AutoGen (menos maduro), CrewAI (menos control) |
| **LLM Principal** | Anthropic Claude 4.5 | Mejor razonamiento matemático, 200k context | GPT-4 (más caro), Llama (menos preciso) |
| **API Framework** | FastAPI | Async nativo, docs auto, typing | Flask (sin async), Django (overkill) |
| **Validación** | Pydantic | Typing nativo, integración FastAPI | Marshmallow (menos integrado) |
| **Parser** | Lark (si necesario) | BNF directo, ligero | ANTLR (overkill), PLY (bajo nivel) |
| **Álgebra Simbólica** | SymPy | Nativo Python, gratis, completo | SageMath (pesado), Wolfram (pago) |
| **Persistencia** | SQLite | Ligero, sin servidor, suficiente | PostgreSQL (overkill), Redis (no relacional) |
| **Monitoring** | LangSmith | Decisión previa del usuario | Prometheus (innecesario según usuario) |
| **Diagramas** | Mermaid | Texto plano, fácil generar | PlantUML (requiere Java), Graphviz (más complejo) |

## 11.2 Requirements Core

```
# Core Framework
langgraph>=0.2.28
langchain>=0.3.0
langchain-anthropic>=0.2.0
pydantic>=2.9.0
# API
fastapi>=0.115.0
uvicorn[standard]>=0.32.0
# Parsing (opcional, si se usa)
lark>=1.2.0
# Matemáticas
sympy>=1.13.0
# Base de datos
sqlalchemy>=2.0.0
aiosqlite>=0.20.0
# Utilidades
python-dotenv>=1.0.0
httpx>=0.27.0
```
