"""
Response schemas for VUTAX ML Service
"""

from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime

class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    models_loaded: Dict[str, bool]
    services_ready: Dict[str, bool]

class StockAnalysisResponse(BaseModel):
    symbol: str
    analysis: Dict[str, Any]
    sentiment: Optional[Dict[str, Any]] = None
    timestamp: datetime

class RecommendationResponse(BaseModel):
    recommendations: List[Dict[str, Any]]
    risk_tier: str
    timestamp: datetime

class PredictionResponse(BaseModel):
    symbol: str
    prediction: Dict[str, Any]
    timestamp: datetime

class ChatResponse(BaseModel):
    response: str
    timestamp: datetime
