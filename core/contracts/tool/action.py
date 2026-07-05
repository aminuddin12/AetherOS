from typing import Dict, Any
from pydantic import Field
from ..base import Command

class Action(Command):
    """
    Niat (Intent) eksekusi spesifik oleh agen yang memanggil sebuah Tool.
    """
    tool_id: str = Field(..., description="Reference to the Tool entity")
    arguments: Dict[str, Any] = Field(..., description="Arguments provided by LLM")
