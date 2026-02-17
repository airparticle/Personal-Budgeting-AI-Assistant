from pydantic import BaseModel
from typing import Optional

# Analytics schemas
class SpendingPrediction(BaseModel):
    predicted_amount: float
    confidence_score: float
    currency: str = "USD"
    message: Optional[str] = None

class CategoryBreakdown(BaseModel):
    category: str
    total_amount: float