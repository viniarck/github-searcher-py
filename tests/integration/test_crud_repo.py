#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import uuid4

from app.crud.repo import RepoRepository
from app.models.repo import RepoWrModel


def test_create_repo(repo_model_data, db_session) -> None:
    model = RepoWrModel(**repo_model_data)
    repo = RepoRepository(db_session)
    model_created = repo.create_repo(model)
    assert model_created
    model_get = repo.get_repo(str(model_created.id))
    assert model_get.name == model_created.name  # type: ignore


def test_get_not_found(repo_model_data, db_session) -> None:
    uuid = str(uuid4())
    repo = RepoRepository(db_session)
    assert not repo.get_repo(uuid)


def test_get_repos(repo_model_data, db_session) -> None:
    RepoWrModel(**repo_model_data)
    repo = RepoRepository(db_session)
    res = repo.get_repos()
    assert res.pagination.page == 1
    assert len(res.items) >= 1
