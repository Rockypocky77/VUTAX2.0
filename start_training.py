#!/usr/bin/env python3
"""
VUTAX 2.0 - Flask AI Training Launcher
Starts ML training using Flask and opens progress tracking dashboard
"""

import os
import sys
import time
import subprocess
import requests
import webbrowser
import threading
from datetime import datetime

# Add backend paths
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'ml-service'))

def print_header():
    """Print the startup header"""
    print("\n" + "="*60)
    print("                VUTAX 2.0 - FLASK AI TRAINING LAUNCHER")
    print("="*60)
    print("\n🤖 This script will:")
    print("   1. Start the ML service using Flask")
    print("   2. Launch the training progress tracker")
    print("   3. Begin training all AI models")
    print("   4. Open the progress dashboard in your browser")
    print("\n⏱️  Expected training time: 15-30 minutes")
    print("📊 Progress tracking: http://localhost:5000")
    print("\n" + "="*60 + "\n")

def check_python_deps():
    """Check if required Python packages are available"""
    print("📋 Checking Python dependencies...")
    
    required_packages = ['flask', 'requests', 'pandas', 'numpy', 'scikit-learn']
    missing_packages = []
    
    for package in required_packages:
        try:
            if package == 'scikit-learn':
                __import__('sklearn')
            else:
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
            print(f"   Please run: pip install {' '.join(missing_packages)}")
            return False
    else:
        print("✅ All required packages available")
    
    return True

def setup_ml_environment():
    """Set up ML training environment"""
    print("🔧 Setting up ML training environment...")
    
    # Ensure data directories exist
    ml_dirs = [
        'backend/ml-service/data',
        'backend/ml-service/models/saved',
        'backend/ml-service/cache',
        'backend/ml-service/logs',
        'data/market_data',
        'data/models',
        'data/cache',
        'data/logs'
    ]
    
    for dir_path in ml_dirs:
        full_path = os.path.join(os.path.dirname(__file__), dir_path)
        os.makedirs(full_path, exist_ok=True)
    
    print("✅ ML environment ready")
    return True

def start_training_tracker():
    """Start the training progress tracker using Flask"""
    print("\n📊 Starting training progress tracker...")
    
    try:
        # Start the training tracker Flask app
        tracker_process = subprocess.Popen([
            sys.executable, 
            os.path.join('backend', 'training-tracker', 'app.py')
        ], cwd=os.path.dirname(__file__))
        
        print("✅ Training tracker started at http://localhost:5000")
        return tracker_process
        
    except Exception as e:
        print(f"❌ Failed to start training tracker: {e}")
        return None

def start_ml_service():
    """Start the ML service for training"""
    print("\n🤖 Starting ML service...")
    
    try:
        # Try to start the ML service directly
        ml_service_path = os.path.join('backend', 'ml-service', 'main.py')
        if os.path.exists(ml_service_path):
            ml_process = subprocess.Popen([
                sys.executable, ml_service_path
            ], cwd=os.path.dirname(__file__))
            print("✅ ML service started")
            return ml_process
        else:
            print("⚠️  ML service not found, will use training tracker only")
            return None
            
    except Exception as e:
        print(f"⚠️  Could not start ML service: {e}")
        return None

def wait_for_services():
    """Wait for services to be ready"""
    print("\n⏳ Waiting for services to start up...")
    
    max_attempts = 15
    for attempt in range(max_attempts):
        try:
            # Check training tracker
            response = requests.get('http://localhost:5000/api/status', timeout=2)
            if response.status_code == 200:
                print("✅ Training tracker is ready")
                break
        except requests.exceptions.RequestException:
            pass
        
        if attempt < max_attempts - 1:
            time.sleep(2)
            if attempt % 5 == 0:
                print(f"   Still starting up... ({attempt + 1}/{max_attempts})")
    else:
        print("⚠️  Services may still be starting up")

def start_training():
    """Start the AI model training"""
    print("\n🤖 Starting AI model training...")
    print("   - Analytical Model: Stock prediction and recommendations")
    print("   - Feature Engineering: 70+ technical indicators")
    print("   - Real-time Analysis: Market sentiment and trends")
    
    # Wait a moment for services to be ready
    time.sleep(3)
    
    try:
        # Try to start training via training tracker
        response = requests.post('http://localhost:5000/api/start-training',
                               json={'model_type': 'analytical'},
                               timeout=10)
        
        if response.status_code == 200:
            print("✅ Training started successfully")
            return True
        else:
            print("⚠️  Training will start automatically - check dashboard")
            return True
            
    except requests.exceptions.RequestException as e:
        print("⚠️  Could not start training automatically")
        print("   You can start training manually from the dashboard")
        return True

