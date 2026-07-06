from enum import StrEnum
from pydantic import Field
from ..base import ValueObject


class ExtensionType(StrEnum):
    AGENT = "agent"
    PROVIDER = "provider"
    TOOL = "tool"
    SKILL = "skill"
    WORKFLOW = "workflow"
    DASHBOARD_WIDGET = "dashboard_widget"
    DISTRIBUTION = "distribution"
    CLI = "cli"


class Extension(ValueObject):
    """
    Representasi dari komponen (apa pun jenisnya) yang diekspor oleh Plugin.
    """

    name: str = Field(..., description="Extension name")
    type: ExtensionType = Field(..., description="Type of extension")
    entrypoint: str = Field(..., description="Python module path or reference")
