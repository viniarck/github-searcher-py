#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.database import Base


class Repo(Base):
    """Represent a GitHub repo."""

    __tablename__ = "repo"

    id = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
    )
    search_id = Column(UUID(as_uuid=True), ForeignKey("search.id"), nullable=True)
    search = relationship("Search")
    gh_id = Column(String, nullable=False)
    name = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    html_url = Column(String)
    private = Column(Boolean, nullable=False)
    description = Column(String)
    language = Column(String)
    stargazers_count = Column(Integer)
    watchers_count = Column(Integer)
    forks_count = Column(Integer)
    open_issues = Column(Integer)
    owner = Column(JSONB)
    license = Column(JSONB)
    gh_created_at = Column(DateTime, nullable=False)
    gh_updated_at = Column(DateTime, nullable=False)
    gh_pushed_at = Column(DateTime)

    inserted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime)
