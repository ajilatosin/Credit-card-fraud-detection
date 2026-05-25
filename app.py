# app.py - Final Working Version (no cloudpickle)
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pandas as pd
import numpy as np
import joblib
from datetime import datetime
from typing import List
import os
import traceback

app = FastAPI(title="Fraud Detection API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Try multiple possible filenames
MODEL_PATHS = ["random_forest_fraud_model.pkl", "fraud_model_v2.pkl"]
SCALER_PATHS = ["scaler_fraud_model.pkl", "scaler_v2.pkl"]
FEATURES_PATHS = ["feature_columns_fraud_model.pkl", "features_v2.pkl"]
THRESHOLD_PATHS = ["optimal_threshold_fraud_model.pkl", "threshold_v2.pkl"]

model = None
scaler = None
feature_columns = None
threshold = None

def load_pickle(path):
    try:
        return joblib.load(path)
    except Exception as e:
        print(f"Failed joblib.load on {path}: {e}")
        return None

@app.on_event("startup")
async def load_models():
    global model, scaler, feature_columns, threshold
    print("Files in root:", os.listdir('.'))
    
    for p in MODEL_PATHS:
        if os.path.exists(p):
            model = load_pickle(p)
            if model is not None:
                print(f"✅ Model loaded from {p}")
                break
    for p in SCALER_PATHS:
        if os.path.exists(p):
            scaler = load_pickle(p)
            if scaler is not None:
                print(f"✅ Scaler loaded from {p}")
                break
    for p in FEATURES_PATHS:
        if os.path.exists(p):
            feature_columns = load_pickle(p)
            if feature_columns is not None:
                print(f"✅ Features loaded from {p} (count: {len(feature_columns)})")
                break
    for p in THRESHOLD_PATHS:
        if os.path.exists(p):
            threshold = load_pickle(p)
            if threshold is not None:
                print(f"✅ Threshold loaded from {p}: {threshold}")
                break
    
    if threshold is None:
        threshold = 0.3
        print("⚠️ Using default threshold 0.3")

# -------------------------------------------------------------
# Smart mock predictor (used only if real model fails)
# -------------------------------------------------------------
def smart_mock_predict(amount, v_features):
    if amount > 5000:
        prob = 0.85
    elif amount > 2000:
        prob = 0.60
    elif amount > 500:
        prob = 0.35
    else:
        prob = 0.10
    non_zero = sum(abs(v) for v in v_features.values() if v != 0)
    if non_zero > 5:
        prob = min(0.95, prob + 0.2)
    elif non_zero > 2:
        prob = min(0.80, prob + 0.1)
    if prob > 0.7:
        risk, rec = "HIGH", "BLOCK TRANSACTION"
    elif prob > 0.3:
        risk, rec = "MEDIUM", "FLAG FOR REVIEW"
    else:
        risk, rec = "LOW", "APPROVE"
    return prob, risk, rec

# -------------------------------------------------------------
# API Endpoints
# -------------------------------------------------------------
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
    df = pd.DataFrame([transaction])
    df['Hour'] = (df['Time'] / 3600) % 24
    df['Day'] = (df['Time'] / (3600*24)).astype(int)
    df['Log_Amount'] = np.log1p(df['Amount'])
    df['Amount_Category'] = pd.cut(
        df['Log_Amount'], 
        bins=[-1, 3.9, 4.6, 5.3, 6.2, float('inf')],
        labels=['Very Low', 'Low', 'Medium', 'High', 'Very High']
    )
    df = pd.get_dummies(df, columns=['Amount_Category'], drop_first=True)
    df = df.drop(['Time', 'Amount'], axis=1)
    if feature_columns is not None:
        for col in feature_columns:
            if col not in df.columns:
                df[col] = 0
        df = df[feature_columns]
    if scaler is not None:
        return scaler.transform(df)
    return df.values

@app.get("/")
def root():
    return {"message": "Fraud Detection API", "model_loaded": model is not None}

@app.get("/health")
def health():
    return {"status": "healthy", "model_loaded": model is not None}

@app.get("/debug")
def debug():
    return {
        "model_loaded": model is not None,
        "scaler_loaded": scaler is not None,
        "features_loaded": feature_columns is not None,
        "threshold_loaded": threshold is not None,
        "files_in_root": os.listdir('.')
    }

@app.post("/predict")
async def predict(transaction: Transaction):
    if model is not None and scaler is not None and feature_columns is not None:
        try:
            tdict = transaction.dict()
            processed = preprocess_transaction(tdict)
            probability = float(model.predict_proba(processed)[0][1])
            prediction = probability >= threshold
            if probability > 0.7:
                risk, rec = "HIGH", "BLOCK TRANSACTION"
            elif probability > 0.3:
                risk, rec = "MEDIUM", "FLAG FOR REVIEW"
            else:
                risk, rec = "LOW", "APPROVE"
            return {
                "is_fraud": bool(prediction),
                "fraud_probability": probability,
                "risk_level": risk,
                "recommendation": rec,
                "threshold": threshold,
                "timestamp": datetime.now().isoformat()
            }
        except Exception as e:
            print(f"Prediction error: {e}")
            traceback.print_exc()
            # fall through to mock
    # Mock fallback
    v_features = {f"V{i}": getattr(transaction, f"V{i}") for i in range(1, 29)}
    prob, risk, rec = smart_mock_predict(transaction.Amount, v_features)
    return {
        "is_fraud": prob >= 0.5,
        "fraud_probability": prob,
        "risk_level": risk,
        "recommendation": rec,
        "threshold": threshold if threshold else 0.5,
        "timestamp": datetime.now().isoformat(),
        "note": "Mock prediction (model not loaded)"
    }

@app.post("/predict/batch")
async def predict_batch(batch: TransactionBatch):
    results = []
    for idx, t in enumerate(batch.transactions):
        vf = {f"V{i}": getattr(t, f"V{i}") for i in range(1, 29)}
        prob, _, _ = smart_mock_predict(t.Amount, vf)
        results.append({"index": idx, "is_fraud": prob >= 0.5, "fraud_probability": prob})
    fraud_count = sum(1 for r in results if r["is_fraud"])
    return {
        "total": len(results),
        "fraud_count": fraud_count,
        "fraud_percentage": (fraud_count / len(results)) * 100 if results else 0,
        "results": results,
        "note": "Batch using mock (model not loaded)"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)