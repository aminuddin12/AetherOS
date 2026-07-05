from enum import StrEnum
from pydantic import Field
from ..base import ValueObject

class MessageRole(StrEnum):
    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"

class Message(ValueObject):
    """
    Satu gelembung obrolan dalam percakapan (Conversation).
    """
    role: MessageRole = Field(..., description="The role of the message sender")
    content: str = Field(..., description="The textual content of the message")
    name: str | None = Field(default=None, description="Optional name of the sender/tool")
    tool_call_id: str | None = Field(default=None, description="Optional ID if this is a tool response")
