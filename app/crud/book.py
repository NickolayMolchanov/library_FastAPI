from fastapi import HTTPException
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.author import Author
from app.models.book import Book
from app.schemas.book import SBookCreate


async def create_book(
    session: AsyncSession,
    book_data: SBookCreate,
) -> Book:
    result = await session.execute(
        select(Author).where(
            Author.id.in_(book_data.author_ids)
        )
    )

    authors = list(result.scalars().all())

    if len(authors) != len(book_data.author_ids):
        raise HTTPException(
            status_code=404,
            detail="One or more authors not found"
        )

    new_book = Book(
        title=book_data.title,
        description=book_data.description,
        authors=authors,
        year=book_data.year,
    )

    if authors is None:
        raise HTTPException(
            status_code=404,
            detail="No author found",
        )

    session.add(new_book)
    await session.commit()
    await session.refresh(new_book)
    return new_book


async def get_books(
    session: AsyncSession,
    year: int | None = None,
    author_id: int | None = None,
    search: str | None = None,
    sort: str | None = None,
    page: int = 1,
    limit: int = 10,
) -> dict:

    query = select(Book)
    count_query = select(func.count(func.distinct(Book.id)))

    # Фильтры
    filters = []
    joins = []

    if year is not None:
        filters.append(Book.year == year)

    if search is not None:
        filters.append(Book.title.ilike(f"%{search}%"))

    if author_id is not None:
        joins.append(Book.authors)
        filters.append(Author.id == author_id)

    query = query.where(*filters)
    count_query = count_query.where(*filters)

    for join in joins:
        query = query.join(join)
        count_query = count_query.join(join)

    #Сортировка
    if sort is not None:
        if sort == "year":
            query = query.order_by(Book.year)
        elif sort == "-year":
            query = query.order_by(Book.year.desc())
        else:
            raise HTTPException(
                status_code=404,
                detail="Sort query must be either year or -year"
            )

    count_result = await session.execute(count_query)
    total = count_result.scalar_one()

    #Пагинация
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    result = await session.execute(query)

    books = list(result.scalars().all())

    return {
        "books": books,
        "total": total,
        "page": page,
        "limit": limit,
    }


async def get_book_by_id(
    session: AsyncSession,
    book_id: int,
) -> Book | None:
    stmt = select(Book).where(Book.id == book_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def upd_book(
    session: AsyncSession,
    book_id: int,
    book_data: SBookCreate,
):
    result = await session.execute(
        select(Book)
        .options(selectinload(Book.authors))
        .where(Book.id == book_id)
    )

    book = result.scalar_one_or_none()

    if book is None:
        return None

    book.title = book_data.title
    book.description = book_data.description

    if book_data.author_ids is not None:
        authors_result = await session.execute(
            select(Author).where(Author.id.in_(book_data.author_ids))
        )

        authors = authors_result.scalars().all()

        if len(authors) != len(book_data.author_ids):
            raise HTTPException(
                status_code=404,
                detail="One or more authors not found"
            )

        book.authors = authors

    await session.commit()
    await session.refresh(book)

    return book


async def delete_book(
    session: AsyncSession,
    book_id: int,
):
    result = await session.execute(
        select(Book).where(Book.id == book_id)
    )

    book = result.scalar_one_or_none()

    if book is None:
        return None

    await session.delete(book)
    await session.commit()

    return book


