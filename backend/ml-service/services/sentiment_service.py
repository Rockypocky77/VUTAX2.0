"""
Sentiment Service for VUTAX 2.0
Handles sentiment analysis for stocks
"""

import asyncio
import aiohttp
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
import re
from textblob import TextBlob
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from utils.logger import setup_logger

logger = setup_logger(__name__)

class SentimentService:
    """
    Service for analyzing stock sentiment from various sources
    """
    
    def __init__(self):
        self.vader_analyzer = SentimentIntensityAnalyzer()
        self.sentiment_cache = {}
        self.cache_ttl = 1800  # 30 minutes
        
        # News sources (in production, you'd use proper news APIs)
        self.news_sources = [
            'https://finance.yahoo.com',
            'https://www.marketwatch.com',
            'https://www.cnbc.com'
        ]
    
    async def get_sentiment(self, symbol: str) -> Dict[str, Any]:
        """
        Get comprehensive sentiment analysis for a stock
        """
        try:
            # Check cache
            cache_key = f"sentiment_{symbol}"
            if cache_key in self.sentiment_cache:
                cached_sentiment, timestamp = self.sentiment_cache[cache_key]
                if (datetime.now() - timestamp).seconds < self.cache_ttl:
                    return cached_sentiment
            
            # Gather sentiment from multiple sources
            sentiment_data = await self._gather_sentiment_data(symbol)
            
            # Analyze and aggregate sentiment
            aggregated_sentiment = self._aggregate_sentiment(sentiment_data)
            
            # Cache the result
            self.sentiment_cache[cache_key] = (aggregated_sentiment, datetime.now())
            
            return aggregated_sentiment
            
        except Exception as e:
            logger.error(f"Error getting sentiment for {symbol}: {e}")
            return self._default_sentiment()
    
    async def _gather_sentiment_data(self, symbol: str) -> Dict[str, List[str]]:
        """
        Gather sentiment data from various sources
        """
        sentiment_data = {
            'news_headlines': [],
            'social_mentions': [],
            'analyst_notes': []
        }
        
        try:
            # In a real implementation, you would:
            # 1. Fetch recent news headlines about the stock
            # 2. Scrape social media mentions (Twitter, Reddit, etc.)
            # 3. Get analyst reports and notes
            
            # For demonstration, we'll simulate some data
            sentiment_data['news_headlines'] = await self._simulate_news_headlines(symbol)
            sentiment_data['social_mentions'] = await self._simulate_social_mentions(symbol)
            sentiment_data['analyst_notes'] = await self._simulate_analyst_notes(symbol)
            
        except Exception as e:
            logger.warning(f"Error gathering sentiment data for {symbol}: {e}")
        
        return sentiment_data
    
    async def _simulate_news_headlines(self, symbol: str) -> List[str]:
        """
        Simulate news headlines for demonstration
        """
        # In production, this would fetch real news headlines
        sample_headlines = [
            f"{symbol} reports strong quarterly earnings, beating expectations",
            f"Analysts upgrade {symbol} price target following positive outlook",
            f"{symbol} announces new product launch, shares rise in pre-market",
            f"Market volatility affects {symbol} along with broader tech sector",
            f"{symbol} CEO discusses growth strategy in recent interview"
        ]
        
        # Return a subset randomly
        import random
        return random.sample(sample_headlines, min(3, len(sample_headlines)))
    
    async def _simulate_social_mentions(self, symbol: str) -> List[str]:
        """
        Simulate social media mentions for demonstration
        """
        sample_mentions = [
            f"Really bullish on {symbol} right now, great fundamentals",
            f"{symbol} looking strong, might add to my position",
            f"Concerned about {symbol} valuation at current levels",
            f"{symbol} has been performing well in my portfolio",
            f"Waiting for a dip to buy more {symbol}"
        ]
        
        import random
        return random.sample(sample_mentions, min(4, len(sample_mentions)))
    
    async def _simulate_analyst_notes(self, symbol: str) -> List[str]:
        """
        Simulate analyst notes for demonstration
        """
        sample_notes = [
            f"Maintain BUY rating on {symbol} with $200 price target",
            f"{symbol} well-positioned for growth in current market environment",
            f"Recommend HOLD on {symbol} pending Q3 earnings results"
        ]
        
        import random
        return random.sample(sample_notes, min(2, len(sample_notes)))
    
    def _aggregate_sentiment(self, sentiment_data: Dict[str, List[str]]) -> Dict[str, Any]:
        """
        Aggregate sentiment from all sources
        """
        try:
            all_texts = []
            source_sentiments = {}
            
            # Analyze sentiment for each source
            for source, texts in sentiment_data.items():
                if texts:
                    source_sentiment = self._analyze_texts(texts)
                    source_sentiments[source] = source_sentiment
                    all_texts.extend(texts)
            
            # Overall sentiment
            overall_sentiment = self._analyze_texts(all_texts) if all_texts else self._neutral_sentiment()
            
            # Calculate weighted sentiment score
            weighted_score = self._calculate_weighted_sentiment(source_sentiments)
            
            return {
                'overall_sentiment': overall_sentiment,
                'source_breakdown': source_sentiments,
                'weighted_score': weighted_score,
                'confidence': self._calculate_sentiment_confidence(source_sentiments),
                'summary': self._generate_sentiment_summary(overall_sentiment, weighted_score),
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error aggregating sentiment: {e}")
            return self._default_sentiment()
    
    def _analyze_texts(self, texts: List[str]) -> Dict[str, Any]:
        """
        Analyze sentiment of a list of texts
        """
        if not texts:
            return self._neutral_sentiment()
        
        # Combine all texts
        combined_text = ' '.join(texts)
        
        # TextBlob analysis
        blob = TextBlob(combined_text)
        textblob_polarity = blob.sentiment.polarity  # -1 to 1
        textblob_subjectivity = blob.sentiment.subjectivity  # 0 to 1
        
        # VADER analysis
        vader_scores = self.vader_analyzer.polarity_scores(combined_text)
        
        # Combine scores
        combined_score = (textblob_polarity + vader_scores['compound']) / 2
        
        # Classify sentiment
        if combined_score >= 0.1:
            classification = 'positive'
        elif combined_score <= -0.1:
            classification = 'negative'
        else:
            classification = 'neutral'
        
        return {
            'classification': classification,
            'score': combined_score,
            'textblob_polarity': textblob_polarity,
            'textblob_subjectivity': textblob_subjectivity,
            'vader_compound': vader_scores['compound'],
            'vader_positive': vader_scores['pos'],
            'vader_negative': vader_scores['neg'],
            'vader_neutral': vader_scores['neu'],
            'text_count': len(texts)
        }
    
    def _calculate_weighted_sentiment(self, source_sentiments: Dict[str, Dict[str, Any]]) -> float:
        """
        Calculate weighted sentiment score across sources
        """
        # Weights for different sources
        weights = {
            'news_headlines': 0.4,
            'analyst_notes': 0.4,
            'social_mentions': 0.2
        }
        
        weighted_sum = 0.0
        total_weight = 0.0
        
        for source, sentiment in source_sentiments.items():
            weight = weights.get(source, 0.1)
            score = sentiment.get('score', 0.0)
            
            weighted_sum += score * weight
            total_weight += weight
        
        return weighted_sum / total_weight if total_weight > 0 else 0.0
    
    def _calculate_sentiment_confidence(self, source_sentiments: Dict[str, Dict[str, Any]]) -> float:
        """
        Calculate confidence in sentiment analysis
        """
        if not source_sentiments:
            return 0.0
        
        # Base confidence on number of sources and agreement
        num_sources = len(source_sentiments)
        
        # Calculate agreement (how similar are the sentiment scores)
        scores = [s.get('score', 0.0) for s in source_sentiments.values()]
        
        if len(scores) <= 1:
            return 0.5
        
        # Standard deviation of scores (lower = more agreement)
        import statistics
        score_std = statistics.stdev(scores) if len(scores) > 1 else 0
        
        # Confidence decreases with higher disagreement
        agreement_factor = max(0, 1 - score_std)
        
        # Confidence increases with more sources
        source_factor = min(1.0, num_sources / 3.0)
        
        return (agreement_factor + source_factor) / 2
    
    def _generate_sentiment_summary(self, overall_sentiment: Dict[str, Any], weighted_score: float) -> str:
        """
        Generate human-readable sentiment summary
        """
        classification = overall_sentiment.get('classification', 'neutral')
        score = abs(weighted_score)
        
        if classification == 'positive':
            if score >= 0.5:
                return "Strongly positive sentiment with high optimism"
            elif score >= 0.2:
                return "Moderately positive sentiment with cautious optimism"
            else:
                return "Slightly positive sentiment with mixed signals"
        elif classification == 'negative':
            if score >= 0.5:
                return "Strongly negative sentiment with significant concerns"
            elif score >= 0.2:
                return "Moderately negative sentiment with some pessimism"
            else:
                return "Slightly negative sentiment with mixed signals"
        else:
            return "Neutral sentiment with balanced perspectives"
    
    def _neutral_sentiment(self) -> Dict[str, Any]:
        """
        Return neutral sentiment data
        """
        return {
            'classification': 'neutral',
            'score': 0.0,
            'textblob_polarity': 0.0,
            'textblob_subjectivity': 0.0,
            'vader_compound': 0.0,
            'vader_positive': 0.33,
            'vader_negative': 0.33,
            'vader_neutral': 0.34,
            'text_count': 0
        }
    
    def _default_sentiment(self) -> Dict[str, Any]:
        """
        Return default sentiment when analysis fails
        """
        return {
            'overall_sentiment': self._neutral_sentiment(),
            'source_breakdown': {},
            'weighted_score': 0.0,
            'confidence': 0.0,
            'summary': "Sentiment analysis unavailable",
            'timestamp': datetime.now().isoformat()
        }
