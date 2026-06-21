from pydantic import BaseModel
from datetime import date

class TransactionCreate(BaseModel):
    operation_date: date
    payment_date: date
    card_number: str
    status: str   
    operation_amount: float
    operation_curr: str
    payment_amount: float
    payment_curr: str
    cashback: float
    category: str
    mcc: str
    description: str
    bonus: str
    investment_round: float
    operation_round: float

class TransactionResponse(BaseModel):
    id: int
    operation_date: date
    payment_date: date
    card_number: str
    status: str   
    operation_amount: float
    operation_curr: str
    payment_amount: float
    payment_curr: str
    cashback: float
    category: str
    mcc: str
    description: str
    bonus: str
    investment_round: float
    operation_round: float

    class Config:
        from_attributes = True