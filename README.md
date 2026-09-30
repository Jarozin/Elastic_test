# Search Service

Простой поисковик по текстам документов.

Принимает текстовый запрос, ищет по тексту документа в Elasticsearch и возвращает первые 20 документов со всеми полями из БД, отсортированные по дате создания. Умеет удалять документ по id из БД и индекса.

Стек: Python 3.12, FastAPI, SQLAlchemy (async) + asyncpg, PostgreSQL, Elasticsearch, Docker, Pytest.

# Запуск

docker compose up --build -d

Проверить, что сервис поднялся:

curl http://localhost:8000/health

{"status":"ok"}
Swagger UI открывается по адресу:

http://localhost:8000/docs

# Импорт данных

Необходимо положить CSV-файл в data/posts.csv. Ожидаемые колонки:

text,created_date,rubrics

# Запустить импорт:

docker compose exec app python -m scripts.import_csv /data/posts.csv

Скрипт сохраняет документы в PostgreSQL и индексирует их в Elasticsearch.

# API

GET /search?query=<текст>

Поиск по тексту документа. Возвращает до 20 документов, отсортированных по created_date по убыванию.

Пример:

curl -G "http://localhost:8000/search" --data-urlencode "query=мерседес"

DELETE /documents/{id}

Удаляет документ из БД и индекса. Ответ 204 No Content. Если документа нет — 404.

Пример:

curl -X DELETE http://localhost:8000/documents/34

GET /health

Проверка работоспособности сервиса.

# Тесты

docker compose exec app pytest -q

# OpenAPI

Актуальная документация — docs.json в корне проекта. Сгенерировать заново:

docker compose exec app python -c "import json,urllib.request;print(json.dumps(json.load(urllib.request.urlopen('http://localhost:8000/openapi.json')),indent=2,ensure_ascii=False))" > docs.json

# Остановка

docker compose down

# С удалением данных:

docker compose down -v