import streamlit as st
import requests
from datetime import datetime
import pandas as pd

# Configure page
st.set_page_config(
    page_title="OPD Flow Optimizer",
    page_icon="🏥",
    layout="wide"
)

# API Configuration
API_BASE_URL = "http://127.0.0.1:8002"

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

# Header
st.markdown('<p class="main-header">🏥 OPD Flow Optimizer</p>', unsafe_allow_html=True)

# Sidebar for MLOps
with st.sidebar:
    st.header("📊 MLOps Panel")
    
    if st.button("🔄 Refresh Metrics"):
        try:
            response = requests.get(f"{API_BASE_URL}/mlops/metrics")
            if response.status_code == 200:
                metrics = response.json()
                st.success("Metrics loaded successfully!")
                st.json(metrics)
            else:
                st.error(f"Failed to load metrics: {response.status_code}")
        except Exception as e:
            st.error(f"Error: {str(e)}")
    
    st.divider()
    
    if st.button("🎯 Retrain Model"):
        with st.spinner("Retraining model..."):
            try:
                response = requests.post(f"{API_BASE_URL}/mlops/retrain")
                if response.status_code == 200:
                    result = response.json()
                    st.success(f"Status: {result['status']}")
                    st.info(f"Model Version: {result['model_version']}")
                else:
                    st.error(f"Failed to retrain: {response.status_code}")
            except Exception as e:
                st.error(f"Error: {str(e)}")

# Main content
tab1, tab2 = st.tabs(["🎫 New Patient Token", "👨‍⚕️ Doctor Dashboard"])

with tab1:
    st.subheader("Generate Patient Token")
    
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
        scheduled_time = st.time_input("Scheduled Time (Optional)")
        scheduled_date = st.date_input("Scheduled Date (Optional)")
        
        doctor_id = st.text_input("Doctor Preference (Optional)", placeholder="e.g., DOC_001")
    
    if st.button("🎫 Generate Token", use_container_width=True):
        # Prepare payload
        priority_flag = 1 if priority == "High Priority" else 0
        scheduled_datetime = datetime.combine(scheduled_date, scheduled_time).isoformat()
        
        payload = {
            "Department": department,
            "PriorityFlag": priority_flag,
            "ScheduledTime": scheduled_datetime,
            "DoctorID": doctor_id if doctor_id else None
        }
        
        with st.spinner("Generating token..."):
            try:
                response = requests.post(f"{API_BASE_URL}/predict", json=payload)
                
                if response.status_code == 200:
                    result = response.json()
                    
                    st.success("✅ Token Generated Successfully!")
                    
                    # Display results in columns
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric("Token Number", result["TokenNumber"])
                    
                    with col2:
                        st.metric("Assigned Doctor", result["DoctorID"])
                    
                    with col3:
                        st.metric("Wait Time (min)", f"{result['WaitTime_Minutes']:.0f}")
                    
                    with col4:
                        consult_time = datetime.fromisoformat(result["PredictedConsultTime"])
                        st.metric("Estimated Time", consult_time.strftime("%H:%M"))
                    
                    st.divider()
                    st.info(f"📋 Please proceed to {department} department and wait for Token #{result['TokenNumber']}")
                    
                else:
                    st.error(f"❌ Error: {response.json().get('detail', 'Unknown error')}")
                    
            except requests.exceptions.ConnectionError:
                st.error("❌ Cannot connect to backend server. Please ensure it's running on http://127.0.0.1:8002")
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")

with tab2:
    st.subheader("Doctor Load Dashboard")
    
    # Mock data for dashboard (since we don't have a real-time queue system)
    mock_doctors = [
        {"Doctor": "Dr. Smith (DOC_001)", "Department": "Cardiology", "Queue": 5, "Avg Wait": "15 min", "Status": "Busy"},
        {"Doctor": "Dr. Jones (DOC_002)", "Department": "Orthopedics", "Queue": 3, "Avg Wait": "10 min", "Status": "Available"},
        {"Doctor": "Dr. Emily (DOC_003)", "Department": "Pediatrics", "Queue": 8, "Avg Wait": "25 min", "Status": "Busy"},
        {"Doctor": "Dr. Brown (DOC_004)", "Department": "Dermatology", "Queue": 2, "Avg Wait": "5 min", "Status": "Available"},
    ]
    
    df = pd.DataFrame(mock_doctors)
    
    # Display as a styled dataframe
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True
    )
    
    st.info("📊 This is mock data. Real-time queue tracking would require additional backend implementation.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #6B7280; padding: 1rem;'>
    <p>OPD Flow Optimizer | Backend API: http://127.0.0.1:8002</p>
</div>
""", unsafe_allow_html=True)
