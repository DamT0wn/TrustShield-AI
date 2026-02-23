from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from ai_models.speech_to_text import transcribe_audio
from ai_models.scam_classifier import predict_scam
from ai_models.anomaly_detector import detect_anomaly
from backend.services.risk_engine import calculate_risk

app = FastAPI()

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze-call")

def analyze_call():
    
    # Use sample transcript if audio file doesn't exist
    try:
        transcript = transcribe_audio("demo_assets/scam_call.wav")
    except Exception as e:
        # Fallback to sample scam transcript
        transcript = "Hello, this is calling from your bank security department. We've detected suspicious activity on your account. You need to verify your account immediately by providing your account number and PIN. If you don't act now, your account will be frozen within 24 hours. Please transfer your funds to a secure account we'll provide."

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

