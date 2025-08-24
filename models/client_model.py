from sqlalchemy import Column, Integer, String
from database.db import Base

class Client(Base):
    """
    نموذج بيانات العميل (Client Model)
    يمثل عميل ذكي في منصة NexoraTrix
    """
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    type = Column(String, nullable=False)
    status = Column(String, nullable=False, default="Active")
    settings = Column(String, nullable=True, default="")
    visits = Column(Integer, default=0)
