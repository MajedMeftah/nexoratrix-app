from sqlalchemy import Column, Integer, String
from database.db import Base

class Client(Base):
    __tablename__ = "clients"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    type = Column(String)
    settings = Column(String)
    visits = Column(Integer, default=0)

