from fastapi import APIRouter, Body, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.book import create_book
from app.database import get_db
from app.schemas.book import SBookCreate

router = APIRouter(
    prefix="/books",
    tags=["books"],
)

@router.post("/")
async def create_new_book(
    title: str = Body(...),
    description: str | None = Body(None),
    session: AsyncSession = Depends(get_db()),
):
    book_data = SBookCreate(title=title, description=description)
    new_book = await create_book(session, book_data)
    return new_book