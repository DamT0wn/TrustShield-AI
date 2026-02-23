# How to Test TrustShield AI

## Current Status: ❌ Application Not Running

The application is currently not running. Follow the steps below to start and test it.

---

## Quick Start (3 Steps)

### Step 1: Install Dependencies
Double-click `install_dependencies.bat` or run:
```bash
pip install -r trustshield-ai/backend/requirements.txt
cd trustshield-ai/frontend && npm install
```

### Step 2: Start Backend
Open a terminal and run `start_backend.bat` or:
```bash
cd trustshield-ai/backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```
Wait for: `Application startup complete`

### Step 3: Start Frontend
Open another terminal and run `start_frontend.bat` or:
```bash
cd trustshield-ai/frontend
npm start
```
Browser will open at `http://localhost:3000`

---

## Testing All Features

### Method 1: Automated Test (Recommended)
```bash
pip install colorama requests
python test_application.py
```

This will test:
- ✓ Backend server running
- ✓ Analyze call endpoint
- ✓ Transaction risk endpoint
- ✓ Final risk endpoint
- ✓ Frontend server running

### Method 2: Manual Testing

#### Test Backend API
Open `http://127.0.0.1:8000/docs` in browser

Test each endpoint:
1. Click `/analyze-call` → Try it out → Execute
2. Click `/transaction-risk` → Try it out → Execute
3. Click `/final-risk` → Try it out → Execute

#### Test Frontend Dashboard
Open `http://localhost:3000`

1. Verify you see the dashboard with:
   - TrustShield AI header
   - Transcript box
   - Risk gauge
   - Alert panel

2. Click "Run Analysis" button
   - Should show "Analyzing..."
   - Should update all panels with new data
   - Should show risk score and level

3. Check alerts panel for warnings

---

## Feature Checklist

### ✅ Core Features to Test

- [ ] Backend starts without errors
- [ ] Frontend loads in browser
- [ ] "Run Analysis" button works
- [ ] Transcript updates after analysis
- [ ] Risk score displays correctly (0-100%)
- [ ] Risk level shows (Low/Medium/Critical)
- [ ] Alerts appear in alert panel
- [ ] API status shows "Live API: http://127.0.0.1:8000"

### ✅ AI Models to Test

- [ ] Scam Classifier detects fraud in text
- [ ] Anomaly Detector flags suspicious transactions
- [ ] Risk Engine calculates combined score
- [ ] Speech-to-Text transcribes audio (requires audio file)

---

## Expected Results

### When Backend is Running:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### When Frontend is Running:
```
Compiled successfully!
webpack compiled with 0 warnings
```

### When You Click "Run Analysis":
- Transcript updates with call content
- Risk score shows percentage (e.g., 85%)
- Risk level shows (Low/Medium/Critical)
- Alerts show relevant warnings

---

## Troubleshooting

### Backend won't start
```bash
# Install missing packages
pip install fastapi uvicorn pandas scikit-learn numpy openai-whisper torch
```

### Frontend won't start
```bash
# Install node modules
cd trustshield-ai/frontend
npm install
```

### "Module not found" error
```bash
# Run from project root
cd trustshield-ai
python -m backend.main
```

### CORS errors in browser console
Already fixed! CORS middleware is now enabled.

### Whisper model download
First run downloads ~140MB model. Wait for completion.

---

## Performance Expectations

- Backend startup: ~5-10 seconds
- Frontend startup: ~10-15 seconds
- API response time: <2 seconds
- Model inference: <1 second

---

## Next Steps After Testing

1. Add real audio files to `demo_assets/scam_call.wav`
2. Train models with more data in `datasets/scam_texts.csv`
3. Customize risk thresholds in `risk_engine.py`
4. Add more alert types in frontend
5. Deploy to production server

---

## Need Help?

Check `TESTING_GUIDE.md` for detailed testing instructions.
