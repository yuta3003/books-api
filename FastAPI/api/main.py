"""
FastAPI アプリケーションのエントリポイント。

著者と書籍のルーターを登録してアプリケーションを構成する。
"""

from fastapi import FastAPI

from api.routers import author, book

app = FastAPI()

app.include_router(author.router)
app.include_router(book.router)
