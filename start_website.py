#!/usr/bin/env python3
"""
VUTAX 2.0 - Main Website Launcher
Starts the complete VUTAX trading platform
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
    print("              VUTAX 2.0 - TRADING PLATFORM LAUNCHER")
    print("="*60)
    print("\n🌐 This script will:")
    print("   1. Start the complete VUTAX trading platform")
    print("   2. Launch frontend, backend, and ML services")
    print("   3. Open the main platform in your browser")
    print("   4. Ready for trading and AI analysis")
    print("\n🚀 Platform URL: http://localhost:3000")
    print("📊 Features: Trading, AI recommendations, portfolio tracking")
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

def start_platform():
    """Start the complete VUTAX platform"""
    print("\n🐳 Starting VUTAX 2.0 trading platform...")
    
    try:
        # Start all services using docker-compose
        result = subprocess.run(['docker-compose', 'up', '-d'], 
                              capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            print("✅ Platform services started successfully")
            return True
        else:
            print("❌ Failed to start platform:")
            print(result.stderr)
            return False
            
    except subprocess.TimeoutExpired:
        print("⚠️  Platform is taking longer than expected to start")
        return True  # Continue anyway
    except FileNotFoundError:
        print("❌ docker-compose not found")
        print("   Please make sure Docker Compose is installed")
        return False

def wait_for_platform():
    """Wait for platform to be ready"""
    print("\n⏳ Waiting for platform to start up...")
    
    services = [
        ('Frontend', 'http://localhost:3000'),
        ('Backend API', 'http://localhost:4000/health'),
        ('ML Service', 'http://localhost:8001/health')
    ]
    
    max_attempts = 60
    for attempt in range(max_attempts):
        all_ready = True
        
        for service_name, url in services:
            try:
                response = requests.get(url, timeout=2)
                if response.status_code == 200:
                    if service_name not in [s[0] for s in services if hasattr(s, '_ready')]:
                        print(f"✅ {service_name} is ready")
                        setattr(services[services.index((service_name, url))], '_ready', True)
                else:
                    all_ready = False
            except requests.exceptions.RequestException:
                all_ready = False
        
        if all_ready:
            print("✅ All platform services are ready!")
            break
        
        if attempt < max_attempts - 1:
            time.sleep(2)
            if attempt % 10 == 0:
                print(f"   Still starting up... ({attempt + 1}/{max_attempts})")
    else:
        print("⚠️  Platform may still be starting up")

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
    print("                  PLATFORM READY!")
    print("="*60)
    print("\n🌐 Main Platform: http://localhost:3000")
    print("🔍 API Gateway: http://localhost:4000")
    print("🤖 ML Service: http://localhost:8001")
    print("📊 Training Tracker: http://localhost:5000")
    print("\n🎯 Platform Features:")
    print("   • Real-time stock data and analysis")
    print("   • AI-powered trading recommendations")
    print("   • Interactive portfolio management")
    print("   • Advanced charting with technical indicators")
    print("   • Discover page with 3000+ stocks")
    print("   • Watchlist with expandable analysis")
    print("   • Beautiful animations and smooth UI")
    print("\n🤖 AI Features:")
    print("   • Automatic model training every 6 hours")
    print("   • 70+ technical indicators analysis")
    print("   • Real-time market sentiment analysis")
    print("   • Personalized stock recommendations")
    print("\n" + "="*60)
    print("\n💡 Tips:")
    print("   - Explore the Discover page to find new stocks")
    print("   - Add stocks to your watchlist for tracking")
    print("   - Check AI recommendations for trading ideas")
    print("   - Use the training tracker to monitor AI improvements")
    print("\n" + "="*60 + "\n")

def main():
    """Main function"""
    print_header()
    
    # Ask user to continue
    try:
        input("Press Enter to start the platform, or Ctrl+C to cancel...")
    except KeyboardInterrupt:
        print("\n❌ Platform startup cancelled by user")
        sys.exit(0)
    
    print("🚀 Starting VUTAX 2.0 Trading Platform...\n")
    
    # Check Docker
    print("📋 Checking Docker status...")
    if not check_docker():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Start platform
    if not start_platform():
        input("\nPress Enter to exit...")
        sys.exit(1)
    
    # Wait for platform
    wait_for_platform()
    
    # Open platform
    open_platform()
    
    # Print platform info
    print_platform_info()
    
    print("🎉 VUTAX 2.0 Trading Platform is now running!")
    print("🌐 Visit http://localhost:3000 to start trading!")
    
    try:
        input("\nPress Enter to stop the platform...")
        print("\n🛑 Stopping platform services...")
        subprocess.run(['docker-compose', 'down'], capture_output=True)
        print("✅ Platform stopped successfully")
    except KeyboardInterrupt:
        print("\n🛑 Platform will continue running in background")
        print("   Use 'docker-compose down' to stop all services")

if __name__ == '__main__':
    main()
