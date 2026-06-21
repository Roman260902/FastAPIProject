from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.database.db import get_db
from backend.database.models import Transaction
from backend.app.schemas.transaction import (
    TransactionCreate,
    TransactionResponse
)
import pandas as pd
from fastapi import UploadFile, File

router = APIRouter()

@router.post("/addtransaction")
def create_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db)
):
    new_transaction = Transaction(
        operation_date=transaction.operation_date,
        payment_date=transaction.payment_date,
        card_number=transaction.card_number,
        status=transaction.status,
        operation_amount=transaction.operation_amount,
        operation_curr=transaction.operation_curr,
        payment_amount=transaction.payment_amount,
        payment_curr=transaction.payment_curr,
        cashback=transaction.cashback,
        category=transaction.category,
        mcc=transaction.mcc,
        description=transaction.description,
        bonus=transaction.bonus,
        investment_round=transaction.investment_round,
        operation_round=transaction.operation_round
    )

    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)

    return new_transaction

@router.get("/load_transaction", response_model=list[TransactionResponse])
def get_transactions(
    db: Session = Depends(get_db)
):
    transactions = db.query(Transaction).all()

    return transactions

@router.post("/upload-csv")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    required_columns = [
        "operation_date",
        "payment_date",
        "card_number",
        "status", 
        "operation_amount",
        "operation_curr",
        "payment_amount",
        "payment_curr",
        "cashback",
        "category",
        "mcc",
        "description",
        "bonus",
        "investment_round",
        "operation_round"
    ]
   
    df = pd.read_csv(file.file, sep=";", decimal=",")

    for col in required_columns:
        if col not in df.columns:
            return {
                "error": f"Missing column: {col}"
            }

    df["operation_date"] = pd.to_datetime(df["operation_date"]).dt.date

    df["payment_date"] = pd.to_datetime(df["payment_date"]).dt.date

    df = df.fillna(0)

    for _, row in df.iterrows():

        transaction = Transaction(
            operation_date=row["operation_date"],
            payment_date=row["payment_date"],
            card_number=row["card_number"],
            status=row["status"],
            operation_amount=row["operation_amount"],
            operation_curr=row["operation_curr"],
            payment_amount=row["payment_amount"],
            payment_curr=row["payment_curr"],
            cashback=row["cashback"],
            category=row["category"],
            mcc=row["mcc"],
            description=row["description"],
            bonus=row["bonus"],
            investment_round=row["investment_round"],
            operation_round=row["operation_round"]
        )

        db.add(transaction)

    db.commit()

    return {"message": "CSV uploaded successfully",
            "count": len(df)
        }