@echo off
title VUTAX 2.0 - Trading Platform Launcher

echo.
echo ================================================================
echo              VUTAX 2.0 - TRADING PLATFORM LAUNCHER
echo ================================================================
echo.
echo 🌐 This script will:
echo    1. Start the complete VUTAX trading platform
echo    2. Launch frontend, backend, and ML services
echo    3. Open the main platform in your browser
echo    4. Ready for trading and AI analysis
echo.
echo 🚀 Platform URL: http://localhost:3000
echo 📊 Features: Trading, AI recommendations, portfolio tracking
echo.
echo ================================================================
echo.

pause

echo 🚀 Starting VUTAX 2.0 Trading Platform...
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

REM Start the complete platform
echo.
echo 🐳 Starting VUTAX 2.0 trading platform...
docker-compose up -d

REM Wait for services to be ready
echo.
echo ⏳ Waiting for platform to start up...
timeout /t 15 /nobreak >nul

REM Check if services are running
echo.
echo 📋 Checking service status...
docker-compose ps

echo.
echo 🌐 Opening VUTAX 2.0 trading platform...
start http://localhost:3000

echo.
echo ================================================================
echo                      PLATFORM READY!
echo ================================================================
echo.
echo 🌐 Main Platform: http://localhost:3000
echo 🔍 API Gateway: http://localhost:4000
echo 🤖 ML Service: http://localhost:8001
echo 📊 Training Tracker: http://localhost:5000
echo.
echo 🎯 Platform Features:
echo    • Real-time stock data and analysis
echo    • AI-powered trading recommendations
echo    • Interactive portfolio management
echo    • Advanced charting with technical indicators
echo    • Discover page with 3000+ stocks
echo    • Watchlist with expandable analysis
echo    • Beautiful animations and smooth UI
echo.
echo 🤖 AI Features:
echo    • Automatic model training every 6 hours
echo    • 70+ technical indicators analysis
echo    • Real-time market sentiment analysis
echo    • Personalized stock recommendations
echo.
echo ================================================================
echo.
echo 💡 Tips:
echo    - Explore the Discover page to find new stocks
echo    - Add stocks to your watchlist for tracking
echo    - Check AI recommendations for trading ideas
echo    - Use the training tracker to monitor AI improvements
echo.
echo ================================================================
echo.

echo 🎉 VUTAX 2.0 Trading Platform is now running!
echo 🌐 Visit http://localhost:3000 to start trading!
echo.
echo Press any key to stop the platform...
pause >nul

echo.
echo 🛑 Stopping platform services...
docker-compose down
echo ✅ Platform stopped successfully
pause
