#!/usr/bin/env python
# -*- coding: utf-8 -*-
from uuid import uuid4

from app.crud.search import SearchRepository
from app.models.search import SearchWrModel


def test_create_search(search_read_model_data, db_session) -> None:
    model = SearchWrModel(**search_read_model_data)
    repo = SearchRepository(db_session)
    res = repo.create_search(model)
    assert res.keywords == model.keywords


def test_get_search(search_read_model_data, db_session) -> None:
    model = SearchWrModel(**search_read_model_data)
    repo = SearchRepository(db_session)
    res = repo.get_search(str(model.id))
    assert res.id == model.id  # type: ignore
    assert not repo.get_search(str(uuid4()))


def test_get_searches(search_read_model_data, db_session) -> None:
    SearchWrModel(**search_read_model_data)
    repo = SearchRepository(db_session)
    res = repo.get_searches()
    assert len(res.items) >= 1
