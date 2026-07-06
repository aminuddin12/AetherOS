from typing import List
from pydantic import Field
from ..base import AggregateRoot
from .message import Message


class Conversation(AggregateRoot):
    """
    Rangkaian pesan obrolan utuh yang memiliki konteks.
    """

    topic: str = Field(..., description="Summary of what the conversation is about")
    messages: List[Message] = Field(
        default_factory=list, description="Chronological list of messages"
    )
    is_active: bool = Field(default=True, description="Whether new messages can be added")
