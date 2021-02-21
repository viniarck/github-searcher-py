#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

from typing import Any
from typing import Dict
from typing import List
from uuid import uuid4

from pydantic import BaseModel

from .repo import RepoModel
from .search import SearchOptions


class GHReposRespModel(BaseModel):
    total_count: int
    incomplete_results: bool
    items: List[RepoModel]

    @staticmethod
    def from_github(data: Dict[str, Any]) -> GHReposRespModel:
        """Instantiate from a dict."""
        data_items = data.get("items", {})
        from_to = {
            "id": "gh_id",
            "updated_at": "gh_updated_at",
            "pushed_at": "gh_pushed_at",
            "created_at": "gh_created_at",
        }
        items = [
            {k: v for k, v in entry.items() if k not in from_to} for entry in data_items
        ]
        for i in range(len(items)):
            kwargs = items[i]
            for k, v in from_to.items():
                kwargs[v] = data_items[i][k]
            kwargs["id"] = uuid4()

        return GHReposRespModel(
            incomplete_results=data.get("incomplete_results"),
            total_count=data.get("total_count"),
            items=[RepoModel(**item) for item in items],
        )


class GHReposSearchModel(BaseModel):
    search_options: SearchOptions
    accept: str = "application/vnd.github.v3+json"
    sort = "stars"
    order = "desc"
    per_page = 1000
    page = 1

    def to_query(self) -> str:
        """Transform to query."""

        return "&".join(
            [
                self.search_options.to_query(),
                f"accept={self.accept}",
                f"sort={self.sort}",
                f"order={self.order}",
                f"per_page={self.per_page}",
                f"page={self.page}",
            ]
        )
