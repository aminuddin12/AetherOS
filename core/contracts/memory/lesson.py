from pydantic import Field
from ..base import Entity


class LessonLearned(Entity):
    """
    Catatan dari kegagalan masa lalu agar tidak diulangi (Organizational Intelligence).
    """

    incident_description: str = Field(..., description="What went wrong")
    root_cause: str = Field(..., description="Why it went wrong")
    resolution: str = Field(..., description="How it was fixed")
    prevention: str = Field(..., description="How to prevent in the future")
