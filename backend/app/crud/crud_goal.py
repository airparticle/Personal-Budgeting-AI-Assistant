from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.goal import Goal
from app.schemas.goal import GoalCreate, GoalUpdate


class CRUDGoal:
    def get(self, db: Session, id: int) -> Optional[Goal]:
        """
        Get a single goal by ID.
        """
        return db.query(Goal).filter(Goal.goal_id == id).first()

    def get_multi_by_user(
            self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100
    ) -> List[Goal]:
        """
        Get all goals for a specific user.
        """
        return (
            db.query(Goal)
            .filter(Goal.user_id == user_id)
            .offset(skip)
            .limit(limit)
            .all()
        )

    def create_with_owner(
            self, db: Session, *, obj_in: GoalCreate, user_id: int
    ) -> Goal:
        """
        Create a new goal linked to the logged-in user.
        """
        db_obj = Goal(
            user_id=user_id,
            goal_name=obj_in.goal_name,
            target_value=obj_in.target_value,
            current_progress=obj_in.current_progress
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
            self, db: Session, *, db_obj: Goal, obj_in: GoalUpdate
    ) -> Goal:
        """
        Update a goal's details or progress.
        """
        update_data = obj_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def delete(self, db: Session, *, id: int) -> Optional[Goal]:
        """
        Delete a goal by ID.
        """
        obj = db.query(Goal).get(id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj


# Create a single instance to be imported elsewhere
goal = CRUDGoal()