def open_dashboard():
    """Open the training dashboard in browser"""
    print("\n🌐 Opening training progress dashboard...")
    
    try:
        webbrowser.open('http://localhost:5000')
        print("✅ Dashboard opened in browser")
    except Exception as e:
        print("⚠️  Could not open browser automatically")
        print("   Please visit: http://localhost:5000")

def print_status():
    """Print the final status and instructions"""
    print("\n" + "="*60)
    print("                  FLASK TRAINING STARTED!")
    print("="*60)
    print("\n📊 Training Dashboard: http://localhost:5000")
    print("🌐 Main Platform: http://localhost:3000")
    print("🤖 ML Training: Flask-based service")
    print("\n📈 What's happening now:")
    print("   • AI models are collecting fresh market data")
    print("   • 70+ technical indicators being calculated")
    print("   • Machine learning algorithms training on real data")
    print("   • Progress tracked in real-time on the dashboard")
    print("\n⏱️  Estimated completion: 15-30 minutes")
    print("🔄 Models will improve automatically every 6 hours")
    print("\n" + "="*60)
    print("\n💡 Tips:")
    print("   - Visit the dashboard to watch detailed progress")
    print("   - Training continues in background Flask processes")
    print("   - Models save automatically when training completes")
    print("   - All data stored locally in data/ folders")
    print("\n" + "="*60 + "\n")

def monitor_training():
    """Monitor training progress"""
    print("🔄 Monitoring training progress...")
    print("   (Press Ctrl+C to stop monitoring, training will continue)\n")
    
    try:
        while True:
            try:
                response = requests.get('http://localhost:5000/api/status', timeout=5)
                if response.status_code == 200:
                    status = response.json()
                    
                    if status.get('is_training', False):
                        progress = status.get('progress', 0)
                        stage = status.get('current_stage', 'training')
                        eta = status.get('eta_minutes', 0)
                        
                        print(f"🤖 Training in progress: {stage} ({progress:.1f}%)")
                        if eta > 0:
                            print(f"⏱️  Estimated time remaining: {eta} minutes")
                        print(f"   Last updated: {datetime.now().strftime('%H:%M:%S')}")
                        print()
                    else:
                        print("✅ Training completed or idle")
                        print("📊 Check the dashboard for results: http://localhost:5000")
                        break
                        
            except requests.exceptions.RequestException:
                print("📡 Checking services...")
            
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print("\n🔄 Monitoring stopped (training continues in background)")
        print("📊 Visit http://localhost:5000 to check progress")

def main():
    """Main function"""
    print_header()
    
    # Ask user to continue
    try:
        input("Press Enter to start Flask training, or Ctrl+C to cancel...")
    except KeyboardInterrupt:
        print("\n❌ Training cancelled by user")
        sys.exit(0)
    
    print("🚀 Starting VUTAX 2.0 Flask AI Training System...\n")
    
    # Check Python dependencies
    if not check_python_deps():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Setup ML environment
    if not setup_ml_environment():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Start training tracker
    tracker_process = start_training_tracker()
    if not tracker_process:
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Start ML service (optional)
    ml_process = start_ml_service()
    
    # Wait for services
    wait_for_services()
    
    # Start training
    start_training()
    
    # Open dashboard with delay
    def delayed_open():
        time.sleep(3)
        open_dashboard()
    
    threading.Thread(target=delayed_open, daemon=True).start()
    
    # Print status
    print_status()
    
    print("🎉 VUTAX 2.0 Flask AI Training is now running!")
    print("📊 Visit http://localhost:5000 to watch training progress!")
    print("🌐 Visit http://localhost:3000 for the main platform!")
    print("\n⚠️  Press Ctrl+C to stop monitoring (training continues)")
    
    try:
        # Monitor training
        monitor_training()
    except KeyboardInterrupt:
        print("\n🔄 Monitoring stopped")
        print("🤖 Training processes continue in background")
        print("📊 Visit http://localhost:5000 to check progress")
        
        # Ask if user wants to stop services
        try:
            stop = input("\nStop training services? (y/N): ").lower().strip()
            if stop == 'y':
                print("🛑 Stopping training services...")
                if tracker_process:
                    tracker_process.terminate()
                if ml_process:
                    ml_process.terminate()
                print("✅ Training services stopped")
            else:
                print("🔄 Training services continue running in background")
        except KeyboardInterrupt:
            print("\n🔄 Training services continue running in background")

if __name__ == '__main__':
    main()
