@echo off
echo Starting TrustShield AI Backend...
cd trustshield-ai\backend
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
