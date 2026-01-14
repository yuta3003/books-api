"""
Author Models Module.

This module defines Pydantic models for representing author-related data structures.

Classes:
    - AuthorBase: Base model for author data.
    - AuthorCreate: Model for creating an author.
    - AuthorResponse: Model representing the response for author data.

Usage:
    - Import the required model classes.
    - Use these models for validating and handling author-related data.

Example:
    from author import AuthorCreate, AuthorResponse

    author_data = {"name": "太宰治"}
    author = AuthorCreate(**author_data)
"""
from pydantic import BaseModel, Field, field_validator


class AuthorBase(BaseModel):
    """
    Base model for author data.
    """

    name: str = Field(..., min_length=1, max_length=50, description="著者名 (最大50文字)")

    @field_validator("name")
    @classmethod
    def name_must_not_be_empty(cls, v: str) -> str:
        """著者名が空白のみでないことを検証"""
        if not v or not v.strip():
            raise ValueError("著者名は必須です")
        return v


class AuthorCreate(AuthorBase):
    """
    Model for creating an author.
    """

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "太宰治",
                }
            ]
        }
    }


class AuthorResponse(AuthorBase):
    """
    Model representing the response for author data.
    """

    id: str = Field(..., description="著者ID (UUID)")

    model_config = {
        "from_attributes": True,
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "太宰治",
                }
            ]
        },
    }
