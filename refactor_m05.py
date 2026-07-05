import os

def rewrite_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content.strip() + "\n")

# --- BASE ---
rewrite_file("core/contracts/base/__init__.py", """
from .contract import BaseContract
from .reference import ResourceReference
from .value_object import ValueObject
from .entity import Entity
from .aggregate import AggregateRoot
from .event import DomainEvent
from .command import Command
from .query import Query
from .protocol import ContractProtocol

__all__ = [
    "BaseContract",
    "ResourceReference",
    "ValueObject",
    "Entity",
    "AggregateRoot",
    "DomainEvent",
    "Command",
    "Query",
    "ContractProtocol"
]
""")

rewrite_file("core/contracts/base/contract.py", """
from typing import Dict, Any
from pydantic import BaseModel, ConfigDict, Field

class BaseContract(BaseModel):
    \"\"\"
    Fondasi paling bawah untuk semua model AetherOS (API Public).
    Menyediakan versioning dan Kubernetes-style metadata.
    \"\"\"
    model_config = ConfigDict(frozen=True, extra="forbid")

    # Versioning
    schema_version: str = Field(default="1.0", description="Schema version of this contract")
    contract_version: str = Field(default="1.0", description="Data contract compatibility version")
    api_version: str = Field(default="v1", description="API route version")
    spec_version: str = Field(default="1.0", description="Specification/Behavioral version")

    # Metadata
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Generic metadata")
    labels: Dict[str, str] = Field(default_factory=dict, description="Identifying labels (e.g., tier: backend)")
    annotations: Dict[str, str] = Field(default_factory=dict, description="Non-identifying metadata")
    tags: list[str] = Field(default_factory=list, description="Categorization tags")
    extensions: Dict[str, Any] = Field(default_factory=dict, description="Plugin specific extensions")
    
    # Ownership
    owner: str | None = Field(default=None, description="Resource owner reference")
    created_by: str | None = Field(default=None, description="Who created this resource")
    managed_by: str = Field(default="aether-kernel", description="Controller managing this resource")
""")

rewrite_file("core/contracts/base/value_object.py", """
from pydantic import BaseModel, ConfigDict

class ValueObject(BaseModel):
    \"\"\"
    Base class untuk semua Value Objects.
    Value Objects mendefinisikan objek berdasarkan atributnya, bukan identitasnya.
    Oleh karena itu bersifat immutable. (Tidak mewarisi BaseContract agar tetap ringan).
    \"\"\"
    model_config = ConfigDict(frozen=True, extra="forbid")
""")

rewrite_file("core/contracts/base/reference.py", """
from pydantic import Field
from typing import Dict
from .value_object import ValueObject

class ResourceReference(ValueObject):
    \"\"\"
    Pointers ke resource lain untuk mencegah deep object graph.
    Sangat cocok untuk Event Sourcing dan penyimpanan relasional.
    \"\"\"
    id: str = Field(..., description="Unique ID of the referenced resource")
    kind: str = Field(..., description="Type of the resource (e.g., 'Worker', 'Task')")
    namespace: str = Field(default="default", description="Resource namespace")
    name: str | None = Field(default=None, description="Human readable name")
    version: str | None = Field(default=None, description="Specific version if applicable")
    labels: Dict[str, str] = Field(default_factory=dict, description="Cached labels for fast filtering")
""")

rewrite_file("core/contracts/base/entity.py", """
from pydantic import Field
from uuid import UUID, uuid4
from datetime import datetime, UTC
from .contract import BaseContract

class Entity(BaseContract):
    \"\"\"
    Base class untuk entitas domain yang memiliki identitas unik (ID) dan lifecycle.
    Mewarisi BaseContract sehingga memiliki full metadata & versioning.
    \"\"\"
    id: UUID = Field(default_factory=uuid4, description="Global unique identifier for this entity")
    namespace: str = Field(default="default", description="Namespace isolating this entity")
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC), description="Creation timestamp")
    updated_at: datetime | None = Field(default=None, description="Last modification timestamp")
""")

rewrite_file("core/contracts/base/aggregate.py", """
from typing import List, Sequence
from pydantic import Field, PrivateAttr
from .entity import Entity
from .event import DomainEvent

class AggregateRoot(Entity):
    \"\"\"
    Aggregate Root adalah pintu masuk utama (transaction boundary).
    Mendukung Domain Events mutation secara internal,
    sementara akses dari luar tetap immutable.
    \"\"\"
    
    # Internal list of domain events. 
    # PrivateAttr allows mutation inside the class despite frozen=True.
    _domain_events: List[DomainEvent] = PrivateAttr(default_factory=list)

    def raise_domain_event(self, event: DomainEvent) -> None:
        \"\"\"
        Mencatat event domain yang terjadi di dalam boundary aggregate ini.
        \"\"\"
        self._domain_events.append(event)

    def clear_events(self) -> None:
        \"\"\"
        Membersihkan event setelah di-commit/dipublish ke Event Bus.
        \"\"\"
        self._domain_events.clear()

    def get_events(self) -> Sequence[DomainEvent]:
        \"\"\"
        Mengembalikan sequence immutable (tuple) dari event.
        \"\"\"
        return tuple(self._domain_events)
""")

# --- TASK ---
rewrite_file("core/contracts/task/task.py", """
from enum import StrEnum
from typing import List
from pydantic import Field
from ..base import AggregateRoot, ResourceReference

class TaskStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    BLOCKED = "blocked"
    IN_REVIEW = "in_review"
    COMPLETED = "completed"
    FAILED = "failed"

class Task(AggregateRoot):
    \"\"\"
    Unit kerja terdiskrit (seperti tiket JIRA) di dalam organisasi.
    \"\"\"
    title: str = Field(..., description="Task title")
    description: str = Field(..., description="Detailed instructions")
    status: TaskStatus = Field(default=TaskStatus.PENDING, description="Current execution status")
    creator_ref: ResourceReference = Field(..., description="Reference to who created the task (Principal/User)")
    dependencies: List[ResourceReference] = Field(default_factory=list, description="References to blocking tasks")
""")

