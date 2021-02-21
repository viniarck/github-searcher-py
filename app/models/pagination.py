#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pydantic import BaseModel


class Pagination(BaseModel):

    total_count: int
    page: int
