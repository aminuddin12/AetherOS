from pydantic import Field
from ..base import ValueObject

class Recommendation(ValueObject):
    """
    Saran tindakan berdasarkan metrik atau pola.
    """
    context: str = Field(..., description="Situation triggering recommendation")
    suggested_action: str = Field(..., description="What should be done")
    expected_benefit: str = Field(..., description="Why it should be done")
