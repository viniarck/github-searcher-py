#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pytest
from pydantic import ValidationError

from app.models.search import SearchOptions
from app.models.search import SearchWrModel


def test_search_rw_model(search_read_model_data) -> None:
    s = SearchWrModel(**search_read_model_data)
    assert s
    for key in {
        "qualifiers",
        "keywords",
    }:
        assert getattr(s, key)


def test_search_options_model() -> None:
    with pytest.raises(ValidationError) as e:
        SearchOptions(**{"qualifiers": [], "keywords": []})
    assert "Either" in str(e)


def test_search_options(search_read_model_data) -> None:
    s = SearchOptions(**search_read_model_data)
    assert s
    for key in {
        "qualifiers",
        "keywords",
    }:
        assert getattr(s, key)
    assert s.to_query() == "ml language:Elixir language:Python created:>2020-01-01"
