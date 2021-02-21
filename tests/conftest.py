from typing import Any
from typing import Dict

import pytest
from data.models import gh_repos_resp_data
from data.models import pagination_data
from data.models import repo_data
from data.models import search_read_data

from app.database import SessionLocal


@pytest.fixture
def repo_model_data() -> Dict[str, Any]:
    return repo_data()


@pytest.fixture
def pagination_model_data() -> Dict[str, Any]:
    return pagination_data()


@pytest.fixture
def search_read_model_data() -> Dict[str, Any]:
    return search_read_data()


@pytest.fixture
def gh_repos_resp_model_data() -> Dict[str, Any]:
    return gh_repos_resp_data()


@pytest.fixture
def gh_repos_search_model_data() -> Dict[str, Any]:
    return {"search_options": search_read_data()}


@pytest.fixture
def db_session() -> SessionLocal:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        db.rollback()
