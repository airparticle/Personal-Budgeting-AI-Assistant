from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Goal(Base):
    """Matches spec: Goals Table"""
    __tablename__ = "goals"

    goal_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"), nullable=False)
    goal_name = Column(String, nullable=False)
    target_value = Column(Float, nullable=False)
    current_progress = Column(Float, default=0.0)

    user = relationship("User", back_populates="goals")
