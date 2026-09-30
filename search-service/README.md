# Search Service

Простой поисковик по текстам документов.

Принимает произвольный текстовый запрос, ищет по тексту документа в Elasticsearch
и возвращает первые 20 документов со всеми полями из БД, отсортированные по дате
создания. Умеет удалять документ по `id` из БД и индекса.

## Стек

- Python 3.12
- FastAPI
- SQLAlchemy (async) + asyncpg
- PostgreSQL 16
- Elasticsearch 8.13
- Docker / Docker Compose
- Pytest + httpx

## Структура проекта

```
.
├── app/                # код приложения
│   ├── api.py          # роуты
│   ├── config.py       # настройки
│   ├── db.py           # подключение к PostgreSQL и модель Document
│   ├── es.py           # работа с Elasticsearch
│   ├── main.py         # точка входа FastAPI
│   └── schemas.py      # Pydantic-схемы
├── scripts/
│   └── import_csv.py   # импорт CSV в БД и индекс
├── tests/
│   └── test_api.py     # функциональные тесты
├── data/
│   └── posts.csv       # исходные данные
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── pytest.ini
└── docs.json           # OpenAPI-документация
```

## Запуск

```bash
docker compose up --build -d
```

Проверить, что сервис поднялся:

```bash
curl http://localhost:8000/health
# {"status":"ok"}
```

Swagger UI:

```
http://localhost:8000/docs
```

## Импорт данных

Положи CSV-файл в `data/posts.csv`. Ожидаемые колонки:

```text
text,created_date,rubrics
```

Пример:

```csv
text,created_date,rubrics
"Текст поста",2019-07-25 12:42:13,"['VK-1', 'VK-2']"
```

Запустить импорт:

```bash
docker compose exec app python -m scripts.import_csv /data/posts.csv
```

Скрипт сохраняет документы в PostgreSQL и индексирует их в Elasticsearch.

## API

### `GET /search?query=<текст>`

Поиск по тексту документа.

Пример:

```bash
curl -G "http://localhost:8000/search" --data-urlencode "query=мерседес"
```

Возвращает до 20 документов, отсортированных по `created_date` по убыванию.

### `DELETE /documents/{id}`

Удаляет документ из БД и индекса.

Пример:

```bash
curl -X DELETE http://localhost:8000/documents/34
```

Ответ: `204 No Content`. Если документа нет — `404`.

### `GET /health`

Проверка работоспособности сервиса.

## Тесты

```bash
docker compose exec app pytest -q
```

## OpenAPI

Актуальная документация — `docs.json` в корне проекта. Сгенерировать заново:

```bash
docker compose exec app python -c "import json,urllib.request;print(json.dumps(json.load(urllib.request.urlopen('http://localhost:8000/openapi.json')),indent=2,ensure_ascii=False))" > docs.json
```

## Остановка

```bash
docker compose down
```

С удалением данных (томов):

```bash
docker compose down -v
```