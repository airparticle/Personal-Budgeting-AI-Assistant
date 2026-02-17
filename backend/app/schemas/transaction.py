from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TransactionBase(BaseModel):
    amount: float
    category: str
    description: Optional[str] = None
    timestamp: Optional[datetime] = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    transaction_id: int
    user_id: int

    class Config:
        from_attributes = True