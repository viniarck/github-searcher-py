#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from uuid import uuid4

from fastapi import HTTPException
from tenacity import RetryError

from app.crud.repo import RepoRepository
from app.crud.search import SearchRepository
from app.github.client import GitHubClient
from app.models.repo import PaginatedRepoModel
from app.models.repo import RepoWrModel
from app.models.search import SearchOptions
from app.models.search import SearchWrModel
from app.schemas.repo import Repo


class RepoController:

    """RepoController."""

    def __init__(
        self,
        search_repo: SearchRepository,
        repo_repo: RepoRepository,
        gh_client: GitHubClient,
    ) -> None:
        """Constructor of RepoController."""
        self.search_repo = search_repo
        self.repo_repo = repo_repo
        self.client = gh_client

    def get_repo_or_404(self, repo_id: str) -> Repo:
        """get_repo_or_404."""
        repo = self.repo_repo.get_repo(repo_id)
        if not repo:
            raise HTTPException(status_code=404, detail="not found")
        return repo

    def get_repos(
        self, page: int, per_page: int, search_id: Optional[str] = None
    ) -> PaginatedRepoModel:
        return self.repo_repo.get_repos(page - 1, per_page, search_id)

    def _validate_github_page_limits_or_400(self, per_page: int) -> int:
        if per_page < 1 or per_page > 1000:
            raise HTTPException(
                status_code=400,
                detail="GitHub repo search API limits up to 1000 results",
            )
        return per_page

    def search_repos(
        self,
        search_options: SearchOptions,
        page: int = 1,
        per_page: int = 5,
    ) -> PaginatedRepoModel:
        """search."""

        self._validate_github_page_limits_or_400(per_page)

        try:
            search_id = uuid4()
            self.search_repo.create_search(
                SearchWrModel(
                    id=search_id,
                    keywords=search_options.keywords,
                    qualifiers=search_options.qualifiers,
                ),
                commit=False,
            )
            response = self.client.search_repos(
                search_options=search_options,
                page=page,
                per_page=per_page,
            )

            for repo in response.items:
                repo.search_id = search_id
                repo_wr = RepoWrModel(**repo.dict())
                self.repo_repo.create_repo(repo_wr, commit=False)
            self.repo_repo.db.commit()
            response.search_id = search_id

            return response
        except RetryError:
            raise HTTPException(
                status_code=503,
                detail="GitHub API isn't available for this client. Please, retry later",
            )
