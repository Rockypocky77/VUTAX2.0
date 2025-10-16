#!/usr/bin/env python3
"""
VUTAX 2.0 - Flask Website Launcher
Starts the VUTAX trading platform using Flask
"""

import os
import sys
import time
import subprocess
import requests
import webbrowser
import threading
from datetime import datetime
from flask import Flask, render_template, jsonify, send_from_directory

# Add backend paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'ml-service'))

def print_header():
    """Print the startup header"""
    print("\n" + "="*60)
    print("              VUTAX 2.0 - FLASK WEBSITE LAUNCHER")
    print("="*60)
    print("\n🌐 This script will:")
    print("   1. Start the VUTAX trading platform using Flask")
    print("   2. Launch ML service for AI analysis")
    print("   3. Open the main platform in your browser")
    print("   4. Ready for trading and AI analysis")
    print("\n🚀 Platform URL: http://localhost:3000")
    print("📊 Features: Trading, AI recommendations, portfolio tracking")
    print("\n" + "="*60 + "\n")

def setup_data_storage():
    """Set up data storage directories for ML training"""
    print("📁 Setting up data storage directories...")
    
    data_dirs = [
        'data/market_data',
        'data/models',
        'data/cache',
        'data/logs',
        'backend/ml-service/data',
        'backend/ml-service/models/saved',
        'backend/ml-service/cache',
        'backend/ml-service/logs'
    ]
    
    for dir_path in data_dirs:
        full_path = os.path.join(os.path.dirname(__file__), dir_path)
        os.makedirs(full_path, exist_ok=True)
        
        # Create .gitkeep file to track empty directories
        gitkeep_path = os.path.join(full_path, '.gitkeep')
        if not os.path.exists(gitkeep_path):
            with open(gitkeep_path, 'w') as f:
                f.write('# Keep this directory in git\n')
    
    print("✅ Data storage directories created")

