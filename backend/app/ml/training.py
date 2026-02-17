import os
import pickle
import random
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Define where to save the model
MODEL_PATH = "app/ml/models/spending_predictor_v1.pkl"
os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)


def generate_synthetic_data(num_samples=2000):
    """
    Generates dummy financial data to train the initial model.
    Features (X):
        - Total spend last 30 days
        - Number of transactions
    Target (y):
        - Total spend next 30 days
    """
    X = []
    y = []

    for _ in range(num_samples):
        # Simulate a user's monthly spending (e.g., between $500 and $5000)
        current_spend = random.uniform(500, 5000)

        # Simulate transaction count (e.g., average transaction is ~$50)
        tx_count = int(current_spend / random.uniform(20, 100))

        # Simulate next month's spending based on current patterns + randomness
        # Logic: Spending usually fluctuates by +/- 20% month over month
        change_factor = random.uniform(0.8, 1.2)
        next_month_spend = current_spend * change_factor

        # Add noise (unexpected expenses)
        if random.random() > 0.9:  # 10% chance of a big spike
            next_month_spend += random.uniform(200, 800)

        X.append([current_spend, tx_count])
        y.append(next_month_spend)

    return np.array(X), np.array(y)


def train_and_save_model():
    print("Generating synthetic training data...")
    X, y = generate_synthetic_data()

    # Split data to test accuracy
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    print(f"Training RandomForestRegressor on {len(X_train)} samples...")
    # Initialize scikit-learn model
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)

    # Validate
    predictions = model.predict(X_test)
    mae = mean_absolute_error(y_test, predictions)
    print(f"Model Training Complete. Mean Absolute Error: ${mae:.2f}")

    # Save to disk
    print(f"Saving model to {MODEL_PATH}...")
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print("Done.")


if __name__ == "__main__":
    train_and_save_model()