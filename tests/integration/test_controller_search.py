#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import uuid4

import pytest
from fastapi import HTTPException

from app.controllers.search import SearchController
from app.crud.search import SearchRepository
from app.models.search import SearchWrModel


def test_get_search(search_read_model_data, db_session) -> None:

    search_read_model_data["id"] = uuid4()
    model = SearchWrModel(**search_read_model_data)
    repo = SearchRepository(db_session)
    res = repo.create_search(model)
    assert res.keywords == model.keywords
    controller = SearchController(repo)
    assert controller.get_search_or_404(res.id).id == model.id  # type: ignore


def test_get_search_404(search_read_model_data, db_session) -> None:

    repo = SearchRepository(db_session)
    controller = SearchController(repo)
    with pytest.raises(HTTPException) as e:
        controller.get_search_or_404(str(uuid4()))
    assert str(e)


def test_get_searches(search_read_model_data, db_session) -> None:

    repo = SearchRepository(db_session)
    controller = SearchController(repo)
    assert controller.get_searches(1, 10)
