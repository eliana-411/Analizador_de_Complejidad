from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from core.validador.router import router as validador_router
from core.analizador.router import router as analizador_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)

# Crear app FastAPI
app = FastAPI(
    title="Backend Analizador de Complejidad",
    description="API para validación de pseudocódigo por capas de gramática",
    version="1.0.0",
)

# Configurar CORS para permitir conexiones desde el frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Frontend local
        "http://localhost:3001",
        "http://localhost:3002",
        "http://localhost:3003",
        "http://localhost:3004",
        "http://localhost:5173",  # Vite default port
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "http://127.0.0.1:3002",
        "http://127.0.0.1:3003",
        "http://127.0.0.1:3004",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(validador_router)
app.include_router(analizador_router)


@app.get("/", tags=["root"])
async def root():
    """Root endpoint con información de la API"""
    return {
        "message": "Backend Analizador de Complejidad",
        "version": "1.0.0",
        "endpoints": {
            "validador": "/validador/validar",
            "analisis": "/analisis/analizar",
            "analisis_archivo": "/analisis/analizar-archivo",
            "health_validador": "/validador/health",
            "health_analisis": "/analisis/health",
            "docs": "/docs",
        },
    }


@app.get("/health", tags=["root"])
async def health_check():
    """Global health check endpoint"""
    return {"status": "ok", "service": "backend"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
