from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.crud.crud_goal import goal as crud_goal
from app.models.user import User
from app.schemas.goal import GoalCreate, GoalUpdate, GoalResponse

router = APIRouter()


@router.get("/", response_model=List[GoalResponse])
def get_user_goals(
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        skip: int = 0,
        limit: int = 20,
) -> Any:
    """Get all goals for the current user."""
    goals = crud_goal.get_multi_by_user(db, user_id=current_user.user_id, skip=skip, limit=limit)
    return goals


@router.post("/", response_model=GoalResponse, status_code=status.HTTP_201_CREATED)
def create_goal(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        goal_in: GoalCreate,
) -> Any:
    """Create a new financial goal."""
    goal = crud_goal.create_with_owner(db, obj_in=goal_in, user_id=current_user.user_id)
    return goal


@router.put("/{goal_id}", response_model=GoalResponse)
def update_goal(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        goal_id: int,
        goal_in: GoalUpdate,
) -> Any:
    """Update a goal's progress or details."""
    goal = crud_goal.get(db, id=goal_id)
    if not goal or goal.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Goal not found")

    goal = crud_goal.update(db, db_obj=goal, obj_in=goal_in)
    return goal


@router.delete("/{goal_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_goal(
        *,
        db: Session = Depends(deps.get_db),
        current_user: User = Depends(deps.get_current_user),
        goal_id: int,
) -> None:
    """Delete a financial goal."""
    goal = crud_goal.get(db, id=goal_id)
    if not goal or goal.user_id != current_user.user_id:
        raise HTTPException(status_code=404, detail="Goal not found")

    crud_goal.delete(db, id=goal_id)