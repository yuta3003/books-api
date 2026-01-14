"""
Author API Router.

This module defines FastAPI routes for managing author-related operations.

Classes:
    - router: FastAPI APIRouter instance for author operations.

Routes:
    - GET /authors: List all authors.
    - POST /authors: Create a new author.

Usage:
    - Import the 'router' instance.
    - Include the router in your FastAPI app.

Example:
    from fastapi import FastAPI
    from api.routers import author

    app = FastAPI()
    app.include_router(author.router)

    # Your FastAPI app now includes the author routes.
"""
from typing import List

import starlette.status
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

import api.cruds.author as author_crud
import api.schemas.author as author_schema
from api.db import get_db
from api.exceptions import IntegrityViolationError

router = APIRouter()


@router.get("/authors", response_model=List[author_schema.AuthorResponse])
async def list_authors(db: AsyncSession = Depends(get_db)):
    """
    Get a list of all authors.

    Args:
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        List[author_schema.AuthorResponse]: List of author data.

    Raises:
        HTTPException: If an error occurs during the operation.
    """
    return await author_crud.get_authors(db=db)


@router.post(
    "/authors",
    response_model=author_schema.AuthorResponse,
    status_code=starlette.status.HTTP_201_CREATED,
)
async def create_author(
    author_body: author_schema.AuthorCreate, db: AsyncSession = Depends(get_db)
):
    """
    Create a new author.

    Args:
        author_body (author_schema.AuthorCreate): Request body containing author data.
        db (AsyncSession): AsyncSQLAlchemy session.

    Returns:
        author_schema.AuthorResponse: Created author data.

    Raises:
        HTTPException: If an error occurs during the operation.
    """
    try:
        created_author = await author_crud.create_author(
            db=db, author_create=author_body
        )
        return created_author
    except IntegrityViolationError as e:
        raise HTTPException(
            status_code=starlette.status.HTTP_400_BAD_REQUEST,
            detail="Failed to create author",
        ) from e
