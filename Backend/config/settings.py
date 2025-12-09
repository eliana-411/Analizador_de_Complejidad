from typing import Optional
from pathlib import Path

from pydantic_settings import BaseSettings

# Obtener la ruta del directorio Backend
# [ ] BACKEND_DIR = Path(__file__).parent.parent
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    """
    Configuración centralizada del sistema.
    Lee las variables de entorno desde el archivo .env
    """

    # API Keys
    anthropic_api_key: Optional[str] = None

    # Model Configuration
    model_name: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096
    temperature: float = 0.0

    # LangSmith (opcional - para monitoring)
    langsmith_api_key: Optional[str] = None
    langsmith_project: str = "complexity-analyzer"

    class Config:
        # Buscar .env en la raíz del proyecto (un nivel arriba de Backend/)
        # Buscar .env en el directorio Backend/
        env_file = PROJECT_ROOT / ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()
