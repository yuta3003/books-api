"""
非同期データベースモジュール。

SQLAlchemy の非同期機能を使って DB 接続を管理する。
非同期エンジンとセッションの生成、および DB セッション取得用の関数を提供する。

利用方法:
    - async_engine / async_session / Base をインポートする
    - get_db コルーチンで非同期セッションを取得する

例:
    async with get_db() as session:
        # session を使って DB 操作を行う

注意:
    ASYNC_DB_URL は接続先に合わせて更新すること
"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker

ASYNC_DB_URL = "mysql+aiomysql://root@db:3306/prod?charset=utf8"

async_engine = create_async_engine(ASYNC_DB_URL, echo=True)
async_session = sessionmaker(
    autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)

Base = declarative_base()


async def get_db():
    """
    非同期データベースセッションを取得するコルーチン。

    利用方法:
        async with get_db() as session: でセッションを取得し、
        非同期コンテキスト内で session を使って DB 操作を行う。

    例:
        async with get_db() as session:
            # session を使って DB 操作を行う
    """
    async with async_session() as session:
        yield session
