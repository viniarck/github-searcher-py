#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Any
from typing import List
from typing import Optional

from sqlalchemy.orm import Session

from app.models.search import PaginatedSearchModel
from app.models.search import SearchReadModel
from app.models.search import SearchWrModel
from app.schemas.search import Search


class SearchRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create_search(self, model: SearchWrModel, commit=True) -> SearchWrModel:
        db_item = Search(**model.dict())
        self.db.add(db_item)
        if commit:
            self.db.commit()
            self.db.refresh(db_item)
        return model

    def get_search(self, repo_id: str) -> Optional[Search]:
        return self.db.query(Search).filter(Search.id == repo_id).first()

    def get_searches(self, page=0, per_page=20) -> PaginatedSearchModel:

        filters: List[Any] = []
        query = (
            self.db.query(Search)
            if not filters
            else self.db.query(Search).filter(*filters)
        )

        repos_len = len(query.all())
        if per_page:
            query = query.limit(per_page)
        if page:
            query = query.offset(page * per_page)
        return PaginatedSearchModel(
            pagination=dict(total_count=repos_len, page=page + 1, per_page=per_page),
            items=[SearchReadModel.from_orm(r) for r in query.all()],
        )
