#!/usr/bin/env python3
"""
VUTAX 2.0 - Dependency Installation Script
Installs all required packages for the Flask training system
"""

import subprocess
import sys
import os

def install_dependencies():
    """Install all required dependencies"""
    print("\n" + "="*60)
    print("🔧 VUTAX 2.0 - DEPENDENCY INSTALLATION")
    print("="*60)
    print("\n📦 This script will install:")
    print("   • Flask and Flask-SocketIO for web services")
    print("   • Pandas and NumPy for data processing")
    print("   • Scikit-learn for machine learning")
    print("   • Pandas-TA for technical analysis")
    print("   • YFinance for market data")
    print("   • Matplotlib for visualization")
    print("\n" + "="*60 + "\n")
    
    # Core packages that are essential
    core_packages = [
        'flask>=2.3.0',
        'flask-socketio>=5.3.0', 
        'requests>=2.31.0',
        'pandas>=2.0.0',
        'numpy>=1.24.0',
        'scikit-learn>=1.3.0'
    ]
    
    # ML and financial packages
    ml_packages = [
        'pandas-ta>=0.3.14b',
        'yfinance>=0.2.18',
        'matplotlib>=3.7.0'
    ]
    
    print("🚀 Installing core packages...")
    for package in core_packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', package
            ], capture_output=True, text=True, check=True)
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {package}")
            print(f"      Error: {e.stderr}")
    
    print("\n🤖 Installing ML and financial packages...")
    for package in ml_packages:
        try:
            print(f"   Installing {package}...")
            result = subprocess.run([
                sys.executable, '-m', 'pip', 'install', package
            ], capture_output=True, text=True, check=True)
            print(f"   ✅ {package} installed successfully")
        except subprocess.CalledProcessError as e:
            print(f"   ⚠️  Failed to install {package}")
            print(f"      Error: {e.stderr}")
            print(f"      This package may require additional setup")
    
    print("\n" + "="*60)
    print("✅ DEPENDENCY INSTALLATION COMPLETE!")
    print("="*60)
    print("\n🎯 Next steps:")
    print("   1. Run: python start_website.py (for Flask website)")
    print("   2. Run: python start_training.py (for AI training)")
    print("   3. Visit: http://localhost:3000 (main platform)")
    print("   4. Visit: http://localhost:5000 (training dashboard)")
    print("\n💡 If any packages failed to install:")
    print("   • Try: pip install -r requirements.txt")
    print("   • For pandas-ta issues: pip install --upgrade pandas-ta")
    print("   • For Windows TA-Lib: download from unofficial binaries")
    print("\n" + "="*60 + "\n")

if __name__ == '__main__':
    try:
        install_dependencies()
    except KeyboardInterrupt:
        print("\n❌ Installation cancelled by user")
    except Exception as e:
        print(f"\n❌ Installation failed: {e}")
        print("Please try manual installation: pip install -r requirements.txt")
