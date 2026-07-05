# Base Contracts

Package ini mendefinisikan Domain-Driven Design (DDD) primitives yang menjadi fondasi bagi seluruh kontrak dalam AetherOS.

## Aturan
- **Wajib Ada:** Definisi abstract base classes untuk struktur DDD (Entity, ValueObject, Aggregate).
- **Tidak Boleh Ada:** Logika spesifik bisnis, referensi ke package lain di luar `base`, dependensi eksternal selain `pydantic`, `uuid`, dan standard library Python.
- **Dependensi yang Diizinkan:** Standard Library.

## Contoh Penggunaan
```python
from core.contracts.base import Entity, ValueObject

class Capability(ValueObject):
    name: str
```
