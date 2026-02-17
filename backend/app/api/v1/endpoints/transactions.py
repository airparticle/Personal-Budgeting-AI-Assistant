from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_transaction import transaction as crud_transaction
from app.models.user import User
from app.schemas.transaction import TransactionCreate, TransactionUpdate, TransactionResponse

router = APIRouter()


@router.get("/", response_model=List[TransactionResponse])
def get_user_transactions(
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        skip: int = 0,
        limit: int = 100,
) -> Any:
    """
    Retrieve all transactions for the current user.
    """
    transactions = crud_transaction.get_multi_by_user(
        db, user_id=current_user.user_id, skip=skip, limit=limit
    )
    return transactions


@router.post("/", response_model=TransactionResponse, status_code=status.HTTP_201_CREATED)
def create_transaction(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        transaction_in: TransactionCreate,
) -> Any:
    """
    Create a new transaction for the current user.
    """
    transaction = crud_transaction.create_with_owner(
        db, obj_in=transaction_in, user_id=current_user.user_id
    )
    return transaction


@router.get("/{transaction_id}", response_model=TransactionResponse)
def get_transaction(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        transaction_id: int,
) -> Any:
    """
    Get a specific transaction by ID.
    """
    transaction = crud_transaction.get(db, id=transaction_id)
    if not transaction or transaction.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction


@router.delete("/{transaction_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_transaction(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        transaction_id: int,
) -> None:
    """
    Delete a transaction.
    """
    transaction = crud_transaction.get(db, id=transaction_id)
    if not transaction or transaction.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Transaction not found")

    crud_transaction.delete(db, id=transaction_id)