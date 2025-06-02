from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from .database import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    hostname = Column(String, nullable=False)
    ip = Column(String, nullable=False)
    mac = Column(String, nullable=False, unique=True)
    registered_at = Column(DateTime, default=datetime.utcnow)

class Command(Base):
    __tablename__ = "commands"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer)
    command = Column(String)
    processed = Column(Boolean, default=False)
