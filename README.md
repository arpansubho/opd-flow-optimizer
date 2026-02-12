# OPD Flow Optimizer

Machine Learning-powered OPD (Outpatient Department) flow optimization system with wait time prediction.

## Features

- **Wait Time Prediction**: ML model predicts patient wait times based on department, priority, and doctor availability
- **Token Management**: Automated token generation and queue management
- **MLOps Dashboard**: Monitor model metrics and trigger retraining
- **Doctor Dashboard**: Real-time view of doctor workload and queue status

## Tech Stack

- **Backend**: FastAPI + Python
- **Frontend**: Streamlit
- **ML Model**: RandomForest (scikit-learn)
- **Data Processing**: Pandas, NumPy

## Setup

### Backend

```bash
cd backend
pip install -r requirements.txt
python model.py  # Train the initial model
python -m uvicorn main:app --host 127.0.0.1 --port 8002
```

### Frontend (Streamlit)

```bash
pip install streamlit
streamlit run streamlit_app.py --server.port=8501
```

## Usage

1. **Start Backend**: `cd backend && python -m uvicorn main:app --port 8002`
2. **Start Frontend**: `streamlit run streamlit_app.py`
3. **Open Browser**: Navigate to http://localhost:8501
4. **Generate Token**: Fill patient details and get wait time prediction

## API Endpoints

- `GET /` - Health check
- `POST /predict` - Predict wait time
- `GET /mlops/metrics` - View model metrics
- `POST /mlops/retrain` - Retrain model

## Project Structure

```
.
├── backend/
│   ├── main.py           # FastAPI application
│   ├── model.py          # ML model training
│   ├── preprocessing.py  # Data preprocessing
│   ├── mlops.py         # MLOps utilities
│   ├── schemas.py       # Pydantic models
│   └── requirements.txt
├── streamlit_app.py     # Streamlit frontend
└── opd_flow_optimizer_synthetic_fixed.xlsx  # Training data
```

## License

MIT
