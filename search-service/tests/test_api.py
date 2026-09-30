import os

import httpx
import pytest

BASE_URL = os.getenv("APP_URL", "http://localhost:8000")


@pytest.mark.asyncio
async def test_create_search_delete():
    async with httpx.AsyncClient(base_url=BASE_URL, timeout=10) as client:
        payload = {
            "rubrics": ["test"],
            "text": "unique pytest search text",
            "created_date": "2024-01-01T00:00:00Z",
        }

        response = await client.post("/documents", json=payload)
        assert response.status_code == 201, response.text
        doc_id = response.json()["id"]

        response = await client.get("/search", params={"query": "unique pytest"})
        assert response.status_code == 200
        items = response.json()
        assert any(item["id"] == doc_id for item in items)

        response = await client.delete(f"/documents/{doc_id}")
        assert response.status_code == 204

        response = await client.get("/search", params={"query": "unique pytest"})
        assert response.status_code == 200
        items = response.json()
        assert all(item["id"] != doc_id for item in items)