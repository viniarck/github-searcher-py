#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from itertools import chain
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import BaseModel
from pydantic import validator

from app.models.pagination import Pagination


class SearchQualifiers(BaseModel):
    language: Optional[str]
    created: Optional[str]
    user: Optional[str]


class SearchOptions(BaseModel):
    keywords: List[str] = []
    qualifiers: List[SearchQualifiers]

    @validator("qualifiers")
    def validate_qualifiers(cls, v, values, **kwargs) -> str:
        if not v and not values.get("keywords"):
            raise ValueError("Either 'keywords' or 'qualifiers' should be set")
        return v

    def to_query(self) -> str:
        """Convert this SearchOptions to GH query."""
        quals = []
        for qualifiers in self.qualifiers:
            for k, v in qualifiers:
                if v:
                    quals.append(f"{k}:{v}")
        return " ".join(chain(self.keywords, quals))


class SearchReadModel(BaseModel):
    id: UUID
    qualifiers: List[SearchQualifiers]
    keywords: List[str]
    inserted_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class SearchWrModel(SearchReadModel):
    id = uuid4()

    class Config:
        orm_mode = True


class PaginatedSearchModel(BaseModel):
    pagination: Pagination
    items: List[SearchReadModel]
