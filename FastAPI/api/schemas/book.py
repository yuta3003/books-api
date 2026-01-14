"""
Book Models Module.

This module defines Pydantic models for representing book-related data structures.

Classes:
    - BookBase: Base model for book data.
    - BookCreate: Model for creating a book.
    - BookResponse: Model representing the response for book data.

Usage:
    - Import the required model classes.
    - Use these models for validating and handling book-related data.

Example:
    from book import BookCreate, BookResponse

    book_data = {"title": "人間失格", "author_id": "550e8400-e29b-41d4-a716-446655440000"}
    book = BookCreate(**book_data)
"""
from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    """
    Base model for book data.
    """

    title: str = Field(..., min_length=1, max_length=100, description="書籍タイトル (最大100文字)")
    author_id: str = Field(..., description="著者ID (UUID)")

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, v: str) -> str:
        """タイトルが空白のみでないことを検証"""
        if not v or not v.strip():
            raise ValueError("タイトルは必須です")
        return v


class BookCreate(BookBase):
    """
    Model for creating a book.
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "人間失格",
                    "author_id": "550e8400-e29b-41d4-a716-446655440000",
                }
            ]
        }
    }


class BookResponse(BookBase):
    """
    Model representing the response for book data.
    """

    id: str = Field(..., description="書籍ID (UUID)")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "660e8400-e29b-41d4-a716-446655440001",
                    "title": "人間失格",
                    "author_id": "550e8400-e29b-41d4-a716-446655440000",
                }
            ]
        },
    }
