"""
Aplicación FastAPI principal del Analizador de Complejidad
============================================================

Integra todos los routers y configura la aplicación web.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging

from core.analizador.router import router as analizador_router
from core.validador.router import router as validador_router

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Crear aplicación FastAPI
app = FastAPI(
    title="Analizador de Complejidad Algorítmica",
    description="API para análisis de complejidad de algoritmos y validación de pseudocódigo",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción, especificar orígenes permitidos
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar routers
app.include_router(analizador_router)
app.include_router(validador_router)


@app.get("/")
async def root():
    """Endpoint raíz con información de la API"""
    return {
        "message": "Analizador de Complejidad Algorítmica API",
        "version": "1.0.0",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "analisis": "/analisis",
            "validador": "/validador"
        }
    }


@app.get("/health")
async def health_check():
    """Endpoint de salud"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
