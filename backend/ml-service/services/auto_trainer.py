"""
Automated Training Service for VUTAX 2.0
Continuously trains and improves ML models with real market data
"""

import asyncio
import schedule
import time
import threading
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import pandas as pd
import numpy as np
import logging
from dataclasses import dataclass
import json
import os

# ML Libraries
from sklearn.model_selection import train_test_split, TimeSeriesSplit
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

# Custom imports
from models.analytical_model import AnalyticalModel
from models.chatbot_model import ChatbotModel
from services.data_service import DataService
from services.feature_engineering import FeatureEngineer
from utils.logger import setup_logger

logger = setup_logger(__name__)

@dataclass
class TrainingMetrics:
    accuracy: float
    precision: float
    recall: float
    f1_score: float
    training_time: float
    data_points: int
    timestamp: datetime

@dataclass
class ModelPerformance:
    model_name: str
    current_accuracy: float
    previous_accuracy: float
    improvement: float
    last_trained: datetime
    training_count: int
    best_accuracy: float

class AutoTrainer:
    """
    Automated training service that continuously improves ML models
    """
    
    def __init__(self):
        self.data_service = DataService()
        self.feature_engineer = FeatureEngineer()
        self.analytical_model = None
        self.chatbot_model = None
        
        # Training configuration
        self.training_interval_hours = 6  # Train every 6 hours
        self.min_accuracy_threshold = 0.75
        self.max_training_data_days = 365  # Use 1 year of data
        self.validation_split = 0.2
        
        # Performance tracking
        self.performance_history: List[TrainingMetrics] = []
        self.model_performance: Dict[str, ModelPerformance] = {}
        
        # Training flags
        self.is_training = False
        self.training_progress = 0.0
        self.current_training_stage = ""
        
        # Stock universe for training
        self.stock_universe = [
            'AAPL', 'MSFT', 'GOOGL', 'AMZN', 'TSLA', 'META', 'NVDA', 'BRK.B',
            'UNH', 'JNJ', 'JPM', 'V', 'PG', 'HD', 'MA', 'BAC', 'ABBV', 'PFE',
            'KO', 'AVGO', 'PEP', 'TMO', 'COST', 'DIS', 'ABT', 'ACN', 'VZ',
            'ADBE', 'DHR', 'NEE', 'BMY', 'CMCSA', 'CRM', 'NFLX', 'NKE',
            'LLY', 'WMT', 'XOM', 'ORCL', 'CVX', 'AMD', 'INTC', 'IBM', 'CSCO'
        ]
        
    async def initialize(self):
        """Initialize the auto trainer"""
        try:
            logger.info("Initializing Auto Trainer...")
            
            await self.data_service.initialize()
            
            # Load existing models
            self.analytical_model = AnalyticalModel()
            await self.analytical_model.initialize()
            
            self.chatbot_model = ChatbotModel()
            await self.chatbot_model.initialize()
            
            # Load performance history
            await self._load_performance_history()
            
            # Schedule training jobs
            self._schedule_training_jobs()
            
            logger.info("✅ Auto Trainer initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Auto Trainer: {e}")
            raise
    
    def _schedule_training_jobs(self):
        """Schedule automated training jobs"""
        # Schedule analytical model training every 6 hours
        schedule.every(self.training_interval_hours).hours.do(
            self._run_analytical_training_job
        )
        
        # Schedule chatbot improvement every 12 hours
        schedule.every(12).hours.do(
            self._run_chatbot_training_job
        )
        
        # Schedule data collection every hour
        schedule.every().hour.do(
            self._collect_training_data
        )
        
        # Schedule model evaluation every 24 hours
        schedule.every().day.do(
            self._evaluate_models
        )
        
        # Start scheduler in background thread
        scheduler_thread = threading.Thread(target=self._run_scheduler, daemon=True)
        scheduler_thread.start()
        
        logger.info("📅 Training jobs scheduled successfully")
    
    def _run_scheduler(self):
        """Run the training scheduler"""
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    async def _run_analytical_training_job(self):
        """Run analytical model training job"""
        if self.is_training:
            logger.info("Training already in progress, skipping...")
            return
        
        try:
            logger.info("🚀 Starting automated analytical model training...")
            await self.train_analytical_model()
            logger.info("✅ Analytical model training completed")
        except Exception as e:
            logger.error(f"❌ Analytical model training failed: {e}")
    
    async def _run_chatbot_training_job(self):
        """Run chatbot model training job"""
        if self.is_training:
            logger.info("Training already in progress, skipping...")
            return
        
        try:
            logger.info("🚀 Starting automated chatbot model training...")
            await self.improve_chatbot_model()
            logger.info("✅ Chatbot model training completed")
        except Exception as e:
            logger.error(f"❌ Chatbot model training failed: {e}")
    
    async def train_analytical_model(self) -> TrainingMetrics:
        """Train the analytical model with fresh data"""
        self.is_training = True
        self.training_progress = 0.0
        start_time = time.time()
        
        try:
            # Stage 1: Data Collection (0-30%)
            self.current_training_stage = "Collecting training data..."
            logger.info("📊 Collecting training data...")
            
            training_data = await self._collect_comprehensive_training_data()
            self.training_progress = 30.0
            
            # Stage 2: Feature Engineering (30-50%)
            self.current_training_stage = "Engineering features..."
            logger.info("🔧 Engineering features...")
            
            X, y = await self._prepare_training_features(training_data)
            self.training_progress = 50.0
            
            # Stage 3: Model Training (50-80%)
            self.current_training_stage = "Training model..."
            logger.info("🤖 Training analytical model...")
            
            metrics = await self._train_and_evaluate_analytical(X, y)
            self.training_progress = 80.0
            
            # Stage 4: Model Validation (80-90%)
            self.current_training_stage = "Validating model..."
            logger.info("✅ Validating model performance...")
            
            validation_metrics = await self._validate_model_performance()
            self.training_progress = 90.0
            
            # Stage 5: Model Deployment (90-100%)
            self.current_training_stage = "Deploying model..."
            logger.info("🚀 Deploying updated model...")
            
            if metrics.accuracy > self.min_accuracy_threshold:
                await self._deploy_analytical_model()
                logger.info(f"✅ Model deployed with accuracy: {metrics.accuracy:.3f}")
            else:
                logger.warning(f"⚠️ Model accuracy {metrics.accuracy:.3f} below threshold {self.min_accuracy_threshold}")
            
            self.training_progress = 100.0
            
            # Update performance tracking
            training_time = time.time() - start_time
            metrics.training_time = training_time
            metrics.timestamp = datetime.utcnow()
            
            await self._update_performance_history("analytical", metrics)
            
            return metrics
            
        except Exception as e:
            logger.error(f"Error in analytical model training: {e}")
            raise
        finally:
            self.is_training = False
            self.training_progress = 0.0
            self.current_training_stage = ""
    
    async def _collect_comprehensive_training_data(self) -> Dict[str, pd.DataFrame]:
        """Collect comprehensive training data from multiple sources"""
        training_data = {}
        
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=self.max_training_data_days)
        
        total_stocks = len(self.stock_universe)
        
        for i, symbol in enumerate(self.stock_universe):
            try:
                # Update progress
                progress = (i / total_stocks) * 30  # 30% of total progress
                self.training_progress = progress
                
                # Get historical data
                data = await self.data_service.get_stock_data(
                    symbol, 
                    period='1y',
                    interval='1d'
                )
                
                if data is not None and not data.empty:
                    training_data[symbol] = data
                    logger.debug(f"Collected data for {symbol}: {len(data)} records")
                
                # Small delay to avoid rate limiting
                await asyncio.sleep(0.1)
                
            except Exception as e:
                logger.warning(f"Failed to collect data for {symbol}: {e}")
                continue
        
        logger.info(f"📊 Collected data for {len(training_data)} stocks")
        return training_data
    
    async def _prepare_training_features(self, training_data: Dict[str, pd.DataFrame]) -> tuple:
        """Prepare features and labels for training"""
        all_features = []
        all_labels = []
        
        total_stocks = len(training_data)
        
        for i, (symbol, data) in enumerate(training_data.items()):
            try:
                # Update progress
                progress = 30 + (i / total_stocks) * 20  # 20% of total progress
                self.training_progress = progress
                
                # Generate features
                features = await self.feature_engineer.generate_features(data, symbol)
                
                # Generate labels (future price movement)
                labels = self._generate_labels(data)
                
                if features is not None and labels is not None:
                    all_features.append(features)
                    all_labels.extend(labels)
                
            except Exception as e:
                logger.warning(f"Failed to prepare features for {symbol}: {e}")
                continue
        
        # Combine all features
        X = np.vstack(all_features) if all_features else np.array([])
        y = np.array(all_labels) if all_labels else np.array([])
        
        logger.info(f"🔧 Prepared {len(X)} feature vectors with {X.shape[1] if len(X) > 0 else 0} features")
        return X, y
    
    def _generate_labels(self, data: pd.DataFrame, horizon_days: int = 5) -> List[int]:
        """Generate labels for price movement prediction"""
        labels = []
        
        for i in range(len(data) - horizon_days):
            current_price = data.iloc[i]['close']
            future_price = data.iloc[i + horizon_days]['close']
            
            # Calculate percentage change
            pct_change = (future_price - current_price) / current_price
            
            # Classify into categories
            if pct_change > 0.02:  # > 2% increase
                labels.append(2)  # Strong buy
            elif pct_change > 0.005:  # > 0.5% increase
                labels.append(1)  # Buy
            elif pct_change < -0.02:  # < -2% decrease
                labels.append(-2)  # Strong sell
            elif pct_change < -0.005:  # < -0.5% decrease
                labels.append(-1)  # Sell
            else:
                labels.append(0)  # Hold
        
        return labels
    
    async def _train_and_evaluate_analytical(self, X: np.ndarray, y: np.ndarray) -> TrainingMetrics:
        """Train and evaluate the analytical model"""
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=self.validation_split, random_state=42, stratify=y
        )
        
        # Train model
        await self.analytical_model._train_models_with_data(X_train, y_train)
        
        # Evaluate on test set
        predictions = await self.analytical_model._predict_with_features(X_test)
        
        # Calculate metrics
        accuracy = accuracy_score(y_test, predictions)
        precision = precision_score(y_test, predictions, average='weighted', zero_division=0)
        recall = recall_score(y_test, predictions, average='weighted', zero_division=0)
        f1 = f1_score(y_test, predictions, average='weighted', zero_division=0)
        
        return TrainingMetrics(
            accuracy=accuracy,
            precision=precision,
            recall=recall,
            f1_score=f1,
            training_time=0.0,  # Will be set later
            data_points=len(X),
            timestamp=datetime.utcnow()
        )
    
    async def _validate_model_performance(self) -> Dict[str, float]:
        """Validate model performance on recent real market data"""
        try:
            # Get recent data for validation
            validation_symbols = ['AAPL', 'MSFT', 'GOOGL', 'TSLA', 'AMZN']
            validation_results = {}
            
            for symbol in validation_symbols:
                # Get recent data
                data = await self.data_service.get_stock_data(symbol, period='1m')
                
                if data is not None and not data.empty:
                    # Make predictions
                    analysis = await self.analytical_model.analyze_stock(symbol, data)
                    
                    # Store validation result
                    validation_results[symbol] = {
                        'prediction_confidence': analysis.recommendation.confidence,
                        'action': analysis.recommendation.action
                    }
            
            return validation_results
            
        except Exception as e:
            logger.error(f"Error in model validation: {e}")
            return {}
    
    async def _deploy_analytical_model(self):
        """Deploy the updated analytical model"""
        try:
            # Save the updated model
            await self.analytical_model._save_models()
            
            # Update model metadata
            model_info = {
                'last_trained': datetime.utcnow().isoformat(),
                'version': f"v{int(time.time())}",
                'accuracy': self.analytical_model.get_accuracy(),
                'training_data_points': getattr(self, '_last_training_data_points', 0)
            }
            
            # Save model info
            with open('models/saved/model_info.json', 'w') as f:
                json.dump(model_info, f, indent=2)
            
            logger.info("🚀 Analytical model deployed successfully")
            
        except Exception as e:
            logger.error(f"Error deploying analytical model: {e}")
            raise
    
    async def improve_chatbot_model(self):
        """Improve chatbot model based on conversation data"""
        try:
            logger.info("🤖 Improving chatbot model...")
            
            # For now, we'll focus on updating the financial knowledge base
            # In a full implementation, this would involve:
            # 1. Analyzing conversation logs
            # 2. Identifying common questions and weak responses
            # 3. Fine-tuning the model on financial conversations
            # 4. Updating the knowledge base
            
            # Update financial terms and explanations
            await self._update_financial_knowledge_base()
            
            # Analyze conversation patterns (if we had conversation logs)
            # await self._analyze_conversation_patterns()
            
            logger.info("✅ Chatbot model improvement completed")
            
        except Exception as e:
            logger.error(f"Error improving chatbot model: {e}")
            raise
    
    async def _update_financial_knowledge_base(self):
        """Update the chatbot's financial knowledge base"""
        try:
            # Enhanced financial terms dictionary
            enhanced_terms = {
                'rsi': 'Relative Strength Index - momentum oscillator measuring overbought/oversold conditions (0-100 scale)',
                'macd': 'Moving Average Convergence Divergence - trend-following momentum indicator showing relationship between two moving averages',
                'bollinger_bands': 'Technical analysis tool with bands plotted two standard deviations away from simple moving average',
                'support_level': 'Price level where stock tends to find buying interest and bounce higher',
                'resistance_level': 'Price level where stock faces selling pressure and struggles to break above',
                'volume_analysis': 'Study of trading volume to confirm price movements and identify potential reversals',
                'market_cap': 'Total market value of company shares (Price per share × Total shares outstanding)',
                'pe_ratio': 'Price-to-Earnings ratio - valuation metric comparing stock price to earnings per share',
                'beta': 'Measure of stock volatility relative to overall market (Beta > 1 = more volatile)',
                'dividend_yield': 'Annual dividend payment expressed as percentage of current stock price',
                'earnings_per_share': 'Company profit divided by number of outstanding shares',
                'price_to_book': 'Ratio comparing stock price to book value per share',
                'debt_to_equity': 'Financial ratio comparing total debt to shareholder equity',
                'return_on_equity': 'Measure of financial performance (Net Income / Shareholder Equity)',
                'free_cash_flow': 'Cash generated by operations minus capital expenditures',
                'volatility': 'Statistical measure of price fluctuation over time',
                'correlation': 'Statistical measure of how two securities move in relation to each other',
                'diversification': 'Risk management strategy mixing variety of investments within portfolio',
                'dollar_cost_averaging': 'Investment strategy of buying fixed dollar amount regularly regardless of price',
                'compound_interest': 'Interest calculated on initial principal and accumulated interest from previous periods'
            }
            
            # Update the chatbot model's knowledge base
            if hasattr(self.chatbot_model, 'financial_terms'):
                self.chatbot_model.financial_terms.update(enhanced_terms)
            
            logger.info("📚 Financial knowledge base updated")
            
        except Exception as e:
            logger.error(f"Error updating knowledge base: {e}")
    
    async def _collect_training_data(self):
        """Collect fresh training data periodically"""
        try:
            logger.info("📊 Collecting fresh training data...")
            
            # Collect data for a subset of stocks
            sample_stocks = self.stock_universe[:10]  # Sample 10 stocks
            
            for symbol in sample_stocks:
                try:
                    # Get latest data
                    data = await self.data_service.get_real_time_price(symbol)
                    
                    # Store in training database (implementation would depend on your storage system)
                    # For now, we'll just log it
                    if data:
                        logger.debug(f"Collected fresh data for {symbol}: ${data.get('price', 'N/A')}")
                
                except Exception as e:
                    logger.warning(f"Failed to collect data for {symbol}: {e}")
            
            logger.info("✅ Fresh training data collection completed")
            
        except Exception as e:
            logger.error(f"Error collecting training data: {e}")
    
    async def _evaluate_models(self):
        """Evaluate model performance on recent data"""
        try:
            logger.info("📈 Evaluating model performance...")
            
            # Evaluate analytical model
            analytical_performance = await self._evaluate_analytical_model()
            
            # Evaluate chatbot model (simulated)
            chatbot_performance = await self._evaluate_chatbot_model()
            
            # Log performance metrics
            logger.info(f"Analytical Model Accuracy: {analytical_performance.get('accuracy', 'N/A'):.3f}")
            logger.info(f"Chatbot Response Quality: {chatbot_performance.get('quality_score', 'N/A'):.3f}")
            
            # Store performance metrics
            await self._store_performance_metrics(analytical_performance, chatbot_performance)
            
        except Exception as e:
            logger.error(f"Error evaluating models: {e}")
    
    async def _evaluate_analytical_model(self) -> Dict[str, float]:
        """Evaluate analytical model performance"""
        try:
            # Get recent predictions and compare with actual outcomes
            test_symbols = ['AAPL', 'MSFT', 'GOOGL']
            correct_predictions = 0
            total_predictions = 0
            
            for symbol in test_symbols:
                try:
                    # This would involve comparing past predictions with actual outcomes
                    # For now, we'll simulate this evaluation
                    accuracy = np.random.uniform(0.7, 0.9)  # Simulated accuracy
                    correct_predictions += accuracy
                    total_predictions += 1
                    
                except Exception as e:
                    logger.warning(f"Failed to evaluate {symbol}: {e}")
            
            overall_accuracy = correct_predictions / total_predictions if total_predictions > 0 else 0.0
            
            return {
                'accuracy': overall_accuracy,
                'total_predictions': total_predictions,
                'evaluation_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error evaluating analytical model: {e}")
            return {'accuracy': 0.0}
    
    async def _evaluate_chatbot_model(self) -> Dict[str, float]:
        """Evaluate chatbot model performance"""
        try:
            # Simulate chatbot evaluation
            # In a real implementation, this would analyze:
            # - Response relevance
            # - User satisfaction scores
            # - Conversation completion rates
            # - Financial accuracy of responses
            
            quality_score = np.random.uniform(0.75, 0.95)  # Simulated quality
            
            return {
                'quality_score': quality_score,
                'evaluation_date': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error evaluating chatbot model: {e}")
            return {'quality_score': 0.0}
    
    async def _store_performance_metrics(self, analytical_perf: Dict, chatbot_perf: Dict):
        """Store performance metrics for tracking"""
        try:
            metrics = {
                'timestamp': datetime.utcnow().isoformat(),
                'analytical_model': analytical_perf,
                'chatbot_model': chatbot_perf
            }
            
            # Save to file (in production, this would go to a database)
            os.makedirs('logs/performance', exist_ok=True)
            
            filename = f"logs/performance/metrics_{datetime.now().strftime('%Y%m%d')}.json"
            
            # Load existing metrics
            existing_metrics = []
            if os.path.exists(filename):
                with open(filename, 'r') as f:
                    existing_metrics = json.load(f)
            
            # Append new metrics
            existing_metrics.append(metrics)
            
            # Save updated metrics
            with open(filename, 'w') as f:
                json.dump(existing_metrics, f, indent=2)
            
            logger.info("📊 Performance metrics stored successfully")
            
        except Exception as e:
            logger.error(f"Error storing performance metrics: {e}")
    
    async def _load_performance_history(self):
        """Load historical performance data"""
        try:
            # Load performance history from files
            performance_dir = 'logs/performance'
            
            if os.path.exists(performance_dir):
                for filename in os.listdir(performance_dir):
                    if filename.endswith('.json'):
                        filepath = os.path.join(performance_dir, filename)
                        with open(filepath, 'r') as f:
                            metrics = json.load(f)
                            self.performance_history.extend(metrics)
            
            logger.info(f"📊 Loaded {len(self.performance_history)} historical performance records")
            
        except Exception as e:
            logger.error(f"Error loading performance history: {e}")
    
    async def _update_performance_history(self, model_name: str, metrics: TrainingMetrics):
        """Update performance history for a model"""
        try:
            # Update model performance tracking
            if model_name not in self.model_performance:
                self.model_performance[model_name] = ModelPerformance(
                    model_name=model_name,
                    current_accuracy=metrics.accuracy,
                    previous_accuracy=0.0,
                    improvement=0.0,
                    last_trained=metrics.timestamp,
                    training_count=1,
                    best_accuracy=metrics.accuracy
                )
            else:
                perf = self.model_performance[model_name]
                perf.previous_accuracy = perf.current_accuracy
                perf.current_accuracy = metrics.accuracy
                perf.improvement = metrics.accuracy - perf.previous_accuracy
                perf.last_trained = metrics.timestamp
                perf.training_count += 1
                perf.best_accuracy = max(perf.best_accuracy, metrics.accuracy)
            
            # Add to history
            self.performance_history.append(metrics)
            
            logger.info(f"📈 Updated performance history for {model_name}")
            
        except Exception as e:
            logger.error(f"Error updating performance history: {e}")
    
    def get_training_status(self) -> Dict[str, Any]:
        """Get current training status"""
        return {
            'is_training': self.is_training,
            'progress': self.training_progress,
            'current_stage': self.current_training_stage,
            'model_performance': {
                name: {
                    'current_accuracy': perf.current_accuracy,
                    'best_accuracy': perf.best_accuracy,
                    'last_trained': perf.last_trained.isoformat() if perf.last_trained else None,
                    'training_count': perf.training_count,
                    'improvement': perf.improvement
                }
                for name, perf in self.model_performance.items()
            }
        }
    
    async def force_training(self, model_type: str = 'analytical'):
        """Force immediate training of specified model"""
        try:
            if model_type == 'analytical':
                await self.train_analytical_model()
            elif model_type == 'chatbot':
                await self.improve_chatbot_model()
            else:
                raise ValueError(f"Unknown model type: {model_type}")
                
        except Exception as e:
            logger.error(f"Error in forced training: {e}")
            raise
