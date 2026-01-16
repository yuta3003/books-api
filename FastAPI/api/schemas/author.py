"""
著者スキーマモジュール。

著者関連のデータ構造を表す Pydantic モデルを定義する。

クラス:
    - AuthorBase: 著者データの基底モデル
    - AuthorCreate: 著者作成用モデル
    - AuthorResponse: 著者レスポンス用モデル

利用方法:
    - 必要なモデルクラスをインポートする
    - 著者データの検証や取り扱いに利用する

例:
    from author import AuthorCreate, AuthorResponse

    author_data = {"name": "太宰治"}
    author = AuthorCreate(**author_data)
"""
from pydantic import BaseModel, Field, field_validator


class AuthorBase(BaseModel):
    """
    著者データの基底モデル。
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
    著者作成用モデル。
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
    著者レスポンス用モデル。
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
