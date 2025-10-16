#!/usr/bin/env python3
"""
Test script to verify automatic data fetching for VUTAX 2.0
This script tests the data service and auto trainer functionality
"""

import asyncio
import sys
import os
import logging

# Add the ML service to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend', 'ml-service'))

from services.data_service import DataService
from services.auto_trainer import AutoTrainer
from utils.logger import setup_logger

logger = setup_logger(__name__)

async def test_data_service():
    """Test the data service functionality"""
    logger.info("🧪 Testing Data Service...")
    
    try:
        # Initialize data service
        data_service = DataService()
        await data_service.initialize()
        
        # Test getting stock data
        test_symbols = ['AAPL', 'MSFT', 'GOOGL']
        
        for symbol in test_symbols:
            logger.info(f"Testing data fetch for {symbol}...")
            
            try:
                # Test historical data
                data = await data_service.get_stock_data(symbol, period='1y')
                if data is not None and not data.empty:
                    logger.info(f"✅ {symbol}: Got {len(data)} historical records")
                else:
                    logger.warning(f"⚠️ {symbol}: No historical data received")
                
                # Test real-time data
                real_time = await data_service.get_real_time_price(symbol)
                if real_time:
                    logger.info(f"✅ {symbol}: Real-time price: ${real_time.get('price', 'N/A')}")
                else:
                    logger.warning(f"⚠️ {symbol}: No real-time data received")
                    
            except Exception as e:
                logger.error(f"❌ {symbol}: Data fetch failed - {e}")
        
        # Test market status
        try:
            market_status = await data_service.get_market_status()
            logger.info(f"✅ Market Status: {'OPEN' if market_status.is_open else 'CLOSED'}")
        except Exception as e:
            logger.error(f"❌ Market status failed - {e}")
        
        logger.info("✅ Data Service test completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Data Service test failed: {e}")
        return False

async def test_auto_trainer():
    """Test the auto trainer functionality"""
    logger.info("🧪 Testing Auto Trainer...")
    
    try:
        # Initialize auto trainer
        auto_trainer = AutoTrainer()
        await auto_trainer.initialize()
        
        # Test training status
        status = auto_trainer.get_training_status()
        logger.info(f"✅ Training Status: {status}")
        
        # Test data collection (small subset)
        logger.info("Testing data collection...")
        auto_trainer.stock_universe = ['AAPL', 'MSFT', 'GOOGL']  # Limit for testing
        
        try:
            training_data = await auto_trainer._collect_comprehensive_training_data()
            logger.info(f"✅ Collected training data for {len(training_data)} stocks")
            
            for symbol, data in training_data.items():
                logger.info(f"  - {symbol}: {len(data)} records")
                
        except Exception as e:
            logger.error(f"❌ Data collection failed: {e}")
            return False
        
        logger.info("✅ Auto Trainer test completed")
        return True
        
    except Exception as e:
        logger.error(f"❌ Auto Trainer test failed: {e}")
        return False

async def test_api_keys():
    """Test API key configuration"""
    logger.info("🧪 Testing API Keys...")
    
    # Check environment variables
    alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
    resend_key = os.getenv('RESEND_API_KEY')
    
    if alpha_vantage_key:
        logger.info("✅ Alpha Vantage API key found")
    else:
        logger.warning("⚠️ Alpha Vantage API key not found in environment")
    
    if resend_key:
        logger.info("✅ Resend API key found")
    else:
        logger.warning("⚠️ Resend API key not found in environment")
    
    # Test basic API connectivity
    try:
        import requests
        
        # Test Alpha Vantage (if key available)
        if alpha_vantage_key:
            url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol=AAPL&apikey={alpha_vantage_key}"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if 'Global Quote' in data:
                    logger.info("✅ Alpha Vantage API connectivity confirmed")
                else:
                    logger.warning("⚠️ Alpha Vantage API returned unexpected format")
            else:
                logger.warning(f"⚠️ Alpha Vantage API returned status {response.status_code}")
        
        # Test Yahoo Finance (free alternative)
        try:
            import yfinance as yf
            ticker = yf.Ticker("AAPL")
            info = ticker.info
            if info and 'currentPrice' in info:
                logger.info("✅ Yahoo Finance connectivity confirmed")
            else:
                logger.warning("⚠️ Yahoo Finance returned unexpected format")
        except Exception as e:
            logger.warning(f"⚠️ Yahoo Finance test failed: {e}")
        
    except Exception as e:
        logger.error(f"❌ API connectivity test failed: {e}")
    
    return True

async def main():
    """Main test function"""
    logger.info("🚀 Starting VUTAX 2.0 Data Fetch Tests...")
    
    # Load environment variables
    try:
        from dotenv import load_dotenv
        load_dotenv()
        logger.info("✅ Environment variables loaded")
    except ImportError:
        logger.warning("⚠️ python-dotenv not available, using system environment")
    except Exception as e:
        logger.warning(f"⚠️ Failed to load .env file: {e}")
    
    # Run tests
    tests = [
        ("API Keys", test_api_keys),
        ("Data Service", test_data_service),
        ("Auto Trainer", test_auto_trainer),
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        logger.info(f"\n{'='*50}")
        logger.info(f"Running {test_name} Test")
        logger.info(f"{'='*50}")
        
        try:
            result = await test_func()
            results[test_name] = result
        except Exception as e:
            logger.error(f"❌ {test_name} test crashed: {e}")
            results[test_name] = False
    
    # Summary
    logger.info(f"\n{'='*50}")
    logger.info("TEST SUMMARY")
    logger.info(f"{'='*50}")
    
    for test_name, result in results.items():
        status = "✅ PASSED" if result else "❌ FAILED"
        logger.info(f"{test_name}: {status}")
    
    passed = sum(results.values())
    total = len(results)
    
    logger.info(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        logger.info("🎉 All tests passed! Data fetching is working correctly.")
    else:
        logger.warning("⚠️ Some tests failed. Check the logs above for details.")
        logger.info("\n📋 Troubleshooting Tips:")
        logger.info("1. Make sure you have internet connectivity")
        logger.info("2. Check that API keys are set in .env file")
        logger.info("3. Verify that required Python packages are installed")
        logger.info("4. Try running: pip install -r backend/ml-service/requirements.txt")

if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Run the tests
    asyncio.run(main())
