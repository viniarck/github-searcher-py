#!/usr/bin/env python
# -*- coding: utf-8 -*-
from unittest.mock import Mock
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.controllers.repo import RepoController
from app.crud.repo import RepoRepository
from app.models.repo import RepoWrModel
from app.models.search import SearchOptions


def test_get_repo(repo_model_data, db_session) -> None:
    model = RepoWrModel(**repo_model_data)
    repo = RepoRepository(db_session)
    model_created = repo.create_repo(model)
    assert model_created
    controller = RepoController(search_repo=Mock(), repo_repo=repo, gh_client=Mock())

    model_get = controller.get_repo_or_404(str(model_created.id))
    assert model_get.name == model_created.name  # type: ignore


def test_get_repo_404(repo_model_data, db_session) -> None:
    model = RepoWrModel(**repo_model_data)
    repo = RepoRepository(db_session)
    model_created = repo.create_repo(model)
    assert model_created
    controller = RepoController(search_repo=Mock(), repo_repo=repo, gh_client=Mock())

    with pytest.raises(HTTPException):
        controller.get_repo_or_404(str(uuid4()))


def test_validate_github_page_limits_or_400(repo_model_data, db_session) -> None:
    controller = RepoController(search_repo=Mock(), repo_repo=Mock(), gh_client=Mock())

    with pytest.raises(HTTPException) as e:
        controller._validate_github_page_limits_or_400(1001)
    assert str(e)


def test_search_repo(repo_model_data, db_session) -> None:
    model = RepoWrModel(**repo_model_data)
    repo = RepoRepository(db_session)
    model_created = repo.create_repo(model)
    assert model_created

    client = Mock()

    items = Mock()
    items.items = []
    client.search_repos = Mock(return_value=items)

    controller = RepoController(search_repo=Mock(), repo_repo=repo, gh_client=client)
    model_get = controller.search_repos(
        SearchOptions(keywords=["Python"], qualifiers=[])
    )
    assert model_get
