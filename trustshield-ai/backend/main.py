from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
import random
import os
import shutil
from pathlib import Path

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

# Create uploads directory if it doesn't exist
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

# Allowed audio file extensions
ALLOWED_EXTENSIONS = {".mp3", ".wav", ".ogg", ".m4a", ".flac", ".aac"}
MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB

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
            "/demo-scenarios",
            "/upload-audio"
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

@app.post("/upload-audio")
async def upload_audio(file: UploadFile = File(...)):
    """
    Upload and analyze audio file.
    Supports: mp3, wav, ogg, m4a, flac, aac
    Max size: 50MB
    """
    try:
        # Validate file extension
        file_ext = Path(file.filename).suffix.lower()
        if file_ext not in ALLOWED_EXTENSIONS:
            raise HTTPException(
                status_code=400,
                detail=f"Invalid file type. Allowed: {', '.join(ALLOWED_EXTENSIONS)}"
            )
        
        # Read file content
        contents = await file.read()
        file_size = len(contents)
        
        # Validate file size
        if file_size > MAX_FILE_SIZE:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Max size: {MAX_FILE_SIZE / (1024*1024)}MB"
            )
        
        if file_size == 0:
            raise HTTPException(
                status_code=400,
                detail="Empty file uploaded"
            )
        
        # Generate unique filename
        import time
        timestamp = int(time.time())
        safe_filename = f"{timestamp}_{file.filename}"
        file_path = UPLOAD_DIR / safe_filename
        
        # Save file
        with open(file_path, "wb") as f:
            f.write(contents)
        
        # Analyze the audio file
        try:
            result = analyzer.run_full_analysis(
                audio_path=str(file_path),
                transaction_data=None
            )
            
            # Add file info to result
            result["file_info"] = {
                "filename": file.filename,
                "size": file_size,
                "format": file_ext,
                "saved_as": safe_filename
            }
            
            return result
            
        except Exception as e:
            # If analysis fails, clean up file and raise error
            if file_path.exists():
                file_path.unlink()
            raise HTTPException(
                status_code=500,
                detail=f"Audio analysis failed: {str(e)}"
            )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Upload failed: {str(e)}"
        )

@app.delete("/upload-audio/{filename}")
async def delete_uploaded_audio(filename: str):
    """Delete uploaded audio file."""
    try:
        file_path = UPLOAD_DIR / filename
        if file_path.exists():
            file_path.unlink()
            return {"status": "deleted", "filename": filename}
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/analyze-call")
def analyze_call(request: AnalyzeCallRequest = None):
    """
    Analyze call audio or transcript for scam indicators.
    Supports demo scenarios for reliable testing.
    """
    try:
        if request is None:
            request = AnalyzeCallRequest()
        
        if request.demo_scenario:
            scenario = analyzer.demo_scenarios.get(request.demo_scenario)
            if scenario:
                transcript = scenario["transcript"]
            else:
                transcript = request.transcript
        else:
            transcript = request.transcript
        
        if transcript:
            result = analyzer.analyze_transcript(transcript)
        else:
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

