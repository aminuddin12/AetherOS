from pydantic import BaseModel, ConfigDict

class ValueObject(BaseModel):
    """
    Base class untuk semua Value Objects.
    Value Objects mendefinisikan objek berdasarkan atributnya, bukan identitasnya.
    Oleh karena itu bersifat immutable. (Tidak mewarisi BaseContract agar tetap ringan).
    """
    model_config = ConfigDict(frozen=True, extra="forbid")
