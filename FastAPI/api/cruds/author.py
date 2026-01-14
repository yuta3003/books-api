"""
Author CRUD Operations Module.

This module defines asynchronous CRUD (Create, Read) operations
for the 'authors' table in the database.

Functions:
    - create_author: Create a new author in the database.
    - get_authors: Retrieve a list of all authors from the database.

Usage:
    - Import the functions and use them to interact with the 'authors' table.

Example:
    from api.cruds.author import create_author, get_authors
    from api.schemas.author import AuthorCreate
    from api.db import get_db

    async with get_db() as db:
        # Create a new author
        new_author = AuthorCreate(name="太宰治")
        created_author = await create_author(db, author_create=new_author)

        # Get all authors
        authors_list = await get_authors(db)
"""
from typing import List

from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

import api.schemas.author as author_schema
from api.exceptions import IntegrityViolationError
from api.models import model


async def create_author(
    db: AsyncSession, author_create: author_schema.AuthorCreate
) -> model.Author:
    """
    Create a new author in the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.
        author_create (author_schema.AuthorCreate): Author creation data.

    Returns:
        model.Author: Created author data.

    Raises:
        IntegrityViolationError: If database integrity constraint is violated.
    """
    try:
        author = model.Author(**author_create.model_dump())
        db.add(author)
        await db.commit()
        await db.refresh(author)
        return author
    except IntegrityError as e:
        await db.rollback()
        raise IntegrityViolationError from e


async def get_authors(db: AsyncSession) -> List[model.Author]:
    """
    Retrieve a list of all authors from the database.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        List[model.Author]: List of all authors.
    """
    result: Result = await db.execute(
        select(model.Author).order_by(model.Author.name)
    )
    return result.scalars().all()
