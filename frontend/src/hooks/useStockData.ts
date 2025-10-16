'use client';

import { useState, useEffect, useCallback } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Stock, MarketStatus, ChartData } from '@/types';
import { stockApi } from '@/lib/api';

export function useStockData(symbol?: string) {
  const [isConnected, setIsConnected] = useState(false);
  const queryClient = useQueryClient();

  // Real-time stock price query
  const { 
    data: stockPrice, 
    isLoading: priceLoading, 
    error: priceError 
  } = useQuery({
    queryKey: ['stock-price', symbol],
    queryFn: () => symbol ? stockApi.getRealTimePrice(symbol) : null,
    enabled: !!symbol,
    refetchInterval: 60000, // Refetch every minute
    staleTime: 30000, // Consider data stale after 30 seconds
  });

  // Market status query
  const { 
    data: marketStatus, 
    isLoading: marketLoading 
  } = useQuery({
    queryKey: ['market-status'],
    queryFn: stockApi.getMarketStatus,
    refetchInterval: 300000, // Refetch every 5 minutes
    staleTime: 240000, // Consider stale after 4 minutes
  });

  // Stock chart data query
  const getChartData = useCallback((
    symbol: string, 
    timeframe: '1d' | '1w' | '1m' | '1y' | '5y' = '1d'
  ) => {
    return useQuery({
      queryKey: ['chart-data', symbol, timeframe],
      queryFn: () => stockApi.getChartData(symbol, timeframe),
      enabled: !!symbol,
      staleTime: timeframe === '1d' ? 60000 : 300000, // 1min for intraday, 5min for others
    });
  }, []);

  // Multiple stocks query
  const { 
    data: multipleStocks, 
    isLoading: multipleLoading 
  } = useQuery({
    queryKey: ['multiple-stocks'],
    queryFn: () => stockApi.getMultipleStocks(['AAPL', 'MSFT', 'GOOGL', 'TSLA']),
    refetchInterval: 60000,
    staleTime: 30000,
  });

  // WebSocket connection for real-time updates
  useEffect(() => {
    if (typeof window === 'undefined') return;

    const wsUrl = process.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:3001';
    let ws: WebSocket;

    const connectWebSocket = () => {
      try {
        ws = new WebSocket(wsUrl);

        ws.onopen = () => {
          console.log('WebSocket connected');
          setIsConnected(true);
          
          // Subscribe to stock updates if symbol is provided
          if (symbol) {
            ws.send(JSON.stringify({
              type: 'subscribe_stocks',
              symbols: [symbol]
            }));
          }
        };

        ws.onmessage = (event) => {
          try {
            const data = JSON.parse(event.data);
            
            if (data.type === 'stock_update') {
              // Update the query cache with new data
              queryClient.setQueryData(
                ['stock-price', data.symbol], 
                data.data
              );
            } else if (data.type === 'market_status') {
              queryClient.setQueryData(['market-status'], data.data);
            }
          } catch (error) {
            console.error('Error parsing WebSocket message:', error);
          }
        };

        ws.onclose = () => {
          console.log('WebSocket disconnected');
          setIsConnected(false);
          
          // Attempt to reconnect after 5 seconds
          setTimeout(connectWebSocket, 5000);
        };

        ws.onerror = (error) => {
          console.error('WebSocket error:', error);
          setIsConnected(false);
        };
      } catch (error) {
        console.error('Failed to connect WebSocket:', error);
        setIsConnected(false);
      }
    };

    connectWebSocket();

    return () => {
      if (ws && ws.readyState === WebSocket.OPEN) {
        ws.close();
      }
    };
  }, [symbol, queryClient]);

  // Subscribe to additional stocks
  const subscribeToStocks = useCallback((symbols: string[]) => {
    // This would send a WebSocket message to subscribe to multiple stocks
    // Implementation depends on WebSocket setup
  }, []);

  // Unsubscribe from stocks
  const unsubscribeFromStocks = useCallback((symbols: string[]) => {
    // This would send a WebSocket message to unsubscribe from stocks
    // Implementation depends on WebSocket setup
  }, []);

  return {
    // Single stock data
    stockPrice,
    priceLoading,
    priceError,
    
    // Market status
    marketStatus,
    marketLoading,
    
    // Multiple stocks
    multipleStocks,
    multipleLoading,
    
    // Chart data function
    getChartData,
    
    // WebSocket status
    isConnected,
    
    // Subscription functions
    subscribeToStocks,
    unsubscribeFromStocks,
  };
}
