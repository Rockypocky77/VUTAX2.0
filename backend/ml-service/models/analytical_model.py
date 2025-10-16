"""
Analytical Model for VUTAX 2.0
Handles stock ranking, buy/sell recommendations, risk scoring, and technical indicators
Target accuracy: 80%+
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
import joblib
import asyncio
from dataclasses import dataclass

# ML Libraries
from sklearn.ensemble import RandomForestRegressor, GradientBoostingClassifier
from sklearn.preprocessing import StandardScaler, RobustScaler
from sklearn.model_selection import TimeSeriesSplit, cross_val_score
from sklearn.metrics import accuracy_score, precision_score, recall_score

# Technical Analysis
import pandas_ta as ta
import talib

# Custom imports
from utils.logger import setup_logger
from services.data_service import DataService
from services.feature_engineering import FeatureEngineer
from utils.risk_calculator import RiskCalculator

logger = setup_logger(__name__)

@dataclass
class TechnicalIndicator:
    name: str
    value: float
    signal: str  # 'bullish', 'bearish', 'neutral'
    description: str
    confidence: float

@dataclass
class StockRecommendation:
    symbol: str
    action: str  # 'BUY', 'SELL', 'HOLD'
    risk_tier: str  # 'conservative', 'regular', 'high-risk'
    confidence: float  # 0-100
    target_price: Optional[float]
    stop_loss: Optional[float]
    reasoning: str
    timestamp: datetime
    valid_until: datetime

@dataclass
class StockAnalysis:
    symbol: str
    technical_indicators: List[TechnicalIndicator]
    sentiment_score: float
    prediction: Dict[str, Any]
    risk_metrics: Dict[str, float]
    recommendation: StockRecommendation

class AnalyticalModel:
    """
    Main analytical model for stock analysis and recommendations
    """
    
    def __init__(self):
        self.models = {}
        self.scalers = {}
        self.feature_engineer = FeatureEngineer()
        self.risk_calculator = RiskCalculator()
        self.data_service = None
        self.last_trained = None
        self.model_accuracy = {}
        self.is_initialized = False
        
        # Model parameters
        self.lookback_period = 252  # 1 year of trading days
        self.prediction_horizon = [1, 5, 22]  # 1 day, 1 week, 1 month
        self.risk_tiers = ['conservative', 'regular', 'high-risk']
        
    async def initialize(self):
        """Initialize the analytical model"""
        try:
            logger.info("Initializing Analytical Model...")
            
            # Initialize data service
            self.data_service = DataService()
            
            # Load or train models
            await self._load_or_train_models()
            
            self.is_initialized = True
            logger.info("✅ Analytical Model initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Analytical Model: {e}")
            raise
    
    def is_ready(self) -> bool:
        """Check if model is ready for inference"""
        return (
            self.is_initialized and 
            len(self.models) > 0 and 
            all(model is not None for model in self.models.values())
        )
    
    async def analyze_stock(
        self, 
        symbol: str, 
        data: pd.DataFrame = None,
        risk_tolerance: str = 'regular'
    ) -> StockAnalysis:
        """
        Perform comprehensive stock analysis
        """
        try:
            logger.info(f"Analyzing stock: {symbol}")
            
            # Get stock data if not provided
            if data is None:
                data = await self.data_service.get_stock_data(symbol, period='1y')
            
            # Calculate technical indicators
            technical_indicators = self._calculate_technical_indicators(data)
            
            # Generate features
            features = await self.feature_engineer.generate_features(data, symbol)
            
            # Make predictions
            prediction = await self._predict_price_movement(features, symbol)
            
            # Calculate risk metrics
            risk_metrics = self.risk_calculator.calculate_risk_metrics(data)
            
            # Generate recommendation
            recommendation = await self._generate_recommendation(
                symbol, technical_indicators, prediction, risk_metrics, risk_tolerance
            )
            
            return StockAnalysis(
                symbol=symbol,
                technical_indicators=technical_indicators,
                sentiment_score=0.0,  # Will be filled by sentiment service
                prediction=prediction,
                risk_metrics=risk_metrics,
                recommendation=recommendation
            )
            
        except Exception as e:
            logger.error(f"Error analyzing stock {symbol}: {e}")
            raise
    
    async def get_recommendations(
        self,
        risk_tier: str = 'regular',
        max_recommendations: int = 10,
        exclude_symbols: List[str] = None
    ) -> List[StockRecommendation]:
        """
        Get stock recommendations based on risk tier
        """
        try:
            logger.info(f"Generating recommendations for risk tier: {risk_tier}")
            
            # Get list of stocks to analyze (S&P 500 subset for now)
            symbols = await self._get_stock_universe(exclude_symbols)
            
            recommendations = []
            
            # Analyze each stock
            for symbol in symbols[:50]:  # Limit for performance
                try:
                    analysis = await self.analyze_stock(symbol, risk_tolerance=risk_tier)
                    
                    # Filter by risk tier and action
                    if (analysis.recommendation.risk_tier == risk_tier and 
                        analysis.recommendation.action in ['BUY', 'SELL']):
                        recommendations.append(analysis.recommendation)
                        
                except Exception as e:
                    logger.warning(f"Failed to analyze {symbol}: {e}")
                    continue
            
            # Sort by confidence and return top recommendations
            recommendations.sort(key=lambda x: x.confidence, reverse=True)
            return recommendations[:max_recommendations]
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {e}")
            raise
    
    def _calculate_technical_indicators(self, data: pd.DataFrame) -> List[TechnicalIndicator]:
        """Calculate technical indicators for stock analysis"""
        indicators = []
        
        try:
            # Price-based indicators
            sma_20 = ta.sma(data['close'], length=20).iloc[-1]
            sma_50 = ta.sma(data['close'], length=50).iloc[-1]
            current_price = data['close'].iloc[-1]
            
            # Moving Average signals
            if current_price > sma_20 > sma_50:
                ma_signal = 'bullish'
                ma_confidence = 0.8
            elif current_price < sma_20 < sma_50:
                ma_signal = 'bearish'
                ma_confidence = 0.8
            else:
                ma_signal = 'neutral'
                ma_confidence = 0.5
            
            indicators.append(TechnicalIndicator(
                name="Moving Average Trend",
                value=round((current_price - sma_20) / sma_20 * 100, 2),
                signal=ma_signal,
                description=f"Price vs 20-day SMA: {ma_signal}",
                confidence=ma_confidence
            ))
            
            # RSI
            rsi = ta.rsi(data['close'], length=14).iloc[-1]
            if rsi > 70:
                rsi_signal = 'bearish'  # Overbought
            elif rsi < 30:
                rsi_signal = 'bullish'  # Oversold
            else:
                rsi_signal = 'neutral'
            
            indicators.append(TechnicalIndicator(
                name="RSI",
                value=round(rsi, 2),
                signal=rsi_signal,
                description=f"RSI: {rsi:.1f} - {rsi_signal}",
                confidence=0.7
            ))
            
            # MACD
            macd_line = ta.macd(data['close'])['MACD_12_26_9'].iloc[-1]
            macd_signal = ta.macd(data['close'])['MACDs_12_26_9'].iloc[-1]
            
            if macd_line > macd_signal:
                macd_trend = 'bullish'
            else:
                macd_trend = 'bearish'
            
            indicators.append(TechnicalIndicator(
                name="MACD",
                value=round(macd_line - macd_signal, 4),
                signal=macd_trend,
                description=f"MACD: {macd_trend} crossover",
                confidence=0.75
            ))
            
            # Bollinger Bands
            bb = ta.bbands(data['close'], length=20)
            bb_upper = bb['BBU_20_2.0'].iloc[-1]
            bb_lower = bb['BBL_20_2.0'].iloc[-1]
            bb_middle = bb['BBM_20_2.0'].iloc[-1]
            
            if current_price > bb_upper:
                bb_signal = 'bearish'  # Overbought
            elif current_price < bb_lower:
                bb_signal = 'bullish'  # Oversold
            else:
                bb_signal = 'neutral'
            
            indicators.append(TechnicalIndicator(
                name="Bollinger Bands",
                value=round((current_price - bb_middle) / bb_middle * 100, 2),
                signal=bb_signal,
                description=f"Price position in Bollinger Bands: {bb_signal}",
                confidence=0.65
            ))
            
            # Volume analysis
            volume_sma = ta.sma(data['volume'], length=20).iloc[-1]
            current_volume = data['volume'].iloc[-1]
            
            volume_ratio = current_volume / volume_sma
            if volume_ratio > 1.5:
                volume_signal = 'bullish' if data['close'].iloc[-1] > data['close'].iloc[-2] else 'bearish'
            else:
                volume_signal = 'neutral'
            
            indicators.append(TechnicalIndicator(
                name="Volume Analysis",
                value=round(volume_ratio, 2),
                signal=volume_signal,
                description=f"Volume: {volume_ratio:.1f}x average",
                confidence=0.6
            ))
            
        except Exception as e:
            logger.error(f"Error calculating technical indicators: {e}")
        
        return indicators
    
    async def _predict_price_movement(self, features: np.ndarray, symbol: str) -> Dict[str, Any]:
        """Predict price movement using ML models"""
        try:
            predictions = {}
            
            for horizon in self.prediction_horizon:
                model_key = f"price_model_{horizon}d"
                if model_key in self.models:
                    model = self.models[model_key]
                    scaler = self.scalers.get(f"scaler_{horizon}d")
                    
                    if scaler:
                        features_scaled = scaler.transform(features.reshape(1, -1))
                    else:
                        features_scaled = features.reshape(1, -1)
                    
                    prediction = model.predict(features_scaled)[0]
                    confidence = min(self.model_accuracy.get(model_key, 0.5) * 100, 95)
                    
                    predictions[f"{horizon}d"] = {
                        "predicted_change": float(prediction),
                        "confidence": float(confidence)
                    }
            
            return predictions
            
        except Exception as e:
            logger.error(f"Error predicting price movement for {symbol}: {e}")
            return {}
    
    async def _generate_recommendation(
        self,
        symbol: str,
        technical_indicators: List[TechnicalIndicator],
        prediction: Dict[str, Any],
        risk_metrics: Dict[str, float],
        risk_tolerance: str
    ) -> StockRecommendation:
        """Generate buy/sell/hold recommendation"""
        try:
            # Calculate overall signal strength
            bullish_signals = sum(1 for ind in technical_indicators if ind.signal == 'bullish')
            bearish_signals = sum(1 for ind in technical_indicators if ind.signal == 'bearish')
            total_signals = len(technical_indicators)
            
            # Weight by confidence
            weighted_bullish = sum(ind.confidence for ind in technical_indicators if ind.signal == 'bullish')
            weighted_bearish = sum(ind.confidence for ind in technical_indicators if ind.signal == 'bearish')
            
            # Get prediction confidence
            pred_1d = prediction.get('1d', {})
            predicted_change = pred_1d.get('predicted_change', 0)
            pred_confidence = pred_1d.get('confidence', 50)
            
            # Determine action
            if weighted_bullish > weighted_bearish and predicted_change > 0.02:  # 2% threshold
                action = 'BUY'
                confidence = min((weighted_bullish / total_signals) * pred_confidence, 95)
            elif weighted_bearish > weighted_bullish and predicted_change < -0.02:
                action = 'SELL'
                confidence = min((weighted_bearish / total_signals) * pred_confidence, 95)
            else:
                action = 'HOLD'
                confidence = 50
            
            # Determine risk tier based on volatility and other factors
            volatility = risk_metrics.get('volatility', 0.2)
            if volatility < 0.15:
                risk_tier = 'conservative'
            elif volatility < 0.3:
                risk_tier = 'regular'
            else:
                risk_tier = 'high-risk'
            
            # Adjust for user risk tolerance
            if risk_tolerance != risk_tier:
                confidence *= 0.8  # Reduce confidence for mismatched risk
            
            # Generate reasoning
            reasoning = self._generate_reasoning(technical_indicators, prediction, action)
            
            return StockRecommendation(
                symbol=symbol,
                action=action,
                risk_tier=risk_tier,
                confidence=round(confidence, 1),
                target_price=None,  # TODO: Calculate target price
                stop_loss=None,     # TODO: Calculate stop loss
                reasoning=reasoning,
                timestamp=datetime.utcnow(),
                valid_until=datetime.utcnow() + timedelta(hours=24)
            )
            
        except Exception as e:
            logger.error(f"Error generating recommendation for {symbol}: {e}")
            raise
    
    def _generate_reasoning(
        self, 
        indicators: List[TechnicalIndicator], 
        prediction: Dict[str, Any], 
        action: str
    ) -> str:
        """Generate human-readable reasoning for recommendation"""
        try:
            bullish_indicators = [ind for ind in indicators if ind.signal == 'bullish']
            bearish_indicators = [ind for ind in indicators if ind.signal == 'bearish']
            
            if action == 'BUY':
                reasoning = f"BUY signal based on {len(bullish_indicators)} bullish indicators: "
                reasoning += ", ".join([ind.name for ind in bullish_indicators[:3]])
            elif action == 'SELL':
                reasoning = f"SELL signal based on {len(bearish_indicators)} bearish indicators: "
                reasoning += ", ".join([ind.name for ind in bearish_indicators[:3]])
            else:
                reasoning = "HOLD - Mixed signals with no clear directional bias"
            
            pred_1d = prediction.get('1d', {})
            if pred_1d:
                change = pred_1d.get('predicted_change', 0) * 100
                reasoning += f". AI predicts {change:+.1f}% movement in 1 day."
            
            return reasoning
            
        except Exception as e:
            logger.error(f"Error generating reasoning: {e}")
            return f"{action} recommendation based on technical analysis"
    
    async def _load_or_train_models(self):
        """Load existing models or train new ones"""
        try:
            # Try to load existing models
            model_loaded = await self._load_models()
            
            if not model_loaded:
                logger.info("No existing models found, training new models...")
                await self._train_models()
            else:
                logger.info("Existing models loaded successfully")
                
        except Exception as e:
            logger.error(f"Error loading/training models: {e}")
            raise
    
    async def _load_models(self) -> bool:
        """Load pre-trained models from disk"""
        try:
            import os
            model_dir = "models/saved"
            
            if not os.path.exists(model_dir):
                return False
            
            for horizon in self.prediction_horizon:
                model_path = f"{model_dir}/price_model_{horizon}d.joblib"
                scaler_path = f"{model_dir}/scaler_{horizon}d.joblib"
                
                if os.path.exists(model_path) and os.path.exists(scaler_path):
                    self.models[f"price_model_{horizon}d"] = joblib.load(model_path)
                    self.scalers[f"scaler_{horizon}d"] = joblib.load(scaler_path)
                else:
                    return False
            
            # Load accuracy metrics
            accuracy_path = f"{model_dir}/accuracy_metrics.joblib"
            if os.path.exists(accuracy_path):
                self.model_accuracy = joblib.load(accuracy_path)
            
            return True
            
        except Exception as e:
            logger.error(f"Error loading models: {e}")
            return False
    
    async def _train_models(self):
        """Train new ML models"""
        try:
            logger.info("Training analytical models...")
            
            # Get training data
            training_data = await self._prepare_training_data()
            
            for horizon in self.prediction_horizon:
                logger.info(f"Training {horizon}-day prediction model...")
                
                X, y = training_data[f"{horizon}d"]
                
                # Split data
                split_idx = int(len(X) * 0.8)
                X_train, X_test = X[:split_idx], X[split_idx:]
                y_train, y_test = y[:split_idx], y[split_idx:]
                
                # Scale features
                scaler = RobustScaler()
                X_train_scaled = scaler.fit_transform(X_train)
                X_test_scaled = scaler.transform(X_test)
                
                # Train model
                model = GradientBoostingClassifier(
                    n_estimators=100,
                    learning_rate=0.1,
                    max_depth=6,
                    random_state=42
                )
                
                model.fit(X_train_scaled, y_train)
                
                # Evaluate
                y_pred = model.predict(X_test_scaled)
                accuracy = accuracy_score(y_test, y_pred)
                
                # Store model and metrics
                model_key = f"price_model_{horizon}d"
                scaler_key = f"scaler_{horizon}d"
                
                self.models[model_key] = model
                self.scalers[scaler_key] = scaler
                self.model_accuracy[model_key] = accuracy
                
                logger.info(f"✅ {horizon}-day model trained with {accuracy:.3f} accuracy")
            
            # Save models
            await self._save_models()
            
            self.last_trained = datetime.utcnow()
            logger.info("✅ All models trained successfully")
            
        except Exception as e:
            logger.error(f"Error training models: {e}")
            raise
    
    async def _prepare_training_data(self) -> Dict[str, Tuple[np.ndarray, np.ndarray]]:
        """Prepare training data for all prediction horizons"""
        # This is a simplified version - in production, you'd want to:
        # 1. Download historical data for many stocks
        # 2. Calculate features for each stock
        # 3. Create labels based on future price movements
        # 4. Handle data quality and missing values
        
        # For now, return mock data structure
        training_data = {}
        
        for horizon in self.prediction_horizon:
            # Mock training data - replace with real data preparation
            n_samples = 10000
            n_features = 50
            
            X = np.random.randn(n_samples, n_features)
            y = np.random.choice([0, 1, 2], n_samples)  # 0: down, 1: flat, 2: up
            
            training_data[f"{horizon}d"] = (X, y)
        
        return training_data
    
    async def _save_models(self):
        """Save trained models to disk"""
        try:
            import os
            model_dir = "models/saved"
            os.makedirs(model_dir, exist_ok=True)
            
            for horizon in self.prediction_horizon:
                model_key = f"price_model_{horizon}d"
                scaler_key = f"scaler_{horizon}d"
                
                if model_key in self.models:
                    joblib.dump(self.models[model_key], f"{model_dir}/{model_key}.joblib")
                    joblib.dump(self.scalers[scaler_key], f"{model_dir}/scaler_{horizon}d.joblib")
            
            # Save accuracy metrics
            joblib.dump(self.model_accuracy, f"{model_dir}/accuracy_metrics.joblib")
            
            logger.info("✅ Models saved successfully")
            
        except Exception as e:
            logger.error(f"Error saving models: {e}")
    
    async def _get_stock_universe(self, exclude_symbols: List[str] = None) -> List[str]:
        """Get list of stocks to analyze"""
        # S&P 500 subset for demonstration
        sp500_subset = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.B',
            'UNH', 'JNJ', 'JPM', 'V', 'PG', 'HD', 'MA', 'BAC', 'ABBV', 'PFE',
            'KO', 'AVGO', 'PEP', 'TMO', 'COST', 'DIS', 'ABT', 'ACN', 'VZ',
            'ADBE', 'DHR', 'NEE', 'BMY', 'CMCSA', 'CRM', 'NFLX', 'NKE'
        ]
        
        if exclude_symbols:
            return [s for s in sp500_subset if s not in exclude_symbols]
        
        return sp500_subset
    
    async def retrain(self):
        """Retrain models with latest data"""
        try:
            logger.info("Retraining analytical models...")
            await self._train_models()
            logger.info("✅ Models retrained successfully")
        except Exception as e:
            logger.error(f"Error retraining models: {e}")
            raise
    
    async def update_market_data(self):
        """Update market data and recalibrate models if needed"""
        try:
            logger.info("Updating market data...")
            # Implementation for updating market data
            # This would typically involve:
            # 1. Fetching latest market data
            # 2. Updating feature calculations
            # 3. Recalibrating model thresholds if needed
            pass
        except Exception as e:
            logger.error(f"Error updating market data: {e}")
    
    def get_accuracy(self) -> Dict[str, float]:
        """Get model accuracy metrics"""
        return self.model_accuracy.copy()
