"""
Book API Router.

This module defines FastAPI routes for managing book-related operations.

Classes:
    - router: FastAPI APIRouter instance for book operations.

Routes:
    - GET /books: List all books.
    - POST /books: Create a new book.
    - DELETE /books/{book_id}: Delete an existing book.

Usage:
    - Import the 'router' instance.
    - Include the router in your FastAPI app.

Example:
    from fastapi import FastAPI
    from api.routers import book

    app = FastAPI()
    app.include_router(book.router)

    # Your FastAPI app now includes the book routes.
"""
from typing import List

import starlette.status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.book as book_crud
import api.schemas.book as book_schema
from api.db import get_db
from api.exceptions import IntegrityViolationError

router = APIRouter()


@router.get("/books", response_model=List[book_schema.BookResponse])
async def list_books(db: AsyncSession = Depends(get_db)):
    """
    Get a list of all books.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        List[book_schema.BookResponse]: List of book data.

    Raises:
        HTTPException: If an error occurs during the operation.
    """
    return await book_crud.get_books(db=db)


@router.post(
    "/books",
    response_model=book_schema.BookResponse,
    status_code=starlette.status.HTTP_201_CREATED,
)
async def create_book(
    book_body: book_schema.BookCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new book.

    Args:
        book_body (book_schema.BookCreate): Request body containing book data.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        book_schema.BookResponse: Created book data.

    Raises:
        HTTPException: If an error occurs during the operation, such as invalid author_id.
    """
    try:
        created_book = await book_crud.create_book(db=db, book_create=book_body)
        return created_book
    except IntegrityViolationError as e:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail="Failed to create book. Please check if the author_id is valid.",
        ) from e


@router.delete("/books/{book_id}", status_code=starlette.status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: str, db: AsyncSession = Depends(get_db)):
    """
    Delete an existing book.

    Args:
        book_id (str): ID of the book to delete (UUID).
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        None

    Raises:
        HTTPException: If the book is not found or an error occurs during the operation.
    """
    book = await book_crud.get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=starlette.status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    await book_crud.delete_book(db=db, original=book)
    return None
