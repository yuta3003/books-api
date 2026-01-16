"""
書籍 CRUD 操作モジュール。

このモジュールは、books テーブルに対する CRUD (作成・取得・削除) 操作を提供する。

関数:
    - create_book: 書籍を作成する
    - get_books: 書籍一覧を取得する
    - get_book_by_id: ID で書籍を取得する
    - delete_book: 書籍を削除する

利用方法:
    - 必要な関数をインポートする
    - books テーブルの操作に利用する

例:
    from api.cruds.book import create_book, get_books, get_book_by_id, delete_book
    from api.schemas.book import BookCreate
    from sqlalchemy.ext.asyncio import AsyncSession

    async with AsyncSession() as session:
        # 書籍を作成する
        new_book_data = BookCreate(title="人間失格", author_id="550e8400-e29b-41d4-a716-446655440000")
        created_book = await create_book(session, book_create=new_book_data)

        # 書籍一覧を取得する
        books_list = await get_books(session)

        # ID で書籍を取得する
        book_by_id = await get_book_by_id(session, book_id=created_book.id)

        # 書籍を削除する
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
    書籍を DB に作成する。

    Args:
        db (AsyncSession): 非同期 SQLAlchemy セッション
        book_create (book_schema.BookCreate): 書籍作成データ

    Returns:
        model.Book: 作成された書籍データ

    Raises:
        IntegrityViolationError: DB の整合性制約に違反した場合 (例: author_id 不正)
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
    書籍一覧を DB から取得する。

    Args:
        db (AsyncSession): 非同期 SQLAlchemy セッション

    Returns:
        List[model.Book]: 書籍一覧
    """
    result: Result = await db.execute(
        select(model.Book).order_by(model.Book.title)
    )
    return result.scalars().all()


async def get_book_by_id(db: AsyncSession, book_id: str) -> Optional[model.Book]:
    """
    ID で書籍を DB から取得する。

    Args:
        db (AsyncSession): 非同期 SQLAlchemy セッション
        book_id (str): 取得する書籍 ID (UUID)

    Returns:
        Optional[model.Book]: 書籍データ (未検出なら None)
    """
    result: Result = await db.execute(
        select(model.Book).filter(model.Book.id == book_id)
    )
    book: Optional[Tuple[model.Book]] = result.first()
    return book[0] if book else None


async def delete_book(db: AsyncSession, original: model.Book) -> None:
    """
    書籍を DB から削除する。

    Args:
        db (AsyncSession): 非同期 SQLAlchemy セッション
        original (model.Book): 削除対象の書籍データ

    Returns:
        なし
    """
    await db.delete(original)
    await db.commit()
