"""
Data Service for VUTAX 2.0
Handles real-time and historical stock data from multiple sources
"""

import asyncio
import aiohttp
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any, Tuple
import os
from dataclasses import dataclass
import redis
import json
from alpha_vantage.timeseries import TimeSeries
from alpha_vantage.fundamentaldata import FundamentalData

from utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class StockData:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: int
    adjusted_close: Optional[float] = None

@dataclass
class MarketStatus:
    is_open: bool
    next_open: Optional[datetime]
    next_close: Optional[datetime]
    timezone: str

class DataService:
    """
    Unified data service for stock market data
    """
    
    def __init__(self):
        self.alpha_vantage_key = os.getenv('ALPHA_VANTAGE_API_KEY')
        self.polygon_key = os.getenv('POLYGON_API_KEY')
        self.redis_client = None
        self.session = None
        
        # Data sources
        self.alpha_vantage_ts = None
        self.alpha_vantage_fd = None
        
        # Cache settings
        self.cache_ttl = {
            'intraday': 60,      # 1 minute for real-time data
            'daily': 3600,       # 1 hour for daily data
            'historical': 86400,  # 24 hours for historical data
        }
        
        # Rate limiting
        self.rate_limits = {
            'alpha_vantage': {'calls': 5, 'period': 60},  # 5 calls per minute
            'polygon': {'calls': 100, 'period': 60},      # 100 calls per minute
            'yahoo': {'calls': 2000, 'period': 3600},     # 2000 calls per hour
        }
        
    async def initialize(self):
        """Initialize data service"""
        try:
            logger.info("Initializing Data Service...")
            
            # Initialize Redis for caching
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'localhost'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                decode_responses=True
            )
            
            # Initialize HTTP session
            self.session = aiohttp.ClientSession()
            
            # Initialize Alpha Vantage
            if self.alpha_vantage_key:
                self.alpha_vantage_ts = TimeSeries(key=self.alpha_vantage_key, output_format='pandas')
                self.alpha_vantage_fd = FundamentalData(key=self.alpha_vantage_key, output_format='pandas')
                logger.info("✅ Alpha Vantage initialized")
            else:
                logger.warning("⚠️ Alpha Vantage API key not found")
            
            logger.info("✅ Data Service initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Data Service: {e}")
            raise
    
    async def get_stock_data(
        self, 
        symbol: str, 
        period: str = '1y',
        interval: str = '1d'
    ) -> pd.DataFrame:
        """
        Get stock data with caching
        """
        try:
            cache_key = f"stock_data:{symbol}:{period}:{interval}"
            
            # Try cache first
            cached_data = await self._get_from_cache(cache_key)
            if cached_data is not None:
                return cached_data
            
            # Fetch from primary source
            data = await self._fetch_stock_data_yahoo(symbol, period, interval)
            
            if data is not None and not data.empty:
                # Cache the data
                await self._set_cache(cache_key, data, self.cache_ttl['daily'])
                return data
            
            # Fallback to Alpha Vantage
            if self.alpha_vantage_key:
                data = await self._fetch_stock_data_alpha_vantage(symbol, period)
                if data is not None and not data.empty:
                    await self._set_cache(cache_key, data, self.cache_ttl['daily'])
                    return data
            
            raise Exception(f"No data available for {symbol}")
            
        except Exception as e:
            logger.error(f"Error getting stock data for {symbol}: {e}")
            raise
    
    async def get_real_time_price(self, symbol: str) -> Dict[str, Any]:
        """
        Get real-time stock price
        """
        try:
            cache_key = f"realtime:{symbol}"
            
            # Check cache (1-minute TTL for real-time data)
            cached_price = await self._get_from_cache(cache_key)
            if cached_price is not None:
                return cached_price
            
            # Fetch real-time data
            price_data = await self._fetch_realtime_yahoo(symbol)
            
            if price_data:
                await self._set_cache(cache_key, price_data, self.cache_ttl['intraday'])
                return price_data
            
            # Fallback to Alpha Vantage
            if self.alpha_vantage_key:
                price_data = await self._fetch_realtime_alpha_vantage(symbol)
                if price_data:
                    await self._set_cache(cache_key, price_data, self.cache_ttl['intraday'])
                    return price_data
            
            raise Exception(f"No real-time data available for {symbol}")
            
        except Exception as e:
            logger.error(f"Error getting real-time price for {symbol}: {e}")
            raise
    
    async def get_multiple_stocks(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        Get real-time data for multiple stocks efficiently
        """
        try:
            tasks = []
            for symbol in symbols:
                task = asyncio.create_task(self.get_real_time_price(symbol))
                tasks.append((symbol, task))
            
            results = {}
            for symbol, task in tasks:
                try:
                    results[symbol] = await task
                except Exception as e:
                    logger.warning(f"Failed to get data for {symbol}: {e}")
                    results[symbol] = None
            
            return results
            
        except Exception as e:
            logger.error(f"Error getting multiple stocks data: {e}")
            raise
    
    async def get_market_status(self) -> MarketStatus:
        """
        Get current market status
        """
        try:
            cache_key = "market_status"
            
            # Check cache
            cached_status = await self._get_from_cache(cache_key)
            if cached_status is not None:
                return MarketStatus(**cached_status)
            
            # Calculate market status
            now = datetime.now()
            
            # US market hours: 9:30 AM - 4:00 PM ET, Monday-Friday
            market_open_time = now.replace(hour=9, minute=30, second=0, microsecond=0)
            market_close_time = now.replace(hour=16, minute=0, second=0, microsecond=0)
            
            is_weekday = now.weekday() < 5  # Monday = 0, Sunday = 6
            is_market_hours = market_open_time <= now <= market_close_time
            
            is_open = is_weekday and is_market_hours
            
            # Calculate next open/close
            if is_open:
                next_close = market_close_time
                next_open = None
            else:
                if now < market_open_time and is_weekday:
                    next_open = market_open_time
                else:
                    # Next business day
                    days_ahead = 1
                    if now.weekday() == 4:  # Friday
                        days_ahead = 3  # Skip to Monday
                    elif now.weekday() == 5:  # Saturday
                        days_ahead = 2  # Skip to Monday
                    
                    next_open = (now + timedelta(days=days_ahead)).replace(
                        hour=9, minute=30, second=0, microsecond=0
                    )
                
                next_close = None
            
            status = MarketStatus(
                is_open=is_open,
                next_open=next_open,
                next_close=next_close,
                timezone="US/Eastern"
            )
            
            # Cache for 1 minute
            await self._set_cache(cache_key, status.__dict__, 60)
            
            return status
            
        except Exception as e:
            logger.error(f"Error getting market status: {e}")
            raise
    
    async def get_company_info(self, symbol: str) -> Dict[str, Any]:
        """
        Get company fundamental information
        """
        try:
            cache_key = f"company_info:{symbol}"
            
            # Check cache (24-hour TTL)
            cached_info = await self._get_from_cache(cache_key)
            if cached_info is not None:
                return cached_info
            
            # Fetch from Yahoo Finance
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Extract relevant information
            company_info = {
                'symbol': symbol,
                'name': info.get('longName', symbol),
                'sector': info.get('sector'),
                'industry': info.get('industry'),
                'market_cap': info.get('marketCap'),
                'employees': info.get('fullTimeEmployees'),
                'description': info.get('longBusinessSummary'),
                'website': info.get('website'),
                'pe_ratio': info.get('trailingPE'),
                'forward_pe': info.get('forwardPE'),
                'price_to_book': info.get('priceToBook'),
                'dividend_yield': info.get('dividendYield'),
                'beta': info.get('beta'),
                '52_week_high': info.get('fiftyTwoWeekHigh'),
                '52_week_low': info.get('fiftyTwoWeekLow'),
            }
            
            # Cache for 24 hours
            await self._set_cache(cache_key, company_info, self.cache_ttl['historical'])
            
            return company_info
            
        except Exception as e:
            logger.error(f"Error getting company info for {symbol}: {e}")
            raise
    
    async def _fetch_stock_data_yahoo(
        self, 
        symbol: str, 
        period: str = '1y',
        interval: str = '1d'
    ) -> pd.DataFrame:
        """
        Fetch stock data from Yahoo Finance
        """
        try:
            ticker = yf.Ticker(symbol)
            data = ticker.history(period=period, interval=interval)
            
            if data.empty:
                return None
            
            # Standardize column names
            data.columns = [col.lower().replace(' ', '_') for col in data.columns]
            data.reset_index(inplace=True)
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching Yahoo Finance data for {symbol}: {e}")
            return None
    
    async def _fetch_stock_data_alpha_vantage(
        self, 
        symbol: str, 
        period: str = '1y'
    ) -> pd.DataFrame:
        """
        Fetch stock data from Alpha Vantage
        """
        try:
            if not self.alpha_vantage_ts:
                return None
            
            # Get daily data
            data, meta_data = self.alpha_vantage_ts.get_daily_adjusted(
                symbol=symbol, outputsize='full'
            )
            
            if data.empty:
                return None
            
            # Standardize format
            data.reset_index(inplace=True)
            data.columns = ['date', 'open', 'high', 'low', 'close', 'adjusted_close', 'volume', 'dividend', 'split']
            
            # Filter by period
            if period == '1y':
                cutoff_date = datetime.now() - timedelta(days=365)
                data = data[data['date'] >= cutoff_date]
            
            return data
            
        except Exception as e:
            logger.error(f"Error fetching Alpha Vantage data for {symbol}: {e}")
            return None
    
    async def _fetch_realtime_yahoo(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch real-time price from Yahoo Finance
        """
        try:
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            return {
                'symbol': symbol,
                'price': info.get('currentPrice') or info.get('regularMarketPrice'),
                'change': info.get('regularMarketChange'),
                'change_percent': info.get('regularMarketChangePercent'),
                'volume': info.get('regularMarketVolume'),
                'market_cap': info.get('marketCap'),
                'timestamp': datetime.now().isoformat(),
                'source': 'yahoo'
            }
            
        except Exception as e:
            logger.error(f"Error fetching Yahoo real-time data for {symbol}: {e}")
            return None
    
    async def _fetch_realtime_alpha_vantage(self, symbol: str) -> Dict[str, Any]:
        """
        Fetch real-time price from Alpha Vantage
        """
        try:
            if not self.alpha_vantage_ts:
                return None
            
            data, _ = self.alpha_vantage_ts.get_quote_endpoint(symbol)
            
            if data.empty:
                return None
            
            latest = data.iloc[0]
            
            return {
                'symbol': symbol,
                'price': float(latest['05. price']),
                'change': float(latest['09. change']),
                'change_percent': float(latest['10. change percent'].replace('%', '')),
                'volume': int(latest['06. volume']),
                'timestamp': datetime.now().isoformat(),
                'source': 'alpha_vantage'
            }
            
        except Exception as e:
            logger.error(f"Error fetching Alpha Vantage real-time data for {symbol}: {e}")
            return None
    
    async def _get_from_cache(self, key: str) -> Any:
        """
        Get data from Redis cache
        """
        try:
            if not self.redis_client:
                return None
            
            cached_data = self.redis_client.get(key)
            if cached_data:
                return json.loads(cached_data)
            
            return None
            
        except Exception as e:
            logger.warning(f"Cache get error for key {key}: {e}")
            return None
    
    async def _set_cache(self, key: str, data: Any, ttl: int):
        """
        Set data in Redis cache
        """
        try:
            if not self.redis_client:
                return
            
            # Handle pandas DataFrame
            if isinstance(data, pd.DataFrame):
                data_dict = {
                    'data': data.to_dict('records'),
                    'columns': data.columns.tolist(),
                    'index': data.index.tolist(),
                    'type': 'dataframe'
                }
                self.redis_client.setex(key, ttl, json.dumps(data_dict, default=str))
            else:
                self.redis_client.setex(key, ttl, json.dumps(data, default=str))
                
        except Exception as e:
            logger.warning(f"Cache set error for key {key}: {e}")
    
    async def close(self):
        """
        Close connections
        """
        if self.session:
            await self.session.close()
        
        if self.redis_client:
            self.redis_client.close()
    
    def __del__(self):
        """
        Cleanup on deletion
        """
        if hasattr(self, 'session') and self.session:
            asyncio.create_task(self.session.close())
