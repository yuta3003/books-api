"""
著者 API ルーター。

著者に関する操作の FastAPI ルートを定義する。

クラス:
    - router: 著者操作用の FastAPI APIRouter インスタンス

ルート:
    - GET /authors: 著者一覧取得
    - POST /authors: 著者作成

利用方法:
    - router インスタンスをインポートする
    - FastAPI アプリにルーターを登録する

例:
    from fastapi import FastAPI
    from api.routers import author

    app = FastAPI()
    app.include_router(author.router)

    # これで著者ルートが利用可能になる
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
    著者一覧を取得する。

    Args:
        db (AsyncSession): 非同期 SQLAlchemy セッション

    Returns:
        List[author_schema.AuthorResponse]: 著者一覧

    Raises:
        HTTPException: 処理中にエラーが発生した場合
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
    著者を作成する。

    Args:
        author_body (author_schema.AuthorCreate): 著者作成リクエストボディ
        db (AsyncSession): 非同期 SQLAlchemy セッション

    Returns:
        author_schema.AuthorResponse: 作成された著者データ

    Raises:
        HTTPException: 処理中にエラーが発生した場合
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
