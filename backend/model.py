import pandas as pd
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error
import os
import json
from preprocessing import load_data, preprocess_data, save_processors

# Configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# Data path relative to backend or project root
# Assuming data file is in project root, backend is in backend/
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DATA_PATH = os.path.join(PROJECT_ROOT, "opd_flow_optimizer_synthetic_fixed.xlsx")
MODEL_DIR = os.path.join(BASE_DIR, "artifacts")
MODEL_PATH = os.path.join(MODEL_DIR, "opd_model.pkl")
METRICS_PATH = os.path.join(MODEL_DIR, "model_metrics.json")

def train_model():
    print("Loading data...")
    df = load_data(DATA_PATH)
    
    print("Preprocessing data...")
    X_train, X_test, y_train, y_test, label_encoders = preprocess_data(df)
    
    print("Training model...")
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    
    print("Evaluating model...")
    y_pred = model.predict(X_test)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    mae = mean_absolute_error(y_test, y_pred)
    
    print(f"RMSE: {rmse:.2f}")
    print(f"MAE: {mae:.2f}")
    
    # Save Artifacts
    print("Saving artifacts...")
    os.makedirs(MODEL_DIR, exist_ok=True)
    joblib.dump(model, MODEL_PATH)
    save_processors(label_encoders, MODEL_DIR)
    
    # Save Metrics
    metrics = {
        "rmse": rmse,
        "mae": mae,
        "model_version": "v1.0",
        "description": "RandomForestRegressor trained on synthetic data"
    }
    with open(METRICS_PATH, "w") as f:
        json.dump(metrics, f, indent=4)
        
    print("Training complete.")

if __name__ == "__main__":
    train_model()
