"""
VUTAX 2.0 ML Service
Main FastAPI application for machine learning models and predictions
"""

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import uvicorn
from contextlib import asynccontextmanager
import asyncio
from datetime import datetime
import os
from typing import List, Dict, Any

from models.analytical_model import AnalyticalModel
from models.chatbot_model import ChatbotModel
from services.data_service import DataService
from services.prediction_service import PredictionService
from services.sentiment_service import SentimentService
from utils.logger import setup_logger
from schemas.requests import (
    StockAnalysisRequest,
    ChatRequest,
    PredictionRequest,
    RecommendationRequest
)
from schemas.responses import (
    StockAnalysisResponse,
    ChatResponse,
    PredictionResponse,
    RecommendationResponse,
    HealthResponse
)

# Initialize logger
logger = setup_logger(__name__)

# Global model instances
analytical_model: AnalyticalModel = None
chatbot_model: ChatbotModel = None
data_service: DataService = None
prediction_service: PredictionService = None
sentiment_service: SentimentService = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup and shutdown events"""
    global analytical_model, chatbot_model, data_service, prediction_service, sentiment_service
    
    logger.info("🚀 Starting VUTAX ML Service...")
    
    try:
        # Initialize services
        data_service = DataService()
        sentiment_service = SentimentService()
        
        # Initialize models
        logger.info("Loading analytical model...")
        analytical_model = AnalyticalModel()
        await analytical_model.initialize()
        
        logger.info("Loading chatbot model...")
        chatbot_model = ChatbotModel()
        await chatbot_model.initialize()
        
        # Initialize prediction service
        prediction_service = PredictionService(analytical_model, data_service)
        
        logger.info("✅ All models and services initialized successfully")
        
        # Start background tasks
        asyncio.create_task(background_model_updates())
        
    except Exception as e:
        logger.error(f"❌ Failed to initialize ML service: {e}")
        raise
    
    yield
    
    logger.info("🛑 Shutting down VUTAX ML Service...")

# Create FastAPI app
app = FastAPI(
    title="VUTAX 2.0 ML Service",
    description="Machine Learning API for stock analysis and predictions",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        models_loaded={
            "analytical": analytical_model is not None and analytical_model.is_ready(),
            "chatbot": chatbot_model is not None and chatbot_model.is_ready()
        },
        services_ready={
            "data_service": data_service is not None,
            "prediction_service": prediction_service is not None,
            "sentiment_service": sentiment_service is not None
        }
    )

@app.post("/analyze", response_model=StockAnalysisResponse)
async def analyze_stock(request: StockAnalysisRequest):
    """
    Analyze a stock using the analytical model
    Returns technical indicators, risk assessment, and recommendations
    """
    try:
        if not analytical_model or not analytical_model.is_ready():
            raise HTTPException(status_code=503, detail="Analytical model not ready")
        
        logger.info(f"Analyzing stock: {request.symbol}")
        
        # Get stock data
        stock_data = await data_service.get_stock_data(request.symbol, request.timeframe)
        
        # Perform analysis
        analysis = await analytical_model.analyze_stock(
            symbol=request.symbol,
            data=stock_data,
            risk_tolerance=request.risk_tolerance
        )
        
        # Get sentiment if requested
        sentiment = None
        if request.include_sentiment:
            sentiment = await sentiment_service.get_sentiment(request.symbol)
        
        return StockAnalysisResponse(
            symbol=request.symbol,
            analysis=analysis,
            sentiment=sentiment,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error analyzing stock {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: RecommendationRequest):
    """
    Get stock recommendations based on risk tier and market conditions
    """
    try:
        if not analytical_model or not analytical_model.is_ready():
            raise HTTPException(status_code=503, detail="Analytical model not ready")
        
        logger.info(f"Getting recommendations for risk tier: {request.risk_tier}")
        
        recommendations = await analytical_model.get_recommendations(
            risk_tier=request.risk_tier,
            max_recommendations=request.max_recommendations,
            exclude_symbols=request.exclude_symbols
        )
        
        return RecommendationResponse(
            recommendations=recommendations,
            risk_tier=request.risk_tier,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error getting recommendations: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/predict", response_model=PredictionResponse)
async def predict_price(request: PredictionRequest):
    """
    Generate price predictions for a stock
    """
    try:
        if not prediction_service:
            raise HTTPException(status_code=503, detail="Prediction service not ready")
        
        logger.info(f"Predicting price for {request.symbol}")
        
        prediction = await prediction_service.predict_price(
            symbol=request.symbol,
            timeframe=request.timeframe,
            confidence_interval=request.confidence_interval
        )
        
        return PredictionResponse(
            symbol=request.symbol,
            prediction=prediction,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error predicting price for {request.symbol}: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/chat", response_model=ChatResponse)
async def chat_with_bot(request: ChatRequest):
    """
    Chat with the AI assistant about stocks and portfolio
    """
    try:
        if not chatbot_model or not chatbot_model.is_ready():
            raise HTTPException(status_code=503, detail="Chatbot model not ready")
        
        logger.info(f"Processing chat request: {request.message[:50]}...")
        
        response = await chatbot_model.generate_response(
            message=request.message,
            context=request.context,
            portfolio_data=request.portfolio_data
        )
        
        return ChatResponse(
            response=response,
            timestamp=datetime.utcnow()
        )
        
    except Exception as e:
        logger.error(f"Error processing chat request: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/retrain")
async def retrain_models(background_tasks: BackgroundTasks):
    """
    Trigger model retraining (background task)
    """
    try:
        background_tasks.add_task(retrain_analytical_model)
        return {"message": "Model retraining started", "timestamp": datetime.utcnow()}
    except Exception as e:
        logger.error(f"Error starting model retraining: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models/status")
async def get_model_status():
    """
    Get status of all ML models
    """
    return {
        "analytical_model": {
            "loaded": analytical_model is not None,
            "ready": analytical_model.is_ready() if analytical_model else False,
            "last_trained": analytical_model.last_trained if analytical_model else None,
            "accuracy": analytical_model.get_accuracy() if analytical_model else None
        },
        "chatbot_model": {
            "loaded": chatbot_model is not None,
            "ready": chatbot_model.is_ready() if chatbot_model else False,
            "last_trained": chatbot_model.last_trained if chatbot_model else None
        },
        "timestamp": datetime.utcnow()
    }

async def background_model_updates():
    """Background task for periodic model updates"""
    while True:
        try:
            # Update models every 30 minutes
            await asyncio.sleep(1800)
            
            logger.info("Running background model updates...")
            
            if analytical_model:
                await analytical_model.update_market_data()
            
            if prediction_service:
                await prediction_service.update_predictions()
                
        except Exception as e:
            logger.error(f"Error in background model updates: {e}")

async def retrain_analytical_model():
    """Retrain the analytical model with latest data"""
    try:
        logger.info("Starting analytical model retraining...")
        
        if analytical_model:
            await analytical_model.retrain()
            logger.info("✅ Analytical model retrained successfully")
        
    except Exception as e:
        logger.error(f"❌ Error retraining analytical model: {e}")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8001)),
        reload=os.getenv("ENVIRONMENT") == "development"
    )
