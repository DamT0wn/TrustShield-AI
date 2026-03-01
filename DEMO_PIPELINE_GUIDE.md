# TrustShield AI - Complete Demo Pipeline Guide

## 🎯 Overview

This guide covers the complete call-analysis demo pipeline for hackathon demonstrations:

**Pipeline Flow:**
```
Audio Call → Transcript → Scam Detection → Transaction Risk → Fraud Score → Alert → Dashboard
```

## 🚀 Quick Start for Demo

### 1. Start the Application

```bash
# Option A: Use batch files (Windows)
1. Double-click `start_backend.bat`
2. Double-click `start_frontend.bat`

# Option B: Manual start
# Terminal 1 - Backend
cd trustshield-ai/backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000

# Terminal 2 - Frontend
cd trustshield-ai/frontend
npm start
```

### 2. Test the Pipeline

```bash
# Run comprehensive test suite
python demo_test.py
```

### 3. Access the Dashboard

- Frontend: http://localhost:3000
- Backend API: http://127.0.0.1:8000
- API Documentation: http://127.0.0.1:8000/docs

---

## 📊 Demo Scenarios

The system includes 6 pre-configured scenarios for reliable demonstrations:

### High-Risk Scenarios (Critical)

1. **Bank Scam**
   - Impersonates bank security
   - Requests account credentials
   - Threatens account freeze
   - Large wire transfer ($50,000)

2. **IRS Scam**
   - Impersonates IRS agent
   - Threatens arrest/legal action
   - Demands immediate payment
   - Uses urgency tactics

3. **Tech Support Scam**
   - Impersonates Microsoft support
   - Requests remote access
   - Demands payment for "protection"
   - Uses technical jargon

4. **Grandparent Scam**
   - Impersonates family member
   - Creates emergency situation
   - Requests secrecy
   - Demands immediate money transfer

### Low-Risk Scenarios (Legitimate)

5. **Legitimate Call**
   - Doctor's office appointment reminder
   - Professional tone
   - No urgency or threats
   - No financial requests

6. **Legitimate Business**
   - Business follow-up call
   - Professional communication
   - No pressure tactics
   - Standard business inquiry

---

## 🔧 Technical Architecture

### Backend Components

#### 1. Enhanced Scam Classifier (`enhanced_scam_classifier.py`)
- **ML Model**: Logistic Regression with TF-IDF vectorization
- **Features**: 
  - Keyword detection (30+ scam indicators)
  - Urgency language analysis
  - Sensitive information requests
  - Threat language detection
- **Output**: Probability, confidence, risk factors

#### 2. Call Analyzer (`call_analyzer.py`)
- **Complete Pipeline Orchestration**
- **Functions**:
  - Audio transcription (Whisper integration)
  - Transcript analysis
  - Transaction risk assessment
  - Final risk calculation
- **Demo Mode**: Pre-configured scenarios for reliable testing

#### 3. Risk Engine (`risk_engine.py`)
- **Multi-factor Risk Assessment**
- **Weighted Scoring**:
  - Voice analysis: 65%
  - Transaction analysis: 35%
- **Risk Levels**: Critical, Medium, Low, Minimal
- **Confidence Weighting**: Adjusts scores based on analysis confidence

#### 4. API Endpoints (`main.py`)

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/` | GET | Health check |
| `/demo-scenarios` | GET | List available scenarios |
| `/analyze-call` | POST | Analyze call transcript |
| `/transaction-risk` | POST | Analyze transaction |
| `/final-risk` | POST | Calculate final risk |
| `/full-analysis` | POST | **Complete pipeline** (recommended) |

### Frontend Components

#### Dashboard Features
- **Real-time Analysis**: Click "Run Analysis" for instant results
- **Demo Scenario Selector**: Quick access to all 6 scenarios
- **Risk Gauge**: Visual risk score representation
- **Alert Panel**: Detailed risk factors and recommendations
- **Confidence Display**: Shows analysis confidence level

---

## 🎬 Hackathon Demo Script

### Setup (Before Demo)
1. Start backend and frontend
2. Run `python demo_test.py` to verify all scenarios work
3. Open dashboard at http://localhost:3000
4. Have API docs ready at http://127.0.0.1:8000/docs

### Demo Flow (5-7 minutes)

#### Introduction (1 min)
"TrustShield AI is a real-time fraud detection system that analyzes phone calls to protect vulnerable individuals from scams."

#### Live Demo (4-5 min)

**Step 1: Show Critical Scam Detection**
1. Click "Bank Scam" scenario
2. Point out:
   - Transcript showing scam language
   - High fraud probability (85%+)
   - Critical risk level
   - Specific alerts (urgency, sensitive info requests)
   - Recommendation: Block transaction

**Step 2: Show Transaction Analysis**
1. Highlight transaction indicators:
   - Large amount ($50,000)
   - High frequency
   - Anomaly detection flag

**Step 3: Show Different Scam Types**
1. Click "IRS Scam" - show threat detection
2. Click "Tech Support Scam" - show technical manipulation

**Step 4: Show Legitimate Call**
1. Click "Legitimate Call"
2. Point out:
   - Low risk score
   - No suspicious patterns
   - Green "Allow" recommendation

#### Technical Deep Dive (1-2 min)
1. Show API documentation
2. Explain pipeline: Audio → Transcript → ML Analysis → Risk Score
3. Mention: Multi-factor analysis, confidence scoring, real-time processing

#### Q&A
Common questions:
- **Accuracy?** "85%+ on test data, uses ensemble of ML + rule-based detection"
- **Real audio?** "Yes, integrates Whisper for speech-to-text"
- **Scalability?** "FastAPI backend, can handle concurrent requests"
- **False positives?** "Confidence scoring helps, can tune thresholds"

---

## 🧪 Testing Guide

### Automated Testing
```bash
# Full test suite
python demo_test.py

