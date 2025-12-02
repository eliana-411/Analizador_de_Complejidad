from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Configuración centralizada del sistema.
    Lee las variables de entorno desde el archivo .env
    """

    # API Keys
    anthropic_api_key: str

    # Model Configuration
    model_name: str = "claude-sonnet-4-5-20250929"
    max_tokens: int = 4096
    temperature: float = 0.0

    # LangSmith (opcional - para monitoring)
    langsmith_api_key: Optional[str] = None
    langsmith_project: str = "complexity-analyzer"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


# Instancia global de configuración
settings = Settings()