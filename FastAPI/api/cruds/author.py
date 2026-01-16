"""
著者 CRUD 操作モジュール。

このモジュールは、DB の authors テーブルに対する
非同期 CRUD (作成・取得) 操作を提供する。

関数:
    - create_author: 著者を作成する
    - get_authors: 著者一覧を取得する

利用方法:
    - これらの関数をインポートして authors テーブルを操作する

例:
    from api.cruds.author import create_author, get_authors
    from api.schemas.author import AuthorCreate
    from api.db import get_db

    async with get_db() as db:
        # 著者を作成する
        new_author = AuthorCreate(name="太宰治")
        created_author = await create_author(db, author_create=new_author)

        # 著者一覧を取得する
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
    著者を DB に作成する。

    Args:
        db (AsyncSession): 非同期 SQLAlchemy セッション
        author_create (author_schema.AuthorCreate): 著者作成データ

    Returns:
        model.Author: 作成された著者データ

    Raises:
        IntegrityViolationError: DB の整合性制約に違反した場合
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
    著者一覧を DB から取得する。

    Args:
        db (AsyncSession): 非同期 SQLAlchemy セッション

    Returns:
        List[model.Author]: 著者一覧
    """
    result: Result = await db.execute(
        select(model.Author).order_by(model.Author.name)
    )
    return result.scalars().all()