# Expected output:
# - API health check: PASS
# - 6 scenario tests: ALL PASS
# - Detailed analysis for each scenario
```

### Manual Testing

#### Test 1: Basic Pipeline
1. Open dashboard
2. Click "Run Analysis"
3. Verify: Transcript loads, risk score displays, alerts appear

#### Test 2: All Scenarios
1. Click each scenario button
2. Verify: Different transcripts, varying risk scores, appropriate alerts

#### Test 3: API Direct
```bash
# Test full analysis endpoint
curl -X POST http://127.0.0.1:8000/full-analysis \
  -H "Content-Type: application/json" \
  -d '{"demo_scenario": "bank_scam"}'
```

---

## 🐛 Troubleshooting

### Backend Won't Start
```bash
# Check Python version (need 3.8+)
python --version

# Reinstall dependencies
cd trustshield-ai/backend
pip install -r requirements.txt

# Check port availability
netstat -an | findstr 8000
```

### Frontend Won't Start
```bash
# Reinstall node modules
cd trustshield-ai/frontend
rm -rf node_modules
npm install

# Check port availability
netstat -an | findstr 3000
```

### API Connection Error
1. Verify backend is running: http://127.0.0.1:8000
2. Check CORS settings in `backend/main.py`
3. Verify frontend API_URL in `frontend/src/App.js`

### Low Accuracy
1. Check `datasets/enhanced_scam_texts.csv` is loaded
2. Verify model training in `enhanced_scam_classifier.py`
3. Review risk thresholds in `risk_engine.py`

---

## 📈 Performance Metrics

### Expected Results

| Scenario | Risk Score | Risk Level | Response Time |
|----------|-----------|------------|---------------|
| Bank Scam | 85-95% | Critical | <500ms |
| IRS Scam | 85-95% | Critical | <500ms |
| Tech Support | 80-90% | Critical | <500ms |
| Grandparent | 75-85% | Critical | <500ms |
| Legitimate Call | 5-15% | Low | <500ms |
| Legitimate Business | 5-15% | Low | <500ms |

### System Requirements
- **Backend**: Python 3.8+, 2GB RAM
- **Frontend**: Node.js 14+, Modern browser
- **Network**: Local (no external dependencies for demo)

---

## 🔐 Security Features

1. **Multi-factor Analysis**: Voice + Transaction + Behavioral
2. **Confidence Scoring**: Weighted by analysis certainty
3. **Real-time Processing**: Immediate fraud detection
4. **Explainable AI**: Clear risk factors and recommendations
5. **Threshold Tuning**: Adjustable sensitivity

---

## 🚀 Future Enhancements

1. **Real Audio Processing**: Live microphone input
2. **Voice Biometrics**: Speaker verification
3. **Historical Analysis**: Pattern detection across calls
4. **Integration APIs**: Bank systems, CRM platforms
5. **Mobile App**: iOS/Android support
6. **Multi-language**: Support for non-English calls

---

## 📝 API Usage Examples

### Python
```python
import requests

# Full analysis
response = requests.post(
    "http://127.0.0.1:8000/full-analysis",
    json={"demo_scenario": "bank_scam"}
)
result = response.json()
print(f"Risk: {result['final_risk']['risk_level']}")
```

### JavaScript
```javascript
// Full analysis
const response = await fetch('http://127.0.0.1:8000/full-analysis', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ demo_scenario: 'bank_scam' })
});
const result = await response.json();
console.log(`Risk: ${result.final_risk.risk_level}`);
```

### cURL
```bash
curl -X POST http://127.0.0.1:8000/full-analysis \
  -H "Content-Type: application/json" \
  -d '{"demo_scenario": "bank_scam"}'
```

---

## 📞 Support

For issues or questions:
1. Check troubleshooting section above
2. Review API docs: http://127.0.0.1:8000/docs
3. Run test suite: `python demo_test.py`
4. Check logs in terminal windows

---

## ✅ Pre-Demo Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 3000
- [ ] All 6 scenarios tested with `demo_test.py`
- [ ] Dashboard loads without errors
- [ ] All scenario buttons work
- [ ] Risk scores display correctly
- [ ] Alerts show appropriate messages
- [ ] API documentation accessible
- [ ] Backup plan if internet fails (all local)

**You're ready to demo! 🎉**
