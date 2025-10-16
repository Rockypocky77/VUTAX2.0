'use client';

import { useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Portfolio } from '@/types';
import { portfolioApi } from '@/lib/api';

export function usePortfolio() {
  const { 
    data: portfolio, 
    isLoading: loading, 
    error,
    refetch
  } = useQuery({
    queryKey: ['portfolio'],
    queryFn: portfolioApi.getPortfolio,
    refetchInterval: 60000, // Refetch every minute
    staleTime: 30000, // Consider stale after 30 seconds
  });

  // Mock portfolio data for testing without authentication
  const mockPortfolio: Portfolio = {
    id: 'mock-portfolio',
    name: 'Paper Trading Portfolio',
    totalValue: 125430.50,
    totalGainLoss: 15430.50,
    totalGainLossPercent: 13.95,
    cashBalance: 25000.00,
    lastUpdated: new Date().toISOString(),
    positions: [
      {
        symbol: 'AAPL',
        quantity: 50,
        avgCostBasis: 150.00,
        currentPrice: 175.43,
        totalValue: 8771.50,
        unrealizedGainLoss: 1271.50,
        unrealizedGainLossPercent: 16.95,
        dateAdded: '2024-01-15'
      },
      {
        symbol: 'MSFT',
        quantity: 25,
        avgCostBasis: 350.00,
        currentPrice: 378.85,
        totalValue: 9471.25,
        unrealizedGainLoss: 721.25,
        unrealizedGainLossPercent: 8.24,
        dateAdded: '2024-02-01'
      },
      {
        symbol: 'GOOGL',
        quantity: 30,
        avgCostBasis: 130.00,
        currentPrice: 142.56,
        totalValue: 4276.80,
        unrealizedGainLoss: 376.80,
        unrealizedGainLossPercent: 9.66,
        dateAdded: '2024-01-20'
      }
    ]
  };

  return {
    portfolio: portfolio || mockPortfolio, // Use mock data if no real data
    loading: loading && !mockPortfolio, // Don't show loading if we have mock data
    error,
    refetch
  };
}
