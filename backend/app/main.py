from fastapi import FastAPI
from backend.database.db import engine
from backend.database.models import Base
from backend.app.routers import transaction



app = FastAPI()

@app.get("/")
def root():
    return {"message": "Expense Tracker API"}

Base.metadata.create_all(bind=engine)

app.include_router(
    transaction.router,
    prefix="/transactions",
    tags=["Transactions"]
)