from enum import StrEnum
from pydantic import Field
from ..base import ValueObject


class NotificationPriority(StrEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


class Notification(ValueObject):
    """
    Pesan informasi satu arah yang ditujukan kepada manusia (User).
    """

    recipient_id: str = Field(..., description="Identity ID of the recipient")
    title: str = Field(..., description="Notification title")
    body: str = Field(..., description="Detailed message")
    priority: NotificationPriority = Field(
        default=NotificationPriority.NORMAL, description="Urgency level"
    )
    read: bool = Field(default=False, description="Whether it has been read")
