"""
Main FastAPI application module.

This module sets up a FastAPI application and includes routers for author and book.
"""

from fastapi import FastAPI

from api.routers import author, book

app = FastAPI()

app.include_router(author.router)
app.include_router(book.router)
