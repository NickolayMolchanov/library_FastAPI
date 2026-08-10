from datetime import date
from pydantic import BaseModel, ConfigDict


class SAuthorBase(BaseModel):
    name: str
    biography: str
    birthdate: date

class SAuthorCreate(BaseModel):
    pass

class SAuthor(BaseModel):
    id: int

    model_config = ConfigDict(from_attributes=True)