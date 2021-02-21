#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from pydantic import PositiveInt
from sqlalchemy.orm import Session

from app.controllers.search import SearchController
from app.database import get_db
from app.dependables import get_search_controller
from app.models.search import PaginatedSearchModel
from app.models.search import SearchReadModel

router = APIRouter()


@router.get(
    "/{search_id}",
    response_model=SearchReadModel,
    summary="Get search detailed information",
)
def searches_id(
    search_id: UUID,
    db: Session = Depends(get_db),
):
    controller: SearchController = get_search_controller(db)
    return controller.get_search_or_404(str(search_id))


@router.get("", response_model=PaginatedSearchModel, summary="List searches")
def repos(
    page: PositiveInt = PositiveInt(1),
    per_page: PositiveInt = PositiveInt(10),
    db: Session = Depends(get_db),
):
    controller: SearchController = get_search_controller(db)
    return controller.get_searches(int(page), int(per_page))
