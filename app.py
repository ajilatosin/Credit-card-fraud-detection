# app.py - FastAPI Backend
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from typing import List
import os

# Initialize FastAPI
app = FastAPI(title="Fraud Detection API")

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load models (update path as needed)
MODEL_PATH = "models/random_forest_fraud_model.pkl"
SCALER_PATH = "models/scaler_fraud_model.pkl"
FEATURES_PATH = "models/feature_columns_fraud_model.pkl"
THRESHOLD_PATH = "models/optimal_threshold_fraud_model.pkl"

# Global variables
model = None
scaler = None
feature_columns = None
threshold = None

# Load models on startup
try:
    model = joblib.load(MODEL_PATH)
    scaler = joblib.load(SCALER_PATH)
    feature_columns = joblib.load(FEATURES_PATH)
    threshold = joblib.load(THRESHOLD_PATH)
    print("✅ Models loaded successfully!")
except Exception as e:
    print(f"❌ Error loading models: {e}")

# Define request/response models
class Transaction(BaseModel):
    Time: float
    V1: float = 0.0
    V2: float = 0.0
    V3: float = 0.0
    V4: float = 0.0
    V5: float = 0.0
    V6: float = 0.0
    V7: float = 0.0
    V8: float = 0.0
    V9: float = 0.0
    V10: float = 0.0
    V11: float = 0.0
    V12: float = 0.0
    V13: float = 0.0
    V14: float = 0.0
    V15: float = 0.0
    V16: float = 0.0
    V17: float = 0.0
    V18: float = 0.0
    V19: float = 0.0
    V20: float = 0.0
    V21: float = 0.0
    V22: float = 0.0
    V23: float = 0.0
    V24: float = 0.0
    V25: float = 0.0
    V26: float = 0.0
    V27: float = 0.0
    V28: float = 0.0
    Amount: float

class TransactionBatch(BaseModel):
    transactions: List[Transaction]

def preprocess_transaction(transaction: dict):
    """Preprocess transaction for prediction"""
    df = pd.DataFrame([transaction])
    
    # Add engineered features
    df['Hour'] = (df['Time'] / 3600) % 24
    df['Day'] = (df['Time'] / (3600*24)).astype(int)
    df['Log_Amount'] = np.log1p(df['Amount'])
    
    # Add amount category
    df['Amount_Category'] = pd.cut(
        df['Log_Amount'], 
        bins=[-1, 3.9, 4.6, 5.3, 6.2, float('inf')],
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
    )
    
    # One-hot encode
    df = pd.get_dummies(df, columns=['Amount_Category'], drop_first=True)
    
    # Drop original columns
    df = df.drop(['Time', 'Amount'], axis=1)
    
    # Align columns
    for col in feature_columns:
        if col not in df.columns:
            df[col] = 0
    
    df = df[feature_columns]
    
    # Scale
    scaled = scaler.transform(df)
    
    return scaled

@app.get("/")
def root():
    return {
        "message": "Credit Card Fraud Detection API",
        "status": "active",
        "model_loaded": model is not None
    }

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.post("/predict")
async def predict(transaction: Transaction):
    """Predict fraud for a single transaction"""
    try:
        # Convert to dict
        transaction_dict = transaction.dict()
        
        # Preprocess
        processed = preprocess_transaction(transaction_dict)
        
        # Predict
        probability = float(model.predict_proba(processed)[0][1])
        prediction = probability >= threshold
        
        # Risk assessment
        if probability > 0.7:
            risk_level = "HIGH"
            recommendation = "BLOCK TRANSACTION"
        elif probability > 0.3:
            risk_level = "MEDIUM"
            recommendation = "FLAG FOR REVIEW"
        else:
            risk_level = "LOW"
            recommendation = "APPROVE"
        
        return {
            "is_fraud": bool(prediction),
            "fraud_probability": probability,
            "risk_level": risk_level,
            "recommendation": recommendation,
            "threshold": threshold,
            "timestamp": datetime.now().isoformat()
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict/batch")
async def predict_batch(batch: TransactionBatch):
    """Predict fraud for multiple transactions"""
    try:
        results = []
        fraud_count = 0
        
        for idx, transaction in enumerate(batch.transactions):
            transaction_dict = transaction.dict()
            processed = preprocess_transaction(transaction_dict)
            probability = float(model.predict_proba(processed)[0][1])
            prediction = probability >= threshold
            
            if prediction:
                fraud_count += 1
            
            results.append({
                "index": idx,
                "is_fraud": bool(prediction),
                "fraud_probability": probability
            })
        
        return {
            "total": len(results),
            "fraud_count": fraud_count,
            "fraud_percentage": (fraud_count / len(results)) * 100 if results else 0,
            "results": results
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    # FIXED: Changed from 127.0.0.1 to 0.0.0.0 for Docker compatibility
    uvicorn.run(app, host="0.0.0.0", port=8000)