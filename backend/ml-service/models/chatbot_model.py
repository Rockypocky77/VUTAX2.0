"""
Chatbot Model for VUTAX 2.0
Handles user interactions, portfolio interpretation, and explanations
"""

import asyncio
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
import numpy as np
import pandas as pd

# NLP Libraries
from transformers import (
    AutoTokenizer, 
    AutoModelForCausalLM, 
    pipeline,
    BitsAndBytesConfig
)
import torch
from textblob import TextBlob

from utils.logger import setup_logger
from services.data_service import DataService

logger = setup_logger(__name__)

class ChatbotModel:
    """
    AI Chatbot for user interactions and portfolio explanations
    """
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.pipeline = None
        self.data_service = None
        self.is_initialized = False
        self.last_trained = None
        
        # Model configuration
        self.model_name = "microsoft/DialoGPT-medium"  # Lightweight conversational model
        self.max_length = 512
        self.temperature = 0.7
        self.top_p = 0.9
        
        # Context management
        self.conversation_history = {}
        self.max_history_length = 10
        
        # Financial knowledge base
        self.financial_terms = self._load_financial_terms()
        self.stock_explanations = {}
        
    async def initialize(self):
        """Initialize the chatbot model"""
        try:
            logger.info("Initializing Chatbot Model...")
            
            # Initialize data service
            self.data_service = DataService()
            
            # Load model with optimizations for local inference
            await self._load_model()
            
            # Initialize conversation pipeline
            self._setup_pipeline()
            
            self.is_initialized = True
            self.last_trained = datetime.utcnow()
            
            logger.info("✅ Chatbot Model initialized successfully")
            
        except Exception as e:
            logger.error(f"❌ Failed to initialize Chatbot Model: {e}")
            raise
    
    def is_ready(self) -> bool:
        """Check if chatbot is ready for inference"""
        return (
            self.is_initialized and 
            self.model is not None and 
            self.tokenizer is not None
        )
    
    async def generate_response(
        self,
        message: str,
        context: Optional[Dict[str, Any]] = None,
        portfolio_data: Optional[Dict[str, Any]] = None,
        user_id: str = "default"
    ) -> str:
        """
        Generate conversational response to user message
        """
        try:
            logger.info(f"Processing chat message: {message[:50]}...")
            
            # Preprocess message
            processed_message = self._preprocess_message(message)
            
            # Determine intent
            intent = await self._classify_intent(processed_message)
            
            # Generate response based on intent
            if intent == "portfolio_question":
                response = await self._handle_portfolio_question(
                    processed_message, portfolio_data, context
                )
            elif intent == "stock_question":
                response = await self._handle_stock_question(
                    processed_message, context
                )
            elif intent == "recommendation_explanation":
                response = await self._handle_recommendation_explanation(
                    processed_message, context
                )
            elif intent == "general_finance":
                response = await self._handle_general_finance_question(
                    processed_message, context
                )
            else:
                response = await self._generate_conversational_response(
                    processed_message, user_id
                )
            
            # Update conversation history
            self._update_conversation_history(user_id, message, response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I apologize, but I'm having trouble processing your request right now. Please try again or rephrase your question."
    
    async def _load_model(self):
        """Load the conversational model"""
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Configure for efficient inference
            device = "cuda" if torch.cuda.is_available() else "cpu"
            
            # Load tokenizer
            self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            # Load model with optimizations
            if device == "cuda":
                # Use quantization for GPU
                quantization_config = BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_compute_dtype=torch.float16
                )
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    quantization_config=quantization_config,
                    device_map="auto"
                )
            else:
                # CPU inference
                self.model = AutoModelForCausalLM.from_pretrained(
                    self.model_name,
                    torch_dtype=torch.float32
                )
                self.model.to(device)
            
            logger.info(f"✅ Model loaded on {device}")
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            # Fallback to simpler approach
            await self._load_fallback_model()
    
    async def _load_fallback_model(self):
        """Load a simpler fallback model if main model fails"""
        try:
            logger.info("Loading fallback conversational model...")
            
            # Use a simpler pipeline approach
            self.pipeline = pipeline(
                "text-generation",
                model="gpt2",
                tokenizer="gpt2",
                max_length=256,
                device=0 if torch.cuda.is_available() else -1
            )
            
            logger.info("✅ Fallback model loaded")
            
        except Exception as e:
            logger.error(f"Error loading fallback model: {e}")
            # Use rule-based responses as final fallback
            self.pipeline = None
    
    def _setup_pipeline(self):
        """Setup conversation pipeline"""
        try:
            if self.model and self.tokenizer:
                self.pipeline = pipeline(
                    "text-generation",
                    model=self.model,
                    tokenizer=self.tokenizer,
                    max_length=self.max_length,
                    temperature=self.temperature,
                    top_p=self.top_p,
                    do_sample=True,
                    pad_token_id=self.tokenizer.eos_token_id
                )
        except Exception as e:
            logger.error(f"Error setting up pipeline: {e}")
    
    def _preprocess_message(self, message: str) -> str:
        """Preprocess user message"""
        # Clean and normalize
        message = message.strip()
        message = re.sub(r'\s+', ' ', message)
        
        # Extract stock symbols
        symbols = re.findall(r'\b[A-Z]{1,5}\b', message)
        
        # Store extracted symbols for context
        if hasattr(self, '_current_symbols'):
            self._current_symbols = symbols
        else:
            self._current_symbols = symbols
        
        return message
    
    async def _classify_intent(self, message: str) -> str:
        """Classify user intent"""
        message_lower = message.lower()
        
        # Portfolio-related keywords
        portfolio_keywords = [
            'portfolio', 'positions', 'holdings', 'my stocks', 'my investments',
            'gains', 'losses', 'performance', 'returns', 'profit'
        ]
        
        # Stock-related keywords
        stock_keywords = [
            'stock', 'share', 'ticker', 'company', 'price', 'chart',
            'analysis', 'technical', 'fundamental'
        ]
        
        # Recommendation keywords
        recommendation_keywords = [
            'recommend', 'suggestion', 'buy', 'sell', 'hold', 'advice',
            'should i', 'what do you think', 'opinion'
        ]
        
        # General finance keywords
        finance_keywords = [
            'market', 'economy', 'trading', 'investing', 'finance',
            'risk', 'volatility', 'dividend', 'earnings'
        ]
        
        # Check for patterns
        if any(keyword in message_lower for keyword in portfolio_keywords):
            return "portfolio_question"
        elif any(keyword in message_lower for keyword in stock_keywords):
            return "stock_question"
        elif any(keyword in message_lower for keyword in recommendation_keywords):
            return "recommendation_explanation"
        elif any(keyword in message_lower for keyword in finance_keywords):
            return "general_finance"
        else:
            return "general_conversation"
    
    async def _handle_portfolio_question(
        self,
        message: str,
        portfolio_data: Optional[Dict[str, Any]],
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Handle portfolio-related questions"""
        try:
            if not portfolio_data:
                return "I don't have access to your portfolio data right now. Please make sure you're logged in and have positions in your portfolio."
            
            message_lower = message.lower()
            
            # Performance questions
            if any(word in message_lower for word in ['performance', 'how am i doing', 'returns']):
                return self._generate_portfolio_performance_response(portfolio_data)
            
            # Position questions
            elif any(word in message_lower for word in ['positions', 'holdings', 'what do i own']):
                return self._generate_portfolio_positions_response(portfolio_data)
            
            # Risk questions
            elif any(word in message_lower for word in ['risk', 'risky', 'safe']):
                return self._generate_portfolio_risk_response(portfolio_data)
            
            # Gains/losses
            elif any(word in message_lower for word in ['gains', 'losses', 'profit', 'loss']):
                return self._generate_portfolio_pnl_response(portfolio_data)
            
            else:
                return self._generate_general_portfolio_response(portfolio_data)
                
        except Exception as e:
            logger.error(f"Error handling portfolio question: {e}")
            return "I'm having trouble analyzing your portfolio right now. Please try again later."
    
    async def _handle_stock_question(
        self,
        message: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Handle stock-specific questions"""
        try:
            # Extract stock symbols from message
            symbols = getattr(self, '_current_symbols', [])
            
            if not symbols:
                return "Which stock are you asking about? Please mention the stock symbol (e.g., AAPL, MSFT)."
            
            symbol = symbols[0]  # Use first mentioned symbol
            
            # Get stock data
            if self.data_service:
                stock_data = await self.data_service.get_real_time_price(symbol)
                company_info = await self.data_service.get_company_info(symbol)
            else:
                stock_data = None
                company_info = None
            
            message_lower = message.lower()
            
            # Price questions
            if any(word in message_lower for word in ['price', 'cost', 'worth', 'trading at']):
                return self._generate_stock_price_response(symbol, stock_data)
            
            # Analysis questions
            elif any(word in message_lower for word in ['analysis', 'technical', 'indicators']):
                return self._generate_stock_analysis_response(symbol, context)
            
            # Company questions
            elif any(word in message_lower for word in ['company', 'business', 'what does', 'about']):
                return self._generate_company_info_response(symbol, company_info)
            
            else:
                return self._generate_general_stock_response(symbol, stock_data)
                
        except Exception as e:
            logger.error(f"Error handling stock question: {e}")
            return f"I'm having trouble getting information about that stock right now. Please try again later."
    
    async def _handle_recommendation_explanation(
        self,
        message: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Handle recommendation explanation requests"""
        try:
            if not context or 'recommendation' not in context:
                return "I'd be happy to explain recommendations, but I don't see any recent recommendations to discuss. Would you like me to get some current recommendations for you?"
            
            recommendation = context['recommendation']
            symbol = recommendation.get('symbol', 'the stock')
            action = recommendation.get('action', 'HOLD')
            reasoning = recommendation.get('reasoning', 'Based on technical analysis')
            confidence = recommendation.get('confidence', 50)
            
            response = f"Here's why I {action.lower()} {symbol}:\n\n"
            response += f"{reasoning}\n\n"
            response += f"My confidence in this recommendation is {confidence}%. "
            
            if confidence >= 80:
                response += "This is a high-confidence recommendation based on strong technical signals."
            elif confidence >= 60:
                response += "This is a moderate-confidence recommendation with some supporting indicators."
            else:
                response += "This is a low-confidence recommendation - consider it as one factor among many in your decision."
            
            response += "\n\nRemember, this is for informational purposes only and not financial advice. Always do your own research and consider your risk tolerance."
            
            return response
            
        except Exception as e:
            logger.error(f"Error handling recommendation explanation: {e}")
            return "I'm having trouble explaining that recommendation right now. Please try asking about a specific stock or recommendation."
    
    async def _handle_general_finance_question(
        self,
        message: str,
        context: Optional[Dict[str, Any]]
    ) -> str:
        """Handle general finance questions"""
        try:
            message_lower = message.lower()
            
            # Market questions
            if any(word in message_lower for word in ['market', 'markets', 'dow', 'nasdaq', 's&p']):
                return self._generate_market_response()
            
            # Risk questions
            elif any(word in message_lower for word in ['risk', 'risky', 'safe', 'conservative']):
                return self._generate_risk_education_response()
            
            # Trading questions
            elif any(word in message_lower for word in ['trading', 'day trading', 'swing trading']):
                return self._generate_trading_education_response()
            
            # Investment questions
            elif any(word in message_lower for word in ['invest', 'investing', 'investment']):
                return self._generate_investment_education_response()
            
            else:
                return await self._generate_conversational_response(message, "default")
                
        except Exception as e:
            logger.error(f"Error handling general finance question: {e}")
            return "That's a great finance question! I'd recommend doing some research on reputable financial education websites for detailed information."
    
    async def _generate_conversational_response(
        self,
        message: str,
        user_id: str
    ) -> str:
        """Generate general conversational response"""
        try:
            # Get conversation history
            history = self.conversation_history.get(user_id, [])
            
            # Build context
            context = ""
            if history:
                for entry in history[-3:]:  # Last 3 exchanges
                    context += f"User: {entry['user']}\nAssistant: {entry['assistant']}\n"
            
            context += f"User: {message}\nAssistant:"
            
            # Generate response using model
            if self.pipeline:
                try:
                    outputs = self.pipeline(
                        context,
                        max_length=len(context) + 100,
                        num_return_sequences=1,
                        temperature=self.temperature,
                        do_sample=True,
                        pad_token_id=self.tokenizer.eos_token_id if self.tokenizer else None
                    )
                    
                    generated_text = outputs[0]['generated_text']
                    response = generated_text[len(context):].strip()
                    
                    # Clean up response
                    response = response.split('\n')[0]  # Take first line
                    response = response.replace('User:', '').replace('Assistant:', '').strip()
                    
                    if response and len(response) > 10:
                        return response
                        
                except Exception as e:
                    logger.warning(f"Model generation failed: {e}")
            
            # Fallback responses
            return self._get_fallback_response(message)
            
        except Exception as e:
            logger.error(f"Error generating conversational response: {e}")
            return "I'm here to help with your investment questions. What would you like to know about stocks, your portfolio, or the market?"
    
    def _generate_portfolio_performance_response(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate portfolio performance response"""
        total_value = portfolio_data.get('total_value', 0)
        total_gain_loss = portfolio_data.get('total_gain_loss', 0)
        total_gain_loss_percent = portfolio_data.get('total_gain_loss_percent', 0)
        
        response = f"Your portfolio is currently worth ${total_value:,.2f}. "
        
        if total_gain_loss >= 0:
            response += f"You're up ${total_gain_loss:,.2f} ({total_gain_loss_percent:+.2f}%) overall. Great job! 📈"
        else:
            response += f"You're down ${abs(total_gain_loss):,.2f} ({total_gain_loss_percent:.2f}%) overall. Remember, investing is long-term - stay focused on your strategy. 📊"
        
        return response
    
    def _generate_portfolio_positions_response(self, portfolio_data: Dict[str, Any]) -> str:
        """Generate portfolio positions response"""
        positions = portfolio_data.get('positions', [])
        
        if not positions:
            return "You don't have any positions in your portfolio yet. Consider adding some stocks to start tracking your investments!"
        
        response = f"You have {len(positions)} positions in your portfolio:\n\n"
        
        for i, position in enumerate(positions[:5]):  # Show top 5
            symbol = position.get('symbol', 'Unknown')
            quantity = position.get('quantity', 0)
            current_value = position.get('total_value', 0)
            gain_loss_percent = position.get('unrealized_gain_loss_percent', 0)
            
            status = "📈" if gain_loss_percent >= 0 else "📉"
            response += f"{i+1}. {symbol}: {quantity} shares, ${current_value:,.2f} ({gain_loss_percent:+.1f}%) {status}\n"
        
        if len(positions) > 5:
            response += f"\n...and {len(positions) - 5} more positions."
        
        return response
    
    def _get_fallback_response(self, message: str) -> str:
        """Get fallback response when model fails"""
        message_lower = message.lower()
        
        greetings = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        if any(greeting in message_lower for greeting in greetings):
            return "Hello! I'm your AI investment assistant. I can help you understand your portfolio, explain stock recommendations, and answer questions about the market. What would you like to know?"
        
        thanks = ['thank', 'thanks', 'appreciate']
        if any(thank in message_lower for thank in thanks):
            return "You're welcome! I'm here to help with your investment questions anytime."
        
        help_words = ['help', 'what can you do', 'capabilities']
        if any(word in message_lower for word in help_words):
            return "I can help you with:\n• Portfolio analysis and performance\n• Stock information and analysis\n• Explaining investment recommendations\n• General market and finance questions\n• Investment education and tips\n\nWhat would you like to explore?"
        
        return "I'm here to help with your investment questions. You can ask me about your portfolio, specific stocks, market analysis, or general investing topics. What interests you?"
    
    def _update_conversation_history(self, user_id: str, user_message: str, assistant_response: str):
        """Update conversation history"""
        if user_id not in self.conversation_history:
            self.conversation_history[user_id] = []
        
        self.conversation_history[user_id].append({
            'user': user_message,
            'assistant': assistant_response,
            'timestamp': datetime.utcnow().isoformat()
        })
        
        # Keep only recent history
        if len(self.conversation_history[user_id]) > self.max_history_length:
            self.conversation_history[user_id] = self.conversation_history[user_id][-self.max_history_length:]
    
    def _load_financial_terms(self) -> Dict[str, str]:
        """Load financial terms dictionary"""
        return {
            'rsi': 'Relative Strength Index - measures overbought/oversold conditions',
            'macd': 'Moving Average Convergence Divergence - trend-following momentum indicator',
            'pe ratio': 'Price-to-Earnings ratio - valuation metric comparing price to earnings',
            'market cap': 'Market capitalization - total value of company shares',
            'volatility': 'Measure of price fluctuation over time',
            'beta': 'Measure of stock volatility relative to market',
            'dividend yield': 'Annual dividend payment as percentage of stock price',
            'bollinger bands': 'Technical indicator showing price volatility bands',
            'support': 'Price level where stock tends to find buying interest',
            'resistance': 'Price level where stock tends to face selling pressure'
        }
    
    def _generate_market_response(self) -> str:
        """Generate market-related response"""
        return "The stock market can be influenced by many factors including economic data, company earnings, geopolitical events, and investor sentiment. For current market conditions, I'd recommend checking the latest market indices and news. Remember that markets can be volatile in the short term but tend to grow over long periods."
    
    def _generate_risk_education_response(self) -> str:
        """Generate risk education response"""
        return "Investment risk refers to the possibility of losing money or not achieving expected returns. Key types include market risk (overall market decline), company-specific risk, and volatility risk. Generally, higher potential returns come with higher risk. Diversification and long-term investing can help manage risk. Always invest only what you can afford to lose."
    
    def _generate_trading_education_response(self) -> str:
        """Generate trading education response"""
        return "Trading involves buying and selling securities frequently to profit from short-term price movements. Day trading (same-day trades) and swing trading (days to weeks) require significant time, skill, and risk tolerance. Most successful long-term wealth building comes from patient investing rather than frequent trading. Remember: this platform is for educational purposes only."
    
    def _generate_investment_education_response(self) -> str:
        """Generate investment education response"""
        return "Investing is about putting money into assets with the expectation of generating returns over time. Key principles include: start early to benefit from compound growth, diversify across different assets, invest regularly (dollar-cost averaging), and maintain a long-term perspective. Consider your risk tolerance and investment timeline when making decisions."
