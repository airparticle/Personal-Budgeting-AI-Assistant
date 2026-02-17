import os
import pickle
import numpy as np
import logging
from typing import List, Dict, Any

# Configure logging
logger = logging.getLogger(__name__)


class SpendingPredictor:
    """
    A singleton class to handle loading the ML model and making predictions.
    """

    def __init__(self, model_path: str = "app/ml/models/spending_predictor_v1.pkl"):
        self.model_path = model_path
        self.model = None
        self._load_model()

    def _load_model(self):
        """
        Loads the model from disk.
        """
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                logger.info(f"ML Model loaded successfully from {self.model_path}")
            except Exception as e:
                logger.error(f"Failed to load model: {e}")
                self.model = None
        else:
            logger.warning(f"Model file not found at {self.model_path}. Running in MOCK mode.")
            self.model = None

    def predict_next_month_spending(self, recent_transactions: List[Dict[str, Any]]) -> Dict[str, float]:
        """
        Predicts total spending for the upcoming month.
        """

        # 1. Feature Engineering
        # Calculate the exact same features used in training.py
        if not recent_transactions:
            total_spent_last_30_days = 0.0
            tx_count = 0
        else:
            total_spent_last_30_days = sum(t['amount'] for t in recent_transactions)
            tx_count = len(recent_transactions)

        predicted_amount = 0.0
        confidence = 0.0

        if self.model and recent_transactions:
            try:
                # --- SCIKIT-LEARN INFERENCE ---
                # Prepare input vector: [[total_spend, tx_count]]
                features = np.array([[total_spent_last_30_days, tx_count]])

                # Get prediction
                prediction = self.model.predict(features)[0]

                predicted_amount = float(prediction)
                # Random Forest doesn't give a simple "confidence probability" for regression
                # but we can assume high confidence if we have data.
                confidence = 0.85

                logger.info(f"ML Prediction: Input=${total_spent_last_30_days} -> Output=${predicted_amount}")
            except Exception as e:
                logger.error(f"Error during inference: {e}")
                # Fallback to simple logic if inference crashes
                predicted_amount = total_spent_last_30_days * 1.05
                confidence = 0.0

        else:
            # --- MOCK MODE (Fallback) ---
            # Used if model file is missing OR if user has no transactions
            if total_spent_last_30_days > 0:
                predicted_amount = total_spent_last_30_days * 1.05
            else:
                predicted_amount = 0.0

            confidence = 0.0
            logger.info("Generated prediction using Mock Mode.")

        return {
            "predicted_amount": round(predicted_amount, 2),
            "confidence_score": confidence,
            "currency": "USD"
        }


# Global instance
predictor = SpendingPredictor()