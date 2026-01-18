from pydantic import BaseModel
from typing import Literal

class CustomerData(BaseModel):
    gender: Literal['Male', 'Female']
    SeniorCitizen: int
    Partner: Literal['Yes', 'No']
    Dependents: Literal['Yes', 'No']
    tenure: int
    PhoneService: Literal['Yes', 'No']
    MultipleLines: Literal['No phone service', 'No', 'Yes']
    InternetService: Literal['DSL', 'Fiber optic', 'No']
    OnlineSecurity: Literal['No internet service', 'No', 'Yes']
    OnlineBackup: Literal['No internet service', 'No', 'Yes']
    DeviceProtection: Literal['No internet service', 'No', 'Yes']
    TechSupport: Literal['No internet service', 'No', 'Yes']
    StreamingTV: Literal['No internet service', 'No', 'Yes']
    StreamingMovies: Literal['No internet service', 'No', 'Yes']
    Contract: Literal['Month-to-month', 'One year', 'Two year']
    PaperlessBilling: Literal['Yes', 'No']
    PaymentMethod: Literal['Electronic check', 'Mailed check', 'Bank transfer (automatic)', 'Credit card (automatic)']
    MonthlyCharges: float
    TotalCharges: float | str # Can be string with space, we handle this in preprocessing

class PredictionResult(BaseModel):
    churn_prediction: int
    churn_probability: float
    churn_label: str
