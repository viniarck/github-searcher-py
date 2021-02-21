#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.github import GHReposRespModel
from app.models.github import GHReposSearchModel


def test_gh_repos_resp_model(gh_repos_resp_model_data) -> None:
    m = GHReposRespModel.from_github(gh_repos_resp_model_data)
    assert m
    assert m.total_count == gh_repos_resp_model_data["total_count"]


def test_gh_repos_search_model(gh_repos_search_model_data) -> None:
    m = GHReposSearchModel(**gh_repos_search_model_data)
    assert m
    expected = r"ml language:Elixir language:Python created:>2020-01-01&accept=application/vnd.github.v3+json&sort=stars&order=desc&per_page=1000&page=1"
    assert m.to_query() == expected
