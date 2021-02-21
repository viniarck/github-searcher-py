#!/usr/bin/env python
# -*- coding: utf-8 -*-
from app.models.repo import Pagination
from app.models.repo import RepoModel
from app.models.repo import RepoWrModel


def test_repo_model(repo_model_data) -> None:
    r = RepoModel(**repo_model_data)
    assert r
    for key in {
        "id",
        "gh_id",
        "name",
        "full_name",
        "language",
        "description",
        "html_url",
        "private",
        "stargazers_count",
        "watchers_count",
        "forks_count",
        "open_issues",
        "owner",
        "license",
        "gh_created_at",
        "gh_updated_at",
        "gh_pushed_at",
    }:
        assert getattr(r, key)


def test_repo_rw_model(repo_model_data) -> None:
    del repo_model_data["id"]
    r = RepoWrModel(**repo_model_data)
    assert r.id


def test_pagination_data(pagination_model_data) -> None:
    r = Pagination(**pagination_model_data)
    assert r
    assert r.total_count == 100
    assert r.page == 10
