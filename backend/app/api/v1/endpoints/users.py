from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_user import user as crud_user
from app.schemas.user import UserCreate, UserResponse

router = APIRouter()


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
        *,
        db: Session = Depends(deps.get_db),
        user_in: UserCreate,
) -> Any:
    """
    Register a new user.
    Matches spec: POST /api/users/register
    """
    # Check if user already exists
    existing_user = crud_user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A user with this email already exists.",
        )

    user = crud_user.create(db, obj_in=user_in)
    return user


@router.get("/me", response_model=UserResponse)
def read_current_user(
        current_user=Depends(deps.get_current_user),
) -> Any:
    """
    Get current logged-in user profile.
    """
    return current_user