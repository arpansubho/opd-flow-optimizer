import streamlit as st
import pandas as pd
import numpy as np
import joblib
import os
from datetime import datetime, timedelta
from pathlib import Path

# Configure page
st.set_page_config(
    page_title="OPD Flow Optimizer",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #4F46E5;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #4F46E5;
        color: white;
    }
    .metric-card {
        background-color: #F3F4F6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Load Model & Artifacts
@st.cache_resource
def load_model_artifacts():
    """Load ML model and label encoders"""
    try:
        BASE_DIR = Path(__file__).parent
        BACKEND_DIR = BASE_DIR / "backend"
        ARTIFACTS_DIR = BACKEND_DIR / "artifacts"
        
        MODEL_PATH = ARTIFACTS_DIR / "opd_model.pkl"
        
        if not MODEL_PATH.exists():
            st.error(f"❌ Model file not found at: {MODEL_PATH}")
            return None, None
        
        # Load model
        model = joblib.load(MODEL_PATH)
        
        # Load label encoders
        ENCODER_PATH = ARTIFACTS_DIR / "label_encoders.pkl"
        label_encoders = {}
        
        if ENCODER_PATH.exists():
            label_encoders = joblib.load(ENCODER_PATH)
        else:
            st.warning("⚠️ Label encoders not found. Prediction might be limited.")
        
        return model, label_encoders
    except Exception as e:
        st.error(f"Error loading model: {str(e)}")
        return None, None

# Initialize model
model, label_encoders = load_model_artifacts()

# Header
st.markdown('<p class="main-header">🏥 OPD Flow Optimizer</p>', unsafe_allow_html=True)

# Sidebar for MLOps
with st.sidebar:
    st.header("📊 MLOps Panel")
    
    if model:
        st.success("✅ Model Loaded Successfully")
        st.info(f"Model Type: {type(model).__name__}")
        
        if label_encoders:
            st.write("**Available Encoders:**")
            for name in label_encoders.keys():
                st.write(f"- {name}")
    else:
        st.error("❌ Model Not Loaded")
        st.warning("Please ensure model artifacts exist in backend/artifacts/")
    
    st.divider()
    
    # Model info
    st.subheader("ℹ️ About")
    st.write("""
    This application predicts OPD wait times using machine learning.
    
    **Features:**
    - Patient token generation
    - Wait time prediction
    - Doctor assignment
    - Queue management
    """)

# Main content
tab1, tab2 = st.tabs(["🎫 New Patient Token", "👨‍⚕️ Doctor Dashboard"])

with tab1:
    st.subheader("Generate Patient Token")
    
    if not model:
        st.error("⚠️ Cannot generate tokens: Model not loaded")
        st.stop()
    
    col1, col2 = st.columns(2)
    
    with col1:
        department = st.selectbox(
            "Department",
            ["Cardiology", "Orthopedics", "Dermatology", "Pediatrics", "Neurology"]
        )
        
        priority = st.selectbox(
            "Priority",
            ["Normal", "High Priority"]
        )
        
    with col2:
        scheduled_time = st.time_input("Scheduled Time (Optional)", value=datetime.now().time())
        scheduled_date = st.date_input("Scheduled Date (Optional)", value=datetime.now().date())
        
        doctor_id = st.text_input("Doctor Preference (Optional)", placeholder="e.g., DOC_001")
    
    if st.button("🎫 Generate Token", use_container_width=True):
        try:
            # Prepare data
            priority_flag = 1 if priority == "High Priority" else 0
            scheduled_datetime = datetime.combine(scheduled_date, scheduled_time)
            
            # Prepare DataFrame
            data = {
                'Department': [department],
                'PriorityFlag': [priority_flag],
                'DayOfWeek': [scheduled_datetime.weekday()],
                'HourOfDay': [scheduled_datetime.hour],
                'DoctorID': [doctor_id if doctor_id else "UNKNOWN"]
            }
            
            # Simple Routing Logic if DoctorID is missing
            if not doctor_id or doctor_id == "UNKNOWN":
                if label_encoders and 'DoctorID' in label_encoders:
                    known_doctors = label_encoders['DoctorID'].classes_
                    valid_doctors = [d for d in known_doctors if d != 'UNKNOWN']
                    if valid_doctors:
                        data['DoctorID'] = [np.random.choice(valid_doctors)]
                    else:
                        data['DoctorID'] = ["DOC_001"]
                else:
                    data['DoctorID'] = ["DOC_001"]
            
            df = pd.DataFrame(data)
            
            # Encode inputs
            for col, le in label_encoders.items():
                if col in df.columns:
                    try:
                        df[col] = le.transform(df[col].astype(str))
                    except ValueError:
                        # If unseen label, use the first class (0)
                        df[col] = 0
            
            # Predict
            predicted_wait = model.predict(df[['Department', 'PriorityFlag', 'DayOfWeek', 'HourOfDay', 'DoctorID']])[0]
            
            # Post-process
            token_num = np.random.randint(100, 999)
            predicted_consult_time = scheduled_datetime + timedelta(minutes=float(predicted_wait))
            
            # Display results
            st.success("✅ Token Generated Successfully!")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Token Number", token_num)
            
            with col2:
                assigned_doctor = data['DoctorID'][0]
                st.metric("Assigned Doctor", assigned_doctor)
            
            with col3:
                st.metric("Wait Time (min)", f"{predicted_wait:.0f}")
            
            with col4:
                st.metric("Estimated Time", predicted_consult_time.strftime("%H:%M"))
            
            st.divider()
            st.info(f"📋 Please proceed to {department} department and wait for Token #{token_num}")
            
        except Exception as e:
            st.error(f"❌ Error generating token: {str(e)}")
            st.exception(e)

with tab2:
    st.subheader("Doctor Load Dashboard")
    
    # Mock data for dashboard
    mock_doctors = [
        {"Doctor": "Dr. Smith (DOC_001)", "Department": "Cardiology", "Queue": 5, "Avg Wait": "15 min", "Status": "🔴 Busy"},
        {"Doctor": "Dr. Jones (DOC_002)", "Department": "Orthopedics", "Queue": 3, "Avg Wait": "10 min", "Status": "🟢 Available"},
        {"Doctor": "Dr. Emily (DOC_003)", "Department": "Pediatrics", "Queue": 8, "Avg Wait": "25 min", "Status": "🔴 Busy"},
        {"Doctor": "Dr. Brown (DOC_004)", "Department": "Dermatology", "Queue": 2, "Avg Wait": "5 min", "Status": "🟢 Available"},
        {"Doctor": "Dr. Wilson (DOC_005)", "Department": "Neurology", "Queue": 4, "Avg Wait": "12 min", "Status": "🟡 Moderate"},
    ]
    
    df = pd.DataFrame(mock_doctors)
    
    # Display as a styled dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    # Add summary metrics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_queue = sum([d["Queue"] for d in mock_doctors])
        st.metric("Total Queue", total_queue)
    
    with col2:
        avg_wait = np.mean([int(d["Avg Wait"].split()[0]) for d in mock_doctors])
        st.metric("Avg Wait Time", f"{avg_wait:.0f} min")
    
    with col3:
        available_docs = len([d for d in mock_doctors if "Available" in d["Status"]])
        st.metric("Available Doctors", available_docs)
    
    st.info("📊 This is mock data. Real-time queue tracking would require additional backend implementation.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 1rem;'>
    <p>OPD Flow Optimizer | Standalone Streamlit Application</p>
    <p style='font-size: 0.8rem;'>No backend server required - ML model runs directly in the app</p>
</div>
""", unsafe_allow_html=True)
