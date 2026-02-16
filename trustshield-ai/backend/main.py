from fastapi import FastAPI

from ai_models.speech_to_text import transcribe_audio
from ai_models.scam_classifier import predict_scam
from ai_models.anomaly_detector import detect_anomaly
from backend.services.risk_engine import calculate_risk

app = FastAPI()

@app.post("/analyze-call")

def analyze_call():

    transcript = transcribe_audio("demo_assets/scam_call.wav")

    fraud_prob = predict_scam(transcript)

    return {
        "transcript": transcript,
        "fraud_probability": fraud_prob
    }

@app.post("/transaction-risk")

def transaction_risk():

    flag = detect_anomaly([50000, 3, 1])

    return {"transaction_flag": flag}

@app.post("/final-risk")

def final_risk():

    voice_prob = 0.85
    transaction_flag = -1

    score, level = calculate_risk(
        voice_prob,
        transaction_flag
    )

    return {
        "risk_score": score,
        "risk_level": level
    }

