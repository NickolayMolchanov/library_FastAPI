from datetime import date
from typing import List

from pydantic import BaseModel, ConfigDict


class SAuthorBase(BaseModel):
    name: str
    country: str | None
    biography: str
    birthdate: date

class SAuthorCreate(SAuthorBase):
    pass

class SAuthor(SAuthorBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class SAuthorList(BaseModel):
    authors: List[SAuthor]
    total: int
    page: int
    limit: int