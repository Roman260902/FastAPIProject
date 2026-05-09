from pydantic import BaseModel

class TransactionCreate(BaseModel):
    date: str
    amount: float
    description: str
    category: str