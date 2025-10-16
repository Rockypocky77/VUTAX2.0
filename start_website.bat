@echo off
title VUTAX 2.0 - Flask Website Launcher

echo.
echo ================================================================
echo              VUTAX 2.0 - FLASK WEBSITE LAUNCHER
echo ================================================================
echo.
echo 🌐 This script will:
echo    1. Start the VUTAX trading platform using Flask
echo    2. Launch ML service for AI analysis
echo    3. Open the main platform in your browser
echo    4. Ready for trading and AI analysis
echo.
echo 🚀 Platform URL: http://localhost:3000 (Flask)
echo 📊 Features: Trading, AI recommendations, portfolio tracking
echo.
echo ================================================================
echo.

pause

echo 🚀 Starting VUTAX 2.0 Flask Platform...
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

REM Start the Flask platform
echo.
echo 🌐 Starting Flask-based VUTAX platform...
echo 📁 Setting up data storage directories...
echo 🤖 Installing required packages if needed...
echo.

REM Run the Python Flask launcher
python start_website.py

echo.
echo ✅ Flask platform stopped
pause
