"""
Book CRUD Operations Module.

This module provides functions for performing CRUD (Create, Read, Delete) operations on the 'books' table.

Functions:
    - create_book: Create a new book in the database.
    - get_books: Retrieve a list of all books from the database.
    - get_book_by_id: Retrieve a book by its ID from the database.
    - delete_book: Delete an existing book from the database.

Usage:
    - Import the functions as needed.
    - Use these functions to interact with the 'books' table in the database.

Example:
    from api.cruds.book import create_book, get_books, get_book_by_id, delete_book
    from api.schemas.book import BookCreate
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession() as session:
        # Create a new book
        new_book_data = BookCreate(title="人間失格", author_id="550e8400-e29b-41d4-a716-446655440000")
        created_book = await create_book(session, book_create=new_book_data)

        # Get all books
        books_list = await get_books(session)

        # Get book by ID
        book_by_id = await get_book_by_id(session, book_id=created_book.id)

        # Delete book
        await delete_book(session, original=book_by_id)
"""
from typing import List, Optional, Tuple

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.book as book_schema
from api.exceptions import IntegrityViolationError
from api.models import model


async def create_book(
    db: AsyncSession, book_create: book_schema.BookCreate
) -> model.Book:
    """
    Create a new book in the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        book_create (book_schema.BookCreate): Book data for creation.

    Returns:
        model.Book: Created book data.

    Raises:
        IntegrityViolationError: If database integrity constraint is violated (e.g., invalid author_id).
    """
    try:
        book = model.Book(**book_create.model_dump())
        db.add(book)
        await db.commit()
        await db.refresh(book)
        return book
    except IntegrityError as e:
        await db.rollback()
        raise IntegrityViolationError from e


async def get_books(db: AsyncSession) -> List[model.Book]:
    """
    Retrieve a list of all books from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        List[model.Book]: List of all books.
    """
    result: Result = await db.execute(
        select(model.Book).order_by(model.Book.title)
    )
    return result.scalars().all()


async def get_book_by_id(db: AsyncSession, book_id: str) -> Optional[model.Book]:
    """
    Retrieve a book by its ID from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        book_id (str): ID of the book to retrieve (UUID).

    Returns:
        Optional[model.Book]: Book data if found, otherwise None.
    """
    result: Result = await db.execute(
        select(model.Book).filter(model.Book.id == book_id)
    )
    book: Optional[Tuple[model.Book]] = result.first()
    return book[0] if book else None


async def delete_book(db: AsyncSession, original: model.Book) -> None:
    """
    Delete an existing book from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        original (model.Book): Book data to be deleted.

    Returns:
        None
    """
    await db.delete(original)
    await db.commit()
