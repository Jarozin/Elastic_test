from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api import router
from app.db import init_db
from app.es import ensure_index, es_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    await ensure_index()
    yield
    await es_client.close()


app = FastAPI(
    title="Search Service",
    version="1.0.0",
    lifespan=lifespan,
)

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}