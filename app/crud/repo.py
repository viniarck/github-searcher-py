#!/usr/bin/env python
# -*- coding: utf-8 -*-
from typing import Optional

from sqlalchemy.orm import Session

from app.models.repo import PaginatedRepoModel
from app.models.repo import RepoModel
from app.models.repo import RepoWrModel
from app.schemas.repo import Repo


class RepoRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_repo(self, repo_id: str) -> Optional[Repo]:
        return self.db.query(Repo).filter(Repo.id == repo_id).first()

    def get_repos(
        self, page=0, per_page=20, search_id: Optional[str] = None
    ) -> PaginatedRepoModel:
        filters = []
        if search_id:
            filters.append((Repo.search_id == search_id))
        query = (
            self.db.query(Repo) if not filters else self.db.query(Repo).filter(*filters)
        )

        repos_len = len(query.all())
        if per_page:
            query = query.limit(per_page)
        if page:
            query = query.offset(page * per_page)
        return PaginatedRepoModel(
            pagination=dict(total_count=repos_len, page=page + 1, per_page=per_page),
            items=[RepoModel.from_orm(r) for r in query.all()],
        )

    def create_repo(self, model: RepoWrModel, commit=True) -> RepoWrModel:
        db_item = Repo(**model.dict())
        self.db.add(db_item)
        if commit:
            self.db.commit()
            self.db.refresh(db_item)
        return model
