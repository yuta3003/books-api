"""
書籍 API ルーター。

書籍に関する操作の FastAPI ルートを定義する。

クラス:
    - router: 書籍操作用の FastAPI APIRouter インスタンス

ルート:
    - GET /books: 書籍一覧取得
    - POST /books: 書籍作成
    - DELETE /books/{book_id}: 書籍削除

利用方法:
    - router インスタンスをインポートする
    - FastAPI アプリにルーターを登録する

例:
    from fastapi import FastAPI
    from api.routers import book

    app = FastAPI()
    app.include_router(book.router)

    # これで書籍ルートが利用可能になる
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
    書籍一覧を取得する。

    Args:
        db (AsyncSession): 非同期 SQLAlchemy セッション

    Returns:
        List[book_schema.BookResponse]: 書籍一覧

    Raises:
        HTTPException: 処理中にエラーが発生した場合
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
    書籍を作成する。

    Args:
        book_body (book_schema.BookCreate): 書籍作成リクエストボディ
        db (AsyncSession): 非同期 SQLAlchemy セッション

    Returns:
        book_schema.BookResponse: 作成された書籍データ

    Raises:
        HTTPException: 処理中にエラーが発生した場合 (例: author_id 不正)
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
    書籍を削除する。

    Args:
        book_id (str): 削除対象の書籍 ID (UUID)
        db (AsyncSession): 非同期 SQLAlchemy セッション

    Returns:
        なし

    Raises:
        HTTPException: 書籍が見つからない、または処理中にエラーが発生した場合
    """
    book = await book_crud.get_book_by_id(db=db, book_id=book_id)
    if book is None:
        raise HTTPException(
            status_code=starlette.status.HTTP_404_NOT_FOUND,
            detail="Book not found",
        )
    await book_crud.delete_book(db=db, original=book)
    return None
