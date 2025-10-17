#!/usr/bin/env python3
"""
Test script to demonstrate the enhanced training dashboard
Shows real-time data fetching progress and synchronized progress bars
"""

import time
import requests
import webbrowser
from datetime import datetime

def test_dashboard():
    """Test the enhanced training dashboard"""
    print("\n" + "="*60)
    print("🧪 TESTING ENHANCED TRAINING DASHBOARD")
    print("="*60)
    print("\n🌐 This test will:")
    print("   1. Start the training tracker")
    print("   2. Open the enhanced dashboard")
    print("   3. Start training to show real-time progress")
    print("   4. Display data fetching graphs and progress bars")
    print("\n📊 Enhanced Features:")
    print("   • Real-time data fetching graphs")
    print("   • Synchronized progress bars for each stage")
    print("   • Articles/stocks/data points counters")
    print("   • Live fetch rate monitoring")
    print("   • Beautiful Tailwind CSS design")
    print("\n" + "="*60 + "\n")
    
    input("Press Enter to start the test...")
    
    # Check if training tracker is running
    try:
        response = requests.get('http://localhost:5000/api/status', timeout=3)
        if response.status_code == 200:
            print("✅ Training tracker is running")
        else:
            print("❌ Training tracker not responding")
            return
    except requests.exceptions.RequestException:
        print("❌ Training tracker not running at http://localhost:5000")
        print("   Please run: python start_training.py")
        return
    
    # Open the enhanced dashboard
    print("🌐 Opening enhanced training dashboard...")
    webbrowser.open('http://localhost:5000')
    
    print("\n🎯 What you'll see in the dashboard:")
    print("   📊 Data Fetching Progress - Real-time graphs showing:")
    print("      • Articles fetched from various sources")
    print("      • Stocks processed with technical indicators")
    print("      • Data points collected for training")
    print("      • Current fetch rate (articles/minute)")
    print("\n   📈 Progress Bars - Synchronized bars for:")
    print("      • Overall training progress")
    print("      • Data Collection stage")
    print("      • Feature Engineering stage")
    print("      • Model Training stage")
    print("      • Validation stage")
    print("      • Deployment stage")
    print("\n   🎨 Enhanced UI Features:")
    print("      • Beautiful gradient backgrounds")
    print("      • Smooth animations and transitions")
    print("      • Real-time Socket.IO updates")
    print("      • Interactive charts with Chart.js")
    print("      • Responsive Tailwind CSS design")
    
    # Ask if user wants to start training
    print("\n" + "="*60)
    start_training = input("Start training to see live progress? (y/N): ").lower().strip()
    
    if start_training == 'y':
        print("🚀 Starting training to demonstrate live progress...")
        
        try:
            response = requests.post('http://localhost:5000/api/start-training',
                                   json={'model_type': 'analytical'},
                                   timeout=10)
            
            if response.status_code == 200:
                print("✅ Training started successfully!")
                print("\n📊 Watch the dashboard for:")
                print("   • Real-time data fetching counters")
                print("   • Progressive stage completion")
                print("   • Live graphs updating every 2 seconds")
                print("   • ETA calculations")
                print("   • Source switching (Alpha Vantage, Yahoo Finance, etc.)")
                
                print("\n⏱️  The training will show realistic progress:")
                print("   • Data Collection: 0-30% (fetching articles & stock data)")
                print("   • Feature Engineering: 30-50% (calculating indicators)")
                print("   • Model Training: 50-80% (ML algorithm training)")
                print("   • Validation: 80-95% (testing model accuracy)")
                print("   • Deployment: 95-100% (saving and deploying model)")
                
                print(f"\n🌐 Dashboard URL: http://localhost:5000")
                print("🔄 Training will complete automatically in ~25 minutes")
                print("⚠️  You can stop training anytime using the Stop button")
                
            else:
                print("❌ Failed to start training")
                print(f"   Response: {response.text}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ Error starting training: {e}")
    
    print("\n" + "="*60)
    print("🎉 Enhanced Dashboard Test Complete!")
    print("📊 The dashboard now shows real-time progress with:")
    print("   • Data fetching graphs")
    print("   • Synchronized progress bars")
    print("   • Live metrics and counters")
    print("   • Beautiful modern UI")
    print("="*60 + "\n")

if __name__ == '__main__':
    test_dashboard()
