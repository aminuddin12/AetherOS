from enum import StrEnum
from typing import Any
from pydantic import Field
from ..base import ValueObject


class ResultStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    PARTIAL = "partial"


class ExecutionResult(ValueObject):
    """
    Keluaran dari suatu task atau aksi.
    """

    status: ResultStatus = Field(..., description="Outcome of the execution")
    summary: str = Field(..., description="Brief outcome description")
    output_data: Any = Field(default=None, description="Artifacts or structured results")
