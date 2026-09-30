from elasticsearch import AsyncElasticsearch, NotFoundError

from app.config import settings


es_client = AsyncElasticsearch(settings.elasticsearch_url)


async def ensure_index() -> None:
    exists = await es_client.indices.exists(index=settings.es_index)
    if not exists:
        await es_client.indices.create(
            index=settings.es_index,
            mappings={
                "properties": {
                    "id": {"type": "keyword"},
                    "text": {"type": "text"},
                }
            },
        )


async def index_document(doc_id: int, text: str) -> None:
    await es_client.index(
        index=settings.es_index,
        id=str(doc_id),
        document={"id": doc_id, "text": text},
        refresh=True,
    )


async def delete_document(doc_id: int) -> None:
    try:
        await es_client.delete(
            index=settings.es_index,
            id=str(doc_id),
            refresh=True,
        )
    except NotFoundError:
        pass


async def search_ids(query: str, size: int = 10000) -> list[int]:
    response = await es_client.search(
        index=settings.es_index,
        query={"match": {"text": query}},
        size=size,
    )
    return [int(hit["_id"]) for hit in response["hits"]["hits"]]