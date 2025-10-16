"""
Prediction Service for VUTAX 2.0
Handles price predictions and forecasting
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import asyncio

from utils.logger import setup_logger

logger = setup_logger(__name__)

class PredictionService:
    """
    Service for generating stock price predictions
    """
    
    def __init__(self, analytical_model, data_service):
        self.analytical_model = analytical_model
        self.data_service = data_service
        self.prediction_cache = {}
        self.cache_ttl = 300  # 5 minutes
        
    async def predict_price(
        self,
        symbol: str,
        timeframe: str = "1d",
        confidence_interval: float = 0.95
    ) -> Dict[str, Any]:
        """
        Generate price prediction for a stock
        """
        try:
            cache_key = f"{symbol}_{timeframe}_{confidence_interval}"
            
            # Check cache
            if cache_key in self.prediction_cache:
                cached_prediction, timestamp = self.prediction_cache[cache_key]
                if (datetime.now() - timestamp).seconds < self.cache_ttl:
                    return cached_prediction
            
            # Get stock data
            stock_data = await self.data_service.get_stock_data(symbol, period='1y')
            
            if stock_data is None or stock_data.empty:
                raise ValueError(f"No data available for {symbol}")
            
            # Generate prediction using analytical model
            analysis = await self.analytical_model.analyze_stock(symbol, stock_data)
            
            # Extract prediction from analysis
            prediction = analysis.prediction if hasattr(analysis, 'prediction') else {}
            
            # Enhance prediction with confidence intervals
            enhanced_prediction = await self._enhance_prediction_with_confidence(
                stock_data, prediction, confidence_interval
            )
            
            # Cache the prediction
            self.prediction_cache[cache_key] = (enhanced_prediction, datetime.now())
            
            return enhanced_prediction
            
        except Exception as e:
            logger.error(f"Error predicting price for {symbol}: {e}")
            raise
    
    async def _enhance_prediction_with_confidence(
        self,
        data: pd.DataFrame,
        base_prediction: Dict[str, Any],
        confidence_interval: float
    ) -> Dict[str, Any]:
        """
        Enhance prediction with confidence intervals
        """
        try:
            current_price = data['close'].iloc[-1]
            volatility = data['close'].pct_change().std() * np.sqrt(252)  # Annualized volatility
            
            # Calculate confidence intervals
            z_score = 1.96 if confidence_interval == 0.95 else 2.58  # 95% or 99%
            
            enhanced_prediction = {
                'current_price': current_price,
                'volatility': volatility,
                'confidence_interval': confidence_interval,
                'predictions': {}
            }
            
            # Process each timeframe prediction
            for timeframe, pred_data in base_prediction.items():
                if isinstance(pred_data, dict) and 'predicted_change' in pred_data:
                    predicted_change = pred_data['predicted_change']
                    confidence = pred_data.get('confidence', 50) / 100.0
                    
                    # Calculate predicted price
                    predicted_price = current_price * (1 + predicted_change)
                    
                    # Calculate confidence bounds
                    time_factor = self._get_time_factor(timeframe)
                    uncertainty = volatility * np.sqrt(time_factor) * (1 - confidence)
                    
                    upper_bound = predicted_price * (1 + z_score * uncertainty)
                    lower_bound = predicted_price * (1 - z_score * uncertainty)
                    
                    enhanced_prediction['predictions'][timeframe] = {
                        'predicted_price': predicted_price,
                        'predicted_change_percent': predicted_change * 100,
                        'confidence': confidence * 100,
                        'upper_bound': upper_bound,
                        'lower_bound': lower_bound,
                        'uncertainty': uncertainty
                    }
            
            return enhanced_prediction
            
        except Exception as e:
            logger.error(f"Error enhancing prediction: {e}")
            return base_prediction
    
    def _get_time_factor(self, timeframe: str) -> float:
        """
        Get time factor for volatility scaling
        """
        time_factors = {
            '1d': 1/252,
            '5d': 5/252,
            '1w': 7/252,
            '1m': 30/252,
            '3m': 90/252,
            '6m': 180/252,
            '1y': 1.0
        }
        return time_factors.get(timeframe, 1/252)
    
    async def update_predictions(self):
        """
        Update cached predictions
        """
        try:
            logger.info("Updating cached predictions...")
            
            # Clear old cache entries
            current_time = datetime.now()
            expired_keys = []
            
            for key, (_, timestamp) in self.prediction_cache.items():
                if (current_time - timestamp).seconds > self.cache_ttl:
                    expired_keys.append(key)
            
            for key in expired_keys:
                del self.prediction_cache[key]
            
            logger.info(f"Cleared {len(expired_keys)} expired predictions from cache")
            
        except Exception as e:
            logger.error(f"Error updating predictions: {e}")
    
    def get_cache_stats(self) -> Dict[str, Any]:
        """
        Get prediction cache statistics
        """
        return {
            'cached_predictions': len(self.prediction_cache),
            'cache_ttl_seconds': self.cache_ttl,
            'last_updated': datetime.now().isoformat()
        }
