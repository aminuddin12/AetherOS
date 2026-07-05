from pydantic import Field
from ..base import Entity

class ReviewFeedback(Entity):
    """
    Ulasan kualitas (bisa dari QA Agent, Security Agent, atau Manusia).
    """
    task_id: str = Field(..., description="The task reviewed")
    reviewer_id: str = Field(..., description="Who reviewed it")
    score: float = Field(..., description="Quality score (0.0 to 1.0)")
    comments: str = Field(..., description="Feedback text")

class Review(ReviewFeedback):
    pass
