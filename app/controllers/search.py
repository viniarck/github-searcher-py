#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import HTTPException

from app.crud.search import SearchRepository
from app.models.search import PaginatedSearchModel
from app.models.search import SearchReadModel


class SearchController:

    """SearchController."""

    def __init__(
        self,
        search_repo: SearchRepository,
    ) -> None:
        """Constructor of SearchController."""
        self.search_repo = search_repo

    def get_search_or_404(self, search_id: str) -> SearchReadModel:
        """get_search_or_404."""
        repo = self.search_repo.get_search(search_id)
        if not repo:
            raise HTTPException(status_code=404, detail="not found")
        return repo

    def get_searches(self, page: int, per_page: int) -> PaginatedSearchModel:
        return self.search_repo.get_searches(page - 1, per_page)
