from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import extract

from app.models.transaction import Transaction
from app.schemas.transaction import TransactionCreate, TransactionUpdate

class CRUDTransaction:
    def get(self, db: Session, id: int) -> Optional[Transaction]:
        """
        Get a single transaction by ID.
        """
        return db.query(Transaction).filter(Transaction.transaction_id == id).first()

    def get_multi_by_user(
        self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Transaction]:
        """
        Get transactions for a specific user, ordered by newest date.
        """
        return (
            db.query(Transaction)
            .filter(Transaction.user_id == user_id)
            .order_by(Transaction.timestamp.desc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
        self, db: Session, *, obj_in: TransactionCreate, user_id: int
    ) -> Transaction:
        """
        Create a new transaction linked to the logged-in user.
        """
        # Convert Pydantic model to dict
        db_obj = Transaction(
            user_id=user_id,
            amount=obj_in.amount,
            category=obj_in.category,
            description=obj_in.description,
            timestamp=obj_in.timestamp
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Transaction:
        """
        Delete a transaction by ID.
        """
        obj = db.query(Transaction).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    def get_by_month(
        self, db: Session, *, user_id: int, year: int, month: int
    ) -> List[Transaction]:
        """
        Fetch all transactions for a specific month (useful for budgeting features).
        """
        return (
            db.query(Transaction)
            .filter(
                Transaction.user_id == user_id,
                extract('year', Transaction.timestamp) == year,
                extract('month', Transaction.timestamp) == month
            )
            .all()
        )

# Create a single instance to be imported elsewhere
transaction = CRUDTransaction()