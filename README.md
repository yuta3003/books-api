# Backend API

FastAPI + MySQL を使ったシンプルな書籍/著者管理 API です。

## 構成

- API: FastAPI
- DB: MySQL 8
- 起動: Docker Compose

## 起動方法

```
docker compose up -d --build
```

## API ドキュメント

- Swagger UI: http://localhost:8000/docs

## テスト

```
docker compose exec api poetry run pytest .
```

## UML/ER 図

- ER 図: `docs/er-diagram.md`
