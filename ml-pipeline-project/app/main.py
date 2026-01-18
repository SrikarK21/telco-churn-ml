import pandas as pd
import joblib
from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager
from pathlib import Path
import sys

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

from src.config import MODEL_PATH
from app.schemas import CustomerData, PredictionResult

ml_models = {}

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load model
    if not MODEL_PATH.exists():
        raise RuntimeError(f"Model not found at {MODEL_PATH}. Please train the model first.")
    
    ml_models["model"] = joblib.load(MODEL_PATH)
    print("Model loaded successfully.")
    yield
    # Clean up if needed
    ml_models.clear()

app = FastAPI(lifespan=lifespan, title="Telco Customer Churn Prediction API")

@app.get("/")
def read_root():
    return RedirectResponse(url="/docs")

@app.get("/health")
def health_check():
    return {"status": "ok", "model_loaded": "model" in ml_models}

@app.post("/predict", response_model=PredictionResult)
def predict(data: CustomerData):
    if "model" not in ml_models:
        raise HTTPException(status_code=503, detail="Model not loaded")
    
    model = ml_models["model"]
    
    # Convert input to DataFrame
    input_data = data.model_dump()
    df = pd.DataFrame([input_data])
    
    # Preprocessing is handled by the pipeline inside the model
    try:
        prediction = model.predict(df)[0]
        probability = model.predict_proba(df)[0][1] # Probability of Churn=1
        
        return {
            "churn_prediction": int(prediction),
            "churn_probability": float(probability),
            "churn_label": "Yes" if prediction == 1 else "No"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
