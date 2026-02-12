import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
import joblib
import os

def load_data(file_path):
    """Loads dataset from Excel file."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    return pd.read_excel(file_path)

def preprocess_data(df):
    """
    Cleans and processes data for training.
    Returns X_train, X_test, y_train, y_test, label_encoders, scaler
    """
    # Feature Engineering
    df['ScheduledTime'] = pd.to_datetime(df['ScheduledTime'])
    df['DayOfWeek'] = df['ScheduledTime'].dt.dayofweek
    df['HourOfDay'] = df['ScheduledTime'].dt.hour
    
    # Select Features and Target
    features = ['Department', 'PriorityFlag', 'DayOfWeek', 'HourOfDay', 'DoctorID']
    target = 'WaitTime_Minutes'
    
    # Drop rows with missing target or features
    df = df.dropna(subset=features + [target])
    
    X = df[features].copy()
    y = df[target].copy()
    
    # Encoding Categorical Variables
    label_encoders = {}
    for col in ['Department', 'DoctorID']:
        le = LabelEncoder()
        X[col] = le.fit_transform(X[col].astype(str))
        label_encoders[col] = le
        
    # Splitting Data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scaling Numerical Features (Optional for RF, but good for others)
    # We will just scale for consistency
    scaler = StandardScaler()
    # Identifying numerical columns (Priority, Day, Hour are ordinal/numeric enough)
    # Actually just scale everything for simplicity or leave as is. 
    # RF doesn't strictly need scaling, but we'll do it for potential model switch.
    # For this simple MVP, let's skip scaling to keep inference simple, or use it. 
    # Let's use it for 'PriorityFlag', 'DayOfWeek', 'HourOfDay' 
    
    # To keep it simple for the first iteration and "Simple Data Schema", 
    # we will skip scaling as RandomForest handles unscaled data well.
    
    return X_train, X_test, y_train, y_test, label_encoders

def save_processors(label_encoders, output_dir=None):
    """Saves label encoders for inference."""
    if output_dir is None:
        output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")
    os.makedirs(output_dir, exist_ok=True)
    joblib.dump(label_encoders, os.path.join(output_dir, "label_encoders.pkl"))

def load_processors(input_dir=None):
    """Loads label encoders."""
    if input_dir is None:
        input_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "artifacts")
    path = os.path.join(input_dir, "label_encoders.pkl")
    if not os.path.exists(path):
        return None
    return joblib.load(path)
