from sqlalchemy import Column, Table, ForeignKey, Integer

from app.database import Base

association_table = Table(
    'association',
    Base.metadata,
    Column('book_id', ForeignKey('books.id'), primary_key=True),
    Column('author_id', ForeignKey('authors.id'), primary_key=True),
)