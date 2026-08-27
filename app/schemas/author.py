from datetime import datetime
from pydantic import BaseModel, ConfigDict


class SAuthorBase(BaseModel):
    name: str
    biography: str
    birthdate: datetime

class SAuthorCreate(SAuthorBase):
    pass

class SAuthor(SAuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)