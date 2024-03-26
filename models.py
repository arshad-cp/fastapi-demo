from sqlalchemy import Column, DateTime, String
from sqlalchemy.dialects.postgresql import JSONB
from datetime import datetime
from database.base import Base


class Tenant(Base):
    __tablename__ = 'tenants'
    id = Column(String(255), primary_key=True)
    data = Column(JSONB)
    created_at = Column(DateTime, default=datetime.now)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now)
