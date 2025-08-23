from pydantic import BaseModel

class Client(BaseModel):
    id: int
    name: str
    type: str
    status: str
    settings: str | None = None
    visits: int = 0
