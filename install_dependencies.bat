@echo off
echo Installing TrustShield AI Dependencies...
echo.
echo [1/2] Installing Backend Dependencies...
cd trustshield-ai\backend
pip install -r requirements.txt
cd ..\..
echo.
echo [2/2] Installing Frontend Dependencies...
cd trustshield-ai\frontend
npm install
cd ..\..
echo.
echo Installation Complete!
echo.
echo To start the application:
echo 1. Run start_backend.bat in one terminal
echo 2. Run start_frontend.bat in another terminal
pause
