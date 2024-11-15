from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Application(Base):
    __tablename__ = 'applicants'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    path = Column(String)
    original_file_name = Column(String)
    details = Column(String)
    uploaded = Column(DateTime, server_default=func.now())