from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext
import bcrypt

from app.models.user import User
from app.schemas.user import UserCreate

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class CRUDUser:
    """
    CRUD operations for User model
    """

    def get(self, db: Session, user_id: int) -> Optional[User]:
        """Get user by ID"""
        return db.query(User).filter(User.user_id == user_id).first()

    def get_by_email(self, db: Session, email: str) -> Optional[User]:
        """Get user by email"""
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """Create a new user"""
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(obj_in.password.encode('utf-8'), salt).decode('utf-8')

        db_user = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'),
            hashed_password.encode('utf-8')
        )

    def authenticate(self, db: Session, email: str, password: str) -> Optional[User]:
        """Authenticate a user"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not self.verify_password(password, user.hashed_password):
            return None
        return user


# Create a singleton instance
user = CRUDUser()