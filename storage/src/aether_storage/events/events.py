from pydantic import BaseModel
from typing import Dict, Any

class StorageEvent(BaseModel):
    id: str
    type: str
    payload: Dict[str, Any]

class StorageMounted(StorageEvent): type: str = "StorageMounted"
class StorageUnmounted(StorageEvent): type: str = "StorageUnmounted"
class ResourceCreated(StorageEvent): type: str = "ResourceCreated"
class ResourceDeleted(StorageEvent): type: str = "ResourceDeleted"
class ResourceUpdated(StorageEvent): type: str = "ResourceUpdated"
class HandleOpened(StorageEvent): type: str = "HandleOpened"
class HandleClosed(StorageEvent): type: str = "HandleClosed"
class TransactionStarted(StorageEvent): type: str = "TransactionStarted"
class TransactionCommitted(StorageEvent): type: str = "TransactionCommitted"
class LeaseExpired(StorageEvent): type: str = "LeaseExpired"