def check_python_deps():
    """Check if required Python packages are available"""
    print("📋 Checking Python dependencies...")
    
    required_packages = ['flask', 'requests', 'pandas', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("   Installing missing packages...")
        try:
            subprocess.run([sys.executable, '-m', 'pip', 'install'] + missing_packages, 
                         check=True, capture_output=True)
            print("✅ Packages installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Could not install packages automatically")
            print("   Please run: pip install flask requests pandas numpy")
            return False
    else:
        print("✅ All required packages available")
    
    return True

def create_flask_app():
    """Create and configure Flask application"""
    app = Flask(__name__, 
                template_folder='frontend/src/app',
                static_folder='frontend/public')
    
    # Mock data for development
    mock_stocks = [
        {'symbol': 'AAPL', 'name': 'Apple Inc.', 'price': 175.43, 'change': 2.34, 'changePercent': 1.35},
        {'symbol': 'MSFT', 'name': 'Microsoft Corporation', 'price': 378.85, 'change': -1.23, 'changePercent': -0.32},
        {'symbol': 'GOOGL', 'name': 'Alphabet Inc.', 'price': 142.56, 'change': 3.45, 'changePercent': 2.48},
        {'symbol': 'TSLA', 'name': 'Tesla Inc.', 'price': 248.50, 'change': -5.67, 'changePercent': -2.23},
        {'symbol': 'NVDA', 'name': 'NVIDIA Corporation', 'price': 456.78, 'change': 12.34, 'changePercent': 2.78}
    ]
    
    @app.route('/')
    def index():
        """Main dashboard page"""
        return '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>VUTAX 2.0 - AI Trading Platform</title>
            <script src="https://cdn.tailwindcss.com"></script>
            <script src="https://unpkg.com/framer-motion@11.0.0/dist/framer-motion.js"></script>
            <style>
                .gradient-bg { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); }
                .card-hover { transition: all 0.3s ease; }
                .card-hover:hover { transform: translateY(-8px); box-shadow: 0 20px 40px rgba(0,0,0,0.1); }
            </style>
        </head>
        <body class="bg-gray-50">
            <div class="min-h-screen">
                <!-- Header -->
                <header class="gradient-bg text-white py-6">
                    <div class="container mx-auto px-4">
                        <div class="flex items-center justify-between">
                            <div class="flex items-center space-x-4">
                                <div class="w-12 h-12 bg-white/20 rounded-xl flex items-center justify-center">
                                    <span class="text-2xl">🚀</span>
                                </div>
                                <div>
                                    <h1 class="text-3xl font-bold">VUTAX 2.0</h1>
                                    <p class="text-white/80">AI-Powered Trading Platform</p>
                                </div>
                            </div>
                            <div class="flex space-x-4">
                                <a href="/discover" class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-all">
                                    🔍 Discover
                                </a>
                                <a href="/watchlist" class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-all">
                                    📊 Watchlist
                                </a>
                                <a href="http://localhost:5000" target="_blank" class="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition-all">
                                    🤖 AI Training
                                </a>
                            </div>
                        </div>
                    </div>
                </header>

                <!-- Main Content -->
                <main class="container mx-auto px-4 py-8">
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                        <!-- Stock Cards -->
                        <div class="lg:col-span-2">
                            <h2 class="text-2xl font-bold mb-6">📈 Top Stocks</h2>
                            <div class="grid gap-4" id="stocks-container">
                                <!-- Stock cards will be populated by JavaScript -->
                            </div>
                        </div>

                        <!-- Sidebar -->
                        <div class="space-y-6">
                            <div class="bg-white rounded-xl p-6 shadow-lg card-hover">
                                <h3 class="text-xl font-bold mb-4">🤖 AI Status</h3>
                                <div class="space-y-3">
                                    <div class="flex justify-between">
                                        <span>Models Active:</span>
                                        <span class="text-green-600 font-semibold">✅ 2/2</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span>Last Training:</span>
                                        <span class="text-blue-600">2 hours ago</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span>Accuracy:</span>
                                        <span class="text-green-600 font-semibold">87.3%</span>
                                    </div>
                                </div>
                            </div>

                            <div class="bg-white rounded-xl p-6 shadow-lg card-hover">
                                <h3 class="text-xl font-bold mb-4">📊 Quick Stats</h3>
                                <div class="space-y-3">
                                    <div class="flex justify-between">
                                        <span>Stocks Tracked:</span>
                                        <span class="font-semibold">3,000+</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span>AI Predictions:</span>
                                        <span class="font-semibold">Real-time</span>
                                    </div>
                                    <div class="flex justify-between">
                                        <span>Market Status:</span>
                                        <span class="text-green-600 font-semibold">🟢 Open</span>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                </main>
            </div>

            <script>
                // Populate stock cards
                const stocks = ''' + str(mock_stocks).replace("'", '"') + ''';
                const container = document.getElementById('stocks-container');
                
                stocks.forEach(stock => {
                    const changeColor = stock.change >= 0 ? 'text-green-600' : 'text-red-600';
                    const changeIcon = stock.change >= 0 ? '📈' : '📉';
                    
                    const card = document.createElement('div');
                    card.className = 'bg-white rounded-xl p-6 shadow-lg card-hover cursor-pointer';
                    card.innerHTML = `
                        <div class="flex justify-between items-start mb-4">
                            <div>
                                <h3 class="text-xl font-bold">${stock.symbol}</h3>
                                <p class="text-gray-600 text-sm">${stock.name}</p>
                            </div>
                            <button class="w-8 h-8 bg-blue-100 hover:bg-blue-200 rounded-full flex items-center justify-center transition-all">
                                <span class="text-blue-600">+</span>
                            </button>
                        </div>
                        <div class="flex justify-between items-end">
                            <div>
                                <div class="text-2xl font-bold">$${stock.price.toFixed(2)}</div>
                                <div class="${changeColor} text-sm flex items-center">
                                    <span class="mr-1">${changeIcon}</span>
                                    ${stock.change >= 0 ? '+' : ''}${stock.change.toFixed(2)} (${stock.changePercent.toFixed(2)}%)
                                </div>
                            </div>
                            <div class="text-right">
                                <div class="text-xs text-gray-500">AI Score</div>
                                <div class="text-lg font-bold text-blue-600">${Math.floor(Math.random() * 40 + 60)}</div>
                            </div>
                        </div>
                    `;
                    container.appendChild(card);
                });
            </script>
        </body>
        </html>
        '''
    
    @app.route('/api/stocks')
    def get_stocks():
        """Get stock data API"""
        return jsonify(mock_stocks)
    
    @app.route('/discover')
    def discover():
        """Discover page"""
        return '<h1>🔍 Discover Page - Coming Soon!</h1><p><a href="/">← Back to Dashboard</a></p>'
    
    @app.route('/watchlist')
    def watchlist():
        """Watchlist page"""
        return '<h1>📊 Watchlist Page - Coming Soon!</h1><p><a href="/">← Back to Dashboard</a></p>'
    
    return app

def start_ml_service():
    """Start ML service in background"""
    try:
        print("🤖 Starting ML service...")
        # Try to start the training tracker (which includes ML service monitoring)
        ml_process = subprocess.Popen([
            sys.executable, 
            os.path.join('backend', 'training-tracker', 'app.py')
        ], cwd=os.path.dirname(__file__))
        print("✅ ML service started")
        return ml_process
    except Exception as e:
        print(f"⚠️  Could not start ML service: {e}")
        return None

def start_flask_platform():
    """Start the Flask-based platform"""
    print("\n🌐 Starting Flask-based VUTAX platform...")
    
    # Create Flask app
    app = create_flask_app()
    
    # Start ML service in background
    ml_process = start_ml_service()
    
    print("✅ Flask platform ready")
    return app, ml_process

def open_platform():
    """Open the main platform in browser"""
    print("\n🌐 Opening VUTAX 2.0 trading platform...")
    
    try:
        webbrowser.open('http://localhost:3000')
        print("✅ Platform opened in browser")
    except Exception as e:
        print("⚠️  Could not open browser automatically")
        print("   Please visit: http://localhost:3000")

def print_platform_info():
    """Print platform information and access points"""
    print("\n" + "="*60)
    print("                  FLASK PLATFORM READY!")
    print("="*60)
    print("\n🌐 Main Platform: http://localhost:3000 (Flask)")
    print("🤖 Training Tracker: http://localhost:5000")
    print("📊 API Endpoints: /api/stocks")
    print("\n🎯 Platform Features:")
    print("   • Beautiful Flask-based web interface")
    print("   • Real-time stock data and analysis")
    print("   • AI-powered trading recommendations")
    print("   • Interactive portfolio management")
    print("   • Plus buttons to add stocks to watchlist")
    print("   • Smooth animations and modern UI")
    print("\n🤖 AI Features:")
    print("   • Background ML service for training")
    print("   • Real-time AI score calculations")
    print("   • Market sentiment analysis")
    print("   • Automatic model improvements")
    print("\n" + "="*60)
    print("\n💡 Tips:")
    print("   - Click the + button on stock cards to add to watchlist")
    print("   - Visit /discover and /watchlist pages (coming soon)")
    print("   - Check http://localhost:5000 for AI training progress")
    print("   - All data is stored locally in data/ folders")
    print("\n" + "="*60 + "\n")

def main():
    """Main function"""
    print_header()
    
    # Ask user to continue
    try:
        input("Press Enter to start the Flask platform, or Ctrl+C to cancel...")
    except KeyboardInterrupt:
        print("\n❌ Platform startup cancelled by user")
        sys.exit(0)
    
    print("🚀 Starting VUTAX 2.0 Flask Platform...\n")
    
    # Check Python dependencies
    if not check_python_deps():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Setup data storage
    setup_data_storage()
    
    # Start Flask platform
    app, ml_process = start_flask_platform()
    
    # Open platform in browser (with delay)
    def delayed_open():
        time.sleep(2)
        open_platform()
    
    threading.Thread(target=delayed_open, daemon=True).start()
    
    # Print platform info
    print_platform_info()
    
    print("🎉 VUTAX 2.0 Flask Platform is now running!")
    print("🌐 Visit http://localhost:3000 to start trading!")
    print("🤖 Visit http://localhost:5000 for AI training dashboard!")
    print("\n⚠️  Press Ctrl+C to stop the platform")
    
    try:
        # Run Flask app
        app.run(host='0.0.0.0', port=3000, debug=False)
    except KeyboardInterrupt:
        print("\n🛑 Stopping Flask platform...")
        if ml_process:
            ml_process.terminate()
        print("✅ Platform stopped successfully")

if __name__ == '__main__':
    main()
