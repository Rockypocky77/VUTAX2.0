@echo off
title VUTAX 2.0 - Flask AI Training Launcher

echo.
echo ================================================================
echo                VUTAX 2.0 - FLASK AI TRAINING LAUNCHER
echo ================================================================
echo.
echo 🤖 This script will:
echo    1. Start the ML service using Flask
echo    2. Launch the training progress tracker
echo    3. Begin training all AI models
echo    4. Open the progress dashboard in your browser
echo.
echo ⏱️  Expected training time: 15-30 minutes
echo 📊 Progress tracking: http://localhost:5000 (Flask)
echo.
echo ================================================================
echo.

pause

echo 🚀 Starting VUTAX 2.0 Flask AI Training System...
echo.

REM Check if Python is available
echo 📋 Checking Python status...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo    Please install Python 3.8+ and make sure it's in your PATH
    pause
    exit /b 1
)
echo ✅ Python is ready

REM Start the Flask-based training system
echo.
echo 🌐 Starting Flask-based AI training system...
echo 📁 Setting up ML environment...
echo 🤖 Installing required packages if needed...
echo 📊 Starting training tracker and ML service...
echo.

REM Run the Python Flask training launcher
python start_training.py

echo.
echo ✅ Flask training system stopped
pause
