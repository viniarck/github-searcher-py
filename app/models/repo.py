#!/usr/bin/env python
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from uuid import UUID
from uuid import uuid4

from pydantic import AnyHttpUrl
from pydantic import BaseModel

from app.models.pagination import Pagination


class RepoModel(BaseModel):
    id: UUID
    search_id: Optional[UUID]
    gh_id: int
    name: str
    full_name: str
    language: Optional[str]
    description: Optional[str]
    html_url: AnyHttpUrl
    private: bool
    stargazers_count: Optional[int]
    watchers_count: Optional[int]
    forks_count: Optional[int]
    open_issues: Optional[int]
    owner: Optional[Dict[str, Any]]
    license: Optional[Dict[str, Any]]
    gh_created_at: datetime
    gh_updated_at: datetime
    gh_pushed_at: datetime

    inserted_at: Optional[datetime]
    updated_at: Optional[datetime]

    class Config:
        orm_mode = True


class PaginatedRepoModel(BaseModel):
    search_id: Optional[UUID]
    pagination: Pagination
    items: List[RepoModel]


class RepoWrModel(RepoModel):
    id = uuid4()

    class Config:
        orm_mode = True
