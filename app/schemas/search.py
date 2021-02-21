#!/usr/bin/env python
# -*- coding: utf-8 -*-
import uuid
from datetime import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.dialects.postgresql import UUID

from app.database import Base


class Search(Base):
    """Represent a GitHub Search."""

    __tablename__ = "search"

    id = Column(
        UUID(as_uuid=True),
        unique=True,
        nullable=False,
        primary_key=True,
        default=uuid.uuid4,
    )
    qualifiers = Column(JSONB, nullable=False)
    keywords = Column(ARRAY(String), nullable=False)

    inserted_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    deleted_at = Column(DateTime)
