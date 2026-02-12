from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
import joblib
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from schemas import PatientBase, PredictionResponse, RetrainResponse
from mlops import get_model_metrics, trigger_retraining, log_prediction
from preprocessing import load_processors
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="OPD Flow Optimizer API", version="1.0")

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load Model & Artifacts
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)
FRONTEND_DIST = os.path.join(PROJECT_ROOT, "frontend", "dist")
MODEL_PATH = os.path.join(BASE_DIR, "artifacts", "opd_model.pkl")
LABEL_ENCODERS_PATH = os.path.join(BASE_DIR, "artifacts")

model = None
label_encoders = None

def load_model_artifacts():
    global model, label_encoders
    if os.path.exists(MODEL_PATH):
        model = joblib.load(MODEL_PATH)
        label_encoders = load_processors(LABEL_ENCODERS_PATH)
    else:
        print("Model not found. Please train the model first.")

@app.on_event("startup")
async def startup_event():
    load_model_artifacts()

@app.get("/")
def read_root():
    return {"message": "OPD Flow Optimizer API is running"}

@app.post("/predict", response_model=PredictionResponse)
def predict_wait_time(patient: PatientBase):
    if not model or not label_encoders:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    # Preprocess Input
    try:
        # Prepare DataFrame
        data = {
            'Department': [patient.Department],
            'PriorityFlag': [patient.PriorityFlag],
            'DayOfWeek': [patient.ScheduledTime.weekday()],
            'HourOfDay': [patient.ScheduledTime.hour],
            'DoctorID': [patient.DoctorID] if patient.DoctorID else ["UNKNOWN"] 
        }
        
        # Simple Routing Logic if DoctorID is missing
        if not patient.DoctorID or patient.DoctorID == "UNKNOWN":
            # Assign a doctor if one isn't specified.
            # In a real system, this would check availability.
            # For MVP, pick a random doctor from the known doctors.
            if label_encoders and 'DoctorID' in label_encoders:
                # Pick a random doctor from trained classes
                known_doctors = label_encoders['DoctorID'].classes_
                # Filter out 'UNKNOWN' if it exists in classes
                valid_doctors = [d for d in known_doctors if d != 'UNKNOWN']
                if valid_doctors:
                    data['DoctorID'] = [np.random.choice(valid_doctors)]
                else:
                    data['DoctorID'] = ["DOC_001"]
            else:
                data['DoctorID'] = ["DOC_001"] # Fallback
        
        df = pd.DataFrame(data)
        
        # Encode inputs
        for col, le in label_encoders.items():
            if col in df.columns:
                # Handle unseen labels by assigning a default or mode
                try:
                    df[col] = le.transform(df[col].astype(str))
                except ValueError:
                    # If unseen label, use the first class (0)
                    df[col] = 0

        # Predict
        predicted_wait = model.predict(df[['Department', 'PriorityFlag', 'DayOfWeek', 'HourOfDay', 'DoctorID']])[0]
        
        # Post-process
        token_num = np.random.randint(100, 999) # Simulated token
        predicted_consult_time = patient.ScheduledTime + timedelta(minutes=float(predicted_wait))
        
        response = PredictionResponse(
            TokenNumber=token_num,
            DoctorID=data['DoctorID'][0] if isinstance(data['DoctorID'][0], str) else "DOC_ASSIGNED", # Simplified
            WaitTime_Minutes=float(predicted_wait),
            PredictedConsultTime=predicted_consult_time
        )
        
        log_prediction(patient.dict(), response.dict())
        return response
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/mlops/metrics")
def get_metrics():
    return get_model_metrics()

@app.post("/mlops/retrain", response_model=RetrainResponse)
def retrain_model_endpoint():
    result = trigger_retraining()
    # Reload model after retraining
    load_model_artifacts()
    return RetrainResponse(
        status=result["status"],
        model_version="v1.1" if result["status"] == "Success" else "v1.0", # Mock version increment
        metrics=result.get("new_metrics", {})
    )

# Serve Frontend disabled - use separate dev server or build
# if os.path.exists(FRONTEND_DIST):
#     app.mount("/", StaticFiles(directory=FRONTEND_DIST, html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
