from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class DocumentBase(BaseModel):
    rubrics: list[str] = Field(default_factory=list)
    text: str
    created_date: datetime


class DocumentCreate(DocumentBase):
    id: int | None = None


class DocumentOut(DocumentBase):
    id: int

    model_config = ConfigDict(from_attributes=True)