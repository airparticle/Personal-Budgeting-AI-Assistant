
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.core.database import Base


class Transaction(Base):
    __tablename__ = "transactions"
    transaction_id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    amount = Column(Float)
    category = Column(String)  # e.g., "Food", "Rent"
    timestamp = Column(DateTime)
    description = Column(String)

    user = relationship("User", back_populates="transactions")