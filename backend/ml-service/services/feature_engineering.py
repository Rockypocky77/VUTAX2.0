"""
Feature Engineering Service for VUTAX 2.0
Generates comprehensive features for ML model training
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Any
import pandas_ta as ta
import talib
from datetime import datetime, timedelta
import asyncio

from utils.logger import setup_logger

logger = setup_logger(__name__)

class FeatureEngineer:
    """
    Advanced feature engineering for stock market data
    """
    
    def __init__(self):
        self.feature_cache = {}
        self.lookback_periods = [5, 10, 20, 50, 200]  # Common technical analysis periods
        
    async def generate_features(self, data: pd.DataFrame, symbol: str) -> np.ndarray:
        """
        Generate comprehensive feature set for a stock
        """
        try:
            if data is None or data.empty:
                return None
            
            # Ensure we have required columns
            required_columns = ['open', 'high', 'low', 'close', 'volume']
            if not all(col in data.columns for col in required_columns):
                logger.warning(f"Missing required columns for {symbol}")
                return None
            
            features = []
            
            # Price-based features
            price_features = self._generate_price_features(data)
            features.extend(price_features)
            
            # Technical indicator features
            technical_features = self._generate_technical_features(data)
            features.extend(technical_features)
            
            # Volume features
            volume_features = self._generate_volume_features(data)
            features.extend(volume_features)
            
            # Volatility features
            volatility_features = self._generate_volatility_features(data)
            features.extend(volatility_features)
            
            # Momentum features
            momentum_features = self._generate_momentum_features(data)
            features.extend(momentum_features)
            
            # Pattern features
            pattern_features = self._generate_pattern_features(data)
            features.extend(pattern_features)
            
            # Market structure features
            structure_features = self._generate_market_structure_features(data)
            features.extend(structure_features)
            
            # Time-based features
            time_features = self._generate_time_features(data)
            features.extend(time_features)
            
            # Convert to numpy array
            feature_array = np.array(features).reshape(1, -1)
            
            logger.debug(f"Generated {len(features)} features for {symbol}")
            return feature_array
            
        except Exception as e:
            logger.error(f"Error generating features for {symbol}: {e}")
            return None
    
    def _generate_price_features(self, data: pd.DataFrame) -> List[float]:
        """Generate price-based features"""
        features = []
        
        try:
            close = data['close']
            high = data['high']
            low = data['low']
            open_price = data['open']
            
            # Current price relative to recent highs/lows
            for period in [5, 10, 20]:
                if len(close) >= period:
                    recent_high = high.rolling(period).max().iloc[-1]
                    recent_low = low.rolling(period).min().iloc[-1]
                    current_price = close.iloc[-1]
                    
                    # Position within recent range
                    if recent_high != recent_low:
                        position_in_range = (current_price - recent_low) / (recent_high - recent_low)
                        features.append(position_in_range)
                    else:
                        features.append(0.5)  # Neutral position
                    
                    # Distance from recent high/low
                    features.append((current_price - recent_high) / recent_high)
                    features.append((current_price - recent_low) / recent_low)
            
            # Price gaps
            if len(data) >= 2:
                prev_close = close.iloc[-2]
                current_open = open_price.iloc[-1]
                gap = (current_open - prev_close) / prev_close
                features.append(gap)
            else:
                features.append(0.0)
            
            # Intraday range
            current_range = (high.iloc[-1] - low.iloc[-1]) / close.iloc[-1]
            features.append(current_range)
            
            # Body vs shadow ratios (candlestick analysis)
            body_size = abs(close.iloc[-1] - open_price.iloc[-1]) / close.iloc[-1]
            upper_shadow = (high.iloc[-1] - max(close.iloc[-1], open_price.iloc[-1])) / close.iloc[-1]
            lower_shadow = (min(close.iloc[-1], open_price.iloc[-1]) - low.iloc[-1]) / close.iloc[-1]
            
            features.extend([body_size, upper_shadow, lower_shadow])
            
        except Exception as e:
            logger.warning(f"Error in price features: {e}")
            # Return zeros if calculation fails
            features = [0.0] * 20  # Expected number of price features
        
        return features
    
    def _generate_technical_features(self, data: pd.DataFrame) -> List[float]:
        """Generate technical indicator features"""
        features = []
        
        try:
            close = data['close']
            high = data['high']
            low = data['low']
            volume = data['volume']
            
            # Moving averages and their relationships
            for period in [5, 10, 20, 50]:
                if len(close) >= period:
                    ma = ta.sma(close, length=period)
                    if not ma.empty:
                        current_ma = ma.iloc[-1]
                        # Price relative to MA
                        features.append((close.iloc[-1] - current_ma) / current_ma)
                        
                        # MA slope
                        if len(ma) >= 2:
                            ma_slope = (ma.iloc[-1] - ma.iloc[-2]) / ma.iloc[-2]
                            features.append(ma_slope)
                        else:
                            features.append(0.0)
                    else:
                        features.extend([0.0, 0.0])
                else:
                    features.extend([0.0, 0.0])
            
            # RSI
            rsi = ta.rsi(close, length=14)
            if not rsi.empty:
                features.append(rsi.iloc[-1] / 100.0)  # Normalize to 0-1
            else:
                features.append(0.5)
            
            # MACD
            macd_data = ta.macd(close)
            if macd_data is not None and not macd_data.empty:
                macd_line = macd_data['MACD_12_26_9'].iloc[-1] if 'MACD_12_26_9' in macd_data.columns else 0
                macd_signal = macd_data['MACDs_12_26_9'].iloc[-1] if 'MACDs_12_26_9' in macd_data.columns else 0
                macd_histogram = macd_data['MACDh_12_26_9'].iloc[-1] if 'MACDh_12_26_9' in macd_data.columns else 0
                
                # Normalize MACD values
                features.extend([
                    np.tanh(macd_line),  # Bounded between -1 and 1
                    np.tanh(macd_signal),
                    np.tanh(macd_histogram)
                ])
            else:
                features.extend([0.0, 0.0, 0.0])
            
            # Bollinger Bands
            bb = ta.bbands(close, length=20)
            if bb is not None and not bb.empty:
                bb_upper = bb['BBU_20_2.0'].iloc[-1] if 'BBU_20_2.0' in bb.columns else close.iloc[-1]
                bb_lower = bb['BBL_20_2.0'].iloc[-1] if 'BBL_20_2.0' in bb.columns else close.iloc[-1]
                bb_middle = bb['BBM_20_2.0'].iloc[-1] if 'BBM_20_2.0' in bb.columns else close.iloc[-1]
                
                # Position within Bollinger Bands
                if bb_upper != bb_lower:
                    bb_position = (close.iloc[-1] - bb_lower) / (bb_upper - bb_lower)
                    features.append(bb_position)
                else:
                    features.append(0.5)
                
                # Bollinger Band width (volatility measure)
                bb_width = (bb_upper - bb_lower) / bb_middle
                features.append(bb_width)
            else:
                features.extend([0.5, 0.0])
            
            # Stochastic Oscillator
            stoch = ta.stoch(high, low, close)
            if stoch is not None and not stoch.empty:
                stoch_k = stoch['STOCHk_14_3_3'].iloc[-1] if 'STOCHk_14_3_3' in stoch.columns else 50
                stoch_d = stoch['STOCHd_14_3_3'].iloc[-1] if 'STOCHd_14_3_3' in stoch.columns else 50
                features.extend([stoch_k / 100.0, stoch_d / 100.0])
            else:
                features.extend([0.5, 0.5])
            
            # Williams %R
            willr = ta.willr(high, low, close)
            if not willr.empty:
                features.append((willr.iloc[-1] + 100) / 100.0)  # Normalize to 0-1
            else:
                features.append(0.5)
            
        except Exception as e:
            logger.warning(f"Error in technical features: {e}")
            # Return zeros if calculation fails
            features = [0.0] * 20  # Expected number of technical features
        
        return features
    
    def _generate_volume_features(self, data: pd.DataFrame) -> List[float]:
        """Generate volume-based features"""
        features = []
        
        try:
            volume = data['volume']
            close = data['close']
            
            # Volume moving averages
            for period in [5, 20]:
                if len(volume) >= period:
                    vol_ma = volume.rolling(period).mean().iloc[-1]
                    current_vol = volume.iloc[-1]
                    
                    # Volume relative to average
                    if vol_ma > 0:
                        vol_ratio = current_vol / vol_ma
                        features.append(np.log1p(vol_ratio))  # Log transform for stability
                    else:
                        features.append(0.0)
                else:
                    features.append(0.0)
            
            # Volume trend
            if len(volume) >= 5:
                vol_trend = np.polyfit(range(5), volume.iloc[-5:].values, 1)[0]
                features.append(np.tanh(vol_trend / volume.iloc[-1]))  # Normalized trend
            else:
                features.append(0.0)
            
            # On-Balance Volume (OBV)
            obv = ta.obv(close, volume)
            if not obv.empty and len(obv) >= 2:
                obv_change = (obv.iloc[-1] - obv.iloc[-2]) / abs(obv.iloc[-2]) if obv.iloc[-2] != 0 else 0
                features.append(np.tanh(obv_change))
            else:
                features.append(0.0)
            
            # Volume Price Trend (VPT)
            vpt = ta.vpt(close, volume)
            if not vpt.empty and len(vpt) >= 2:
                vpt_change = (vpt.iloc[-1] - vpt.iloc[-2]) / abs(vpt.iloc[-2]) if vpt.iloc[-2] != 0 else 0
                features.append(np.tanh(vpt_change))
            else:
                features.append(0.0)
            
        except Exception as e:
            logger.warning(f"Error in volume features: {e}")
            features = [0.0] * 5  # Expected number of volume features
        
        return features
    
    def _generate_volatility_features(self, data: pd.DataFrame) -> List[float]:
        """Generate volatility-based features"""
        features = []
        
        try:
            close = data['close']
            high = data['high']
            low = data['low']
            
            # Historical volatility (different periods)
            for period in [5, 20]:
                if len(close) >= period + 1:
                    returns = close.pct_change().dropna()
                    if len(returns) >= period:
                        volatility = returns.rolling(period).std().iloc[-1]
                        features.append(volatility * np.sqrt(252))  # Annualized volatility
                    else:
                        features.append(0.0)
                else:
                    features.append(0.0)
            
            # Average True Range (ATR)
            atr = ta.atr(high, low, close, length=14)
            if not atr.empty:
                atr_normalized = atr.iloc[-1] / close.iloc[-1]
                features.append(atr_normalized)
            else:
                features.append(0.0)
            
            # Volatility ratio (short vs long term)
            if len(close) >= 21:
                short_vol = close.pct_change().rolling(5).std().iloc[-1]
                long_vol = close.pct_change().rolling(20).std().iloc[-1]
                if long_vol > 0:
                    vol_ratio = short_vol / long_vol
                    features.append(vol_ratio)
                else:
                    features.append(1.0)
            else:
                features.append(1.0)
            
        except Exception as e:
            logger.warning(f"Error in volatility features: {e}")
            features = [0.0] * 4  # Expected number of volatility features
        
        return features
    
    def _generate_momentum_features(self, data: pd.DataFrame) -> List[float]:
        """Generate momentum-based features"""
        features = []
        
        try:
            close = data['close']
            
            # Rate of Change (ROC) for different periods
            for period in [1, 5, 10]:
                if len(close) >= period + 1:
                    roc = (close.iloc[-1] - close.iloc[-1-period]) / close.iloc[-1-period]
                    features.append(roc)
                else:
                    features.append(0.0)
            
            # Momentum oscillator
            if len(close) >= 11:
                momentum = close.iloc[-1] - close.iloc[-11]
                momentum_normalized = momentum / close.iloc[-11]
                features.append(momentum_normalized)
            else:
                features.append(0.0)
            
            # Price acceleration (second derivative)
            if len(close) >= 3:
                acceleration = (close.iloc[-1] - close.iloc[-2]) - (close.iloc[-2] - close.iloc[-3])
                acceleration_normalized = acceleration / close.iloc[-3]
                features.append(acceleration_normalized)
            else:
                features.append(0.0)
            
        except Exception as e:
            logger.warning(f"Error in momentum features: {e}")
            features = [0.0] * 5  # Expected number of momentum features
        
        return features
    
    def _generate_pattern_features(self, data: pd.DataFrame) -> List[float]:
        """Generate pattern recognition features"""
        features = []
        
        try:
            open_price = data['open'].values
            high = data['high'].values
            low = data['low'].values
            close = data['close'].values
            
            if len(close) >= 3:
                # Candlestick patterns (simplified)
                
                # Doji pattern
                body_size = abs(close[-1] - open_price[-1])
                total_range = high[-1] - low[-1]
                is_doji = (body_size / total_range) < 0.1 if total_range > 0 else 0
                features.append(float(is_doji))
                
                # Hammer pattern
                lower_shadow = min(close[-1], open_price[-1]) - low[-1]
                upper_shadow = high[-1] - max(close[-1], open_price[-1])
                is_hammer = (lower_shadow > 2 * body_size) and (upper_shadow < body_size) if total_range > 0 else 0
                features.append(float(is_hammer))
                
                # Engulfing pattern
                if len(close) >= 2:
                    prev_body = abs(close[-2] - open_price[-2])
                    curr_body = abs(close[-1] - open_price[-1])
                    is_engulfing = curr_body > prev_body and (
                        (close[-1] > open_price[-1] and close[-2] < open_price[-2] and 
                         close[-1] > open_price[-2] and open_price[-1] < close[-2]) or
                        (close[-1] < open_price[-1] and close[-2] > open_price[-2] and 
                         close[-1] < open_price[-2] and open_price[-1] > close[-2])
                    )
                    features.append(float(is_engulfing))
                else:
                    features.append(0.0)
                
                # Gap patterns
                if len(close) >= 2:
                    gap_up = open_price[-1] > close[-2]
                    gap_down = open_price[-1] < close[-2]
                    features.extend([float(gap_up), float(gap_down)])
                else:
                    features.extend([0.0, 0.0])
            else:
                features = [0.0] * 5  # Default pattern features
            
        except Exception as e:
            logger.warning(f"Error in pattern features: {e}")
            features = [0.0] * 5  # Expected number of pattern features
        
        return features
    
    def _generate_market_structure_features(self, data: pd.DataFrame) -> List[float]:
        """Generate market structure features"""
        features = []
        
        try:
            close = data['close']
            high = data['high']
            low = data['low']
            
            # Support and resistance levels
            if len(close) >= 20:
                # Recent highs and lows
                recent_highs = high.rolling(10).max()
                recent_lows = low.rolling(10).min()
                
                # Distance to nearest support/resistance
                current_price = close.iloc[-1]
                nearest_resistance = recent_highs.iloc[-10:].min()
                nearest_support = recent_lows.iloc[-10:].max()
                
                if nearest_resistance > 0:
                    resistance_distance = (nearest_resistance - current_price) / current_price
                    features.append(resistance_distance)
                else:
                    features.append(0.0)
                
                if nearest_support > 0:
                    support_distance = (current_price - nearest_support) / current_price
                    features.append(support_distance)
                else:
                    features.append(0.0)
            else:
                features.extend([0.0, 0.0])
            
            # Trend strength
            if len(close) >= 20:
                # Linear regression slope
                x = np.arange(len(close))
                slope = np.polyfit(x, close.values, 1)[0]
                trend_strength = slope / close.iloc[0] if close.iloc[0] > 0 else 0
                features.append(trend_strength)
                
                # R-squared (trend consistency)
                correlation = np.corrcoef(x, close.values)[0, 1]
                r_squared = correlation ** 2
                features.append(r_squared)
            else:
                features.extend([0.0, 0.0])
            
        except Exception as e:
            logger.warning(f"Error in market structure features: {e}")
            features = [0.0] * 4  # Expected number of structure features
        
        return features
    
    def _generate_time_features(self, data: pd.DataFrame) -> List[float]:
        """Generate time-based features"""
        features = []
        
        try:
            # If we have datetime index, extract time features
            if hasattr(data.index, 'hour'):
                # Hour of day (market hours effect)
                current_hour = data.index[-1].hour if len(data) > 0 else 12
                hour_normalized = current_hour / 24.0
                features.append(hour_normalized)
                
                # Day of week effect
                current_dow = data.index[-1].dayofweek if len(data) > 0 else 2
                dow_normalized = current_dow / 6.0
                features.append(dow_normalized)
                
                # Month effect
                current_month = data.index[-1].month if len(data) > 0 else 6
                month_normalized = current_month / 12.0
                features.append(month_normalized)
            else:
                # Default time features if no datetime index
                features.extend([0.5, 0.5, 0.5])
            
            # Days since recent high/low
            if len(data) >= 20:
                high_idx = data['high'].rolling(20).apply(lambda x: x.argmax()).iloc[-1]
                low_idx = data['low'].rolling(20).apply(lambda x: x.argmin()).iloc[-1]
                
                days_since_high = (len(data) - 1 - high_idx) / 20.0
                days_since_low = (len(data) - 1 - low_idx) / 20.0
                
                features.extend([days_since_high, days_since_low])
            else:
                features.extend([0.5, 0.5])
            
        except Exception as e:
            logger.warning(f"Error in time features: {e}")
            features = [0.5, 0.5, 0.5, 0.5, 0.5]  # Default time features
        
        return features
    
    def get_feature_names(self) -> List[str]:
        """Get names of all generated features"""
        feature_names = []
        
        # Price features
        for period in [5, 10, 20]:
            feature_names.extend([
                f'position_in_range_{period}d',
                f'distance_from_high_{period}d',
                f'distance_from_low_{period}d'
            ])
        feature_names.extend([
            'price_gap', 'intraday_range', 'body_size', 'upper_shadow', 'lower_shadow'
        ])
        
        # Technical features
        for period in [5, 10, 20, 50]:
            feature_names.extend([f'price_vs_ma_{period}', f'ma_slope_{period}'])
        feature_names.extend([
            'rsi', 'macd_line', 'macd_signal', 'macd_histogram',
            'bb_position', 'bb_width', 'stoch_k', 'stoch_d', 'williams_r'
        ])
        
        # Volume features
        feature_names.extend([
            'volume_ratio_5d', 'volume_ratio_20d', 'volume_trend', 'obv_change', 'vpt_change'
        ])
        
        # Volatility features
        feature_names.extend([
            'volatility_5d', 'volatility_20d', 'atr_normalized', 'volatility_ratio'
        ])
        
        # Momentum features
        feature_names.extend([
            'roc_1d', 'roc_5d', 'roc_10d', 'momentum_10d', 'price_acceleration'
        ])
        
        # Pattern features
        feature_names.extend([
            'is_doji', 'is_hammer', 'is_engulfing', 'gap_up', 'gap_down'
        ])
        
        # Market structure features
        feature_names.extend([
            'resistance_distance', 'support_distance', 'trend_strength', 'trend_consistency'
        ])
        
        # Time features
        feature_names.extend([
            'hour_normalized', 'day_of_week', 'month', 'days_since_high', 'days_since_low'
        ])
        
        return feature_names
