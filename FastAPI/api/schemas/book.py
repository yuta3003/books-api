"""
書籍スキーマモジュール。

書籍関連のデータ構造を表す Pydantic モデルを定義する。

クラス:
    - BookBase: 書籍データの基底モデル
    - BookCreate: 書籍作成用モデル
    - BookResponse: 書籍レスポンス用モデル

利用方法:
    - 必要なモデルクラスをインポートする
    - 書籍データの検証や取り扱いに利用する

例:
    from book import BookCreate, BookResponse

    book_data = {"title": "人間失格", "author_id": "550e8400-e29b-41d4-a716-446655440000"}
    book = BookCreate(**book_data)
"""
from pydantic import BaseModel, Field, field_validator


class BookBase(BaseModel):
    """
    書籍データの基底モデル。
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
    書籍作成用モデル。
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
    書籍レスポンス用モデル。
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
