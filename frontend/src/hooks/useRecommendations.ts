'use client';

import { useQuery } from '@tanstack/react-query';
import { StockRecommendation } from '@/types';
import { mlApi } from '@/lib/api';

export function useRecommendations(riskTier: string = 'regular') {
  const { 
    data: recommendations, 
    isLoading: loading, 
    error,
    refetch
  } = useQuery({
    queryKey: ['recommendations', riskTier],
    queryFn: () => mlApi.getRecommendations(riskTier, 10),
    refetchInterval: 300000, // Refetch every 5 minutes
    staleTime: 240000, // Consider stale after 4 minutes
  });

  // Mock recommendations for testing without ML service
  const mockRecommendations: StockRecommendation[] = [
    {
      symbol: 'AAPL',
      action: 'BUY',
      riskTier: 'regular',
      confidence: 87,
      targetPrice: 185.00,
      stopLoss: 165.00,
      reasoning: 'Strong bullish momentum with RSI showing oversold conditions. MACD crossover suggests potential upward movement.',
      timestamp: new Date().toISOString(),
      validUntil: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    },
    {
      symbol: 'MSFT',
      action: 'HOLD',
      riskTier: 'conservative',
      confidence: 72,
      targetPrice: 390.00,
      stopLoss: 360.00,
      reasoning: 'Consolidating near resistance levels. Wait for clear breakout above $385 before adding positions.',
      timestamp: new Date().toISOString(),
      validUntil: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    },
    {
      symbol: 'TSLA',
      action: 'BUY',
      riskTier: 'high-risk',
      confidence: 78,
      targetPrice: 280.00,
      stopLoss: 230.00,
      reasoning: 'High volatility stock showing strong momentum. Volume surge indicates institutional interest.',
      timestamp: new Date().toISOString(),
      validUntil: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    },
    {
      symbol: 'GOOGL',
      action: 'BUY',
      riskTier: 'regular',
      confidence: 83,
      targetPrice: 155.00,
      stopLoss: 135.00,
      reasoning: 'Breaking above key resistance with strong volume. Technical indicators align for upward move.',
      timestamp: new Date().toISOString(),
      validUntil: new Date(Date.now() + 24 * 60 * 60 * 1000).toISOString()
    }
  ];

  return {
    recommendations: recommendations || mockRecommendations,
    loading: loading && !mockRecommendations,
    error,
    refetch
  };
}
