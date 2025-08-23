from sqlalchemy import Column, Integer, String
from database.db import Base

class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False)
    settings = Column(String, nullable=True)
    visits = Column(Integer, default=0)
