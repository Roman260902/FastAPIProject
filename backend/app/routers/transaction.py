from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database.db import get_db
from database.models import Transaction
from app.schemas.transaction import TransactionCreate

router = APIRouter()

@router.post("/addtransaction")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    new_transaction = Transaction(
        date=transaction.date,
        amount=transaction.amount,
        description=transaction.description,
        category=transaction.category
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction