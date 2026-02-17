from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps  # Dependencies like get_db, get_current_user
from app.ml.engine import predictor

router = APIRouter()


@router.get("/prediction", response_model=schemas.SpendingPrediction)
def get_spending_prediction(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get AI-driven spending prediction for the next month based on user history.
    """
    # 1. Fetch recent transactions for the current user
    # We fetch the last 100 transactions to give the model context
    transactions = crud.transaction.get_multi_by_user(
        db, user_id=current_user.user_id, limit=100
    )

    if not transactions:
        # Handle new users with no data
        return {
            "predicted_amount": 0.0,
            "confidence_score": 0.0,
            "currency": "USD",
            "message": "Not enough data to generate a prediction."
        }

    # 2. Format data for the ML Engine
    # The ML engine expects a clean list of dictionaries, not SQLAlchemy objects
    transaction_data = [
        {
            "amount": t.amount,
            "category": t.category,
            "timestamp": t.timestamp
        }
        for t in transactions
    ]

    # 3. Run Inference (Fast, loaded in memory)
    prediction_result = predictor.predict_next_month_spending(transaction_data)

    return prediction_result


@router.get("/breakdown", response_model=List[schemas.CategoryBreakdown])
def get_spending_breakdown(
        db: Session = Depends(deps.get_db),
        current_user: models.User = Depends(deps.get_current_user),
) -> Any:
    """
    Get spending aggregated by category for visualization (Pie Charts).
    """
    transactions = crud.transaction.get_multi_by_user(
        db, user_id=current_user.user_id, limit=500
    )

    # Simple aggregation logic (could also be done via SQL query for performance)
    category_totals = {}
    for t in transactions:
        category_totals[t.category] = category_totals.get(t.category, 0) + t.amount

    # Convert to list for the response schema
    results = [
        {"category": cat, "total_amount": amount}
        for cat, amount in category_totals.items()
    ]

    return results