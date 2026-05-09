from sqlalchemy import Column, Integer, String, Float, Date
from .db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date)
    amount = Column(Float)
    description = Column(String)
    category = Column(String)