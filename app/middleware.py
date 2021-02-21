#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def setup_cors(app: FastAPI) -> FastAPI:

    if os.getenv("STAGE", "") == "develop":
        origins = [
            "http://localhost",
            "http://localhost:8080",
            "http://localhost:8081",
        ]
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    else:
        deployment_origin = os.getenv(
            "DEPLOYMENT_ORIGIN", "https://github-searcher-js-py.herokuapp.com"
        )
        origins = deployment_origin.split(",")
        app.add_middleware(
            CORSMiddleware,
            allow_origins=origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    return app
