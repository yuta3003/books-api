"""
api.models.model モジュール

このモジュールは SQLAlchemy を使用してデータベースモデルを定義します。
以下は含まれるクラスの簡単な説明です:

- Author: 著者情報を表すデータベーステーブルのモデルクラス。
- Book: 書籍情報を表すデータベーステーブルのモデルクラス。

これらのクラスはデータベース内の異なるテーブルを表し、それぞれのテーブルに対する関連性も定義されています。
"""
import uuid
from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.mysql import CHAR
from sqlalchemy.orm import relationship

from api.db import Base


class Author(Base):
    """
    著者情報を表すデータベーステーブルのモデルクラスです。

    属性:
        id (str): 著者の一意の識別子 (UUID)。
        name (str): 著者名 (最大50文字)。
        books (relationship): 著者が執筆した書籍との関連性。
    """

    __tablename__ = "authors"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = Column(String(50), nullable=False)

    books = relationship("Book", back_populates="author", cascade="delete")


class Book(Base):
    """
    書籍情報を表すデータベーステーブルのモデルクラスです。

    属性:
        id (str): 書籍の一意の識別子 (UUID)。
        title (str): 書籍タイトル (最大100文字)。
        author_id (str): 著者の識別子 (UUID)。
        author (relationship): 書籍の著者との関連性。
    """

    __tablename__ = "books"

    id = Column(CHAR(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(100), nullable=False)
    author_id = Column(CHAR(36), ForeignKey("authors.id"), nullable=False)

    author = relationship("Author", back_populates="books")
