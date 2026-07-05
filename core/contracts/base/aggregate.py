from typing import List
from pydantic import Field
from .entity import Entity
from .event import DomainEvent

class AggregateRoot(Entity):
    """
    Aggregate Root adalah pintu masuk utama untuk sekumpulan entitas dan value objects (Aggregate).
    Semua interaksi yang memodifikasi state dalam boundary aggregate harus melalui Aggregate Root.
    """
    
    # Internal list of domain events that occurred within this aggregate
    _domain_events: List[DomainEvent] = Field(default_factory=list, exclude=True, repr=False)
