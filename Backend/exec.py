#!/usr/bin/env python3
"""
Script para iniciar el servidor FastAPI con configuración predeterminada.
Uso: python exec.py
"""
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )
