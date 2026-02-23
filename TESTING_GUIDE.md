# TrustShield AI - Testing Guide

## Quick Start

### 1. Install Dependencies

**Backend:**
```bash
cd trustshield-ai/backend
pip install -r requirements.txt
```

**Frontend:**
```bash
cd trustshield-ai/frontend
npm install
```

### 2. Start the Application

**Terminal 1 - Backend:**
```bash
cd trustshield-ai/backend
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd trustshield-ai/frontend
npm start
```

The frontend will open at `http://localhost:3000`
The backend API docs will be at `http://127.0.0.1:8000/docs`

---

## Feature Testing Checklist

### ✅ Backend API Tests

#### Test 1: Check Backend is Running
```bash
curl http://127.0.0.1:8000/docs
```
Expected: Should return FastAPI documentation page

#### Test 2: Analyze Call Endpoint
```bash
curl -X POST http://127.0.0.1:8000/analyze-call
```
Expected: Returns transcript and fraud_probability

#### Test 3: Transaction Risk Endpoint
```bash
curl -X POST http://127.0.0.1:8000/transaction-risk
```
Expected: Returns transaction_flag (-1 for anomaly, 1 for normal)

#### Test 4: Final Risk Endpoint
```bash
curl -X POST http://127.0.0.1:8000/final-risk
```
Expected: Returns risk_score and risk_level

### ✅ Frontend Tests

#### Test 1: Dashboard Loads
- Open `http://localhost:3000`
- Should see "TrustShield AI" header
- Should see default transcript text
- Should see risk gauge
- Should see alerts panel

#### Test 2: Run Analysis Button
- Click "Run Analysis" button
- Button should show "Analyzing..."
- After completion, should update:
  - Transcript text
  - Risk score percentage
  - Risk level (Low/Medium/Critical)
  - Alert messages

#### Test 3: API Connection
- Check status pill shows "Live API: http://127.0.0.1:8000"
- If backend is down, should show "Backend unreachable" alert

### ✅ AI Model Tests

#### Test 1: Scam Classifier
Test with sample texts:
- "Urgent! Send money now or your account will be closed" → High fraud score
- "Hello, how can I help you today?" → Low fraud score

#### Test 2: Anomaly Detector
Test transactions:
- `[500, 1, 0]` → Normal (score: 1)
- `[50000, 5, 1]` → Anomaly (score: -1)

#### Test 3: Speech-to-Text
Requires audio file at `demo_assets/scam_call.wav`

---

## Common Issues & Fixes

### Issue: Backend won't start
**Fix:** Install missing dependencies
```bash
pip install fastapi uvicorn pandas scikit-learn numpy openai-whisper torch
```

### Issue: Frontend won't start
**Fix:** Install node modules
```bash
cd trustshield-ai/frontend
npm install
```

### Issue: "Module not found" errors
**Fix:** Check Python path and run from correct directory
```bash
cd trustshield-ai
python -m backend.main
```

### Issue: Whisper model download fails
**Fix:** The first run downloads the Whisper model (~140MB). Ensure internet connection.

### Issue: CORS errors in browser
**Fix:** Add CORS middleware to backend/main.py:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Automated Test Script

Run the automated test script to check all features:
```bash
python test_application.py
```

---

## Expected Behavior

### Low Risk Scenario
- Risk Score: 0-40%
- Risk Level: Low
- Alerts: "Monitoring - no active alerts"

### Medium Risk Scenario
- Risk Score: 40-75%
- Risk Level: Medium
- Alerts: "Voice pattern matches prior scam script"

### Critical Risk Scenario
- Risk Score: 75-100%
- Risk Level: Critical
- Alerts: "Fraud detected - auto block engaged"

---

## Performance Benchmarks

- API Response Time: < 2 seconds
- Frontend Load Time: < 3 seconds
- Model Inference: < 1 second per prediction
