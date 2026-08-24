from fastapi import APIRouter, Body, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.book import create_book, get_book_by_id, get_books, upd_book, delete_book
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
    session: AsyncSession = Depends(get_db),
):
    book_data = SBookCreate(title=title, description=description)
    new_book = await create_book(session, book_data)
    return new_book

@router.get("/{book_id}")
async def get_book(book_id: int, session: AsyncSession = Depends(get_db)):
    book = await get_book_by_id(session, book_id)
    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.get("/")
async def get_all_books(session: AsyncSession = Depends(get_db)):
    books = await get_books(session)
    if books is None:
        raise HTTPException(status_code=404, detail="Not a single book")
    return books

@router.put("/{book_id}")
async def update_book(
        book_id: int,
        data: SBookCreate,
        session: AsyncSession = Depends(get_db),
):
    book = await upd_book(
        session=session,
        book_id=book_id,
        data=data,
    )

    if book is None:
        raise HTTPException(status_code=404, detail="Book not found")

    return book

@router.delete("/{book_id}")
async def delete_book_route(
    book_id: int,
    session: AsyncSession = Depends(get_db),
):
    book = await delete_book(
        session=session,
        book_id=book_id,
    )

    if book is None:
        raise HTTPException(
            status_code=404,
            detail="Book not found",
        )

    return {
        "message": "Book deleted successfully"
    }