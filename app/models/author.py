from datetime import datetime
from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import mapped_column, Mapped, relationship

from app.database import Base
from app.models.associations import association_table

class Author(Base):
    __tablename__ = 'authors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    biography: Mapped[Optional[str]] = mapped_column(String(200))
    birthdate: Mapped[Optional[datetime]] = mapped_column(String(200))

    books: Mapped[List["Book"]] = relationship(
        secondary=association_table,
        back_populates="authors",
    )