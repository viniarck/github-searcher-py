#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from sqlalchemy.orm import Session

from app.controllers.repo import RepoController
from app.controllers.search import SearchController
from app.crud.repo import RepoRepository
from app.crud.search import SearchRepository
from app.github.client import GitHubClient


def get_github() -> GitHubClient:
    return GitHubClient(os.getenv("GH_TOKEN", ""))


def get_repo_controller(db: Session) -> RepoController:
    return RepoController(
        search_repo=SearchRepository(db),
        repo_repo=RepoRepository(db),
        gh_client=get_github(),
    )


def get_search_controller(db: Session) -> SearchController:
    return SearchController(search_repo=SearchRepository(db))
