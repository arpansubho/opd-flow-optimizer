import os
import json
import joblib
from datetime import datetime
from model import train_model

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
METRICS_PATH = os.path.join(BASE_DIR, "artifacts", "model_metrics.json")

def get_model_metrics():
    """Returns the latest model metrics."""
    if not os.path.exists(METRICS_PATH):
        return {"error": "No metrics found. Model might not be trained."}
    
    with open(METRICS_PATH, "r") as f:
        return json.load(f)

def trigger_retraining():
    """Triggers model retraining and returns status."""
    try:
        train_model()
        metrics = get_model_metrics()
        return {
            "status": "Success",
            "message": "Model retrained successfully.",
            "new_metrics": metrics,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        return {
            "status": "Failed",
            "message": str(e),
            "timestamp": datetime.now().isoformat()
        }

def log_prediction(input_data, prediction):
    """Logs prediction for monitoring (mock implementation)."""
    # In a real system, this would write to a database or a file.
    # For MVP, we'll just print or pass.
    pass
