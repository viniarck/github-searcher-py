#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import annotations

import logging
import os
from typing import Any
from typing import Dict
from typing import Optional

import httpx
from cachetools import cached
from cachetools import TTLCache
from cachetools.keys import hashkey
from httpx import HTTPStatusError
from httpx import TimeoutException
from tenacity import after_log
from tenacity import before_log
from tenacity import retry
from tenacity import retry_if_exception_type
from tenacity import stop_after_attempt
from tenacity import wait_random

from ..models.github import GHReposRespModel
from ..models.github import GHReposSearchModel
from ..models.repo import PaginatedRepoModel
from ..models.search import SearchOptions

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def my_before_search_sleep(retry_state):
    logger.info(
        f"retrying number #{retry_state.attempt_number} for {retry_state.fn} "
        f", args: {retry_state.args}, outcome {retry_state.outcome}"
    )


def cachekey(_: GitHubClient, url: str, timeout: int):
    """Function used to generate the cache key"""
    return hashkey(url)


class GitHubClient:

    """HTTP REST client for GitHub's API v3 see https://docs.github.com/rest for
    more information."""

    def __init__(
        self,
        api_key: Optional[str] = os.getenv("GH_TOKEN"),
        base_url: str = "https://api.github.com",
    ) -> None:
        """Constructor of GitHubClient."""

        self._base_url = base_url
        self._repos_search_url = f"{base_url}/search/repositories?q="
        self._api_key = api_key

    @property
    def _headers(self) -> dict:
        """HTTP headers used when making requests upstream."""

        headers = {
            "Content-Type": "application/json",
        }
        if self._api_key:
            headers["Authorization"] = f"token {self._api_key}"
        return headers

    @cached(cache=TTLCache(maxsize=10_000_000, ttl=3600), key=cachekey)  # type: ignore
    def _search_repos_cached_request(
        self,
        url: str,
        timeout=10,
    ) -> Dict[str, Any]:
        """Cached search request up to ttl secs."""
        logger.info(f"It'll search with {url}")
        r = httpx.get(
            url,
            headers=self._headers,
            timeout=timeout,
        )
        r.raise_for_status()
        response_dict = r.json()
        logger.debug(f"search_repos, status_code: {r.status_code}, r: {response_dict}")
        return response_dict

    @retry(
        stop=stop_after_attempt(5),
        wait=wait_random(min=0, max=1),
        before=before_log(logger, logging.INFO),
        before_sleep=my_before_search_sleep,
        after=after_log(logger, logging.WARN),
        retry=retry_if_exception_type(
            (HTTPStatusError, TimeoutException, ConnectionError)
        ),
    )
    def search_repos(
        self,
        search_options: SearchOptions,
        page=1,
        per_page=1000,
        timeout=10,
    ) -> PaginatedRepoModel:
        """Search repos, the recursion should be done at the caller site."""

        search_model = GHReposSearchModel(
            search_options=search_options, page=page, per_page=per_page
        ).to_query()
        url = f"{self._repos_search_url}{search_model}"
        response_dict = self._search_repos_cached_request(url=url, timeout=timeout)
        gh_response = GHReposRespModel.from_github(response_dict)

        if gh_response.incomplete_results:
            exc_msg = f"incomplete_results for {search_options}"
            raise TimeoutException(exc_msg, request=None)  # type: ignore
        return PaginatedRepoModel(
            pagination=dict(
                total_count=gh_response.total_count, page=page, per_page=per_page
            ),
            items=gh_response.items,
        )
