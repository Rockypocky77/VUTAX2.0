"""
Risk Calculator for VUTAX 2.0
Calculates various risk metrics for stock analysis
"""

import numpy as np
import pandas as pd
from typing import Dict, List, Optional
from scipy import stats
import math

class RiskCalculator:
    """
    Calculate comprehensive risk metrics for stocks
    """
    
    def __init__(self):
        self.risk_free_rate = 0.02  # 2% annual risk-free rate (adjustable)
        self.market_return = 0.10   # 10% annual market return (adjustable)
    
    def calculate_risk_metrics(self, data: pd.DataFrame) -> Dict[str, float]:
        """
        Calculate comprehensive risk metrics for a stock
        """
        try:
            if data is None or data.empty or len(data) < 2:
                return self._default_risk_metrics()
            
            close_prices = data['close']
            returns = close_prices.pct_change().dropna()
            
            if len(returns) < 2:
                return self._default_risk_metrics()
            
            metrics = {}
            
            # Volatility metrics
            metrics.update(self._calculate_volatility_metrics(returns))
            
            # Downside risk metrics
            metrics.update(self._calculate_downside_risk_metrics(returns))
            
            # Performance metrics
            metrics.update(self._calculate_performance_metrics(returns, close_prices))
            
            # Market risk metrics
            metrics.update(self._calculate_market_risk_metrics(returns))
            
            # Value at Risk metrics
            metrics.update(self._calculate_var_metrics(returns))
            
            return metrics
            
        except Exception as e:
            print(f"Error calculating risk metrics: {e}")
            return self._default_risk_metrics()
    
    def _calculate_volatility_metrics(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate volatility-based risk metrics"""
        metrics = {}
        
        # Standard deviation (volatility)
        daily_vol = returns.std()
        annual_vol = daily_vol * np.sqrt(252)  # Annualized volatility
        metrics['volatility'] = annual_vol
        metrics['daily_volatility'] = daily_vol
        
        # Rolling volatility (30-day)
        if len(returns) >= 30:
            rolling_vol = returns.rolling(30).std().iloc[-1] * np.sqrt(252)
            metrics['rolling_volatility_30d'] = rolling_vol
        else:
            metrics['rolling_volatility_30d'] = annual_vol
        
        # Volatility of volatility
        if len(returns) >= 30:
            rolling_vols = returns.rolling(10).std()
            vol_of_vol = rolling_vols.std()
            metrics['volatility_of_volatility'] = vol_of_vol
        else:
            metrics['volatility_of_volatility'] = 0.0
        
        return metrics
    
    def _calculate_downside_risk_metrics(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate downside risk metrics"""
        metrics = {}
        
        # Downside deviation
        negative_returns = returns[returns < 0]
        if len(negative_returns) > 0:
            downside_deviation = negative_returns.std() * np.sqrt(252)
            metrics['downside_deviation'] = downside_deviation
        else:
            metrics['downside_deviation'] = 0.0
        
        # Maximum drawdown
        cumulative_returns = (1 + returns).cumprod()
        running_max = cumulative_returns.expanding().max()
        drawdowns = (cumulative_returns - running_max) / running_max
        max_drawdown = drawdowns.min()
        metrics['max_drawdown'] = abs(max_drawdown)
        
        # Average drawdown
        negative_drawdowns = drawdowns[drawdowns < 0]
        if len(negative_drawdowns) > 0:
            avg_drawdown = negative_drawdowns.mean()
            metrics['average_drawdown'] = abs(avg_drawdown)
        else:
            metrics['average_drawdown'] = 0.0
        
        # Downside frequency
        downside_frequency = len(negative_returns) / len(returns)
        metrics['downside_frequency'] = downside_frequency
        
        return metrics
    
    def _calculate_performance_metrics(self, returns: pd.Series, prices: pd.Series) -> Dict[str, float]:
        """Calculate performance-adjusted risk metrics"""
        metrics = {}
        
        # Sharpe ratio
        mean_return = returns.mean() * 252  # Annualized return
        annual_vol = returns.std() * np.sqrt(252)
        if annual_vol > 0:
            sharpe_ratio = (mean_return - self.risk_free_rate) / annual_vol
            metrics['sharpe_ratio'] = sharpe_ratio
        else:
            metrics['sharpe_ratio'] = 0.0
        
        # Sortino ratio
        negative_returns = returns[returns < 0]
        if len(negative_returns) > 0:
            downside_std = negative_returns.std() * np.sqrt(252)
            if downside_std > 0:
                sortino_ratio = (mean_return - self.risk_free_rate) / downside_std
                metrics['sortino_ratio'] = sortino_ratio
            else:
                metrics['sortino_ratio'] = 0.0
        else:
            metrics['sortino_ratio'] = float('inf') if mean_return > self.risk_free_rate else 0.0
        
        # Calmar ratio
        max_dd = metrics.get('max_drawdown', 0.0)
        if max_dd > 0:
            calmar_ratio = mean_return / max_dd
            metrics['calmar_ratio'] = calmar_ratio
        else:
            metrics['calmar_ratio'] = float('inf') if mean_return > 0 else 0.0
        
        # Information ratio (assuming market return as benchmark)
        excess_returns = returns - (self.market_return / 252)  # Daily market return
        tracking_error = excess_returns.std() * np.sqrt(252)
        if tracking_error > 0:
            information_ratio = (excess_returns.mean() * 252) / tracking_error
            metrics['information_ratio'] = information_ratio
        else:
            metrics['information_ratio'] = 0.0
        
        return metrics
    
    def _calculate_market_risk_metrics(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate market-related risk metrics"""
        metrics = {}
        
        # Beta (simplified - using correlation with market proxy)
        # In a real implementation, you would correlate with actual market returns
        # For now, we'll estimate based on volatility relative to typical market volatility
        annual_vol = returns.std() * np.sqrt(252)
        typical_market_vol = 0.16  # Typical market volatility ~16%
        estimated_beta = annual_vol / typical_market_vol
        metrics['beta'] = min(max(estimated_beta, 0.1), 3.0)  # Cap between 0.1 and 3.0
        
        # Systematic risk (portion of risk due to market factors)
        # Simplified calculation
        correlation_with_market = 0.7  # Assumed correlation (would be calculated with real market data)
        systematic_risk = (correlation_with_market ** 2) * (annual_vol ** 2)
        metrics['systematic_risk'] = systematic_risk
        
        # Idiosyncratic risk (stock-specific risk)
        idiosyncratic_risk = (annual_vol ** 2) - systematic_risk
        metrics['idiosyncratic_risk'] = max(idiosyncratic_risk, 0.0)
        
        return metrics
    
    def _calculate_var_metrics(self, returns: pd.Series) -> Dict[str, float]:
        """Calculate Value at Risk metrics"""
        metrics = {}
        
        confidence_levels = [0.95, 0.99]
        
        for confidence in confidence_levels:
            # Historical VaR
            var_percentile = (1 - confidence) * 100
            historical_var = np.percentile(returns, var_percentile)
            metrics[f'var_{int(confidence*100)}'] = abs(historical_var)
            
            # Parametric VaR (assuming normal distribution)
            z_score = stats.norm.ppf(1 - confidence)
            parametric_var = returns.mean() + z_score * returns.std()
            metrics[f'parametric_var_{int(confidence*100)}'] = abs(parametric_var)
            
            # Expected Shortfall (Conditional VaR)
            tail_returns = returns[returns <= historical_var]
            if len(tail_returns) > 0:
                expected_shortfall = tail_returns.mean()
                metrics[f'expected_shortfall_{int(confidence*100)}'] = abs(expected_shortfall)
            else:
                metrics[f'expected_shortfall_{int(confidence*100)}'] = abs(historical_var)
        
        return metrics
    
    def _default_risk_metrics(self) -> Dict[str, float]:
        """Return default risk metrics when calculation fails"""
        return {
            'volatility': 0.2,
            'daily_volatility': 0.2 / np.sqrt(252),
            'rolling_volatility_30d': 0.2,
            'volatility_of_volatility': 0.0,
            'downside_deviation': 0.15,
            'max_drawdown': 0.1,
            'average_drawdown': 0.05,
            'downside_frequency': 0.45,
            'sharpe_ratio': 0.0,
            'sortino_ratio': 0.0,
            'calmar_ratio': 0.0,
            'information_ratio': 0.0,
            'beta': 1.0,
            'systematic_risk': 0.1,
            'idiosyncratic_risk': 0.1,
            'var_95': 0.02,
            'var_99': 0.03,
            'parametric_var_95': 0.02,
            'parametric_var_99': 0.03,
            'expected_shortfall_95': 0.025,
            'expected_shortfall_99': 0.035
        }
    
    def categorize_risk_level(self, metrics: Dict[str, float]) -> str:
        """
        Categorize overall risk level based on metrics
        """
        try:
            volatility = metrics.get('volatility', 0.2)
            max_drawdown = metrics.get('max_drawdown', 0.1)
            sharpe_ratio = metrics.get('sharpe_ratio', 0.0)
            beta = metrics.get('beta', 1.0)
            
            # Risk scoring
            risk_score = 0
            
            # Volatility component
            if volatility > 0.3:
                risk_score += 3
            elif volatility > 0.2:
                risk_score += 2
            else:
                risk_score += 1
            
            # Drawdown component
            if max_drawdown > 0.2:
                risk_score += 3
            elif max_drawdown > 0.1:
                risk_score += 2
            else:
                risk_score += 1
            
            # Beta component
            if beta > 1.5:
                risk_score += 2
            elif beta > 1.2:
                risk_score += 1
            
            # Sharpe ratio component (negative scoring - higher is better)
            if sharpe_ratio < 0:
                risk_score += 2
            elif sharpe_ratio < 0.5:
                risk_score += 1
            
            # Categorize based on total score
            if risk_score >= 7:
                return 'high-risk'
            elif risk_score >= 4:
                return 'regular'
            else:
                return 'conservative'
                
        except Exception as e:
            print(f"Error categorizing risk level: {e}")
            return 'regular'
    
    def calculate_position_size(self, 
                              portfolio_value: float, 
                              risk_metrics: Dict[str, float], 
                              risk_tolerance: str = 'regular') -> Dict[str, float]:
        """
        Calculate appropriate position size based on risk metrics and tolerance
        """
        try:
            # Risk tolerance multipliers
            risk_multipliers = {
                'conservative': 0.5,
                'regular': 1.0,
                'high-risk': 2.0
            }
            
            base_multiplier = risk_multipliers.get(risk_tolerance, 1.0)
            
            # Kelly Criterion approximation
            sharpe_ratio = risk_metrics.get('sharpe_ratio', 0.0)
            volatility = risk_metrics.get('volatility', 0.2)
            
            if volatility > 0:
                # Simplified Kelly fraction
                kelly_fraction = max(0, sharpe_ratio / (volatility ** 2))
                kelly_fraction = min(kelly_fraction, 0.25)  # Cap at 25%
            else:
                kelly_fraction = 0.05  # Default 5%
            
            # Risk parity approach
            var_95 = risk_metrics.get('var_95', 0.02)
            target_risk = 0.01 * base_multiplier  # 1% daily risk for regular tolerance
            
            if var_95 > 0:
                risk_parity_fraction = target_risk / var_95
                risk_parity_fraction = min(risk_parity_fraction, 0.3)  # Cap at 30%
            else:
                risk_parity_fraction = 0.05
            
            # Volatility-based sizing
            target_volatility = 0.15 * base_multiplier  # Target portfolio volatility
            vol_based_fraction = target_volatility / max(volatility, 0.05)
            vol_based_fraction = min(vol_based_fraction, 0.25)  # Cap at 25%
            
            # Average the approaches
            recommended_fraction = (kelly_fraction + risk_parity_fraction + vol_based_fraction) / 3
            recommended_fraction = max(0.01, min(recommended_fraction, 0.2))  # Between 1% and 20%
            
            # Calculate position sizes
            recommended_value = portfolio_value * recommended_fraction
            max_position_value = portfolio_value * 0.1  # Never more than 10% in single position
            
            return {
                'recommended_fraction': recommended_fraction,
                'recommended_value': min(recommended_value, max_position_value),
                'max_position_value': max_position_value,
                'kelly_fraction': kelly_fraction,
                'risk_parity_fraction': risk_parity_fraction,
                'volatility_based_fraction': vol_based_fraction
            }
            
        except Exception as e:
            print(f"Error calculating position size: {e}")
            return {
                'recommended_fraction': 0.05,
                'recommended_value': portfolio_value * 0.05,
                'max_position_value': portfolio_value * 0.1,
                'kelly_fraction': 0.05,
                'risk_parity_fraction': 0.05,
                'volatility_based_fraction': 0.05
            }
