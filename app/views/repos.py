#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID

from fastapi import APIRouter
from fastapi import Body
from fastapi import Depends
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.controllers.repo import RepoController
from app.database import get_db
from app.dependables import get_repo_controller
from app.models.repo import PaginatedRepoModel
from app.models.repo import RepoModel
from app.models.search import SearchOptions

router = APIRouter()


@router.get(
    "/{repo_id}",
    response_model=RepoModel,
    summary="Get repo detailed information",
)
def repos_id(
    repo_id: UUID,
    db: Session = Depends(get_db),
):
    controller: RepoController = get_repo_controller(db)
    return controller.get_repo_or_404(str(repo_id))


@router.get("", response_model=PaginatedRepoModel, summary="List repos")
def repos(
    page: PositiveInt = PositiveInt(1),
    per_page: PositiveInt = PositiveInt(10),
    search_id: Optional[UUID] = None,
    db: Session = Depends(get_db),
):
    controller: RepoController = get_repo_controller(db)
    if search_id:
        search_id = str(search_id)  # type: ignore
    return controller.get_repos(int(page), int(per_page), search_id=search_id)  # type: ignore


@router.post(
    "/search",
    response_model=PaginatedRepoModel,
    summary="Search GitHub repos",
)
def repos_search(
    search_options: SearchOptions = Body(
        ...,
        example={
            "qualifiers": [
                {"language": "Elixir", "created": ">2020-01-01"},
                {"language": "Python"},
            ]
        },
    ),
    page: PositiveInt = PositiveInt(1),
    per_page: PositiveInt = PositiveInt(10),
    db: Session = Depends(get_db),
):
    controller: RepoController = get_repo_controller(db)
    return controller.search_repos(search_options, int(page), int(per_page))
