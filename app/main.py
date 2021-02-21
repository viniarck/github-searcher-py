#!/usr/bin/env python
# -*- coding: utf-8 -*-
from fastapi import FastAPI

from app.middleware import setup_cors


app = FastAPI(title="github-searcher API", version="v1")
app = setup_cors(app)
from .views.repos import router as repo_router  # noqa
from .views.searches import router as search_router  # noqa

api_prefix = "/api/v1"
app.include_router(repo_router, prefix=f"{api_prefix}/repos")
app.include_router(search_router, prefix=f"{api_prefix}/searches")
