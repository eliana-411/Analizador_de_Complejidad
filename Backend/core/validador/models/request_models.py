from pydantic import BaseModel, Field, field_validator


class ValidationRequest(BaseModel):
    """Request model para validación de pseudocódigo"""

    pseudocodigo: str = Field(..., min_length=1, max_length=50000)
    return_suggestions: bool = True

    @field_validator("pseudocodigo")
    @classmethod
    def sanitize_input(cls, v: str) -> str:
        """
        Sanitizar input del usuario.
        NEVER trust user input - validar y limpiar.
        """
        if not v or not v.strip():
            raise ValueError("Pseudocódigo no puede estar vacío")

        # Normalizar espacios pero no modificar el contenido
        return v.strip()
