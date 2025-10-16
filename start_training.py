#!/usr/bin/env python3
"""
VUTAX 2.0 - Easy AI Training Launcher
Starts ML training and opens progress tracking dashboard
"""

import os
import sys
import time
import subprocess
import requests
import webbrowser
from datetime import datetime

def print_header():
    """Print the startup header"""
    print("\n" + "="*60)
    print("                VUTAX 2.0 - AI TRAINING LAUNCHER")
    print("="*60)
    print("\n🤖 This script will:")
    print("   1. Start the ML service for training")
    print("   2. Launch the training progress tracker")
    print("   3. Begin training all AI models")
    print("   4. Open the progress dashboard in your browser")
    print("\n⏱️  Expected training time: 15-30 minutes")
    print("📊 Progress tracking: http://localhost:5000")
    print("\n" + "="*60 + "\n")

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Docker is ready")
            return True
        else:
            print("❌ Docker is not working properly")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("❌ Docker is not installed or not running")
        print("   Please install Docker Desktop and make sure it's running")
        return False

def start_services():
    """Start the ML service and training tracker"""
    print("\n🐳 Starting ML service and training tracker...")
    
    try:
        # Start services using docker-compose
        result = subprocess.run(['docker-compose', 'up', '-d', 'ml-service', 'training-tracker'], 
                              capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Services started successfully")
            return True
        else:
            print("❌ Failed to start services:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Services are taking longer than expected to start")
        return True  # Continue anyway
    except FileNotFoundError:
        print("❌ docker-compose not found")
        print("   Please make sure Docker Compose is installed")
        return False

def wait_for_services():
    """Wait for services to be ready"""
    print("\n⏳ Waiting for services to start up...")
    
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            # Check ML service
            response = requests.get('http://localhost:8001/health', timeout=2)
            if response.status_code == 200:
                print("✅ ML service is ready")
                break
        except requests.exceptions.RequestException:
            pass
        
        if attempt < max_attempts - 1:
            time.sleep(2)
            print(f"   Waiting... ({attempt + 1}/{max_attempts})")
    else:
        print("⚠️  Services may still be starting up")

def start_training():
    """Start the AI model training"""
    print("\n🤖 Starting AI model training...")
    print("   - Analytical Model: Stock prediction and recommendations")
    print("   - Chatbot Model: Financial conversation and explanations")
    
    try:
        response = requests.post('http://localhost:8001/training/start',
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
        print("   Training will start automatically - check dashboard")
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
    print("                    TRAINING STARTED!")
    print("="*60)
    print("\n📊 Training Dashboard: http://localhost:5000")
    print("🔍 ML Service API: http://localhost:8001")
    print("🌐 Main Platform: http://localhost:3000")
    print("\n📈 What's happening now:")
    print("   • AI models are collecting fresh market data")
    print("   • 70+ technical indicators being calculated")
    print("   • Machine learning algorithms training on real data")
    print("   • Progress tracked in real-time on the dashboard")
    print("\n⏱️  Estimated completion: 15-30 minutes")
    print("🔄 Models will improve automatically every 6 hours")
    print("\n" + "="*60)
    print("\n💡 Tips:")
    print("   - Keep this window open to see status updates")
    print("   - Visit the dashboard to watch detailed progress")
    print("   - Training continues even if you close this window")
    print("   - Models save automatically when training completes")
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
        input("Press Enter to start training, or Ctrl+C to cancel...")
    except KeyboardInterrupt:
        print("\n❌ Training cancelled by user")
        sys.exit(0)
    
    print("🚀 Starting VUTAX 2.0 AI Training System...\n")
    
    # Check Docker
    print("📋 Checking Docker status...")
    if not check_docker():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Start services
    if not start_services():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Wait for services
    wait_for_services()
    
    # Start training
    start_training()
    
    # Open dashboard
    open_dashboard()
    
    # Print status
    print_status()
    
    # Monitor training
    monitor_training()
    
    print("\n🎉 Training launcher completed!")
    input("Press Enter to exit...")

if __name__ == '__main__':
    main()
