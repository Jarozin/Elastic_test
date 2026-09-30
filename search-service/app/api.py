from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app import es
from app.db import Document, get_session
from app.schemas import DocumentCreate, DocumentOut


router = APIRouter()


@router.get("/search", response_model=list[DocumentOut])
async def search(
    query: str = Query(..., min_length=1),
    session: AsyncSession = Depends(get_session),
):
    ids = await es.search_ids(query)
    if not ids:
        return []

    stmt = (
        select(Document)
        .where(Document.id.in_(ids))
        .order_by(Document.created_date.desc())
        .limit(20)
    )
    result = await session.execute(stmt)
    return list(result.scalars().all())


@router.post("/documents", response_model=DocumentOut, status_code=201)
async def create_document(
    payload: DocumentCreate,
    session: AsyncSession = Depends(get_session),
):
    data = payload.model_dump(exclude_none=True)
    doc = Document(**data)

    session.add(doc)
    await session.commit()
    await session.refresh(doc)

    await es.index_document(doc.id, doc.text)
    return doc


@router.delete("/documents/{doc_id}", status_code=204)
async def delete_document(
    doc_id: int,
    session: AsyncSession = Depends(get_session),
):
    doc = await session.get(Document, doc_id)
    if not doc:
        raise HTTPException(status_code=404, detail="Document not found")

    await session.delete(doc)
    await session.commit()

    await es.delete_document(doc_id)
    return Response(status_code=204)