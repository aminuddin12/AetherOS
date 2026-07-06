from enum import Enum


class ServiceScope(Enum):
    SINGLETON = "singleton"
    TRANSIENT = "transient"
