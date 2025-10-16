"""
Request schemas for VUTAX ML Service
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class StockAnalysisRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol to analyze")
    timeframe: str = Field(default="1d", description="Timeframe for analysis")
    risk_tolerance: str = Field(default="regular", description="Risk tolerance level")
    include_sentiment: bool = Field(default=True, description="Include sentiment analysis")

class RecommendationRequest(BaseModel):
    risk_tier: str = Field(default="regular", description="Risk tier for recommendations")
    max_recommendations: int = Field(default=10, description="Maximum number of recommendations")
    exclude_symbols: Optional[List[str]] = Field(default=None, description="Symbols to exclude")

class PredictionRequest(BaseModel):
    symbol: str = Field(..., description="Stock symbol for prediction")
    timeframe: str = Field(default="1d", description="Prediction timeframe")
    confidence_interval: float = Field(default=0.95, description="Confidence interval")

class ChatRequest(BaseModel):
    message: str = Field(..., description="User message")
    context: Optional[Dict[str, Any]] = Field(default=None, description="Conversation context")
    portfolio_data: Optional[Dict[str, Any]] = Field(default=None, description="User portfolio data")
