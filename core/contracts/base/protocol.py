from typing import Protocol, runtime_checkable

@runtime_checkable
class ContractProtocol(Protocol):
    """
    Base protocol class untuk antarmuka service/infrastruktur murni
    yang tidak memiliki state data.
    """
    pass