rewrite_file("core/contracts/task/assignment.py", """
from pydantic import Field
from ..base import ValueObject, ResourceReference

class Assignment(ValueObject):
    \"\"\"
    Penugasan sebuah Task kepada seorang Worker.
    \"\"\"
    task_ref: ResourceReference = Field(..., description="The task to execute")
    worker_ref: ResourceReference = Field(..., description="The assigned agent")
    is_active: bool = Field(default=True, description="Whether this assignment is current")
""")

rewrite_file("core/contracts/task/approval.py", """
from enum import StrEnum
from pydantic import Field
from ..base import ValueObject, ResourceReference

class ApprovalStatus(StrEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Approval(ValueObject):
    \"\"\"
    Gatekeeper (Human-in-the-Loop) persetujuan aksi kritis.
    \"\"\"
    required_role: str = Field(..., description="Role required to approve")
    status: ApprovalStatus = Field(default=ApprovalStatus.PENDING)
    approved_by_ref: ResourceReference | None = Field(default=None, description="Who approved it")
""")

# --- WORKER ---
rewrite_file("core/contracts/worker/worker.py", """
from pydantic import Field
from ..base import AggregateRoot, ResourceReference
from .role import Role
from .capability_profile import CapabilityProfile
from .reputation import ReputationScore
from .lifecycle import WorkerLifecycle

class Worker(AggregateRoot):
    \"\"\"
    Entitas utama (Aggregate) yang mewakili satu Agent di AetherOS.
    \"\"\"
    principal_ref: ResourceReference = Field(..., description="Identity mapped to this worker")
    role: Role = Field(..., description="Assigned role (persona)")
    profile: CapabilityProfile = Field(default_factory=CapabilityProfile, description="Capabilities & Skills")
    reputation: ReputationScore = Field(default_factory=ReputationScore, description="Performance metrics")
    lifecycle: WorkerLifecycle = Field(default_factory=WorkerLifecycle, description="Current state")
""")

rewrite_file("core/contracts/worker/capability_profile.py", """
from typing import List
from enum import StrEnum
from pydantic import Field
from ..base import ValueObject, Entity

class ProficiencyLevel(StrEnum):
    BEGINNER = "beginner"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class Capability(Entity):
    \"\"\"
    Kemampuan/Skill absolut yang immutable (mis: 'Python', 'Vue3').
    \"\"\"
    name: str = Field(..., description="Skill name")
    category: str = Field(default="general", description="Skill category")

class CapabilityRecord(ValueObject):
    \"\"\"
    Rekaman penguasaan suatu skill oleh agent tertentu (Mutable state).
    \"\"\"
    skill: Capability = Field(..., description="The immutable skill")
    level: ProficiencyLevel = Field(default=ProficiencyLevel.BEGINNER)
    confidence: float = Field(default=0.5, description="Confidence score (0.0 to 1.0)")
    version: str | None = Field(default=None, description="Specific tool/skill version (e.g. '3.12')")

class CapabilityProfile(ValueObject):
    \"\"\"
    Kumpulan rekaman kemampuan agen.
    \"\"\"
    records: List[CapabilityRecord] = Field(default_factory=list)
""")

# --- WORKSPACE ---
rewrite_file("core/contracts/workspace/deployment.py", """
from enum import StrEnum
from pydantic import Field
from ..base import DomainEvent, ResourceReference

class DeploymentStatus(StrEnum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    SUCCESS = "success"
    FAILED = "failed"
    ROLLED_BACK = "rolled_back"

class Deployment(DomainEvent):
    \"\"\"
    Catatan pengiriman kode/artefak ke environment.
    \"\"\"
    environment_ref: ResourceReference = Field(..., description="Target environment")
    commit_ref: ResourceReference = Field(..., description="What was deployed")
    status: DeploymentStatus = Field(default=DeploymentStatus.PENDING)
""")

# --- PLUGIN ---
rewrite_file("core/contracts/plugin/extension.py", """
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
    \"\"\"
    Representasi dari komponen (apa pun jenisnya) yang diekspor oleh Plugin.
    \"\"\"
    name: str = Field(..., description="Extension name")
    type: ExtensionType = Field(..., description="Type of extension")
    entrypoint: str = Field(..., description="Python module path or reference")
""")

rewrite_file("core/contracts/plugin/extension_manifest.py", """
from typing import List, Dict
from pydantic import Field
from ..base import ValueObject
from .extension import Extension

class ExtensionManifest(ValueObject):
    \"\"\"
    Deklarasi paket (Plugin/Distribution) yang mendaftarkan sekumpulan Extension.
    Memiliki mekanisme dependency management untuk Marketplace.
    \"\"\"
    pack_name: str = Field(..., description="E.g., 'CyberSecurityPack'")
    version: str = Field(..., description="SemVer version")
    author: str = Field(..., description="Vendor/Author name")
    
    # Metadata Ekstensi
    dependencies: Dict[str, str] = Field(default_factory=dict, description="Required plugins and versions")
    conflicts: List[str] = Field(default_factory=list, description="Plugins that cannot run together with this")
    compatibility: List[str] = Field(default_factory=list, description="Supported AetherOS components")
    minimum_kernel_version: str = Field(default="1.0.0", description="Minimum AetherOS version required")

    extensions: List[Extension] = Field(default_factory=list, description="Provided components")
""")

print("Milestone 0.5 Refactor Complete.")
