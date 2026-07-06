from typing import Dict, Any
from pydantic import Field
from ..base import Entity


class Tool(Entity):
    """
    Definisi spesifikasi statis (schema) dari sebuah perkakas.
    Ini yang dikirim ke LLM sebagai instruksi 'function calling'.
    """

    name: str = Field(..., description="Function name")
    description: str = Field(..., description="Function description")
    input_schema: Dict[str, Any] = Field(..., description="JSON Schema for arguments")
