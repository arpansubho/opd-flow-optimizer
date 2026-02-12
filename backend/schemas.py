from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class PatientBase(BaseModel):
    Department: str
    PriorityFlag: int
    ScheduledTime: datetime
    # We might infer Day/Hour from ScheduledTime, but for input we just need these.
    # If DoctorID is optional (assigned by system), we make it optional.
    DoctorID: Optional[str] = None

class PredictionRequest(PatientBase):
    pass

class PredictionResponse(BaseModel):
    TokenNumber: int
    DoctorID: str
    WaitTime_Minutes: float
    PredictedConsultTime: datetime

class RetrainResponse(BaseModel):
    status: str
    model_version: str
    metrics: dict
