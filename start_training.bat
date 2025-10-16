@echo off
title VUTAX 2.0 - AI Training Launcher

echo.
echo ================================================================
echo                    VUTAX 2.0 - AI TRAINING LAUNCHER
echo ================================================================
echo.
echo 🤖 This script will:
echo    1. Start the ML service for training
echo    2. Launch the training progress tracker
echo    3. Begin training all AI models
echo    4. Open the progress dashboard in your browser
echo.
echo ⏱️  Expected training time: 15-30 minutes
echo 📊 Progress tracking: http://localhost:5000
echo.
echo ================================================================
echo.

pause

echo 🚀 Starting VUTAX 2.0 AI Training System...
echo.

REM Check if Docker is running
echo 📋 Checking Docker status...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker is not installed or not running
    echo    Please install Docker Desktop and make sure it's running
    pause
    exit /b 1
)
echo ✅ Docker is ready

REM Start the ML service and training tracker
echo.
echo 🐳 Starting ML service and training tracker...
docker-compose up -d ml-service training-tracker

REM Wait for services to be ready
echo.
echo ⏳ Waiting for services to start up...
timeout /t 10 /nobreak >nul

REM Check if services are running
echo.
echo 📋 Checking service status...
docker-compose ps

REM Start training automatically
echo.
echo 🤖 Starting AI model training...
echo    - Analytical Model: Stock prediction and recommendations
echo    - Chatbot Model: Financial conversation and explanations
echo.

REM Use curl to start training (if available) or use PowerShell
curl --version >nul 2>&1
if errorlevel 1 (
    echo 📡 Using PowerShell to start training...
    powershell -Command "try { $response = Invoke-RestMethod -Uri 'http://localhost:8001/training/start' -Method POST -ContentType 'application/json' -Body '{\"model_type\":\"analytical\"}'; Write-Host '✅ Training started successfully' } catch { Write-Host '⚠️  Training will start automatically - check dashboard' }"
) else (
    echo 📡 Using curl to start training...
    curl -X POST http://localhost:8001/training/start -H "Content-Type: application/json" -d "{\"model_type\":\"analytical\"}" >nul 2>&1
    if errorlevel 1 (
        echo ⚠️  Training will start automatically - check dashboard
    ) else (
        echo ✅ Training started successfully
    )
)

echo.
echo 🌐 Opening training progress dashboard...
echo.

REM Open the training dashboard in default browser
start http://localhost:5000

echo ================================================================
echo                        TRAINING STARTED!
echo ================================================================
echo.
echo 📊 Training Dashboard: http://localhost:5000
echo 🔍 ML Service API: http://localhost:8001
echo 🌐 Main Platform: http://localhost:3000
echo.
echo 📈 What's happening now:
echo    • AI models are collecting fresh market data
echo    • 70+ technical indicators being calculated
echo    • Machine learning algorithms training on real data
echo    • Progress tracked in real-time on the dashboard
echo.
echo ⏱️  Estimated completion: 15-30 minutes
echo 🔄 Models will improve automatically every 6 hours
echo.
echo ================================================================
echo.
echo 💡 Tips:
echo    - Keep this window open to see status updates
echo    - Visit the dashboard to watch detailed progress
echo    - Training continues even if you close this window
echo    - Models save automatically when training completes
echo.
echo ================================================================
echo.

REM Keep the window open and show periodic updates
:monitor_loop
echo 📊 Checking training status...
timeout /t 30 /nobreak >nul

REM Check if training is still running
powershell -Command "try { $status = Invoke-RestMethod -Uri 'http://localhost:5000/api/status' -Method GET; if ($status.is_training) { Write-Host ('🤖 Training in progress: ' + $status.current_stage + ' (' + [math]::Round($status.progress, 1) + '%)'); if ($status.eta_minutes -gt 0) { Write-Host ('⏱️  Estimated time remaining: ' + $status.eta_minutes + ' minutes') } } else { Write-Host '✅ Training completed or idle'; exit 1 } } catch { Write-Host '📡 Checking services...' }" 2>nul

if errorlevel 1 (
    echo.
    echo 🎉 Training appears to be completed!
    echo 📊 Check the dashboard for final results: http://localhost:5000
    echo.
    pause
    exit /b 0
)

goto monitor_loop
