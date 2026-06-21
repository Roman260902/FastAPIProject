from sqlalchemy import Column, Integer, String, Float, Date, Numeric
from .db import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    operation_date = Column(Date)
    payment_date = Column(Date)
    card_number = Column(String)
    status = Column(String)   
    operation_amount = Column(Numeric(12,2))
    operation_curr = Column(String)
    payment_amount = Column(Numeric(12,2))
    payment_curr = Column(String)
    cashback = Column(Numeric(12,2))
    category = Column(String)
    mcc = Column(String)
    description = Column(String)
    bonus = Column(String)
    investment_round = Column(Numeric(12,2))
    operation_round = Column(Numeric(12,2))
