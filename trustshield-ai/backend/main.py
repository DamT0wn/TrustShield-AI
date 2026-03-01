from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import random

from ai_models.call_analyzer import analyzer

app = FastAPI(title="TrustShield AI - Fraud Detection API")

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request models
class AnalyzeCallRequest(BaseModel):
    audio_path: Optional[str] = None
    transcript: Optional[str] = None
    demo_scenario: Optional[str] = None

class TransactionRiskRequest(BaseModel):
    amount: float = 50000
    frequency: int = 3
    is_international: int = 1

class FullAnalysisRequest(BaseModel):
    audio_path: Optional[str] = None
    transcript: Optional[str] = None
    transaction_data: Optional[List[float]] = None
    demo_scenario: Optional[str] = None

@app.get("/")
def root():
    """API health check."""
    return {
        "status": "online",
        "service": "TrustShield AI Fraud Detection",
        "version": "2.0",
        "endpoints": [
            "/analyze-call",
            "/transaction-risk", 
            "/final-risk",
            "/full-analysis",
            "/demo-scenarios"
        ]
    }

@app.get("/demo-scenarios")
def get_demo_scenarios():
    """Get available demo scenarios for testing."""
    scenarios = analyzer.demo_scenarios
    return {
        "scenarios": list(scenarios.keys()),
        "details": {
            name: {
                "expected_risk": data["expected_risk"],
                "has_transaction": data["transaction"][0] > 0
            }
            for name, data in scenarios.items()
        }
    }

@app.post("/analyze-call")
def analyze_call(request: AnalyzeCallRequest = None):
    """
    Analyze call audio or transcript for scam indicators.
    Supports demo scenarios for reliable testing.
    """
    try:
        # Handle both request body and no body (backward compatibility)
        if request is None:
            request = AnalyzeCallRequest()
        
        # Use demo scenario if specified
        if request.demo_scenario:
            scenario = analyzer.demo_scenarios.get(request.demo_scenario)
            if scenario:
                transcript = scenario["transcript"]
            else:
                transcript = request.transcript
        else:
            transcript = request.transcript
        
        # Analyze transcript
        if transcript:
            result = analyzer.analyze_transcript(transcript)
        else:
            # Use audio file or default demo
            transcript, confidence = analyzer.analyze_audio_file(request.audio_path)
            result = analyzer.analyze_transcript(transcript)
            result["audio_confidence"] = confidence
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

@app.post("/transaction-risk")
def transaction_risk(request: TransactionRiskRequest = None):
    """Analyze transaction for anomalies."""
    try:
        if request is None:
            request = TransactionRiskRequest()
        
        result = analyzer.analyze_transaction(
            request.amount,
            request.frequency,
            request.is_international
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transaction analysis failed: {str(e)}")

@app.post("/final-risk")
def final_risk():
    """
    Calculate final risk score (backward compatible endpoint).
    Uses sample data for demonstration.
    """
    try:
        # Use sample data
        voice_analysis = {
            "fraud_probability": 0.85,
            "confidence": 0.90,
            "risk_factors": ["Urgency language detected", "Requesting sensitive information"]
        }
        
        transaction_analysis = {
            "anomaly_flag": -1,
            "is_anomalous": True,
            "risk_indicators": ["Large transaction amount: $50,000.00"]
        }
        
        result = analyzer.calculate_final_risk(voice_analysis, transaction_analysis)
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Risk calculation failed: {str(e)}")

@app.post("/full-analysis")
def full_analysis(request: FullAnalysisRequest = None):
    """
    Run complete end-to-end fraud detection pipeline.
    This is the main endpoint for comprehensive analysis.
    """
    try:
        if request is None:
            # Use random demo scenario for testing
            scenarios = list(analyzer.demo_scenarios.keys())
            demo_scenario = random.choice(scenarios)
            request = FullAnalysisRequest(demo_scenario=demo_scenario)
        
        result = analyzer.run_full_analysis(
            audio_path=request.audio_path,
            transcript=request.transcript,
            transaction_data=request.transaction_data,
            demo_scenario=request.demo_scenario
        )
        
        return result
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Full analysis failed: {str(e)}")

