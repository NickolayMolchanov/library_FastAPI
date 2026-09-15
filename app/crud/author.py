from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author import Author
from app.schemas.author import SAuthorCreate


async def create_author(
    session: AsyncSession,
    author_data: SAuthorCreate,
) -> Author:
    author = Author(
        name=author_data.name,
        biography=author_data.biography,
        birthdate=author_data.birthdate,
    )

    session.add(author)
    await session.commit()
    await session.refresh(author)

    return author


async def get_authors(
    session: AsyncSession,
    birthdate: str | None = None,
    search: str |None = None,
    page: int = 1,
    limit: int = 10,
) -> dict:

    query = select(Author)
    count_query = select(func.count(func.distinct(Author.id)))

    #Фильтры
    filters = []
    joins = []

    if birthdate is not None:
        filters.append(Author.birthdate == birthdate)

    if search is not None:
        filters.append(Author.name.ilike(f'%{search}%'))

    query = query.where(*filters)
    count_query = query.where(*filters)


    count_result = await session.execute(count_query)
    total = count_result.scalar_one()


    #Пагинация
    offset = (page - 1) * limit
    query = query.offset(offset).limit(limit)

    result = await session.execute(query)

    authors = list(result.scalars().all())

    return {
        "authors": authors,
        "total": total,
        "page": page,
        "limit": limit
    }


async def get_author_by_id(
    session: AsyncSession,
    author_id: int,
) -> Author | None:
    stmt = select(Author).where(Author.id == author_id)
    result = await session.execute(stmt)
    return result.scalar_one_or_none()


async def upd_author(
    session: AsyncSession,
    author_id: int,
    author_data: SAuthorCreate,
) -> Author | None:
    stmt = select(Author).where(Author.id == author_id)
    result = await session.execute(stmt)

    author = result.scalar_one_or_none()

    if author is None:
        return None

    author.name = author_data.name
    author.biography = author_data.biography
    author.birthdate = author_data.birthdate

    await session.commit()
    await session.refresh(author)

    return author


async def delete_author(
    session: AsyncSession,
    author: Author,
) -> None:
    await session.delete(author)
    await session.commit()