from typing import List, Sequence
from pydantic import Field, PrivateAttr
from .entity import Entity
from .event import DomainEvent


class AggregateRoot(Entity):
    """
    Aggregate Root adalah pintu masuk utama (transaction boundary).
    Mendukung Domain Events mutation secara internal,
    sementara akses dari luar tetap immutable.
    """

    # Internal list of domain events.
    # PrivateAttr allows mutation inside the class despite frozen=True.
    _domain_events: List[DomainEvent] = PrivateAttr(default_factory=list)

    def raise_domain_event(self, event: DomainEvent) -> None:
        """
        Mencatat event domain yang terjadi di dalam boundary aggregate ini.
        """
        self._domain_events.append(event)

    def clear_events(self) -> None:
        """
        Membersihkan event setelah di-commit/dipublish ke Event Bus.
        """
        self._domain_events.clear()

    def get_events(self) -> Sequence[DomainEvent]:
        """
        Mengembalikan sequence immutable (tuple) dari event.
        """
        return tuple(self._domain_events)
