from fastapi.testclient import TestClient
from main import app
import os
from datetime import datetime


def run_tests():
    with TestClient(app) as client:
        def test_read_root():
            response = client.get("/")
            assert response.status_code == 200
            assert response.json() == {"message": "OPD Flow Optimizer API is running"}

        def test_predict():
            payload = {
                "Department": "Cardiology",
                "PriorityFlag": 0,
                "ScheduledTime": datetime.now().isoformat(),
                "DoctorID": "DOC_001"
            }
            response = client.post("/predict", json=payload)
            if response.status_code != 200:
                print(response.json())
            assert response.status_code == 200
            data = response.json()
            assert "TokenNumber" in data
            assert "WaitTime_Minutes" in data
            assert "DoctorID" in data

        def test_metrics():
            response = client.get("/mlops/metrics")
            assert response.status_code == 200
            data = response.json()
            assert "model_version" in data
            assert "rmse" in data

        def test_retrain():
            # This might take a while, so we just check if endpoint exists and returns valid structure
            # For smoke test, maybe skip actual training if it's heavy, but our model is small.
            response = client.post("/mlops/retrain")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "Success"
            assert data["model_version"] == "v1.1"

        test_read_root()
        print("Root endpoint: PASS")
        test_predict()
        print("Prediction endpoint: PASS")
        test_metrics()
        print("Metrics endpoint: PASS")
        # test_retrain() # Skip retrain to avoid changing state during test or long wait
        # print("Retraining endpoint: PASS")
        print("All smoke tests passed!")

if __name__ == "__main__":
    try:
        run_tests()
    except Exception as e:
        print(f"Smoke tests failed: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
