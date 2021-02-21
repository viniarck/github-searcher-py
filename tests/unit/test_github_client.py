#!/usr/bin/env python
# -*- coding: utf-8 -*-
import respx
from httpx import Response

from app.github.client import GitHubClient
from app.models.github import GHReposSearchModel


@respx.mock
def test_gh_repos_search_model(
    gh_repos_search_model_data, gh_repos_resp_model_data
) -> None:

    search_query_params = GHReposSearchModel(
        search_options=gh_repos_search_model_data["search_options"], page=1, per_page=20
    ).to_query()
    client = GitHubClient()
    url = f"{client._repos_search_url}{search_query_params}"
    respx.get(url).mock(
        return_value=Response(status_code=200, json=gh_repos_resp_model_data)
    )

    res = client.search_repos(
        gh_repos_search_model_data["search_options"], page=1, per_page=20
    )
    assert res.pagination.page == 1
    assert len(res.items) >= 1

    # m = GHReposSearchModel(**gh_repos_search_model_data)
